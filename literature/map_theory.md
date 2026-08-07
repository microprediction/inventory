# Literature Map — Theory

This map organizes the theoretical literature around the project's central mechanical question: **what stabilizes inventory and price when the cost of carry is nearly zero?** Classical supply-of-storage theory and rational-expectations (RE) storage theory both rely on two stabilizers: the *non-negativity of stocks* below (the stockout constraint) and *positive carrying cost plus interest* above. For low-carry goods with carry ≈ 20 bps/yr, the upper stabilizer essentially vanishes, and the question becomes whether anything endogenous — risk-bearing capacity, dealer balance sheets, limits to arbitrage — replaces it, or whether optimal inventory is explosive in general equilibrium. The strands below are ordered accordingly: (1)–(2) supply the two stabilizers and the equilibrium machinery; (3)–(4) supply the reduced-form and cross-sectionally-constrained (HJM-style) representations that the project wants to extend to a joint system of inventory, price, volatility, and bid-offer width; (5) supplies the empirical shape constraints any such model must reproduce; (6) supplies the instability and cycle mechanisms (including Weymar's endogenous ~9-year cocoa cycle and the capital-constraint upper stabilizer); (7) supplies episodes where the stabilizers visibly failed; (8) collects directly-on-point adjacent work found in the search (latent-inventory filtering, byproduct metals, dealer inventory control, mean-field-game storage).

A citation-correction note up front: the sometimes-cited "Weymar (1966), *The Dynamics of Commodity Futures Prices*, JPE" **does not exist**. Weymar's journal publication is a 1966 *American Economic Review* note, "The Supply of Storage Revisited"; the thesis (MIT, 1965) and the book (MIT Press, 1968) carry the full model. Details in Strand 1.

---

## 1. Classical supply-of-storage theory

**Keynes, J.M. (1930). *A Treatise on Money*, Vol. II: *The Applied Theory of Money*. London: Macmillan (esp. ch. 29).**
Introduces "normal backwardation": hedgers pay speculators an insurance premium, so futures prices sit below expected spot prices even in balanced markets; also discusses the large price falls needed to induce holding of "redundant" stocks. Relevance: the risk-premium channel is the germ of the project's *upper* stabilizer — someone must be paid to hold inventory, and the price of that risk-bearing, not physical carry, is what bounds stocks when warehousing costs ~20 bps.

**Working, H. (1933). "Price Relations between July and September Wheat Futures at Chicago since 1885." *Wheat Studies of the Food Research Institute* 9(6).**
First systematic documentation that intertemporal price spreads are a *function of stocks*: spreads near full carry when stocks are ample, inverted when stocks are scarce. Relevance: establishes the spread-vs-inventory curve that the project must re-derive for markets that have *no* futures spread — only a dealer bid-offer and an assessment price.

**Working, H. (1948). "Theory of the Inverse Carrying Charge in Futures Markets." *Journal of Farm Economics* 30(1): 1–28.**
**Working, H. (1949). "The Theory of Price of Storage." *American Economic Review* 39(6): 1254–1262.**
Formalizes the "supply of storage" curve: the market pays (or charges) for storage as a continuous function of aggregate stocks; inverse carrying charges are rational because stocks yield a stream of services (later named convenience yield). Storage occurs even at negative apparent return. Relevance: the supply-of-storage curve is the *static* cross-section the project dynamizes; note that for low-carry goods the cost leg of Working's curve is nearly flat, so the entire curve is convenience yield — one-signed, which is precisely the destabilizing configuration.

**Kaldor, N. (1939). "Speculation and Economic Stability." *Review of Economic Studies* 7(1): 1–27.**
Introduces convenience yield explicitly and analyzes when speculation stabilizes versus destabilizes: speculation stabilizes only if speculators' price expectations are less than unit-elastic in current price; extrapolative expectations destabilize. Relevance: gives the project its cleanest classical statement of the destabilization condition — Weymar's extrapolative long-run anchor is exactly a Kaldor elasticity-greater-than-one configuration, and near-zero carry removes the friction that otherwise damps it.

**Brennan, M.J. (1958). "The Supply of Storage." *American Economic Review* 48(1): 50–72.**
Estimates the supply-of-storage curve for several commodities, decomposing marginal storage cost into physical outlay, a *risk premium increasing in stocks*, and convenience yield decreasing in stocks. Relevance: Brennan's risk-aversion term is the first formal appearance of the project's conjectured endogenous upper stabilizer — when physical carry ≈ 0, his stock-increasing marginal risk premium is the only thing that makes the supply-of-storage curve slope up.

**Telser, L.G. (1958). "Futures Trading and the Storage of Cotton and Wheat." *Journal of Political Economy* 66(3): 233–255.**
Estimates supply-of-storage relations and finds no evidence of a Keynesian risk premium in futures returns — speculators appear to earn nothing on average. Relevance: if Telser is right and risk-bearing is supplied elastically at zero price, then for a zero-carry commodity *neither* upper stabilizer (cost or risk premium) operates, sharpening the project's explosive-inventory concern.

**Cootner, P.H. (1960). "Returns to Speculators: Telser versus Keynes." *Journal of Political Economy* 68(4): 396–404 (with "Rejoinder," same issue, 415–418).**
**Cootner, P.H. (1961). "Common Elements in Futures Markets for Commodities and Bonds." *American Economic Review (Papers & Proceedings)* 51(2): 173–183.**
Re-examines Telser's data and defends a state-dependent normal backwardation: the risk premium flips sign with net hedging pressure (backwardation when hedgers are net short, contango when net long); the 1961 paper unifies commodity futures with the bond term structure. Relevance: the sign-flipping premium is a primitive of the project's dealer-centric view (premium = price of warehousing net imbalance), and Cootner 1961 is the earliest explicit commodity–term-structure analogy, a direct ancestor of the project's HJM conjecture. (Cootner later co-founded Commodities Corporation with Weymar — the two strands share a personal history.)

