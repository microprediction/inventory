/* Regression checks for the capped twin-dealer coupling. Run with Node. */
'use strict';

const assert = require('node:assert/strict');
const TWINS = require('./twins_core.js');

const valid = TWINS.setup({ q: 0.65, a: 0.001 });
assert.equal(valid.exact, true);
assert.equal(valid.floorCount, 0);
assert.ok(valid.minQuote > 0.07);
assert.ok(valid.devQuote < 1e-12);
assert.ok(valid.devRate < 1e-12);

// This was the old default.  Its capped optimum reaches the quote floor, so
// the imbalance translation and common embedded chain are no longer exact.
const binding = TWINS.setup({ q: 0.65, a: 0.01, eps: 0, N: 8 });
assert.equal(binding.exact, false);
assert.ok(binding.floorCount > 0);
assert.ok(binding.devQuote > 0.3);
assert.throws(() => TWINS.makeSim(binding), /exact coupling unavailable/);

const sim = TWINS.makeSim(valid);
const random = Math.random;
Math.random = () => 0.25;
try {
  sim.step();
} finally {
  Math.random = random;
}
assert.ok(Math.abs(sim.tBal / sim.tImb - valid.D) < 1e-14);

console.log('PASS: capped policies converge and map term by term');
console.log('PASS: the former floor-binding default is rejected');
console.log('PASS: the coupled clocks use the verified generator scale');
