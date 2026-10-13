/* Mind the gap: a game isomorphic to the sealed-bid market making problem.
 *
 * Each enquiry is judged against the quote in force when it arrives, so the
 * player quotes before the cover is revealed, as the model's dealer does.
 *
 * Enquiries fall from the sky. Each lands at the best competing quote: a
 * displacement z ~ Exp(mean w) from the fair value, on the sellers' side
 * (green, a buy opportunity) or the buyers' side (red, a sell opportunity).
 * The player holds a bar with a gap in it. The gap is the bid/offer: its
 * left edge is the bid, its right edge the offer. An enquiry landing in
 * the gap went to a competitor. One landing on the bar is won, at a margin
 * equal to the distance from the fair value to the bar's edge, less eps.
 * Won buys stack as inventory; a buy and a sell cancel. Carrying inventory
 * x costs a x^2 per unit time: back pain.
 *
 * Three levels, two symmetries:
 *   easy    balanced flow (q = 1/2), fixed fair value;
 *   medium  imbalanced flow, fixed fair value;
 *   hard    imbalanced flow, fair value a martingale the player must track.
 * medium -> easy by the imbalance symmetry (tilt by delta, carry times M(q));
 * hard -> medium by the frame remark (quote relative to the fair value; the
 * price term x dF has zero mean, and a mean-variance dealer's price risk is
 * exactly the quadratic carry).
 *
 * The benchmark is the policy-iteration optimum on the same lattice, from
 * fourcorners_core.js. Pure logic; game.html renders it.
 */
