# Literature Map — Instability Theory (the oscillator of §5)

This map traces the lineage of the central dynamical claim in `notes/spread_as_endogenous_carry.tex` §5 ("The oscillator"): that a low-carry storable-goods market behaves as an oscillator with **amplitude-dependent damping** — Van der Pol type — with *negative* damping at small amplitude (extrapolative expectations plus near-zero effective carry) and *positive* damping at large amplitude (volatility-driven risk charge in the quoted spread, plus the imbalance multiplier). The generic attractor is a **limit cycle**, and the operating point is **self-organized marginal stability**: "the spread is the thermostat."

Every load-bearing piece of that sentence has an ancestor. The strands below identify each one, give the exact citation, state what it establishes, and say how it relates: **supports** (compatible evidence or mechanism), **anticipates** (contains a version of the idea), or **differs** (same words, different mechanism — and where). Verification notes flag anything not confirmed against a bibliographic source this pass. Citations below were checked against Crossref except where marked.

Companion maps: `map_theory.md` (storage theory proper), `map_control.md`, `map_markets.md`. Weymar's cocoa cycle and the competitive-storage stationarity theorems live there; this map covers only the oscillator/instability machinery.

---

## 1. Limit cycles in economics — the macro lineage

The nonlinear endogenous-cycle tradition is where "amplitude-dependent damping" enters economics. The mechanism was imported *explicitly* from Van der Pol's relaxation oscillations, twice, in the very first volumes of Econometrica — so "Van der Pol economics" is not a metaphor the note invents; it is a 1933 research program the note re-aims at a different nonlinearity.

**Le Corbeiller, Ph. (1933). "Les systèmes autoentretenus et les oscillations de relaxation." *Econometrica* 1(3): 328–332.** [verified: Crossref]
The physicist Philippe Le Corbeiller — Van der Pol's expositor, later Goodwin's teacher at Harvard — writes in Econometrica vol. 1 urging economists to model persistent cycles as *self-sustained (relaxation) oscillations* of nonlinear systems rather than damped linear systems kept alive by shocks. This is the founding document of Van der Pol economics. **Anticipates**: the program statement ("cycles are limit cycles of a nonlinear dissipative system") is exactly the note's, sixty pages of storage theory earlier. **Differs**: no economic mechanism at all — it is an invitation, not a model.

**Hamburger, L. (1934). "Note on Economic Cycles and Relaxation-Oscillations." *Econometrica* 2(1): 112.** [verified: Crossref]
Companion note (Hamburger had been pushing the analogy since ~1930 in Dutch): business cycles as Van der Pol relaxation oscillations. **Anticipates** likewise; likewise mechanism-free.

**Kaldor, N. (1940). "A Model of the Trade Cycle." *Economic Journal* 50(197): 78–92.** [verified previous pass]
Sigmoid (S-shaped) investment and savings functions of activity: near the equilibrium the marginal propensities make it locally *unstable*; far away the flattening of I(Y) bounds the motion. First economic model with the Van der Pol *shape* — local instability + large-amplitude saturation — argued graphically. **Anticipates** the note's damping-sign structure precisely, at the level of geometry. **Differs**: nonlinearity lives in the investment function; no storage, no prices of immediacy; and Kaldor asserts rather than proves the cycle (see Chang–Smyth).

**Chang, W.W. & Smyth, D.J. (1971). "The Existence and Persistence of Cycles in a Non-linear Model: Kaldor's 1940 Model Re-examined." *Review of Economic Studies* 38(1): 37–44.** [verified: Crossref]
Proves Kaldor's cycle is a limit cycle via Poincaré–Bendixson: local instability of the stationary point + a trapping region ⇒ closed orbit. **Supports**: this is the exact theorem-shape the note's Conjecture (stability boundary + bounded endogenous damping ⇒ limit cycle) would need; cite it as the precedent for how such claims get proved in economics.

