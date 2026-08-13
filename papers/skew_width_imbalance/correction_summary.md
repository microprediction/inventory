# Correction package v2: skew_width_imbalance (2026-08-12)

Supersedes the seven-edit patch. The revision is structural at the statement
layer; the core algebraic reduction in the proof remains valid, and the proof
now derives the theorem from the full average-reward equation via the
termwise Hamiltonian scaling H_q = D(q) H_bal, which covers the one-sided
boundary rows explicitly (the cosh identity remains as the two-sided scalar
manifestation).

## The error ledger

One central interpretation error. The submitted Theorem 1 treated the
carrying-cost multiplier M(q)c and the overhead displacement eps -> eps + gamma
as simultaneous corrections. They are two representations of the same factor
e^{h gamma}; the proof supports one at a time. The false consequence was that
physical width increases directly by gamma.

Downstream false statements, all now removed: "widen by gamma" (Corollary 2,
Section 4, Section 6); experience transfer through (delta, gamma, M(q)) in the
RL paragraph (correct transfer: (delta, M(q))); the parameter-free
physical-width prediction; "one balanced solve serves every imbalance" (one
balanced SOLVER, one solve per multiplier); and the zero-carry "inventory tax"
sentence, which is incompatible with M(q) x 0 = 0.

Missing hypotheses, now explicit (substantive, not stylistic): even carrying
cost, symmetric domain, and solution uniqueness for the flat-book skew
S_q(0) = delta (numerically, an asymmetric cost gives S_q(0) = 0.221 vs
delta = 0.203); interior quotes in BOTH members of the equivalence (the tilt
makes one side's floor bind earlier); a finite-MDP state space with
one-sided boundaries, with the full average-reward equation rho = -c +
(s/tau)H preceding the centered form. The theorem is now stated as a
BIJECTION of normalized interior solution sets, assuming no uniqueness and
valid at c = 0 (M x 0 = 0); uniqueness is invoked only in the corollaries
that need it. The zero-carry remark records that the centered two-sided
interior equations alone are nonidentifying (every interior tilt solves
them), that this does not affect the theorem, and that on the finite
lattice the boundary rows select -- numerically, the optimal tilted branch
with S(0) = delta.

One localized independent inconsistency. The paper had already recognized the
Bellman incompatibility of quadratic CWLS with generic carrying costs ("solve
for nu rather than pretend nu ~ x^2 works"). What it had not stated is the
kinematic identity S(x+s) - S(x) = C(x) + C(x+s), which shows the
constant-width/nonlinear-skew inversion of eq. (7) cannot arise from ANY
single nu, Bellman equation or no. Section 4 now leads with the identity,
presents eq. (7) as a reduced-form pointwise inversion with the sign branch,
and corrects the hypothesis behind the quadratic form (even carrying cost, not
nonnegative liquidation costs).

## What replaces the width claim

The theorem is restated in the cost frame as an equivalence of relative values
and policies with gain scaling rho_bal,Mc = M(q) rho_q, plus the quote map
m_q = m_bal +/- delta: physical width equals the balanced-at-M(q)c width
exactly. The organizing interpretation is the inventory clock: after the skew
translation both fill rates scale by D(q) = 2 sqrt(q(1-q)) (generator identity
L_{q,c} = D(q) L_{1/2,Mc}; same embedded jump chain and stationary inventory
distribution), so positive carry is amplified by M(q) = 1/D(q) per effective
transition. gamma survives as the logarithmic clock slowdown in markup units
(D e^{-hm} = e^{-h(m+gamma)}), the overhead frame as a scoped operator
reparameterization remark with the quote remapping m_q = m_over + delta -
gamma (buy side). New corollaries: parity without cost symmetry
(S_q - S_{1-q} = 2 delta, C_q = C_{1-q}) and the exact width identity
W_q - W_{1/2,c} = 2[C_Mc - C_c], with the closed small-skew approximation
Delta C(0) ~ gamma hC0/(2 - hC0), eq. (10), on the branch hC0 < 2 (C0 the balanced
baseline; full-width response ~ 2 C0 (q - 1/2)^2 for small hC0).

## Verification

verify_all_claims.py: 38 labeled finite-lattice implementation checks of the
principal identities and approximations, keyed to paper sections -- checks
corroborate identities and implementations; they do not establish existence,
uniqueness, or asymptotic assumptions. Every test configuration now satisfies
the interior-quote assumption by explicit assertion, with a separate
piecewise-G check showing exactness fails once clipping occurs. Covered
-- the FOC and piecewise G, the quote identities, the policy-evaluation
identity gain = s H_q(0) (6e-17; optimality itself is established separately
in verify_optimality.py via the Howard fixed-point certificate), the theorem map in both
directions, gain scaling, quote map, time change, stationary-distribution
equality, the overhead remapping, flat-book skew (and its failure under
asymmetric cost), parity, Taylor orders, the exact width identity, zero-carry
degeneracy (interior) with boundary selection, the envelope identity for
non-exponential curves, the integrability identity, the CWLS corner (interior
exactness and its boundary layer), the cosh family, the width-response
formula and its branch, the margin/fill-ratio facts, and the scoring table by
Monte Carlo. All pass. verify_width_response.py retained (two cost
configurations for eq. (10)); verify_local_exponentiality.py unchanged.

verify_optimality.py: optimality attacked directly, with the competitor
space raw quote vectors rather than nu-parameterized policies. (i) Exact
policy-iteration fixed point: evaluate the consistency policy by linear
solve, apply closed-form greedy improvement; the policy reproduces itself
to 1e-15 -- by Howard's policy-improvement theorem for finite unichain
average-reward MDPs this certifies optimality on the lattice up to floating
point. (ii) Derivative-free search (humpday) over the full 16-dimensional
raw quote vector from cold starts: no policy beats the consistency gain,
and the polished search argmax reproduces the consistency quotes to
about 1e-7. (iii)
4800 random policy perturbations across six scales: none improves. Run for
both members of the equivalence; the two searched optima are related by
the theorem's quote map and gains by M(q) -- at machine precision for the
Howard optima (4e-16, 6e-17), with the derivative-free search outputs
corroborating to about 1e-7 (humpday) or 1e-6 (scipy fallback) after local
polish. Extended:
(iv) the Howard/consistency correspondence swept across eight
configurations (q up to 0.8, quadratic/asymmetric/quartic/kinked costs,
N up to 8) -- the policy-iteration optimum is interior and satisfies the
paper's consistency equation to 5e-16 in each; (v) at c = 0 the
boundary-selected solution is itself the Howard optimum and the gain over
pure tilt policies peaks at b = delta to 3e-4 -- on the finite lattice it
is OPTIMALITY that selects the tilted branch; (vi) in the floor-binding
regime policy iteration converges to a clipped optimum and the quote map
+-delta FAILS between the clipped optima (deviation 1.2), confirming
interiority as a substantive hypothesis; (vii) an interior carrying-cost
spike clips that interior state first, so boundary-first clipping is a
property of the convex families tested, not universal -- the manuscript's
interiority remark is worded accordingly. The humpday search is optional
(scipy differential evolution is the fallback), so the certificate is
portable; (viii) a fuzz stage draws random configurations across
(q, N, eps, cost shape), keeps the ~60 percent whose two members are both
interior, and checks consistency, the quote map, and gain scaling at every
one of 150 admissible draws (worst deviation 3e-15). 14/14 pass.

verify_symbolic.py: every purely algebraic identity verified EXACTLY in
sympy under the log-odds parameterization q = e^t/(e^t + e^-t) -- the FOC
and enquiry value, the cosh imbalance identity, the termwise Hamiltonian
scaling used by the new proof, M = e^{h gamma} and DM = 1, parity, the
integrability identity, and the width-sensitivity derivative
dC0/dlog a = C0/(2 - hC0). 12/12, no floating point involved.

verify_interval.py: a Krawczyk interval-Newton certificate with
outward-rounded arithmetic (mpmath.iv) PROVES, at the flagship
configuration and its balanced image, that exactly one solution exists in
a box of radius 1e-7 around the reported solution (enclosure width
2.4e-12), that every available quote of both proven solutions is interior
(rigorous lower bounds 0.0226 and 0.2254), and that the proven enclosures
satisfy the tilt map to 2.4e-12. A continuation stage then tiles
q in [0.55, 0.605] into 220 slabs and reruns Krawczyk with q as an
INTERVAL parameter (mean-value form in the parameter, monotone-hull
enclosure of the cost scale), proving existence, local uniqueness, and
interiority for EVERY q in that range and for every corresponding
balanced image -- a continuum of configurations, not samples. This proves
existence, LOCAL uniqueness (exactly one solution in each stated box; not
global uniqueness over the whole interior region), and interiority; the
interval constants are built from exact decimal strings and the slab
edges are exact rationals (2200+k)/4000, so the certificate covers the
decimal parameters printed in the paper. 6/6.

Scope finding from the sweep, now a remark after the theorem: in the
convex cost families tested, interiority binds first at the one-sided
boundary state, and at strong imbalance it binds at every cost level
including c -> 0, because the value of escaping the one-sided state (its
Hamiltonian is halved) exceeds w + eps - delta; an interior cost spike can
instead clip that interior state first. At eps = 0.15 the frontier passes
near (q = 0.6, N = 8, a = 0.002); the certificate configurations sit just
inside it and assert membership.

verify_diagrams.py: every commutative diagram certified from directly
optimized strategies only -- all corners produced by policy iteration from
flat cold starts, no consistency solver anywhere. The tilt square (quote
map, width, mid, gain scaling), the time-change diagram (generator,
embedded chain, stationary distribution, carry per transition), the
overhead square (quote map with equal gain and overhead width = physical
width + 2 gamma -- the gamma widening provably lives in that frame alone),
and the parity square all commute between independent optima at 1e-15;
the CWLS corner (constant width, affine mid, boundary layer shrinking
sharply with N) and the flat-book skew delta are certified as optimality
statements the same way. 6/6.

A new remark in Section 2 records the moving-price equivalence: quoting
relative to a martingale fair price adds only the mean-zero term int x dF
(no Bellman comparison changes; time average vanishes on the bounded
lattice), and by Ito isometry a mean-variance dealer's price risk in that
frame is exactly the quadratic carrying cost -- the fixed-price frame is
lossless and the canonical c(x) is derived rather than assumed.
verify_moving_price.py (4 checks) accompanies it. State-dependent adverse
selection (fill-correlated price moves) is explicitly outside and is
follow-on work.

## Editor framing (draft in editor_note.txt)

The core algebraic reduction in the proof remains valid; the theorem now
carries explicit scope assumptions, the average-reward scaling, and the quote
map. The revision corrects an overinterpretation in which the equivalent
overhead representation was treated as an additional physical widening, and
correspondingly revises the width and zero-carry consequences; it makes the
interiority, symmetry, and uniqueness assumptions explicit; and it clarifies
that the constant-width inversion is reduced-form unless its integrability
condition holds. The central symmetry emerges more cleanly, as a skew
translation composed with a uniform time change of the inventory process.

## Venues

- SIFIN: send the replacement manuscript promptly (draft note ready); waiting
  risks referees spending time on claims known to be incorrect.
- arXiv v2 when the identifier allows; SSRN revision.
- Downstream repo: notes/spread_as_endogenous_carry.tex (H7 and the
  "manufactures its own carrying cost" reading at k = 0) and
  data_scout_imbalance.md width tests tracked in revision_notes.md section 5.
