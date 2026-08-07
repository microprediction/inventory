# Literature Map: Control Theory Applied to Inventory and Pricing

**Strand:** the operations-research / management-science / stochastic-control line on inventory and pricing, as distinct from commodity-storage *economics* (Working–Gustafson–Deaton–Laroque, mapped elsewhere).

**Organizing logic.** This strand treats inventory as the *state* of a controlled dynamical system and ordering/pricing as the *control*. It runs from the 1950s dynamic-programming formulation of the inventory problem (Arrow–Harris–Marschak through Scarf), through the parallel servomechanism tradition (Simon, Vassian, HMMS, Forrester) in which inventory policy is a feedback loop with gains, lags, and stability properties, to the modern strands: joint pricing-and-inventory control, storage as a real option (the warehouse problem and its energy-market descendants), dealer inventory control in market making, mean field games where the price is an equilibrium output of a continuum of controllers, and the control-theoretic pathology literature (cheap control, turnpikes, oscillation) that becomes relevant precisely when holding costs go to zero — as they do for low-carry goods at ~20 bps/yr. The project's two anchors sit at the junction of these strands: Weymar's cocoa thesis was written inside Forrester's Industrial Dynamics group (strand 2 meets storage economics), and Cotton & Papanicolaou's "Trading Illiquid Goods" is a dealer stochastic-control model (strand 5) applied to a physical commodity (strand 4).

---

## 1. Classical stochastic inventory control

- **Arrow, K. J., Harris, T., and Marschak, J. (1951). "Optimal Inventory Policy." *Econometrica* 19(3), 250–272.**
  The founding paper of stochastic inventory theory: derives optimal ordering under deterministic and then stochastic demand, introducing the (s, S) two-bin structure into a formal expected-cost framework. Relevance: the ancestor of every "inventory as controlled state" model in this project; note that holding cost enters as the essential coercive term — the object that nearly vanishes for low-carry goods.

- **Dvoretzky, A., Kiefer, J., and Wolfowitz, J. (1952). "The Inventory Problem: I. Case of Known Distributions of Demand" and "II. Case of Unknown Distributions of Demand." *Econometrica* 20(2), 187–222 and 20(3), 450–466.**
  Gives the first rigorous functional-equation treatment of the dynamic inventory problem, including conditions for optimality of simple policies, and (Part II) the adaptive case where the demand distribution must be learned. Relevance: Part II is the earliest treatment of inventory control under an *unknown* demand law — directly analogous to controlling metal stocks when the deficit distribution is itself uncertain.

- **Bellman, R., Glicksberg, I., and Gross, O. (1955). "On the Optimal Inventory Equation." *Management Science* 2(1), 83–104.** (Also ch. 5 of Bellman, *Dynamic Programming*, Princeton University Press, 1957.)
  Systematizes the inventory problem as a family of dynamic-programming functional equations and establishes structure of solutions (convexity, one-period lookahead characterizations). Relevance: the canonical bridge from inventory practice to the Bellman equation formalism this project uses throughout.

- **Scarf, H. (1960). "The Optimality of (S, s) Policies in the Dynamic Inventory Problem." In K. J. Arrow, S. Karlin, and P. Suppes (eds.), *Mathematical Methods in the Social Sciences, 1959*, Stanford University Press, 196–202.**
  Proves optimality of (s, S) policies under fixed ordering costs by inventing K-convexity, the prototype of "shaped value function ⇒ simple policy" arguments. Relevance: the project's inventory-indifference-cost convexity (width = convexity in Cotton–Papanicolaou) is a direct descendant of this style of argument; K-convexity is what fixed transaction costs do to the value function.

- **Clark, A. J., and Scarf, H. (1960). "Optimal Policies for a Multi-Echelon Inventory Problem." *Management Science* 6(4), 475–490.**
  Shows a serial supply chain decomposes into single-stage problems via echelon stocks, making multi-tier inventory tractable. Relevance: metal supply chains (mine → refiner → fabricator → consumer stocks) are multi-echelon; echelon decomposition suggests how unobserved above-ground stocks at different tiers aggregate into one effective state variable.

