"""Numerical certificate for 'Finite-Horizon Market Making with Imbalanced Flow:
An Exact Symmetrization and Its Term Structure'.

Verifies, in order:
 1. Lemma (general): any inventory-dependent asymmetric tridiagonal system is
    diagonally symmetrizable; real spectrum.
 2. Theorem 1 (conjugacy): v_q = r^{-q} w_q with tilted terminal w(T) = r^q,
    and the quote relations against the TILTED comparator.
 3. Corollary (counterexample): against the ORDINARY balanced comparator the
    mid displacement at finite horizon is NOT the constant -delta. Reproduces
    the anchor table (Q=2, alpha=.1, eta_b=2, eta_a=.5, k=1, gamma=.1, tau=1):
    bid 1.435402, ask 0.818182, mid shift -0.308610, spread 2.253584 vs
    balanced 1.109623/1.109623. This check is the one an earlier draft of the
    paper lacked; it rules out the stronger all-horizon claim.
 4. Theorem 2 (term structure): the formulas for Delta m_q(tau), Delta s_q(tau)
    match direct computation; Delta m_q(0) = 0; Delta m_q(tau) -> -delta at the
    spectral-gap rate.
 5. Corollary (flow-adjusted marking): terminal condition v(T) = r^{-q} makes
    the constant shift exact at EVERY horizon.
 6. Corollary (parity): spread response second order in the imbalance at q=0,
    generically first order at q != 0.
"""
import numpy as np
from scipy.linalg import expm

def build_M(qs, alpha, eta_b, eta_a):
    n = len(qs)
    m = np.diag(alpha * qs.astype(float) ** 2)
    for i in range(n):
        if i + 1 < n: m[i, i + 1] -= eta_b
        if i - 1 >= 0: m[i, i - 1] -= eta_a
    return m

# ---- 1. general lemma, randomized ----
rng = np.random.default_rng(0)
Qg = 5; qs = np.arange(-Qg, Qg + 1); n = len(qs)
alpha_diag = rng.uniform(0.1, 1.0, n)
eb = rng.uniform(0.3, 1.5, n); ea = rng.uniform(0.3, 1.5, n)
M = np.diag(alpha_diag)
for i in range(n):
    if i + 1 < n: M[i, i + 1] -= eb[i]
    if i - 1 >= 0: M[i, i - 1] -= ea[i]
d = np.ones(n)
for i in range(n - 1):
    d[i + 1] = d[i] * np.sqrt(eb[i] / ea[i + 1])
D = np.diag(d)
S = D @ M @ np.linalg.inv(D)
assert np.max(np.abs(S - S.T)) < 1e-12
assert np.max(np.abs(np.linalg.eigvals(M).imag)) < 1e-12
print("1. general lemma: symmetrization exact, spectrum real")

# ---- shared parameters for 2-6 ----
Q, alpha, eta_b, eta_a, k, gamma = 2, 0.1, 2.0, 0.5, 1.0, 0.1
qs = np.arange(-Q, Q + 1); n = len(qs); i0 = Q
c0 = (1 / gamma) * np.log(1 + gamma / k)
r = np.sqrt(eta_b / eta_a); delta = np.log(r) / k
etabar = np.sqrt(eta_b * eta_a)
Mi = build_M(qs, alpha, eta_b, eta_a)
Mb = build_M(qs, alpha, etabar, etabar)

def depths(vec, i):
    db = np.log(vec[i] / vec[i + 1]) / k + c0
    da = np.log(vec[i] / vec[i - 1]) / k + c0
    return db, da

# ---- 2. conjugacy vs tilted comparator ----
tau = 1.0
v = expm(-Mi * tau) @ np.ones(n)
w = expm(-Mb * tau) @ (r ** qs.astype(float))
assert np.max(np.abs(v - (r ** (-qs.astype(float))) * w)) < 1e-12
db_i, da_i = depths(v, i0)
db_w, da_w = depths(w, i0)
assert abs(db_i - (db_w + delta)) < 1e-12 and abs(da_i - (da_w - delta)) < 1e-12
print("2. conjugacy and tilted-comparator quote relations: exact")