**Goodwin, R.M. (1951). "The Nonlinear Accelerator and the Persistence of Business Cycles." *Econometrica* 19(1): 1–17.** [verified previous pass; Rayleigh reading is the standard one — see verification note]
The canonical execution of Le Corbeiller's program. Investment is a bounded nonlinear function of the *rate of change* of output (capacity floor and ceiling on the accelerator); the resulting second-order ODE has its nonlinearity in the velocity term — i.e., it is of **Rayleigh type**, the integral twin of the Van der Pol equation (differentiate Rayleigh and you get VdP). Goodwin explicitly presents the solution as a *relaxation oscillation* — a self-sustained limit cycle independent of initial conditions, approached from inside and outside — and credits Le Corbeiller for the apparatus. How explicit is the VdP identification? Explicit in structure and in the relaxation-oscillation language and phase-plane treatment; the equation is presented in piecewise-linear form rather than with the cubic, and Goodwin says "Rayleigh/relaxation" rather than writing "Van der Pol equation" in the text. (Verification note: the Rayleigh-type reading is standard in the history-of-thought literature on Goodwin, e.g. Velupillai's essays; not re-checked against the 1951 text this pass — WebSearch budget was exhausted.) **Anticipates**: this is the closest *formal* ancestor of Eq. (vdp) in the note — negative damping near equilibrium, saturation at amplitude, limit cycle. **Differs**: the amplitude-dependence sits in the accelerator's capacity bounds (a technological constraint), not in an endogenously priced cost of carrying inventory; nothing in Goodwin corresponds to the damping coefficient *itself* being a market-quoted price.

**Hicks, J.R. (1950). *A Contribution to the Theory of the Trade Cycle*. Oxford: Clarendon Press.** [standard; not re-verified]
Linear unstable accelerator–multiplier kept bounded by an exogenous *ceiling* (full employment) and *floor* (gross investment ≥ 0). **Differs instructively**: bounded instability via hard constraints rather than smooth amplitude-dependent damping — the piecewise-linear cousin of the same idea. The note's 2022 exchange-suspension remark ("the market improvised infinite width") is a Hicksian ceiling supplied by the dealer layer; worth a sentence when citing.

**Goodwin, R.M. (1967). "A Growth Cycle." In C.H. Feinstein (ed.), *Socialism, Capitalism and Economic Growth: Essays Presented to Maurice Dobb*, 54–58. Cambridge University Press.** [standard; not re-verified]
Employment–wage-share predator–prey cycle (Lotka–Volterra). **Differs in a way worth being precise about**: the 1967 model is *conservative* — a continuum of closed orbits, no attractor, structurally unstable — i.e., exactly what the note's mechanism is *not*. Citing Goodwin 1967 as a limit-cycle precedent is a common error; the limit-cycle Goodwin is 1951.

**Torre, V. (1977). "Existence of Limit Cycles and Control in Complete Keynesian System by Theory of Bifurcations." *Econometrica* 45(6): 1457–1466.** [verified: Crossref]
First explicit Hopf-bifurcation existence proof of limit cycles in a Keynesian IS-LM-type system. **Supports** (toolkit precedent — see Strand 6).

**Chiarella, C. & Flaschel, P. (2000). *The Dynamics of Keynesian Monetary Growth: Macro Foundations*. Cambridge University Press.** [standard; not re-verified]
The systematic modern program of nonlinear macrodynamics: high-dimensional disequilibrium models where locally destabilizing feedbacks (Mundell, Rose, accelerator) are bounded by outer nonlinearities, generating persistent cycles; explicitly in the Kaldor–Goodwin tradition and explicit about "local instability + global boundedness" as the organizing principle. **Supports/anticipates** the design pattern; **differs** in domain (macro aggregates) and in the boundedness devices (behavioral switching, fiscal/monetary feedback) — none is a quoted spread.

*Explicit "Van der Pol economics" beyond the above:* the tradition is surveyed in **Lorenz, H.-W. (1993). *Nonlinear Dynamical Economics and Chaotic Motion*, 2nd ed. Springer** [standard; not re-verified], which treats Van der Pol/Rayleigh business-cycle equations, averaging, and Hopf applications in one place — the efficient citation if the note wants a single pointer to the genre.

---

## 2. Commodity cycles as oscillators — the directly-on-point strand

**Ezekiel, M. (1938). "The Cobweb Theorem." *Quarterly Journal of Economics* 52(2): 255–280.** [standard; not re-verified]
Codifies the cobweb: production lag + naive expectations ⇒ discrete oscillation in a single commodity market; convergence/divergence governed by the supply/demand slope ratio. **Anticipates** the note's spring (production/consumption response to the price gap) — but the cobweb oscillation is a *linear* mechanism with knife-edge stability, exactly the pathology (converge or explode, nothing in between) that both Larson and the note are built to escape.

