/* Finite-horizon imbalanced market making: exact solver via the paper's own
 * spectral representation (Corollary: v(t) = D^{-1} U e^{-Lambda tau} U^T D v_T).
 *
 * System (GLFT with asymmetric scales):
 *   vdot_q = alpha q^2 v_q - eta_b v_{q+1} - eta_a v_{q-1},  |q| <= Q,
 * terminal v(T) = 1 (standard marking) or r^{-q} (flow-adjusted marking).
 * Depths: delta_b = ln(v_q/v_{q+1})/k + c0, delta_a = ln(v_q/v_{q-1})/k + c0.
 */

const FH = (() => {

  // cyclic Jacobi eigensolver for small symmetric matrices
  function eigSym(Ain) {
    const n = Ain.length;
    const A = Ain.map(r => r.slice());
    let V = Array.from({ length: n }, (_, i) =>
      Array.from({ length: n }, (_, j) => (i === j ? 1 : 0)));
    for (let sweep = 0; sweep < 100; sweep++) {
      let off = 0;
      for (let p = 0; p < n - 1; p++)
        for (let q = p + 1; q < n; q++) off += A[p][q] * A[p][q];
      if (off < 1e-24) break;
      for (let p = 0; p < n - 1; p++) {
        for (let q = p + 1; q < n; q++) {
          if (Math.abs(A[p][q]) < 1e-18) continue;
          const theta = (A[q][q] - A[p][p]) / (2 * A[p][q]);
          const t = Math.sign(theta || 1) / (Math.abs(theta) + Math.sqrt(theta * theta + 1));
          const c = 1 / Math.sqrt(t * t + 1), s = t * c;
          for (let i = 0; i < n; i++) {
            const aip = A[i][p], aiq = A[i][q];
            A[i][p] = c * aip - s * aiq;
            A[i][q] = s * aip + c * aiq;
          }
          for (let i = 0; i < n; i++) {
            const api = A[p][i], aqi = A[q][i];
            A[p][i] = c * api - s * aqi;
            A[q][i] = s * api + c * aqi;
          }
          for (let i = 0; i < n; i++) {
            const vip = V[i][p], viq = V[i][q];
            V[i][p] = c * vip - s * viq;
            V[i][q] = s * vip + c * viq;
          }
        }
      }
    }
    const lam = A.map((row, i) => row[i]);
    return { lam, V };  // columns of V are eigenvectors
  }

  function make({ Q = 6, k = 1, gamma = 0.1, sigma = 1.0, Ab = 2.0, Aa = 0.5 }) {
    const alpha = k * gamma * sigma * sigma / 2;
    const C = Math.pow(1 + gamma / k, -(1 + k / gamma));
    const etab = Ab * C, etaa = Aa * C;
    const r = Math.sqrt(etab / etaa), etabar = Math.sqrt(etab * etaa);
    const delta = Math.log(r) / k;
    const c0 = Math.log(1 + gamma / k) / gamma;
    const qs = [];
    for (let q = -Q; q <= Q; q++) qs.push(q);
    const n = qs.length, i0 = Q;

    // symmetrized matrix Mbar (same for imbalanced-conjugated and balanced)
    const Mbar = Array.from({ length: n }, (_, i) =>
      Array.from({ length: n }, () => 0));
    for (let i = 0; i < n; i++) {
      Mbar[i][i] = alpha * qs[i] * qs[i];
      if (i + 1 < n) Mbar[i][i + 1] = -etabar;
      if (i - 1 >= 0) Mbar[i][i - 1] = -etabar;
    }
    const { lam, V } = eigSym(Mbar);

    // propagate terminal vector through e^{-Mbar tau}
    function prop(tau, y0) {
      const c = new Float64Array(n);
      for (let j = 0; j < n; j++)
        for (let i = 0; i < n; i++) c[j] += V[i][j] * y0[i];
      const y = new Float64Array(n);
      for (let j = 0; j < n; j++) {
        const e = Math.exp(-lam[j] * tau) * c[j];
        for (let i = 0; i < n; i++) y[i] += V[i][j] * e;
      }
      return y;
    }

    // imbalanced v(tau): v = D^{-1} w, w solves symmetric system with
    // terminal w(T) = D v(T); marking: 'standard' v_T=1, 'adjusted' v_T=r^{-q}
    function vAt(tau, marking) {
      const vT = qs.map(q => marking === 'adjusted' ? Math.pow(r, -q) : 1.0);
      const wT = vT.map((x, i) => Math.pow(r, qs[i]) * x);
      const w = prop(tau, wT);
      return w.map((x, i) => Math.pow(r, -qs[i]) * x);
    }
    // ordinary balanced z(tau)
    function zAt(tau) { return prop(tau, qs.map(() => 1.0)); }

    function depths(vec, i) {
      return {
        db: Math.log(vec[i] / vec[i + 1]) / k + c0,
        da: Math.log(vec[i] / vec[i - 1]) / k + c0,
      };
    }

    // term structure at inventory q (interior): mid displacement and spread
    // difference vs the ordinary balanced problem
    function termStructure(tau, q, marking = 'standard') {
      const i = q + Q;
      const v = vAt(tau, marking), z = zAt(tau);
      const dv = depths(v, i), dz = depths(z, i);
      return {
        dm: (dv.da - dv.db) / 2 - (dz.da - dz.db) / 2,
        ds: (dv.db + dv.da) - (dz.db + dz.da),
        db: dv.db, da: dv.da,
      };
    }

    return { qs, n, i0, alpha, etab, etaa, etabar, r, delta, c0,
             vAt, zAt, depths, termStructure,
             gap: (() => { const s = lam.slice().sort((a, b) => a - b); return s[1] - s[0]; })() };
  }

  return { make, eigSym };
})();

if (typeof module !== 'undefined') module.exports = FH;