**Weymar, F.H. (1965). *The Dynamics of the World Cocoa Market*. PhD thesis, MIT, Department of Economics.**
**Weymar, F.H. (1966). "The Supply of Storage Revisited." *American Economic Review* 56(5): 1226–1234.**
**Weymar, F.H. (1968). *The Dynamics of the World Cocoa Market*. Cambridge, MA: MIT Press (MIT Monographs in Economics 9, ix + 253 pp.).**
The project's founding document. Weymar extends the supply of storage from a static stock–spread relation to a *dynamic* one: the spot price is a functional of the *expected future coverage (inventory/consumption) trajectory*, discounted convenience yields integrate along the expected path, and the long-run price anchor is formed extrapolatively from past prices. Combined with production lags (cocoa tree maturation), this generates an endogenous price cycle of roughly nine years, which he documents in cocoa. The 1966 AER note is the journal-length statement of the path-integral supply-of-storage argument. Verification note: the book exists exactly as titled (MIT Press 1968, ISBN 0262230283); *no* 1966 JPE article "The Dynamics of Commodity Futures Prices" exists — cite the AER note instead. Relevance: supplies the project's core state variable (expected coverage path), its expectation formation (extrapolative anchor → Kaldor-unstable), and its empirical target (endogenous multi-year cycle); the project's task is to restate this in modern stochastic-control language and ask what happens as carry → 0.

**Gilbert, C.L. (2016). "The Dynamics of the World Cocoa Price." In M.P. Squicciarini and J. Swinnen (eds.), *The Economics of Chocolate*. Oxford University Press.**
Modern re-examination of the cocoa market explicitly in dialogue with Weymar; documents the long cycle's persistence and the role of stock estimates. Relevance: the only substantive modern engagement with Weymar's framework — evidence the framework was abandoned rather than refuted, which is part of the project's motivation.

---

## 2. Rational-expectations competitive storage

**Gustafson, R.L. (1958). *Carryover Levels for Grains: A Method for Determining Amounts That Are Optimal under Specified Conditions*. USDA Technical Bulletin 1178. Washington, DC.**
First stochastic dynamic-programming solution of optimal storage: characterizes the optimal carryover rule as the fixed point of a functional equation, with the non-negativity constraint on stocks binding in bad states. Relevance: supplies the **non-negativity constraint that is the only lower stabilizer when carrying cost ≈ 0** — everything in the project's "floor" behavior (stockouts, price spikes, kinked price function) descends from Gustafson's Kuhn–Tucker condition.

**Samuelson, P.A. (1957). "Intertemporal Price Equilibrium: A Prologue to the Theory of Speculation." *Weltwirtschaftliches Archiv* 79: 181–221.**
**Samuelson, P.A. (1971). "Stochastic Speculative Price." *Proceedings of the National Academy of Sciences* 68(2): 335–337.**
1957: deterministic intertemporal arbitrage pins spot-price paths to grow at interest-plus-carry between stockouts — the "sawtooth" skeleton. 1971: shows the stochastic storage problem's Bellman equation makes price a supermartingale bounded by the arbitrage band. Relevance: Samuelson's rate-of-interest-plus-carry drift restriction *is* the commodity analog of the HJM drift condition; with carry ≈ 0 the restricted drift is nearly zero, so nearly-flat expected price paths coexist with arbitrarily large inventories — the precise sense in which explosive stocks become "cheap" to sustain.

**Muth, J.F. (1961). "Rational Expectations and the Theory of Price Movements." *Econometrica* 29(3): 315–335.**
Introduces rational expectations, motivated explicitly by commodity markets with inventories and speculation; shows RE kills the naive cobweb. Relevance: Muth is the hinge between Strand 6 (extrapolative cycles) and Strand 2 (RE storage); the project's Weymar-style anchor deliberately steps back across this hinge, so Muth defines exactly what assumption is being relaxed and why (Deaton–Laroque show RE storage fails on persistence — see below).

**Scheinkman, J.A., and Schechtman, J. (1983). "A Simple Competitive Model with Production and Storage." *Review of Economic Studies* 50(3): 427–441.**
Rigorous RE equilibrium with production and storage: existence, uniqueness, and a stationary distribution for i.i.d. shocks; establishes that storage raises the autocorrelation of prices but cannot by itself produce very long memory; clarifies the role of the interest rate in bounding stocks. Relevance: the paper's boundedness arguments lean on discounting and storage cost — reading their proofs with carry → 0 and byproduct (price-inelastic) supply identifies precisely which stationarity conditions the low-carry-goods setting violates.

**Wright, B.D., and Williams, J.C. (1982). "The Economic Role of Commodity Storage." *Economic Journal* 92(367): 596–614.**
**Williams, J.C., and Wright, B.D. (1991). *Storage and Commodity Markets*. Cambridge: Cambridge University Press.**
The 1982 paper and 1991 book are the canonical numerical treatment of competitive storage: the kinked equilibrium price function, welfare effects, the interaction of storage with supply elasticity, and (in the book) squeezes, floors, and public stockpiles. Relevance: the book's comparative statics in storage cost and supply elasticity are the project's baseline — low-carry goods sit at the corner (cost ≈ 0, supply elasticity ≈ 0 because byproduct) where their numerical solutions become extreme and, in the limit, potentially non-stationary.