**Larson, A.B. (1964). "The Hog Cycle as Harmonic Motion." *Journal of Farm Economics* 46(2): 375–386.** [VERIFIED: Crossref — title, journal, volume, date, first page all confirmed. It is real.]
The directly-on-point ancestor, and it holds up. Larson rejects the cobweb (wrong period: cobweb gives a 2-production-period sawtooth, hogs cycle at ~4 years) and models the hog market in *continuous time*: a distributed production lag responding to price yields a second-order system whose observed behavior is **undamped harmonic motion** — a commodity market as a literal mechanical oscillator, in the farm-economics literature, in 1964. (Follow-up confirming the empirical program: Jelavich, M.S. (1973). "Distributed Lag Estimation of Harmonic Motion in the Hog Market." *AJAE* 55(2): 223–224. [verified: Crossref])
**Anticipates**: the note's Eq. (oscillator) *is* Larson's equation plus a damping term with structure. **Differs — and this is the sharpest single contrast in the whole map**: Larson's oscillator has (approximately) *zero* damping as an empirical finding he cannot explain — sustained harmonic motion sits on a measure-zero knife edge, and he must simply posit that the damping nets out. The note supplies the missing mechanism: amplitude-dependent damping with a sign change *makes the knife edge an attractor*. Read this way, Larson measured the limit cycle from inside and mistook marginal stability for a coincidence; the note's self-organization argument is exactly the explanation his paper lacks. This is the citation that most sharpens the note's residual novelty, and it should be cited prominently.

**Meadows, D.L. (1970). *Dynamics of Commodity Production Cycles*. Cambridge, MA: Wright-Allen Press.** [standard; not re-verified]
System-dynamics generic commodity model (hogs, cattle, broilers): production delays + stock-management decision rules ⇒ persistent oscillation; parameterized per commodity. **Supports**: delays + nonlinear decision rules generate the cycles, simulated honestly. **Differs**: simulation without reduction — no phase-plane object, no damping decomposition, no pricing of the stabilizer; the dealer/spread channel absent entirely.

**Sterman, J.D. (2000). *Business Dynamics: Systems Thinking and Modeling for a Complex World*. Boston: Irwin/McGraw-Hill (commodity-cycle chapter).** and **Sterman, J.D. (1989). "Modeling Managerial Behavior: Misperceptions of Feedback in a Dynamic Decision Making Experiment." *Management Science* 35(3): 321–339.** [standard; not re-verified]
Codifies Meadows' commodity oscillator and supplies the behavioral microfoundation: humans systematically under-account for supply-line delays, so locally destabilizing stock-adjustment behavior is robust in experiments. **Supports** the note's extrapolative/negative-damping ingredient with laboratory evidence. **Differs**: the stabilizer in Sterman's models is capacity/attrition nonlinearity, not an endogenous price of immediacy.

**Chiarella, C. (1988). "The Cobweb Model: Its Instability and the Onset of Chaos." *Economic Modelling* 5(4): 377–384.** [verified: Crossref]
Cobweb with adaptive expectations and nonlinear (S-shaped) supply: locally unstable steady state + globally bounding nonlinearity ⇒ limit cycle, then period-doubling to chaos. **Anticipates** the local-instability/global-boundedness pattern *within a commodity market*. **Differs**: expectational/supply nonlinearity in discrete time; no inventory state, no volatility feedback, no spread.

**Hommes, C.H. (1994). "Dynamics of the Cobweb Model with Adaptive Expectations and Nonlinear Supply and Demand." *Journal of Economic Behavior & Organization* 24(3): 315–335.** [verified: Crossref]
Systematic treatment of the chaotic cobweb: strange attractors and bounded aperiodic price fluctuations from deterministic dynamics with plausible (non-steep) demand/supply. **Supports** the general claim that commodity-market fluctuations can be endogenous attractors rather than shock responses. **Differs** as Chiarella 1988, and note the attractor type: the note claims a (noisy) limit cycle, not chaos — the empirical discipline (a characteristic period, à la Weymar's nine years and Larson's four) is what distinguishes them.

---

## 3. Stability is destabilizing — the sign of the small-amplitude damping

