const assert = require('node:assert/strict');
const RL = require('./rl_core.js');
const MM = require('./mm_core.js');

function stationaryGain(env, q, sol) {
  const n = 2 * env.N + 1, up = [], dn = [], rew = [];
  for (let i = 0; i < n; i++) {
    up[i] = i < n - 1 ? q * env.survQ(sol.md[i], q) : 0;
    dn[i] = i > 0 ? (1 - q) * env.survQ(sol.mu[i], q) : 0;
    rew[i] = (i < n - 1 ? up[i] * sol.md[i] : 0)
      + (i > 0 ? dn[i] * sol.mu[i] : 0) - env.cost(i - env.N);
  }
  const logp = [0];
  for (let i = 0; i < n - 1; i++) logp.push(logp[i] + Math.log(up[i]) - Math.log(dn[i + 1]));
  const mx = Math.max(...logp), p = logp.map(z => Math.exp(z - mx));
  const z = p.reduce((a, b) => a + b, 0);
  return p.reduce((a, v, i) => a + v * rew[i] / z, 0);
}

let worstFixed = 0, worstGain = 0, floorCases = 0;
for (const winCurve of ['exponential', 'logistic']) {
  const env = RL.makeEnv({ winCurve });
  for (const q of env.regimes) {
    const sol = RL.solveCapped(env, q), n = 2 * env.N + 1;
    let fixed = 0;
    for (let i = 0; i < n; i++) {
      if (i < n - 1) {
        const m = env.mstar(sol.h[i] - sol.h[i + 1], q);
        fixed = Math.max(fixed, Math.abs(m - sol.md[i]));
        if (sol.md[i] <= 0.010000000001) floorCases++;
      }
      if (i > 0) {
        const m = env.mstar(sol.h[i] - sol.h[i - 1], q);
        fixed = Math.max(fixed, Math.abs(m - sol.mu[i]));
        if (sol.mu[i] <= 0.010000000001) floorCases++;
      }
    }
    const gainErr = Math.abs(stationaryGain(env, q, sol) - sol.gain);
    worstFixed = Math.max(worstFixed, fixed);
    worstGain = Math.max(worstGain, gainErr);
    assert.ok(fixed < 2e-11, `${winCurve} q=${q}: policy not fixed (${fixed})`);
    assert.ok(gainErr < 2e-12, `${winCurve} q=${q}: gain mismatch (${gainErr})`);
  }
}
assert.ok(floorCases > 0, 'default sweep must exercise the quote floor');

// The inverse chart must compare sample sizes on a fixed five-state estimand.
// The former implementation silently expanded its RMSE domain as tail cells
// accumulated three target-regime observations.
for (const winCurve of ['exponential', 'logistic']) {
  for (const nObs of [1000, 64000]) {
    const r = RL.irlRun({
      env: RL.makeEnv({ seed: 42, winCurve }),
      nObs, noise: 0.4, targetQ: 0.6,
    });
    assert.equal(r.evaluatedStates, 5,
      `${winCurve} n=${nObs}: inverse RMSE support changed`);
    assert.ok(Number.isFinite(r.pooledRMSE),
      `${winCurve} n=${nObs}: inverse RMSE missing`);
  }
}

// Reproduce the defect in the former exponential oracle: MM.solve closes the
// endpoints by equal third differences instead of using one-sided cap rows.
let worstOldQuote = 0, worstOldRegret = 0;
const env = RL.makeEnv({ winCurve: 'exponential' });
for (const q of env.regimes) {
  const exact = RL.solveCapped(env, q);
  const old = MM.solve({ q, w: env.w, N: env.N, cost: x => env.cost(x), G: K => env.G(K, q) });
  const n = 2 * env.N + 1, approx = { md: [], mu: [] };
  for (let i = 0; i < n; i++) {
    approx.md[i] = i < n - 1 ? env.mstar(old.nu[i + 1] - old.nu[i], q) : NaN;
    approx.mu[i] = i > 0 ? env.mstar(old.nu[i - 1] - old.nu[i], q) : NaN;
    if (i < n - 1) worstOldQuote = Math.max(worstOldQuote, Math.abs(approx.md[i] - exact.md[i]));
    if (i > 0) worstOldQuote = Math.max(worstOldQuote, Math.abs(approx.mu[i] - exact.mu[i]));
  }
  worstOldRegret = Math.max(worstOldRegret,
    stationaryGain(env, q, exact) - stationaryGain(env, q, approx));
}
assert.ok(worstOldQuote > 1.0, `former oracle discrepancy not reproduced (${worstOldQuote})`);
assert.ok(worstOldRegret > 2e-5, `former oracle regret not reproduced (${worstOldRegret})`);

console.log(`PASS capped RL oracle: 8 exponential/logistic regimes; `
  + `fixed-point ${worstFixed.toExponential(2)}, gain ${worstGain.toExponential(2)}, `
  + `${floorCases} floor quotes; former oracle max quote error ${worstOldQuote.toFixed(12)}, `
  + `regret ${worstOldRegret.toExponential(6)}`);