- **Veinott, A. F., Jr. (1966). "On the Optimality of (s, S) Inventory Policies: New Conditions and a New Proof." *SIAM Journal on Applied Mathematics* 14(5), 1067–1083.** (See also his survey: "The Status of Mathematical Inventory Theory," *Management Science* 12(11), 745–777, 1966.)
  Weakens Scarf's convexity hypotheses (quasiconvexity plus regularity of cost minima over time) and re-proves (s, S) optimality; the survey consolidates the first fifteen years of the field. Relevance: shows how robust threshold-policy structure is to the shape of the holding/shortage cost — useful when arguing that near-zero carrying cost, not cost shape, is what breaks the standard theory.

- **Porteus, E. L. (2002). *Foundations of Stochastic Inventory Theory*. Stanford University Press.**
  Graduate-level consolidation of the DP theory of inventory: K-convexity, myopic policies, dynamic programming structure. Relevance: the cleanest modern statement of the machinery this project perturbs by sending holding cost to zero.

- **Zipkin, P. H. (2000). *Foundations of Inventory Management*. McGraw-Hill, Boston.**
  The standard reference synthesis of inventory theory — deterministic and stochastic, single- and multi-echelon — with careful treatment of holding-cost logic and of inventory as a flow-balance state. Relevance: baseline against which "commodity with a spot market and speculative demand for stocks" departs from "firm minimizing its own cost"; Zipkin's holding-cost accounting is where the 20 bps number plugs in.

## 2. Production control as servomechanism / feedback

- **Simon, H. A. (1952). "On the Application of Servomechanism Theory in the Study of Production Control." *Econometrica* 20(2), 247–268.**
  Models a production-inventory system as a servo loop, applies Laplace-transform and stability analysis to ordering rules, and shows how lag structure produces oscillation. Relevance: the founding document of the "inventory policy = feedback controller with gain and phase" view; the project's stability questions are Simon's, with price added as a second feedback channel.

- **Vassian, H. J. (1955). "Application of Discrete Variable Servo Theory to Inventory Control." *Operations Research* (JORSA) 3(3), 272–282.**
  Discrete-time (z-transform) servo analysis of periodic-review replenishment; derives the order rule minimizing inventory variance. Relevance: earliest statement that the *variance* of inventory is controlled by the transfer function of the ordering rule — the discrete-time ancestor of the bullwhip transfer-function literature and a template for analyzing dealer restocking rules.

- **Holt, C. C., Modigliani, F., Muth, J. F., and Simon, H. A. (1960). *Planning Production, Inventories, and Work Force*. Prentice-Hall, Englewood Cliffs, NJ.**
  The "HMMS" book: quadratic costs yield *linear decision rules* for production, workforce, and inventory — LQ control before LQ control was named, estimated on real factory data. Relevance: with quadratic costs, optimal inventory policy is linear feedback — exactly the structure in which vanishing holding cost shows up as loss of coercivity in the LQ problem (Section 7). Note the Muth connection: rational expectations was born adjacent to inventory control — **Muth, J. F. (1961). "Rational Expectations and the Theory of Price Movements." *Econometrica* 29(3), 315–335** — written at Carnegie out of the HMMS forecasting problem, and its lead example is a market with inventory speculation; the project's general-equilibrium worry (everyone solving the same control problem) is Muth's consistency requirement.

- **Forrester, J. W. (1961). *Industrial Dynamics*. MIT Press, Cambridge, MA.** (Preceded by "Industrial Dynamics: A Major Breakthrough for Decision Makers," *Harvard Business Review* 36(4), 37–66, 1958.)
  Simulation of industrial supply chains as coupled stock-flow feedback loops; demonstrates demand amplification and oscillation from ordering delays (the "Forrester effect"). Relevance: the intellectual home of Weymar's cocoa thesis — Weymar built his supply-of-storage price model inside this group — so the project's lineage runs literally through this book; it is also the qualitative source of the instability the project wants to formalize.

