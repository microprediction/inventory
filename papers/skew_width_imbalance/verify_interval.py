"""Validated-numerics certificate: a Krawczyk interval-Newton proof of
existence, local uniqueness, and interiority for the consistency solution
at the flagship configuration and its balanced image.

For F the bounded-chain consistency system (16 unknowns at N = 8, nu(0) = 0
pinned) and a box X around the floating-point solution, the Krawczyk
operator is

    K(X) = m - Y F(m) + (I - Y J(X)) (X - m),

with m the box midpoint, Y an approximate inverse Jacobian (any float
matrix works; rigor comes from the interval evaluation), and J(X) the
interval Jacobian over X. If K(X) is contained in the interior of X,
then F has EXACTLY ONE zero in X. All interval arithmetic is outward
rounded (mpmath.iv), so the conclusion is a machine-checked theorem, not
a floating-point observation:

    I1  the imbalanced problem (q = 0.6, c = 0.0015 x^2, N = 8,
        eps = 0.15) has exactly one solution in a box of radius 1e-7
        around the reported certificate solution;
    I2  the balanced image (q = 1/2, cost M(q) c) likewise;
    I3  every available quote of both proven solutions is interior
        (positive lower interval bound), so Assumption 3 HOLDS, provably,
        at this configuration;
    I4  the proven enclosures satisfy the theorem's tilt map
        nu_q = nu_bal + delta x within the enclosure widths.

    I5  continuation: tiling q in [0.55, 0.605] into 220 slabs and
        running Krawczyk with q as an INTERVAL parameter (mean-value
        form) proves the same conclusions for EVERY q in the range,
        not merely sampled values;
    I6  the balanced image likewise, with the cost scale M(q) c as the
        interval parameter (enclosed by monotonicity of M).

This upgrades Assumptions 2 (existence/uniqueness, locally) and 3
(interiority) from "instantiated by floating-point certificates" to
"proven at the certificate configuration". Global uniqueness over the
whole interior region, and anything asymptotic, remain analytic matters.
"""

import numpy as np
from scipy.optimize import root
from mpmath import iv, mp

mp.dps = 30
iv.dps = 30

N = 8
NS = 2 * N + 1
I0 = N
XS = np.arange(-N, N + 1)
EPS = 0.15
Q = 0.6
MQ = 1.0 / (2.0 * np.sqrt(Q * (1 - Q)))
DELTA = 0.5 * np.log(Q / (1 - Q))
COST_A = 0.0015


# ---------------------------------------------------------------- floats
def solve_float(q, ca):
    def ham(nu, i):
        v = 0.0
        if i < NS - 1:
            v += q * np.exp(-1 - EPS - (nu[i + 1] - nu[i]))
        if i > 0:
            v += (1 - q) * np.exp(-1 - EPS - (nu[i - 1] - nu[i]))
        return v

    def res(u):
        nu = np.concatenate([u[:I0], [0.0], u[I0:]])
        h0 = ham(nu, I0)
        return [ca * XS[i] ** 2 - (ham(nu, i) - h0)
                for i in range(NS) if i != I0]

    sol = root(res, [0.05 * XS[i] ** 2 + DELTA * XS[i]
                     for i in range(NS) if i != I0],
               method="lm", options={"maxiter": 80000, "xtol": 1e-15})
    assert np.max(np.abs(res(sol.x))) < 1e-12
    return sol.x  # 16-vector, nu at states != 0


# ------------------------------------------------- interval machinery
def nu_of(u):
    """u: length-16 list of iv numbers -> nu list with nu[I0] = 0."""
    return list(u[:I0]) + [iv.mpf(0)] + list(u[I0:])


def G_iv(K):
    return iv.exp(-1 - K)


def F_iv(u, q, ca):
    q = iv.convert(q)
    nu = nu_of(u)

    def ham(i):
        v = iv.mpf(0)
        if i < NS - 1:
            v += q * G_iv(iv.mpf(EPS) + nu[i + 1] - nu[i])
        if i > 0:
            v += (1 - q) * G_iv(iv.mpf(EPS) + nu[i - 1] - nu[i])
        return v

    h0 = ham(I0)
    return [iv.convert(ca) * int(XS[i]) ** 2 - (ham(i) - h0)
            for i in range(NS) if i != I0]


def J_iv(u, q, ca):
    """Interval Jacobian of F wrt the 16 unknowns. G' = -G (h = 1)."""
    q = iv.convert(q)
    nu = nu_of(u)
    cols = [i for i in range(NS) if i != I0]

    def dham(i):  # dict: dH(i)/dnu_j over lattice index j
        d = {}
        if i < NS - 1:
            g = q * G_iv(iv.mpf(EPS) + nu[i + 1] - nu[i])
            d[i + 1] = d.get(i + 1, iv.mpf(0)) - g
            d[i] = d.get(i, iv.mpf(0)) + g
        if i > 0:
            g = (1 - q) * G_iv(iv.mpf(EPS) + nu[i - 1] - nu[i])
            d[i - 1] = d.get(i - 1, iv.mpf(0)) - g
            d[i] = d.get(i, iv.mpf(0)) + g
        return d

    d0 = dham(I0)
    J = []
    for i in cols:
        di = dham(i)
        J.append([-(di.get(j, iv.mpf(0)) - d0.get(j, iv.mpf(0)))
                  for j in cols])
    return J


