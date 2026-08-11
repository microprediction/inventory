# Prior-art sweep: the exponential normal form

Verified web sweep of 2026-08-11 (searches plus arXiv abstract fetches; full texts
where linked). Companion-paper prior art (Karlin–McGregor, Chernoff, ASEP gauge,
the imbalance equivalence itself) is documented in
`../skew_width_imbalance/symmetry_prior_art.md` and was excluded here. Where only
an abstract was seen, that is flagged. Honest absences are recorded as such.

## 1. Normal form for arbitrary win curves

Verdict: NOVEL; nearest neighbors strictly weaker.

- Campi & Zabaljauregui, "Optimal Market Making under Partial Information with
  General Intensities," Applied Mathematical Finance 27(1–2), 1–45, 2020
  (arXiv:1902.01157, doi 10.1080/1350486X.2020.1758587): general decreasing
  intensities via viscosity solutions; no translation identity, no normal
  coordinates.
- Guéant & Lehalle, "General Intensity Shapes in Optimal Liquidation,"
  Mathematical Finance 25(3), 457–495, 2015 (arXiv:1204.0148, doi
  10.1111/mafi.12052): the canonical beyond-exponential-intensity paper
  (execution side); general Hamiltonian characterization, no
  imbalance-as-translation. This is the state of the art the normal form goes
  beyond; cite it as such.
- The exponential-case linearization is GLFT (arXiv:1105.3115) and Guéant 2017
  (AMF 24(2), 112–154) — exponential-only, which is the foil.
- Queueing/stat-phys sweeps (birth–death symmetrization with general jumps,
  geometric-mean rates, arXiv:1509.02511, intertwining literature): the
  h-transform symmetrization is classical, but nothing resembling U/V
  coordinates built from the log of an optimized value function, and no identity
  qG(K+) + (1−q)G(K−) = 2√(q(1−q)) G* e^{−U} cosh(V−ℓ) for arbitrary F̄.
- Feys, "Axiomatic Market Making," arXiv:2606.09454 (June 2026): translation
  symmetry as an axiom, skew odd in inventory, but forces a linear-in-inventory
  three-parameter family; an axiomatic uniqueness result, not a
  nonlinear-coordinates result (abstract-level check). Cite as contemporaneous
  contrast.

Caveat: Guéant's 2016 book interior and all 2026 preprints could not be
full-text-searched; the cosh/log-odds structure in the exponential case pervades
the Guéant school, so the novelty must be phrased as "arbitrary F̄," not the cosh
identity per se.

## 2. Rigidity / exponential characterization

Verdict: ANTICIPATED-BY (classical) for the functional-equation core; NOVEL for
the Hamiltonian-level affine-exponential theorem.

- "G(K+a)/G(K) independent of K forces exponential" is the multiplicative Cauchy
  equation / lack-of-memory characterization. Citations: Galambos & Kotz,
  Characterizations of Probability Distributions, LNM 675, Springer, 1978;
  Marsaglia & Tubilla, "A Note on the 'Lack of Memory' Property of the
  Exponential Distribution," Annals of Probability 3(2), 353–354, 1975 (doi
  10.1214/aop/1176996406 — notable for weakening the hypothesis to a partial set
  of shifts); Aczél, Lectures on Functional Equations and Their Applications,
  Academic Press, 1966. Strongest modern form: integrated Cauchy equation /
  Deny's theorem (Lau–Rao; Ramachandran survey, Adv. Appl. Prob.). The paper
  should present its sidewise rigidity as a pricing-theoretic instance of this
  literature.
- Economic cousin: exponential demand as unique constant-absolute-markup demand;
  citation shape is the pass-through literature (Weyl & Fabinger, JPE 121(3),
  528–583, 2013, doi 10.1086/670401). No paper found stating the exact converse
  as a theorem.
