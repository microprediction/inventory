# Papers roadmap — the symmetry program

Candidate papers building on the imbalance equivalence (git tag `submitted-2026-08-07`),
in recommended order. Each entry: the claim, the attack, the risk, the venue. Gleanings
and verified absences backing these are in `skew_width_imbalance/revision_notes.md`.

## Tier 1 — direct descendants, provable now

### P1. Finite-horizon imbalanced market making in closed form
**Claim.** The transient (finite-horizon) version of the equivalence: with asymmetric
intensities, the GLFT linear ODE system symmetrizes under the diagonal conjugation
D = diag((q/(1−q))^{x/2}); the spectrum rescales by the geometric mean of the rates, and
the finite-horizon solution is the balanced solution under the same three corrections.
The steady-state theorem becomes a corollary.
**Attack.** GLFT (2012) reduce the HJB to v′ = A v with A an asymmetric birth–death
matrix. Conjugate, diagonalize, transform back. Watch the two exactness hazards: the
terminal condition (inventory penalty must transform consistently under the tilt) and
the max(·,0) quote floor (excluded region, as in the current paper).
**Risk.** RETIRED — verified 2026-08-10 (`finite_horizon_imbalance/verify_finite_horizon.py`):
the conjugation is exact to machine precision, boundary rows included, and the tilted
terminal condition means precisely "mark the terminal book at fair value shifted by
delta". The skew shift is the SAME (w/2) log-odds constant at every time and inventory.
What remains is writing, not proving.
**Venue.** Mathematics and Financial Economics (GLFT's home) or SIFIN full-length.

### P2. Closed-form order book first-passage laws via symmetrization
**Claim.** The first-passage quantities of Cont–Stoikov–Talreja (2010) — probability of
a mid up-move before a down-move given queue sizes, durations — currently computed by
numerical Laplace inversion, have closed or near-closed forms: a tilt prefactor
(q/p)^{z/2} times symmetric-walk cosh/sinh ratios (Feller Ch. XIV).
**Attack.** Their quantities race two birth–death processes (bid and ask queues);
symmetrize each marginal first-passage law, then the race by independence.
**Risk.** Low for the 1D laws; the race integral may resist closed form and settle for
"one quadrature instead of Laplace inversion" — still publishable as a note.
**Venue.** Operations Research (technical note) or SIFIN Short Communication.
**Strategic value.** Plants the symmetry in the most-cited LOB model; the map's dashed
edge made solid.

## Tier 2 — the approximate symmetry, made rigorous

### P3. The exponential normal form (UPGRADED 2026-08-10; drafted)
**Was:** "robustness of the equivalence under locally exponential win curves, with an
error bound." Now an exponential normal-form theory, standalone paper drafted at
`exponential_normal_form/exponential_normal_form.tex` with certificate
`verify_normal_form.py` (all checks pass).
**Claim.** Five results. (1) Normal form: for EVERY smooth positive win curve, in the
coordinates of the effective log-value Φ = −log G, imbalance is exactly a translation
(by log M(q) in width, by the log-odds ℓ in skew); exponentiality is precisely
affinity of those coordinates, which makes the translation a rigid quote motion.
(2) Rigidity, two theorems: sidewise gauges are translations only for the
exponential; rigid balancing of the two-sided Hamiltonian holds exactly for the
affine-exponential family C + Be^(-hK), pure exponential under the tail
condition G(inf) = 0.
(3) Integrability defect: the pointwise gauge T_c = Φ⁻¹(Φ − log c) always removes
imbalance pointwise but fails to lift to a single inventory potential; the failure is
a curvature functional of ψ = the deformation of Φ, and its constant value at the
affine point is exactly 2γ — the widening IS the defect functional at the integrable
point. (4) Perturbation hierarchy: ν_η = ν₀ + ην₁ + ..., every order solved by ONE
pinned tridiagonal operator L₀ assembled at the exponential anchor; envelope transfer
converts log-survival deformations of any named family (Weibull ψ = (1+hK)log(1+hK),
Gompertz, gamma, mixtures, empirical win curves) into forcing terms without
recomputing the optimal markup — a precomputable response library. (5) Distribution-
free parity: skew odd / width even in ℓ for any symmetric-sided win curve;
exponentiality supplies the coefficients (δ = ℓ/h, γ = log cosh ℓ / h), not the
parity. Certified: exact claims ~1e-15; expansions O(η²)/O(η³) at ratios ~4/~8;
curved-curve d₁ ≈ 0.797/h ≠ 1/h.
**Round-1 revision applied 2026-08-10.** (i) Rigidity was overstated: G = C + Be^{−hK}
balances rigidly with curved Φ (the constant passes through both Hamiltonians and
cancels from the consistency equation, so the companion compression holds verbatim
for the affine-exponential family). Now two theorems: sidewise gauge rigidity
(exponential) and Hamiltonian rigidity (affine-exponential; pure exponential under
the tail condition G(∞)=0, automatic for genuine win curves). (ii) Sign error in the
displayed ν₂ formula fixed (∂νF = −L₀; the certificate always had the correct sign).
(iii) Parity softened: symmetry gives odd/even powers only; leading orders one and
two under nondegeneracy (certified d₁ ≈ 0.797/h ≠ 0, g₂ ≈ 0.019 ≠ 0). (iv) L₀
described as tridiagonal + rank-one centering (bordered tridiagonal). (v) C^r vs
analytic split in the hierarchy theorem (splines legal through order r). (vi) NEW:
local admissibility proposition (Φ′>0, Φ″<Φ′², GΦ′≤1 ⟹ genuine markup distribution;
reconstruction re-optimizes to G at 1e-16). (vii) NEW: tangent-policy corollary
m* correction = D±ν₁ − ψ′/h² (the bridge to P7; certified O(η²)). (viii) NEW:
defect oscillation bound osc D ≤ (|η|/h)diam(I)(|a₁|+|a₂|)‖ψ″‖∞ and the resolvent
amplification remark ‖ν₁‖ ≤ ‖L₀⁻¹‖‖R_ψ‖ (spectral gap of the anchor; the low-carry
bridge). (ix) Terminology: win curve = F̄, enquiry-value curve = G; gauge scalar λ.
**Round-2 revision applied 2026-08-11.** (i) Strike rigidity was FALSE without
convexity: the concave family kappa - B e^{+hK} balances rigidly with
opposite-signed translations (verified at 4e-16). Fixed by a new indirect-value
lemma (G is a sup of affine functions, hence convex with -1 <= G' < 0) and a
convexity hypothesis; renamed the constant C -> kappa (collision with convexity
C(x)). (ii) The local-to-tail step was invalid on bounded intervals; the tail
clause now requires a right half-line, and a new remark shows kappa =
lim m* Fbar(m*): a positive constant is a borderline 1/m tail, so finite mean
markup forces kappa = 0. (iii) Strikes vs quotes separated: NEW quote-rigidity
corollary — the submitted-quote map translates rigidly iff kappa = 0, so quote
rigidity characterizes the pure exponential with no tail condition; the
identification remark now operates at the quote level. (iv) Parity restated as
Taylor jets under C^r with convergent series only under analyticity; the gamma
vs endogenous-convexity-response conflation fixed. (v) Hierarchy stated for any
smooth path; NEW homotopy remark — straight line in Phi = log-geometric
interpolation, higher coefficients path-dependent, additive constant is a null
direction, and Xi = -log(-G') is the coordinate adapted to strike rigidity.
(vi) Theorem 2 proof repaired for local shifts; envelope proposition given C^3
and nondegeneracy hypotheses; admissibility inequality made strict and scoped as
local; matrix structure stated honestly (interior tridiagonal + two narrow-band
boundary rows + rank-one centering, with the equation count); spectral-gap
language demoted to conditioning; defect renamed mathcal-D; intro reorganized
around the five-level ladder (coordinates / sidewise / strikes / quotes /
global). Certificate extended: concave impostor and borderline-tail checks.
**Round-3 revision applied 2026-08-11.** (i) Path dependence begins at FIRST order,
not second: nu_1 depends on the initial tangent, and the additive path's tangent
-kappa/G_0 has forcing annihilated by the centering (nu_1 = 0 exactly, certified)
while the Phi-line to the same endpoint moves nu_1 (~0.06 on the test problem);
the path-convention discussion now sits directly after the deformation equation.
(ii) Defect scope corrected: mathcal-D measures the gauge-lifting failure, NOT the
policy correction (additive counterexample: nonconstant defect, potential never
moves); NEW policy-sensitivity corollary ||nu_1|| <= ||L0^-1|| Gmax R^2 ||psi''||
is the true robustness radius (certified: 4.11 <= 13.90 <= 196.47). (iii) NEW
coordinate-uniqueness lemma: chi(lambda z) - chi(z) independent of z forces
chi = a + b log z, so Phi is canonical, not convenient. (iv) Strike-rigidity
statement now requires translated strikes to stay in the domain; quote-rigidity
corollary given its rationalizability hypothesis. (v) Rigid-manifold remark
upgraded with the osculating anchor formulas (h0 = G''/(-G'), kappa_0 = G -
(G')^2/G''; verified exactly); Xi geometry retained. (vi) Abstract rewritten to
the reviewer's tighter shape ("need not lift"); intro item 5 no longer conflates
gamma with the endogenous convexity response; Weibull domain 1 + hK > 0 stated;
admissibility openness qualified by a uniform margin; Cotton 2026a/b bibliography
labels fixed; ancestry remarks moved to related work. Certificate: two new checks
(13 path dependence/null direction, 14 policy bound), all passing.
**Round-4 revision applied 2026-08-11** (reviewer's upload predated round 3, so
several flagged items were already in; the new ones): hierarchy opener no longer
claims the defect obstructs compression (null directions); higher-order forcing
R_j explicitly uses the path jet of Phi_eta for general paths; gauge maps given
their domains I_lambda; strike-rigidity proof derives A e^{-hK} before writing
A = hB; Prop 2 uniqueness replaced by the reviewer's two-line sign argument
(verified numerically); pre-Theorem-1 sentence fixed (both U and V translate);
Weibull psi-perp comment made precise (raw psi is the fixed-scale path tangent);
identification remark localized to the visited strike range; rigid-manifold
remark gains the tangent-space observation span{1, K, e^{hK}} explaining the
null direction; directional-Taylor framing of the hierarchy added to the setup.
**Round-5 revision applied 2026-08-12** (fresh-reader review). Retitled
"Exponential Rigidity and a Log-Value Normal Form for Imbalanced Market Making"
(coordinate canonical, path a convention). MAJOR FINDING: the gamma/M
double-count — widening the overhead and multiplying the carry are alternative
frames of ONE transformation; the imbalanced dealer's physical width equals the
balanced-at-Mc dealer's exactly (certificate check 15), so the width response is
the cost-dependent second-order convexity response, not gamma. This propagates
to the SUBMITTED skew paper's Theorem 1 wording, its Corollary 2, the width
tests in data_scout, and H7 — recorded in skew_width_imbalance/revision_notes.md
§5 for the SIFIN revision. Also: sensitivity corollary extended to submitted
quotes (D L0^-1 term + direct psi'/h^2 term, certified); resolvent factor
renamed inventory-feedback amplification; null direction qualified (null for
the centered potential only); Theorem 3 now concludes gamma(q), delta(q) and
requires a common interval; blunt canonical/convention statement in Section 2;
Prop 2 restated in G-coordinates (G>0, -1<G'<0, G''>0); parity extended to
submitted quotes (corollary); envelope identity proved in place; m Fbar -> 0
one-liner; nu_j convention; Thm 4 uniformity; osculating anchor needs G''>0;
numerics section carries full configuration and independence statement; "To our
knowledge" hedge. Certificate at 15 checks.
**Remaining.** Editorial pass; decide venue; optionally derive the companion Remark's
≈0.25 constant in closed form from the ψ of the linear-hazard experiment; the
finite-horizon instance (P1's concluding problem) is now posed as this hierarchy with
the tilted terminal condition in the forcing.
**Venue.** Standalone — SIFIN or MAFE. No longer folded into P1.

### P4. The spectral carry multiplier: Markov-modulated imbalance
**Claim.** When the imbalance q_t follows a Markov chain, the equivalence survives with
2√(q(1−q)) replaced by the Perron root of the exponentially tilted modulation kernel: a
spectral carry multiplier. Slow modulation recovers the static formula adiabatically —
an approximate symmetry with a rate.
**Attack.** Asmussen's change-of-measure machinery for Markov-additive processes; the
tilt that removes drift state-by-state has a normalizing eigenvalue in place of the
scalar geometric mean.
**Risk.** Medium: Markov-additive tilting is standard but the market making overlay
(coupled ν per state) may only symmetrize approximately. Either outcome is a paper.
**Venue.** This should become the spine of the revised **Cotton–Papanicolaou** companion
(clustered arrivals + stochastic imbalance), giving it exact structure where it had
approximation. Discuss with Andrew before scoping as standalone.

## Tier 3 — the bridges

### P5. Reading latent flow from dealer quotes (filtering + the symmetry)
**Claim.** Certainty equivalence in the odds: with hidden imbalance, the optimal skew is
(w/2) · log(posterior odds of seller arrival). Then observed skew surfaces INVERT: a
dealer's quotes reveal the market's posterior on the flow, and cross-sectional quote
data becomes a filter readout for latent imbalance — and, in the storage program, for
the latent stock.
**Attack.** Zabaljauregui–Campi setting (hidden Markov intensities); check whether the
exponential family makes the conjecture exact; if not, quantify the gap. Then the
inverse problem is regression.
**Risk.** Medium-high on exactness; the approximate version is still the program's
load-bearing bridge (quotes as observables for the latent state).
**Venue.** SIFIN or Applied Mathematical Finance.
**Strategic value.** THE connector between the solo paper and the wider inventory
program's filtering formulation (`notes/formulation.md`).

### P6. The bid–offer as endogenous carry (the program flagship)
**Claim.** For goods with negligible physical carry, the dealer market's spread and the
imbalance tax M(q) supply the missing stabilizer — and the closed loop (inventory →
imbalance → effective carry → inventory) is an oscillator with amplitude-dependent
damping. The symmetry provides the exact microstructure input to a general-equilibrium
storage question.
**Attack.** Promote `notes/spread_as_endogenous_carry.tex` from note to paper, now with
M(q) exact rather than heuristic; the explosiveness boundary via the cheap-control limit.
**Risk.** High — this is the ambitious one; scope creep is the enemy. Gate it behind P4
and P5 so its inputs are theorems.
**Venue.** Aim high (Mathematical Finance / JET-adjacent), accept the journey.

## Tier 4 — applied and empirical

### P7. Normal-form RL for market making (UPGRADED 2026-08-10)
**Was:** "the symmetry as an equivariance layer / data augmentation across q."
Now a three-layer architecture, designed in `normal_form_rl/architecture.md`:
exact exponential controller + perturbative tangent controller + small learned
residual. The learner never spends data rediscovering the exponential symmetry;
learning is reserved for the curvature of −log G, its uncertainty, and the global
integrability defect.
**Claim.** (a) Learn one inventory potential ν(x,z), not two quote functions —
quotes extracted analytically, edge identity enforced by construction. (b) Critic
and replay in the nonlinear normal coordinates (Ū, V̄) = (U + log M(q), V − ℓ):
imbalance vanishes from the local Hamiltonian for EVERY win curve, so every regime
lands in one balanced frame. (c) Response library: L₀νⱼ = −Rⱼ solved once per
curvature basis direction; residual indexed by win-curve shape, not regime label —
extrapolates to unseen q and unseen families. (d) Robustness as a sensitivity
penalty ρ‖Σ^{1/2}∇_θ J‖ over hazard curvature, not rectangular robust MDPs;
minimax regret rather than max–min so "do no business" cannot win. (e) Exponential
anchor as Bellman control variate (shaped TD target, telescoping potential).
(f) Demo learner replacement with identification: R(0,q)=0, E_q[R]=0, hierarchical
λ_t set by measured symmetry failure.
**Certified 2026-08-10** (`normal_form_rl/verify_tangent_rates.py`): on the bounded
lattice the consistency solution is exactly average-reward optimal (gain = sH_q(0),
agreement 6e-17) and the imbalance tilt is exact through the boundary rows; regret
of the exponential controller is O(ε²) and of the anchor+tangent controller O(ε⁴)
(ratios → 15.5 ≈ 16), three orders of magnitude better at Weibull k = 1.16.
**Remaining.** The ε⁴ theorem (strong concavity + implicit function); the oracle
inequality; rebuild rl_core.js per the design; the model-based experiment grid with
held-out families. **Venue.** Applied Mathematical Finance, or an ML-for-finance
workshop for speed. Depends on P3 (the normal form supplies the coordinates).

### P9. Efficient inverse reinforcement learning: reading ν from quotes across regimes
**Claim.** Inferring a dealer's objective from behavior — inverse RL — is generically
ill-posed and data-hungry; here it is neither. The identities make inversion direct
(skew = slope, discretionary width = convexity of ν), and the symmetry makes it
efficient: quotes observed under ANY flow regime q, de-tilted by δ(q), all estimate the
same balanced-frame ν, so K regimes cut estimation error by √K and the sample complexity
of identifying a dealer's inventory cost is independent of which regimes you happened to
observe her in. Deviations from the pooled fit isolate what the symmetry cannot explain:
private information.
**Attack.** Estimator: per-quote de-tilting then pooled regression for S(x), C(x);
compare to per-regime estimation at equal observation budget. Theory is elementary
(averaging); the content is the framing plus the identifiability corollary.
**Risk.** Low. Companion demo on the site (see `docs/` RL demo).
**Venue.** Pairs with P7 in one paper, or standalone short communication.

### P8. Skew, width and the log-odds of flow: an identification test
**Claim.** Structural flow skew and informational widening are separable by parity: δ is
odd in (q−½) with coefficient PINNED at w/2; informational effects are even. A
parameter-free horse race on RFQ/FX data.
**Attack.** Datasets scouted in `skew_width_imbalance/data_scout_imbalance.md`;
practitioner data would be better. Estimate w from the win curve (fill ratios,
log-linear), q from direction counts, test the pinned coefficient.
**Risk.** Data access is the whole risk. Everything else is a regression.
**Venue.** Journal of Financial Markets or Quantitative Finance.

## Sequencing

```
P1 (finite horizon) ──┬─▶ P4 (spectral, = C–P revision) ──▶ P6 (endogenous carry)
P3 (normal form,      │
  standalone, drafted)┘         P5 (filtering bridge) ─────▶ P6
P2 (LOB note) ────────┘
P7 (RL) + P9 (inverse RL) share a demo and likely a paper; P8 (empirics) opportunistic
P3 also feeds P1's open problem (finite-horizon local exponentiality) and P5 (the
exponential-family exactness question is a Φ-affinity question)
```

## Tier 5 — symmetry, more broadly (added 2026-08-10)

### P10. Which market making effects are gauge?
**Claim.** A classification of perturbations of the Avellaneda–Stoikov family into pure
gauge (absorbable into quote translations and clock changes: drift, imbalance, price
level, reference-price choice) and physical (spread-changing: risk aversion, decay k,
adverse selection). GLFT's drift result and our two imbalance papers are the first
entries of the table; the paper completes it.
**Risk.** Low-medium; the work is finding the right group action and checking each
generator. **Venue.** SIFIN or MAFE.

### P11. The de Finetti projection program — MOVED to the private reynolds repo (2026-08-10)
The program (symmetric payoffs, portfolio theory, fast repricing demos) now lives in
github.com/microprediction/reynolds. Only leg (b), exchangeable RFQ books, remains an
inventory paper, composing with the imbalance gauge.

### P11-archive. Original entry (superseded)
**Vision (Peter).** A whole industry of projection onto de Finetti-style bases for
re-pricing and re-evaluating symmetric payoffs. Exchangeability is the model-free part;
the latent mixing measure is the only unknown. Calibrate the mixing measure from liquid
symmetric instruments, then re-price ANY symmetric payoff by projection.
**Provenance.** Peter's own 2006 work, never written up properly. Extant sources: the
GFC/CDO essay (allocation repo, `docs/essays/gfc/longform.html`, 14 de Finetti
references), the implied-correlation article (`article/implied-correlation/`), earlier
Medium articles referenced therein, and the signed-de Finetti thread
(conformalprediction repo, `paper/definetti-feynman/`).
**Legs, in write-up order.**
(a) *Foundations, overdue*: "Projection onto de Finetti bases: re-pricing symmetric
payoffs" — the 2006 program stated properly. CDO tranches, nth-to-default, baskets,
index-versus-constituents as projections of one calibrated mixing measure. The
implied-copula literature (Hull–White) is the nearest neighbour to distinguish.
(b) *Market making*: exchangeable RFQ books — the multi-asset indifference cost reduces
by permutation symmetry to radial + identical relative components; the exact counterpart
of Bergault–Guéant's numerical factor reductions, composed with the imbalance gauge.
(c) *Portfolio theory*: allocation among exchangeable assets — within-cluster
exchangeability is the unstated reason parity-style weights work inside blocks, so the
de Finetti mixing measure is what the Schur/HRP cluster factor has been all along.
Connects this program to the schur repo's bridge.
**Risk.** (a) low, it exists and needs writing; (b) medium; (c) medium, high payoff.
**Venue.** (a) could aim wide (JPM-adjacent practitioner or Mathematical Finance);
(b), (c) follow.

### P12. Explicit spectrum for the balanced GLFT oscillator
**Claim.** The symmetrized balanced GLFT matrix (quadratic diagonal, constant
off-diagonal) is a discrete harmonic oscillator; Karlin–McGregor orthogonal-polynomial
machinery may give its spectrum in closed or semi-closed form, upgrading P1's
Corollary 2 to fully explicit eigenvalues. **Risk.** A week's exploration; either it
closes or it doesn't. **Venue.** Addendum to P1 or standalone note.

### P13. Adverse selection as broken time reversal (speculative)
**Claim.** Under detailed balance a dealer's expected P&L behaves like entropy
production; informed flow is statistically irreversible, and fluctuation-theorem
machinery gives model-free inequalities relating P&L asymmetry to flow irreversibility,
measurable as a KL divergence between the forward and reversed tape. A model-free
toxicity metric with a physics pedigree — or a costume. Time-boxed exploration first.
**Risk.** High. **Venue.** Decide after the exploration.

```
P10 gauge classification: our two papers are two-thirds of its work — likely next after P2
```

Start with P1 + P2 concurrently: P1 is the natural sequel the referees of the submitted
paper will themselves suggest; P2 is small, sharp, and stakes the probability-side claim
before someone else notices the dashed red edge on our own public map.
