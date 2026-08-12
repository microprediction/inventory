"""The moving-price equivalence, certified.

Claim: if the fair price F_t is a martingale independent of enquiry
arrivals and the dealer quotes RELATIVE to it, the problem is equivalent
to the fixed-price model: cash P&L = model-frame margin flow + int x dF,
the second term has zero conditional expectation given any (state,
action), so every Bellman comparison -- hence the optimal policy -- is
unchanged, and with inventory bounded on the finite lattice the time
average of int x dF vanishes, so the long-run gain is the same rho*.

    M1  exact decomposition: cash P&L - model P&L = sum x dF, pathwise
        to machine precision.
    M2  the martingale term's time average -> 0 at the 1/sqrt(T) rate
        (slope of log-RMS vs log-T within 15 percent of -1/2).
    M3  gain invariance: simulated long-run cash gain matches the
        fixed-price gain rho* for the optimal policy AND for two
        deliberately suboptimal policies (the equivalence is about the
        accounting, not the optimizer), each within Monte Carlo error.
"""

import numpy as np

W, EPS, Q, N = 1.0, 0.15, 0.6, 6
NS, I0 = 2 * N + 1, N
XS = np.arange(-N, N + 1)
COST = lambda x: 0.0025 * x ** 2
rng = np.random.default_rng(5)


def pi_optimize(q, cost, eps):
    md = np.where(XS < N, W + eps, np.nan)
    mu = np.where(XS > -N, W + eps, np.nan)
    for _ in range(300):
        up = np.array([q * np.exp(-md[i]) if XS[i] < N else 0.0
                       for i in range(NS)])
        dn = np.array([(1 - q) * np.exp(-mu[i]) if XS[i] > -N else 0.0
                       for i in range(NS)])
        r = np.array([(up[i] * (md[i] - eps) if XS[i] < N else 0.0)
                      + (dn[i] * (mu[i] - eps) if XS[i] > -N else 0.0)
                      - cost(XS[i]) for i in range(NS)])
        A = np.zeros((NS + 1, NS + 1))
        b = np.zeros(NS + 1)
        for i in range(NS):
            A[i, i] = up[i] + dn[i]
            if XS[i] < N:
                A[i, i + 1] -= up[i]
            if XS[i] > -N:
                A[i, i - 1] -= dn[i]
            A[i, NS] = 1.0
            b[i] = r[i]
        A[NS, I0] = 1.0
        sol = np.linalg.solve(A, b)
        h, rho = sol[:NS], sol[NS]
        md2 = np.array([max(0.0, W + eps - (h[i + 1] - h[i]))
                        if XS[i] < N else np.nan for i in range(NS)])
        mu2 = np.array([max(0.0, W + eps - (h[i - 1] - h[i]))
                        if XS[i] > -N else np.nan for i in range(NS)])
        d = max(np.nanmax(np.abs(md2 - md)), np.nanmax(np.abs(mu2 - mu)))
        md, mu = md2, mu2
        if d < 1e-13:
            return md, mu, rho
    raise RuntimeError


def simulate(md, mu, T, sigma=0.5):
    """Enquiry-epoch simulation with a random-walk fair price. Returns
    (model P&L, cash P&L, sum of x dF) over T epochs."""
    x_i = I0
    F = 0.0
    pnl_model = pnl_cash = mart = 0.0
    inv_cash = 0.0            # cash paid/received at absolute prices
    for _ in range(T):
        dF = sigma * rng.choice([-1.0, 1.0])   # martingale, indep of fills
        mart += (x_i - I0) * dF
        F += dF
        pnl_model -= COST(XS[x_i])
        pnl_cash -= COST(XS[x_i])
        u = rng.random()
        if XS[x_i] < N and u < Q * np.exp(-md[x_i]):
            # dealer buys at F - md (seller pays the markdown), concedes EPS
            pnl_model += md[x_i] - EPS
            inv_cash -= (F - (md[x_i] - EPS))
            x_i += 1
        elif XS[x_i] > -N and u > 1 - (1 - Q) * np.exp(-mu[x_i]):
            pnl_model += mu[x_i] - EPS
            inv_cash += F + (mu[x_i] - EPS)
            x_i -= 1
    pnl_cash += inv_cash + (XS[x_i]) * F   # mark residual inventory at F
    return pnl_model, pnl_cash, mart


PASS = []


def check(tag, ok, detail=""):
    PASS.append(ok)
    print(("PASS " if ok else "FAIL ") + tag + ("  " + detail if detail else ""))