- **Lee, H. L., Padmanabhan, V., and Whang, S. (1997). "Information Distortion in a Supply Chain: The Bullwhip Effect." *Management Science* 43(4), 546–558.**
  Rationalizes Forrester's amplification as the outcome of *optimizing* agents, via four mechanisms: demand-signal processing, rationing games, order batching, and price variations. Relevance: proves amplification is not irrationality but equilibrium behavior — the same claim the project makes about explosive metal inventories; their fourth cause (price variation inducing forward buying) is precisely speculative stockpiling in embryo.

- **Dejonckheere, J., Disney, S. M., Lambrecht, M. R., and Towill, D. R. (2003). "Measuring and Avoiding the Bullwhip Effect: A Control Theoretic Approach." *European Journal of Operational Research* 147(3), 567–590.**
  Transfer-function (z-transform) analysis of order-up-to policies; proves bullwhip is *guaranteed* for order-up-to rules regardless of forecasting method, and designs smoothed rules that avoid it. Relevance: the exemplary modern "gain analysis of an ordering policy"; the project can do the same frequency-domain analysis on the price-mediated feedback loop between aggregate stocks and metal prices.

- **Disney, S. M., and Towill, D. R. (2003). "On the Bullwhip and Inventory Variance Produced by an Ordering Policy." *Omega* 31(3), 157–167.** (Ancestor: Towill, D. R. (1982). "Dynamic Analysis of an Inventory and Order-Based Production Control System." *International Journal of Production Research* 20(6), 671–687 — the IOBPCS model.)
  Closed-form bullwhip and inventory-variance expressions via z-transforms for proportional-feedback replenishment; exhibits the trade-off frontier between order smoothing and inventory variance. Relevance: skew/width in Cotton–Papanicolaou play the role of the feedback gains here; the bullwhip-vs-inventory-variance trade-off is the dealer's quote-width trade-off in supply-chain clothing.

## 3. Joint pricing and inventory control

- **Whitin, T. M. (1955). "Inventory Control and Price Theory." *Management Science* 2(1), 61–68.** (Book: *The Theory of Inventory Management*, Princeton University Press, 1953.)
  First paper to couple the newsvendor/lot-size model with a demand curve, making price a decision variable alongside stock. Relevance: the point where inventory control stops taking price as given — the project's central move (inventory and price co-determined) starts here.

- **Federgruen, A., and Heching, A. (1999). "Combined Pricing and Inventory Control Under Uncertainty." *Operations Research* 47(3), 454–475.**
  For periodic review with price-dependent stochastic demand and no fixed ordering cost, proves a base-stock–list-price policy is optimal: order up to a base level and mark price down as a monotone function of excess inventory. Relevance: the "price falls monotonically in inventory overhang" result is the firm-level version of supply-of-storage; the monotone map from stock to price is exactly what the project needs at market level.

- **Chen, X., and Simchi-Levi, D. (2004). "Coordinating Inventory Control and Pricing Strategies with Random Demand and Fixed Ordering Cost: The Finite Horizon Case." *Operations Research* 52(6), 887–896.** (Infinite-horizon companion: *Mathematics of Operations Research* 29(3), 698–723, 2004.)
  With a fixed ordering cost, invents symmetric K-convexity to prove an (s, S, p) policy — (s, S) in stock, state-dependent price — is optimal. Relevance: shows the Scarf machinery survives the addition of pricing; the value-function convexity that prices the dealer's skew and width persists under fixed transaction costs.

- **Gallego, G., and van Ryzin, G. (1994). "Optimal Dynamic Pricing of Inventories with Stochastic Demand over Finite Horizons." *Management Science* 40(8), 999–1020.**
  Continuous-time intensity-control formulation of selling a fixed stock by a deadline; closed form for exponential demand, and proves a fixed price is asymptotically optimal as volume grows. Relevance: the pure "liquidate an inventory by pricing" control problem — the deterministic-price limit against which the project's stochastic dealer problem can be benchmarked; its HJB structure recurs in Section 5.

- **Elmaghraby, W., and Keskinocak, P. (2003). "Dynamic Pricing in the Presence of Inventory Considerations: Research Overview, Current Practices, and Future Directions." *Management Science* 49(10), 1287–1309.**
  Survey organizing the pricing-with-inventory literature along replenishment/no-replenishment and myopic/strategic-customer axes. Relevance: the map of the firm-level field; conspicuously, *speculative third-party stockholders* fall outside both of its axes — a gap this project occupies.

