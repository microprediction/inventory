// Reproduce the forward-learning statements and separate action-grid loss
// from finite-horizon learning loss.
//
// Usage: node audit_rl_forward.js [seeds=50] [horizon=64000]

const RL = require('./rl_core.js');

function runOne(seed, winCurve, horizon) {
  const env = RL.makeEnv({ seed, winCurve });
  const actions = RL.makeActions();
  const agents = {
    sym: RL.makeLearner({ env, mode: 'sym', actions }),
    rob: RL.makeLearner({ env, mode: 'robust', actions, resRate: 0.3 }),
    base: RL.makeLearner({ env, mode: 'per', actions }),
    ora: RL.makeOracle({ env }),
  };
  const window = 4000;
  const atWindowStart = {};
  for (let t = 1; t <= horizon; t++) {
    const e = env.enquiry();
    agents.sym.learn(e);
    agents.rob.learn(e);
    agents.base.learn(e);
    agents.ora.learn(e);
    if (t === horizon - window) {
      for (const k of Object.keys(agents)) atWindowStart[k] = agents[k].pnl;
    }
  }
  const result = {};
  for (const k of Object.keys(agents)) {
    const start = horizon > window ? atWindowStart[k] : 0;
    result[k] = (agents[k].pnl - start) / Math.min(horizon, window);
  }
  return result;
}

function quantile(xs, p) {
  const ys = [...xs].sort((a, b) => a - b);
  const x = (ys.length - 1) * p;
  const i = Math.floor(x), f = x - i;
  return ys[i] * (1 - f) + ys[Math.min(i + 1, ys.length - 1)] * f;
}

function gauss(A, b) {
  const n = b.length, M = A.map((r, i) => r.concat(b[i]));
  for (let c = 0; c < n; c++) {
    let p = c;
    for (let r = c + 1; r < n; r++) {
      if (Math.abs(M[r][c]) > Math.abs(M[p][c])) p = r;
    }
    [M[c], M[p]] = [M[p], M[c]];
    const z = M[c][c];
    for (let k = c; k <= n; k++) M[c][k] /= z;
    for (let r = 0; r < n; r++) {
      if (r === c) continue;
      const f = M[r][c];
      for (let k = c; k <= n; k++) M[r][k] -= f * M[c][k];
    }
  }
  return M.map(r => r[n]);
}

function solveGrid(env, q, mapped) {
  const actions = RL.makeActions(), n = 2 * env.N + 1, i0 = env.N;
  const d = mapped ? RL.delta(q, env.w) : 0;
  const mdSet = actions.map(a => Math.max(0.01, a + d));
  const muSet = actions.map(a => Math.max(0.01, a - d));
  const md = Array(n).fill(mdSet[Math.floor(mdSet.length / 2)]);
  const mu = Array(n).fill(muSet[Math.floor(muSet.length / 2)]);

  function evaluate() {
    const A = [], b = [];
    for (let i = 0; i < n; i++) {
      const up = i < n - 1 ? q * env.survQ(md[i], q) : 0;
      const dn = i > 0 ? (1 - q) * env.survQ(mu[i], q) : 0;
      const row = Array(n + 1).fill(0);
      row[i] = up + dn;
      if (i < n - 1) row[i + 1] -= up;
      if (i > 0) row[i - 1] -= dn;
      row[n] = 1;
      A.push(row);
      b.push((i < n - 1 ? up * md[i] : 0)
        + (i > 0 ? dn * mu[i] : 0) - env.cost(i - i0));
    }
    const pin = Array(n + 1).fill(0);
    pin[i0] = 1;
    A.push(pin);
    b.push(0);
    const z = gauss(A, b);
    return { h: z.slice(0, n), gain: z[n] };
  }

  for (let iter = 0; iter < 100; iter++) {
    const sol = evaluate();
    let changed = false;
    for (let i = 0; i < n; i++) {
      if (i < n - 1) {
        let best = md[i], bestValue = -Infinity;
        for (const m of mdSet) {
          const value = env.survQ(m, q) * (m + sol.h[i + 1] - sol.h[i]);
          if (value > bestValue + 1e-14) {
            best = m;
            bestValue = value;
          }
        }
        changed ||= best !== md[i];
        md[i] = best;
      }
      if (i > 0) {
        let best = mu[i], bestValue = -Infinity;
        for (const m of muSet) {
          const value = env.survQ(m, q) * (m + sol.h[i - 1] - sol.h[i]);
          if (value > bestValue + 1e-14) {
            best = m;
            bestValue = value;
          }
        }
        changed ||= best !== mu[i];
        mu[i] = best;
      }
    }
    if (!changed) return evaluate();
  }
  throw new Error(`grid policy iteration failed at q=${q}`);
}

const seeds = +(process.argv[2] || 50);
const horizon = +(process.argv[3] || 64000);
if (!Number.isInteger(seeds) || seeds < 1) throw new Error('seeds must be a positive integer');
if (!Number.isInteger(horizon) || horizon < 4000) {
  throw new Error('horizon must be an integer of at least 4000');
}

for (const winCurve of ['exponential', 'logistic']) {
  const runs = [];
  for (let seed = 1; seed <= seeds; seed++) runs.push(runOne(seed, winCurve, horizon));
  const learners = {};
  for (const k of ['sym', 'rob', 'base']) {
    const gaps = runs.map(r => r.ora - r[k]);
    learners[k] = {
      meanGap: gaps.reduce((a, b) => a + b, 0) / gaps.length,
      gapP10: quantile(gaps, 0.1),
      gapP90: quantile(gaps, 0.9),
      beatsBaseline: k === 'base' ? null : runs.filter(r => r[k] > r.base).length,
    };
  }

  const env = RL.makeEnv({ winCurve });
  const grid = { physical: 0, mapped: 0 };
  for (const q of env.regimes) {
    const continuous = RL.solveCapped(env, q).gain;
    grid.physical += (continuous - solveGrid(env, q, false).gain) / env.regimes.length;
    grid.mapped += (continuous - solveGrid(env, q, true).gain) / env.regimes.length;
  }
  console.log(JSON.stringify({ winCurve, seeds, horizon, learners, gridRegret: grid }));
}