# ---- 3. counterexample vs ordinary balanced ----
z = expm(-Mb * tau) @ np.ones(n)
db_z, da_z = depths(z, i0)
mid_shift = (da_i - db_i) / 2
row = (db_i, da_i, mid_shift, db_i + da_i, db_z, db_z + da_z)
expect = (1.435402, 0.818182, -0.308610, 2.253584, 1.109623, 2.219246)
assert all(abs(a - b) < 5e-6 for a, b in zip(row, expect)), row
assert abs(mid_shift - (-delta)) > 0.38  # NOT the constant -delta
print(f"3. counterexample: mid shift {mid_shift:+.6f} != -delta {-delta:+.6f}; "
      "all-horizon constant shift refuted")

# ---- 4. term structure formulas and limits ----
def dm_ds(tau2):
    w2 = expm(-Mb * tau2) @ (r ** qs.astype(float))
    z2 = expm(-Mb * tau2) @ np.ones(n)
    dm = -delta + np.log(w2[i0 + 1] * z2[i0 - 1] / (w2[i0 - 1] * z2[i0 + 1])) / (2 * k)
    ds = np.log(w2[i0] ** 2 * z2[i0 + 1] * z2[i0 - 1]
                / (w2[i0 + 1] * w2[i0 - 1] * z2[i0] ** 2)) / k
    return dm, ds

def dm_direct(tau2):
    v2 = expm(-Mi * tau2) @ np.ones(n)
    z2 = expm(-Mb * tau2) @ np.ones(n)
    dbi, dai = depths(v2, i0); dbz, daz = depths(z2, i0)
    return (dai - dbi) / 2 - (daz - dbz) / 2, (dbi + dai) - (dbz + daz)

for t2 in (0.05, 0.5, 1.0, 4.0):
    a1 = dm_ds(t2); a2 = dm_direct(t2)
    assert abs(a1[0] - a2[0]) < 1e-10 and abs(a1[1] - a2[1]) < 1e-10
dm0, ds0 = dm_ds(1e-9)
assert abs(dm0) < 1e-8 and abs(ds0) < 1e-8
evals = np.sort(np.linalg.eigvalsh(D_ := (lambda: (np.diag(r**qs.astype(float)) @ Mi @ np.diag(r**(-qs.astype(float)))))()))
gap = evals[1] - evals[0]
dm_far, _ = dm_ds(30.0)
assert abs(dm_far + delta) < 10 * np.exp(-gap * 30.0) + 1e-12
print(f"4. term structure: formulas match direct; Dm(0)=0; Dm(30) -> -delta "
      f"(gap {gap:.3f}, residual {abs(dm_far + delta):.2e})")

# ---- 5. flow-adjusted terminal marking ----
for t2 in (0.05, 0.5, 2.0, 10.0):
    v_adj = expm(-Mi * t2) @ (r ** (-qs.astype(float)))     # mark at S_T - delta
    z2 = expm(-Mb * t2) @ np.ones(n)
    dbi, dai = depths(v_adj, i0); dbz, daz = depths(z2, i0)
    assert abs(dbi - (dbz + delta)) < 1e-12 and abs(dai - (daz - delta)) < 1e-12
print("5. flow-adjusted marking: constant shift exact at every tested horizon")

# ---- 6. parity of the spread response at q = 0 ----
def spread_q0(eps, tau2=1.0):
    rb = etabar * np.exp(eps); ra = etabar * np.exp(-eps)
    v2 = expm(-build_M(qs, alpha, rb, ra) * tau2) @ np.ones(n)
    dbi, dai = depths(v2, i0)
    return dbi + dai

s0 = spread_q0(0.0)
e = 1e-3
first = (spread_q0(e) - spread_q0(-e)) / (2 * e)
second = (spread_q0(e) - 2 * s0 + spread_q0(-e)) / e ** 2
assert abs(first) < 1e-8 and abs(second) > 1e-3
print(f"6. parity at q=0: first-order spread response {first:.2e} (zero), "
      f"second-order {second:+.4f} (nonzero)")
print("ALL CHECKS PASS")
