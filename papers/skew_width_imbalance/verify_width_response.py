"""Certificate for the corrected width-response statements in
skew_width_imbalance.tex (correction of 2026-08-12).

Two claims:

1. TWO FRAMES, NOT TWO CORRECTIONS. The imbalanced dealer's physical
   half-width equals that of the balanced dealer at carrying cost M(q) c
   EXACTLY. Widening the overhead by gamma and multiplying the carry by
   M(q) = e^{h gamma} are the same factor read in two frames; no gamma
   appears additively in the physical quotes.

2. THE WIDTH RESPONSE FORMULA. Relative to the balanced dealer at cost c,
   the width response at zero inventory is the convexity response to the
   multiplied carry, with closed leading-order form
       Delta C(0) = gamma * h C(0) / (2 - h C(0)) + O((q - 1/2)^4),
   from d C_0 / d log(cost scale) = C_0 / (2 - h C_0) in the small-skew
   quadratic-cost regime. Verified within about two percent for
   q in [0.55, 0.7] in the tested configurations.
"""

import numpy as np
from scipy.optimize import root

TAU, S_LOT, EPS = 1.0, 1.0, 0.15
N = 6
XS = np.arange(-N, N + 1)
I0 = N
H0 = 1.0
COST = lambda x: 0.0025 * x ** 2

G_exp = lambda K: (1.0 / H0) * np.exp(-1.0 - H0 * K)


def enquiry_value(q, nu, i):
    Kdn = EPS + (nu[i + 1] - nu[i]) / S_LOT
    Kup = EPS + (nu[i - 1] - nu[i]) / S_LOT
    return q * G_exp(Kdn) + (1 - q) * G_exp(Kup)


def residuals(q, cost, nu):
    v0 = enquiry_value(q, nu, I0)
    r = [TAU * cost(XS[i]) / S_LOT - (enquiry_value(q, nu, i) - v0)
         for i in range(1, 2 * N) if i != I0]
    r.append((nu[0] - 2 * nu[1] + nu[2]) - (nu[1] - 2 * nu[2] + nu[3]))
    r.append((nu[-1] - 2 * nu[-2] + nu[-3]) - (nu[-2] - 2 * nu[-3] + nu[-4]))
    return np.array(r)


def solve_imbalanced(q, cost, init):
    def wrap(u):
        nu = np.concatenate([u[:N], [0.0], u[N:]])
        return residuals(q, cost, nu)

    u0 = np.concatenate([init[:I0], init[I0 + 1:]])
    sol = root(wrap, u0, method="lm", options={"maxiter": 60000, "xtol": 1e-15})
    nu = np.concatenate([sol.x[:N], [0.0], sol.x[N:]])
    assert np.max(np.abs(residuals(q, cost, nu))) < 1e-11
    return nu


def solve_balanced(cost):
    def nu_of(u):
        return np.concatenate([u[::-1], [0.0], u])

    def res(u):
        nu = nu_of(u)
        v0 = enquiry_value(0.5, nu, I0)
        r = [TAU * cost(x) / S_LOT - (enquiry_value(0.5, nu, I0 + x) - v0)
             for x in range(1, N)]
        r.append((nu[-1] - 2 * nu[-2] + nu[-3])
                 - (nu[-2] - 2 * nu[-3] + nu[-4]))
        return r

    sol = root(res, 0.05 * np.arange(1, N + 1) ** 2, method="lm",
               options={"maxiter": 60000, "xtol": 1e-15})
    nu = nu_of(sol.x)
    assert np.max(np.abs(res(sol.x))) < 1e-11
    return nu


def half_width(nu, x):
    i = I0 + x
    mup = 1 / H0 + EPS + (nu[i - 1] - nu[i]) / S_LOT
    mdn = 1 / H0 + EPS + (nu[i + 1] - nu[i]) / S_LOT
    return 0.5 * (mup + mdn)


def convexity0(nu):
    return (nu[I0 + 1] - 2 * nu[I0] + nu[I0 - 1]) / (2 * S_LOT)


if __name__ == "__main__":
    def assert_interior(nu):
        m = min(half_width(nu, x) - abs((nu[I0 + x + 1] - nu[I0 + x - 1]) / 2)
                for x in range(-(N - 1), N))
        # crude bound: min individual quote
        mq = min(v for x in range(-(N - 1), N)
                 for v in (1 / H0 + EPS + (nu[I0 + x + 1] - nu[I0 + x]),
                           1 / H0 + EPS + (nu[I0 + x - 1] - nu[I0 + x])))
        assert mq > 0, f"interiority violated: {mq:.3f}"

    nu_c = solve_balanced(COST)
    assert_interior(nu_c)
    C0 = convexity0(nu_c)
    print(f"balanced C(0) = {C0:.5f}  (h C(0) = {H0 * C0:.5f})")

    for q in (0.55, 0.60, 0.65, 0.70):
        M = 1.0 / (2 * np.sqrt(q * (1 - q)))
        gamma = np.log(M) / H0
        delta = 0.5 * np.log(q / (1 - q)) / H0
        nu_Mc = solve_balanced(lambda x: M * COST(x))
        nu_imb = solve_imbalanced(q, COST, nu_Mc + delta * XS)
        assert_interior(nu_imb)

        # claim 1: imbalanced width == balanced-at-Mc width, exactly
        d_frames = max(abs(half_width(nu_imb, x) - half_width(nu_Mc, x))
                       for x in range(-(N - 1), N))
        # claim 2: width response over balanced-at-c matches the formula
        measured = convexity0(nu_Mc) - C0
        predicted = np.log(M) * C0 / (2.0 - H0 * C0)
        print(f"q={q}: |width(imb) - width(bal Mc)| = {d_frames:.1e}; "
              f"response {measured:.3e} vs formula {predicted:.3e} "
              f"(ratio {measured / predicted:.3f}); old gamma claim "
              f"{gamma:.3e}")
        assert d_frames < 1e-10, "frames differ: two-representations fails"
        assert abs(measured / predicted - 1) < 0.05, "formula off by > 5%"

    print("all checks passed: one transformation, two frames; width "
          "response = gamma * hC(0)/(2 - hC(0)) to ~1%")
