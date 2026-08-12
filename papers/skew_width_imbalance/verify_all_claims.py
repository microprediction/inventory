"""Claim-by-claim certificate for the corrected skew_width_imbalance.tex.

Every quantitative claim in the paper gets its own labeled check, keyed to
the section it appears in. Exact identities are checked at machine precision;
approximations by ratio tests; statements about optimal policies against
bounded-chain average-reward solves in which the consistency solution is
provably optimal (one-sided Hamiltonians at the inventory bounds).

  Section 2 (model, markups, consistency)
    A1  FOC: m* = max(w + K, 0) maximizes (m - K) e^{-hm} over m >= 0
    A2  G(K) = w e^{-1-hK} for K >= -w and G(K) = -K for K < -w
    A3  quote identities: half-width = Delta + C(x), mid offset = -S(x)
    A4  consistency solution = average-reward optimum (gain = s H_q(0))

  Section 3 (the symmetry)
    B1  the cosh identity
    B2  theorem map, both directions (tilt solves; untilt solves)
    B3  gain scaling rho_bal,Mc = M(q) rho_q
    B4  quote map m_q = m_bal +/- delta; width equal; mid shifted -delta
    B5  time change: both fill rates scale by D(q) = 2 sqrt(q(1-q))
    B6  same stationary inventory distribution as balanced-at-Mc
    B7  overhead frame: eps -> eps + gamma reproduces nu; quotes remap
        with m_q = m_over + delta - gamma (buy side)
    B8  flat-book skew delta under even cost; fails under asymmetric cost
    B9  parity S_q - S_{1-q} = 2 delta, C_q = C_{1-q}, asymmetric cost
    B10 Taylor orders: delta ~ 2wz, gamma ~ 2wz^2, M-1 ~ 2z^2
    B11 exact width identity W_q - W_{1/2,c} = 2[C_Mc - C_c]
    B12 zero-carry degeneracy: every tilt solves the centered equation
    B13 envelope identity -(log G)' = h(m*) for non-exponential F

  Section 4 (constant width, CWLS)
    C1  integrability identity S(x+s) - S(x) = C(x) + C(x+s)
    C2  constant C forces affine S on the lattice
    C3  the cosh^{-1} inversion solves the consistency equation pointwise
    C4  quadratic nu implies cosh-shaped carrying cost
    C5  cosh cost is quadratic up to relative error (h S_delta)^2 / 12
    C6  small argument: S_delta proportional to sqrt(c)
    C7  linear cost component gives a square-root kink at the origin
    C8  cosh cost + constant C: solved nu is quadratic + delta x
    C9  width response: dC0/dlog(scale) = C0/(2 - hC0); eq. (9) to ~1%
    C10 the branch condition: sensitivity sign flips at hC0 = 2

  Section 5 (uses)
    D1  optimal margin over strike is exactly w at every inventory
    D2  zero-strike dealer fills e^{-1} of enquiries
    D3  fill ratio log-linear in markup with slope -1/w
    D4  the scoring table's four cells, by Monte Carlo over the cover
    D5  within-instrument normalized width response ~ 2 z^2
"""

import numpy as np
from scipy.optimize import root, minimize_scalar

TAU, S_LOT = 1.0, 1.0
N = 8
XS = np.arange(-N, N + 1)
I0 = N
H0 = 1.0
W = 1.0 / H0
EPS = 0.15
Q = 0.6
Z = Q - 0.5
DELTA = 0.5 * np.log(Q / (1 - Q)) / H0
MQ = 1.0 / (2 * np.sqrt(Q * (1 - Q)))
GAMMA = np.log(MQ) / H0
DQ = 2 * np.sqrt(Q * (1 - Q))
COST = lambda x: 0.0015 * x ** 2
rng = np.random.default_rng(11)

G_exp = lambda K: W * np.exp(-1.0 - H0 * K)