if __name__ == "__main__":
    md, mu, rho = pi_optimize(Q, COST, EPS)

    # M1: pathwise decomposition
    a, c, m = simulate(md, mu, 20000)
    check("M1 cash P&L = model P&L + sum x dF, pathwise",
          abs((c - a) - m) < 1e-8, f"decomposition residual {abs(c - a - m):.1e}")

    # M2: the martingale term's average vanishes at 1/sqrt(T)
    Ts = [400, 1600, 6400, 25600]
    rms = []
    for T in Ts:
        vals = [simulate(md, mu, T)[2] / T for _ in range(120)]
        rms.append(np.sqrt(np.mean(np.square(vals))))
    slope = np.polyfit(np.log(Ts), np.log(rms), 1)[0]
    check("M2 (1/T) sum x dF -> 0 at the 1/sqrt(T) rate",
          abs(slope + 0.5) < 0.15, f"log-log slope {slope:.3f}")

    # M3: gain invariance for optimal and suboptimal policies
    T, R = 40000, 60
    ok3, det = True, []
    for tag, md_p, mu_p in [
        ("optimal", md, mu),
        ("flat", np.where(XS < N, W + EPS, np.nan),
         np.where(XS > -N, W + EPS, np.nan)),
        ("wide", np.where(XS < N, W + EPS + 0.3, np.nan),
         np.where(XS > -N, W + EPS + 0.3, np.nan)),
    ]:
        # fixed-price gain of this policy (exact, via stationary dist)
        up = np.array([Q * np.exp(-md_p[i]) if XS[i] < N else 0.0
                       for i in range(NS)])
        dn = np.array([(1 - Q) * np.exp(-mu_p[i]) if XS[i] > -N else 0.0
                       for i in range(NS)])
        logp = np.concatenate([[0.0],
                               np.cumsum(np.log(up[:-1]) - np.log(dn[1:]))])
        p = np.exp(logp - logp.max())
        p /= p.sum()
        r = np.array([(up[i] * (md_p[i] - EPS) if XS[i] < N else 0.0)
                      + (dn[i] * (mu_p[i] - EPS) if XS[i] > -N else 0.0)
                      - COST(XS[i]) for i in range(NS)])
        g_exact = p @ r
        sims = [simulate(md_p, mu_p, T)[1] / T for _ in range(R)]
        z = (np.mean(sims) - g_exact) / (np.std(sims) / np.sqrt(R))
        det.append(f"{tag}: cash {np.mean(sims):.5f} vs fixed {g_exact:.5f} "
                   f"(z = {z:.1f})")
        ok3 &= abs(z) < 3.5
    check("M3 moving-price cash gain = fixed-price gain, optimal and "
          "suboptimal policies", ok3, "; ".join(det))

    # M4: "the dealer pays in risk" -- Ito isometry. Var(sum x dF) =
    # sigma^2 T E[x^2] exactly (x adapted, increments independent), so a
    # mean-variance dealer's entire price-risk from the frame change is a
    # quadratic inventory charge (gamma sigma^2/2) x^2 per unit time:
    # the model's c(x), with the frame choice costing nothing beyond it.
    T4, R4 = 1600, 400
    up = np.array([Q * np.exp(-md[i]) if XS[i] < N else 0.0
                   for i in range(NS)])
    dn = np.array([(1 - Q) * np.exp(-mu[i]) if XS[i] > -N else 0.0
                   for i in range(NS)])
    logp = np.concatenate([[0.0],
                           np.cumsum(np.log(up[:-1]) - np.log(dn[1:]))])
    p = np.exp(logp - logp.max())
    p /= p.sum()
    ex2 = p @ (XS.astype(float) ** 2)
    marts = [simulate(md, mu, T4)[2] for _ in range(R4)]
    v_hat = np.var(marts)
    v_iso = 0.25 * T4 * ex2          # sigma = 0.5
    z = (v_hat - v_iso) / (v_hat * np.sqrt(2.0 / R4))
    check("M4 Ito isometry: Var(sum x dF) = sigma^2 T E[x^2] -- price risk "
          "IS the quadratic inventory charge", abs(z) < 3.5,
          f"simulated {v_hat:.1f} vs isometry {v_iso:.1f} (z = {z:.1f})")

    assert all(PASS)
    print(f"\n{sum(PASS)}/{len(PASS)} moving-price equivalence checks pass")
