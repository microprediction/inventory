# Novelty / Prior-Art Assessment: Imbalance Equivalence Paper

Scope: the four results (R1–R4) to be split out of Cotton & Papanicolaou, *Trading
Illiquid Goods*. The underlying work was completed around 2015 and
first written up April 2022. Model: sealed-bid RFQ market
making in an illiquid good; Poisson enquiries (mean gap τ), sell w.p. p / buy w.p.
1−p; best competing dealer response beyond fair value exponential with mean w = 1/h;
adverse selection ε; policy characterized by inventory indifference cost ν(x), with
skew S(x) = slope and discretionary width C(x) = convexity of ν.

Method: full-text reads of the key stochastic-control papers (arXiv/ar5iv), citation
verification via Crossref (all DOIs below checked 2026-08). Web-search budget was
exhausted mid-task, so a small number of content claims rest on abstracts plus
standing knowledge; these are flagged explicitly in "Honest flags."

---

## R1 — The imbalance equivalence (δ-shift, γ-widening, carrying-cost multiplier M(p))

**Claim being assessed.** Enquiry imbalance p ≠ 1/2 is *exactly* equivalent to the
balanced problem with (i) skew translated by δ = log((1−p)/p)/(2h); (ii)
non-discretionary width widened by γ = [log(1/2) − (log p + log(1−p))/2]/h; (iii)
carrying cost multiplied by M(p) = e^{hγ} = 1/(2√(p(1−p))). Corollary: a dealer with
zero inventory optimally skews by δ — skew responds to flow imbalance independently
of inventory.

**Verdict: NOVEL in 2011, and still NOVEL as a stated theorem in 2026.** No paper
found that states the three-part equivalence (shift + widen + multiplier), the
closed-form multiplier 1/(2√(p(1−p))), or the flat-inventory skew δ as an exact
consequence of stationary flow imbalance.

What the closest strands actually contain:

- **Avellaneda & Stoikov (2008).** Symmetric arrival intensity Λ(δ) = A e^{−kδ} on
  both sides, same A and k. No flow imbalance anywhere. Quotes: reservation price
  (value-function based) ± half-spread; approximate constant-width linear-skew
  solution. Nothing resembling δ, γ, or M(p).
- **Guéant–Lehalle–Fernandez-Tapia (arXiv May 2011; MAFE 2012), full text read.**
  Intensities are *identical* on bid and ask: λ^b(δ) = λ^a(δ) = A e^{−kδ} (verified
  in the ar5iv full text). Exact quotes are δ^b* = (1/k)ln(v_q/v_{q+1}) +
  (1/γ)ln(1+γ/k), and the asymptotic closed forms have constant spread and skew
  linear in q. The only asymmetry they treat is a *price drift* μ, which shifts
  quotes by ±μ/(γσ²)·(scale) — a pure shift, with **no width term and no cost
  multiplier**, and it is drift in the mid-price, not imbalance in enquiry arrival
  rates. So: they have the germ of a shift under directional asymmetry, but of a
  different asymmetry, derived only asymptotically, and with no equivalence
  statement.
- **Guéant, "Optimal market making" (arXiv 2016; also the 2016 CRC book), full text
  read.** The general model *does allow* Λ^b ≠ Λ^a, and the optimal quotes are
  characterized by a hazard-rate-type implicit condition involving Λ/(−Λ′) and value
  function finite differences. But with asymmetric intensities he provides **no
  closed form, no log(A^b/A^a)/(2k) shift term, no widening term, and no statement
  that the asymmetric problem is equivalent to a symmetric one with modified
  costs** (checked in the ar5iv full text; the fetch found no such equivalence
  claim). Asymmetry is handled numerically through the HJB system.
- **Bergault–Evangelista–Guéant–Vieira (arXiv 2018), "Closed-form approximations in
  multi-asset market making," full text checked.** Allows Λ^{i,b} ≠ Λ^{i,a}; quotes
  come through inverse-Hamiltonian derivatives; **no log-ratio shift formula and no
  symmetric-equivalence/multiplier statement.**