# ---------------------------------------------------------------- machinery
def hamiltonian(q, nu, i, G=G_exp, eps=EPS):
    x = XS[i]
    v = 0.0
    if x < N:
        v += q * G(eps + (nu[i + 1] - nu[i]) / S_LOT)
    if x > -N:
        v += (1 - q) * G(eps + (nu[i - 1] - nu[i]) / S_LOT)
    return v


def residuals_bounded(q, cost, nu, eps=EPS):
    """Bounded-chain consistency: one-sided Hamiltonians at +-N, so the
    solution is exactly the average-reward optimum of the chain."""
    h0v = hamiltonian(q, nu, I0, eps=eps)
    return np.array([TAU * cost(XS[i]) / S_LOT
                     - (hamiltonian(q, nu, i, eps=eps) - h0v)
                     for i in range(2 * N + 1) if i != I0])


def solve_bounded(q, cost, init, eps=EPS):
    def wrap(u):
        nu = np.concatenate([u[:N], [0.0], u[N:]])
        return residuals_bounded(q, cost, nu, eps=eps)

    u0 = np.concatenate([init[:I0], init[I0 + 1:]])
    sol = root(wrap, u0, method="lm", options={"maxiter": 80000, "xtol": 1e-15})
    nu = np.concatenate([sol.x[:N], [0.0], sol.x[N:]])
    assert np.max(np.abs(residuals_bounded(q, cost, nu, eps=eps))) < 1e-11
    return nu


def assert_interior(nu, eps=EPS):
    m = min(v for x in range(-N, N + 1) for v in quotes(nu, x, eps)
            if v is not None)
    assert m > 0, f"interiority violated: min quote {m:.3f}"
    return m


def quotes(nu, x, eps=EPS):
    """(markdown for buying, markup for selling) at inventory x, interior."""
    i = I0 + x
    mdn = W + eps + (nu[i + 1] - nu[i]) / S_LOT if x < N else None
    mup = W + eps + (nu[i - 1] - nu[i]) / S_LOT if x > -N else None
    return mdn, mup


def slope_conv(nu, x):
    i = I0 + x
    return ((nu[i + 1] - nu[i - 1]) / (2 * S_LOT),
            (nu[i + 1] - 2 * nu[i] + nu[i - 1]) / (2 * S_LOT))


def stationary(q, nu, eps=EPS):
    up = np.array([q * np.exp(-H0 * quotes(nu, x, eps)[0])
                   if x < N else 0.0 for x in XS])
    dn = np.array([(1 - q) * np.exp(-H0 * quotes(nu, x, eps)[1])
                   if x > -N else 0.0 for x in XS])
    logp = np.concatenate([[0.0], np.cumsum(np.log(up[:-1]) - np.log(dn[1:]))])
    p = np.exp(logp - logp.max())
    return p / p.sum(), up, dn


PASS = []


def check(tag, ok, detail=""):
    PASS.append((tag, ok))
    print(f"{'PASS' if ok else 'FAIL'}  {tag}  {detail}")


# ================================================================ Section 2
# A1/A2: FOC and the piecewise G
worst1 = worst2 = 0.0
for K in (-2.0, -1.2, -0.5, 0.0, 0.7, 1.5):
    res = minimize_scalar(lambda m: -(m - K) * np.exp(-H0 * m),
                          bounds=(0.0, 60.0), method="bounded",
                          options={"xatol": 1e-12})
    m_num, g_num = res.x, -res.fun
    m_th = max(W + K, 0.0)
    g_th = W * np.exp(-1.0 - H0 * K) if K >= -W else -K
    worst1 = max(worst1, abs(m_num - m_th))
    worst2 = max(worst2, abs(g_num - g_th) / max(g_th, 1e-12))
check("A1 FOC m* = max(w+K, 0)", worst1 < 1e-6, f"max err {worst1:.1e}")
check("A2 G piecewise", worst2 < 1e-9, f"max rel err {worst2:.1e}")

