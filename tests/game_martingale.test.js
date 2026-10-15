const test = require('node:test');
const assert = require('node:assert/strict');
global.FOUR = require('../docs/fourcorners_core.js');
const GAME = require('../docs/game_core.js');

test('price increments stay centered at and beyond the former screen edges', () => {
  const g = GAME.create({ level: 'hard', seed: 1 });
  g.nextSpawn = Infinity;
  const dt = 1 / 60;
  // Box-Muller gives opposite normal draws at these two angles.
  const magnitude = 0.6 * Math.sqrt(dt) * Math.sqrt(-2 * Math.log(0.5));
  for (const start of [-100, -2.5, 0, 2.5, 100]) {
    let mean = 0;
    for (const angle of [0, 0.5]) {
      const draws = [0.5, angle];
      g.rng = () => draws.shift();
      g.F = start;
      g.x = 2;
      g.pricePnl = 0;
      GAME.step(g, dt);
      const expected = angle === 0 ? magnitude : -magnitude;
      assert.ok(Math.abs(g.F - start - expected) < 1e-12);
      assert.ok(Math.abs(g.pricePnl - 2 * expected) < 1e-12);
      mean += (g.F - start) / 2;
    }
    assert.ok(Math.abs(mean) < 1e-12);
  }
});
