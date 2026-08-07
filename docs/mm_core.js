/* Core solver for the sealed-bid market making model of
 * "On a Simple Relationship Between Order Imbalance, Skew and Width in
 * Over-The-Counter Trading" (Cotton). Exponential best-competitor with
 * market width w: G(K) = w exp(-1 - K/w) is the value of the next enquiry
 * as a function of its strike. The steady state indifference cost nu(x)
 * solves, for all inventories x on the grid,
 *
 *   tau c(x)/s = q G(eps + (nu(x+s)-nu(x))/s)
 *              + (1-q) G(eps + (nu(x-s)-nu(x))/s)  -  [same at x=0].
 */

const MM = (() => {

  function solve({ q, w, eps = 0, tau = 1, s = 1, N = 10, cost, G: Gcustom }) {
    const G = Gcustom || (K => w * Math.exp(-1 - K / w));
    const n = 2 * N + 1, i0 = N;
    const xs = Array.from({ length: n }, (_, i) => (i - N) * s);

    const residuals = nu => {
      const val = i => {
        const Kdn = eps + (nu[i + 1] - nu[i]) / s;
        const Kup = eps + (nu[i - 1] - nu[i]) / s;
        return q * G(Kdn) + (1 - q) * G(Kup);
      };
      const v0 = val(i0), r = [];
      for (let i = 1; i < n - 1; i++) {
        if (i === i0) continue;
        r.push(tau * cost(xs[i]) / s - (val(i) - v0));
      }
      r.push((nu[0] - 2 * nu[1] + nu[2]) - (nu[1] - 2 * nu[2] + nu[3]));
      r.push((nu[n - 1] - 2 * nu[n - 2] + nu[n - 3]) - (nu[n - 2] - 2 * nu[n - 3] + nu[n - 4]));
      return r;
    };

    // unknowns: nu at x != 0
    const pack = nu => nu.slice(0, i0).concat(nu.slice(i0 + 1));
    const unpack = u => u.slice(0, i0).concat([0], u.slice(i0));

    const delta = 0.5 * w * Math.log(q / (1 - q));
    let u = xs.filter(x => x !== 0).map(x => 0.05 * x * x + delta * x);

    const norm2 = v => v.reduce((a, b) => a + b * b, 0);
    let lambda = 1e-3;
    for (let iter = 0; iter < 200; iter++) {
      const r = residuals(unpack(u));
      const f0 = norm2(r);
      if (f0 < 1e-24) break;
      const m = u.length;
      // numerical Jacobian
      const J = [];
      for (let j = 0; j < m; j++) {
        const h = 1e-7 * (1 + Math.abs(u[j]));
        const u2 = u.slice(); u2[j] += h;
        const r2 = residuals(unpack(u2));
        J.push(r2.map((v, k) => (v - r[k]) / h)); // column j
      }
      // normal equations with Levenberg damping: (JtJ + lam I) d = -Jt r
      const A = [], b = [];
      for (let a = 0; a < m; a++) {
        b.push(-J[a].reduce((acc, v, k) => acc + v * r[k], 0));
        const row = [];
        for (let c = 0; c < m; c++) {
          let acc = 0;
          for (let k = 0; k < r.length; k++) acc += J[a][k] * J[c][k];
          row.push(acc + (a === c ? lambda : 0));
        }
        A.push(row);
      }
      const d = gauss(A, b);
      const u1 = u.map((v, j) => v + d[j]);
      const f1 = norm2(residuals(unpack(u1)));
      if (f1 < f0) { u = u1; lambda = Math.max(lambda / 3, 1e-10); }
      else lambda *= 10;
      if (Math.sqrt(f0) < 1e-11) break;
    }
    const nu = unpack(u);
    return { nu, xs, resid: Math.sqrt(norm2(residuals(nu))) };
  }

  function gauss(A, b) {
    const m = b.length, M2 = A.map((row, i) => row.concat([b[i]]));
    for (let c = 0; c < m; c++) {
      let p = c;
      for (let r2 = c + 1; r2 < m; r2++) if (Math.abs(M2[r2][c]) > Math.abs(M2[p][c])) p = r2;
      [M2[c], M2[p]] = [M2[p], M2[c]];
      for (let r2 = c + 1; r2 < m; r2++) {
        const f = M2[r2][c] / M2[c][c];
        for (let k = c; k <= m; k++) M2[r2][k] -= f * M2[c][k];
      }
    }
    const x = new Array(m).fill(0);
    for (let r2 = m - 1; r2 >= 0; r2--) {
      let acc = M2[r2][m];
      for (let k = r2 + 1; k < m; k++) acc -= M2[r2][k] * x[k];
      x[r2] = acc / M2[r2][r2];
    }
    return x;
  }

  // slope and convexity of nu per unit, at interior grid index i
  function slope(nu, i, s = 1) { return (nu[i + 1] - nu[i - 1]) / (2 * s); }
  function convexity(nu, i, s = 1) { return (nu[i + 1] - 2 * nu[i] + nu[i - 1]) / (2 * s); }

  // the three imbalance constants
  function constants(q, w) {
    return {
      delta: 0.5 * w * Math.log(q / (1 - q)),
      gamma: w * Math.log(1 / (2 * Math.sqrt(q * (1 - q)))),
      M: 1 / (2 * Math.sqrt(q * (1 - q))),
    };
  }

  // optimal markups from nu: markdown (buy) and markup (sell) at index i
  function quotes(nu, i, { w, eps = 0, s = 1 }) {
    const Kdn = eps + (nu[i + 1] - nu[i]) / s;
    const Kup = eps + (nu[i - 1] - nu[i]) / s;
    return { mDown: Math.max(w + Kdn, 0), mUp: Math.max(w + Kup, 0) };
  }

  return { solve, slope, convexity, constants, quotes };
})();

if (typeof module !== 'undefined') module.exports = MM;