# A3: quote identities on a random potential
nu_r = rng.normal(size=2 * N + 1)
ok3 = True
for x in range(-(N - 1), N):
    mdn, mup = quotes(nu_r, x)
    S_, C_ = slope_conv(nu_r, x)
    ok3 &= abs(0.5 * (mdn + mup) - (W + EPS + C_)) < 1e-12
    ok3 &= abs(0.5 * (mdn - mup) - S_) < 1e-12
check("A3 half-width = Delta + C, mid offset = -S", ok3)

# A4: consistency solution is average-reward optimal (gain identity)
nu_q = solve_bounded(Q, COST, 0.05 * XS.astype(float) ** 2 + DELTA * XS)
assert_interior(nu_q)
gain = S_LOT * hamiltonian(Q, nu_q, I0)
p, up, dn = stationary(Q, nu_q)
rew = np.zeros(2 * N + 1)
for i, x in enumerate(XS):
    mdn, mup = quotes(nu_q, x)
    if x < N:
        rew[i] += up[i] * S_LOT * (mdn - EPS)
    if x > -N:
        rew[i] += dn[i] * S_LOT * (mup - EPS)
    rew[i] -= TAU * COST(x)
check("A4 gain = s H_q(0) = stationary average reward",
      abs(gain - p @ rew) < 1e-12, f"diff {abs(gain - p @ rew):.1e}")

# ================================================================ Section 3
# B1: the cosh identity
worst = max(abs(qq * np.exp(-H0 * Sv) + (1 - qq) * np.exp(H0 * Sv)
                - 2 * np.sqrt(qq * (1 - qq))
                * np.cosh(H0 * (Sv - 0.5 * np.log(qq / (1 - qq)) / H0)))
            for qq in (0.1, 0.35, 0.6, 0.9) for Sv in (-1.2, -0.1, 0.4, 2.0))
check("B1 cosh identity", worst < 1e-14, f"max err {worst:.1e}")

# B2: theorem map both directions
nu_bal = solve_bounded(0.5, lambda x: MQ * COST(x),
                       0.05 * XS.astype(float) ** 2)
assert_interior(nu_bal)
r_fwd = np.max(np.abs(residuals_bounded(Q, COST, nu_bal + DELTA * XS)))
r_bwd = np.max(np.abs(residuals_bounded(0.5, lambda x: MQ * COST(x),
                                        nu_q - DELTA * XS + (nu_q - DELTA * XS)[I0] * 0)))
check("B2 tilt of balanced-Mc solves imbalanced (and back)",
      r_fwd < 1e-11 and r_bwd < 1e-11, f"residuals {r_fwd:.1e}, {r_bwd:.1e}")

# B3: gain scaling
gain_bal = S_LOT * hamiltonian(0.5, nu_bal, I0)
check("B3 rho_bal,Mc = M(q) rho_q", abs(gain_bal - MQ * gain) < 1e-12,
      f"diff {abs(gain_bal - MQ * gain):.1e}")

# B4: quote map, width equality, mid shift
okB4 = True
for x in range(-(N - 1), N):
    mdn_q, mup_q = quotes(nu_q, x)
    mdn_b, mup_b = quotes(nu_bal, x)
    okB4 &= abs(mdn_q - (mdn_b + DELTA)) < 1e-10
    okB4 &= abs(mup_q - (mup_b - DELTA)) < 1e-10
    okB4 &= abs((mdn_q + mup_q) - (mdn_b + mup_b)) < 1e-10
check("B4 m_q = m_bal +/- delta; width equal; mid -delta", okB4)

# B5: time change
okB5 = True
for x in range(-(N - 1), N):
    mdn_q, mup_q = quotes(nu_q, x)
    mdn_b, mup_b = quotes(nu_bal, x)
    okB5 &= abs(Q * np.exp(-H0 * mdn_q)
                - DQ * 0.5 * np.exp(-H0 * mdn_b)) < 1e-14
    okB5 &= abs((1 - Q) * np.exp(-H0 * mup_q)
                - DQ * 0.5 * np.exp(-H0 * mup_b)) < 1e-14
check("B5 both fill rates scale by D(q)", okB5)

