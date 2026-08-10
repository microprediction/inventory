/* Reinforcement learning on the sealed-bid market making environment, with and
 * without the imbalance symmetry, plus the inverse problem (inferring the
 * dealer's inventory cost from observed quotes).
 *
 * Two generative models for the best competing quote:
 *   'exponential' — constant hazard; the paper's symmetry is EXACT (to first
 *                   order across regimes via the delta shift).
 *   'logistic'    — increasing hazard, the shape Fermanian–Guéant–Pu fit to
 *                   real RFQ win curves; the symmetry is only approximate.
 *
 * Forward learners (identical tabular Q-learning throughout):
 *   'per'    — a separate table per flow regime (no symmetry).
 *   'sym'    — ONE table in the balanced frame, actions mapped through the
 *              skew shift delta(q); exact under 'exponential', slightly
 *              misspecified under 'logistic'.
 *   'robust' — the sym table PLUS a small per-regime residual table that
 *              absorbs whatever the symmetry gets wrong. Under the exact
 *              model the residual stays near zero and costs little; under
 *              the misspecified model it removes the bias.
 *
 * Inverse estimators for the dealer's skew curve S(x):
 *   per-regime — only observations from the target regime.
 *   pooled     — de-tilt every regime's observations by delta(q).
 *   shrunk     — random-effects partial pooling: the between-regime
 *                dispersion of de-tilted means estimates the symmetry
 *                violation tau^2, and the shrinkage weight sets itself.
 */