- Hamiltonian-level analogue (affine-exponential C + Be^{−hK} as the maximal
  class where the asymmetric two-sided problem reduces by rigid translations):
  NOTHING FOUND in market making, queueing, or the characterization literature.
  Frame as extending the memorylessness characterization to the level of the
  pricing Hamiltonian.

## 3. Integrability defect

Verdict: NOVEL as applied; underlying mathematics classical and must be cited.

- The object — per-edge tilts failing to be a gradient — is the territory of
  Kolmogorov's criterion for reversibility (Kolmogoroff, "Zur Theorie der
  Markoffschen Ketten," Math. Annalen 112, 155–160, 1936 — standard citation,
  not independently re-verified; textbook: Kelly, Reversibility and Stochastic
  Networks, Wiley 1979). Modern nonequilibrium literature phrases the
  obstruction as cycle affinity / probability currents (Zia & Schmittmann,
  cond-mat/0701763; response literature arXiv:1905.07449). Note for the paper:
  on the one-dimensional inventory lattice the obstruction enters through the
  pairing of up and down strikes over each bond, not through cycles, so the
  citation is for the genre of discrete integrability conditions, not a direct
  transplant.
- Connection to market making / inventory / dealer pricing: searched Kolmogorov
  criterion + market making/inventory, detailed balance violation + market
  making, cycle affinity + dealer/order flow — NOTHING FOUND. Closest hits were
  econophysics money-exchange models (arXiv:2311.01535, J. Phys. A 2024) and
  voter models — different objects. No defect functional measuring failure of a
  per-strike gauge to lift to a potential across an inventory lattice exists.

## 4. Perturbation hierarchy

Verdict: PARTIAL — scalar-parameter perturbation around solvable market-making
models is established; functional (curve-valued) deformation of the win curve
appears novel.

- Bergault, Evangelista, Guéant, Vieira, "Closed-form Approximations in
  Multi-asset Market Making," AMF 28(2), 101–142, 2021 (arXiv:1810.04383):
  perturbation in inventory-risk and penalty parameters, exponential
  intensities. The flagship of the approximation school; must cite.
- Lorig-style expansions in algorithmic trading (Barger & Lorig IJTAF 2019;
  Donnelly & Lorig AMF 2020; SIAM J. Fin. Math. doi 10.1137/21m1394473;
  arXiv:1310.1756): scalar/small-parameter expansions, not curve deformations.
- Barzykin–Bergault–Guéant–Lemmel (arXiv:2508.20225): first-order Taylor
  adjustments for adverse selection and price reading — perturbation in
  effect-strength parameters, not in the win curve itself (abstract + HTML
  excerpts).
- General-MDP functional sensitivity: arXiv:1909.07781 (first-order sensitivity
  of the optimal value wrt deviations in the transition function) — the
  general-MDP analogue, worth citing.
- Revenue management "response library" over demand-curve bases: NOTHING FOUND.

## 5. Envelope transfer and admissibility

Verdict: (a) PARTIAL — tool standard, specific device unstated elsewhere; (b)
PARTIAL — citation shape exists, win-curve instance new.

- (a) Milgrom & Segal, Econometrica 70(2), 583–601, 2002 is the right tool
  citation. No paper found stating "transfer a demand-curve perturbation into
  the indirect profit function, then propagate through a quoting problem" — not
  in actuarial premium optimization either (Theismann ASTIN 2025;
  arXiv:1711.07753; arXiv:2605.28327 checked).