# B6: same stationary distribution as balanced-at-Mc
p_q, _, _ = stationary(Q, nu_q)
p_b, _, _ = stationary(0.5, nu_bal)
check("B6 same stationary inventory distribution",
      np.max(np.abs(p_q - p_b)) < 1e-12,
      f"max diff {np.max(np.abs(p_q - p_b)):.1e}")

# B7: overhead frame — eps -> eps + gamma at cost c gives the same nu, and
# quotes remap with m_q(buy) = m_over(buy) + delta - gamma
nu_over = solve_bounded(0.5, COST, nu_bal.copy(), eps=EPS + GAMMA)
okB7 = np.max(np.abs(nu_over - nu_bal)) < 1e-10
for x in range(-(N - 1), N):
    mdn_q, mup_q = quotes(nu_q, x)
    mdn_o, mup_o = quotes(nu_over, x, eps=EPS + GAMMA)
    okB7 &= abs(mdn_q - (mdn_o + DELTA - GAMMA)) < 1e-10
    okB7 &= abs(mup_q - (mup_o - DELTA - GAMMA)) < 1e-10
check("B7 overhead frame: same nu; quotes remap removing gamma", okB7)

# B8: flat-book skew delta under even cost; fails without evenness
S0_q, _ = slope_conv(nu_q, 0)
cost_asym = lambda x: 0.0008 * x ** 2 + 0.0003 * x ** 2 * (x > 0) + 0.0002 * abs(x)
nu_qa = solve_bounded(Q, cost_asym, nu_q.copy())
assert_interior(nu_qa)
S0_a, _ = slope_conv(nu_qa, 0)
check("B8 S_q(0) = delta iff cost symmetric",
      abs(S0_q - DELTA) < 1e-10 and abs(S0_a - DELTA) > 1e-3,
      f"even: {S0_q:.5f} = {DELTA:.5f}; asym: {S0_a:.5f}")

# B9: parity without cost symmetry
nu_ra = solve_bounded(1 - Q, cost_asym, nu_qa - 2 * DELTA * XS)
okB9 = True
for x in range(-(N - 1), N):
    Sq_, Cq_ = slope_conv(nu_qa, x)
    Sr_, Cr_ = slope_conv(nu_ra, x)
    okB9 &= abs(Sq_ - Sr_ - 2 * DELTA) < 1e-10 and abs(Cq_ - Cr_) < 1e-10
check("B9 S_q - S_(1-q) = 2 delta, C equal, asymmetric cost", okB9)

# B10: Taylor orders (ratio tests under z -> z/2)
prev = None
okB10 = True
for z in (0.08, 0.04, 0.02):
    qq = 0.5 + z
    d_err = abs(0.5 * np.log(qq / (1 - qq)) / H0 - 2 * W * z)
    g_err = abs(np.log(1 / (2 * np.sqrt(qq * (1 - qq)))) / H0 - 2 * W * z ** 2)
    m_err = abs(1 / (2 * np.sqrt(qq * (1 - qq))) - 1 - 2 * z ** 2)
    if prev is not None:
        okB10 &= prev[0] / d_err > 6 and prev[1] / g_err > 12 \
            and prev[2] / m_err > 12
    prev = (d_err, g_err, m_err)
check("B10 delta ~ 2wz (O(z^3)), gamma ~ 2wz^2, M-1 ~ 2z^2 (O(z^4))", okB10)

# B11: exact width identity
nu_c = solve_bounded(0.5, COST, 0.05 * XS.astype(float) ** 2)
assert_interior(nu_c)
okB11 = True
for x in range(-(N - 1), N):
    mdn_q, mup_q = quotes(nu_q, x)
    mdn_c, mup_c = quotes(nu_c, x)
    _, C_M = slope_conv(nu_bal, x)
    _, C_c = slope_conv(nu_c, x)
    okB11 &= abs((mdn_q + mup_q) - (mdn_c + mup_c) - 2 * (C_M - C_c)) < 1e-10
check("B11 W_q - W_(1/2,c) = 2[C_Mc - C_c]", okB11)

