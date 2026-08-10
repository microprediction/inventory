"""Numerical certificate for the finite-horizon imbalance equivalence (roadmap P1).

GLFT (2012) reduce the Avellaneda-Stoikov HJB with exponential fill
intensities to a linear ODE system. With asymmetric side scales A_b != A_a:

    vdot_q = alpha q^2 v_q - eta_b v_{q+1} - eta_a v_{q-1},   v_q(T) = 1,

with eta_s = A_s (1+gamma/k)^{-(1+k/gamma)}, alpha = k gamma sigma^2 / 2, and
missing neighbors dropped at the inventory bounds.

THEOREM (verified here to machine precision). Let r = sqrt(eta_b/eta_a) and
etabar = sqrt(eta_b eta_a). Conjugation by D = diag(r^q) maps the asymmetric
system EXACTLY (boundary rows included) onto the balanced system at the
geometric-mean intensity etabar, with terminal condition w_q(T) = r^q.
Consequently v_q(t) = r^{-q} w_q(t) for all t, and the optimal quotes satisfy

    delta_b_imb(t,q) = delta_b_bal(t,q) + (1/2k) ln(A_b/A_a)
    delta_a_imb(t,q) = delta_a_bal(t,q) - (1/2k) ln(A_b/A_a)

i.e. the mid shifts by the SAME (w/2) log-odds constant as the ergodic
theorem, at every horizon and inventory, with w = 1/k. The tilted terminal
condition w_q(T) = r^q means, in original variables, that the balanced dealer
marks terminal inventory at fair value shifted by that same constant. The
ergodic paper's theorem is the T -> infinity limit (Perron eigenvector).
The activity of the equivalent balanced market is 2 sqrt(p(1-p)) times the
original total (p = A_b/(A_b+A_a)): the carry multiplier M(p), again.
"""
import numpy as np

k, gamma, sigma = 1.0, 0.1, 1.0
A_b, A_a = 1.3, 0.7
Q, T = 6, 1.0
alpha = k * gamma * sigma**2 / 2
C = (1 + gamma/k) ** (-(1 + k/gamma))
eta_b, eta_a = A_b * C, A_a * C
r = np.sqrt(eta_b / eta_a)
etabar = np.sqrt(eta_b * eta_a)
qs = np.arange(-Q, Q+1); n = len(qs)

def M(eb, ea):
    m = np.diag(alpha * qs.astype(float)**2)
    for i in range(n):
        if i+1 < n: m[i, i+1] -= eb
        if i-1 >= 0: m[i, i-1] -= ea
    return m

D = np.diag(r**qs.astype(float)); Dinv = np.diag(r**(-qs.astype(float)))
assert np.max(np.abs(D @ M(eta_b, eta_a) @ Dinv - M(etabar, etabar))) < 1e-12

def solve(mat, vT, T, steps=4000):
    v = vT.astype(float).copy(); dt = T/steps; out = [v.copy()]
    for _ in range(steps):
        f = lambda x: mat @ x
        k1=f(v); k2=f(v-dt/2*k1); k3=f(v-dt/2*k2); k4=f(v-dt*k3)
        v = v - dt/6*(k1+2*k2+2*k3+k4); out.append(v.copy())
    return np.array(out[::-1])

v_imb = solve(M(eta_b, eta_a), np.ones(n), T)
w_bal = solve(M(etabar, etabar), r**qs.astype(float), T)
recon = (r**(-qs.astype(float)))[None,:] * w_bal
assert np.max(np.abs(v_imb - recon)) < 1e-10

lnr_k = np.log(r)/k
db_imb = (np.log(v_imb[:,:-1]) - np.log(v_imb[:,1:]))/k
db_bal = (np.log(w_bal[:,:-1]) - np.log(w_bal[:,1:]))/k
assert np.max(np.abs(db_imb - (db_bal + lnr_k))) < 1e-10
p = A_b/(A_b+A_a)
assert abs(lnr_k - (1/k)/2*np.log(p/(1-p))) < 1e-12
print("finite-horizon equivalence: all assertions pass at machine precision")
print("skew shift (all t, q):", lnr_k, "= (w/2) log-odds with w=1/k")
print("activity ratio arith/geom:", (eta_b+eta_a)/(2*etabar), "= 1/(2 sqrt(p(1-p)))")
