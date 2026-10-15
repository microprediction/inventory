"""Numerical certificate for exponential_normal_form.tex.

The objects. G(K) = sup_m (m-K)(1-F(m)) is the value of the next enquiry as
a function of its strike; Phi(K) = -log(G(K)/G_star) is the effective
log-value. Exponential competing markups make Phi affine, Phi = a + h K.
General win curves are deformations Phi_eta = a + h K + eta psi(K), and the
paper's claims are organized around that anchor. The strike coordinates are
A = eps + C (overhead plus convexity) and S (skew), with K_dn = A + S,
K_up = A - S, and the imbalance log-odds is ell = (1/2) log(q/(1-q)).

Checks, numbered as in the paper:

1. NORMAL FORM (Theorem 1). For arbitrary smooth positive G, with
   U = (Phi(A+S)+Phi(A-S))/2 and V = (Phi(A+S)-Phi(A-S))/2,
       q G(A+S) + (1-q) G(A-S) = 2 sqrt(q(1-q)) G_star e^{-U} cosh(V - ell),
   equivalently H_q(U,V) = H_{1/2}(U + log M(q), V - ell): imbalance is
   exactly a translation in the (U,V) coordinates. Machine precision.

2. POINTWISE GAUGE. T_c(K) = Phi^{-1}(Phi(K) - log c) satisfies
   G(T_c(K)) = c G(K), so q G(K_dn) = (1/2) G(T_{2q}(K_dn)) and the
   imbalanced Hamiltonian is pointwise a balanced one. Machine precision.

3. RIGIDITY AND THE INTEGRABILITY DEFECT (Theorems 2, 3). The transformed
   strikes derive from a single inventory potential iff the defect
       D(K) = T_{2q}(K) + T_{2(1-q)}(2 eps - K)
   is constant in K. For affine Phi it is constant and equals
   2 eps + 2 gamma, recovering the widening; for Phi_eta the variation of
   D is first order in eta and matches the finite-difference formula
       T_c(K) = K - log(c)/h + (eta/h)[psi(K) - psi(K - log(c)/h)] + O(eta^2).

4. PERTURBATION HIERARCHY (Theorem 4). With nu_eta = nu_0 + eta nu_1 +
   eta^2 nu_2 + ..., the first correction solves the linear system
       L_0 nu_1 = -R_psi,
       L_0 u  = h Delta_0 [ q G_0(K_dn) D+ u + (1-q) G_0(K_up) D- u ],
       R_psi  = Delta_0 [ q G_0(K_dn) psi(K_dn) + (1-q) G_0(K_up) psi(K_up) ],
   and every higher correction solves a system with the SAME operator L_0
   and known forcing. Verified: || nu_eta - nu_0 - eta nu_1 || = O(eta^2)
   and, with nu_2 from L_0 nu_2 = -lim (1/eta^2) F(nu_0 + eta nu_1, eta),
   || nu_eta - nu_0 - eta nu_1 - eta^2 nu_2 || = O(eta^3).

5. ENVELOPE TRANSFER (Proposition, distributions to deformations). For a
   log-survival expansion -log Fbar_theta(m) = h m + theta r(m), the
   effective log-value is
       Phi_theta(K) = Phi_0(K) + theta r(K + 1/h)
                      - theta^2 r'(K + 1/h)^2 / (2 h^2) + O(theta^3):
   to first order the movement of the optimal markup drops out. Verified on
   the Weibull family Fbar_k(m) = exp(-(hm)^k), k = 1 + theta, whose
   first-order deformation is psi(K) = (1 + hK) log(1 + hK).

6. PARITY (distribution-free). With a common win curve on both sides and
   even carrying cost, reflection maps (q, x) to (1-q, -x), so
   nu_{1-q}(x) = nu_q(-x): the zero-inventory skew contains only odd and
   the zero-inventory convexity only even powers of ell, for win curves
   nowhere near exponential. Verified exactly, plus the nondegeneracy of
   the leading coefficients: S(0)/ell -> d1 != 0 and
   (C(0) - C_bal)/ell^2 -> g2 != 0.

7. STRIKE RIGIDITY BOUNDARY. The affine-exponential family
   G = kappa + B e^{-hK} is balanced exactly by the rigid strike
   translations (A, S) -> (A + gamma, S - delta) even though Phi is
   curved: the constant passes through both Hamiltonians. Verified at
   machine precision, along with the differentiated relation
   2q G'(K) = G'(K + gamma - delta) that drives the rigidity proof.
   Also verified: the CONCAVE family G = kappa - B e^{+hK} (decreasing,
   C^2, but G'' < 0) balances rigidly too, with the opposite-signed
   translations (A - gamma, S + delta) -- the counterexample showing the
   convexity hypothesis in the strike-rigidity theorem is load-bearing.
   And the borderline-tail reading of the constant: along the
   affine-exponential family, m*(K) Fbar(m*(K)) -> kappa as K grows, so
   kappa > 0 is a 1/m survival tail and finite mean forces kappa = 0.

8. ADMISSIBILITY. For the curved deformation, the reconstruction
   m*(K) = K + 1/Phi'(K), survival = G Phi', satisfies the local
   admissibility conditions (Phi' > 0, Phi'' < Phi'^2, G Phi' <= 1), and
   re-optimizing sup_m (m - K)(reconstructed survival) recovers G.

9. TANGENT POLICY. The first-order quote correction decomposes into the
   inventory-value response and the direct markup-distribution response:
   m*_eta at the exact strikes equals
   K_0 + 1/h + eta [D nu_1 - psi'(K_0)/h^2] + O(eta^2), checked by a
   ratio test.

10. NO RIGID BALANCING OFF THE BOUNDARY (the uniqueness direction of
   Hamiltonian rigidity, on an instance). For the curved deformation the
   balancing gap min over ALL (gamma, delta) of
   sup |H_q(A,S) - H_{1/2}(A + gamma, S - delta)| / |H_q| stays bounded
   away from zero, while the affine-exponential family achieves ~1e-16 at
   the standard translations (check 7).

11. OSCILLATION BOUND. The measured oscillation of the defect D on the
   test interval satisfies the bound of the corollary,
   osc D <= (|eta|/h) diam(I) (|a1|+|a2|) ||psi''||_inf, at small eta.

12. RESOLVENT FACTOR. ||nu_1|| <= ||L_0^{-1}|| ||R_psi|| holds, and the
   curvature amplification factor ||L_0^{-1}|| is reported.

13. FIRST-ORDER PATH DEPENDENCE / NULL DIRECTION. The additive path
   G_eta = G_0 + eta*kappa has tangent psi_add = -kappa/G_0 whose forcing
   is exactly constant, so the centering annihilates it: R = 0 and
   nu_1 = 0 at machine precision, while the Phi-straight-line to the SAME
   endpoint has tangent -log(1 + kappa/G_0) with nonzero forcing and
   nonzero nu_1. Path dependence begins at first order.

14. POLICY-SENSITIVITY BOUNDS. With psi normalized to vanish to first
   order at the mid-strike, the chain ||nu_1|| <= ||L_0^{-1}|| ||R_psi||
   <= ||L_0^{-1}|| G_max R^2 ||psi''|| holds on the test problem, and so
   does the submitted-quote version with the direct psi'/h^2 term.

15. ONE TRANSFORMATION, TWO REPRESENTATIONS (not both at once). The
   imbalanced dealer's physical half-width equals that of the balanced
   dealer at cost M(q) c EXACTLY; it does NOT exceed the balanced-at-c
   dealer's width by gamma. Widening the overhead by gamma and
   multiplying the carry by M(q) = e^{h gamma} are alternative
   representations of the same transformation; the physical width
   response to imbalance is the endogenous convexity response
   C_{Mc}(x) - C_c(x), second order but cost-dependent, not the
   universal gamma.
"""

