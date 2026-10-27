/* Reinforcement learning on the sealed-bid market making environment, with and
 * without the imbalance symmetry, plus the inverse problem (inferring the
 * dealer's inventory cost from observed quotes).
 *
 * Two generative models for the best competing quote:
 *   'exponential' — constant hazard; the paper's symmetry holds exactly, but
 *                   it maps regime q to the balanced problem at carry M(q)c,
 *                   so regimes with different M(q) are different problems.
 *   'logistic'    — an illustrative increasing-hazard curve; the symmetry is
 *                   only approximate.
 *
 * Forward learners (identical tabular Q-learning throughout):
 *   'per'    — a separate table per flow regime (no symmetry).
 *   'sym'    — ONE table in the balanced frame, actions mapped through the
 *              skew shift delta(q) only. This is a heuristic even under
 *              'exponential': it ignores the carry multiplier M(q), which
 *              differs from 1 at second order in q - 1/2.
 *   'robust' — the sym table PLUS a small per-regime residual table that
 *              absorbs whatever the symmetry gets wrong. Under the exact
 *              model the residual stays near zero and costs little; under
 *              the misspecified model it removes the bias.
 *
 * Inverse estimators for the dealer's skew curve S(x):
 *   per-regime — only observations from the target regime.
 *   pooled     — de-tilt every regime's observations by delta(q).
 * The estimand is the dealer's submitted quote skew (m_dn - m_up)/2 at each
 * inventory, computed from her model-optimal quotes. Under 'exponential'
 * it equals the value-function slope S(x) wherever no quote is floored.
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
      // invert the optimal-quote map: the strike K whose optimal quote is m.
      // First-order condition (m - K) * hazard(m) = 1.
      strikeOf(m, q) {
        if (this.winCurve === 'exponential') return m - this.w;
        const F = 1 - this.survQ(m, q);
        return m - this.sscale / Math.max(F, 1e-12);
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
    // Continuation value of inventory index xi before the next enquiry's
    // direction is known: the dealer chooses the quote, not the side.
    function cont(qnext, xi) {
      const mx = side => { const row = qval(qnext, side, xi); let b = -Infinity; for (let i = 0; i < nA; i++) if (row[i] > b) b = row[i]; return b; };
      return qnext * mx('dn') + (1 - qnext) * mx('up');
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
        // env.enquiry() has already advanced the clock, so env.regime() is the
        // regime of the next enquiry (it changes at block boundaries)
        const td = r + gammaD * cont(env.regime(), x1 + env.N) - row[a];
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

  // Exact average-reward optimum on the actual capped inventory chain.  The
  // public demo's generic MM.solve uses artificial third-difference endpoint
  // equations; those are useful for interior algebra but are not the Bellman
  // equations at a hard inventory cap.
  function solveCapped(env, q) {
    const n = 2 * env.N + 1, i0 = env.N, floor = 0.01;
    const md = Array.from({ length: n }, (_, i) => i < n - 1 ? env.mstar(0, q) : NaN);
    const mu = Array.from({ length: n }, (_, i) => i > 0 ? env.mstar(0, q) : NaN);

    function gauss(A, b) {
      const m = b.length, M = A.map((row, i) => row.concat([b[i]]));
      for (let c = 0; c < m; c++) {
        let p = c;
        for (let r = c + 1; r < m; r++) if (Math.abs(M[r][c]) > Math.abs(M[p][c])) p = r;
        [M[c], M[p]] = [M[p], M[c]];
        for (let r = 0; r < m; r++) {
          if (r === c) continue;
          const f = M[r][c] / M[c][c];
          for (let k = c; k <= m; k++) M[r][k] -= f * M[c][k];
        }
      }
      return M.map((row, i) => row[m] / row[i]);
    }

    function evaluate() {
      const A = [], b = [];
      for (let i = 0; i < n; i++) {
        const up = i < n - 1 ? q * env.survQ(md[i], q) : 0;
        const dn = i > 0 ? (1 - q) * env.survQ(mu[i], q) : 0;
        const row = new Array(n + 1).fill(0);
        row[i] = up + dn;
        if (i < n - 1) row[i + 1] -= up;
        if (i > 0) row[i - 1] -= dn;
        row[n] = 1;
        A.push(row);
        b.push((i < n - 1 ? up * md[i] : 0)
             + (i > 0 ? dn * mu[i] : 0) - env.cost(i - i0));
      }
      const pin = new Array(n + 1).fill(0); pin[i0] = 1;
      A.push(pin); b.push(0);
      const z = gauss(A, b);
      return { h: z.slice(0, n), gain: z[n] };
    }

    let last;
    for (let iter = 0; iter < 200; iter++) {
      last = evaluate();
      let dev = 0;
      for (let i = 0; i < n; i++) {
        if (i < n - 1) {
          const m = Math.max(floor, env.mstar(last.h[i] - last.h[i + 1], q));
          dev = Math.max(dev, Math.abs(m - md[i])); md[i] = m;
        }
        if (i > 0) {
          const m = Math.max(floor, env.mstar(last.h[i] - last.h[i - 1], q));
          dev = Math.max(dev, Math.abs(m - mu[i])); mu[i] = m;
        }
      }
      if (dev < 1e-13) {
        last = evaluate();
        return { md, mu, h: last.h, gain: last.gain, iterations: iter + 1 };
      }
    }
    throw new Error(`capped policy iteration failed at q=${q}`);
  }

  function makeOracle({ env }) {
    const cache = {};
    const policy = q => cache[q] || (cache[q] = solveCapped(env, q));
    return {
      x: 0, pnl: 0,
      learn({ q, isSeller, Z }) {
        const sol = policy(q);
        const atLimit = isSeller ? this.x >= env.N : this.x <= -env.N;
        const i = this.x + env.N;
        const m = atLimit ? Infinity : (isSeller ? sol.md[i] : sol.mu[i]);
        const win = m < Z;
        if (win) this.x += isSeller ? 1 : -1;
        this.pnl += (win ? m : 0) - env.cost(this.x);
        return win;
      },
    };
  }

  /* ---- inverse problem ---- */

  function irlRun({ env, nObs, noise = 0.4, targetQ }) {
    const cache = {};
    const policy = q => cache[q] || (cache[q] = solveCapped(env, q));
    // optimal submitted quotes and their skew, at interior inventory index i
    const optQuotes = (sol, i) => [sol.md[i], sol.mu[i]];
    const tSol = policy(targetQ);
    const trueS = [];
    for (let i = 1; i < 2 * env.N; i++) { const [a, b] = optQuotes(tSol, i); trueS.push((a - b) / 2); }

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
      // the dealer submits her model-optimal quotes and fills use those;
      // the observer sees them with independent measurement noise
      const [mDn, mUp] = optQuotes(sol, i);
      const skewObs = ((mDn + noise * gauss()) - (mUp + noise * gauss())) / 2;
      const st = byReg[q];
      st.sum[i] += skewObs - delta(q, env.w); st.n[i]++;  // balanced frame
      const m = isSeller ? mDn : mUp;
      const atLimit = isSeller ? x >= env.N : x <= -env.N;
      if (!atLimit && m < Z) x += isSeller ? 1 : -1;
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

  return { makeEnv, makeActions, makeLearner, makeOracle, irlRun, delta, solveCapped };
})();

if (typeof module !== 'undefined') module.exports = RL;
