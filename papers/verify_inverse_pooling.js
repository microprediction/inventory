// node papers/verify_inverse_pooling.js
// Independent capped-chain policy iteration, not the extrapolated MM solver.
const assert = require('node:assert/strict');
const FOUR = require('../docs/fourcorners_core.js');

const N = 4, eps = 0.4, a = 0.01;
const delta = q => 0.5 * Math.log(q / (1 - q));
const multiplier = q => 1 / (2 * Math.sqrt(q * (1 - q)));

function solve(q, scale = 1) {
  const P = FOUR.makeProblem(q, x => scale * a * x * x, eps, N);
  for (let k = 0; k < 200 && !P.done; k++) FOUR.piStep(P);
  assert(P.done, 'policy iteration did not converge');
  const available = [...P.md, ...P.mu].filter(Number.isFinite);
  assert(Math.min(...available) > 0.08, 'quote floor invalidates this test');
  // Interior FOC: nu(x+1)-nu(x) = markdown(x) - 1 - eps.
  const nu = new Array(2 * N + 1).fill(0);
  for (let i = N; i < 2 * N; i++)
    nu[i + 1] = nu[i] + P.md[i] - 1 - eps;
  for (let i = N - 1; i >= 0; i--)
    nu[i] = nu[i + 1] - (P.md[i] - 1 - eps);
  // Check against the independently optimized sell-side differences too.
  for (let i = 1; i <= 2 * N; i++)
    assert(Math.abs(P.mu[i] - (1 + eps + nu[i - 1] - nu[i])) < 1e-12);
  return { P, nu };
}

const q = 0.6, d = delta(q), M = multiplier(q);
const imb = solve(q), unscaled = solve(0.5), matched = solve(0.5, M);
const deTilted = imb.nu.map((v, i) => v - d * (i - N));
const distance = (u, v) => Math.max(...u.map((x, i) => Math.abs(x - v[i])));
const matchedError = distance(deTilted, matched.nu);
const unscaledGap = distance(deTilted, unscaled.nu);
assert(matchedError < 1e-12, 'full cost-conditioned symmetry failed');
assert(unscaledGap > 1e-3, 'fixture must reject delta-only common-potential pooling');

// q and 1-q have the same M: here pooling is valid at fixed physical cost.
const reflected = solve(1 - q);
const reflectedDeTilted = reflected.nu.map((v, i) => v - delta(1 - q) * (i - N));
assert(distance(deTilted, reflectedDeTilted) < 1e-12);

const i = N + 2;
const skew = P => (P.md[i] - P.mu[i]) / 2;
const correctedSkew = skew(imb.P) - d;
assert(Math.abs(correctedSkew - skew(unscaled.P)) > 0.005);
assert(Math.abs(correctedSkew - skew(matched.P)) < 1e-12);
console.log({ q, M, matchedError, unscaledGap,
  atInventory2: { balancedSkew: skew(unscaled.P), deTiltedSkew: correctedSkew } });
console.log('PASS: pool matched effective costs; delta alone does not identify a common potential');