import numpy as np
from scipy.optimize import brentq, root

TAU, S_LOT, EPS = 1.0, 1.0, 0.3  # positive overhead keeps visited strikes
                                 # inside the deformation domain 1 + hK > 0
N = 8  # inventory grid x = -N..N
XS = np.arange(-N, N + 1)
I0 = N

H0 = 1.0        # anchor hazard
GSTAR = 1.0     # normalization of G; Phi = -log(G/GSTAR)

rng = np.random.default_rng(7)


# ----------------------------------------------------------------------
# machinery shared with the companion certificates
# ----------------------------------------------------------------------

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
    sol = root(wrap, u0, method="lm", options={"maxiter": 60000, "xtol": 1e-15})
    nu = np.concatenate([sol.x[:N], [0.0], sol.x[N:]])
    res = np.max(np.abs(residuals_full(G, q, cost, nu)))
    assert res < 1e-11, f"solver residual {res:.2e}"
    return nu


def slope_convexity(nu):
    S0 = (nu[I0 + 1] - nu[I0 - 1]) / (2 * S_LOT)
    C0 = (nu[I0 + 1] - 2 * nu[I0] + nu[I0 - 1]) / (2 * S_LOT)
    return S0, C0


# ----------------------------------------------------------------------
# the deformed family: Phi_eta(K) = 1 + h K + eta psi(K), psi Weibull-born
# ----------------------------------------------------------------------

def psi_weibull(K):
    """First-order Weibull deformation of the effective log-value."""
    z = 1.0 + H0 * K
    return z * np.log(z)


def make_G(eta, psi=psi_weibull):
    """G_eta(K) = GSTAR exp(-1 - h K - eta psi(K)); eta = 0 is exponential."""
    if eta == 0.0:
        return lambda K: GSTAR * np.exp(-1.0 - H0 * K)
    return lambda K: GSTAR * np.exp(-1.0 - H0 * K - eta * psi(K))


def make_Phi(eta, psi=psi_weibull):
    if eta == 0.0:
        return lambda K: 1.0 + H0 * K
    return lambda K: 1.0 + H0 * K + eta * psi(K)


def invert_Phi(Phi, y, lo=-0.95, hi=60.0):
    return brentq(lambda K: Phi(K) - y, lo, hi, xtol=1e-15, rtol=1e-15)


