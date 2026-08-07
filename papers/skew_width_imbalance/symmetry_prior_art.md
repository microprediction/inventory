# Prior-Art Hunt: The Imbalance-to-Balance Symmetry (Theorem 1)

Target result: in the steady-state sealed-bid market-making model, the imbalanced
problem (sell w.p. p, buy w.p. 1-p, exponential win curve with hazard h) compresses
EXACTLY onto the balanced one via: skew translated by delta = log(p/(1-p))/(2h),
width widened by gamma = log(1/(2 sqrt(p(1-p))))/h, carrying cost multiplied by
M(p) = 1/(2 sqrt(p(1-p))). Algebraic core:
p e^{-hS} + (1-p) e^{hS} = 2 sqrt(p(1-p)) cosh(h(S - delta)).

Scope: the SYMMETRY specifically (the broad novelty review is in
novelty_imbalance.md and is not repeated). Coverage: market making 2015-2026 plus
adjacent fields — queueing/birth-death, inventory theory, insurance, statistical
physics — and the economic reading (imbalance as a carrying-cost multiplier).

Method (2026-08-07): full-text checks via ar5iv and extracted PDFs; arXiv API,
Crossref API, and Semantic Scholar API queries. The session's WebSearch quota was
exhausted at task start, so every claim below rests on a direct fetch of a full
text or a structured API query, not on search-engine snippets. Caveats at the end.

---

## Strand 1: Market making / algorithmic trading, 2015-2026

### Guéant (2017), "Optimal market making" (arXiv:1605.01862; Applied Mathematical
### Finance 24(2), 112-154)
Full text checked via ar5iv. The model allows Lambda^b != Lambda^a throughout
("two functions", no symmetry imposed). **No change of variables, equivalence, or
reduction of the asymmetric problem to a symmetric one appears anywhere** — no
log-ratio shift, no geometric mean of intensities, no cost rescaling. Closed-form
approximations are derived from the general ODE system without a
symmetric-reduction step. NONE.

### Bergault-Guéant (2021), "Size matters for OTC market makers"
### (arXiv:1907.01225; Mathematical Finance 31(1))
Full text (incl. appendices) checked via ar5iv. Intensity kernels nu^{i,b} and
nu^{i,a} may differ across sides, but there is no quote-shift log-ratio formula, no
sqrt(lambda_b lambda_a), no cosh, no symmetrization, no imbalance-as-multiplier
statement. NONE. (Consistent with the earlier check of
Bergault-Evangelista-Guéant-Vieira arXiv:1810.04383 in novelty_imbalance.md.)

### Barzykin-Bergault-Guéant (2021-2023), "Market making by an FX dealer: tiers,
### pricing ladders and hedging rates" (arXiv:2112.02269; Math. Finance 33(1))
Full text checked via ar5iv. Asymmetry is *assumed away on empirical grounds*:
"While carrying out the above estimation procedure on individual clients, we
noticed that intensities on the bid and ask sides were not significantly
different. Therefore, we assumed Lambda_k^b(delta) = Lambda_k^a(delta) =
Lambda_k(delta)." No equivalence, no log-ratio shift, no geometric mean, no cosh,
no multiplier. NONE.

### Barzykin-Bergault-Guéant (2024), "Market Making in Spot Precious Metals"
### (arXiv:2404.15478)
Full text checked via ar5iv. Same: "We assume that the functions Lambda^b and
Lambda^a take the form Lambda^b(z,delta) = Lambda^a(z,delta) = Lambda(z,delta) =
lambda(z) f(delta)". Flow imbalance enters only implicitly via inventory
accumulation in simulation. NONE.

### Cartea-Donnelly-Jaimungal (2017), "Algorithmic Trading with Model Uncertainty"
### (SIAM J. Fin. Math. 8(1); doi:10.1137/16M106282X)
Full text (accepted-manuscript PDF from KCL Pure) extracted and grepped: ZERO
occurrences of "asymmetr*", "imbalance", "geometric mean", "cosh", "symmetriz*".
The paper is about ambiguity aversion (robustness) in drift, fill probability and
arrival rates; no flow-imbalance model, no equivalence. NONE.