**Deaton, A., and Laroque, G. (1992). "On the Behaviour of Commodity Prices." *Review of Economic Studies* 59(1): 1–23.**
**Deaton, A., and Laroque, G. (1995). "Estimating a Nonlinear Rational Expectations Commodity Price Model with Unobservable State Variables." *Journal of Applied Econometrics* 10(S): S9–S40.**
**Deaton, A., and Laroque, G. (1996). "Competitive Storage and Commodity Price Dynamics." *Journal of Political Economy* 104(5): 896–923.**
The central empirical confrontation: the stockout non-negativity constraint generates the observed skewness and spikes of commodity prices, but the estimated model — even with unobserved inventory treated as a latent state (1995) — **cannot match the high autocorrelation of observed prices** with plausible interest and storage costs; storage transmits far less persistence than the data show (1996). Relevance: twofold. First, the 1995 paper is the founding treatment of *inventory as an unobservable filtered state*, exactly the low-carry situation. Second, the persistence failure is the strongest modern argument for Weymar's alternative: an extrapolative long-run anchor (or slow-moving capital) supplies the missing persistence that RE storage cannot.

**Routledge, B.R., Seppi, D.J., and Spatt, C.S. (2000). "Equilibrium Forward Curves for Commodities." *Journal of Finance* 55(3): 1297–1338.**
Embeds the storage model in a forward-curve setting: the non-negativity constraint gives the spot commodity an embedded timing option absent from forwards, generating endogenous, inventory-dependent term structures of volatility and conditional violations of the Samuelson effect. Relevance: the closest existing bridge between Strand 2 and Strand 4 — it shows how the *whole forward curve and its volatility surface* are functionals of the inventory state, which is the equilibrium half of the project's HJM-consistency question; the project asks the converse (which reduced-form joint dynamics of curve, vol, and width are consistent with *some* storage equilibrium).

**Bobenrieth, E.S.A., Bobenrieth, J.R.A., and Wright, B.D. (2013). "Bubble Troubles? Rational Storage, Mean Reversion, and Runs in Commodity Prices." NBER Working Paper 19037; published in J.-P. Chavas, D. Hummels, and B.D. Wright (eds.), *The Economics of Food Price Volatility*, University of Chicago Press, 2014.**
In a storage model where price expectations are *unbounded*, prices always equal marginal consumption value — so formal bubbles cannot occur — yet the model generates sustained explosive-looking price runs. Relevance: the nearest existing treatment of the project's "explosive inventory" suspicion; it shows explosive *price* paths are consistent with competitive storage, but leaves open the project's sharper question of whether optimal *inventory* itself diverges in general equilibrium when carry ≈ 0 and supply is byproduct-inelastic.

---

## 3. Reduced-form convenience-yield models

**Gibson, R., and Schwartz, E.S. (1990). "Stochastic Convenience Yield and the Pricing of Oil Contingent Claims." *Journal of Finance* 45(3): 959–976.**
Two-factor model: spot price (GBM) plus mean-reverting Ornstein–Uhlenbeck convenience yield, correlated; prices the futures curve and oil contingent claims. Relevance: the template the project generalizes — its OU convenience yield is a reduced-form stand-in for inventory, and the project's contribution is to make the latent factor an *actual* inventory/coverage state with its own non-negativity and capital constraints.

**Schwartz, E.S. (1997). "The Stochastic Behavior of Commodity Prices: Implications for Valuation and Hedging." *Journal of Finance* 52(3): 923–973.**
Compares one-, two-, and three-factor models on copper, oil, and gold, estimated by Kalman filter with futures prices as noisy observations of latent factors; strong mean reversion in copper and oil, nearly none in gold. Relevance: methodological anchor for latent-state estimation from prices, and an empirical warning — for gold (the extant metal closest to 'pure store of value,' i.e., low carry relative to price), mean reversion largely disappears, consistent with the project's conjecture that low-carry metals lose their stabilizer.

**Schwartz, E.S., and Smith, J.E. (2000). "Short-Term Variations and Long-Term Dynamics in Commodity Prices." *Management Science* 46(7): 893–911.**
Short-term mean-reverting deviations plus a long-term random-walk equilibrium level; shown equivalent to the Gibson–Schwartz model under reparameterization. Relevance: its two-component decomposition (transient scarcity vs drifting anchor) is a linear-Gaussian shadow of Weymar's structure (coverage deviations vs extrapolative long-run anchor); the project replaces the exogenous random-walk anchor with an endogenous, expectation-driven one and asks when the system loses stability.

**Casassus, J., and Collin-Dufresne, P. (2005). "Stochastic Convenience Yield Implied from Commodity Futures and Interest Rates." *Journal of Finance* 60(5): 2283–2331.**
Maximal affine three-factor model in which convenience yield is allowed to depend on spot price and interest rates; finds this level-dependence is essential for oil and copper (consistent with the theory of storage) but not for gold and silver. Relevance: directly documents that for the store-of-value goods in their panel, convenience yield decouples from the price level — i.e., the supply-of-storage feedback loop that stabilizes industrial commodities is empirically absent where carry is small relative to value, exactly the regime of the project's low-carry goods.

---

## 4. HJM-style modeling and consistency

