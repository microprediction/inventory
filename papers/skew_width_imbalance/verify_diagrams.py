"""Every commutative diagram of the symmetry, certified from DIRECTLY
OPTIMIZED strategies only.

Nothing in this file touches the consistency solver or any nu-based
construction. Every policy is obtained by exact policy iteration from a
FLAT cold start (all quotes w + eps), which is direct optimization over
raw quote vectors: each iteration evaluates the incumbent (linear solve)
and greedily improves it, and the Howard fixed point it terminates at is
the average-reward optimum of the finite MDP. The diagrams are then
checked between independently optimized corners:

    D1  the tilt square: optimize (q, c) and (1/2, M(q)c) independently;
        the two optima satisfy the quote map m_q = m_bal +/- delta,
        equal widths, mid displacement -delta, and gain scaling
        rho_bal = M(q) rho_q.
    D2  the time-change diagram: from the same two optimized policies,
        the generator identity L_{q,c} = D(q) L_{1/2,Mc} holds termwise;
        the embedded jump chains coincide; the stationary inventory
        distributions coincide; carry per effective transition is equal.
    D3  the overhead square: optimize the balanced problem with overhead
        eps + gamma and UNSCALED cost c; its optimum maps to the
        imbalanced one by m_q(down) = m_over(down) + delta - gamma,
        m_q(up) = m_over(up) - delta - gamma, with EQUAL gain and with
        the overhead width exceeding the physical width by exactly
        2 gamma: the "widening by gamma" lives in the overhead frame
        and only there, once.
    D4  the parity square: optimize (1-q, c) independently; skews differ
        by 2 delta at every two-sided state, convexities and widths
        agree, gains agree.
    D5  the CWLS corner as an optimality statement: with the compatible
        cosh-shaped carrying cost, the directly optimized policy has
        constant width and affine mid displacement -2ax on central
        states, with the boundary-layer deviation shrinking sharply as the
        caps recede (~600x from N = 8 to N = 12).
    D6  the flat-book corollary as an optimality statement: under an
        even cost the directly optimized imbalanced policy's mid at
        zero inventory sits exactly delta below fair.
"""

import numpy as np

TAU, S_LOT, H0, W = 1.0, 1.0, 1.0, 1.0
Q = 0.6
DELTA = 0.5 * np.log(Q / (1 - Q)) / H0
MQ = 1.0 / (2 * np.sqrt(Q * (1 - Q)))
DQ = 1.0 / MQ
GAMMA = np.log(MQ) / H0
N = 6
NS = 2 * N + 1
I0 = N
XS = np.arange(-N, N + 1)
COST = lambda x: 0.0025 * x ** 2


def configure(Nl):
    global N, NS, I0, XS
    N, NS, I0, XS = Nl, 2 * Nl + 1, Nl, np.arange(-Nl, Nl + 1)


def pi_optimize(q, cost, eps):
    """Exact policy iteration from a flat cold start; returns the Howard
    fixed point (the average-reward optimal raw quote vectors) and gain."""
    md = np.where(XS < N, W + eps, np.nan)
    mu = np.where(XS > -N, W + eps, np.nan)
    for _ in range(500):
        up = np.array([q * np.exp(-H0 * md[i]) if XS[i] < N else 0.0
                       for i in range(NS)])
        dn = np.array([(1 - q) * np.exp(-H0 * mu[i]) if XS[i] > -N else 0.0
                       for i in range(NS)])
        r = np.array([(up[i] * S_LOT * (md[i] - eps) if XS[i] < N else 0.0)
                      + (dn[i] * S_LOT * (mu[i] - eps) if XS[i] > -N else 0.0)
                      - TAU * cost(XS[i]) for i in range(NS)])
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
        md2 = np.array([max(0.0, W + eps - (h[i + 1] - h[i]) / S_LOT)
                        if XS[i] < N else np.nan for i in range(NS)])
        mu2 = np.array([max(0.0, W + eps - (h[i - 1] - h[i]) / S_LOT)
                        if XS[i] > -N else np.nan for i in range(NS)])
        d = max(np.nanmax(np.abs(md2 - md)), np.nanmax(np.abs(mu2 - mu)))
        md, mu = md2, mu2
        if d < 1e-13:
            assert np.nanmin(np.concatenate([md, mu])) > 0, "not interior"
            return md, mu, rho / TAU
    raise RuntimeError("policy iteration did not converge")


def rates(q, md, mu):
    up = np.array([q * np.exp(-H0 * md[i]) / TAU if XS[i] < N else 0.0
                   for i in range(NS)])
    dn = np.array([(1 - q) * np.exp(-H0 * mu[i]) / TAU if XS[i] > -N else 0.0
                   for i in range(NS)])
    return up, dn


def stationary(up, dn):
    logp = np.concatenate([[0.0], np.cumsum(np.log(up[:-1]) - np.log(dn[1:]))])
    p = np.exp(logp - logp.max())
    return p / p.sum()


PASS = []


def check(tag, ok, detail=""):
    PASS.append(ok)
    print(("PASS " if ok else "FAIL ") + tag + ("  " + detail if detail else ""))


