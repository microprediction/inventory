/* Four corners: policy iteration from flat cold starts at the four
 * problems the symmetry connects -- imbalanced (q, c), balanced (1/2, Mc),
 * overhead (1/2, c, eps + gamma), parity (1-q, c) -- with the diagram
 * deviations recomputed at every iteration. No consistency solver, no
 * tilt hints: the optimizers walk to the squares on their own.
 */
const FOUR = (() => {
  const W = 1;

  function gauss(A, b) {
    const n = b.length, M = A.map((r, i) => [...r, b[i]]);
    for (let c = 0; c < n; c++) {
      let p = c;
      for (let r = c + 1; r < n; r++)
        if (Math.abs(M[r][c]) > Math.abs(M[p][c])) p = r;
      [M[c], M[p]] = [M[p], M[c]];
      for (let r = 0; r < n; r++) {
        if (r === c) continue;
        const f = M[r][c] / M[c][c];
        for (let k = c; k <= n; k++) M[r][k] -= f * M[c][k];
      }
    }
    return M.map((r, i) => r[n] / M[i][i]);
  }

  function makeProblem(q, cost, eps, N) {
    const n = 2 * N + 1, i0 = N;
    const md = [], mu = [];
    for (let i = 0; i < n; i++) {
      md.push(i < n - 1 ? W + eps : NaN);
      mu.push(i > 0 ? W + eps : NaN);
    }
    return { q, cost, eps, N, n, i0, md, mu, rho: 0, done: false };
  }

  function piStep(P) {
    const { q, cost, eps, n, i0 } = P;
    const up = [], dn = [], r = [];
    for (let i = 0; i < n; i++) {
      up.push(i < n - 1 ? q * Math.exp(-P.md[i] / W) : 0);
      dn.push(i > 0 ? (1 - q) * Math.exp(-P.mu[i] / W) : 0);
      r.push((i < n - 1 ? up[i] * (P.md[i] - eps) : 0)
           + (i > 0 ? dn[i] * (P.mu[i] - eps) : 0) - cost(i - i0));
    }
    const A = [], b = [];
    for (let i = 0; i < n; i++) {
      const row = new Array(n + 1).fill(0);
      row[i] = up[i] + dn[i];
      if (i < n - 1) row[i + 1] -= up[i];
      if (i > 0) row[i - 1] -= dn[i];
      row[n] = 1;
      A.push(row); b.push(r[i]);
    }
    const last = new Array(n + 1).fill(0);
    last[i0] = 1;
    A.push(last); b.push(0);
    const sol = gauss(A, b);
    let dev = 0;
    for (let i = 0; i < n; i++) {
      if (i < n - 1) {
        const m2 = Math.max(0, W + eps - (sol[i + 1] - sol[i]));
        dev = Math.max(dev, Math.abs(m2 - P.md[i]));
        P.md[i] = m2;
      }
      if (i > 0) {
        const m2 = Math.max(0, W + eps - (sol[i - 1] - sol[i]));
        dev = Math.max(dev, Math.abs(m2 - P.mu[i]));
        P.mu[i] = m2;
      }
    }
    P.rho = sol[n];
    P.done = dev < 1e-14;
    return dev;
  }

  function setup({ q, a, N = 6, eps = 0.15 }) {
    const M = 1 / (2 * Math.sqrt(q * (1 - q)));
    const delta = 0.5 * W * Math.log(q / (1 - q));
    const gamma = W * Math.log(M);
    const cost = x => a * x * x;
    return {
      q, a, N, eps, M, delta, gamma, iter: 0,
      P: {
        imb: makeProblem(q, cost, eps, N),
        bal: makeProblem(0.5, x => M * cost(x), eps, N),
        over: makeProblem(0.5, cost, eps + gamma, N),
        par: makeProblem(1 - q, cost, eps, N),
      },
    };
  }

  function step(S) {
    let d = 0;
    for (const k in S.P) d = Math.max(d, piStep(S.P[k]));
    S.iter += 1;
    return d;
  }

  function deviations(S) {
    const { imb, bal, over, par } = S.P;
    const { delta, gamma, M } = S;
    const n = imb.n;
    let tilt = 0, overd = 0, pard = 0, w2g = 0;
    for (let i = 1; i < n - 1; i++) {
      tilt = Math.max(tilt,
        Math.abs(imb.md[i] - (bal.md[i] + delta)),
        Math.abs(imb.mu[i] - (bal.mu[i] - delta)));
      overd = Math.max(overd,
        Math.abs(imb.md[i] - (over.md[i] + delta - gamma)),
        Math.abs(imb.mu[i] - (over.mu[i] - delta - gamma)));
      w2g = Math.max(w2g, Math.abs(
        (over.md[i] + over.mu[i]) - (imb.md[i] + imb.mu[i]) - 2 * gamma));
      pard = Math.max(pard, Math.abs(
        ((imb.mu[i] - imb.md[i]) / 2 - (par.mu[i] - par.md[i]) / 2)
        + 2 * delta));
    }
    const scale = Math.abs(bal.rho - M * imb.rho);
    const overgain = Math.abs(over.rho - imb.rho);
    return { tilt, overd, pard, w2g, scale, overgain };
  }

  return { setup, step, deviations };
})();
if (typeof module !== "undefined") module.exports = FOUR;