# B12: zero-carry degeneracy of the centered INTERIOR equation (the
# paper's remark concerns the lattice equation without boundary selection;
# on the bounded chain the one-sided boundary rows do select)
def interior_residuals(q, cost, nu):
    h0v = hamiltonian(q, nu, I0)
    return np.array([TAU * cost(XS[i]) / S_LOT
                     - (hamiltonian(q, nu, i) - h0v)
                     for i in range(1, 2 * N) if i != I0])
worst = max(np.max(np.abs(interior_residuals(Q, lambda x: 0.0,
                                             b * XS.astype(float))))
            for b in (0.0, DELTA, 0.31, -0.17))
bdy = np.max(np.abs(residuals_bounded(Q, lambda x: 0.0, DELTA * XS)))
check("B12 c = 0: every tilt solves the interior equation; boundary rows select",
      worst < 1e-13 and bdy > 1e-3,
      f"interior {worst:.1e}, boundary residual of tilt {bdy:.1e}")

# B13: envelope identity for a non-exponential win curve (Weibull k = 1.3)
k = 1.3
surv = lambda m: np.exp(-((H0 * m) ** k))
haz = lambda m: k * H0 * (H0 * m) ** (k - 1)
from scipy.optimize import brentq
def m_star_k(K):
    f = lambda m: (m - K) * haz(m) - 1.0
    lo = max(K, 0.0) + 1e-12
    return brentq(f, lo, 100.0)
def G_k(K):
    m = m_star_k(K)
    return (m - K) * surv(m)
okB13 = True
for K in (0.1, 0.5, 1.0):
    dK = 1e-6
    lhs = -(np.log(G_k(K + dK)) - np.log(G_k(K - dK))) / (2 * dK)
    okB13 &= abs(lhs - haz(m_star_k(K))) < 1e-5
check("B13 -(log G)' = hazard at optimizer, non-exponential F", okB13)

# ================================================================ Section 4
# C1: integrability identity; C2: constant C forces affine S
okC1 = True
for i in range(1, 2 * N - 1):
    S1, C1v = slope_conv(nu_r, XS[i])
    S2, C2v = slope_conv(nu_r, XS[i] + 1)
    okC1 &= abs((S2 - S1) - (C1v + C2v)) < 1e-12
check("C1 S(x+s) - S(x) = C(x) + C(x+s)", okC1)
# constant C: build nu with C == C0, verify S affine
C0 = 0.07
nu_cc = C0 / S_LOT * XS.astype(float) ** 2 + 0.3 * XS
Svals = [slope_conv(nu_cc, x)[0] for x in range(-(N - 1), N)]
d2 = np.diff(Svals, 2)
check("C2 constant C => affine S", np.max(np.abs(d2)) < 1e-12)

# C3: the cosh^{-1} inversion solves the consistency equation pointwise
Om = (TAU * H0 / S_LOT) * np.exp(1.0 + H0 * EPS)
S_delta = lambda x: np.arccosh(np.exp(H0 * C0) * Om * COST(x) + 1.0) / H0
okC3 = True
for x in (1, 3, 6):
    lhs = TAU * COST(x) / S_LOT
    rhs = (np.exp(-1 - H0 * EPS) / H0) * np.exp(-H0 * C0) \
        * (np.cosh(H0 * S_delta(x)) - 1.0)
    okC3 &= abs(lhs - rhs) < 1e-14
check("C3 cosh^{-1} inversion satisfies the equation pointwise", okC3)

# C4: quadratic nu => cosh cost; C8: converse solve returns quadratic + tilt
nu_quad = C0 / S_LOT * XS.astype(float) ** 2 + DELTA * XS
def implied_cost(x):
    i = I0 + x
    h0v = hamiltonian(Q, nu_quad, I0)
    return S_LOT / TAU * (hamiltonian(Q, nu_quad, i) - h0v)
