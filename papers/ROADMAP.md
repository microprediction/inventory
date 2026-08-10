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
**Risk.** Low-medium: the algebra is mechanical; the terminal condition is where it
could degrade from exact to approximate — which would still be a result.
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

### P3. Robustness of the imbalance equivalence (the approximate symmetry)
**Claim.** For win curves that are only locally exponential, the equivalence holds to
first order with the local width, with an explicit error bound and an explicit
second-order correction: δ correction proportional to the hazard's log-slope at the
operating point. Makes the paper's Remark (envelope identity −(log G)′ = h(m*(K))) a
theorem with constants; explains the observed error ≈ 0.25 × hazard variation.
**Attack.** Perturbation expansion of the consistency equation in ε = hazard variation
across the visited strike range; the certificate script already computes both sides.
**Risk.** Low. The numerics already show the scaling; the work is bookkeeping.
**Venue.** Fold into P1 as a section, or standalone SIFIN Short Communication if P1
runs long. Do not let it delay P1.

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

### P7. The symmetry as an invariance for market making RL
**Claim.** Enforcing the (δ, γ, M) equivalence as an equivariance layer (or data
augmentation across q) provably reduces sample complexity in market making RL, and
measurably: same policy quality from a fraction of the episodes.
**Attack.** The simulator already exists (`docs/mm_core.js` / the certificate script's
Python twin). Train identical agents with and without the symmetry layer across q ∈
[0.5, 0.85]; report the sample-efficiency ratio; a one-line theory section (orbit
reduction of the policy space).
**Risk.** Low technically; medium on venue fit. Fun, demonstrable, citable by the
Guéant–Manziuk line.
**Venue.** Applied Mathematical Finance, or an ML-for-finance workshop for speed.

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
P3 folds into P1      │
P2 (LOB note) ────────┘         P5 (filtering bridge) ─────▶ P6
P7 (RL) and P8 (empirics) run parallel, opportunistic
```

Start with P1 + P2 concurrently: P1 is the natural sequel the referees of the submitted
paper will themselves suggest; P2 is small, sharp, and stakes the probability-side claim
before someone else notices the dashed red edge on our own public map.