**Heath, D., Jarrow, R., and Morton, A. (1992). "Bond Pricing and the Term Structure of Interest Rates: A New Methodology for Contingent Claims Valuation." *Econometrica* 60(1): 77–105.**
Models the entire forward curve as the state; no-arbitrage forces the drift of every forward rate to be a specific functional of the volatility structure. Relevance: the structural analogy the project pursues — the drift restriction is the paradigm for how "inventory, price, volatility, and width cannot move independently"; the project seeks the analogous restriction where the curve is the *expected coverage trajectory* and the volatility inputs include bid-offer width.

**Cortazar, G., and Schwartz, E.S. (1994). "The Valuation of Commodity Contingent Claims." *Journal of Derivatives* 1(4): 27–39.**
Early application of curve-as-state (HJM-style, factor-analytic) modeling directly to the copper futures curve. Relevance: proof of concept that metals forward curves admit low-dimensional HJM treatment; the project extends the state to include inventory and quote width for metals with *no* curve.

**Miltersen, K.R., and Schwartz, E.S. (1998). "Pricing of Options on Commodity Futures with Stochastic Term Structures of Convenience Yields and Interest Rates." *Journal of Financial and Quantitative Analysis* 33(1): 33–59.**
Full HJM treatment for commodities: takes the initial term structures of both interest rates and *convenience yields* as given and derives Gaussian arbitrage-free dynamics with closed-form options. Relevance: shows the convenience-yield curve can be modeled HJM-style; since convenience yield is a monotone function of coverage, this is one substitution away from the project's target object — an HJM model *of the expected inventory path itself*.

**Miltersen, K.R. (2003). "Commodity Price Modelling That Matches Current Observables: A New Approach." *Quantitative Finance* 3(1): 51–58.**
Constructs commodity models calibrated to the observed forward curve and term structure of volatilities, HJM-fashion. Relevance: the calibration discipline the project needs when the 'observables' are dealer assessments and widths rather than exchange curves.

**Clewlow, L., and Strickland, C. (2000). *Energy Derivatives: Pricing and Risk Management*. London: Lacima Publications.**
Standard practitioner reference for multi-factor HJM-type forward-curve models of energy (single- and multi-factor forward-curve dynamics with time-damped volatility functions). Relevance: supplies the workhorse volatility parameterizations — exponentially damped factor loadings — that the project can test for *consistency* with a storage equilibrium rather than assume.

**Björk, T., and Christensen, B.J. (1999). "Interest Rate Dynamics and Consistent Forward Rate Curves." *Mathematical Finance* 9(4): 323–348.**
**Björk, T., and Svensson, L. (2001). "On the Existence of Finite-Dimensional Realizations for Nonlinear Forward Rate Models." *Mathematical Finance* 11(2): 205–243.**
**Filipović, D. (2001). *Consistency Problems for Heath–Jarrow–Morton Interest Rate Models*. Lecture Notes in Mathematics 1760, Springer.**
The consistency program: when is a parametric family of curves invariant under an arbitrage-free model (1999); when does an HJM model collapse to a finite-dimensional state (2001); systematic treatment (Filipović). Relevance: this is the exact mathematical technology for the project's conjecture that (inventory, price, vol, width) evolve on a low-dimensional invariant manifold — "supply of storage curve as invariant manifold" is a Björk–Christensen consistency statement, and finite-dimensional-realization theory says when a Weymar-style two-or-three-state model is *exactly*, not approximately, consistent with full curve dynamics.

**Musiela, M. (1993). "Stochastic PDEs and Term Structure Models." Working paper, Journées Internationales de Finance, IGR-AFFI, La Baule.**
Re-coordinatizes HJM in time-to-maturity, turning the forward curve into a solution of a stochastic PDE with a transport term. Relevance: the natural coordinates for a *coverage curve* x ↦ expected coverage at horizon x, whose transport term is physical consumption — the project's inventory dynamics live most naturally in Musiela parameterization.

**Trolle, A.B., and Schwartz, E.S. (2009). "Unspanned Stochastic Volatility and the Pricing of Commodity Derivatives." *Review of Financial Studies* 22(11): 4423–4461.**
HJM-type commodity model with volatility factors that are *not spanned* by the futures curve, strongly supported in NYMEX oil data. Relevance: direct evidence that commodity volatility carries state information beyond the curve — in the project's frame, the unspanned factor is a candidate shadow of latent inventory/coverage, and dealer width may span what futures do not.

**Carmona, R., and Ludkovski, M. (2004). "Spot Convenience Yield Models for the Energy Markets." In G. Yin and Q. Zhang (eds.), *Mathematics of Finance*, AMS Contemporary Mathematics 351: 65–80.**
Surveys convenience-yield models treating the yield as a *hidden state to be filtered* from futures prices; documents misspecification of the OU assumption and reports failure to find a model jointly consistent with spot and forward curve. Relevance: names the project's estimation problem (convenience yield/inventory as filtered hidden state) and its negative result — joint spot/curve inconsistency — is precisely the kind of failure a structurally-constrained (storage-equilibrium-consistent) family should repair.

---

## 5. Inventory–volatility–spread empirics

**Fama, E.F., and French, K.R. (1987). "Commodity Futures Prices: Some Evidence on Forecast Power, Premiums, and the Theory of Storage." *Journal of Business* 60(1): 55–73.**
**Fama, E.F., and French, K.R. (1988). "Business Cycles and the Behavior of Metals Prices." *Journal of Finance* 43(5): 1075–1093.**
1987: across 21 commodities, storage-theory variables (interest-adjusted basis) have more explanatory power than risk-premium variables. 1988: for *metals specifically*, uses the interest-adjusted basis as an inventory proxy and confirms theory-of-storage predictions — spot vol exceeds futures vol when inventories are low, and metals prices are more volatile around business-cycle peaks when inventories fall. Relevance: 1988 is the canonical metals-specific validation and supplies the identification trick (basis as inventory proxy) that fails for the project's low-carry goods — no basis exists — motivating width/skew as replacement proxies.

