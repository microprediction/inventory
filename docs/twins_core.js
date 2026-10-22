/* Coupled twin dealers: the commutative square, live.
 *
 * Left: the imbalanced dealer (seller probability q, carrying cost c).
 * Right: the balanced dealer at carrying cost M(q) c.
 * The theorem: nu_q = nu_bal + delta x, so quotes map as
 * m_down_q = m_down_bal + delta, m_up_q = m_up_bal - delta (equal widths,
 * mid shifted by -delta), and both fill rates scale by D(q) = 1/M(q):
 * the SAME embedded jump chain, with the imbalanced clock slowed by D(q).
 *
 * The coupling is offered only after two independent capped-chain policy
 * iterations have converged, every available quote is strictly positive,
 * and the transformed quotes and actual jump generators agree term by term.
 * Outside that interior region setup() reports why the exact coupling is
 * unavailable and makeSim() refuses to manufacture it.
 */

const TWINS = (() => {
  const F = typeof FOUR !== 'undefined' ? FOUR : require('./fourcorners_core.js');

  function solveCapped(q, cost, eps, N) {
    const P = F.makeProblem(q, cost, eps, N);
    let dev = Infinity;
    for (let iter = 1; iter <= 200; iter++) {
      dev = F.piStep(P);
      if (dev < 1e-12) return { ...P, iter, dev, ok: true };
    }
    return { ...P, iter: 200, dev, ok: false };
  }

  function setup({ q, w = 1, eps = 0.15, a = 0.001, N = 6 }) {
    if (w !== 1) throw new Error('the capped policy solver currently uses w = 1');
    const cost = x => a * x * x;
    const M = 1 / (2 * Math.sqrt(q * (1 - q)));
    const D = 1 / M;
    const delta = 0.5 * w * Math.log(q / (1 - q));
    const imb = solveCapped(q, cost, eps, N);
    const bal = solveCapped(0.5, x => M * cost(x), eps, N);
    const n = 2 * N + 1, i0 = N;

    const Qi = { md: imb.md, mu: imb.mu };
    const Qb = { md: bal.md, mu: bal.mu };

    // Verify the quote map and both directional generator rates, including the
    // one-sided cap states.  This is evidence for the coupling; it is not
    // imposed by the simulator.
    let devQuote = 0, devW = 0, devMid = 0, devRate = 0;
    let minQuote = Infinity, floorCount = 0;
    for (let i = 0; i < n; i++) {
      if (i < n - 1) {
        devQuote = Math.max(devQuote, Math.abs(Qi.md[i] - (Qb.md[i] + delta)));
        const ri = q * Math.exp(-Qi.md[i] / w);
        const rb = 0.5 * Math.exp(-Qb.md[i] / w);
        devRate = Math.max(devRate, Math.abs(ri - D * rb));
        minQuote = Math.min(minQuote, Qi.md[i], Qb.md[i]);
        if (Qi.md[i] <= 1e-12 || Qb.md[i] <= 1e-12) floorCount += 1;
      }
      if (i > 0) {
        devQuote = Math.max(devQuote, Math.abs(Qi.mu[i] - (Qb.mu[i] - delta)));
        const ri = (1 - q) * Math.exp(-Qi.mu[i] / w);
        const rb = 0.5 * Math.exp(-Qb.mu[i] / w);
        devRate = Math.max(devRate, Math.abs(ri - D * rb));
        minQuote = Math.min(minQuote, Qi.mu[i], Qb.mu[i]);
        if (Qi.mu[i] <= 1e-12 || Qb.mu[i] <= 1e-12) floorCount += 1;
      }
    }
    for (let i = 1; i < n - 1; i++) {
      devW = Math.max(devW, Math.abs((Qi.md[i] + Qi.mu[i]) - (Qb.md[i] + Qb.mu[i])));
      devMid = Math.max(devMid, Math.abs((Qi.mu[i] - Qi.md[i]) / 2 - ((Qb.mu[i] - Qb.md[i]) / 2 - delta)));
    }

    const exact = imb.ok && bal.ok && floorCount === 0
      && devQuote < 1e-10 && devRate < 1e-10;
    let reason = '';
    if (!imb.ok || !bal.ok) reason = 'capped policy iteration did not converge';
    else if (floorCount) reason = `${floorCount} available quote(s) bind at zero`;
    else if (devQuote >= 1e-10) reason = 'the capped quote map is outside numerical tolerance';
    else if (devRate >= 1e-10) reason = 'the two actual generators do not scale term by term';

    return { q, w, eps, N, n, i0, cost, M, D, delta, imb, bal, Qi, Qb,
             devQuote, devW, devMid, devRate, minQuote, floorCount,
             exact, reason };
  }

  function makeSim(S) {
    if (!S.exact) throw new Error(`exact coupling unavailable: ${S.reason}`);
    const st = {
      i: S.i0,                       // shared inventory index
      tBal: 0, tImb: 0,              // the two calendar clocks
      trades: 0, buys: 0,
      carryBal: 0, carryImb: 0,      // carry paid, each in its own clock
      occBal: new Float64Array(S.n), // calendar-time occupancy
      occImb: new Float64Array(S.n),
      path: [S.i0],
    };
    st.step = () => {
      const i = st.i, x = i - S.i0;
      // Balanced per-arrival jump rates.  setup() has already verified that
      // the independently optimized imbalanced rates are exactly D times
      // these rates, direction by direction and at both caps.
      const pd = i < S.n - 1 ? 0.5 * Math.exp(-S.Qb.md[i] / S.w) : 0;
      const pu = i > 0 ? 0.5 * Math.exp(-S.Qb.mu[i] / S.w) : 0;
      const rate = pd + pu;                       // balanced jump rate (tau = 1)
      const e = -Math.log(1 - Math.random());     // one shared exponential draw
      const dtB = e / rate, dtI = e / (rate * S.D);
      st.tBal += dtB; st.tImb += dtI;
      st.occBal[i] += dtB; st.occImb[i] += dtI;
      st.carryBal += S.M * S.cost(x) * dtB;
      st.carryImb += S.cost(x) * dtI;
      const up = Math.random() < pd / rate;       // shared jump direction
      st.i += up ? 1 : -1;
      st.trades += 1; if (up) st.buys += 1;
      st.path.push(st.i);
      if (st.path.length > 240) st.path.shift();
    };
    return st;
  }

  return { setup, makeSim };
})();
if (typeof module !== 'undefined') module.exports = TWINS;