This strand formalizes "too quiet: volatility falls, effective carry falls, hoarding is free, instability returns" — the *negative-damping-at-small-amplitude* half of the note's Van der Pol structure. It is the best-developed of the seven strands and the one the note can lean on hardest for the qualitative mechanism.

**Minsky, H.P. (1977). "The Financial Instability Hypothesis: An Interpretation of Keynes and an Alternative to 'Standard' Theory." *Nebraska Journal of Economics and Business* 16(1): 5–16 (also *Challenge* 20(1): 20–27).**
**Minsky, H.P. (1986). *Stabilizing an Unstable Economy*. New Haven: Yale University Press.**
**Minsky, H.P. (1992). "The Financial Instability Hypothesis." Levy Economics Institute Working Paper No. 74.** [standard; not re-verified]
"Stability is destabilizing": tranquil periods rationally erode margins of safety (hedge → speculative → Ponzi finance), so the quiet state is self-undermining; instability is endogenous to capitalist finance. **Anticipates** the note's thermostat logic at the level of narrative — Minsky is precisely "negative damping at small amplitude," stated verbally in 1977. **Differs**: no formal model (Minsky famously resisted one); the margin that erodes is borrower/lender safety margins, not the risk term in a quoted spread; and Minsky's cycle needs institutional evolution, not just a state variable.

**Brunnermeier, M.K. & Sannikov, Y. (2014). "A Macroeconomic Model with a Financial Sector." *American Economic Review* 104(2): 379–421.** [verified: Crossref]
Continuous-time macro-finance with expert balance sheets; delivers the **volatility paradox**: lower *exogenous* risk induces higher equilibrium leverage, so *endogenous* risk and crisis probability do not fall (and can rise). The system's stochastic steady state sits persistently near the unstable region — quiet begets fragility, formally. **Anticipates**: this is the rigorous modern statement of the note's "low measured σ ⇒ cheap effective carry ⇒ instability returns," and the strongest existing formalization of self-organized fragility in economics. **Differs**: the state variable is expert net worth and the amplifier is the leverage constraint, not inventory coverage and a quoted spread; the attractor is a stochastic steady state with occasional crisis excursions, *not a deterministic limit cycle* — the note's claim of an orbit with a characteristic period is genuinely different and more falsifiable.

**Danielsson, J. & Shin, H.S. (2003). "Endogenous Risk." In *Modern Risk Management: A History*. London: Risk Books.** and **Danielsson, J., Shin, H.S. & Zigrand, J.-P. (2012). "Endogenous Extreme Events and the Dual Role of Prices." *Annual Review of Economics* 4: 111–129.** [2012 verified: Crossref]
Risk is generated by the system, not visited upon it: risk-sensitive constraints (VaR) make measured volatility feed back into positions, so prices play a dual role (allocation *and* imperative to act), producing endogenous volatility clustering and extreme events. The 2012 review states the feedback loop — low measured risk → larger positions → latent fragility → realized spike — as a closed loop. **Anticipates** the note's σ²-feedback channel directly. **Differs**: the loop closes through risk-*constraints* on leveraged intermediaries, not through the effective carry of physical inventory; no oscillator reduction, no amplitude equation.

**Geanakoplos, J. (2010). "The Leverage Cycle." *NBER Macroeconomics Annual* 24: 1–66.** [verified: Crossref]
Equilibrium determination of *margins* (not just rates): in quiet times leverage expands and asset prices rise; bad news + loss of optimist wealth + tightened margins crash them. A genuine endogenous **cycle in the price of balance-sheet space**. **Anticipates**: the note's ν(x) — the shadow price of the storage the physical world failed to supply — is the commodity-dealer analog of Geanakoplos' endogenous margin. **Differs**: heterogeneous-beliefs collateral equilibrium, discrete regimes, no continuous damping term, no spread.

**Adrian, T. & Shin, H.S. (2010). "Liquidity and Leverage." *Journal of Financial Intermediation* 19(3): 418–437.** [verified: Crossref]
Empirics: broker-dealer leverage is *procyclical* — balance sheets expand when measured risk falls (VaR per dollar of assets is roughly constant). **Supports**: direct evidence that intermediaries price balance-sheet space off recent volatility, which is exactly the behavior that makes the note's ψ ∝ γσ² damping coefficient state-dependent. **Differs**: securities dealers marking to market, not physical-inventory dealers quoting two-way prices.

