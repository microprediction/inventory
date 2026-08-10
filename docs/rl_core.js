/* Reinforcement learning on the sealed-bid market making environment, with and
 * without the imbalance symmetry, plus the inverse problem (inferring the
 * dealer's inventory cost from observed quotes).
 *
 * Forward: tabular Q-learning over discretized markups. The SYMMETRY agent
 * keeps ONE Q-table in the balanced frame and maps actions through the skew
 * shift delta(q) = (w/2) log(q/(1-q)); experience from every flow regime
 * trains the same table (exact to first order in q - 1/2; the residual gamma
 * and M(q) effects are second order). The BASELINE agent runs the identical
 * algorithm with a separate table per regime. The ORACLE quotes the exact
 * optimal policy from the solved indifference cost (mm_core.js).
 *
 * Inverse: watch a dealer's noisy quotes across regimes. Skew observations
 * satisfy S_q(x) = S_bal(x) + delta(q); de-tilting pools every regime into
 * one balanced-frame estimate (error down by sqrt(#regimes)), versus
 * estimating each regime separately.
 */

const RL = (() => {

  function makeEnv({ w = 1, c2 = 0.01, N = 8, regimes = [0.40, 0.50, 0.60, 0.70], block = 400, seed = 12345 }) {
    let s = seed >>> 0;
    const rnd = () => (s = (s * 1664525 + 1013904223) >>> 0) / 4294967296;
    return {
      w, c2, N, regimes, block, rnd,
      t: 0,
      regime() { return this.regimes[Math.floor(this.t / this.block) % this.regimes.length]; },
      cost(x) { return this.c2 * x * x; },
      // one enquiry: returns {q, isSeller, Z}
      enquiry() {
        const q = this.regime();
        const isSeller = this.rnd() < q;
        const Z = -this.w * Math.log(1 - this.rnd());
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

  // one tabular Q-learner: Q[side][x+N][action]
  function makeTable(N, nA) {
    const mk = () => Array.from({ length: 2 * N + 1 }, () => new Float64Array(nA).fill(1.0));
    return { dn: mk(), up: mk(), counts: { dn: mk(), up: mk() } };
  }

  function makeLearner({ env, symmetry, gammaD = 0.97, actions }) {
    const nA = actions.length;
    const tables = {}; // keyed by regime for baseline; single key 'bal' for symmetry
    const key = q => symmetry ? 'bal' : String(q);
    const ensure = q => tables[key(q)] || (tables[key(q)] = makeTable(env.N, nA));
    let steps = 0;

    function greedy(row) {
      let bi = 0;
      for (let i = 1; i < row.length; i++) if (row[i] > row[bi]) bi = i;
      return bi;
    }

    return {
      x: 0, pnl: 0, tables,
      eps() { return Math.max(0.02, 0.5 * Math.exp(-steps / 6000)); },
      act(q, isSeller) {
        const T = ensure(q);
        const side = isSeller ? 'dn' : 'up';
        const row = T[side][this.x + env.N];
        const a = (env.rnd() < this.eps()) ? Math.floor(env.rnd() * nA) : greedy(row);
        const d = symmetry ? delta(q, env.w) : 0;
        // balanced-frame action -> executed markup: buy side +delta, sell side -delta
        const m = Math.max(0.01, actions[a] + (isSeller ? d : -d));
        return { a, m, side, T };
      },
      learn({ q, isSeller, Z }) {
        const { a, m, side, T } = this.act(q, isSeller);
        const atLimit = isSeller ? this.x >= env.N : this.x <= -env.N;
        const win = !atLimit && m < Z;
        const x1 = win ? this.x + (isSeller ? 1 : -1) : this.x;
        // reward in the LEARNING frame: symmetry agent books the balanced-frame
        // margin (the delta part of the executed margin is offset, to first
        // order, by the tilted win odds -- that is the theorem)
        const margin = win ? (symmetry ? actions[a] : m) : 0;
        const r = margin - env.cost(x1);
        this.pnl += (win ? m : 0) - env.cost(x1); // realized P&L is always raw
        const row = T[side][this.x + env.N];
        const nextBest = Math.max(
          Math.max(...T.dn[x1 + env.N]),
          Math.max(...T.up[x1 + env.N]));
        const c = ++T.counts[side][this.x + env.N][a];
        const alpha = 0.6 / (1 + 0.03 * c);
        row[a] += alpha * (r + gammaD * nextBest - row[a]);
        this.x = x1;
        steps++;
        return win;
      },
    };
  }

  // exact optimal dealer (recomputes policy per regime via MM.solve, cached)
  function makeOracle({ env, MM }) {
    const cache = {};
    const policy = q => cache[q] || (cache[q] = MM.solve({ q, w: env.w, N: env.N, cost: x => env.cost(x) }));
    return {
      x: 0, pnl: 0,
      learn({ q, isSeller, Z }) {
        const sol = policy(q);
        const i = Math.max(1, Math.min(2 * env.N - 1, this.x + env.N));
        const S = MM.slope(sol.nu, i), C = MM.convexity(sol.nu, i);
        const m = Math.max(0.01, env.w + C + (isSeller ? S : -S));
        const atLimit = isSeller ? this.x >= env.N : this.x <= -env.N;
        const win = !atLimit && m < Z;
        if (win) this.x += isSeller ? 1 : -1;
        this.pnl += (win ? m : 0) - env.cost(this.x);
        return win;
      },
    };
  }

  /* ---- inverse problem ---- */

  // Watch the oracle quote with noise; estimate the balanced skew curve
  // pooled (de-tilted, all regimes) vs per-regime (only matching regime).
  function irlRun({ env, MM, nObs, noise = 0.25, targetQ }) {
    const cache = {};
    const policy = q => cache[q] || (cache[q] = MM.solve({ q, w: env.w, N: env.N, cost: x => env.cost(x) }));
    // true balanced skew curve (the estimand, in the balanced frame)
    const balSol = policy(targetQ);
    const trueS = [];
    for (let i = 1; i < 2 * env.N; i++) trueS.push(MM.slope(balSol.nu, i));

    const pooled = { sum: new Float64Array(2 * env.N + 1), n: new Float64Array(2 * env.N + 1) };
    const perReg = { sum: new Float64Array(2 * env.N + 1), n: new Float64Array(2 * env.N + 1) };
    let x = 0;
    const gauss = () => { // Box-Muller on env.rnd
      const u = Math.max(env.rnd(), 1e-12), v = env.rnd();
      return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
    };
    for (let k = 0; k < nObs; k++) {
      const { q, isSeller, Z } = env.enquiry();
      const sol = policy(q);
      const i = Math.max(1, Math.min(2 * env.N - 1, x + env.N));
      const S = MM.slope(sol.nu, i), C = MM.convexity(sol.nu, i);
      // observe BOTH quotes of the dealer at this state, with noise
      const mDn = env.w + C + S + noise * gauss();
      const mUp = env.w + C - S + noise * gauss();
      const skewObs = (mDn - mUp) / 2; // = S + noise
      // pooled: de-tilt to balanced frame, then re-tilt to the target regime
      const sBalObs = skewObs - delta(q, env.w);
      pooled.sum[i] += sBalObs + delta(targetQ, env.w); pooled.n[i]++;
      if (q === targetQ) { perReg.sum[i] += skewObs; perReg.n[i]++; }
      // dealer trades per her policy; inventory random-walks through states
      const m = isSeller ? mDn : mUp;
      const atLimit = isSeller ? x >= env.N : x <= -env.N;
      if (!atLimit && Math.max(0.01, m) < Z) x += isSeller ? 1 : -1;
    }
    // evaluate both estimators on the same support: states where even the
    // per-regime estimator has at least 3 observations (conservative for us)
    const rmse = est => {
      let se = 0, n = 0;
      for (let i = 1; i < 2 * env.N; i++) {
        if (perReg.n[i] >= 3 && est.n[i] > 0) {
          const e = est.sum[i] / est.n[i] - trueS[i - 1]; se += e * e; n++;
        }
      }
      return n ? Math.sqrt(se / n) : NaN;
    };
    return { pooledRMSE: rmse(pooled), perRegimeRMSE: rmse(perReg),
             pooledCurve: pooled, perRegimeCurve: perReg, trueS };
  }

  return { makeEnv, makeActions, makeLearner, makeOracle, irlRun, delta };
})();

if (typeof module !== 'undefined') module.exports = RL;
