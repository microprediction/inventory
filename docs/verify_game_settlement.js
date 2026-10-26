global.FOUR = require('./fourcorners_core.js');
const GAME = require('./game_core.js');

function uniforms(values) {
  let i = 0;
  return () => {
    if (i >= values.length) throw new Error('deterministic RNG exhausted');
    return values[i++];
  };
}

function uForExpo(z) { return 1 - Math.exp(-z); }

function spawn(g, sideUniform, z) {
  g.nextSpawn = 0;
  g.rng = uniforms([sideUniform, uForExpo(z), uForExpo(10)]);
  GAME.step(g, 0, { autopilot: true });
}

// The second seller's cover lies strictly between the optimal x=0 and x=1
// bid markdowns. Immediate settlement moves the first fill into inventory, so
// autopilot evaluates the second enquiry at x=1 and rejects it.
const g = GAME.create({ level: 'medium', q: 0.6, a: 0.002, eps: 0.25, N: 6, fall: 0.45, seed: 1 });
const md0 = g.pol.md[g.pol.i0];
const md1 = g.pol.md[g.pol.i0 + 1];
const zBetween = (md0 + md1) / 2;
spawn(g, 0.1, 3);
if (g.x !== 1 || g.won !== 1 || g.lost !== 0) throw new Error('first fill was not settled immediately');
spawn(g, 0.1, zBetween);
if (g.x !== 1 || g.won !== 1 || g.lost !== 1) throw new Error('second enquiry used stale inventory');
if (g.items.length !== 2) throw new Error('animation records were not retained');

const economicBeforeLanding = [g.x, g.won, g.lost, g.margin];
g.nextSpawn = 100;
GAME.step(g, 0.46, { autopilot: true });
const economicAfterLanding = [g.x, g.won, g.lost, g.margin];
if (JSON.stringify(economicAfterLanding) !== JSON.stringify(economicBeforeLanding)) {
  throw new Error('visual landing changed economic state');
}
if (g.items.length !== 0) throw new Error('animations did not finish');

// Economic settlement and subsequent carry are independent of fall duration.
function oneFill(fall) {
  const h = GAME.create({ level: 'medium', q: 0.6, a: 0.002, eps: 0.25, N: 6, fall, seed: 2 });
  spawn(h, 0.1, 3);
  h.nextSpawn = 100;
  GAME.step(h, 0.1, { autopilot: true });
  return [h.x, h.won, h.lost, h.margin, h.carry, h.pricePnl];
}
const quick = oneFill(0.01), slow = oneFill(100);
if (JSON.stringify(quick) !== JSON.stringify(slow)) throw new Error('animation duration changes economics');

// Two arrivals inside one step are still processed against sequential states.
const sameFrame = GAME.create({ level: 'medium', q: 0.6, a: 0.002, eps: 0.25, N: 6, fall: 1, seed: 4 });
const sameFrameZ = (sameFrame.pol.md[sameFrame.pol.i0] + sameFrame.pol.md[sameFrame.pol.i0 + 1]) / 2;
sameFrame.nextSpawn = 0;
sameFrame.rng = uniforms([
  0.1, uForExpo(3), 0,
  0.1, uForExpo(sameFrameZ), uForExpo(10),
]);
GAME.step(sameFrame, 0, { autopilot: true });
if (sameFrame.x !== 1 || sameFrame.won !== 1 || sameFrame.lost !== 1) {
  throw new Error('same-frame arrivals were not settled sequentially');
}

// In a moving market the animation keeps the absolute arrival-time cover.
const visual = GAME.create({ level: 'medium', q: 0.6, a: 0.002, eps: 0.25, N: 6, fall: 100, seed: 3 });
spawn(visual, 0.1, 3);
const fixedLand = visual.items[0].land;
visual.F += 1.25;
if (visual.items[0].land !== fixedLand) throw new Error('animation cover moved with fair value');

// Long seeded runs have identical economics under extreme animation speeds.
for (const level of ['easy', 'medium', 'hard']) {
  const fast = GAME.create({ level, fall: 0.01, seed: 12345 });
  const slowMotion = GAME.create({ level, fall: 100, seed: 12345 });
  for (let k = 0; k < 3000; k++) {
    GAME.step(fast, 0.01, { autopilot: true });
    GAME.step(slowMotion, 0.01, { autopilot: true });
  }
  for (const key of ['t', 'F', 'x', 'B', 'A', 'nextSpawn', 'won', 'lost', 'margin', 'carry', 'pricePnl']) {
    if (fast[key] !== slowMotion[key]) throw new Error(`${level}: ${key} depends on fall duration`);
  }
}

console.log('PASS: immediate settlement, sequential autopilot, animation-only landing, fall-time invariance');