**Pindyck, R.S. (1994). "Inventories and the Short-Run Dynamics of Commodity Prices." *RAND Journal of Economics* 25(1): 141–159.**
**Pindyck, R.S. (2001). "The Dynamics of Commodity Spot and Futures Markets: A Primer." *Energy Journal* 22(3): 1–29.**
**Pindyck, R.S. (2004). "Volatility and Commodity Price Dynamics." *Journal of Futures Markets* 24(11): 1029–1047.**
Develops and estimates the structural "market for storage" (price of storage = convenience yield read off the futures spread) alongside the cash market; 2004 shows volatility itself *feeds back* into the storage market: higher vol raises the marginal convenience yield and hence inventories and spreads. Relevance: Pindyck's two-market diagram (cash market + storage market) is the cleanest pedagogical skeleton for the project's model, and the 2004 vol→convenience-yield feedback is one leg of the joint (inventory, vol, width) dynamics the project wants to close with a no-arbitrage restriction.

**Geman, H., and Nguyen, V.-N. (2005). "Soybean Inventory and Forward Curve Dynamics." *Management Science* 51(7): 1076–1091.**
Constructs an inventory ("scarcity" = reciprocal of inventory) time series and shows soybean price volatility is an increasing affine function of scarcity; embeds scarcity as a state variable in a three-factor forward-curve model. Relevance: the direct precedent for putting *measured inventory* inside a forward-curve model as a priced state — the project does the same with *filtered* (unobservable) inventory, and with width in place of the exchange curve.

**Gorton, G.B., Hayashi, F., and Rouwenhorst, K.G. (2013). "The Fundamentals of Commodity Futures Returns." *Review of Finance* 17(1): 35–105.**
31 commodities, 1971–2010, with physical inventory data: convenience yield is a decreasing, strongly *nonlinear* (hockey-stick) function of inventories; risk premia, basis, momentum, and volatility all organize around the inventory state; price-based signals work because they proxy inventories. Relevance: the definitive empirical shape constraints (nonlinearity, asymmetry near stockout) that any low-carry-goods model must inherit, and the demonstration that when inventories are unobserved, price-based statistics can stand in for them — the project extends the instrument set to dealer skew and width.

**Kogan, L., Livdan, D., and Yaron, A. (2009). "Oil Futures Prices in a Production Economy with Investment Constraints." *Journal of Finance* 64(3): 1345–1375.**
General-equilibrium production economy with irreversible, capacity-constrained investment: generates the documented **V-shaped** relation between futures volatility and the slope/basis of the term structure — vol is high at both very low and very high inventory/slope states. Relevance: shows supply-side constraints (not just storage) shape the vol–inventory relation; for byproduct goods, investment in *own* supply is essentially impossible at any price, putting the market permanently on one arm of the V — persistently convex vol response, a testable implication.

---

## 6. Cycles, system dynamics, and instability

**Ezekiel, M. (1938). "The Cobweb Theorem." *Quarterly Journal of Economics* 52(2): 255–280.**
Canonical statement of lagged-supply-response cycles: naive expectations plus a production lag give convergent, persistent, or explosive oscillations depending on relative supply/demand elasticities. Relevance: the ur-model of the project's endogenous cycle; Weymar's cocoa cycle is a cobweb *smoothed through an inventory buffer* — and the project's question is what happens when the buffer's cost discipline (carry) is removed.

**Coase, R.H., and Fowler, R.F. (1935). "Bacon Production and the Pig-Cycle in Great Britain." *Economica* 2(6): 142–167.**
**Harlow, A.A. (1960). "The Hog Cycle and the Cobweb Theorem." *Journal of Farm Economics* 42(4): 842–853.**
**Rosen, S., Murphy, K.M., and Scheinkman, J.A. (1994). "Cattle Cycles." *Journal of Political Economy* 102(3): 468–492.**
The livestock-cycle arc: Coase–Fowler show producers' expectations were *not* naive, undermining the simple cobweb; Harlow reconciles the hog cycle with a modified cobweb; Rosen–Murphy–Scheinkman show a fully *rational-expectations* model with biological gestation/holding lags still produces cattle cycles (the capital-good character of breeding stock does the work). Relevance: the crucial lesson that multi-year commodity cycles do **not** require irrational expectations if the stock is simultaneously an input and a hold-able asset — above-ground metal stocks have exactly this dual character, so the project's cycle can be given either a Weymar (extrapolative) or an RMS (rational, delay-driven) foundation, with different policy implications.

**Forrester, J.W. (1961). *Industrial Dynamics*. Cambridge, MA: MIT Press.**
Founds system dynamics: supply chains with stocks, delays, and behavioral ordering rules generate endogenous oscillation and amplification (bullwhip). Relevance: MIT ambient influence on Weymar's thesis (same institution, same years); provides the simulation-first methodology and the stock-and-delay canon for the project's disequilibrium benchmark against which the stochastic-control model is compared.