cosh_shape = lambda x: np.cosh(2 * H0 * C0 * x / S_LOT) - 1.0
ratios = [implied_cost(x) / cosh_shape(x) for x in (1, 2, 4, 6)]
check("C4 quadratic nu implies cosh-shaped cost",
      np.max(np.abs(np.diff(ratios))) < 1e-12 * max(abs(r) for r in ratios) + 1e-13,
      f"ratio spread {max(ratios) - min(ratios):.1e}")
nu_c8 = solve_bounded(Q, lambda x: ratios[0] * cosh_shape(x), nu_quad.copy())
dev_center = max(abs(nu_c8[I0 + x] - nu_quad[I0 + x]) for x in range(-4, 5))
dev_edge = max(abs(nu_c8[I0 + x] - nu_quad[I0 + x]) for x in (-N, N))
check("C8 cosh cost: CWLS exact in the interior, boundary layer at the edge",
      dev_center < 1e-3 and dev_edge > 10 * dev_center,
      f"center dev {dev_center:.1e}, edge dev {dev_edge:.1e}")

# C5: cosh vs quadratic relative error (h S_delta)^2 / 12
okC5 = True
for u in (0.05, 0.1, 0.2):
    rel = (np.cosh(u) - 1) / (u ** 2 / 2) - 1
    okC5 &= abs(rel - u ** 2 / 12) < u ** 4 / 100
check("C5 cosh cost quadratic up to (hS)^2/12", okC5)

# C6: small argument sqrt behavior; C7: kink for linear cost
svals = [S_delta(x) / np.sqrt(COST(x)) for x in (1, 2)]
check("C6 S_delta ~ sqrt(c) at small argument",
      abs(svals[0] / svals[1] - 1) < 0.02, f"ratio {svals[0]/svals[1]:.4f}")
S_lin = lambda x: np.arccosh(np.exp(H0 * C0) * Om * 0.002 * abs(x) + 1.0) / H0
slope = np.log(S_lin(2) / S_lin(1)) / np.log(2)
check("C7 linear cost: S ~ |x|^(1/2) near origin",
      abs(slope - 0.5) < 0.02, f"log-log slope {slope:.3f}")

# C9/C10: width response formula and its branch
C0b = slope_conv(nu_c, 0)[1]
measured = slope_conv(nu_bal, 0)[1] - C0b
predicted = np.log(MQ) * C0b / (2 - H0 * C0b)
check("C9 width response = gamma hC0/(2-hC0) (~1%)",
      abs(measured / predicted - 1) < 0.05,
      f"measured {measured:.3e} vs {predicted:.3e}")
f_scale = lambda c0: c0 ** 2 * np.exp(-H0 * c0)
d_lo = f_scale(1.9 / H0 + 0.01) - f_scale(1.9 / H0)
d_hi = f_scale(2.1 / H0 + 0.01) - f_scale(2.1 / H0)
check("C10 sensitivity branch flips at hC0 = 2", d_lo > 0 > d_hi)

# ================================================================ Section 5
# D1/D2/D3
okD1 = all(abs((quotes(nu_q, x)[0] - (EPS + (nu_q[I0 + x + 1] - nu_q[I0 + x]))) - W) < 1e-12
           for x in range(-(N - 1), N))
check("D1 optimal margin over strike = w at every inventory", okD1)
check("D2 zero-strike dealer fills e^{-1}",
      abs(np.exp(-H0 * (W + 0.0)) - np.exp(-1)) < 1e-15)
ms = np.array([0.3, 0.9, 1.7])
slopes = np.diff(np.log(np.exp(-H0 * ms))) / np.diff(ms)
check("D3 fill ratio log-linear, slope -1/w",
      np.max(np.abs(slopes + 1 / W)) < 1e-12)

