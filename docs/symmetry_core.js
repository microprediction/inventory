/* Capped finite-lattice verification core for symmetry.html.
 *
 * The imbalanced and balanced-at-Mc problems are solved independently by
 * policy iteration.  The imbalance theorem is reported only if every
 * available quote is strictly positive and both directional generators map
 * term by term.  A zero-markup floor changes the control problem, so a small
 * residual from the unconstrained exponential equations is not enough.
 */
const SYMMETRY = (() => {
  const F = typeof FOUR !== 'undefined' ? FOUR : require('./fourcorners_core.js');
  const W = 1;

  function solveCapped(q, cost, eps, N) {
    const P = F.makeProblem(q, cost, eps, N);
    let dev = Infinity;
    for (let iter = 1; iter <= 200; iter++) {
      dev = F.piStep(P);
      if (dev < 1e-12) return { ...P, iter, dev, ok: true };
    }
    return { ...P, iter: 200, dev, ok: false };
  }

  function floorCount(P, tol = 1e-12) {
    let count = 0, minQuote = Infinity;
    for (let i = 0; i < P.n; i++) {
      if (i < P.n - 1) {
        minQuote = Math.min(minQuote, P.md[i]);
        if (P.md[i] <= tol) count++;
      }
      if (i > 0) {
        minQuote = Math.min(minQuote, P.mu[i]);
        if (P.mu[i] <= tol) count++;
      }
    }
    return { count, minQuote };
  }

  function skew(P, i) { return (P.md[i] - P.mu[i]) / 2; }
  function width(P, i) { return P.md[i] + P.mu[i]; }

  function setup({ q, a, eps = 0.15, N = 6, w = 1 }) {
    if (w !== W) throw new Error('the capped policy solver currently uses w = 1');
    const M = 1 / (2 * Math.sqrt(q * (1 - q)));
    const D = 1 / M;
    const delta = 0.5 * Math.log(q / (1 - q));
    const cost = x => a * x * x;
    const imb = solveCapped(q, cost, eps, N);
    const bal = solveCapped(0.5, x => M * cost(x), eps, N);
    const base = solveCapped(0.5, cost, eps, N);
    const fi = floorCount(imb), fb = floorCount(bal), f0 = floorCount(base);

    let devQuote = 0, devRate = 0;
    for (let i = 0; i < imb.n; i++) {
      if (i < imb.n - 1) {
        devQuote = Math.max(devQuote, Math.abs(imb.md[i] - (bal.md[i] + delta)));
        devRate = Math.max(devRate, Math.abs(
          q * Math.exp(-imb.md[i]) - D * 0.5 * Math.exp(-bal.md[i])));
      }
      if (i > 0) {
        devQuote = Math.max(devQuote, Math.abs(imb.mu[i] - (bal.mu[i] - delta)));
        devRate = Math.max(devRate, Math.abs(
          (1 - q) * Math.exp(-imb.mu[i]) - D * 0.5 * Math.exp(-bal.mu[i])));
      }
    }

    const floors = fi.count + fb.count;
    const exact = imb.ok && bal.ok && floors === 0
      && devQuote < 1e-10 && devRate < 1e-10;
    let reason = '';
    if (!imb.ok || !bal.ok) reason = 'capped policy iteration did not converge';
    else if (floors) reason = `${floors} available quote(s) bind at zero`;
    else if (devQuote >= 1e-10) reason = 'the capped quote map is outside tolerance';
    else if (devRate >= 1e-10) reason = 'the actual generators do not scale term by term';

    const pointsImb = [], pointsBal = [];
    for (let i = 1; i < imb.n - 1; i++) {
      const x = i - N;
      pointsImb.push([x, skew(imb, i)]);
      pointsBal.push([x, skew(bal, i) + delta]);
    }
    const widthOk = exact && base.ok && f0.count === 0;
    const widthChange = widthOk ? width(imb, N) - width(base, N) : NaN;
    return {
      q, a, eps, N, M, D, delta, imb, bal, base,
      floors, minQuote: Math.min(fi.minQuote, fb.minQuote),
      devQuote, devRate, exact, reason,
      baseFloors: f0.count, widthOk, widthChange,
      pointsImb, pointsBal,
    };
  }

  return { setup, solveCapped, floorCount, skew, width };
})();

if (typeof module !== 'undefined') module.exports = SYMMETRY;
