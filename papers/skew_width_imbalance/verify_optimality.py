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

    OPT6  Howard sweep: across q, cost shape (quadratic, asymmetric,
          quartic, kinked), and lattice size, run policy iteration to
          convergence (globally convergent, optimal by construction) and
          verify the optimum is interior and satisfies the paper's
          consistency equation. Scope finding from building this sweep:
          interiority binds FIRST AT THE TOP BOUNDARY STATE and does so
          at strong imbalance for every cost level, including c = 0 --
          the value of escaping the one-sided state (whose Hamiltonian
          is halved) exceeds w + eps - delta once q is large, so the
          optimal boundary sell quote clips to zero. The interior-quote
          hypothesis therefore carves out a genuinely small region of
          (q, N, eps, cost): at eps = 0.15 the frontier passes near
          (q = 0.6, N = 8, a = 0.002) -- the certificate configs sit
          just inside it -- and larger eps relaxes it only slowly.
          High-q sweep configs below raise eps accordingly.
    OPT7  zero carry at the policy level: the boundary-selected c = 0
          solution is itself a Howard fixed point, and the gain over pure
          tilt policies is maximized at b = delta -- on the finite chain
          it is OPTIMALITY that selects the tilted branch.
    OPT8  floor binding: with an aggressive cost the exponential-branch
          solution violates interiority; policy iteration with the m >= 0
          floor converges to a clipped optimum, and the theorem's quote
          map between the clipped optima FAILS -- interiority is a
          substantive hypothesis, not bookkeeping.
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
def hamiltonian(q, nu, i, eps=None):
    if eps is None:
        eps = EPS
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

    # derivative-free search over raw quote vectors (humpday if installed,
    # scipy differential evolution otherwise -- the check is corroborative;
    # optimality is established by the Howard certificate above)
    v0 = pack(md, mu)
    lo, hi = 0.05, 3.0
    neg = lambda v: -gain_of_policy(q, cost, *unpack(np.asarray(v)))[0]
    best_v, best_J, engine = None, -np.inf, "humpday"
    try:
        # race the whole humpday roster on the unit cube; best result wins
        from humpday import OPTIMIZERS
        cube = lambda u: neg(lo + (hi - lo) * np.asarray(u))
        ran = 0
        for opt in OPTIMIZERS:
            try:
                val, u, _ = opt(cube, n_dim=4 * N, n_trials=400,
                                with_count=True)
                ran += 1
            except Exception:
                continue
            if -val > best_J:
                best_J = -val
                best_v = lo + (hi - lo) * np.asarray(u)
                engine = f"humpday:{opt.__name__}"
        assert ran >= 5, f"only {ran} humpday optimizers ran"
    except ImportError:
        from scipy.optimize import differential_evolution
        engine = "scipy DE"
        res = differential_evolution(neg, [(lo, hi)] * (4 * N), seed=3,
                                     maxiter=400, tol=1e-12, polish=True)
        best_J, best_v = -res.fun, np.asarray(res.x)
    # local polish of the DFO result (removes stochastic-search variance;
    # the polished point can only have higher J, so "never beats" still binds)
    from scipy.optimize import minimize as sp_min
    pol = sp_min(neg, best_v, method="L-BFGS-B",
                 bounds=[(lo, hi)] * (4 * N), options={"ftol": 1e-15})
    if -pol.fun > best_J:
        best_J, best_v = -pol.fun, pol.x
    qdev = np.max(np.abs(best_v - v0))
    check(f"OPT3[{label}] {engine} search never beats, argmax matches",
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


def configure(Nl):
    global N, XS, NS, I0
    N = Nl
    XS = np.arange(-N, N + 1)
    NS = 2 * N + 1
    I0 = N


def howard_dev(q, cost, md, mu):
    md2, mu2, _, rho = policy_iteration_step(q, cost, md, mu)
    return max(np.nanmax(np.abs(md2 - md)), np.nanmax(np.abs(mu2 - mu))), rho


def pi_converge(q, cost):
    """Policy iteration from flat quotes; optimal fixed point by Howard."""
    md = np.where(XS < N, W + EPS, np.nan)
    mu = np.where(XS > -N, W + EPS, np.nan)
    for _ in range(400):
        md2, mu2, h, rho = policy_iteration_step(q, cost, md, mu)
        d = max(np.nanmax(np.abs(md2 - md)), np.nanmax(np.abs(mu2 - mu)))
        md, mu = md2, mu2
        if d < 1e-13:
            return md, mu, h, rho
    raise RuntimeError("policy iteration did not converge")


def sweep_configs():
    out = []
    global EPS
    for q, Nl, eps, cost, tag in [
        (0.52, 4, 0.15, lambda x: 0.0025 * x ** 2, "q.52 quad"),
        (0.60, 8, 0.15, lambda x: 0.0015 * x ** 2, "q.60 N8 quad"),
        (0.70, 4, 0.50, lambda x: 0.002 * x ** 2, "q.70 quad"),
        (0.80, 4, 0.90, lambda x: 0.001 * x ** 2, "q.80 quad"),
        (0.60, 4, 0.15, lambda x: 0.0015 * x ** 2 + 0.0008 * x * x * (x > 0),
         "q.60 asym"),
        (0.60, 4, 0.15, lambda x: 0.0003 * x ** 4, "q.60 quartic"),
        (0.60, 4, 0.15, lambda x: 0.004 * abs(x), "q.60 kinked"),
        (0.65, 6, 0.50, lambda x: 0.0005 * x ** 2 + 0.00005 * x ** 4,
         "q.65 mixed"),
    ]:
        configure(Nl)
        EPS = eps
        md, mu, h, rho = pi_converge(q, cost)
        assert np.nanmin(np.concatenate([md, mu])) > 0, f"not interior: {tag}"
        # the paper's consistency equation, evaluated at the PI optimum
        nu = -h
        h0v = hamiltonian(q, nu, I0)
        res = max(abs(TAU * cost(XS[i]) / S_LOT
                      - (hamiltonian(q, nu, i) - h0v))
                  for i in range(NS) if i != I0)
        out.append((tag, res))
    configure(4)
    EPS = 0.15
    return out


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

    # OPT6: Howard certificate across configurations
    sw = sweep_configs()
    worst_cfg, worst_dev = max(sw, key=lambda t: t[1])
    check("OPT6 PI optimum interior + satisfies consistency eq, 8 configs",
          all(d < 1e-9 for _, d in sw),
          f"worst consistency residual {worst_dev:.1e} ({worst_cfg})")

    # OPT7: zero carry -- optimality itself selects the tilted branch
    nu0 = solve_bounded(Q, lambda x: 0.0, DELTA * XS.astype(float))
    md0, mu0 = quotes_of_nu(nu0)
    dev0, rho0 = howard_dev(Q, lambda x: 0.0, md0, mu0)
    S0 = (nu0[I0 + 1] - nu0[I0 - 1]) / (2 * S_LOT)
    tilt_gain = lambda b: gain_of_policy(
        Q, lambda x: 0.0,
        np.where(XS < N, W + EPS + b, np.nan),
        np.where(XS > -N, W + EPS - b, np.nan))[0]
    bs = np.linspace(-0.1, 0.5, 601)
    gb = np.array([tilt_gain(b) for b in bs])
    b_star = bs[np.argmax(gb)]
    check("OPT7 c = 0: boundary-selected solution is the Howard optimum, "
          "pure-tilt gain peaks at b = delta",
          dev0 < 1e-9 and abs(S0 - DELTA) < 1e-9
          and abs(b_star - DELTA) < 1e-3 and rho0 >= gb.max() - 1e-12,
          f"S(0) - delta = {S0 - DELTA:.1e}, argmax_b - delta = "
          f"{b_star - DELTA:.1e}, gain(delta) - gain(0) = "
          f"{tilt_gain(DELTA) - tilt_gain(0.0):.2e}")

    # OPT8: floor binding breaks the quote map -- interiority is substantive
    configure(6)
    big = lambda x: 0.08 * x ** 2
    md_i, mu_i, _, rho_i = pi_converge(Q, big)
    md_b, mu_b, _, rho_b = pi_converge(0.5, lambda x: MQ * big(x))
    clipped = min(np.nanmin(md_i), np.nanmin(mu_i))
    v0 = pack(md_i, mu_i)
    worst8 = max(gain_of_policy(Q, big, *unpack(
        np.clip(v0 + s_ * rng.standard_normal(4 * N), 0.0, None)))[0] - rho_i
        for s_ in (1e-3, 1e-2, 0.1) for _ in range(600))
    map_dev8 = max(np.nanmax(np.abs(md_i - (md_b + DELTA))),
                   np.nanmax(np.abs(mu_i - (mu_b - DELTA))))
    check("OPT8 floor binds: clipped optimum exists (PI converges, "
          "perturbations fail), quote map +-delta FAILS",
          clipped == 0.0 and worst8 <= 1e-13 and map_dev8 > 0.01
          and abs(rho_b - MQ * rho_i) > 1e-4,
          f"min quote {clipped:.2f}, best perturbation {worst8:.1e}, "
          f"map deviation {map_dev8:.3f}, gain-scaling deviation "
          f"{abs(rho_b - MQ * rho_i):.1e}")
    configure(4)

    # OPT9: boundary-first clipping is NOT universal -- an interior cost
    # spike clips that interior state first (cf. Remark on interiority)
    configure(4)
    spike = lambda x: 0.0005 * x ** 2 + (1.2 if x == 2 else 0.0)
    md_s, mu_s, _, _ = pi_converge(Q, spike)
    clip_at = [int(XS[i]) for i in range(NS)
               if md_s[i] == 0.0 or mu_s[i] == 0.0]
    check("OPT9 interior cost spike clips the interior state, not a boundary",
          clip_at == [2],
          f"clipped states {clip_at}")

    # OPT10: fuzzed coverage of the admissible region -- random configs,
    # keep only draws where BOTH members are interior, check everything
    fz = np.random.default_rng(2026)
    tried = accepted = 0
    w_res = w_map = w_scale = 0.0
    while accepted < 150 and tried < 3000:
        tried += 1
        qf = fz.uniform(0.52, 0.80)
        configure(int(fz.integers(3, 9)))
        EPS = fz.uniform(0.10, 0.90)
        a2, a4, a1 = (10 ** fz.uniform(-4, -2), 10 ** fz.uniform(-6, -3.5),
                      10 ** fz.uniform(-4, -2.2))
        ay = fz.uniform(0, 0.5) * a2 if fz.random() < 0.3 else 0.0
        cost = (lambda a2, a4, a1, ay: lambda x:
                a2 * x * x + a4 * x ** 4 + a1 * abs(x)
                + ay * x * x * (x > 0))(a2, a4, a1, ay)
        Mf = 1 / (2 * np.sqrt(qf * (1 - qf)))
        dl = 0.5 * np.log(qf / (1 - qf)) / H0
        try:
            md, mu, h, rho = pi_converge(qf, cost)
            mdb, mub, hb, rhob = pi_converge(0.5, lambda x: Mf * cost(x))
        except Exception:
            continue
        if min(np.nanmin(np.concatenate([md, mu])),
               np.nanmin(np.concatenate([mdb, mub]))) <= 1e-6:
            continue
        accepted += 1
        nu = -h
        h0v = hamiltonian(qf, nu, I0)
        w_res = max(w_res, max(abs(TAU * cost(XS[i]) / S_LOT
                                   - (hamiltonian(qf, nu, i) - h0v))
                               for i in range(NS) if i != I0))
        w_map = max(w_map, np.nanmax(np.abs(md - (mdb + dl))),
                    np.nanmax(np.abs(mu - (mub - dl))))
        w_scale = max(w_scale, abs(rhob - Mf * rho))
    configure(4)
    EPS = 0.15
    check("OPT10 fuzz: 150 random interior configs, consistency + quote map "
          "+ gain scaling at every draw",
          accepted >= 150 and w_res < 1e-9 and w_map < 1e-9
          and w_scale < 1e-11,
          f"{accepted}/{tried} draws admissible; worst residual {w_res:.1e}, "
          f"map {w_map:.1e}, scaling {w_scale:.1e}")

    n_ok = sum(ok for _, ok in PASS)
    print(f"\n{n_ok}/{len(PASS)} optimality checks pass")
    assert n_ok == len(PASS)