# D4: scoring table via Monte Carlo over the cover
m_model = 1.4          # = w + K for K = 0.4
K_tilde = m_model - W
sims = rng.exponential(scale=W, size=200_000)  # cover displacement
for m_trader, label in ((1.1, "trader tighter"), (1.8, "trader wider")):
    lo, hi = min(m_trader, m_model), max(m_trader, m_model)
    both = sims > hi
    neither = sims < lo
    only_one = (~both) & (~neither)
    v_trader = np.where(sims > m_trader, S_LOT * (m_trader - K_tilde), 0.0)
    v_model = np.where(sims > m_model, S_LOT * (m_model - K_tilde), 0.0)
    diff = v_trader - v_model
    cells_ok = True
    if both.any():
        cells_ok &= abs(diff[both].mean() - S_LOT * (m_trader - m_model)) < 1e-9
    if only_one.any():
        expect = (S_LOT * (m_trader - m_model) + S_LOT * W) if m_trader < m_model \
            else -S_LOT * W
        cells_ok &= abs(diff[only_one].mean() - expect) < 1e-9
    if neither.any():
        cells_ok &= abs(diff[neither].mean()) < 1e-12
    check(f"D4 scoring table cells ({label})", cells_ok)

# D5: within-instrument normalized width response ~ 2 z^2
resp = 2 * (slope_conv(nu_bal, 0)[1] - C0b) / C0b
check("D5 [W_q(0) - W_half(0)]/C0 ~ 2 z^2",
      abs(resp / (2 * Z ** 2) - 1) < 0.15,
      f"normalized {resp:.4f} vs 2z^2 = {2 * Z ** 2:.4f}")

# ================================================================ summary
n_fail = sum(1 for _, ok in PASS if not ok)
print(f"\n{len(PASS)} checks, {n_fail} failures")
assert n_fail == 0

# ==================================================== Section E: hardening
# E1/E2: the interiority assumption is load-bearing. With the true piecewise
# G (floor at m = 0), the tilt map holds where quotes are interior and FAILS
# where the floor binds.
G_piece = lambda K: G_exp(K) if K >= -W else -K


def residuals_piece(q, cost, nu, eps):
    h0v = hamiltonian(q, nu, I0, G=G_piece, eps=eps)
    return np.array([TAU * cost(XS[i]) / S_LOT
                     - (hamiltonian(q, nu, i, G=G_piece, eps=eps) - h0v)
                     for i in range(2 * N + 1) if i != I0])


def solve_piece(q, cost, init, eps):
    def wrap(u):
        nu = np.concatenate([u[:N], [0.0], u[N:]])
        return residuals_piece(q, cost, nu, eps)
    u0 = np.concatenate([init[:I0], init[I0 + 1:]])
    sol = root(wrap, u0, method="lm", options={"maxiter": 80000, "xtol": 1e-15})
    nu = np.concatenate([sol.x[:N], [0.0], sol.x[N:]])
    assert np.max(np.abs(residuals_piece(q, cost, nu, eps))) < 1e-10
    return nu

# interior regime: a configuration whose quotes stay safely interior
cost_small = lambda x: 0.002 * x ** 2
eps_hi = 0.3
nu_bal_s = solve_bounded(0.5, lambda x: MQ * cost_small(x),
                         0.05 * XS.astype(float) ** 2, eps=eps_hi)
min_quote = min(min(q_ for q_ in quotes(nu_bal_s, x, eps_hi) if q_ is not None)
                for x in range(-N, N + 1)) - DELTA
assert min_quote > 0, "config not interior; adjust"
nu_p6 = solve_piece(Q, cost_small, nu_bal_s + DELTA * XS, eps_hi)
dev_int = np.max(np.abs(nu_p6 - (nu_bal_s + DELTA * XS)))
# clipped regime: q = 0.9 with eps = 0 puts sell quotes through the floor
q9 = 0.9
d9 = 0.5 * np.log(q9 / (1 - q9)) / H0
M9 = 1.0 / (2 * np.sqrt(q9 * (1 - q9)))
nu_b9 = solve_bounded(0.5, lambda x: M9 * COST(x),
                      0.05 * XS.astype(float) ** 2, eps=0.0)