---

## 4. Self-organized criticality in economics — the "parks itself at the edge" claim

**Bak, P., Chen, K., Scheinkman, J. & Woodford, M. (1993). "Aggregate Fluctuations from Independent Sectoral Shocks: Self-Organized Criticality in a Model of Production and Inventory Dynamics." *Ricerche Economiche* 47(1): 3–30.** [verified: Crossref; NBER WP version Dec 1992]
Imports Bak's sandpile into economics through — pleasingly for the note — an *inventory* model: (S,s) inventory rules on a production lattice make the economy self-organize to a critical state where independent micro shocks produce scale-free aggregate avalanches. **Anticipates** "the system parks itself at the edge" *and* does so via inventory dynamics. **Differs fundamentally in mechanism**: SOC here comes from threshold (non-convex ordering-cost) rules and local interaction — criticality without any price. The note's marginal stability is *price-mediated*: a quoted spread adjusts continuously and acts as a thermostat. SOC is an avalanche statistics claim (power laws, no characteristic scale); the note claims a limit cycle (a characteristic period). These are different, testably so.

**Scheinkman, J.A. & Woodford, M. (1994). "Self-Organized Criticality and Economic Fluctuations." *American Economic Review* 84(2), Papers & Proceedings: 417–421.** [standard citation; Crossref lookup did not surface it this pass — old AER P&P items often lack DOIs — page range from memory, worth a one-minute check before final submission]
The economist-facing summary of the above: why non-convexities + local interaction defeat the law of large numbers and put the economy at criticality. Same relation as the 1993 paper.

**Lux, T. & Marchesi, M. (1999). "Scaling and Criticality in a Stochastic Multi-Agent Model of a Financial Market." *Nature* 397: 498–500.** [verified: Crossref]
The substantive "edge of chaos" market result: chartist/fundamentalist switching makes the market hover around the point where the chartist fraction destabilizes it — deviations into the unstable region generate volatility that drives agents back. Self-organized *marginal stability* with on-off intermittency, volatility clustering, and fat tails as the signature. **Anticipates** the note's attractor description remarkably closely — "long near-random-walk drifts punctuated by spikes" is on-off intermittency around a marginally stable point. **Differs**: the thermostat is population flow between forecasting strategies, not a quoted spread; no storage, no carry; agent-based simulation rather than a reduced oscillator.

**Sornette, D. (2003). *Why Stock Markets Crash: Critical Events in Complex Financial Systems*. Princeton University Press** (with the Johansen–Sornette log-periodic power-law papers behind it). [standard; not re-verified]
Markets as self-organizing toward critical points, crashes as critical phenomena with log-periodic precursors. **Grade: skeptical, and the note should keep its distance.** The LPPL fitting methodology has known degeneracy problems (many free parameters, unstable fits, weak out-of-sample record; see the Feigenbaum and Brée–Joseph critiques), and the criticality framing is analogical — no mechanism *locates* the market at the critical point, which is precisely the thing the note claims to supply. Cite, if at all, as the maximalist version of the edge-of-criticality idea, distinguished from the note's mechanism-first, falsifiable version.

---

## 5. Volatility feedback in storage — the ψ ∝ σ² channel

**Deaton, A. & Laroque, G. (1992). "On the Behaviour of Commodity Prices." *Review of Economic Studies* 59(1): 1–23.** [verified: Crossref]
Rational-expectations competitive storage: the non-negativity constraint makes conditional volatility *endogenous and state-dependent* — high when stocks are low (near stockout), low when the market is well covered. **Supports**: σ² as a function of the coverage state is half of the note's amplitude-dependent damping (σ² small when quiet, large when disturbed). **Differs — the crucial half is missing**: in Deaton–Laroque volatility is an *output*; it never feeds back into the cost of holding. Storage decisions respond to expected price, not to σ², so the loop σ² → effective carry → inventory dynamics is open. (Also: with carry intact their process is stationary — the note deletes the carry term; see `map_theory.md`.)

