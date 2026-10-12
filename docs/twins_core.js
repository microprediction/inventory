/* Coupled twin dealers: the commutative square, live.
 *
 * Left: the imbalanced dealer (seller probability q, carrying cost c).
 * Right: the balanced dealer at carrying cost M(q) c.
 * The theorem: nu_q = nu_bal + delta x, so quotes map as
 * m_down_q = m_down_bal + delta, m_up_q = m_up_bal - delta (equal widths,
 * mid shifted by -delta), and both fill rates scale by D(q) = 1/M(q):
 * the SAME embedded jump chain, with the imbalanced clock slowed by D(q).
 *
 * Coupling: one inventory path drives both panels; sojourn times share one
 * exponential draw, the imbalanced sojourn stretched by exactly 1/D(q).
 * Carry paid per transition (c(x) * sojourn_imb vs M c(x) * sojourn_bal)
 * is then identical: the multiplier is the clock, seen from the cost side.
 */

const TWINS = (() => {
  function setup({ q, w = 1, eps = 0, a = 0.01, N = 8 }) {
    const cost = x => a * x * x;
    const M = 1 / (2 * Math.sqrt(q * (1 - q)));
    const D = 1 / M;
    const delta = 0.5 * w * Math.log(q / (1 - q));
    const imb = MM.solve({ q, w, eps, N, cost });
    const bal = MM.solve({ q: 0.5, w, eps, N, cost: x => M * cost(x) });
    const n = 2 * N + 1, i0 = N;

    // quotes per interior state: [markdown for buying, markup for selling]
    const quotes = nu => {
      const md = [], mu = [];
      for (let i = 0; i < n; i++) {
        md.push(i < n - 1 ? w + eps + (nu[i + 1] - nu[i]) : NaN);
        mu.push(i > 0 ? w + eps + (nu[i - 1] - nu[i]) : NaN);
      }
      return { md, mu };
    };
    const Qi = quotes(imb.nu), Qb = quotes(bal.nu);

    // identity readouts (solver precision, computed from two independent solves)
    let devNu = 0, devW = 0, devMid = 0;
    for (let i = 1; i < n - 1; i++) {
      devNu = Math.max(devNu, Math.abs(imb.nu[i] - (bal.nu[i] + delta * (i - i0))));
      devW = Math.max(devW, Math.abs((Qi.md[i] + Qi.mu[i]) - (Qb.md[i] + Qb.mu[i])));
      devMid = Math.max(devMid, Math.abs((Qi.mu[i] - Qi.md[i]) / 2 - ((Qb.mu[i] - Qb.md[i]) / 2 - delta)));
    }

    return { q, w, eps, N, n, i0, cost, M, D, delta, imb, bal, Qi, Qb,
             devNu, devW, devMid };
  }

  function makeSim(S) {
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
      // balanced per-arrival trade probabilities at state i
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