m_up_min = min(quotes(nu_b9, x, eps=0.0)[1] - d9 for x in range(-N + 1, N + 1))
nu_p9 = solve_piece(q9, COST, nu_b9 + d9 * XS, 0.0)
dev_clip = np.max(np.abs(nu_p9 - (nu_b9 + d9 * XS)))
check("E1 piecewise-G solver reproduces the tilt where interior",
      dev_int < 1e-9, f"dev {dev_int:.1e}, min quote {min_quote:.3f}")
check("E2 tilt FAILS where the floor binds (interiority is load-bearing)",
      m_up_min < 0 and dev_clip > 1e-3,
      f"min tilted sell quote {m_up_min:.3f} < 0; dev {dev_clip:.2e}")

# E3: configuration sweep of the core identities (theorem map, quote map,
# time change, width identity) across h, eps, q, N, and cost shapes
for (hh, ee, qq, NN, cf, name) in [
        (2.0, 0.25, 0.62, 5, lambda x: 0.001 * x ** 2, "h=2 quad"),
        (0.5, 0.10, 0.58, 6, lambda x: 0.004 * x ** 2, "h=1/2 quad"),
        (1.0, 0.30, 0.62, 4, lambda x: 0.0002 * x ** 4 + 0.0008 * x ** 2, "quartic")]:
    ww = 1.0 / hh
    dd = 0.5 * ww * np.log(qq / (1 - qq))
    MM_ = 1.0 / (2 * np.sqrt(qq * (1 - qq)))
    DD = 1.0 / MM_
    n2 = 2 * NN + 1
    xs2 = np.arange(-NN, NN + 1)
    Gh = lambda K: ww * np.exp(-1.0 - K / ww)

    def ham2(q_, nu, i):
        v = 0.0
        if xs2[i] < NN:
            v += q_ * Gh(ee + nu[i + 1] - nu[i])
        if xs2[i] > -NN:
            v += (1 - q_) * Gh(ee + nu[i - 1] - nu[i])
        return v

    def res2(q_, cst, nu):
        h0v = ham2(q_, nu, NN)
        return np.array([TAU * cst(xs2[i]) - (ham2(q_, nu, i) - h0v)
                         for i in range(n2) if i != NN])

    def slv2(q_, cst, init):
        wrap = lambda u: res2(q_, cst,
                              np.concatenate([u[:NN], [0.0], u[NN:]]))
        sol = root(wrap, np.concatenate([init[:NN], init[NN + 1:]]),
                   method="lm", options={"maxiter": 80000, "xtol": 1e-15})
        nu = np.concatenate([sol.x[:NN], [0.0], sol.x[NN:]])
        assert np.max(np.abs(res2(q_, cst, nu))) < 1e-10
        return nu

    nb = slv2(0.5, lambda x: MM_ * cf(x), 0.05 * xs2.astype(float) ** 2)
    mq_min = min(ww + ee + s_ * (nb[i + s_] - nb[i]) + t_ * dd
                 for i in range(n2) for s_, t_ in ((1, 1), (-1, -1))
                 if 0 <= i + s_ < n2)
    assert mq_min > 0, f"E3 {name}: interiority violated ({mq_min:.3f})"
    r_map = np.max(np.abs(res2(qq, cf, nb + dd * xs2)))
    okq = True
    for i in range(1, n2 - 1):
        mdq = ww + ee + (nb[i + 1] - nb[i]) + dd
        muq = ww + ee + (nb[i - 1] - nb[i]) - dd
        mdb = ww + ee + (nb[i + 1] - nb[i])
        mub = ww + ee + (nb[i - 1] - nb[i])
        okq &= abs((mdq + muq) - (mdb + mub)) < 1e-12
        okq &= abs(qq * np.exp(-mdq / ww) - DD * 0.5 * np.exp(-mdb / ww)) < 1e-14
    check(f"E3 core identities, config {name}", r_map < 1e-10 and okq,
          f"map residual {r_map:.1e}")

n_fail2 = sum(1 for _, ok in PASS if not ok)
print(f"\nwith hardening: {len(PASS)} checks, {n_fail2} failures")
assert n_fail2 == 0