### Bergault-Guéant (2023), "Liquidity Dynamics in RFQ Markets and Impact on
### Pricing" (arXiv:2309.04216)
Full text checked via ar5iv. This is the CLOSEST recent statement in spirit: flow
imbalance is modeled (Markov-modulated Poisson intensities) and they observe that
a flow-aware market maker "skew[s] their quotes even in the absence of inventory.
As a consequence, the average between the optimal bid and ask quotes ceases to
coincide with the reference price." But the effect is produced numerically through
the HJB system; there is NO closed-form shift, NO log-ratio formula, NO
geometric-mean rescaling, NO width term, NO cost multiplier, NO equivalence
statement. Partial qualitative anticipation of the zero-inventory-skew corollary
(in 2023); zero anticipation of the symmetry theorem.

### Systematic sweeps (arXiv API metadata, q-fin, through 2026-08)
Queries: "asymmetric intensities" + market making; "market making" + imbalance;
"request-for-quote" + market; "detailed balance" + market making; "geometric
mean" + market making; skew + "order flow" + market making; symmetrization +
q-fin.TR; "Avellaneda" + asymmetric; "flow imbalance" + market maker/making;
Barzykin + market making (full recent series: 2601.13421, 2603.07752, 2603.10569,
2604.20406 hit-ratio, 2608.02002 Hawkes OTC, 2508.20225 adverse selection/price
reading). Abstracts of all hits inspected. **No paper states an exact reduction of
asymmetric-intensity market making to the symmetric case.** The "detailed balance"
and "geometric mean" queries return zero market-making hits at all — the
vocabulary of the mechanism is absent from the field.

**Strand 1 conclusion:** the canonical general-intensity treatments either assume
symmetry away (Barzykin et al., explicitly, on empirical grounds) or carry the
asymmetry numerically (Guéant 2017; Bergault-Guéant 2021, 2023). Nobody states the
compression, in any form, through August 2026.

---

## Strand 2: Queueing / birth-death theory — ancestry of the mechanism

The mechanism is classical, and the correct citations are:

1. **Ledermann & Reuter (1954)**, "Spectral theory for the differential equations
   of simple birth and death processes", *Phil. Trans. R. Soc. Lond. A* 246,
   321-369 (doi:10.1098/rsta.1954.0001, Crossref-verified), and
   **Karlin & McGregor (1957)**, "The differential equations of birth-and-death
   processes, and the Stieltjes moment problem", *Trans. Amer. Math. Soc.* 85,
   489-546 (doi:10.1090/s0002-9947-1957-0091566-1, Crossref-verified).
   These are the canonical sources for the fact that a birth-death generator is
   symmetrizable: conjugating by the square root of the stationary/potential
   measure pi_n = prod(lambda_k/mu_{k+1}) turns the tridiagonal generator into a
   symmetric one whose off-diagonal entries are the geometric means
   sqrt(lambda_n mu_{n+1}). This diagonal conjugation is exactly the (p/(1-p))^{x/2}
   absorption behind Theorem 1, and the geometric mean is where 2 sqrt(p(1-p))
   comes from. Karlin-McGregor build their entire spectral theory on this
   self-adjointness; Ledermann-Reuter precede them for the simple case.

2. **Exponential tilting of the +-1 random walk.** The identity
   min_theta E[e^{theta X}] = 2 sqrt(pq) for a p/q signed Bernoulli step — i.e.
   p e^{-t} + q e^{t} = 2 sqrt(pq) cosh(t - (1/2)log(p/q)), the paper's Eq. (5)
   verbatim — is the Cramér/Chernoff change of measure that centers an asymmetric
   walk: **Chernoff (1952)**, "A measure of asymptotic efficiency for tests of a
   hypothesis based on the sum of observations", *Ann. Math. Stat.* 23, 493-507
   (doi:10.1214/aoms/1177729330, Crossref-verified). The factor sqrt(4pq) also
   pervades the classical random-walk generating functions in **Feller**,
   *An Introduction to Probability Theory and Its Applications*, Vol. I (3rd ed.,
   Wiley, 1968), Ch. XI and XIV (first-passage f(s) = (1 - sqrt(1-4pq s^2))/(2qs)).