- (b) The inverse question "which G arise as sup_m (m−K)F̄(m)": citation shape is
  producer-theory duality (Hotelling's lemma; convex-conjugate recoverability)
  and, on point for the converse direction, Sinander, "The Converse Envelope
  Theorem," Econometrica 2022 (doi 10.3982/ECTA18119, arXiv:1909.11219). The
  model "quote against the survival curve of the best competing bid" goes back
  to Friedman, "A Competitive-Bidding Strategy," Operations Research 4(1),
  104–112, 1956 (doi 10.1287/opre.4.1.104) — cite for the provenance of G.
  Nobody found doing rationalizability for win curves specifically.

## 6. Parity

Verdict: NOVEL at the claimed generality.

- Skew-odd-in-inventory is folklore (Guéant school; axiomatically in Feys
  arXiv:2606.09454, within a forced linear family). That is parity in
  inventory, not in flow log-odds, and not distribution-free.
- Searched skew odd / spread second order / even in imbalance / reflection
  symmetry + market making: NO paper stating that for arbitrary win curves the
  skew is odd and the spread response even in the log-odds of flow imbalance.
  Near-misses: arXiv:2508.20225 (spread widening at zero inventory from price
  reading, informational mechanism); arXiv:2511.02518 (side-dependent widening
  under asymmetric flow) — model-specific, not parity theorems. Caveat: parity
  claims can hide in remarks; full-text absence is harder to guarantee here
  than for items 1–3.

## 7. Recent work 2024–2026

- Exact phrases "exponential normal form" + market/trading, "imbalance gauge",
  "win curve" perturbation: no hits on the concepts.
- Barzykin–Bergault–Guéant line: arXiv:2508.20225 (adverse selection / price
  reading, v6 Aug 2026) — tractable first-order corrections, no normal form.
  arXiv:2604.20406, Barzykin & Ciceri, "Bond Market Making with a Hit-Ratio
  Target" (Apr 2026) — general fill-probability function, exact quote-map
  inversion, quadratic approximation for decompositions; the closest recent
  paper in spirit but no imbalance-translation structure, no parity/rigidity
  (abstract-level). Adjacent: arXiv:2601.13421 (transient impact spot FX);
  arXiv:2603.10569 (win-score promotion gates in aggregator-routed RFQ);
  arXiv:2607.17991 (prediction markets, asymmetric intensities generate skew,
  stochastic-control not structural).

## Must-add citations (applied to the tex 2026-08-11)

1. Galambos & Kotz 1978 (LNM 675) — rigidity.
2. Marsaglia & Tubilla 1975, Ann. Probab. 3(2), 353–354 — rigidity.
3. Aczél 1966 — Cauchy-equation machinery.
4. Kolmogorov 1936 / Kelly 1979 — integrability-defect genre (bibliographic
   details standard; double-check before submission).
5. Milgrom & Segal 2002 — envelope transfer (already cited).
6. Sinander 2022, Econometrica — admissibility converse direction.
7. Friedman 1956, Oper. Res. 4(1), 104–112 — provenance of G.
8. Guéant & Lehalle 2015, Math. Finance 25(3) — general intensity shapes.
9. Bergault–Evangelista–Guéant–Vieira 2021, AMF 28(2) — perturbation genre.
10. Campi & Zabaljauregui 2020, AMF 27(1–2) — general intensities, contrast.
11. Barzykin & Ciceri arXiv:2604.20406; Barzykin–Bergault–Guéant–Lemmel
    arXiv:2508.20225 — contemporaneous context.
12. Optional: Weyl & Fabinger 2013 (pass-through reading); Feys arXiv:2606.09454
    (axiomatic contrast); arXiv:1909.07781 (functional MDP sensitivity).

## Overall assessment

The building blocks are individually classical — memorylessness
characterizations, discrete integrability obstructions, envelope theorems,
perturbation around exponential models — and each now carries its classical
citation. No anticipation was found of the paper's actual claims: the normal
coordinates for arbitrary win curves, the Hamiltonian-level affine-exponential
maximality, the defect functional on the inventory lattice, the functional
perturbation hierarchy, the win-curve rationalizability, or the flow-log-odds
parity theorem. Nearest living relatives: Guéant–Lehalle 2015, Campi–
Zabaljauregui 2020, Barzykin–Ciceri 2026 — cited and positioned against in the
tex. Coverage caveats: several 2026 preprints abstract-level only; buried
remarks, non-English work, and paywalled book interiors not exhaustively ruled
out.