- **Anand, K., Anupindi, R., and Bassok, Y. (2008). "Strategic Inventories in Vertical Contracts." *Management Science* 54(10), 1792–1804.**
  In a two-period manufacturer–retailer game, the retailer optimally carries inventory *purely as a bargaining instrument* to depress the future wholesale price — inventory held in equilibrium even when costly and unneeded for demand. Relevance: a clean game-theoretic proof that inventory demand can be strategic rather than operational; with holding costs at 20 bps, this motive alone can dominate, supporting the project's suspicion of explosive equilibrium stocks. (Follow-on: Antoniou & Fiocco, "Strategic Inventories Under Limited Commitment," *RAND Journal of Economics*, 2019.)

## 4. Storage as stochastic control / real option

- **Cahn, A. S. (1948). "The Warehouse Problem" (abstract). *Bulletin of the American Mathematical Society* 54(11), 1073.**
  Poses the original problem: given a warehouse of fixed capacity and known fluctuating prices, find the buy-store-sell program maximizing profit. Relevance: the project's core object — a capacity-constrained trader of a storable good facing prices — stated in 1948.

- **Charnes, A., and Cooper, W. W. (1955). "Generalizations of the Warehousing Model." *Operational Research Quarterly* 6(4), 131–172.**
  Linear-programming treatment of the warehouse problem with buying/selling in multiple periods and financing constraints. Relevance: shows the deterministic warehouse problem is an LP — the degenerate (bang-bang) limit that reappears whenever running costs vanish; cf. cheap control in Section 7.

- **Bellman, R. (1956). "On the Theory of Dynamic Programming — A Warehousing Problem." *Management Science* 2(3), 272–275.** (See also Dreyfus, S., "An Analytic Solution of the Warehouse Problem," *Management Science* 4(1), 99–104, 1957.)
  Recasts the warehouse problem as a DP functional equation; Dreyfus then solves it analytically, with bang-bang (fill/empty) optimal controls. Relevance: the bang-bang structure of optimal storage with negligible holding cost is exactly the project's suspected pathology — inventory slams between bounds, and without bounds it explodes.

- **Boogert, A., and de Jong, C. (2008). "Gas Storage Valuation Using a Monte Carlo Method." *Journal of Derivatives* 15(3), 81–98.**
  Extends Longstaff–Schwartz least-squares Monte Carlo to storage valuation with realistic price dynamics and physical injection/withdrawal constraints. Relevance: the industry-standard computational method for exactly the project's asset class; a warehouse of a low-carry good is a gas cavern with 20 bps carry and no injection limits — which is precisely why the valuation can misbehave.

- **Secomandi, N. (2010). "Optimal Commodity Trading with a Capacitated Storage Asset." *Management Science* 56(3), 449–467.**
  For a Markov spot price and space- plus rate-capacitated storage, proves the optimal merchant policy is a pair of price-dependent basestock targets (buy-up-to / sell-down-to bands). Relevance: the rigorous modern warehouse-problem solution; the two-threshold band is the storage-side twin of the dealer's bid/ask skew, and the width of the band shrinks with carrying cost — degenerating as carry → 0.

- **Carmona, R., and Ludkovski, M. (2010). "Valuation of Energy Storage: An Optimal Switching Approach." *Quantitative Finance* 10(4), 359–374.**
  Models storage (gas dome, pumped hydro) as optimal switching between inject/store/withdraw regimes — a constrained compound American option on calendar spreads — solved by simulation. Relevance: supplies the optimal-switching and impulse-control toolkit for the project's "hold vs. release" decisions on metal stocks, including the option value of unobserved stockpiles.

- **Jaillet, P., Ronn, E. I., and Tompaidis, S. (2004). "Valuation of Commodity-Based Swing Options." *Management Science* 50(7), 909–921.**
  Prices swing (volumetric flexibility) options on energy via a forest-of-trees DP under mean-reverting seasonal prices calibrated to forwards. Relevance: swing rights are storage-like controls priced off the futures curve; the same machinery values a consumer's flexibility to draw inventory versus buy spot — and shows what breaks when there is no liquid futures curve, as for assessment-priced low-carry goods.

