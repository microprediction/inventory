"""Numerical check of Remark [Exponentiality is needed only locally] in
skew_width_imbalance.tex.

The steady-state consistency equation for a general competing-quote survival
function F is

    tau c(x)/s = q G(Kdn(x)) + (1-q) G(Kup(x)) - [same at x=0],

where G(K) = sup_m (m-K)(1-F(m)) is the value of the next enquiry as a
function of its strike, Kdn = eps + C + S and Kup = eps + C - S in terms of
the slope S and convexity C of the indifference cost nu.

Check 1 (certificate for the exact theorem): with exponential F, take the
even solution nu_bal of the balanced problem with cost M(q) c and tilt it,
nu_bal + delta x. This must satisfy the imbalanced system to machine
precision, so the imbalanced problem has an exact solution with S(0) = delta.

Check 2 (the remark): with a slowly varying hazard h(m) = h0 (1 + beta m)
the same construction, using the hazard local to the quotes actually made,
should be approximately a solution, and the directly solved zero-inventory
skew should match delta_local with relative error small next to the hazard's
relative variation across the visited strike range, shrinking as beta does.
"""

import numpy as np
from scipy.optimize import brentq, root

TAU, S_LOT, EPS = 1.0, 1.0, 0.0
N = 8  # grid: x = -N..N
XS = np.arange(-N, N + 1)
I0 = N  # index of x = 0


def strikes(nu, i):
    return (EPS + (nu[i + 1] - nu[i]) / S_LOT,
            EPS + (nu[i - 1] - nu[i]) / S_LOT)


def enquiry_value(G, q, nu, i):
    Kdn, Kup = strikes(nu, i)
    return q * G(Kdn) + (1 - q) * G(Kup)


def residuals_full(G, q, cost, nu):
    """Consistency residuals at 0 < |x| <= N-1 plus two boundary closures."""
    v0 = enquiry_value(G, q, nu, I0)
    r = [TAU * cost(XS[i]) / S_LOT - (enquiry_value(G, q, nu, i) - v0)
         for i in range(1, 2 * N) if i != I0]
    r.append((nu[0] - 2 * nu[1] + nu[2]) - (nu[1] - 2 * nu[2] + nu[3]))
    r.append((nu[-1] - 2 * nu[-2] + nu[-3]) - (nu[-2] - 2 * nu[-3] + nu[-4]))
    return np.array(r)


def solve_imbalanced(G, q, cost, init):
    def wrap(u):
        nu = np.concatenate([u[:N], [0.0], u[N:]])
        return residuals_full(G, q, cost, nu)

    u0 = np.concatenate([init[:I0], init[I0 + 1:]])
    sol = root(wrap, u0, method="lm", options={"maxiter": 40000, "xtol": 1e-14})
    nu = np.concatenate([sol.x[:N], [0.0], sol.x[N:]])
    res = np.max(np.abs(residuals_full(G, q, cost, nu)))
    assert res < 1e-10, f"solver residual {res:.2e}"
    return nu


def solve_balanced_even(G, cost):
    """Even solution of the balanced problem: unknowns nu(1..N)."""

    def nu_of(u):
        return np.concatenate([u[::-1], [0.0], u])

    def res(u):
        nu = nu_of(u)
        v0 = enquiry_value(G, 0.5, nu, I0)
        r = [TAU * cost(x) / S_LOT - (enquiry_value(G, 0.5, nu, I0 + x) - v0)
             for x in range(1, N)]
        r.append((nu[-1] - 2 * nu[-2] + nu[-3]) - (nu[-2] - 2 * nu[-3] + nu[-4]))
        return r

    u0 = 0.05 * np.arange(1, N + 1) ** 2
    sol = root(res, u0, method="lm", options={"maxiter": 40000, "xtol": 1e-14})
    nu = nu_of(sol.x)
    assert np.max(np.abs(res(sol.x))) < 1e-10
    return nu


def slope_convexity(nu):
    S0 = (nu[I0 + 1] - nu[I0 - 1]) / (2 * S_LOT)
    C0 = (nu[I0 + 1] - 2 * nu[I0] + nu[I0 - 1]) / (2 * S_LOT)
    return S0, C0


if __name__ == "__main__":
    q = 0.6
    log_odds = np.log(q / (1 - q))
    M = 1.0 / (2 * np.sqrt(q * (1 - q)))
    cost = lambda x: 0.01 * x ** 2

    # --- Check 1: exponential win curve, machine-precision certificate ----
    w = 1.0
    G_exp = lambda K: w * np.exp(-1.0 - K / w)
    delta = 0.5 * w * log_odds
    nu_bal = solve_balanced_even(G_exp, lambda x: M * cost(x))
    nu_pred = nu_bal + delta * XS
    res = np.max(np.abs(residuals_full(G_exp, q, cost, nu_pred)))
    print(f"exponential: tilted balanced solve plugged into imbalanced "
          f"system,\n   max residual = {res:.2e} (theorem exact; "
          f"S(0) = delta = {delta:+.6f} by construction)")
    assert res < 1e-10, "exact certificate fails"

    # --- Check 2: slowly varying hazard h(m) = h0 (1 + beta m) ------------
    for beta in (0.4, 0.2, 0.1):
        h0 = 1.0
        surv = lambda m: np.exp(-h0 * (m + 0.5 * beta * m * m)) if m > 0 else 1.0
        haz = lambda m: h0 * (1.0 + beta * m)

        def m_star(K, m_hi=60.0):
            f = lambda m: (m - K) * haz(m) - 1.0
            lo = max(K, 0.0) + 1e-13
            return brentq(f, lo, m_hi) if f(lo) < 0 else lo

        def G_gen(K):
            m = m_star(K)
            return (m - K) * surv(m)

        # local hazard at the quotes made near zero inventory, from a
        # preliminary balanced solve with the raw cost
        nu_pre = solve_balanced_even(G_gen, cost)
        _, C0_pre = slope_convexity(nu_pre)
        h_loc = haz(m_star(EPS + C0_pre))
        w_loc = 1.0 / h_loc
        delta_loc = 0.5 * w_loc * log_odds
        M_loc = M  # multiplier depends on q only

        # prediction: balanced solve at cost M c, tilted by delta_loc
        nu_bal = solve_balanced_even(G_gen, lambda x: M_loc * cost(x))
        nu_pred = nu_bal + delta_loc * XS

        # direct imbalanced solve, initialized at the prediction
        nu_imb = solve_imbalanced(G_gen, q, cost, nu_pred)
        S0, _ = slope_convexity(nu_imb)
        err = abs(S0 - delta_loc) / abs(delta_loc)

        # hazard variation across quotes generated by visited strikes
        K_all = [k for i in range(1, 2 * N) for k in strikes(nu_imb, i)]
        h_span = [haz(m_star(min(K_all))), haz(m_star(max(K_all)))]
        var = (max(h_span) - min(h_span)) / min(h_span)

        print(f"linear hazard beta={beta} (local width w={w_loc:.3f}):\n"
              f"   S(0) solved = {S0:+.6f} vs delta_local = {delta_loc:+.6f}"
              f", rel. error = {100*err:.2f}%\n"
              f"   hazard variation across visited strikes = {100*var:.0f}%"
              f", error/variation = {err/var:.3f}")
