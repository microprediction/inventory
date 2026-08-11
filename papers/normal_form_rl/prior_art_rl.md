# Prior-art sweep: the normal-form RL architecture

Verified web sweep of 2026-08-11. Locators verified by live search unless
flagged [unverified]. Honest absences recorded. Scope: the components of
`architecture.md` and their composition.

## Component-by-component verdicts

### Potential-based shaping / shaping with a solvable model's value (section 5 of the design)

Mechanism canonical: Ng, Harada, Russell, "Policy Invariance Under Reward
Transformations," ICML 1999, 278–287. Equivalence to critic warm-starting:
Wiewiora, JAIR 19 (2003), 205–208. Nearest operations use: De Moor, Gijsbrechts,
Boute, EJOR 301(2), 535–545, 2022 — potential shaping from heuristic policies in
perishable inventory DQN; differentiate: their potential is a heuristic's, ours
is the exact optimal value of a solvable model. In market making the nearest is
Bergault–Evangelista–Guéant–Vieira (arXiv:1810.04383), whose abstract proposes
closed-form approximations "as initial value functions in reinforcement
learning" — initialization (Wiewiora-equivalent), not telescoping shaping, no
variance analysis. "Bellman control variate" is a coined framing; the classical
control-variate-in-RL citation (policy-gradient baselines) is Greensmith,
Bartlett, Baxter, JMLR 5, 1471–1530, 2004. Honest absence: no exact-solvable-
model shaping potential in trading RL.

### Linearly solvable / KL control

Todorov, "Linearly-solvable Markov decision problems," NIPS 19 (2006 — note the
year; often miscited as 2007), and "Efficient computation of optimal actions,"
PNAS 106(28), 11478–11483, 2009. No application to market making or dealer
inventory found — a claimable connection. If the kinship claimed is the
exponential (Cole–Hopf) linearization of the MM HJB, the right citation is GLFT
2013, not Todorov.

### Residual policy learning

Silver, Allen, Tenenbaum, Kaelbling, arXiv:1812.06298 (coined the term; never
archival) and Johannink et al., ICRA 2019, arXiv:1812.03201 (peer-reviewed);
cite both. Finance: residual-on-analytic exists for hedging (Qiao & Wan,
arXiv:2407.19367 — learns the residual on Black–Scholes delta, with a useful
sample-efficiency precedent: residuals with 3 years of data comparable to direct
learning with 10; arXiv:2306.10743; arXiv:2605.21696 finds deep hedging
effectively learns delta corrections and is regime-fragile — good motivation).
Market making: Falces Marín, Díaz Pardo de Vera, López Gonzalo, PLOS ONE
17(12):e0277042, 2022 — RL modulates the Avellaneda–Stoikov parameters; the
closest MM prior art and a mandatory differentiation (parameter modulation, not
an additive residual in a symmetry frame). Honest absence: no MM paper learns an
additive residual on the exact controller with the residual constrained small.

### Symmetry / equivariance in RL

MDP homomorphisms: Ravindran & Barto (SMDP homomorphisms, IJCAI 2003 [pages
unverified]). Equivariant networks: van der Pol, Worrall, van Hoof, Oliehoek,
Welling, "MDP Homomorphic Networks," NeurIPS 2020. Continuous extension:
Rezaei-Shoshtari et al., NeurIPS 2022 [author list unverified]. Symmetry replay
augmentation: Lin et al., "Invariant Transform Experience Replay," IEEE RA-L
5(4), 6615–6622, 2020 (arXiv:1909.10707). Honest absence, and the sharpest
novelty of the design: an exact, model-derived NONLINEAR coordinate change
placing critic and replay in a frame where flow imbalance vanishes has no
precedent found, in trading or outside. Distinction to draw: equivariant RL
builds symmetry into the function class; this design builds it into the
coordinates of the critic domain using an exact solution.

### Robust MDPs beyond rectangularity; sensitivity penalties