- **Little, J. D. C. (1955). "The Use of Storage Water in a Hydroelectric System." *Operations Research* (JORSA) 3(2), 187–197.** (Precursor: Massé, P., *Les Réserves et la Régulation de l'Avenir dans la Vie Économique*, Hermann, Paris, 1946. Modern workhorse: Pereira, M. V. F., and Pinto, L. M. V. G., "Multi-Stage Stochastic Optimization Applied to Energy Planning," *Mathematical Programming* 52, 359–375, 1991 — SDDP.)
  Little's stochastic DP for reservoir release under uncertain inflows is the first computational stochastic storage control; Massé's earlier French treatment already framed reservoirs as "regulating the future," and Pereira–Pinto's SDDP made high-dimensional versions solvable. Relevance: hydro is the mature template for "stock with stochastic replenishment and a value of water (shadow price)"; the marginal value of stored water is the exact analogue of the convenience yield the project must endogenize.

- **Berling, P., and Martínez-de-Albéniz, V. (2011). "Optimal Inventory Policies when Purchase Price and Demand Are Stochastic." *Operations Research* 59(1), 109–124.**
  Base-stock levels for a firm buying a commodity input become functions of the current (mean-reverting or GBM) purchase price, blending procurement speculation with operational stocking. Relevance: quantifies how much *price-motivated* inventory an optimizing industrial consumer holds — the mechanism by which fabricator stocks of low-carry goods swell when prices are believed low, feeding the aggregate feedback loop. (Recent data-driven variant: Mandl, C., and Minner, S., "Data-Driven Optimization for Commodity Procurement Under Price Uncertainty," *Manufacturing & Service Operations Management* 25(2), 371–390, 2023.)

## 5. Market making and execution as stochastic control (control-methods angle)

- **Almgren, R., and Chriss, N. (2001). "Optimal Execution of Portfolio Transactions." *Journal of Risk* 3(2), 5–39.**
  Frames liquidation of a block as mean–variance optimal control with temporary and permanent impact; the efficient frontier of trading trajectories in closed form. Relevance: the canonical "reduce an inventory against price impact" control problem; releasing a government stockpile or an LME overhang is an Almgren–Chriss problem on a physical asset.

- **Guéant, O., Lehalle, C.-A., and Fernandez-Tapia, J. (2013). "Dealing with the Inventory Risk: A Solution to the Market Making Problem." *Mathematics and Financial Economics* 7(4), 477–507.** (Underlying model: Avellaneda, M., and Stoikov, S., "High-Frequency Trading in a Limit Order Book," *Quantitative Finance* 8(3), 217–224, 2008.)
  Reduces the Avellaneda–Stoikov market-making HJB with inventory bounds to a linear ODE system; optimal quotes are explicit functions of inventory. Relevance: the closed-form skew-and-width-as-functions-of-inventory result — the mathematical core that Cotton & Papanicolaou transport from securities to illiquid physical goods.

- **Guilbaud, F., and Pham, H. (2013). "Optimal High-Frequency Trading with Limit and Market Orders." *Quantitative Finance* 13(1), 79–94.**
  Mixed regular/impulse stochastic control for a dealer using both limit and market orders, with a Markov-chain spread; solved numerically with inventory penalization. Relevance: methodological template for a metal dealer who can both quote (make) and hit the market (take) — e.g., simultaneously warehousing and lifting offers in a thin minor-metal market.

- **Cartea, Á., Jaimungal, S., and Penalva, J. (2015). *Algorithmic and High-Frequency Trading*. Cambridge University Press.**
  Textbook consolidation of execution and market-making stochastic control: HJB equations, inventory penalties, ambiguity. Relevance: the standard toolbox reference for the project's dealer-side chapters.

- **Guéant, O. (2016). *The Financial Mathematics of Market Liquidity: From Optimal Execution to Market Making*. Chapman & Hall/CRC.**
  Unified monograph treatment of Almgren–Chriss-type execution and quote-driven market making, including closed forms and multi-asset extensions. Relevance: the cleanest derivations of "skew = slope, width = convexity of the inventory value function" — the identity the project generalizes.

- **Spooner, T., Fearnley, J., Savani, R., and Koukorinis, A. (2018). "Market Making via Reinforcement Learning." *Proc. 17th International Conference on Autonomous Agents and MultiAgent Systems (AAMAS)*, 434–442.**
  Temporal-difference RL agents learn quoting policies with inventory-risk shaping in a high-fidelity LOB simulator, recovering skewing behavior without a model. Relevance: evidence that inventory-linked skew emerges from learning, not just from HJB assumptions — relevant when modeling minor-metal dealers who assuredly do not solve PDEs.

## 6. Mean field games and equilibrium control relevant to commodities

- **Lasry, J.-M., and Lions, P.-L. (2007). "Mean Field Games." *Japanese Journal of Mathematics* 2(1), 229–260.**
  Founds MFG theory: a continuum of small optimizing agents coupled through the distribution of states, characterized by a backward HJB coupled to a forward Kolmogorov equation; includes a price-formation example. Relevance: the right formal language for the project's general-equilibrium question — every agent solves the same storage control problem, and the price is a functional of the inventory distribution; explosive inventory would appear as non-existence or blow-up of the MFG system.

- **Carmona, R., and Delarue, F. (2018). *Probabilistic Theory of Mean Field Games with Applications*, Vols. I–II. Springer (Probability Theory and Stochastic Modelling 83–84).**
  The comprehensive probabilistic (FBSDE) treatment of MFGs, including games with common noise and master equations. Relevance: common noise is essential for the project — a global demand shock hits all metal stockholders simultaneously, and the common-noise MFG machinery is what handles it.

- **Chan, P., and Sircar, R. (2015). "Bertrand and Cournot Mean Field Games." *Applied Mathematics & Optimization* 71(3), 533–569.**
  Continuum Bertrand/Cournot competition among producers with exhaustible resources (oil), coupled through average price/quantity; HJB–Kolmogorov system with numerical solutions. Relevance: the closest existing MFG to the project's setting — dynamic price-mediated competition over a stock variable — but their stock is a *resource in the ground*; the project's above-ground speculative stock version appears to be open. (Existence/uniqueness: Graber & Bensoussan, *Applied Mathematics & Optimization*, 2018.)

- **Alasseur, C., Ben Taher, I., and Matoussi, A. (2020). "An Extended Mean Field Game for Storage in Smart Grids." *Journal of Optimization Theory and Applications* 184(2), 644–670.**
  Extended MFG (interaction through the law of the *controls*) for a continuum of consumers each managing a battery, with the electricity price depending on aggregate storage behavior; existence and characterization via FBSDEs. Relevance: the direct methodological precedent for "price depends on aggregate storage flows" — replace batteries with warehouses and electricity with any low-carry good and this is the project's equilibrium model, minus the speculative motive and near-zero carry.

- **Firoozi, D., and Caines, P. E. (2017). "An Optimal Execution Problem in Finance with Acquisition and Liquidation Objectives: An MFG Formulation." *IFAC-PapersOnLine* 50(1) (20th IFAC World Congress), 4960–4967.** (Related major–minor LQG MFG execution papers by the same authors, CDC 2015–2017.)
  Major–minor agent LQG mean field games for execution: an institutional (major) trader and continuum of (minor) HFTs, with partial observation. Relevance: the major–minor architecture maps onto low-carry dealer markets — a dominant stockholder (e.g., a state stockpile agency, or an exchange-financed hoard) interacting with a fringe of small speculators.

- **Gomes, D. A., and Saúde, J. (2021). "A Mean-Field Game Approach to Price Formation." *Dynamic Games and Applications* 11(1), 29–53.**
  Derives the market-clearing price of a constrained commodity (electricity) as the Lagrange multiplier of a supply–demand balance inside an MFG, giving a price *determined by* the distribution of agents' states. Relevance: the technical device (price = multiplier on aggregate flow balance) the project needs to endogenize metal prices from the inventory distribution, rather than positing a price process exogenously.

## 7. Stability and instability of inventory-feedback systems

- **Metzler, L. A. (1941). "The Nature and Stability of Inventory Cycles." *Review of Economics and Statistics* 23(3), 113–129.**
  The inventory-accelerator model: firms targeting stock proportional to expected sales, with expectation and production lags, generate endogenous damped or explosive cycles depending on the accelerator coefficient — a stability boundary in a second-order difference equation. Relevance: the original proof that inventory feedback can be *explosive* for plausible parameter values; the project's task is Metzler with a price channel and optimizing (not rule-of-thumb) stockholders.

- **Lovell, M. C. (1961). "Manufacturers' Inventories, Sales Expectations, and the Acceleration Principle." *Econometrica* 29(3), 293–314.** (Companion: "Buffer Stocks, Sales Expectations, and Stability: A Multi-Sector Analysis of the Inventory Cycle," *Econometrica* 30(2), 267–296, 1962.)
  Econometric buffer-stock/partial-adjustment estimation of inventory behavior, and (1962) multi-sector stability analysis of the resulting cycle. Relevance: the empirical bridge — his partial-adjustment coefficient is the feedback gain whose estimated magnitude decides which side of the Metzler stability boundary real economies sit on; the same regression is runnable on metal stock data where stocks are observed.

- **Kwakernaak, H., and Sivan, R. (1972). "The Maximally Achievable Accuracy of Linear Optimal Regulators and Linear Optimal Filters." *IEEE Transactions on Automatic Control* 17(1), 79–86.**
  Founds cheap-control analysis: as the control-effort weight ρ → 0 in the LQ cost, regulation error → 0 iff the system is minimum-phase; otherwise a hard performance floor remains. Relevance: the project's ~zero holding cost is a cheap-control limit — the "effort" penalty on carrying inventory vanishes — and this literature says the limit is singular, with qualitative behavior hinging on system zeros (here: the structure of the price-impact channel).

- **Francis, B. A. (1979). "The Optimal Linear-Quadratic Time-Invariant Regulator with Cheap Control." *IEEE Transactions on Automatic Control* 24(4), 616–621.** (See also Jameson, A., and O'Malley, R. E., Jr., "Cheap Control of the Time-Invariant Regulator," *Applied Mathematics & Optimization* 1(4), 337–354, 1975; and O'Malley's singular-perturbation surveys.)
  Rigorous asymptotics of the cheap-control LQ problem: the Riccati solution degenerates, optimal trajectories develop boundary layers (impulsive, near–bang-bang behavior), and the limit is a singular control problem. Relevance: this is the precise mathematical form of the project's suspected pathology — with carry ≈ 0 the inventory LQ problem loses coercivity, optimal stock paths become impulsive/unbounded, and only constraints (capacity, capital) or endogenous price impact restore well-posedness.

- **Trélat, E., and Zuazua, E. (2015). "The Turnpike Property in Finite-Dimensional Nonlinear Optimal Control." *Journal of Differential Equations* 258(1), 81–114.**
  General exponential turnpike theorem: long-horizon optimal trajectories consist of short transients around a long stay near the optimal steady state of the associated static problem. Relevance: gives the project's diagnostic — a well-posed inventory economy should exhibit a turnpike (stocks hover near a steady state); loss of the turnpike as holding cost → 0 (the static problem's solution escaping to infinity) is a sharp formalization of "explosive optimal inventory."

- **Salant, S. W. (1983). "The Vulnerability of Price Stabilization Schemes to Speculative Attack." *Journal of Political Economy* 91(1), 1–38.**
  Shows a buffer-stock agency defending a price band is a control system that rational speculators can break: anticipation of the agency's stock exhaustion triggers a self-fulfilling attack (the commodity analogue of currency-crisis models). Relevance: instability caused not by lags (Metzler) but by *strategic interaction with the controller* — the mechanism by which a metal stockpile policy (or an exchange's visible stocks) invites destabilizing speculation.