def Fq_iv(u, q, ca):
    """Interval enclosure of dF/dq (holding nu fixed)."""
    nu = nu_of(u)

    def dhq(i):
        v = iv.mpf(0)
        if i < NS - 1:
            v += G_iv(iv.mpf(EPS) + nu[i + 1] - nu[i])
        if i > 0:
            v -= G_iv(iv.mpf(EPS) + nu[i - 1] - nu[i])
        return v

    d0 = dhq(I0)
    return [-(dhq(i) - d0) for i in range(NS) if i != I0]


def J_np(u, q, ca):
    """Float Jacobian (analytic), for the preconditioner only."""
    nu = np.concatenate([u[:I0], [0.0], u[I0:]])
    cols = [i for i in range(NS) if i != I0]

    def dham(i):
        d = {}
        if i < NS - 1:
            g = q * np.exp(-1 - EPS - (nu[i + 1] - nu[i]))
            d[i + 1] = d.get(i + 1, 0.0) - g
            d[i] = d.get(i, 0.0) + g
        if i > 0:
            g = (1 - q) * np.exp(-1 - EPS - (nu[i - 1] - nu[i]))
            d[i - 1] = d.get(i - 1, 0.0) - g
            d[i] = d.get(i, 0.0) + g
        return d

    d0 = dham(I0)
    return np.array([[-(dham(i).get(j, 0.0) - d0.get(j, 0.0))
                      for j in cols] for i in cols])


def krawczyk(u_float, q, ca, r, q_iv=None, ca_iv=None):
    """Parametric Krawczyk in mean-value form. r may be a scalar or a
    per-component array. q_iv / ca_iv, when given, are interval
    parameters (a q-slab, a cost-scale slab): a single contraction then
    proves the conclusion for EVERY parameter value in the slab. The
    parameter dependence is enclosed as
        F(m, p) in F(m, p_m) + dF/dp(m, P) (P - p_m),
    and the scalar (P - p_m) is factored out AFTER the product with Y,
    preserving the cancellation Y dF/dp ~ du/dp that naive interval
    evaluation of F(m, P) destroys."""
    if q_iv is None:
        q_iv = iv.mpf(q)
    if ca_iv is None:
        ca_iv = iv.mpf(ca)
    n = len(u_float)
    rvec = np.broadcast_to(np.asarray(r, dtype=float), (n,))
    Y = np.linalg.inv(J_np(u_float, q, ca))
    Yi = [[iv.mpf(Y[i, j]) for j in range(n)] for i in range(n)]

    m = [iv.mpf(x) for x in u_float]              # midpoint, exact points
    X = [iv.mpf([x - rj, x + rj]) for x, rj in zip(u_float, rvec)]
    Fm = F_iv(m, q, ca)                           # at the point parameter
    JX = J_iv(X, q_iv, ca_iv)                     # over box and slab
    # parameter mean-value terms: q-slab and cost-scale slab
    dq = q_iv - iv.mpf(q)
    dca = ca_iv - iv.mpf(ca)
    Fq = Fq_iv(m, q_iv, ca_iv) if float(dq.delta.a) > 0 else None
    Fca = ([iv.mpf(int(XS[i]) ** 2) for i in range(NS) if i != I0]
           if float(dca.delta.a) > 0 else None)            # dF/d(ca) exactly x^2
    K = []
    for i in range(n):
        acc = m[i]
        for j in range(n):
            acc -= Yi[i][j] * Fm[j]
        if Fq is not None:
            yfq = iv.mpf(0)
            for j in range(n):
                yfq += Yi[i][j] * Fq[j]
            acc -= yfq * dq
        if Fca is not None:
            yfc = iv.mpf(0)
            for j in range(n):
                yfc += Yi[i][j] * Fca[j]
            acc -= yfc * dca
        for j in range(n):
            e = (iv.mpf(1) if i == j else iv.mpf(0))
            for k in range(n):
                e -= Yi[i][k] * JX[k][j]
            acc += e * (X[j] - m[j])
        K.append(acc)
    inside = all(K[i].a > X[i].a and K[i].b < X[i].b for i in range(n))
    return inside, K, X


def quote_bounds(K_box, q):
    """Interval quotes of the proven solution; return min lower bound."""
    nu = nu_of(K_box)
    lo = None
    for i in range(NS):
        if i < NS - 1:
            v = iv.mpf(1) + iv.mpf(EPS) + nu[i + 1] - nu[i]
            lo = v.a if lo is None or v.a < lo else lo
        if i > 0:
            v = iv.mpf(1) + iv.mpf(EPS) + nu[i - 1] - nu[i]
            lo = v.a if lo is None or v.a < lo else lo
    return lo