3. **M/M/1 transient solution.** The geometric-mean rate appears explicitly in the
   classical transient law p_k(t) = e^{-(lambda+mu)t}[rho^{(k-i)/2} I_{k-i}(at) +
   ...] with a = 2 sqrt(lambda mu) — half-integer powers of the rate ratio
   (the tilt) times Bessel functions at the geometric-mean clock (verified against
   the standard formula as given in Kleinrock, *Queueing Systems* Vol. 1, 1975).
   Original: **Bailey (1954)**, "A continuous time treatment of a simple queue
   using generating functions", *JRSS B* 16, 288-291
   (doi:10.1111/j.2517-6161.1954.tb00172.x, Crossref-verified). Textbooks: Cohen,
   *The Single Server Queue* (North-Holland, 1969); Kleinrock (1975).

4. **Decay parameter.** The M/M/1 relaxation rate (sqrt(lambda)-sqrt(mu))^2 =
   (lambda+mu) - 2 sqrt(lambda mu) is the additive shadow of the multiplier M(p):
   normalizing lambda+mu = 1, the spectral gap is 1 - 2 sqrt(p(1-p)) = 1 - 1/M(p).
   General birth-death decay parameters: **van Doorn (1985)**, "Conditions for
   exponential ergodicity and bounds for the decay parameter of a birth-death
   process", *Adv. Appl. Prob.* 17, 514-530 (doi:10.2307/1427118,
   Crossref-verified).

**Strand 2 conclusion:** cite Ledermann-Reuter (1954) and Karlin-McGregor (1957)
for the symmetrizing conjugation of birth-death generators, and Chernoff (1952)
(with Feller Vol. I as the textbook anchor) for the exponential tilt producing
2 sqrt(pq) cosh(.). No queueing source, of course, contains the market-making
objects (quotes, skew, width, carrying cost) or the economic decomposition.

---

## Strand 3: Inventory theory

Crossref sweeps on base-stock/(s,S) with asymmetric demand, demand-imbalance
transformations, and state-dependent-rate equivalences (e.g. Hill-Pakkala 2007;
Olsson 2018, *Math. Meth. OR* 90) return birth-death *machinery* (level-dependent
rates, matrix-geometric methods) but **no compression of an imbalanced-demand
problem onto a balanced one, and no imbalance-as-cost-multiplier decomposition**.
Zipkin's *Foundations of Inventory Management* (2000) treats asymmetric
demand/supply rates via standard Markov-chain analysis; no symmetrization theorem
with an economic reading is known there, and none surfaced in the searches.
NOTHING FOUND.

---

## Strand 4: Insurance / actuarial

The actuarial price-optimization literature (win/renewal-probability curves,
Lerner-type FOCs — see novelty_imbalance.md, R2) shares the *first-order
condition* with this paper but not the symmetry: Crossref sweeps on premium
optimization + renewal/win probability + asymmetric/symmetric equivalence return
ruin-theoretic and demand-elasticity work (e.g. Jasiulewicz 2001; Venezia 1979)
with **no mapping of an asymmetric win-rate/renewal problem onto a symmetric
one**. NOTHING FOUND.

---

## Strand 5: Physics adjacency (lineage sharpener)

The same conjugation is standard in exclusion processes: the partially asymmetric
exclusion process (rates p right / q left) maps by a similarity transformation
with factors (p/q)^{x/2} onto a symmetric (Hermitian XXZ-type) operator whose
hopping scale is the geometric mean sqrt(pq). Canonical citations, both
Crossref-verified:
- **Gwa & Spohn (1992)**, "Six-vertex model, roughened surfaces, and an asymmetric
  spin Hamiltonian", *Phys. Rev. Lett.* 68, 725-728
  (doi:10.1103/physrevlett.68.725) — the ASEP-to-spin-chain mapping;
- **Sandow (1994)**, "Partially asymmetric exclusion process with open
  boundaries", *Phys. Rev. E* 50, 2660-2667 (doi:10.1103/physreve.50.2660) — uses
  the (p/q)^{x/2} gauge/similarity transformation explicitly.