# ======================================================================
if __name__ == "__main__":
    q = 0.6
    ell = 0.5 * np.log(q / (1 - q))
    Mq = 1.0 / (2 * np.sqrt(q * (1 - q)))
    cost = lambda x: 0.002 * x ** 2

    # --- Check 1: exact normal form for arbitrary smooth G ---------------
    eta_big = 0.35  # nowhere near exponential
    G = make_G(eta_big)
    Phi = make_Phi(eta_big)
    worst_nf = worst_tr = 0.0
    for _ in range(200):
        A = rng.uniform(-0.3, 1.5)
        S = rng.uniform(-0.6, 0.6)
        qq = rng.uniform(0.05, 0.95)
        l = 0.5 * np.log(qq / (1 - qq))
        U = 0.5 * (Phi(A + S) + Phi(A - S))
        V = 0.5 * (Phi(A + S) - Phi(A - S))
        Hq = qq * G(A + S) + (1 - qq) * G(A - S)
        nf = 2 * np.sqrt(qq * (1 - qq)) * GSTAR * np.exp(-U) * np.cosh(V - l)
        worst_nf = max(worst_nf, abs(Hq - nf) / abs(Hq))
        # translation form: H_q(U,V) = H_{1/2}(U + log M, V - ell)
        Mqq = 1.0 / (2 * np.sqrt(qq * (1 - qq)))
        h_half = GSTAR * np.exp(-(U + np.log(Mqq))) * np.cosh(V - l)
        worst_tr = max(worst_tr, abs(Hq - h_half) / abs(Hq))
    print(f"1. normal form  : max rel err {worst_nf:.2e} (identity), "
          f"{worst_tr:.2e} (translation form)")
    assert worst_nf < 1e-13 and worst_tr < 1e-13

    # --- Check 2: pointwise gauge G(T_c(K)) = c G(K) ---------------------
    worst = 0.0
    for _ in range(200):
        K = rng.uniform(-0.3, 1.5)
        c = rng.uniform(0.2, 1.9)
        Tc = invert_Phi(Phi, Phi(K) - np.log(c))
        worst = max(worst, abs(G(Tc) - c * G(K)) / (c * G(K)))
    print(f"2. gauge        : max rel err {worst:.2e} in G(T_c(K)) = c G(K)")
    assert worst < 1e-12

    # --- Check 3: rigidity and the integrability defect ------------------
    # affine case: defect constant and equal to 2 eps + 2 gamma; the defect
    # is evaluated around a positive overhead so the mirrored strike
    # 2 eps - K stays inside the deformation's domain 1 + h K > 0
    gamma = np.log(Mq) / H0
    eps3 = 0.6
    Phi0 = make_Phi(0.0)
    Kgrid = np.linspace(0.0, 1.2, 31)
    D_affine = np.array(
        [invert_Phi(Phi0, Phi0(K) - np.log(2 * q))
         + invert_Phi(Phi0, Phi0(2 * eps3 - K) - np.log(2 * (1 - q)))
         for K in Kgrid])
    err_aff = np.max(np.abs(D_affine - (2 * eps3 + 2 * gamma)))
    print(f"3. defect       : affine case constant = 2 eps + 2 gamma "
          f"to {err_aff:.2e}")
    assert err_aff < 1e-12

    # curved case: the defect's variation is first order in eta and matches
    # the finite-difference formula, with O(eta^2) remainders; T_c matches
    # its own expansion to O(eta^2)
    a1, a2 = np.log(2 * q) / H0, np.log(2 * (1 - q)) / H0
    lin_shape = (psi_weibull(Kgrid) - psi_weibull(Kgrid - a1)
                 + psi_weibull(2 * eps3 - Kgrid)
                 - psi_weibull(2 * eps3 - Kgrid - a2)) / H0
    prev_dev = prev_ferr = None
    for eta in (0.1, 0.05, 0.025):
        Phe = make_Phi(eta)
        D = np.array(
            [invert_Phi(Phe, Phe(K) - np.log(2 * q))
             + invert_Phi(Phe, Phe(2 * eps3 - K) - np.log(2 * (1 - q)))
             for K in Kgrid])
        span = D.max() - D.min()
        dev = np.max(np.abs((D - D.mean()) - eta * (lin_shape
                                                    - lin_shape.mean())))
        ferr = max(
            abs(invert_Phi(Phe, Phe(K) - np.log(c))
                - (K - np.log(c) / H0
                   + (eta / H0) * (psi_weibull(K)
                                   - psi_weibull(K - np.log(c) / H0))))
            for K in Kgrid[::6] for c in (2 * q, 2 * (1 - q)))
        line = (f"   eta={eta:>5}: defect span {span:.3e}, "
                f"|span - first order| {dev:.2e}, T_c expansion err "
                f"{ferr:.2e}")
        if prev_dev is not None:
            line += (f"  [ratios {prev_dev / dev:.2f} ~ 4,"
                     f" {prev_ferr / ferr:.2f} ~ 4]")
            assert 3.0 < prev_dev / dev < 4.8, "defect is not first order"
            assert 3.0 < prev_ferr / ferr < 4.8, "T_c expansion not O(eta^2)"
        print(line)
        prev_dev, prev_ferr = dev, ferr

    # --- Check 4: the perturbation hierarchy -----------------------------
    G0 = make_G(0.0)
    delta = ell / H0
    nu_bal = None  # even balanced solve at cost M(q) c, exponential anchor

    def solve_balanced_even(G, cst):
        def nu_of(u):
            return np.concatenate([u[::-1], [0.0], u])

        def res(u):
            nu = nu_of(u)
            v0 = enquiry_value(G, 0.5, nu, I0)
            r = [TAU * cst(x) / S_LOT
                 - (enquiry_value(G, 0.5, nu, I0 + x) - v0)
                 for x in range(1, N)]
            r.append((nu[-1] - 2 * nu[-2] + nu[-3])
                     - (nu[-2] - 2 * nu[-3] + nu[-4]))
            return r

        u0 = 0.05 * np.arange(1, N + 1) ** 2
        sol = root(res, u0, method="lm",
                   options={"maxiter": 60000, "xtol": 1e-15})
        nu = nu_of(sol.x)
        assert np.max(np.abs(res(sol.x))) < 1e-11
        return nu

    nu_bal = solve_balanced_even(G0, lambda x: Mq * cost(x))
    nu0 = nu_bal + delta * XS          # exact exponential solution (anchor)
    res0 = np.max(np.abs(residuals_full(G0, q, cost, nu0)))
    assert res0 < 1e-11, "anchor certificate fails"
    K_all = [k for i in range(1, 2 * N) for k in strikes(nu0, i)]
    assert 1.0 + H0 * min(K_all) > 0.05, "psi domain violated on the grid"

    # build L_0 and R_psi from the paper's formulas
    def build_L0_Rpsi(nu0, psi_fn=psi_weibull):
        n_unk = 2 * N            # nu_1 at x != 0; nu_1(0) = 0
        idx = {x: (x + N if x < 0 else x + N - 1) for x in XS if x != 0}

        def dplus_row(x):
            row = np.zeros(n_unk)
            if x + 1 != 0:
                row[idx[x + 1]] += 1.0 / S_LOT
            if x != 0:
                row[idx[x]] -= 1.0 / S_LOT
            return row

        def dminus_row(x):
            row = np.zeros(n_unk)
            if x - 1 != 0:
                row[idx[x - 1]] += 1.0 / S_LOT
            if x != 0:
                row[idx[x]] -= 1.0 / S_LOT
            return row

        def hamil_rows(x):
            i = I0 + x
            Kdn, Kup = strikes(nu0, i)
            row = (q * G0(Kdn) * dplus_row(x)
                   + (1 - q) * G0(Kup) * dminus_row(x))
            forc = (q * G0(Kdn) * psi_fn(Kdn)
                    + (1 - q) * G0(Kup) * psi_fn(Kup))
            return row, forc

        row0, forc0 = hamil_rows(0)
        L, R = [], []
        for x in XS:
            if x == 0 or abs(x) == N:
                continue
            row, forc = hamil_rows(x)
            L.append(H0 * (row - row0))
            R.append(forc - forc0)
        # boundary closures: third difference matching, homogeneous
        for sgn in (-1, 1):
            row = np.zeros(n_unk)
            xs = [sgn * N, sgn * (N - 1), sgn * (N - 2), sgn * (N - 3)]
            for xx, cf in zip(xs, (1.0, -3.0, 3.0, -1.0)):
                if xx != 0:
                    row[idx[xx]] += cf
            L.append(row)
            R.append(0.0)
        return np.array(L), np.array(R), idx

    L0, Rpsi, idx = build_L0_Rpsi(nu0)
    u1 = np.linalg.solve(L0, -Rpsi)
    nu1 = np.zeros(2 * N + 1)
    for x, j in idx.items():
        nu1[x + N] = u1[j]

    print("4. hierarchy    : L_0 nu_1 = -R_psi against nonlinear solves")
    prev1 = prev2 = None
    etas = (0.04, 0.02, 0.01)
    nu2 = None
    for eta in etas:
        Ge = make_G(eta)
        nu_eta = solve_imbalanced(Ge, q, cost, nu0 + eta * nu1)
        e1 = np.max(np.abs(nu_eta - nu0 - eta * nu1))
        if nu2 is None:
            # nu_2 from L_0 nu_2 = -(1/eta^2) F(nu_0 + eta nu_1, eta),
            # Richardson-extrapolated in eta
            def rhs2(et):
                Fv = residuals_full(make_G(et), q, cost, nu0 + et * nu1)
                return -Fv / et ** 2
            r_a, r_b = rhs2(1e-3), rhs2(5e-4)
            u2 = np.linalg.solve(L0, (4 * r_b - r_a) / 3.0)
            nu2 = np.zeros(2 * N + 1)
            for x, j in idx.items():
                nu2[x + N] = u2[j]
        e2 = np.max(np.abs(nu_eta - nu0 - eta * nu1 - eta ** 2 * nu2))
        line = f"   eta={eta:>5}: |err_1| {e1:.3e}, |err_2| {e2:.3e}"
        if prev1 is not None:
            line += (f"  [ratios {prev1 / e1:.2f} ~ 4, "
                     f"{prev2 / e2:.2f} ~ 8]")
            assert 3.3 < prev1 / e1 < 4.7, "first order is not O(eta^2)"
            assert 6.0 < prev2 / e2 < 10.0, "second order is not O(eta^3)"
        print(line)
        prev1, prev2 = e1, e2

    # --- Check 5: envelope transfer from the Weibull family --------------
    def G_weibull(K, k):
        surv = lambda m: np.exp(-((H0 * m) ** k)) if m > 0 else 1.0
        haz = lambda m: k * H0 * (H0 * m) ** (k - 1)
        f = lambda m: (m - K) * haz(m) - 1.0
        lo = max(K, 0.0) + 1e-13
        m = brentq(f, lo, 80.0) if f(lo) < 0 else lo
        return (m - K) * surv(m)

    # the Weibull family is nonlinear in theta:
    # (hm)^{1+theta} = hm + theta r(m) + theta^2 r2(m) + O(theta^3),
    # so the second-order effective term is the family's own r2 at the
    # anchor optimum plus the universal envelope quadratic -r'^2/(2h^2)
    r_fun = lambda m: H0 * m * np.log(H0 * m)
    rp_fun = lambda m: H0 * (np.log(H0 * m) + 1.0)
    r2_fun = lambda m: 0.5 * H0 * m * np.log(H0 * m) ** 2
    Ktest = np.linspace(-0.5, 2.0, 11)
    prev1 = prev2 = None
    print("5. envelope     : Phi_theta - Phi_0 = theta r(K + 1/h) "
          "+ theta^2 [r2 - r'^2/(2 h^2)](K + 1/h) + O(theta^3)")
    for th in (0.08, 0.04, 0.02):
        dPhi = np.array([-np.log(G_weibull(K, 1 + th))
                         + np.log(G_weibull(K, 1.0)) for K in Ktest])
        m0 = Ktest + 1 / H0
        first = th * r_fun(m0)
        second = th ** 2 * (r2_fun(m0) - rp_fun(m0) ** 2 / (2 * H0 ** 2))
        e1 = np.max(np.abs(dPhi - first))
        e2 = np.max(np.abs(dPhi - first - second))
        line = f"   theta={th:>4}: |err_1| {e1:.3e}, |err_2| {e2:.3e}"
        if prev1 is not None:
            line += (f"  [ratios {prev1 / e1:.2f} ~ 4, "
                     f"{prev2 / e2:.2f} ~ 8]")
            assert 3.4 < prev1 / e1 < 4.6
            assert 6.5 < prev2 / e2 < 9.5
        print(line)
        prev1, prev2 = e1, e2

    # --- Check 6: distribution-free parity -------------------------------
    Gc = make_G(eta_big)  # far from exponential
    nu_q = solve_imbalanced(Gc, q, cost, nu0)
    nu_r = solve_imbalanced(Gc, 1 - q, cost, nu0[::-1] - nu0[::-1][I0])
    refl = np.max(np.abs(nu_r - (nu_q[::-1] - nu_q[::-1][I0])))
    print(f"6. parity       : |nu_(1-q)(x) - nu_q(-x)| = {refl:.2e} "
          f"(reflection exact)")
    assert refl < 1e-9

    # leading-order scalings: S(0) odd ~ d1 ell, C(0) even ~ g2 ell^2
    nu_b = solve_imbalanced(Gc, 0.5, cost, nu_bal)
    _, C0_bal = slope_convexity(nu_b)
    prevS = prevC = None
    for l in (0.2, 0.1, 0.05):
        qq = 1.0 / (1.0 + np.exp(-2 * l))
        nqq = solve_imbalanced(Gc, qq, cost, nu_b + (l / H0) * XS)
        S0, C0 = slope_convexity(nqq)
        line = (f"   ell={l:>4}: S(0)/ell = {S0 / l:+.6f}, "
                f"(C(0)-C_bal)/ell^2 = {(C0 - C0_bal) / l ** 2:+.6f}")
        if prevS is not None:
            assert abs(S0 / l - prevS) < 0.02 * abs(prevS), "d1 not converging"
            assert abs((C0 - C0_bal) / l ** 2 - prevC) < 0.1 * abs(prevC) + 1e-4
        print(line)
        prevS, prevC = S0 / l, (C0 - C0_bal) / l ** 2

    # --- Check 7: the Hamiltonian rigidity boundary ----------------------
    Cae, Bae = 0.7, 1.3
    G_ae = lambda K: Cae + Bae * np.exp(-H0 * K)
    Gp_ae = lambda K: -H0 * Bae * np.exp(-H0 * K)
    worst_bal = worst_dif = 0.0
    for _ in range(200):
        A = rng.uniform(-0.5, 1.5)
        S = rng.uniform(-0.7, 0.7)
        qq = rng.uniform(0.05, 0.95)
        l = 0.5 * np.log(qq / (1 - qq))
        Mqq = 1.0 / (2 * np.sqrt(qq * (1 - qq)))
        gam, dlt = np.log(Mqq) / H0, l / H0
        lhs = qq * G_ae(A + S) + (1 - qq) * G_ae(A - S)
        rhs = 0.5 * G_ae(A + gam + (S - dlt)) + 0.5 * G_ae(A + gam - (S - dlt))
        worst_bal = max(worst_bal, abs(lhs - rhs) / abs(lhs))
        K = rng.uniform(-0.5, 1.5)
        worst_dif = max(worst_dif,
                        abs(2 * qq * Gp_ae(K) - Gp_ae(K + gam - dlt)))
    print(f"7. rigidity edge: affine-exponential G balanced rigidly to "
          f"{worst_bal:.2e}; 2q G'(K) = G'(K + gamma - delta) to "
          f"{worst_dif:.2e}")
    assert worst_bal < 1e-14 and worst_dif < 1e-13

    # concave counterexample: G = kappa - B e^{+hK}, decreasing but G'' < 0,
    # balances rigidly with the OPPOSITE-signed translations; convexity is
    # what excludes it
    Ccc, Bcc = 3.0, 0.4
    G_cc = lambda K: Ccc - Bcc * np.exp(H0 * K)
    worst_cc = 0.0
    for _ in range(200):
        A = rng.uniform(-0.5, 0.8)
        S = rng.uniform(-0.4, 0.4)
        qq = rng.uniform(0.1, 0.9)
        l = 0.5 * np.log(qq / (1 - qq))
        Mqq = 1.0 / (2 * np.sqrt(qq * (1 - qq)))
        gam, dlt = np.log(Mqq) / H0, l / H0
        lhs = qq * G_cc(A + S) + (1 - qq) * G_cc(A - S)
        rhs = 0.5 * G_cc(A - gam + (S + dlt)) + 0.5 * G_cc(A - gam - (S + dlt))
        worst_cc = max(worst_cc, abs(lhs - rhs) / abs(lhs))
    print(f"   concave family balances rigidly to {worst_cc:.2e} "
          f"(G'' < 0; excluded by the convexity hypothesis)")
    assert worst_cc < 1e-14

    # borderline-tail reading: m* Fbar(m*) -> kappa along the affine family
    tail = [(K + 1 / H0 + Cae / (H0 * Bae) * np.exp(H0 * K))
            * H0 * Bae * np.exp(-H0 * K) for K in (5.0, 10.0, 20.0)]
    print(f"   m* Fbar(m*) at K = 5, 10, 20: "
          + ", ".join(f"{t:.6f}" for t in tail) + f"  -> kappa = {Cae}")
    assert abs(tail[-1] - Cae) < 1e-6

    # --- Check 8: admissibility and reconstruction of the win curve ------
    from scipy.interpolate import CubicSpline
    from scipy.optimize import minimize_scalar
    eta_adm = 0.35
    Ph = make_Phi(eta_adm)
    Phip = lambda K: H0 + eta_adm * H0 * (np.log(1 + H0 * K) + 1.0)
    Phipp = lambda K: eta_adm * H0 ** 2 / (1 + H0 * K)
    Ga = make_G(eta_adm)
    Kg = np.linspace(-0.5, 1.5, 601)
    assert np.all(Phip(Kg) > 0)
    assert np.all(Phipp(Kg) < Phip(Kg) ** 2)
    fbar = Ga(Kg) * Phip(Kg)
    assert np.all(fbar > 0) and np.all(fbar <= 1.0)
    mg = Kg + 1.0 / Phip(Kg)
    assert np.all(np.diff(mg) > 0), "optimizer map not increasing"
    log_fbar = CubicSpline(mg, np.log(fbar))
    worst = 0.0
    for Kt in np.linspace(-0.2, 1.2, 15):
        res = minimize_scalar(
            lambda m: -(m - Kt) * np.exp(log_fbar(m)),
            bounds=(mg[0], mg[-1]), method="bounded",
            options={"xatol": 1e-12})
        worst = max(worst, abs(-res.fun - Ga(Kt)) / Ga(Kt))
    print(f"8. admissibility: reconstructed win curve re-optimizes to G "
          f"with max rel err {worst:.2e}")
    assert worst < 1e-6

    # --- Check 9: the tangent-policy expansion ---------------------------
    psip = lambda K: H0 * (np.log(1 + H0 * K) + 1.0)
    prev = None
    print("9. tangent policy: quote error after the first-order formula")
    for eta in (0.04, 0.02):
        Ge = make_G(eta)
        Phe_p = lambda K: H0 + eta * psip(K)
        nu_eta = solve_imbalanced(Ge, q, cost, nu0 + eta * nu1)
        errs_m = []
        for i in range(1, 2 * N):
            for sgn in (+1, -1):
                K_exact = EPS + (nu_eta[i + sgn] - nu_eta[i]) / S_LOT
                m_exact = K_exact + 1.0 / Phe_p(K_exact)
                K0v = EPS + (nu0[i + sgn] - nu0[i]) / S_LOT
                Dn1 = (nu1[i + sgn] - nu1[i]) / S_LOT
                m_pred = (K0v + 1.0 / H0
                          + eta * (Dn1 - psip(K0v) / H0 ** 2))
                errs_m.append(abs(m_exact - m_pred))
        e = max(errs_m)
        line = f"   eta={eta:>5}: max quote error {e:.3e}"
        if prev is not None:
            line += f"  [ratio {prev / e:.2f} ~ 4]"
            assert 3.2 < prev / e < 4.8, "tangent policy not O(eta^2)"
        print(line)
        prev = e

    # --- Check 10: no rigid balancing off the affine-exponential boundary
    from scipy.optimize import minimize
    Gc10 = make_G(eta_big)
    Agrid = np.linspace(0.2, 1.0, 9)
    Sgrid = np.linspace(-0.4, 0.4, 9)

    def balancing_gap(params):
        gam, dlt = params
        worst = 0.0
        for A in Agrid:
            for S in Sgrid:
                hq = q * Gc10(A + S) + (1 - q) * Gc10(A - S)
                hb = 0.5 * (Gc10(A + gam + (S - dlt))
                            + Gc10(A + gam - (S - dlt)))
                worst = max(worst, abs(hq - hb) / abs(hq))
        return worst

    start = (np.log(Mq) / H0, 0.5 * np.log(q / (1 - q)) / H0)
    best = min(minimize(balancing_gap, s0, method="Nelder-Mead",
                        options={"xatol": 1e-10, "fatol": 1e-12}).fun
               for s0 in (start, (0.0, 0.0), (0.1, 0.3)))
    print(f"10. uniqueness  : curved G best rigid-balancing gap "
          f"{best:.2e} (affine-exponential achieves ~1e-16)")
    assert best > 1e-3, "curved G unexpectedly balances rigidly"

    # --- Check 11: the oscillation bound on the defect ------------------
    psi_pp = lambda K: H0 ** 2 / (1.0 + H0 * K)
    for eta in (0.05, 0.025):
        Phe = make_Phi(eta)
        D = np.array(
            [invert_Phi(Phe, Phe(K) - np.log(2 * q))
             + invert_Phi(Phe, Phe(2 * eps3 - K) - np.log(2 * (1 - q)))
             for K in Kgrid])
        osc = D.max() - D.min()
        hull_lo = min(Kgrid.min() - abs(a1), 2 * eps3 - Kgrid.max() - abs(a2))
        hull_hi = max(Kgrid.max(), 2 * eps3 - Kgrid.min())
        norm_pp = psi_pp(hull_lo)  # psi'' decreasing, max at left end
        bound = (eta / H0) * (Kgrid.max() - Kgrid.min()) \
            * (abs(a1) + abs(a2)) * norm_pp
        print(f"11. osc bound   : eta={eta}: osc D = {osc:.3e} <= "
              f"bound {bound:.3e}")
        assert osc <= bound * 1.05, "oscillation bound violated"

    # --- Check 12: the resolvent factor ----------------------------------
    n1 = np.max(np.abs(u1))
    amp = np.linalg.norm(np.linalg.inv(L0), np.inf)
    rn = np.max(np.abs(Rpsi))
    print(f"12. resolvent   : ||nu_1|| = {n1:.3f} <= ||L_0^-1|| ||R_psi|| "
          f"= {amp:.1f} * {rn:.4f} = {amp * rn:.3f}")
    assert n1 <= amp * rn * (1 + 1e-12)

    # --- Check 13: first-order path dependence and the null direction ----
    kap = 0.05
    psi_add = lambda K: -kap / G0(K)
    psi_geo = lambda K: -np.log(1.0 + kap / G0(K))
    _, R_add, _ = build_L0_Rpsi(nu0, psi_add)
    L_g, R_geo, idx_g = build_L0_Rpsi(nu0, psi_geo)
    n1_geo = np.max(np.abs(np.linalg.solve(L_g, -R_geo)))
    print(f"13. path tangent: additive null direction ||R|| = "
          f"{np.max(np.abs(R_add)):.2e} (nu_1 = 0 exactly); Phi-line to the "
          f"same endpoint ||R|| = {np.max(np.abs(R_geo)):.2e}, "
          f"||nu_1|| = {n1_geo:.2e}")
    assert np.max(np.abs(R_add)) < 1e-15
    assert np.max(np.abs(R_geo)) > 1e-4 and n1_geo > 1e-4

    # --- Check 14: the policy-sensitivity bound --------------------------
    Kmid = 0.5 * (min(K_all) + max(K_all))
    psi_c = lambda K: (psi_weibull(K) - psi_weibull(Kmid)
                       - (H0 * (np.log(1 + H0 * Kmid) + 1.0)) * (K - Kmid))
    L_c, R_c, idx_c = build_L0_Rpsi(nu0, psi_c)
    n1_c = np.max(np.abs(np.linalg.solve(L_c, -R_c)))
    Rn = np.max(np.abs(R_c))
    Gmax = max(G0(k) for k in K_all)
    Rad = max(abs(k - Kmid) for k in K_all)
    pp_max = max(H0 ** 2 / (1 + H0 * k) for k in K_all)
    bound_R = Gmax * Rad ** 2 * pp_max
    bound_n = amp * bound_R
    print(f"14. policy bound: ||nu_1|| = {n1_c:.4f} <= ||L0^-1|| ||R|| = "
          f"{amp * Rn:.4f} <= ||L0^-1|| Gmax R^2 ||psi''|| = {bound_n:.4f}")
    assert n1_c <= amp * Rn * (1 + 1e-12) <= bound_n * (1 + 1e-12)

    # submitted-quote version: m1 = D nu_1 - psi'(K0)/h^2, bounded by
    # (||D L0^-1|| Gmax R^2 + R/h^2) ||psi''||
    nu1_c = np.zeros(2 * N + 1)
    u_c = np.linalg.solve(L_c, -R_c)
    for x, j in idx_c.items():
        nu1_c[x + N] = u_c[j]
    psip_c = lambda K: psip(K) - psip(Kmid)
    Dp = np.zeros((2 * N - 1, 2 * N))
    Dm = np.zeros((2 * N - 1, 2 * N))
    for r_i, x in enumerate(range(-(N - 1), N)):
        if x + 1 != 0:
            Dp[r_i, idx_c[x + 1]] += 1.0 / S_LOT
        if x != 0:
            Dp[r_i, idx_c[x]] -= 1.0 / S_LOT
        if x - 1 != 0:
            Dm[r_i, idx_c[x - 1]] += 1.0 / S_LOT
        if x != 0:
            Dm[r_i, idx_c[x]] -= 1.0 / S_LOT
    Li = np.linalg.inv(L_c)
    opDp = np.linalg.norm(Dp @ Li, np.inf)
    opDm = np.linalg.norm(Dm @ Li, np.inf)
    m1_max = 0.0
    for x in range(-(N - 1), N):
        i = I0 + x
        Kdn0 = EPS + (nu0[i + 1] - nu0[i]) / S_LOT
        Kup0 = EPS + (nu0[i - 1] - nu0[i]) / S_LOT
        m1dn = (nu1_c[i + 1] - nu1_c[i]) / S_LOT - psip_c(Kdn0) / H0 ** 2
        m1up = (nu1_c[i - 1] - nu1_c[i]) / S_LOT - psip_c(Kup0) / H0 ** 2
        m1_max = max(m1_max, abs(m1dn), abs(m1up))
    q_bound = (max(opDp, opDm) * Gmax * Rad ** 2 + Rad / H0 ** 2) * pp_max
    print(f"    quote bound : ||m_1|| = {m1_max:.4f} <= "
          f"(||D L0^-1|| Gmax R^2 + R/h^2) ||psi''|| = {q_bound:.4f}")
    assert m1_max <= q_bound * (1 + 1e-12)

    # --- Check 15: one transformation, two representations ---------------
    def solve_balanced_cost(cst):
        def nu_of(u):
            return np.concatenate([u[::-1], [0.0], u])

        def res15(u):
            nu = nu_of(u)
            v0 = enquiry_value(G0, 0.5, nu, I0)
            r = [TAU * cst(x) / S_LOT
                 - (enquiry_value(G0, 0.5, nu, I0 + x) - v0)
                 for x in range(1, N)]
            r.append((nu[-1] - 2 * nu[-2] + nu[-3])
                     - (nu[-2] - 2 * nu[-3] + nu[-4]))
            return r

        sol = root(res15, 0.05 * np.arange(1, N + 1) ** 2, method="lm",
                   options={"maxiter": 60000, "xtol": 1e-15})
        return nu_of(sol.x)

    nu_c15 = solve_balanced_cost(cost)
    nu_imb15 = solve_imbalanced(G0, q, cost, nu_bal + delta * XS)

    def half_width15(nu, x):
        i = I0 + x
        mup = 1 / H0 + EPS + (nu[i - 1] - nu[i]) / S_LOT
        mdn = 1 / H0 + EPS + (nu[i + 1] - nu[i]) / S_LOT
        return 0.5 * (mup + mdn)

    w_imb = half_width15(nu_imb15, 0)
    w_Mc = half_width15(nu_bal, 0)
    w_c = half_width15(nu_c15, 0)
    print(f"15. two reps    : half-width imb {w_imb:.6f} = bal(Mc) "
          f"{w_Mc:.6f} (diff {abs(w_imb - w_Mc):.1e}); response over "
          f"bal(c) = {w_imb - w_c:.6f}, NOT gamma = {gamma:.6f}")
    assert abs(w_imb - w_Mc) < 1e-10, "imbalanced width != balanced-Mc width"
    assert abs(w_imb - w_c) < 0.2 * gamma, \
        "width response should be far below gamma here"

    print("all checks passed")


# NF16 (added after the base-paper correction): the affine constant kappa
# survives only two-sided closures. The one-sided boundary identity
# requires q*kappa = (D/2)*kappa, which fails for kappa != 0, q != 1/2:
# the corrected finite-state model's boundary rows single out B e^{-hK}.
import numpy as np
_q, _kap = 0.6, 0.7
_D = 2 * np.sqrt(_q * (1 - _q))
_gap = abs(_q * _kap - 0.5 * _D * _kap)
_gap0 = abs(_q * 0.0 - 0.5 * _D * 0.0)
assert _gap > 1e-2 and _gap0 == 0.0
print(f"NF16 PASS: one-sided rows force kappa = 0 "
      f"(q kappa - (D/2) kappa = {_gap:.4f} for kappa = 0.7; 0 for kappa = 0)")
