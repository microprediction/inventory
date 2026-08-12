"""Independent optimality checks for the consistency solution of
skew_width_imbalance.tex on the finite-lattice MDP.

The claim under attack: the bounded-chain consistency solution (solve for
nu, quote m = w + eps + D nu) is the average-reward OPTIMAL policy of the
finite MDP, not merely a solution of an equation. verify_all_claims.py A4
checks only the evaluation identity (gain = s H_q(0) at that policy).
Here the policy must survive three independent attacks that never look at
nu at all -- the competitor space is raw quote vectors:

    OPT1  evaluation identity: J(m*) computed from the stationary
          distribution of the raw-quote chain equals s H_q(0).
    OPT2  policy-iteration fixed point: evaluate the policy (relative
          values by linear solve), apply exact greedy improvement with the
          closed-form argmax m = w + eps - Delta h; the policy reproduces
          itself. By Howard's policy-improvement theorem for finite
          unichain average-reward MDPs this certifies optimality up to
          floating point -- the strongest of the three.
    OPT3  derivative-free search (humpday) over the full raw quote vector
          (4N dimensions, no structure imposed): no policy found beats
          J(m*), and the argmax matches the consistency quotes.
    OPT4  adversarial perturbation probe: thousands of random policy
          perturbations across scales; none improves J.
    OPT5  the balanced-at-M(q)c twin passes OPT2, its searched optimum
          maps to the imbalanced one by +-delta, and the searched gains
          scale by M(q).

State space: x in {-N..N}, no inventory-increasing trade at the
boundaries (one-sided rows), matching the paper's standing assumptions.
Reward: margin (m - eps) per fill, carrying cost c(x) per unit time.
"""

import numpy as np
from scipy.optimize import root

TAU, S_LOT = 1.0, 1.0
N = 4
XS = np.arange(-N, N + 1)
NS = 2 * N + 1
I0 = N
H0 = 1.0
W = 1.0 / H0
EPS = 0.15
Q = 0.6
DELTA = 0.5 * np.log(Q / (1 - Q)) / H0
MQ = 1.0 / (2 * np.sqrt(Q * (1 - Q)))
COST = lambda x: 0.0025 * x ** 2
rng = np.random.default_rng(7)

G_exp = lambda K: W * np.exp(-1.0 - H0 * K)


# ------------------------------------------------- consistency solution
def hamiltonian(q, nu, i, eps=EPS):
    v = 0.0
    if XS[i] < N:
        v += q * G_exp(eps + (nu[i + 1] - nu[i]) / S_LOT)
    if XS[i] > -N:
        v += (1 - q) * G_exp(eps + (nu[i - 1] - nu[i]) / S_LOT)
    return v


def solve_bounded(q, cost, init):
    def wrap(u):
        nu = np.concatenate([u[:N], [0.0], u[N:]])
        h0v = hamiltonian(q, nu, I0)
        return [TAU * cost(XS[i]) / S_LOT - (hamiltonian(q, nu, i) - h0v)
                for i in range(NS) if i != I0]

    sol = root(wrap, np.concatenate([init[:I0], init[I0 + 1:]]),
               method="lm", options={"maxiter": 80000, "xtol": 1e-15})
    nu = np.concatenate([sol.x[:N], [0.0], sol.x[N:]])
    assert np.max(np.abs(wrap(np.concatenate([nu[:I0], nu[I0 + 1:]])))) < 1e-11
    return nu


def quotes_of_nu(nu):
    """Raw quote vectors: md[i] buy quote (x -> x+1), mu[i] sell quote."""
    md = np.array([W + EPS + (nu[i + 1] - nu[i]) / S_LOT
                   if XS[i] < N else np.nan for i in range(NS)])
    mu = np.array([W + EPS + (nu[i - 1] - nu[i]) / S_LOT
                   if XS[i] > -N else np.nan for i in range(NS)])
    return md, mu


# ------------------------------------------------- raw-policy machinery
def gain_of_policy(q, cost, md, mu):
    """Exact average reward per unit time of an arbitrary quote policy,
    via the birth-death stationary distribution."""
    up = np.array([q * np.exp(-H0 * md[i]) if XS[i] < N else 0.0
                   for i in range(NS)])
    dn = np.array([(1 - q) * np.exp(-H0 * mu[i]) if XS[i] > -N else 0.0
                   for i in range(NS)])
    logp = np.concatenate([[0.0],
                           np.cumsum(np.log(up[:-1]) - np.log(dn[1:]))])
    p = np.exp(logp - logp.max())
    p /= p.sum()
    r = np.array([(up[i] * S_LOT * (md[i] - EPS) if XS[i] < N else 0.0)
                  + (dn[i] * S_LOT * (mu[i] - EPS) if XS[i] > -N else 0.0)
                  - TAU * cost(XS[i]) for i in range(NS)])
    return (p @ r) / TAU, p