**Meadows, D.L. (1970). *Dynamics of Commodity Production Cycles*. Cambridge, MA: Wright-Allen Press.**
Builds a generic system-dynamics commodity model (explicit capacity, delays, inventory coverage, price formation) that reproduces hog, cattle, and chicken cycles with commodity-specific delay parameters; argues the cobweb theorem is an inadequate representation. Relevance: notably, Meadows' price-setting rule is driven by *inventory coverage* — the same state variable as Weymar — making this the system-dynamics twin of the project's control formulation; his finding that cycle period ≈ 2× total supply-chain delay gives a falsifiable prediction for low-carry-goods cycle lengths.

**Blanchard, O.J., and Watson, M.W. (1982). "Bubbles, Rational Expectations and Financial Markets." In P. Wachtel (ed.), *Crises in the Economic and Financial Structure*, Lexington Books, 295–315 (also NBER Working Paper 945).**
Rational bubbles: self-fulfilling explosive components consistent with rational expectations, growing at the discount rate, with periodic-collapse variants. Relevance: for an asset with carry ≈ 20 bps, the bubble growth rate needed to compensate holders is only r + carry ≈ tiny — low-carry goods are unusually cheap hosts for rational-bubble components, and the project's "explosive optimal inventory" is the *quantity-side image* of a Blanchard–Watson price bubble (cf. Bobenrieth–Bobenrieth–Wright in Strand 2, who show storage models mimic this without formal bubbles).

**Shleifer, A., and Vishny, R.W. (1997). "The Limits of Arbitrage." *Journal of Finance* 52(1): 35–55.**
Arbitrage is conducted by capital-constrained, agency-afflicted specialists; when mispricing widens, capital flees exactly when it is most needed, so arbitrage fails to discipline prices in extreme states. Relevance: supplies the project's conjectured **upper stabilizer**: with physical carry ≈ 0, the binding cost of holding (or shorting) minor-metal inventory is *risk capital*, and Shleifer–Vishny is the canonical model of why that stabilizer is finite, state-dependent, and prone to sudden withdrawal.

**Duffie, D. (2010). "Presidential Address: Asset Price Dynamics with Slow-Moving Capital." *Journal of Finance* 65(4): 1237–1267.**
Capital moves to investment opportunities with institutional delays, generating initial under-reaction, price overshoot, and slow reversion after supply/demand shocks. Relevance: gives the *time constant* of the upper stabilizer — the speed at which speculative capital arrives to absorb an inventory imbalance — which, interacting with production delays, sets the project's endogenous cycle period in place of Weymar's ad hoc extrapolation window.

**Acharya, V.V., Lochstoer, L.A., and Ramadorai, T. (2013). "Limits to Arbitrage and Hedging: Evidence from Commodity Markets." *Journal of Financial Economics* 109(2): 441–465.**
Ties limits-to-arbitrage directly to commodities: producers' hedging demand and speculators' constrained capital jointly determine futures risk premia, spot prices, and *inventories*; producer default risk raises hedging demand and inventories. Relevance: the existing model closest to the project's general-equilibrium concern — speculative capital enters the inventory equation — but it presumes a futures market; the project's no-futures low-carry goods concentrate all of this risk-bearing on dealer balance sheets.

---

## 7. Hoarding, squeeze, and stockpile episodes (theory testbeds)

**Anderson, R.W., and Gilbert, C.L. (1988). "Commodity Agreements and Commodity Markets: Lessons from Tin." *Economic Journal* 98(389): 1–15.**
Post-mortem of the October 1985 International Tin Council collapse: the buffer stock defended an unrealistic floor with insufficient finance, accumulated enormous stocks and (hidden) forward positions, and failed discontinuously. Relevance: a natural experiment in *state-held explosive inventory* under near-costless carry — the ITC is what the project's runaway-inventory equilibrium looks like when the "speculator" has a mandate instead of a risk limit, and the collapse dynamics test the model's stockpile-release regime.

**Williams, J.C. (1995). *Manipulation on Trial: Economic Analysis and the Hunt Silver Case*. Cambridge: Cambridge University Press (268 pp.).**
The definitive economic post-mortem of the 1979–80 Hunt silver episode (by an expert witness at trial): analyzes how concentrated long positions plus physical accumulation interact with storage arbitrage, delivery, and the definition of manipulation. Relevance: silver is the classic *low-carry-relative-to-value* metal; the episode calibrates how much price displacement a given inventory absorption produces when the supply-of-storage curve is nearly flat — the project's comparative static in its purest historical form. (Complementary theory: **Pirrong, S.C. (1993), "Manipulation of the Commodity Futures Market Delivery Process," *Journal of Business* 66(3): 335–369**, which models squeezes as exercises of market power over the marginal storage/delivery decision.)

**LME Nickel, March 2022.** Best available post-mortems: **Oliver Wyman (2023), *Independent Review of Events in the Nickel Market in March 2022*, commissioned by the LME (final report, January 2023)**; **Office of Financial Research Working Paper 24-09 (2024), "Central Clearing and Trade Cancellation: The Case of LME Nickel Contracts on March 8, 2022"**; plus early case studies of the Tsingshan short squeeze (e.g., CEIBS teaching case "Tsingshan: A Short Squeeze on the LME's Nickel Futures Market"). The squeeze was amplified by a self-reinforcing margin/buy-back loop against a short of order 150–200kt held largely OTC, roughly five times LME deliverable stocks. Relevance: demonstrates the project's *width* channel empirically — as visible inventory (LME stocks) shrank relative to positioning, effective market width exploded to the point of trade cancellation; a joint (inventory, price, vol, width) model should classify March 7–8, 2022 as an exit from the admissible manifold.

