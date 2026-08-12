"""Exact symbolic verification (sympy) of every purely algebraic identity
in skew_width_imbalance.tex. These are not floating-point checks: each
identity is reduced to zero by exact simplification, closing the
"it's still floating point" objection for everything that is algebra.

    S1  FOC: argmax_m (m-K)e^{-hm} = 1/h + K, value G(K) = (1/h)e^{-1-hK}
    S2  the imbalance identity q e^{-hS} + (1-q)e^{hS}
        = 2 sqrt(q(1-q)) cosh(h(S - delta)),  delta = log(q/(1-q))/(2h)
    S3  termwise Hamiltonian scaling (the proof's engine):
        q G(K + delta) = (D/2) G(K),  (1-q) G(K - delta) = (D/2) G(K)
    S4  M(q) = e^{h gamma}, D(q) M(q) = 1
    S5  parity: delta(1-q) = -delta(q), M(1-q) = M(q)
    S6  the integrability identity S(x+s) - S(x) = C(x) + C(x+s)
    S7  width-response sensitivity: from the quadratic-family relation
        e^{-hC0} C0^2 = k a,  dC0/d log a = C0 / (2 - h C0)
"""

import sympy as sp

h, K, S, m, s, t = sp.symbols("h K S m s t", positive=True)
t = sp.Symbol("t", real=True)  # log-odds/2: q = e^t/(e^t + e^-t) in (0,1)
q = sp.exp(t) / (sp.exp(t) + sp.exp(-t))
delta = t / h                       # = log(q/(1-q))/(2h)
D = 2 * sp.sqrt(q * (1 - q))
M = 1 / D
gamma = sp.log(M) / h
G = lambda k: sp.exp(-1 - h * k) / h
check0 = sp.simplify(delta - sp.log(q / (1 - q)) / (2 * h))

checks = []


def check(tag, expr):
    ok = sp.simplify(expr) == 0
    checks.append(ok)
    print(("PASS " if ok else "FAIL ") + tag)


# S1: first-order condition and value
mstar = sp.solve(sp.diff((m - K) * sp.exp(-h * m), m), m)[0]
check("S1 argmax m = 1/h + K", mstar - (1 / h + K))
check("S1 value G(K) = (1/h)e^{-1-hK}",
      (mstar - K) * sp.exp(-h * mstar) - G(K))

# S0: the parameterization is faithful
check("S0 delta = log(q/(1-q))/(2h) under q = e^t/(e^t+e^-t)", check0)

# S2: the imbalance identity
lhs = q * sp.exp(-h * S) + (1 - q) * sp.exp(h * S)
rhs = D * sp.cosh(h * (S - delta))
check("S2 imbalance identity (cosh form)",
      sp.simplify(sp.expand(sp.powsimp((lhs - rhs).rewrite(sp.exp),
                                       force=True))))

# S3: termwise Hamiltonian scaling
check("S3 q G(K + delta) = (D/2) G(K)",
      sp.simplify(q * G(K + delta) - D / 2 * G(K)))
check("S3 (1-q) G(K - delta) = (D/2) G(K)",
      sp.simplify((1 - q) * G(K - delta) - D / 2 * G(K)))

# S4: multiplier and clock
check("S4 M = e^{h gamma}", sp.simplify(M - sp.exp(h * gamma)))
check("S4 D M = 1", sp.simplify(D * M - 1))

# S5: parity
check("S5 delta(1-q) = -delta(q)  (t -> -t)",
      sp.simplify(delta.subs(t, -t) + delta))
check("S5 M(1-q) = M(q)  (t -> -t)", sp.simplify(M.subs(t, -t) - M))

# S6: integrability identity from the difference-quotient definitions
x = sp.Symbol("x")
nu = sp.Function("nu")
Sf = lambda y: (nu(y + s) - nu(y - s)) / (2 * s)
Cf = lambda y: (nu(y + s) - 2 * nu(y) + nu(y - s)) / (2 * s)
check("S6 S(x+s) - S(x) = C(x) + C(x+s)",
      sp.expand(Sf(x + s) - Sf(x) - Cf(x) - Cf(x + s)))

# S7: implicit differentiation of e^{-hC0} C0^2 = k a
a, k = sp.symbols("a k", positive=True)
C0 = sp.Function("C0", positive=True)(a)
rel = sp.exp(-h * C0) * C0 ** 2 - k * a
dC0 = sp.solve(sp.diff(rel, a), sp.Derivative(C0, a))[0]
check("S7 dC0/dlog a = C0/(2 - h C0)",
      sp.simplify(a * dC0 - C0 / (2 - h * C0)).subs(k, sp.exp(-h * C0) * C0 ** 2 / a))

assert all(checks), "symbolic check failed"
print(f"\n{sum(checks)}/{len(checks)} symbolic identities exact")