Citation correction: the 2013 robust-MDP paper is Wiesemann, Kuhn, RUSTEM
(Math. OR 38(1), 153–183, 2013), not Sim (Wiesemann–Kuhn–Sim 2014 is
distributionally robust convex optimization — a different paper). Coupled
low-dimensional uncertainty: Goyal & Grand-Clément, "Beyond Rectangularity,"
Math. OR 48(1), 203–226, 2023 — factor-matrix uncertainty, the primary
differentiation target for the win-curve-shape parameterization; Mannor, Mebel,
Xu k-rectangularity [locator unverified]; Steimle, Kaufman, Denton, IISE Trans.
53(10), 2021 (multi-model MDPs — global parameters by construction).
Gradient-penalty ≡ DRO: Gao, Chen, Kleywegt, Oper. Res. 72(3), 1177–1191, 2024
(arXiv:1712.06050) — exactly the first-order sensitivity-penalty equivalence the
design's ρ‖Σ^{1/2}∇J‖ term needs; Derman, Geist, Mannor, NeurIPS 2021
(robustness ≡ regularization in MDPs). Honest absence: the combination —
low-dimensional functional shape uncertainty shared across all states,
sensitivity-penalized — appears in no trading RL work.

### Minimax regret

Savage, JASA 46(253), 55–67, 1951 [pages standard, unverified]; Hansen &
Sargent, Robustness, 2008 (the max–min foil). Regret in uncertain MDPs: Xu &
Mannor, CDC 2009 (parametric regret; NP-hardness — cite when arguing the
low-dimensional uncertainty restores tractability); Ahmed et al., NeurIPS 2013;
Rigter, Lacerda, Hawes, AAAI 2021 (arXiv:2012.04626). The robust-MM foil to
cite: Cartea, Donnelly, Jaimungal, SIAM J. Fin. Math. 8(1), 635–671, 2017
(ambiguity-averse worst-case quotes) and Spooner & Savani, IJCAI 2020
(adversarial max–min MM RL). No market-making application of minimax regret
found.

### Market-making RL 2018–2026

Spooner et al., AAMAS 2018; Guéant & Manziuk, AMF 26(5), 387–452, 2019 (the
closest methodological neighbor on the exact-model side); Gašperov et al.,
Mathematics 9(21):2689, 2021 (survey [author list unverified]); recent: Hawkes
LOB (arXiv:2207.09951), IJCNN 2023 (arXiv:2305.15821), options
(arXiv:2307.01814), non-Markov (Risks 13(3):40, 2025), latency
(arXiv:2505.12465), entropy-regularized certainty-equivalent
(arXiv:2605.24878), closing auctions (arXiv:2601.17247 — observes learned MMs
quoting asymmetrically to rebalance flow; emergent, not exploited as a
symmetry). Hybrid analytic+RL exists in three weak forms only: parameter
modulation (Falces Marín 2022), value initialization (Bergault et al.), and
analytic benchmark (arXiv:2509.12456; IEEE 2024 A2C/PPO+AS [venue details
unverified]).

### Oracle inequalities for adaptive pooling

Aggregation: Dalalyan & Tsybakov, COLT 2007 (LNCS 4539, 97–111);
Rigollet–Tsybakov exponential screening (arXiv:0911.2919); Leung & Barron 2006
[locator unverified]. Partial pooling: Efron & Morris, JASA 70(350), 311–319,
1975; James–Stein 1961 and Gelman et al. BDA [standard, unverified]; online
version: Cesa-Bianchi & Lugosi 2006 [standard, unverified]. Honest absence: no
oracle inequality over {hard pooling, perturbative pooling, per-regime
learning} in RL for market regimes.

## Bottom line

Every individual mechanism is known and now carries its canonical citation. The
four constructions with no found precedent: (1) the exact nonlinear normal-frame
critic/replay coordinates; (2) the precomputed response library over a win-curve
curvature basis; (3) sensitivity-penalized minimax-regret robustness over a
shared functional uncertainty, in market making; (4) the three-way pooling
oracle inequality. The composition — exact symmetry frame + tangent response
library + small residual with curvature-sensitivity robustness — appears nowhere
assembled. Mandatory differentiations when writing the paper: Bergault et al.
arXiv:1810.04383 (exact-model side) and Falces Marín et al. 2022 (hybrid side);
mandatory corrections: Wiesemann–Kuhn–Rustem (not Sim), Todorov NIPS 2006 (not
2007).