(Optionally the review: G. M. Schütz, "Exactly solvable models for many-body
systems far from equilibrium", in *Phase Transitions and Critical Phenomena*,
Vol. 19, Academic Press, 2001 — bibliographic details standard but not
Crossref-verifiable as a book chapter.)
One citation (Sandow 1994, or Gwa-Spohn 1992) suffices to acknowledge the physics
lineage of the gauge transform.

---

## Strand 6: "Imbalance as a multiplier on effective carrying cost" — the
## economic reading

Direct searches (Crossref + Semantic Scholar) for any statement that order
imbalance *multiplies* a dealer's effective inventory/carrying cost — "one-sided
flow taxes inventory", "imbalance as carrying-cost multiplier", and variants —
return **nothing**. The empirical literature documents the qualitative direction:
dealers in one-sided markets provide less liquidity at worse prices (e.g.
Kruttli-Macchiavelli-Monin, "Liquidity Provision in a One-Sided Market: The Role
of Dealer-Hedge Fund Relations", SSRN 2023; Butz-Oomen 2019 on flow-skewing at
flat inventory, already cited in the paper), but no source states — let alone
derives — a closed-form multiplier on carrying cost, and the specific functional
form 1/(2 sqrt(p(1-p))) appears nowhere in an economic context. NOTHING FOUND.

---

## VERDICT