- **Cartea–Jaimungal–Ricci (SIAM J. Fin. Math. 2014) and Cartea–Jaimungal,
  "Incorporating order-flow into optimal execution" (MAFE 2016); Cartea–Jaimungal–
  Penalva book (2015) ch. 10.** Order-flow imbalance enters as a *state variable /
  short-term-alpha signal* that predicts price moves; optimal postings shift with
  the signal. This is (a) post-2011, (b) a dynamic signal model rather than a
  stationary p ≠ 1/2 structural result, and (c) contains no exact equivalence, no
  width effect, no carrying-cost multiplier. (Content of CJR 2014 and book ch. 10
  characterized from abstract + standing knowledge — see flags.)
- **Garman (JFE 1976).** Has genuinely asymmetric Poisson buy/sell rates λ_a(p_a),
  λ_b(p_b) — the oldest such model — but the dealer sets a single *static* price
  pair (no inventory-dependent policy), and the content is the ruin/failure result:
  the dealer must set prices so expected inflows are positive or fail with
  probability one. No optimal skew, no equivalence, no policy characterization.
- **Amihud–Mendelson (JFE 1980).** Semi-Markov inventory model with price-dependent
  (and possibly asymmetric) arrival functions; results: optimal bid/ask are monotone
  decreasing in inventory and there is a *preferred inventory position*. This is the
  closest classical antecedent in spirit: imbalanced flow moves the preferred
  position and quotes. But everything is qualitative/structural (monotonicity,
  existence); **no closed-form shift δ, no width γ, no multiplier M(p), no exact
  equivalence to a balanced problem.**
- **Ho–Stoll (JFE 1981).** Reservation-price quoting from value-function
  differences; symmetric transaction demand; skew driven by inventory only. No flow
  imbalance.
- **Pre-2011 sealed-bid / RFQ market making.** Nothing found. The RFQ dealer
  literature with win-probability curves begins for practical purposes with
  Fermanian–Guéant–Pu (2016/2017) and continues with Guéant–Manziuk (2019),
  Bergault–Guéant (2021), Barzykin–Bergault–Guéant (2023). All post-date 2011.

**Zero-inventory-skew corollary.** In the drift extension of GLFT, quotes at q = 0
are also shifted — but by predicted *price movement*, not by flow imbalance; the
distinction (skewing because of who is likely to call next, at flat inventory and
zero drift) is not stated anywhere found. Novel then and now as a theorem;
practitioners plainly do this (see empirics below), which is motivation, not
anticipation.

**Material caveat (be candid in the paper).** The mathematical mechanism of R1 is a
symmetrization of a birth–death/tridiagonal structure (absorb (η^b/η^a)^{x/2} into
the value function; the geometric mean √(η^bη^a) appears — whence 2√(p(1−p))). In
the GLFT linear system with A^b ≠ A^a the analogous transformation is *derivable* by
the same trick, so a referee could say the result is "latent" in that framework.
Nobody has stated it, and the width-plus-multiplier decomposition with its economic
reading (imbalance taxes the carry) is not in the literature — but the paper should
present R1 as an exact equivalence theorem with an economic interpretation, not as a
technically deep transformation.

---

## R2 — Sealed-bid best-response formulation; distribution-free FOC m* = 1/h(m*) + K

**Verdict: NOVEL in 2011 within market making; the bare FOC is classical; the
formulation is now standard in the post-2016 RFQ literature (which it predates).**

- The FOC itself — optimal markup = inverse hazard rate of the win-probability curve
  plus marginal cost — is monopoly pricing / first-price-auction best-response logic
  (Lerner-type condition with demand = survival function of the best competing
  quote). It is classical in economics and in actuarial premium-optimization, and
  cannot be claimed as new mathematics.