---

## 8. Directly adjacent work surfaced in the search (not in the original brief)

### 8a. Latent-inventory filtering and structural estimation from prices alone

**Cafiero, C., Bobenrieth H., E.S.A., Bobenrieth H., J.R.A., and Wright, B.D. (2011). "The Empirical Relevance of the Competitive Storage Model." *Journal of Econometrics* 162(1): 44–54.**
Shows Deaton–Laroque's negative persistence result was partly numerical: on a finer grid and with revised specifications, the storage model fits price persistence for several commodities far better than previously believed. Relevance: partially rehabilitates RE storage before the project abandons it — the honest baseline against which a Weymar-style anchor must demonstrate *additional* explanatory power.

**Kleppe, T.S., and Oglend, A. (2017). "Estimating the Competitive Storage Model: A Simulated Likelihood Approach." *Econometrics and Statistics* 4: 39–56.**
Particle-filter simulated maximum likelihood for the storage model when only price data are reliable and shocks are serially dependent; substantially improves on Deaton–Laroque's estimator. Relevance: state-of-the-art machinery for the project's central inference problem — filtering unobserved above-ground stocks of low-carry goods from price (and, in the project's extension, dealer-quote) data.

**Gouel, C., and Legrand, N. (2017). "Estimating the Competitive Storage Model with Trending Commodity Prices." *Journal of Applied Econometrics* 32(4): 744–763** (and the related state-space/particle-MCMC literature, e.g., **Oglend et al., "Estimating the Competitive Storage Model with Stochastic Trends in Commodity Prices," *Econometrics* 9(4): 40, 2021**).
Extend storage-model estimation to trending/stochastic-trend environments via MLE and particle MCMC with latent states. Relevance: low-carry goods often have strong technology-driven demand trends; these papers show how to keep the stockout nonlinearity identified in the presence of such trends.

### 8b. Prices as signals when inventory is unobserved

**Sockin, M., and Xiong, W. (2015). "Informational Frictions and Commodity Markets." *Journal of Finance* 70(5): 2063–2098.**
Noisy-rational-expectations model where producers learn about global demand from commodity prices; informational feedback means supply noise and futures-market noise distort real decisions, and standard price–inventory diagnostics can mislead. Relevance: formalizes the project's setting where *published deficit forecasts* rather than observed stocks drive behavior — with unobserved inventories, prices (and, in this project, dealer quotes) are the signal, and self-confirming demand booms become possible, another destabilizer stacked on cheap carry.

### 8c. Dealer inventory control (the Cotton–Papanicolaou lineage)

**Cotton, P., and Papanicolaou, A. (2017). "Trading Illiquid Goods: Market Making as an Optimal Control Problem." (Working papers/presentation; local copy: `literature/trading_illiquid.pdf`.)**
The project's second anchor: dealer market making in an illiquid good as stochastic control of inventory, with the quoted *skew equal to the slope* and the *width equal to the convexity* of the dealer's inventory indifference cost. Relevance: supplies the measurement equation for latent inventory — observed low-carry-goods dealer skew/width identify the first two derivatives of the value function, hence (through the model) the inventory state itself.

**Amihud, Y., and Mendelson, H. (1980). "Dealership Market: Market-Making with Inventory." *Journal of Financial Economics* 8(1): 31–53.**
**Ho, T., and Stoll, H.R. (1981). "Optimal Dealer Pricing under Transactions and Return Uncertainty." *Journal of Financial Economics* 9(1): 47–73.**
**Avellaneda, M., and Stoikov, S. (2008). "High-Frequency Trading in a Limit Order Book." *Quantitative Finance* 8(3): 217–224.**
**Guéant, O., Lehalle, C.-A., and Fernandez-Tapia, J. (2013). "Dealing with the Inventory Risk: A Solution to the Market Making Problem." *Mathematics and Financial Economics* 7(4): 477–507.**
The dealer-inventory-control canon: optimal bid/ask as functions of dealer inventory; skew monotone in inventory; width driven by volatility and risk aversion; closed forms under exponential utility. Relevance: these give the microstructure half of the project's joint system — in such a good, the "market" *is* a handful of such dealers, so aggregate above-ground stock dynamics are literally the summed controlled inventories of Ho–Stoll/Guéant-type agents, making the macro storage model and the micro market-making model the same object at different scales.

### 8d. Mean-field-game and control-theoretic storage

**Graber, P.J., and Mouzouni, C. (2020). "On Mean Field Games Models for Exhaustible Commodities Trade." *ESAIM: Control, Optimisation and Calculus of Variations* 26: 11 (arXiv:1807.10344).**
Existence/uniqueness for MFG models of a continuum of producers trading an exhaustible commodity with price formed by market clearing. Relevance: template for the project's general-equilibrium passage — replace exhaustible reserves with above-ground stocks and producers with dealer-storers to pose "is optimal aggregate inventory explosive?" as an MFG whose equilibrium may fail to exist as carry → 0.

**Alasseur, C., Ben Tahar, I., and Matoussi, A. (2020). "An Extended Mean Field Game for Storage in Smart Grids." *Journal of Optimization Theory and Applications* 184: 644–670.**
MFG of many small storage units with price as the coupling through the supply–demand balance; explicit solvable structure. Relevance: closest existing MFG to "everyone holds a warehouse"; its stability conditions on the price-coupling map are the natural place to look for the project's explosive-inventory threshold. (See also Gomes–Saúde-type MFG price-formation models and the Natixis thesis literature on MFG gas-storage valuation for numerical approaches.)

### 8e. Byproduct (joint-production) metal supply

**Nassar, N.T., Graedel, T.E., and Harper, E.M. (2015). "By-product Metals Are Technologically Essential but Have Problematic Supply." *Science Advances* 1(3): e1400180.**
Quantifies companionality across the periodic table: indium, gallium, germanium, and most PGM/rare-earth companions are recovered overwhelmingly as byproducts, so their supply responds to the *host* metal's economics, not their own price. Relevance: severs the supply-elasticity stabilizer in the storage model — for goods recovered as byproducts of a host value chain, the supply curve is near-vertical in own price, so *all* equilibration must run through demand and inventory, tightening the case for instability.

**Fizaine, F. (2013). "Byproduct Production of Minor Metals: Threat or Opportunity for the Development of Clean Technologies? The PV Sector as an Illustration." *Resources Policy* 38(3): 373–383.**
Analyzes the economics of byproduct minor-metal supply (price formation, weak own-price supply response, opacity) with photovoltaic metals as the case. Relevance: documents institutional features the model must respect — no futures market, assessment-based pricing, long-term contracts — i.e., the exact environment where dealer quotes replace the futures curve as the observable. (Empirical companions exist on main–byproduct price linkages, e.g., multiscale Granger-causality studies of main/byproduct metal pairs in *Resources Policy* (2021), finding weak and unstable transmission — consistent with byproduct prices being inventory-driven rather than cost-driven.)

---

## Gaps this project could fill

1. **The carry → 0 limit of storage theory is uncharacterized.** Every stationarity proof in Strand 2 (Gustafson; Scheinkman–Schechtman; Deaton–Laroque) leans on interest-plus-storage-cost to make holding stocks expensive; Bobenrieth–Bobenrieth–Wright get explosive *price runs* from unbounded expectations but keep positive carry. No paper derives the equilibrium (or proves its non-existence) when carry ≈ 20 bps, supply is own-price-inelastic (byproduct), and risk capital is the only holding cost. That triple limit is exactly the low-carry case, and the answer — a threshold in dealer risk-bearing capacity separating stationary from explosive inventory — would be new.

2. **No one uses dealer quotes as the measurement equation for latent inventory.** The filtering literature (Deaton–Laroque 1995; Kleppe–Oglend; Gouel–Legrand; Carmona–Ludkovski) filters unobserved stocks or convenience yield from *prices alone*, and Gorton–Hayashi–Rouwenhorst show price statistics proxy inventories. The Cotton–Papanicolaou identities (skew = slope, width = convexity of the inventory indifference cost) imply the dealer quote surface observes the *first two derivatives* of the value function — strictly more information than the price level. A filter for above-ground minor-metal stocks with (mid, skew, width) as observables has, as far as this search found, never been built.

3. **HJM consistency has never been imposed on the joint (coverage, price, vol, width) system.** HJM-for-commodities exists (Cortazar–Schwartz; Miltersen–Schwartz; Trolle–Schwartz), and the consistency/finite-dimensional-realization program exists for interest rates (Björk–Christensen; Björk–Svensson; Filipović). Nobody has treated Weymar's *expected coverage trajectory* as the curve, derived the analog of the HJM drift restriction from storage arbitrage (Samuelson's r + carry drift, degenerate as carry → 0), and asked which parametric families — including the supply-of-storage curve itself — are invariant manifolds. Routledge–Seppi–Spatt give the equilibrium direction; the reduced-form/consistency direction is open.