**Has anyone stated this symmetry in a market-making / economic context? NO.**
Through August 2026, no paper states an exact equivalence between the
asymmetric-flow and symmetric-flow market-making problems — not the delta-shift,
not the gamma-widening, not the carrying-cost multiplier M(p), and not the
three-part decomposition. The general-intensity strand of the literature either
assumes symmetry away explicitly (Barzykin-Bergault-Guéant 2021-2024: "we
noticed that intensities on the bid and ask sides were not significantly
different. Therefore, we assumed Lambda_k^b = Lambda_k^a") or handles asymmetry
numerically with no structural statement (Guéant 2017; Bergault-Guéant 2021,
2023).

**Partial anticipation:** only of the corollary, not the theorem.
Bergault-Guéant (2023, arXiv:2309.04216) observe *numerically* that flow-aware
market makers "skew their quotes even in the absence of inventory" — well after
this work was completed (around 2015), with no closed form and no equivalence.
Butz-Oomen (2019) document the practice empirically.

**Mechanism ancestry (cite honestly):** the algebra is the classical
symmetrization of birth-death/tridiagonal generators — conjugate by the square
root of the potential measure, geometric-mean rates appear — canonical in
Ledermann-Reuter (1954) and Karlin-McGregor (1957); equivalently, the
Cramér-Chernoff exponential tilt of an asymmetric +-1 walk, whose minimized
moment generating function is 2 sqrt(pq) (Chernoff 1952; Feller Vol. I). The
geometric-mean clock 2 sqrt(lambda mu) is visible in Bailey's (1954) M/M/1
transient solution, and the same gauge transform is standard for the asymmetric
exclusion process (Gwa-Spohn 1992; Sandow 1994). None of these contains quotes,
skew, width, carrying cost, or any economic decomposition.

**What is claimable as new:** (i) the statement and use of the compression *as a
theorem about optimal dealer behavior*; (ii) the three-part economic
decomposition — translation of skew (log-odds times half-width), widening
(second order), carrying-cost multiplier M(p) = 1/(2 sqrt(p(1-p))) — all tied to
the one observable w; (iii) the zero-inventory-skew corollary as an exact result;
(iv) the reading "imbalance manufactures carry". No prior art found for any of
these.

### Suggested acknowledgment paragraph for the paper

> The mathematical mechanism behind Theorem 1 is old. The identity (5) is the
> Cramér--Chernoff exponential tilt of an asymmetric $\pm1$ random walk, whose
> minimized moment generating function is $2\sqrt{p(1-p)}$ \cite{chernoff1952};
> equivalently, the consistency equation inherits the classical symmetrization of
> birth--death generators --- conjugate the tridiagonal operator by the square
> root of its potential measure and geometric-mean rates appear --- which
> underlies the spectral theory of Ledermann and Reuter \cite{ledermannreuter1954}
> and Karlin and McGregor \cite{karlinmcgregor1957}, surfaces in the transient
> M/M/1 law through the factor $2\sqrt{\lambda\mu}$ \cite{bailey1954}, and
> reappears in statistical physics as the gauge transformation taking the
> asymmetric exclusion process to a symmetric operator \cite{sandow1994}. What we
> claim is not the transformation but its market-making instantiation and
> economics: that enquiry imbalance compresses exactly onto the balanced dealer
> problem, and that the compression decomposes into a skew translation, a
> widening, and a multiplication of the effective cost of carry, each in closed
> form in the single observable $w$. To our knowledge no such statement exists in
> the market-making, inventory, or insurance literatures; the general-intensity
> treatments closest to it either impose symmetric intensities on empirical
> grounds \cite{barzykin2023} or carry the asymmetry numerically
> \cite{gueant2017,bergaultgueant2021}.

### BibTeX-ready ancestral citations (all Crossref-verified 2026-08-07 except as noted)

- Ledermann, W., Reuter, G. E. H. (1954). Spectral theory for the differential
  equations of simple birth and death processes. *Phil. Trans. R. Soc. Lond. A*
  246(914), 321-369. doi:10.1098/rsta.1954.0001
- Karlin, S., McGregor, J. L. (1957). The differential equations of
  birth-and-death processes, and the Stieltjes moment problem. *Trans. Amer.
  Math. Soc.* 85, 489-546. doi:10.1090/S0002-9947-1957-0091566-1
- Chernoff, H. (1952). A measure of asymptotic efficiency for tests of a
  hypothesis based on the sum of observations. *Ann. Math. Statist.* 23(4),
  493-507. doi:10.1214/aoms/1177729330
- Bailey, N. T. J. (1954). A continuous time treatment of a simple queue using
  generating functions. *J. R. Statist. Soc. B* 16(2), 288-291.
  doi:10.1111/j.2517-6161.1954.tb00172.x
- Feller, W. (1968). *An Introduction to Probability Theory and Its
  Applications*, Vol. I, 3rd ed. Wiley. (Ch. XI, XIV.) [book; not Crossref]
- van Doorn, E. A. (1985). Conditions for exponential ergodicity and bounds for
  the decay parameter of a birth-death process. *Adv. Appl. Prob.* 17(3),
  514-530. doi:10.2307/1427118 [optional]
- Gwa, L.-H., Spohn, H. (1992). Six-vertex model, roughened surfaces, and an
  asymmetric spin Hamiltonian. *Phys. Rev. Lett.* 68(6), 725-728.
  doi:10.1103/PhysRevLett.68.725 [optional]
- Sandow, S. (1994). Partially asymmetric exclusion process with open
  boundaries. *Phys. Rev. E* 50(4), 2660-2667. doi:10.1103/PhysRevE.50.2660

### Honest caveats

1. Guéant's 2016 CRC *book* remains uninspected in physical form (same flag as
   novelty_imbalance.md); the arXiv article version (1605.01862) that contains
   the same general model was full-text checked and contains no equivalence.
2. arXiv API searches cover titles/abstracts, not full text; the full-text
   checks above cover every paper whose model allows asymmetric intensities in
   the Guéant school plus CDJ 2017. A symmetrization buried in an appendix of a
   paper whose abstract never mentions asymmetry cannot be fully excluded, but
   the Barzykin-Bergault-Guéant symmetric-by-assumption quotes make it unlikely
   the school possesses the reduction (they would have used it rather than
   assume symmetry).
3. WebSearch quota was exhausted at task start; SSRN-only working papers are
   underrepresented in the sweep (Crossref catches SSRN DOIs, and none surfaced).
4. Inventory (Zipkin 2000) and Cohen (1969), Kleinrock (1975), Feller (1968),
   Schütz (2001) are books: contents characterized from standing knowledge and
   (for Kleinrock's M/M/1 transient formula) verified against a secondary
   source; bibliographic details not Crossref-checkable.
