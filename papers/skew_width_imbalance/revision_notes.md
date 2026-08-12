# Revision notes — post-submission

The version submitted 2026-08-07 (arXiv submit/7924699, SIFIN Short Communication, SSRN)
is frozen at git tag `submitted-2026-08-07`. Everything below is for the revision round,
sourced from the verified three-strand literature sweep of 2026-08-10 (dealer-inventory
classics; optimal MM & RFQ; probability). No claim below is unverified: every locator was
checked against the publisher page, and every absence was searched for directly.

## 1. Novelty ammunition (for the response to referees)

- **No prior statement of the imbalance equivalence exists.** Nearest misses: the
  Barzykin–Bergault–Guéant FX line manages imbalance numerically ("skew to attract or
  divert flow") with no compression map; arXiv:2508.20225 obtains zero-inventory
  *widening* from an informational mechanism (price reading), not flow imbalance; the
  literature notes qualitatively that asymmetric intensities shift steady-state inventory.
- **No antecedent for "discretionary width reveals the convexity of the inventory
  cost."** Closest partial precedent: O'Hara–Oldfield (1986) prove inventory affects both
  the placement and the size of the spread, but never state the derivative structure. In
  Ho–Stoll-style models the width is mechanically a second difference of the value
  function, but no source remarks on it. Phrase as "we are not aware of a prior explicit
  statement."
- **The birth–death symmetrization has never been applied to market making or LOB
  models.** Verified against full text of Cont–Stoikov–Talreja (2010) — asymmetric
  birth–death LOB queues solved via Abate–Whitt continued fractions and numerical Laplace
  inversion; no symmetrization, no cosh, no geometric mean. This confirms the paper's
  "nobody has done so" remark and names its nearest neighbour.

## 2. Citations to add, mapped to where they go

**§1 Introduction (mechanism isolation).** Glosten–Milgrom (1985), JFE 14(1), doi
10.1016/0304-405X(85)90044-3 — the informational route to quote asymmetry at zero
inventory; one sentence distinguishing it isolates our pure flow channel. Pair with
Barzykin–Bergault–Guéant–Lemmel, arXiv:2508.20225, the modern informational counterpart
of Corollary 1.

**§1.2 Literature, classics paragraph.** Stoll (1978), JF 33(4) — the spread prices an
inventory holding cost, the object whose derivatives our identities isolate. Ho–Stoll
(1983), JF 38(4) — competing dealers, reservation prices as indifference differences (the
discrete ancestor of skew = slope). O'Hara–Oldfield (1986), JFQA 21(4) — placement and
size of the spread with explicit flow asymmetry; our identities give their decomposition
exact content. Mildenstein–Schleef (1983), JF 38(1) — see §3(c) below; cite as the
instructive contrast.

**§1.2 Literature, modern paragraph.** Zabaljauregui–Campi (2020), arXiv:1902.01157 —
one of the few analytical treatments of general asymmetric intensities. The Barzykin FX
series (arXiv:2112.02269, 2207.04100, 2404.15478) — imbalance managed numerically,
never compressed away.

**§1.2 or §2, OTC grounding (optional, referee-dependent).** Grossman–Miller (1988);
Duffie–Gârleanu–Pedersen (2005), Econometrica 73(6); Weill (2007), REStud 74(4) — the
economics of one-sided immediacy. Add only if a finance-side referee asks for grounding.

**"The algebra is old" remark.** Feller Vol. I Ch. XIV (the identity in random-walk
form: first-passage laws carry (q/p)^{z/2} · (2√(pq))^n); Abate–Whitt (1988), QUESTA 3,
doi 10.1007/BF01157854 (modern M/M/1 spectral companion); Asmussen (2003), Springer, the
exponential change-of-measure reading. Replace or augment the "could equally be applied
to LOB linear systems" sentence with a pointed cite of Cont–Stoikov–Talreja (2010), doi
10.1287/opre.1090.0780, as the near miss.

**Empirics (§6 Uses, testing paragraph).** Ho–Macris (1984), JF 39(1) — earliest direct
dealer-book evidence of inventory-driven shading. Madhavan–Smidt (1993), JF 48(5) —
quote revisions respond to order imbalance. Lyons (1995), JFE 39 and Bjønnes–Rime
(2005), JFE 75(3) — FX dealer transaction records. Schrimpf–Sushko (2019), BIS QR Dec —
skewing as the institutional norm for managing flow.

**Corollary 3 (imbalance as carrying cost).** Moran (1959), *The Theory of Storage* —
drift as effective long-run cost in reflected storage processes; the inventory-theory
antecedent of the corollary's reading.

## 3. Gleanings — substantive, not just citational

**(a) The symmetrization plausibly solves the finite-horizon asymmetric problem in
closed form — a second short paper.** GLFT (2012) reduce the finite-horizon
Avellaneda–Stoikov HJB to a *linear* ODE system in inventory whose generator, with
asymmetric intensities, is exactly an asymmetric birth–death matrix. A diagonal
similarity transform D = diag((q/(1−q))^{x/2}) symmetrizes that matrix; its spectrum
rescales by the geometric mean of the rates. If it goes through, the transient
(finite-horizon) version of our theorem holds with the same three corrections, the
steady-state result becomes a corollary, and the "asymmetric intensities are numerical"
gap closes in full generality. Sketch first on the GLFT system; natural title shape:
*Finite-horizon market making with imbalanced flow, in closed form*.

**(b) Cont–Stoikov–Talreja's first-passage quantities should symmetrize too.** Their
LOB probabilities (mid-move up before down, given queue sizes) are birth–death
first-passage laws computed numerically; Feller's chapter says such laws factor as a
tilt prefactor times a symmetric-walk quantity. A short note deriving closed or
near-closed forms for their §4 quantities via the substitution would be the paper's
remark made good, in their own model.

**(c) Mildenstein–Schleef's 40-year-old non-result is our corner case.** They found
spread *unrelated* to inventory and it reads as a puzzle against Stoll (1978). The
convexity identity explains it: width responds to inventory only through the convexity
of ν, so any model in which ν is effectively quadratic — theirs — must find no
spread–inventory link. Worth a remark in §5: the corner case adjudicates a classical
disagreement.

**(d) An identification strategy falls out of the parity structure.** Informational
widening (Glosten–Milgrom; price reading) and structural flow skew make separable
predictions: δ is odd in (q − ½) with the specific log-odds form and slope w/2, while γ
and informational widening are even. Regressing zero-inventory skew on the log-odds of
realized flow, with the coefficient *pinned at w/2*, tests our mechanism against the
informational one — no free parameter. Strengthens §6 "testing the symmetry" from
consistency check to horse race.

**(e) Partial information conjecture.** In the Zabaljauregui–Campi setting (hidden
Markov-modulated intensities), the natural conjecture is certainty-equivalence in the
odds: skew = (w/2) · log(posterior odds of seller arrival). If exponential-family
structure makes this exact, the symmetry composes with filtering — directly relevant to
the wider program's latent-stock formulation.

**(f) Tilting reading upgrades the companion paper.** Asmussen's change-of-measure view:
the substitution is an exponential tilt that removes drift, and M(q) is the tilt's
normalizing cost. For the Cotton–Papanicolaou companion (Markov-modulated imbalance),
the analog of 2√(q(1−q)) should be the Perron root of the tilted modulation kernel —
i.e., a *spectral* carry multiplier for stochastically varying imbalance. If true, the
companion inherits an exact structure rather than an approximation.

**(g) Moran bridges the corollary to the storage program.** "Imbalance acts as a
carrying cost" is dam theory's drift penalty in microstructure clothing; citing Moran
makes the repo's larger claim — the bid–offer as endogenous carry — a two-way bridge
rather than an analogy.

## 4. Style retrofits for the revision (author rulings post-submission)

- The remark title "[What this says, and does not say]" is a retired construction
  (author ruling 2026-08-10: meta-commentary scope framing is an AI tell). Rename to a
  descriptive mathematical title and state the scope as plain fact.
- Sweep the frozen text for "We are explicit about..." openers and the same treatment.

## 4b. Process

- Revisions to the tex branch from `submitted-2026-08-07`; keep the submitted PDF
  reproducible from the tag.
- When the arXiv ID issues, arXiv v2 can carry §2 citations + any referee-driven
  changes; keep v1 as the record of the submitted text.

## 5. CRITICAL for the revision — Theorem 1's wording double-counts (found 2026-08-12)

The submitted theorem states the correspondence as "skew translated by δ AND
non-discretionary width Δ widened to Δ+γ" for the balanced problem at cost
M(q)c. The widening and the multiplier are ALTERNATIVE representations of the
same factor e^{hγ} — overhead frame versus cost frame — not simultaneous
corrections; the submitted proof itself moves e^{−hγ} to the cost side, after
which nothing remains to widen. Numerical demonstration (normal-form paper
certificate, check 15): the imbalanced dealer's physical half-width equals the
balanced-at-Mc dealer's to machine precision, and exceeds the balanced-at-c
dealer's only by the convexity response C_{Mc}(x) − C_c(x) — 6.5e-4 in the test
configuration, an order of magnitude below γ ≈ 0.020.

Fixes needed in the SIFIN revision:
- Restate Theorem 1 as one transformation with two equivalent frames (subtract
  δ from skew and add γ to overhead; or tilt by δx and multiply carry by M).
- Corollary 2: "width responds at second order" survives, but the widening is
  NOT the parameter-free γ; it is the cost-dependent convexity response to the
  multiplied carry. The parameter-free second-order object is M(q) as a carry
  statement, not a width statement.
- §6 "testing the symmetry": the widening-γ prediction and the data-scout
  "width multiplier 1/(2√(p(1−p)))" tests must be recast accordingly. The skew
  predictions (δ, zero-inventory skew, sign flip at q = ½) are unaffected.
- Downstream: `notes/spread_as_endogenous_carry.tex` H7 ("one-sided flow widens
  quotes by M(p)") inherits the same correction; the multiplier's carry reading
  (Proposition, M as effective-carry inflation) is untouched.