4. **No equilibrium model exists for storable commodities *without* futures markets.** Strand 3–4 models presuppose a traded curve; RE storage presupposes a competitive spot auction. Low-carry goods often trade through a handful of dealers against assessment prices. Aggregating Ho–Stoll/Guéant-type market makers into the market-level supply of storage — micro dealer control and macro storage equilibrium as the same object — has no precedent; the MFG storage literature (Alasseur et al.; Graber–Mouzouni) provides the machinery but has only been applied to electricity and exhaustible resources.

5. **Byproduct supply has never been put inside a storage model.** Nassar–Graedel–Harper and Fizaine establish the facts; Williams–Wright's comparative statics stop at low (not zero, not negative-comovement) supply elasticity. A storage model where supply is driven by the *host* metal's price — possibly co-varying perversely with the byproduct's own demand — is absent, and it is the natural home of the project's deficit-forecast-driven dynamics.

6. **Weymar's path-functional pricing was never formalized or stress-tested.** The spot price as a functional of the expected coverage trajectory with an extrapolative long-run anchor (1965/1968) predates and evades the RE revolution; Deaton–Laroque's persistence failure and Cafiero et al.'s partial rescue leave the expectations question genuinely open. Restating Weymar in modern stochastic-control terms, nesting both the RE anchor and the extrapolative anchor, and letting slow-moving capital (Duffie 2010) set the cycle period would connect three literatures that currently do not cite each other — and would predict where low-carry goods sit on the cycle-length spectrum relative to cocoa's ~9 years.

7. **Width is missing from the inventory–volatility empirics.** The V-shape (Kogan–Livdan–Yaron), scarcity-vol link (Geman–Nguyen), and nonlinear convenience yield (Gorton et al.) all stop at volatility; no paper documents or models the bid-offer width of a physical commodity as a function of inventory, despite the 2022 exchange-suspension episode showing width (to the point of market failure) is the binding variable in extremis. A joint no-arbitrage restriction tying width dynamics to convenience-yield convexity would be both new theory and immediately testable on LME and low-carry-goods assessment data.