const RL = (() => {

  function makeEnv({ w = 1, c2 = 0.01, N = 8, regimes = [0.40, 0.50, 0.60, 0.70],
                     block = 400, seed = 12345, winCurve = 'exponential',
                     mu = 1.1, sscale = 0.35, crowd = 0.8 }) {
    let s = seed >>> 0;
    const rnd = () => (s = (s * 1664525 + 1013904223) >>> 0) / 4294967296;
    return {
      w, c2, N, regimes, block, rnd, winCurve, mu, sscale, crowd,
      t: 0,
      regime() { return this.regimes[Math.floor(this.t / this.block) % this.regimes.length]; },
      cost(x) { return this.c2 * x * x; },
      drawZ(q) {
        const u = Math.min(Math.max(this.rnd(), 1e-12), 1 - 1e-12);
        return this.winCurve === 'logistic'
          ? this.muOf(q) + this.sscale * Math.log(u / (1 - u))
          : -this.w * Math.log(1 - u);
      },
      // competitors crowd the flow-heavy side: the win-curve location
      // tightens in imbalanced regimes (regime-dependent, both sides)
      muOf(q) { return this.mu - this.crowd * (q - 0.5) * (q - 0.5) * 4; },
      survQ(m, q) {
        return this.winCurve === 'logistic'
          ? 1 / (1 + Math.exp((m - this.muOf(q)) / this.sscale))
          : Math.exp(-m / this.w);
      },
      mstar(K, q, side) {
        if (this.winCurve === 'exponential') return Math.max(this.w + K, 0.01);
        const mu = this.muOf(q);
        let lo = Math.max(K, mu - 14 * this.sscale), hi = mu + 20 * this.sscale;
        const g = m => (m - K) * (1 - this.survQ(m, q)) / this.sscale - 1;
        if (g(hi) < 0) return hi;
        for (let it = 0; it < 60; it++) {
          const mid = (lo + hi) / 2;
          if (g(mid) < 0) lo = mid; else hi = mid;
        }
        return Math.max((lo + hi) / 2, 0.01);
      },
      G(K, q) {
        if (this.winCurve === 'exponential') return this.w * Math.exp(-1 - K / this.w);
        const m = this.mstar(K, q);
        return Math.max((m - K) * this.survQ(m, q), 0);
      },
      enquiry() {
        const q = this.regime();
        const isSeller = this.rnd() < q;
        const Z = this.drawZ(q);
        this.t++;
        return { q, isSeller, Z };
      },
    };
  }

  function delta(q, w) { return 0.5 * w * Math.log(q / (1 - q)); }

  /* ---- forward learning ---- */

  function makeActions(lo = 0.1, hi = 3.0, n = 15) {
    return Array.from({ length: n }, (_, i) => lo + (hi - lo) * i / (n - 1));
  }

  function makeTable(N, nA, init = 1.0) {
    const mk = v => Array.from({ length: 2 * N + 1 }, () => new Float64Array(nA).fill(v));
    return { dn: mk(init), up: mk(init), cdn: mk(0), cup: mk(0) };
  }

  // mode: 'per' | 'sym' | 'robust'
  function makeLearner({ env, mode, gammaD = 0.97, actions, resRate = 0.5 }) {
    const nA = actions.length;
    const shared = (mode !== 'per') ? makeTable(env.N, nA) : null;
    const residual = {}; // per regime, for 'per' (full tables) and 'robust' (residuals)
    const resFor = q => residual[q] || (residual[q] = makeTable(env.N, nA, mode === 'per' ? 1.0 : 0.0));
    let steps = 0;

    function qval(qreg, side, xi) {
      const out = new Float64Array(nA);
      if (shared) { const row = (side === 'dn' ? shared.dn : shared.up)[xi]; for (let i = 0; i < nA; i++) out[i] += row[i]; }
      if (mode !== 'sym') { const row = (side === 'dn' ? resFor(qreg).dn : resFor(qreg).up)[xi]; for (let i = 0; i < nA; i++) out[i] += row[i]; }
      return out;
    }
    function best(qreg, xi) {
      let b = -Infinity;
      for (const side of ['dn', 'up']) {
        const row = qval(qreg, side, xi);
        for (let i = 0; i < nA; i++) if (row[i] > b) b = row[i];
      }
      return b;
    }

    return {
      x: 0, pnl: 0,
      eps() { return Math.max(0.02, 0.5 * Math.exp(-steps / 6000)); },
      learn({ q, isSeller, Z }) {
        const side = isSeller ? 'dn' : 'up';
        const xi = this.x + env.N;
        const row = qval(q, side, xi);
        let a = 0;
        if (env.rnd() < this.eps()) a = Math.floor(env.rnd() * nA);
        else for (let i = 1; i < nA; i++) if (row[i] > row[a]) a = i;
        const useDelta = (mode !== 'per');
        const d = useDelta ? delta(q, env.w) : 0;
        const m = Math.max(0.01, actions[a] + (isSeller ? d : -d));
        const atLimit = isSeller ? this.x >= env.N : this.x <= -env.N;
        const win = !atLimit && m < Z;
        const x1 = win ? this.x + (isSeller ? 1 : -1) : this.x;
        // learning-frame margin: balanced-frame action for frame-mapped modes
        const margin = win ? (useDelta ? actions[a] : m) : 0;
        const r = margin - env.cost(x1);
        this.pnl += (win ? m : 0) - env.cost(x1);
        const td = r + gammaD * best(q, x1 + env.N) - row[a];
        if (mode === 'per') {
          const T = resFor(q), c = ++((side === 'dn' ? T.cdn : T.cup)[xi][a]);
          (side === 'dn' ? T.dn : T.up)[xi][a] += (0.6 / (1 + 0.03 * c)) * td;
        } else {
          const c = ++((side === 'dn' ? shared.cdn : shared.cup)[xi][a]);
          const alpha = 0.6 / (1 + 0.03 * c);
          (side === 'dn' ? shared.dn : shared.up)[xi][a] += alpha * td;
          if (mode === 'robust') {
            const T = resFor(q);
            (side === 'dn' ? T.dn : T.up)[xi][a] += resRate * alpha * td;
          }
        }
        this.x = x1;
        steps++;
        return win;
      },
    };
  }

  // exact optimal dealer for the env's actual win curve (custom G into MM.solve)
  function makeOracle({ env, MM }) {
    const cache = {};
    const policy = q => cache[q] || (cache[q] = MM.solve({
      q, w: env.w, N: env.N, cost: x => env.cost(x), G: K => env.G(K, q) }));
    return {
      x: 0, pnl: 0,
      learn({ q, isSeller, Z }) {
        const sol = policy(q);
        const i = Math.max(1, Math.min(2 * env.N - 1, this.x + env.N));
        const S = MM.slope(sol.nu, i), C = MM.convexity(sol.nu, i);
        const K = C + (isSeller ? S : -S);
        const m = env.mstar(K, q);
        const atLimit = isSeller ? this.x >= env.N : this.x <= -env.N;
        const win = !atLimit && m < Z;
        if (win) this.x += isSeller ? 1 : -1;
        this.pnl += (win ? m : 0) - env.cost(this.x);
        return win;
      },
    };
  }

  /* ---- inverse problem ---- */

  function irlRun({ env, MM, nObs, noise = 0.4, targetQ }) {
    const cache = {};
    const policy = q => cache[q] || (cache[q] = MM.solve({
      q, w: env.w, N: env.N, cost: x => env.cost(x), G: K => env.G(K, q) }));
    const tSol = policy(targetQ);
    const trueS = [];
    for (let i = 1; i < 2 * env.N; i++) trueS.push(MM.slope(tSol.nu, i));

    const nStates = 2 * env.N + 1;
    // per (regime, state): sum and count of de-tilted skew observations
    const byReg = {};
    for (const q of env.regimes) byReg[q] = { sum: new Float64Array(nStates), n: new Float64Array(nStates) };
    let x = 0;
    const gauss = () => {
      const u = Math.max(env.rnd(), 1e-12), v = env.rnd();
      return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
    };
    for (let k2 = 0; k2 < nObs; k2++) {
      const { q, isSeller, Z } = env.enquiry();
      const sol = policy(q);
      const i = Math.max(1, Math.min(2 * env.N - 1, x + env.N));
      const S = MM.slope(sol.nu, i), C = MM.convexity(sol.nu, i);
      const mDn = env.w + C + S + noise * gauss();
      const mUp = env.w + C - S + noise * gauss();
      const skewObs = (mDn - mUp) / 2;
      const st = byReg[q];
      st.sum[i] += skewObs - delta(q, env.w); st.n[i]++;  // balanced frame
      const m = isSeller ? mDn : mUp;
      const atLimit = isSeller ? x >= env.N : x <= -env.N;
      if (!atLimit && Math.max(0.01, m) < Z) x += isSeller ? 1 : -1;
    }

    const dT = delta(targetQ, env.w);
    const sig2 = noise * noise / 2;  // variance of one skew observation
    const est = { pooled: [], per: [], shrunk: [] };
    const errAt = i => {
      const tgt = byReg[targetQ];
      // pooled mean over all regimes (balanced frame)
      let S1 = 0, n1 = 0, means = [], ns = [];
      for (const q of env.regimes) {
        const st = byReg[q];
        if (st.n[i] > 0) { means.push(st.sum[i] / st.n[i]); ns.push(st.n[i]); S1 += st.sum[i]; n1 += st.n[i]; }
      }
      if (!n1 || tgt.n[i] < 3) return null;
      const pooled = S1 / n1 + dT;
      const per = tgt.sum[i] / tgt.n[i] + dT;
      // random-effects: between-regime dispersion beyond sampling noise
      const grand = S1 / n1;
      let btw = 0;
      for (let j2 = 0; j2 < means.length; j2++) btw += (means[j2] - grand) ** 2;
      btw = means.length > 1 ? btw / (means.length - 1) : 0;
      const meanSampVar = means.length ? ns.reduce((a, n2) => a + sig2 / n2, 0) / ns.length : 0;
      const tau2 = Math.max(0, btw - meanSampVar);
      const lam = tau2 / (tau2 + sig2 / tgt.n[i]);   // weight on per-regime
      const shrunk = lam * per + (1 - lam) * pooled;
      return { pooled, per, shrunk, i };
    };
    let se = { pooled: 0, per: 0, shrunk: 0 }, nn = 0;
    for (let i = 1; i < 2 * env.N; i++) {
      const e = errAt(i);
      if (!e) continue;
      const t = trueS[i - 1];
      se.pooled += (e.pooled - t) ** 2; se.per += (e.per - t) ** 2; se.shrunk += (e.shrunk - t) ** 2;
      nn++;
    }
    const rmse = v => nn ? Math.sqrt(v / nn) : NaN;
    return { pooledRMSE: rmse(se.pooled), perRegimeRMSE: rmse(se.per), shrunkRMSE: rmse(se.shrunk) };
  }

  return { makeEnv, makeActions, makeLearner, makeOracle, irlRun, delta };
})();

if (typeof module !== 'undefined') module.exports = RL;