if __name__ == "__main__":
    EPS = 0.15
    md_q, mu_q, rho_q = pi_optimize(Q, COST, EPS)
    md_b, mu_b, rho_b = pi_optimize(0.5, lambda x: MQ * COST(x), EPS)

    # D1: the tilt square between independent optima
    two = [i for i in range(NS) if 0 < i < NS - 1]
    map_dev = max(np.nanmax(np.abs(md_q - (md_b + DELTA))),
                  np.nanmax(np.abs(mu_q - (mu_b - DELTA))))
    w_dev = max(abs((md_q[i] + mu_q[i]) - (md_b[i] + mu_b[i])) for i in two)
    mid_dev = max(abs((mu_q[i] - md_q[i]) / 2 - ((mu_b[i] - md_b[i]) / 2
                                                 - DELTA)) for i in two)
    check("D1 tilt square: quote map, width, mid, gain scaling",
          map_dev < 1e-11 and w_dev < 1e-11 and mid_dev < 1e-11
          and abs(rho_b - MQ * rho_q) < 1e-13,
          f"map {map_dev:.1e}, width {w_dev:.1e}, mid {mid_dev:.1e}, "
          f"scaling {abs(rho_b - MQ * rho_q):.1e}")

    # D2: the time-change diagram from the same two optima
    up_q, dn_q = rates(Q, md_q, mu_q)
    up_b, dn_b = rates(0.5, md_b, mu_b)
    gen_dev = max(np.max(np.abs(up_q - DQ * up_b)),
                  np.max(np.abs(dn_q - DQ * dn_b)))
    with np.errstate(invalid="ignore", divide="ignore"):
        emb_q = up_q / (up_q + dn_q)
        emb_b = up_b / (up_b + dn_b)
    emb_dev = np.nanmax(np.abs(emb_q - emb_b))
    st_dev = np.max(np.abs(stationary(up_q, dn_q) - stationary(up_b, dn_b)))
    # carry per effective transition: c(x)/(rate_q) vs M c(x)/(rate_b)
    carry_dev = max(abs(COST(XS[i]) / (up_q[i] + dn_q[i])
                        - MQ * COST(XS[i]) / (up_b[i] + dn_b[i]))
                    for i in range(NS) if XS[i] != 0)
    check("D2 time change: generator, embedded chain, stationary, carry",
          gen_dev < 1e-12 and emb_dev < 1e-12 and st_dev < 1e-12
          and carry_dev < 1e-12,
          f"generator {gen_dev:.1e}, embedded {emb_dev:.1e}, "
          f"stationary {st_dev:.1e}, carry {carry_dev:.1e}")

    # D3: the overhead square -- eps + gamma, UNSCALED cost, EQUAL gain
    md_o, mu_o, rho_o = pi_optimize(0.5, COST, EPS + GAMMA)
    o_dev = max(np.nanmax(np.abs(md_q - (md_o + DELTA - GAMMA))),
                np.nanmax(np.abs(mu_q - (mu_o - DELTA - GAMMA))))
    ow_dev = max(abs((md_o[i] + mu_o[i]) - (md_q[i] + mu_q[i])
                     - 2 * GAMMA) for i in two)
    check("D3 overhead square: quote map, equal gain, overhead width = "
          "physical width + 2 gamma",
          o_dev < 1e-11 and abs(rho_o - rho_q) < 1e-13 and ow_dev < 1e-11,
          f"map {o_dev:.1e}, gain diff {abs(rho_o - rho_q):.1e}, "
          f"2-gamma width {ow_dev:.1e}")

    # D4: the parity square -- optimize (1-q, c) independently
    md_p, mu_p, rho_p = pi_optimize(1 - Q, COST, EPS)
    S_q = [(mu_q[i] - md_q[i]) / 2 for i in two]
    S_p = [(mu_p[i] - md_p[i]) / 2 for i in two]
    par_dev = max(abs((S_q[k] - S_p[k]) - (-2 * DELTA))
                  for k in range(len(two)))
    wpar_dev = max(abs((md_q[i] + mu_q[i]) - (md_p[i] + mu_p[i]))
                   for i in two)
    check("D4 parity square: S_q - S_{1-q} = 2 delta, widths and gains equal",
          par_dev < 1e-11 and wpar_dev < 1e-11
          and abs(rho_p - rho_q) < 1e-13,
          f"skew {par_dev:.1e}, width {wpar_dev:.1e}, "
          f"gain diff {abs(rho_p - rho_q):.1e}")

    # D5: the CWLS corner as an optimality statement (mid displacement of
    # the nu = a x^2 policy is -S = -2ax; boundary layer decays as the
    # caps recede)
    a = 0.04
    A5 = np.exp(-1 - H0 * EPS) / H0 * np.exp(-H0 * a)
    cosh_cost = lambda x: (S_LOT / TAU) * A5 * (np.cosh(2 * H0 * a * x) - 1)
    devs = {}
    for Nl in (8, 12):
        configure(Nl)
        md_c, mu_c, _ = pi_optimize(0.5, cosh_cost, EPS)
        idx = [i for i in range(NS) if abs(XS[i]) <= 4]
        widths = [md_c[i] + mu_c[i] for i in idx]
        devs[Nl] = max(max(widths) - min(widths),
                       max(abs((mu_c[i] - md_c[i]) / 2 + 2 * a * XS[i])
                           for i in idx))
    configure(6)
    check("D5 CWLS corner: optimized policy is constant-width/affine-mid "
          "on central states, boundary layer shrinks sharply with N",
          devs[12] < 5e-5 and devs[8] / devs[12] > 100,
          f"central deviation {devs[8]:.1e} (N=8) -> {devs[12]:.1e} (N=12), "
          f"ratio {devs[8] / devs[12]:.0f}")

    # D6: the flat-book corollary as an optimality statement
    mid0 = (mu_q[I0] - md_q[I0]) / 2
    check("D6 flat book: optimized mid at x = 0 sits exactly delta below "
          "fair (even cost)", abs(mid0 - (-DELTA)) < 1e-12,
          f"mid + delta = {mid0 + DELTA:.1e}")

    n_ok = sum(PASS)
    print(f"\n{n_ok}/{len(PASS)} diagram certificates pass "
          f"(all corners directly optimized, no consistency solver)")
    assert n_ok == len(PASS)