## 8. Buffer stocks, stabilization schemes, and strategic stockpiles

- **Newbery, D. M. G., and Stiglitz, J. E. (1981). *The Theory of Commodity Price Stabilization: A Study in the Economics of Risk*. Clarendon Press, Oxford.**
  The definitive welfare analysis of buffer-stock price stabilization: derives optimal (not band) storage rules, treats futures markets as partial substitutes for stabilization, and concludes stabilization schemes are largely undesirable and often dynamically fragile. Relevance: essential grounding — their "optimal buffer stock rule" is a stochastic control problem in the project's exact sense, and their futures-vs-storage substitution result frames the project's with/without-futures-market comparison for low-carry goods.

- **Nichols, A. L., and Zeckhauser, R. J. (1977). "Stockpiling Strategies and Cartel Prices." *Bell Journal of Economics* 8(1), 66–96.**
  Multi-period game between a stockpiling consumer government and a pricing cartel: stockpiles alter the producer's intertemporal pricing problem, and both sides' strategies are computed as equilibrium controls. Relevance: template for modeling China's minor-metal stockpile programs (or the U.S. critical-minerals reserve) as a player whose inventory policy moves price — the strategic layer above the project's competitive equilibrium.

- **Teisberg, T. J. (1981). "A Dynamic Programming Model of the U.S. Strategic Petroleum Reserve." *Bell Journal of Economics* 12(2), 526–546.**
  Stochastic DP over disruption states yielding optimal SPR fill and drawdown rules, including interaction with tariffs/quotas. Relevance: the canonical government-stockpile-as-stochastic-control paper; its fill/release thresholds are (s, S)-like bands in disruption-probability space, directly transplantable to critical-metal reserves with deficit-forecast states. (Empirical coda: Considine 2006 and Kilian & Zhou 2020 estimate SPR release price impacts — the impact function a control model needs.)