if __name__ == "__main__":
    PASS = []

    def check(tag, ok, detail=""):
        PASS.append(ok)
        print(("PASS " if ok else "FAIL ") + tag
              + ("  " + detail if detail else ""))

    r = 1e-7
    u_q = solve_float(Q, COST_A)
    ok_q, K_q, X_q = krawczyk(u_q, Q, COST_A, r)
    wid_q = max(float(k.b - k.a) for k in K_q)
    check("I1 Krawczyk: exactly one imbalanced solution in the box",
          ok_q, f"K(X) subset int(X); enclosure width {wid_q:.1e}")

    u_b = solve_float(0.5, MQ * COST_A)
    ok_b, K_b, X_b = krawczyk(u_b, 0.5, MQ * COST_A, r)
    wid_b = max(float(k.b - k.a) for k in K_b)
    check("I2 Krawczyk: exactly one balanced-at-Mc solution in the box",
          ok_b, f"K(X) subset int(X); enclosure width {wid_b:.1e}")

    lo_q = quote_bounds(K_q, Q)
    lo_b = quote_bounds(K_b, 0.5)
    check("I3 interiority PROVEN: every quote's interval lower bound > 0",
          float(lo_q) > 0 and float(lo_b) > 0,
          f"min lower bounds {float(lo_q):.4f} (imb), {float(lo_b):.4f} (bal)")

    d_iv = iv.log(iv.mpf(Q) / (1 - iv.mpf(Q))) / 2
    xs = [int(XS[i]) for i in range(NS) if i != I0]
    dev = max(float(abs(K_q[k] - (K_b[k] + d_iv * xs[k])).b)
              for k in range(len(xs)))
    check("I4 tilt map nu_q = nu_bal + delta x within proven enclosures",
          dev < 1e-6, f"max |nu_q - (nu_bal + delta x)| <= {dev:.1e}")

    # I5/I6: continuation -- prove the conclusions for EVERY q in
    # [0.55, 0.605] (the interiority frontier at this cost is near 0.610)
    # by tiling into slabs and running Krawczyk with q as an interval.
    QLO, QHI, NSLAB = 0.55, 0.605, 220
    edges = np.linspace(QLO, QHI, NSLAB + 1)
    sol_i = {e: solve_float(e, COST_A) for e in edges}
    Mfun = lambda qq: 1.0 / (2.0 * np.sqrt(qq * (1 - qq)))
    sol_b = {e: solve_float(0.5, Mfun(e) * COST_A) for e in edges}
    ok_i = ok_b = 0
    lo_i = lo_b = None
    for k in range(NSLAB):
        q1, q2 = edges[k], edges[k + 1]
        qm = 0.5 * (q1 + q2)
        Qs = iv.mpf([q1, q2])
        # imbalanced member: radius covers the solution's motion in the slab
        r_i = 1.1 * np.abs(sol_i[q2] - sol_i[q1]) + 1e-6
        okk, Kk, _ = krawczyk(solve_float(qm, COST_A), qm, COST_A, r_i,
                              q_iv=Qs)
        v = quote_bounds(Kk, qm)
        lo_i = v if lo_i is None or v < lo_i else lo_i
        ok_i += okk
        # balanced member: q enters only through the cost scale M(q).
        # M is strictly increasing on q > 1/2, so the tight enclosure is
        # the hull of the endpoint values -- evaluating M(Qs) directly
        # would suffer the interval dependency problem (Qs appears twice)
        # and overestimate the width by a factor 1/|1-2q|.
        c1 = iv.convert(COST_A) / (2 * iv.sqrt(iv.mpf(q1) * (1 - iv.mpf(q1))))
        c2 = iv.convert(COST_A) / (2 * iv.sqrt(iv.mpf(q2) * (1 - iv.mpf(q2))))
        ca_slab = iv.mpf([min(c1.a, c2.a), max(c1.b, c2.b)])
        r_b = 1.1 * np.abs(sol_b[q2] - sol_b[q1]) + 1e-6
        okk, Kk, _ = krawczyk(solve_float(0.5, Mfun(qm) * COST_A), 0.5,
                              Mfun(qm) * COST_A, r_b, ca_iv=ca_slab)
        v = quote_bounds(Kk, 0.5)
        lo_b = v if lo_b is None or v < lo_b else lo_b
        ok_b += okk
    check("I5 continuation: for EVERY q in [0.55, 0.605], exactly one "
          "imbalanced solution, interior",
          ok_i == NSLAB and float(lo_i) > 0,
          f"{ok_i}/{NSLAB} slabs contract; min quote lower bound "
          f"{float(lo_i):.4f}")
    check("I6 continuation: for EVERY q in [0.55, 0.605], the balanced "
          "image likewise",
          ok_b == NSLAB and float(lo_b) > 0,
          f"{ok_b}/{NSLAB} slabs contract; min quote lower bound "
          f"{float(lo_b):.4f}")

    assert all(PASS)
    print(f"\n{sum(PASS)}/{len(PASS)} interval certificates hold")