- What was new in 2011 in the *market-making* context: (i) casting each enquiry as a
  sealed-bid auction against an exponential best competing response; (ii) making the
  "cost" in the Lerner condition the *indifference-adjusted strike* K (adverse
  selection + marginal inventory indifference cost), so that "markup = width +
  adverse selection + marginal inventory cost"; (iii) doing this distribution-free
  via the hazard rate h(m).
- Nearest simultaneous work: GLFT (arXiv May 2011) and later Guéant (2016/2017) have
  the same *shape* of FOC — δ* solves a condition in Λ/(−Λ′) plus a value-function
  difference — for limit-order fills rather than RFQ auctions. Guéant (2017) is
  fully general in Λ and is the cleanest statement in that line; it is 5–6 years
  later.
- The empirically grounded RFQ/win-probability dealer models — Fermanian–Guéant–Pu
  (2016/2017), Guéant–Manziuk (2019), Bergault–Guéant (2021), Barzykin–Bergault–
  Guéant (2023) — all post-date 2011. FGP is empirical/econometric (RFQ win
  probabilities on an MD2C platform), not an optimal-quoting theorem.

Positioning: claim priority for the RFQ/sealed-bid *formulation* of market making
and the indifference-adjusted strike, not for hazard-rate pricing per se.

---

## R3 — Skew = slope, discretionary width = convexity of the indifference cost

**Verdict: slope half ANTICIPATED implicitly; convexity half NOT found stated
anywhere — novel as an explicit exact characterization, but flag as close.**