**Routledge, B.R., Seppi, D.J. & Spatt, C.S. (2000). "Equilibrium Forward Curves for Commodities." *Journal of Finance* 55(3): 1297–1338.** [verified: Crossref]
Equilibrium term structure from storage: endogenous, state-dependent volatility and correlation of spot/forwards, conditional Samuelson effect, one-sided convenience yield. **Supports** the same half-loop with a full term structure; **differs** identically (risk-neutral agents; σ² has no price and no feedback).

**Pindyck, R.S. (2004). "Volatility and Commodity Price Dynamics." *Journal of Futures Markets* 24(11): 1029–1047.** [verified: Crossref]
The paper that *closes* the missing arc, empirically: for crude, heating oil, and gasoline, price volatility (options-implied and realized) *increases the marginal convenience yield* — i.e., σ² raises the market's price of holding inventory — and volatility shocks affect prices and inventories through this channel. In the note's language: measured volatility moves the effective carry. **Anticipates** the note's ψ ∝ γσ² term as an empirical regularity in real storage markets. **Differs**: a structural-empirical exercise, not a dynamical system — Pindyck estimates the arc but never assembles the loop (vol → carry → inventory → imbalance → vol) or asks about its stability; no dealer, no spread, no oscillator. The note's Eq. (vdp) is, in effect, the differential equation Pindyck's regressions are a cross-section of.

*(Also relevant but housed in `map_theory.md`: Pindyck (2001), "The Dynamics of Commodity Spot and Futures Markets: A Primer," Energy Journal 22(3), which lays out the inventory–vol–convenience-yield triangle informally; and Bobenrieth–Bobenrieth–Wright (2013) for explosive price paths inside rational storage.)*

**Bottom line for this strand:** every model has half the loop. State → σ² exists (Deaton–Laroque, RSS); σ² → holding cost exists (Pindyck, empirically). Nobody closes it into dynamics, prices it in a quoted spread, or notices that the closed loop is a Van der Pol damping term. That closure is the note's.

---

## 6. The math toolkit — averaging, describing functions, Hopf

**Kryloff, N. & Bogoliuboff, N. (1947). *Introduction to Non-Linear Mechanics* (transl. S. Lefschetz). Annals of Mathematics Studies 11, Princeton University Press** (Kiev original 1937). [standard; not re-verified]
The method of averaging: for weakly nonlinear oscillators, slow-flow equations for amplitude and phase; limit-cycle amplitude from the zero of the averaged damping. This is the tool that turns the note's "μ(amplitude) − β̃" into a quantitative amplitude prediction.

**Strogatz, S.H. (2015). *Nonlinear Dynamics and Chaos*, 2nd ed. Boulder: Westview Press, §7.5–7.6.** [standard]
The cleanest modern reference: two-timing/averaging worked on Van der Pol (limit-cycle amplitude = 2 in scaled units), relaxation limit, weakly nonlinear regime. Cite for the amplitude calculation.

**Guckenheimer, J. & Holmes, P. (1983). *Nonlinear Oscillations, Dynamical Systems, and Bifurcations of Vector Fields*. Applied Mathematical Sciences 42, Springer.** [standard]
The rigorous backstop: averaging theorem (ch. 4), Hopf bifurcation with first-Lyapunov-coefficient formula (ch. 3). Cite for the claim that the note's stability surface generically spawns the limit cycle via a Hopf.

**Gelb, A. & Vander Velde, W.E. (1968). *Multiple-Input Describing Functions and Nonlinear System Design*. New York: McGraw-Hill.** [standard]
The control-engineering version of the same computation: describing functions predict limit-cycle amplitude and frequency in nonlinear feedback loops. Included because it is the bridge to Strand 7 — the SOAS designers computed their deliberate limit cycle with exactly this tool, and the note's dealer-Bellman nonlinearity (cosh⁻¹ skew, saturating width) is describing-function-friendly.

**Hopf in economics — existing applications:** **Torre (1977)** (Strand 1, verified) is the first; **Benhabib, J. & Nishimura, K. (1979). "The Hopf Bifurcation and the Existence and Stability of Closed Orbits in Multisector Models of Optimal Economic Growth." *Journal of Economic Theory* 21(3): 421–444** [verified: Crossref] shows closed orbits inside *optimal* growth — establishing that limit cycles survive full intertemporal optimization, which preempts the objection that rational storage would arbitrage the note's cycle away. **Supports**; **differs** in domain. (The Kaldor–Kalecki delay literature, e.g. Wu & Wang 2010, NARWA 11:869–887, continues the genre; cite only if delay-driven cycles become relevant — the note's T is a lag, so it might.)