const GAME = (() => {
  const W = 1;

  function policy(q, a, eps, N) {
    const P = FOUR.makeProblem(q, x => a * x * x, eps, N);
    for (let k = 0; k < 200 && !P.done; k++) FOUR.piStep(P);
    return { md: P.md, mu: P.mu, rho: P.rho, n: P.n, i0: P.i0 };
  }

  function mulberry(seed) {
    let s = seed >>> 0;
    return () => {
      s = (s + 0x6D2B79F5) >>> 0;
      let t = s;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  const LEVELS = {
    easy:   { q: 0.5,  sigma: 0,   label: 'Balanced flow, fixed price' },
    medium: { q: 0.6,  sigma: 0,   label: 'Imbalanced flow, fixed price' },
    hard:   { q: 0.6,  sigma: 0.6, label: 'Imbalanced flow, moving price' },
  };

  function create(opts = {}) {
    const level = opts.level || 'medium';
    const L = LEVELS[level];
    const cfg = {
      level, q: opts.q ?? L.q, sigma: opts.sigma ?? L.sigma,
      a: opts.a ?? 0.002, eps: opts.eps ?? 0.25, N: opts.N ?? 6,
      tau: opts.tau ?? 1.0,        // mean inter-arrival, seconds
      fall: opts.fall ?? 0.45,      // seconds from sky to bar: too quick to react to, as in the model you quote before the cover is revealed
      shiftSpeed: 1.5, widenSpeed: 1.0,
    };
    const rng = mulberry(opts.seed ?? (Math.random() * 2 ** 32) >>> 0);
    const pol = policy(cfg.q, cfg.a, cfg.eps, cfg.N);
    const M = 1 / (2 * Math.sqrt(cfg.q * (1 - cfg.q)));
    const delta = 0.5 * W * Math.log(cfg.q / (1 - cfg.q));
    const twin = policy(0.5, M * cfg.a, cfg.eps, cfg.N);
    // The theorem's quote map, checked over every available direction, and
    // its standing assumption: every available quote interior (not floored
    // at zero) in both members. Outside that region the map need not hold.
    let devTwin = 0, interior = true, floorAt = null;
    for (let i = 0; i < pol.n; i++) {
      if (i < pol.n - 1) {
        devTwin = Math.max(devTwin, Math.abs(pol.md[i] - (twin.md[i] + delta)));
        if (pol.md[i] <= 0 || twin.md[i] <= 0) { interior = false; floorAt = floorAt ?? (i - pol.i0); }
      }
      if (i > 0) {
        devTwin = Math.max(devTwin, Math.abs(pol.mu[i] - (twin.mu[i] - delta)));
        if (pol.mu[i] <= 0 || twin.mu[i] <= 0) { interior = false; floorAt = floorAt ?? (i - pol.i0); }
      }
    }
    const g = {
      cfg, rng, pol, twin, M, delta, devTwin, interior, floorAt,
      t: 0, F: 0, x: 0,
      B: -(W + cfg.eps), A: W + cfg.eps,     // bid and offer, absolute price
      items: [], tray: [], nextSpawn: 0,   // tray: caught balls, by offset from the bar edge they sit on
      won: 0, lost: 0, margin: 0, carry: 0, pricePnl: 0,
      events: [],
    };
    g.nextSpawn = expo(g) * cfg.tau;
    return g;
  }

  function expo(g) { return -Math.log(1 - g.rng()); }
  function gauss(g) {
    const u = 1 - g.rng(), v = g.rng();
    return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
  }

  function optimalGap(g) {
    const i = g.x + g.pol.i0;
    return { B: g.F - g.pol.md[i], A: g.F + g.pol.mu[i] };
  }

  // ctrl: { shift: -1|0|1, widen: -1|0|1, autopilot: bool }
  function step(g, dt, ctrl = {}) {
    const { cfg } = g;
    g.events.length = 0;

    // fair value moves (hard level); mark-to-market on the book
    if (cfg.sigma > 0) {
      const L = cfg.reflect ?? 2.5;              // the fair value reflects at +-L so it stays on the board
      let F = g.F + cfg.sigma * Math.sqrt(dt) * gauss(g);
      if (F > L) F = 2 * L - F;
      if (F < -L) F = -2 * L - F;
      g.pricePnl += g.x * (F - g.F);
      g.F = F;
    }

    // controls
    if (ctrl.autopilot) {
      const o = optimalGap(g);
      g.B = o.B; g.A = o.A;
    } else {
      const sh = (ctrl.shift || 0) * cfg.shiftSpeed * dt;
      const wd = (ctrl.widen || 0) * cfg.widenSpeed * dt * 0.5;
      g.B += sh - wd; g.A += sh + wd;
      if (g.A < g.B) { const m = (g.A + g.B) / 2; g.A = m; g.B = m; }
    }

    // carry
    g.carry += cfg.a * g.x * g.x * dt;
    g.t += dt;

    // arrivals
    g.nextSpawn -= dt;
    while (g.nextSpawn <= 0) {
      const seller = g.rng() < cfg.q;
      // the quote in force when the enquiry arrives is the one that competes; the cover is
      // revealed afterwards, so moving the bar while the ball falls changes nothing
      g.items.push({ side: seller ? 1 : -1, z: expo(g) * W, y: 0, B: g.B, A: g.A, F: g.F });
      g.nextSpawn += expo(g) * cfg.tau;
    }

    // falling and landing
    for (let k = g.items.length - 1; k >= 0; k--) {
      const it = g.items[k];
      it.y += dt / cfg.fall;
      if (it.y < 1) continue;
      g.items.splice(k, 1);
      const land = it.F + (it.side > 0 ? -it.z : it.z);   // competitor's price, around the fair value at arrival
      let caught = false, margin = 0;
      if (it.side > 0) {               // seller: we buy if the bid we had out beats the competitor's
        if (it.B > land && g.x < cfg.N) { caught = true; margin = it.F - it.B - cfg.eps; }
      } else {                         // buyer: we sell if the offer we had out undercuts
        if (it.A < land && g.x > -cfg.N) { caught = true; margin = it.A - it.F - cfg.eps; }
      }
      if (caught) {
        g.won += 1; g.margin += margin; g.x += it.side;
        const k = g.tray.findIndex(b => b.side === -it.side);
        if (k >= 0) g.tray.splice(k, 1);                       // a buy and a sell cancel
        else g.tray.push({ side: it.side, off: it.side > 0 ? land - g.B : land - g.A });
      } else {
        g.lost += 1;
      }
      g.events.push({ caught, side: it.side, land, margin });
    }
    return g.events;
  }

  function stats(g) {
    const trading = g.margin - g.carry;
    const bench = g.pol.rho * g.t;
    const o = optimalGap(g);
    return {
      trading, bench, regret: bench - trading,
      total: trading + g.pricePnl,
      skew: g.F - (g.A + g.B) / 2, width: g.A - g.B,
      optSkew: g.F - (o.A + o.B) / 2, optWidth: o.A - o.B,
      fill: g.won + g.lost ? g.won / (g.won + g.lost) : 0,
      pain: g.cfg.a * g.x * g.x,
    };
  }

  return { LEVELS, policy, create, step, stats, optimalGap };
})();
if (typeof module !== "undefined") module.exports = GAME;
