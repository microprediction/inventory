# Correction package v2: skew_width_imbalance (2026-08-12)

Supersedes the seven-edit patch. The revision is structural at the statement
layer; the nu-level algebra, the proof, and the original certificate are
unchanged and correct.

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
S_q(0) = delta (numerically, an asymmetric cost gives S_q(0) = 0.254 vs
delta = 0.203); interior quotes in BOTH members of the equivalence (the tilt
makes one side's floor bind earlier); uniqueness for the steady-state
relative-value solution on the finite lattice (the state space is now stated
as a finite MDP with one-sided boundaries, and the full average-reward
equation rho = -c + (s/tau)H precedes the centered form). The zero-carry
equation is nonidentifying: every interior tilt solves it, so the theorem
excludes c = 0, and which policy is then selected depends on boundary or
transversality conditions (on the finite lattice the boundary rows select --
numerically they select the tilted branch, S(0) = delta). No claim is made
about zero-carry policy or throughput beyond M(q) x 0 = 0.

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
-- the FOC and piecewise G, the quote identities, average-reward optimality of
the consistency solution (gain = s H_q(0) at 6e-17), the theorem map in both
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
and the search argmax reproduces the consistency quotes to 3e-8. (iii)
4800 random policy perturbations across six scales: none improves. Run for
both members of the equivalence; the two searched optima are related by
the theorem's quote map (4e-16) and gains by M(q) (6e-17). 9/9 pass.

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