---

## 7. Self-oscillating adaptive control — the engineering twin

The 1960s aerospace concept is real, and the parallel is exact. A **self-oscillating adaptive system (SOAS)** deliberately maintains a small, controlled limit cycle at the stability boundary of the loop: the relay/high-gain element drives the loop to marginal stability, the measured amplitude of the resulting oscillation identifies the critical gain, and the controller continuously adjusts to hold the system *at* the boundary — the limit cycle is not a defect but the *sensing mechanism*. "The system tunes itself to the stability boundary" is, in control engineering, a design pattern with flight heritage.

**Boskovich, B. & Kaufmann, R.E. (1966). "Evolution of the Honeywell First-Generation Adaptive Autopilot and Its Applications to F-94, F-101, X-15, and X-20 Vehicles." *Journal of Aircraft* 3(4): 296–304.** [verified: Crossref; conference version AIAA Guidance and Control, 1965]
The canonical account from the designers of the Honeywell MH-96 self-adaptive flight control system flown on the X-15. This is the citation for the concept.

**Staff of the NASA Flight Research Center (1971). *Experience with the X-15 Adaptive Flight Control System*. NASA TN D-6208.** [standard; not re-verified]
The operational retrospective, including the failure mode: the MH-96's behavior figured in the loss of X-15-3 in 1967 — a system that lives at the stability boundary can be walked over it. **Relevance to the note**: the cautionary half of the analogy — self-organized marginal stability implies occasional excursions (the note's spikes and hoard collapses) are not anomalies but the operating regime's tail.

**Åström, K.J. & Wittenmark, B. (1995). *Adaptive Control*, 2nd ed. Reading, MA: Addison-Wesley (SOAS treatment).** [standard]
Textbook treatment of self-oscillating adaptive systems; also the relay auto-tuner (Åström–Hägglund), the same idea domesticated: induce a limit cycle, read off the critical point from its amplitude and period.

**Relation to the note**: **anticipates the structure, not the economics.** In SOAS an *engineer* installs the relay and the gain-adjustment law; in the note the market-maker's Bellman equation plays the relay and competition plays the gain adjuster — nobody designs it, which is exactly the "self-organized" in self-organized marginal stability. The note should cite SOAS as the proof-of-concept that "hold a limit cycle at the stability boundary and use its amplitude as the feedback signal" is a coherent, implementable control architecture — and then observe that a dealer market implements it spontaneously, with the spread as the measured oscillation.

---

## Lineage summary — what the note inherits from where

| Ingredient of §5 | Inherited from |
|---|---|
| Cycles as limit cycles of a nonlinear dissipative system | Le Corbeiller (1933), Hamburger (1934) — the program |
| Negative damping near equilibrium + saturation at amplitude ⇒ limit cycle | Kaldor (1940) geometry; Goodwin (1951) Rayleigh/VdP form; Chang–Smyth (1971) proof pattern |
| A commodity market as a literal harmonic oscillator (continuous time, production lag as the spring) | Larson (1964) — including, unexplained, the marginal-stability observation itself |
| Cycles from delays + boundedly rational stock management | Ezekiel (1938); Meadows (1970); Sterman (1989, 2000); Chiarella (1988); Hommes (1994) |
| Quiet erodes the stabilizer: negative damping at small amplitude | Minsky (1977/1986/1992) verbally; Brunnermeier–Sannikov (2014) volatility paradox, formally; Danielsson–Shin(–Zigrand); Adrian–Shin (2010) empirically |
| Endogenous price of balance-sheet/storage space | Geanakoplos (2010) margins; Brennan (1958) risk premium (see map_theory) |
| "Parks itself at the edge" via inventory rules / strategy switching | Bak–Chen–Scheinkman–Woodford (1993); Scheinkman–Woodford (1994); Lux–Marchesi (1999) |
| State-dependent σ² in storage; σ² raises the price of holding | Deaton–Laroque (1992) / Routledge–Seppi–Spatt (2000); Pindyck (2004) |
| Amplitude of the limit cycle by averaging / describing functions | Krylov–Bogoliubov (1937/47); Strogatz; Guckenheimer–Holmes; Gelb–Vander Velde (1968) |
| Limit cycles survive optimization; Hopf in economic systems | Torre (1977); Benhabib–Nishimura (1979) |
| Deliberately holding a limit cycle at the stability boundary as a *mechanism* | SOAS: Boskovich–Kaufmann (1966); NASA TN D-6208; Åström–Wittenmark |