---

## Gaps this project could fill

1. **No equilibrium storage model with near-zero carrying cost.** The OR storage literature (Secomandi; Boogert–de Jong) prices a *single* capacitated asset against an exogenous price; the economics literature closes the loop but assumes material holding costs. Nothing characterizes what happens when the coercive term (carry) is ~20 bps: the cheap-control asymptotics (Kwakernaak–Sivan; Francis) have apparently never been applied to speculative storage, and the loss-of-turnpike diagnostic (Trélat–Zuazua) has never been used to formalize "explosive optimal inventory."

2. **No mean field game of speculative storage/hoarding.** MFG theory covers producers of exhaustible resources (Chan–Sircar), electricity batteries (Alasseur et al.), and price formation via multipliers (Gomes–Saúde), but no published MFG has a continuum of agents choosing *above-ground speculative stocks* of a storable commodity with the spot price clearing the flow market — let alone with common-noise deficit shocks and unobservable aggregate stock. This is the natural home of the project's general-equilibrium explosion question.

3. **Dealer market-making theory has not been closed with storage economics.** Cotton–Papanicolaou give the dealer's skew/width as slope/convexity of the inventory indifference cost; the supply-of-storage line (Weymar) gives the market's convenience yield as a function of aggregate stock. No model equates the two — i.e., derives the convenience-yield curve as the aggregation of dealers' indifference-cost convexities. The bullwhip transfer-function toolkit (Dejonckheere et al.; Disney–Towill) then gives a ready-made stability test for the resulting price-mediated loop, which nobody has run.

4. **Unobserved aggregate stock as a filtering-in-equilibrium problem.** Inventory theory has partial observability of demand (Dvoretzky–Kiefer–Wolfowitz II) and MFGs have partial observation of the major agent (Firoozi–Caines), but the low-carry situation — every agent filtering the *aggregate inventory* from prices while their own storage decisions feed the price — is an open equilibrium-filtering problem, and plausibly the source of exchange-financed-hoard episodes.

5. **Markets without futures as a control problem.** Newbery–Stiglitz treat futures as substitutes for stabilization at the welfare level, and the swing/storage valuation literature *requires* a forward curve for calibration. A control-theoretic account of how the absence of a futures market changes optimal storage (no hedge ⇒ risk-averse indifference pricing ⇒ wider dealer quotes ⇒ different equilibrium stock dynamics) for assessment-priced low-carry goods does not exist.