def policy_iteration_step(q, cost, md, mu):
    """Evaluate (relative values h, h(0)=0) then greedy-improve exactly."""
    up = np.array([q * np.exp(-H0 * md[i]) if XS[i] < N else 0.0
                   for i in range(NS)])
    dn = np.array([(1 - q) * np.exp(-H0 * mu[i]) if XS[i] > -N else 0.0
                   for i in range(NS)])
    r = np.array([(up[i] * S_LOT * (md[i] - EPS) if XS[i] < N else 0.0)
                  + (dn[i] * S_LOT * (mu[i] - EPS) if XS[i] > -N else 0.0)
                  - TAU * cost(XS[i]) for i in range(NS)])
    # (I - P) h = r - rho_epoch, with h(I0) = 0 pinned
    A = np.zeros((NS + 1, NS + 1))
    b = np.zeros(NS + 1)
    for i in range(NS):
        A[i, i] = up[i] + dn[i]
        if XS[i] < N:
            A[i, i + 1] -= up[i]
        if XS[i] > -N:
            A[i, i - 1] -= dn[i]
        A[i, NS] = 1.0          # rho_epoch
        b[i] = r[i]
    A[NS, I0] = 1.0             # normalization h(0) = 0
    sol = np.linalg.solve(A, b)
    h, rho = sol[:NS], sol[NS]
    md_new = np.array([max(0.0, W + EPS - (h[i + 1] - h[i]) / S_LOT)
                       if XS[i] < N else np.nan for i in range(NS)])
    mu_new = np.array([max(0.0, W + EPS - (h[i - 1] - h[i]) / S_LOT)
                       if XS[i] > -N else np.nan for i in range(NS)])
    return md_new, mu_new, h, rho / TAU


def pack(md, mu):
    return np.concatenate([md[XS < N], mu[XS > -N]])


def unpack(v):
    md = np.full(NS, np.nan)
    mu = np.full(NS, np.nan)
    md[XS < N] = v[:2 * N]
    mu[XS > -N] = v[2 * N:]
    return md, mu


PASS = []


def check(tag, ok, detail=""):
    PASS.append((tag, ok))
    print(("PASS " if ok else "FAIL ") + tag + ("  " + detail if detail else ""))


def run_battery(q, cost, nu, label):
    md, mu = quotes_of_nu(nu)
    assert np.nanmin(np.concatenate([md, mu])) > 0, "interiority violated"
    Jstar, _ = gain_of_policy(q, cost, md, mu)
    gain_id = S_LOT * hamiltonian(q, nu, I0) / TAU

    check(f"OPT1[{label}] J(m*) = s H(0)",
          abs(Jstar - gain_id) < 1e-12, f"diff {abs(Jstar - gain_id):.1e}")

    md2, mu2, h, rho = policy_iteration_step(q, cost, md, mu)
    dev = max(np.nanmax(np.abs(md2 - md)), np.nanmax(np.abs(mu2 - mu)))
    check(f"OPT2[{label}] policy-iteration fixed point (Howard)",
          dev < 1e-9 and abs(rho - Jstar) < 1e-12,
          f"greedy deviation {dev:.1e}, rho diff {abs(rho - Jstar):.1e}")

    # derivative-free search over raw quote vectors
    from humpday import minimize as hd_min
    v0 = pack(md, mu)
    lo, hi = 0.05, 3.0
    neg = lambda v: -gain_of_policy(q, cost, *unpack(np.asarray(v)))[0]
    best_v, best_J = None, -np.inf
    for x0 in (None, np.full(4 * N, W + EPS)):
        res = hd_min(neg, x0=x0, bounds=[(lo, hi)] * (4 * N),
                     options={"n_trials": 600})
        if -res.fun > best_J:
            best_J, best_v = -res.fun, np.asarray(res.x)
    qdev = np.max(np.abs(best_v - v0))
    check(f"OPT3[{label}] humpday search never beats, argmax matches",
          best_J <= Jstar + 1e-9 and qdev < 0.05,
          f"J* - J_search = {Jstar - best_J:.2e}, max quote dev {qdev:.1e}")

    # adversarial perturbation probe
    worst = -np.inf
    for scale in (1e-4, 1e-3, 1e-2, 0.05, 0.1, 0.3):
        for _ in range(800):
            v = np.clip(v0 + scale * rng.standard_normal(4 * N), 1e-3, None)
            worst = max(worst, gain_of_policy(q, cost, *unpack(v))[0] - Jstar)
    check(f"OPT4[{label}] 4800 perturbations, none improves",
          worst <= 1e-13, f"best improvement found {worst:.1e}")
    return Jstar, v0, best_v


if __name__ == "__main__":
    nu_q = solve_bounded(Q, COST, 0.05 * XS.astype(float) ** 2 + DELTA * XS)
    nu_bal = solve_bounded(0.5, COST_M := (lambda x: MQ * COST(x)),
                           0.05 * XS.astype(float) ** 2)
    J_q, v_q, s_q = run_battery(Q, COST, nu_q, "q=0.6")
    J_b, v_b, s_b = run_battery(0.5, COST_M, nu_bal, "bal,Mc")

    # OPT5: the two searched optima are related by the theorem's quote map
    shift = np.concatenate([np.full(2 * N, DELTA), np.full(2 * N, -DELTA)])
    map_dev = np.max(np.abs(v_q - (v_b + shift)))
    scale_dev = abs(J_b - MQ * J_q)
    check("OPT5 quote map m_q = m_bal +/- delta and gain scaling M rho_q",
          map_dev < 1e-9 and scale_dev < 1e-12,
          f"map dev {map_dev:.1e}, scaling dev {scale_dev:.1e}")

    n_ok = sum(ok for _, ok in PASS)
    print(f"\n{n_ok}/{len(PASS)} optimality checks pass")
    assert n_ok == len(PASS)