## Residual novelty — the hard-nosed statement

Every *component* of §5 has a respectable ancestor; the note should say so plainly. What has no ancestor, on this search, is the **location and derivation of the amplitude-dependent damping**:

1. **The damping coefficient is derived, not assumed, and it is a quoted price.** In Kaldor/Goodwin the amplitude-dependence is a posited shape of the investment function; in Chiarella/Hommes a posited supply curve; in BCSW a posited (S,s) rule; in Lux–Marchesi a posited switching rate. In the note, ψ ∝ ν″ ∝ γσ² falls out of a market-making Bellman equation with a cost-of-carry term — the dashpot is the *bid-offer spread*, an observable that dealers publish twice a week. No prior work locates a macro-dynamic damping term in the quoted spread of an inventory-controlling dealer, nor derives its state-dependence (the cosh⁻¹/√carry skew shape, the kink fingerprint) from optimization.
2. **The imbalance multiplier as the large-amplitude saturation.** The specific parameter-free form M(p) doing the Hicksian-ceiling work is the note's own (inherited from the Cotton–Papanicolaou sealed-bid machinery, not from any cycle literature).
3. **The closed loop.** Deaton–Laroque have state → σ²; Pindyck has σ² → carrying cost; Brunnermeier–Sannikov have quiet → fragility. Nobody composes them into one ODE, identifies the composition as Van der Pol damping, and reads off the limit cycle. The synthesis is genuinely absent from the record, which is mildly surprising given that Larson (1964) had already exhibited the marginal-stability phenomenology and the tools (Krylov–Bogoliubov) predate him by thirty years.
4. **What is *not* novel and must be credited**: the VdP program (Le Corbeiller), the damping-sign geometry (Kaldor/Goodwin), quiet-is-destabilizing (Minsky, Brunnermeier–Sannikov), edge-parking (BCSW, Lux–Marchesi), vol-raises-carry (Pindyck), commodity-as-oscillator (Larson), and boundary-holding control (SOAS). The note's claim should be phrased as: *these seven known things are one thing, and the thing is visible in the bid-offer.*

Closest single antecedent overall: **Larson (1964)** for the object (a storable-commodity market executing near-undamped oscillation) and **Brunnermeier–Sannikov (2014)** for the mechanism (quiet endogenously regenerates instability). The note is what you get when Larson's oscillator is given Brunnermeier–Sannikov's damping and the damping is priced by Avellaneda–Stoikov dealers.

## What to cite — shortlist

1. **Larson (1964)**, J. Farm Econ. 46(2): 375–386 — the on-point ancestor; the note explains his knife-edge.
2. **Goodwin (1951)**, Econometrica 19(1): 1–17 — the VdP/Rayleigh limit cycle in economics; footnote Le Corbeiller (1933), Econometrica 1(3): 328–332.
3. **Kaldor (1940)**, EJ 50(197): 78–92, with **Chang–Smyth (1971)**, REStud 38(1): 37–44 — damping-sign geometry and the Poincaré–Bendixson proof pattern.
4. **Minsky (1992)**, Levy WP 74 (with 1986 book) — stability is destabilizing, verbal form.
5. **Brunnermeier–Sannikov (2014)**, AER 104(2): 379–421 — the volatility paradox; nearest formal mechanism.
6. **Pindyck (2004)**, J. Futures Markets 24(11): 1029–1047 — σ² raises the price of storage, empirically.
7. **Lux–Marchesi (1999)**, Nature 397: 498–500 — self-organized marginal stability in a market (cite with BCSW 1993, Ricerche Economiche 47: 3–30, for the inventory-SOC root).
8. **Boskovich–Kaufmann (1966)**, J. Aircraft 3(4): 296–304 — SOAS: limit cycle at the stability boundary as a working control architecture.
9. **Strogatz (2015)** §7.5–7.6 (or Guckenheimer–Holmes 1983) — averaging for the amplitude claim.