- Skew = slope: implicit in Ho–Stoll (1981) reservation-price quoting (bid and ask
  are first differences of the dealer's value function) and explicit-in-substance in
  GLFT/Guéant, where quotes are monotone transforms of value-function finite
  differences ((1/k)ln(v_q/v_{q+1}), or H′ evaluated at (θ(q)−θ(q±1))). The mid-quote
  skew equal to the *centered secant slope* of the indifference cost is a cleaner
  statement, but a referee will read it as folklore.
- Width = convexity: the identity that the *discretionary* component of quoted width
  (over the floor Δ = 1/h + ε) equals the second difference C(x) of ν — i.e., a
  dealer's width reveals the convexity of her inventory cost, exactly — was not
  found stated in any paper checked (GLFT's asymptotic spread is constant and
  inventory-independent, which is the degenerate linear-ν case; Guéant 2017's spread
  is a sum of transformed finite differences from which convexity could be extracted
  but is not). Claim this half; concede the slope half as known in substance.
- The off-policy/"revealed inventory cost" use (infer ν from observed skew and
  width) appears to be novel and is worth emphasizing; the later RFQ literature does
  not run the inverse direction.

---

## R4 — Fill-ratio invariance: expected net gain per won trade = s·w at the optimum

**Verdict: NOVEL as stated; the underlying mechanism is a known property of
exponential demand — say so.**

Under an exponential best-competing-response, the optimum has constant absolute
margin over the (indifference-adjusted) strike: m* − K = 1/h = w, so the expected
net gain per won trade is s·w *independent of inventory*, and all inventory
dependence loads onto the win probability. The constant-markup property of
exponential (log-linear) demand is classical pricing economics; the market-making
consequence — differential direct carry cost = differential fill probability × size
× width, an invariance across inventory states usable as a diagnostic on fill
ratios — was not found anywhere. No precedent located in the market-making or RFQ
literature. Present it as a corollary with the honest attribution of the mechanism.

---

## Empirical support for the motivation (flat-inventory skewing on flow)

- Butz & Oomen, *Internalisation by electronic FX spot dealers*, Quantitative
  Finance 19(1), 2019: documents how electronic FX dealers manage flow via skewing
  and internalisation — direct practitioner evidence that quotes are skewed in
  response to expected flow, not only inventory.
- Hendershott & Madhavan, *Click or Call? Auction versus Search in the
  Over-the-Counter Market*, Journal of Finance 70(1), 2015: bond RFQ auctions,
  response/win behavior of dealers — supports the sealed-bid RFQ framing.
- Fermanian–Guéant–Pu (2016/2017): econometrics of dealer answer/win probabilities
  in corporate-bond RFQ — supports the exponential/logistic win-curve assumption.
- No pre-2011 academic documentation of flat-inventory flow-skewing was found; it
  lived in practice. This strengthens the claim that R1's corollary formalized a
  practice before the literature described it.

---

## Recommended positioning paragraph (draft)

Relative to the Avellaneda–Stoikov / Guéant–Lehalle–Fernandez-Tapia line, the
contribution is threefold. First, the market-making problem is posed as a sequence
of sealed-bid auctions against a best competing response — the request-for-quote
mechanism by which illiquid goods actually trade — yielding a distribution-free
first-order condition, markup = inverse hazard of the win curve + indifference-
adjusted strike, that predates the RFQ optimal-quoting literature (Fermanian–Guéant–
Pu 2017; Guéant–Manziuk 2019; Bergault–Guéant 2021) by several years. Second,
whereas that line either assumes symmetric arrival intensities (Avellaneda–Stoikov
2008; GLFT 2012) or accommodates asymmetric ones only numerically (Guéant 2017;
Bergault et al. 2021), we prove that enquiry imbalance is *exactly* equivalent to a
balanced problem with quotes skewed by log((1−p)/p)/2h, non-discretionary width
widened by γ, and carrying cost inflated by 1/(2√(p(1−p))) — in particular, a dealer
with zero inventory optimally skews on flow alone, a practice documented empirically
(Butz–Oomen 2019) but not previously derived. Third, the optimal policy is
characterized exactly by an inventory indifference cost whose slope is the skew and
whose convexity is the discretionary width — the slope half is implicit in
reservation-price dealer models since Ho–Stoll (1981); the convexity half, and the
resulting ability to read a dealer's inventory cost off her quoting behavior, is
new.

---

## Must-cite list (all citations verified via Crossref, 2026-08)

1. Garman, M. B. (1976). Market microstructure. *Journal of Financial Economics*,
   3(3), 257–275. doi:10.1016/0304-405X(76)90006-4
2. Amihud, Y., & Mendelson, H. (1980). Dealership market: Market-making with
   inventory. *Journal of Financial Economics*, 8(1), 31–53.
   doi:10.1016/0304-405X(80)90020-3
3. Ho, T., & Stoll, H. R. (1981). Optimal dealer pricing under transactions and
   return uncertainty. *Journal of Financial Economics*, 9(1), 47–73.
   doi:10.1016/0304-405X(81)90020-9
4. Avellaneda, M., & Stoikov, S. (2008). High-frequency trading in a limit order
   book. *Quantitative Finance*, 8(3), 217–224. doi:10.1080/14697680701381228
5. Guéant, O., Lehalle, C.-A., & Fernandez-Tapia, J. (2012). Dealing with the
   inventory risk: A solution to the market making problem. *Mathematics and
   Financial Economics*, 7(4), 477–507 (arXiv:1105.3115, first posted 16 May 2011).
   doi:10.1007/s11579-012-0087-0
6. Guéant, O. (2016). *The Financial Mathematics of Market Liquidity: From Optimal
   Execution to Market Making*. Chapman & Hall/CRC. (See also Guéant, "Optimal
   market making," arXiv:1605.01862, 2016–2017.)
7. Cartea, Á., Jaimungal, S., & Ricci, J. (2014). Buy low, sell high: A high
   frequency trading perspective. *SIAM Journal on Financial Mathematics*, 5(1),
   415–444. doi:10.1137/130911196
8. Cartea, Á., & Jaimungal, S. (2016). Incorporating order-flow into optimal
   execution. *Mathematics and Financial Economics*, 10(3), 339–364.
   doi:10.1007/s11579-016-0162-z
9. Cartea, Á., Jaimungal, S., & Penalva, J. (2015). *Algorithmic and
   High-Frequency Trading*. Cambridge University Press. (Ch. 10.)
10. Guilbaud, F., & Pham, H. (2013). Optimal high-frequency trading with limit and
    market orders. *Quantitative Finance*, 13(1), 79–94.
    doi:10.1080/14697688.2012.708779
11. Fodra, P., & Pham, H. (2015). High frequency trading and asymptotics for small
    risk aversion in a Markov renewal model. *SIAM Journal on Financial
    Mathematics*, 6(1), 656–684. doi:10.1137/140976005
12. Fermanian, J.-D., Guéant, O., & Pu, J. (2017). The behavior of dealers and
    clients on the European corporate bond market: The case of multi-dealer-to-
    client platforms. *Market Microstructure and Liquidity*, 2(3–4), 1750004.
    doi:10.1142/S2382626617500046
13. Guéant, O., & Manziuk, I. (2019). Deep reinforcement learning for market making
    in corporate bonds: Beating the curse of dimensionality. *Applied Mathematical
    Finance*, 26(5), 387–452. doi:10.1080/1350486X.2020.1714455
14. Bergault, P., & Guéant, O. (2021). Size matters for OTC market makers: General
    results and dimensionality reduction techniques. *Mathematical Finance*, 31(1),
    279–322. doi:10.1111/mafi.12286
15. Bergault, P., Evangelista, D., Guéant, O., & Vieira, D. (2018–2021). Closed-form
    approximations in multi-asset market making. arXiv:1810.04383 (published in
    *Applied Mathematical Finance*; cite journal version in final draft).
16. Barzykin, A., Bergault, P., & Guéant, O. (2023). Algorithmic market making in
    dealer markets with hedging and market impact. *Mathematical Finance*, 33(1),
    41–79. doi:10.1111/mafi.12367
17. Hendershott, T., & Madhavan, A. (2015). Click or call? Auction versus search in
    the over-the-counter market. *Journal of Finance*, 70(1), 419–447.
    doi:10.1111/jofi.12164
18. Butz, M., & Oomen, R. (2019). Internalisation by electronic FX spot dealers.
    *Quantitative Finance*, 19(1), 35–56. doi:10.1080/14697688.2018.1504167

---

## Honest flags

1. **Timing vs GLFT.** GLFT hit arXiv 16 May 2011; this work was completed around
   2015, so GLFT precedes it. For the FOC-shape overlap in R2, present the
   RFQ formulation as independent and in a different mechanism (sealed-bid vs
   limit-order-book, imbalanced vs symmetric flow), not as prior.
2. **R1 "latency" in GLFT.** The δ-shift and √(p(1−p)) multiplier can be *derived*
   from the GLFT-style linear system with A^b ≠ A^a via a standard birth–death
   symmetrization. No one has published this. Claim the theorem and its economics;
   do not oversell the technique.
3. **CJR 2014 / CJ book ch. 10 content** was characterized from abstracts and
   standing knowledge (search budget exhausted); before submission, verify from the
   texts that neither contains an exact stationary-imbalance equivalence (highly
   unlikely — both are signal/short-term-alpha models — but check).
4. **R2's FOC is classical economics** (Lerner condition with survival-function
   demand; also standard in actuarial price optimization pre-2011). Cite the logic
   as known; claim only the market-making/RFQ instantiation with the indifference-
   adjusted strike.
5. **R3 slope half is folklore** (Ho–Stoll reservation prices; GLFT value-function
   differences). Claim only the exact two-sided characterization and the convexity
   = discretionary width half, plus the inverse ("revealed inventory cost") use.
6. **R4's mechanism** (constant margin under exponential demand) is classical;
   the invariance-as-diagnostic across inventory states is what is new.
7. **Bergault et al. (2018) closed forms** were checked in the arXiv full text via
   an automated reader; a final human pass over their Hamiltonian expansions is
   prudent to confirm no log(A^b/A^a) shift term appears in an appendix.
8. Guéant's 2016 *book* was not directly inspected (only arXiv:1605.01862); the
   book's drift/trend chapter should be skimmed before submission to confirm no
   imbalance-equivalence statement.
