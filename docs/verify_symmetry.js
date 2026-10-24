/* Regression checks for the capped symmetry demo. Run with Node. */
'use strict';

const assert = require('node:assert/strict');
const SYMMETRY = require('./symmetry_core.js');

const valid = SYMMETRY.setup({ q: 0.65, a: 0.001 });
assert.equal(valid.exact, true);
assert.equal(valid.floors, 0);
assert.ok(valid.minQuote > 0.07);
assert.ok(valid.devQuote < 2e-13);
assert.ok(valid.devRate < 2e-14);
assert.equal(valid.widthOk, true);

// The live page's former default.  Both capped solves converge, but the quote
// floor binds and the physical policies no longer obey the interior map.
const binding = SYMMETRY.setup({ q: 0.65, a: 0.01, eps: 0, N: 10 });
assert.equal(binding.imb.ok, true);
assert.equal(binding.bal.ok, true);
assert.equal(binding.exact, false);
assert.ok(binding.floors > 0);
assert.ok(binding.devQuote > 0.68);
assert.ok(Math.abs(binding.devQuote - 0.6864001923871479) < 1e-12);

// Check the displayed policy diagnostics are independently reconstructed from
// the two capped optima, rather than imposed on either solver.
for (let i = 0; i < valid.imb.n; i++) {
  if (i < valid.imb.n - 1)
    assert.ok(Math.abs(valid.imb.md[i] - valid.bal.md[i] - valid.delta) < 2e-13);
  if (i > 0)
    assert.ok(Math.abs(valid.imb.mu[i] - valid.bal.mu[i] + valid.delta) < 2e-13);
}

console.log('PASS: capped policies map term by term in the strict interior');
console.log('PASS: the former floor-binding default is rejected');
