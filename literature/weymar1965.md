# Weymar (1965): *The Dynamics of the World Cocoa Market*

F. Helmut Weymar, PhD thesis, Department of Economics, MIT, February 1965 (supervised by Paul Cootner, with Franklin Fisher, Charles Kindleberger and Paul Samuelson on the committee; estimated on monthly data September 1952 – August 1963; later published as *The Dynamics of the World Cocoa Market*, MIT Press, 1968). Weymar went on to co-found Commodities Corporation. The thesis is the grounding document for this project; what follows is a working distillation of the ideas we intend to port to low-carry goods.

## Why it matters here

The thesis does three things that are rarely done together, and never casually: it builds a theory of what a spot price *is* for a storable commodity; it estimates that theory on monthly data much of which the author had to construct; and it runs the estimated system as a dynamic simulation, interrogating it the way an engineer interrogates a filter (Weymar wrote it inside the orbit of Forrester's Industrial Dynamics group). Each leg disciplines the others.

## The bookkeeping argument

Write the general model of any storable commodity: consumption as a function of current and lagged price; production as a function of current and lagged price; a storage relation connecting expected price change to inventories; and the identity that inventory is the running integral of production minus consumption. None of these equations *is* the price mechanism. The price mechanism is implicit in whichever equation is left with degrees of freedom at the chosen data interval — so every empirical commodity study is, whether stated or not, a bet about which equation carries the price. If the data interval is short relative to the response lags of consumption and production (months, for cocoa; plausibly also for the goods of interest), both are predetermined and **the storage relation alone carries the price**: the spot price is the price at which holders are willing to carry exactly the stock that exists.

## Supply of storage, and the anatomy of convenience yield

The storage relation says the expected rate of price appreciation demanded by the marginal holder is an increasing, concave function of the coverage ratio (stocks ÷ consumption rate — always time units, never tonnes). Weymar decomposes the marginal convenience yield into two services:

1. **Outage insurance** — stocks prevent capital-intensive processing from being idled. Large when coverage is thin, decaying quickly to zero as coverage grows.
2. **Cost-coverage / keep-in-line insurance** — processors price finished goods off the average cost of raw material in inventory and prefer not to reprice often; carrying more coverage than competitors is dangerous in a falling market, less than competitors in a rising one. This is a *strategic complementarity* in inventory holding: each firm wants coverage in line with the pack, which makes the marginal convenience yield of this service turn **negative** when coverage is excessive. The upward bend at the right of the storage curve is an equilibrium property, not just warehouses filling up.

Where futures exist, futures and physical stocks are near-perfect substitutes for the cost-coverage service and no substitute at all for outage insurance (you cannot melt a futures contract). Normal backwardation is a condition, not a law: it holds iff short hedging exceeds long hedging when no price change is expected — an empirical matter of industry structure, commodity by commodity.

## The path, not the level

Holbrook Working's empirical rule — intertemporal price spreads are determined by the current inventory level alone — cannot be right in general. Apply the storage relation at one- and two-month horizons and impose consistency of expectations (Muth, cited two years after publication): the two-month spread must depend on inventory *expected to exist one month out*, contradicting a level-only rule. Shrinking the expectation interval to zero makes the storage relation a local object, and integrating it along the horizon gives the central pricing formula: **the spread between the spot price and any expected future price is a path functional of the expected coverage trajectory**,

```
ln( P*ₜ,ₕ / Pₜ ) = ∫₀ʰ f( Y*ₜ,ₛ ) ds
```

where `Y*ₜ,ₛ` is coverage expected at horizon `s` and `f` is the (increasing, concave) storage curve. Because `f` is nonlinear, the functional is economically weighted: expected scarcity while coverage is in the steep region counts enormously; the same tonnage in the flat region counts for almost nothing. Two expected paths with identical endpoints or averages can price differently depending on *when* tightness is expected to fall.

Working's rule survives as a conditional special case: when seasonality makes the future path a predictable function of the present state (post-harvest rundown), or when stocks are ample enough that the whole path lives in the flat region of the curve. The right question for any market is *how far the current state pins down the expected path* — an empirical property of the commodity's calendar and storage economics, not a matter of theory.

Equally important: the storage relation delivers only **slopes**. The level of the whole expected-price curve — and hence the spot price — is set by the terminal condition: the price the market believes prevails once coverage has normalised. This is a boundary-value problem and the boundary does real work; the normal price and the equilibrium coverage ratio cannot be separately identified from the price regression (they trade off through the intercept).

## Dimensional hygiene

The model is homogeneous of degree zero in both money and quantity units: spreads as fractional (log) price changes, inventory as coverage in units of time. The reasons are economic, not cosmetic — speculative capital, carrying charges and processing margins all scale with price; convenience yield and trade-channel capacity scale with throughput. Everything ends up in logarithms.

## The linear special case, and its warning

Linear demand, harvests fluctuating randomly around equilibrium consumption, the inventory identity, and a linear storage relation, under rational expectations and certainty equivalence: the expected inventory path solves a second-order ODE; discarding the explosive root on behavioural grounds (nobody believes price and inventory stay above equilibrium forever) leaves exponential decay, and integrating along it collapses the entire forward-looking apparatus into

```
Pₜ = Pᵉ − √(a/b) · ( Iₜ − Iᵉ )
```

— current price a function of current inventory alone. The collapse is a warning about what strong assumptions buy, and the **root-selection step is exactly the pressure point for this project**: the behavioural argument that kills the explosive root leans on carrying costs being material. (See the README: at ~20 bps/yr it barely binds.)

## Expectations as data

The empirical closure splits the horizon at the crop-year end. Before it, the expected coverage path is pinned by *published industry forecasts* of production and consumption (the London dealer Gill & Duffus published monthly world figures) — expectations enter as observed data, not as an assumed rule. A seasonal bridge (regressing historical mid-months coverage on the two endpoint ratios; R² ≈ 0.97) converts the path integral into a scalar that is linear in the storage-curve parameters. After the crop-year end, coverage is assumed to decay geometrically to equilibrium. The resulting price equation: spot price as a function of current coverage, expected crop-year-end coverage, and the long-run equilibrium price.

Notable sub-machinery:

- **Crop nowcasting**: cumulative marketing-board purchases divided by the fraction normally bought by that week gives a running crop estimate (the multiplier tabulated from six seasons). Its built-in failure mode — the rule cannot tell a small crop from a late one — produced two false alarms and one true one in the sample, indistinguishable in real time.
- **Consumption forecasts** modelled as a filter with time-varying gain on trend, price change, and realised grind — with gain weights that depend on the calendar month, i.e. on how much information has arrived.
- **Priors before estimates**: storage-cost arithmetic brackets the curve's intercept; average coverage brackets the parameter ratio; the estimates are then required to land inside the brackets (they do).

## The anchor, and the nine-year cycle

The long-run equilibrium price expectation is the one expectation never observed. Adaptive smoothing of past price *levels* failed outright; what worked (R² 0.948, all structural parameters inside prior bands) was **extrapolation**: the postwar average price multiplied by the exponential of a weighted average of the last eighty months of fractional price changes. This term is a genuine positive feedback loop sitting inside an otherwise mean-reverting system — recent trend lifts the perceived normal price, which lifts the spot — and it is what gives the estimated system a natural period.

The simulation chapter treats the estimated system as a filter and measures its transfer function: near-total suppression of exogenous consumption cycles below ~2 years, mild amplification near 4½–5 years, strong amplification near **9 years**, plateau of 4.0 at very long periods (the reciprocal of the demand elasticity ≈ −0.25). Impulse response of a single 20% crop failure: price spike → anchor rises → price settles above the old steady state → consumption undershoots, coverage rebuilds → a year of falling prices drags the anchor down in a self-reinforcing decline that runs for years → a second, diminished peak roughly eight years later. Driven by *white* annual crop noise, the system produces major peaks ~8 years apart endogenously.

Three consequences worth carrying around permanently:

1. **Attribution hazard.** A system with a preferred frequency hands credit for its own timing to whatever news arrives near the turning points. In simulation, every major peak coincides with a short crop and every trough with a large one — yet identical shocks in the wrong phase are absorbed silently. The crop–price correlation is real; the causal narrative built on it is spurious; and no amount of care in reading the news can fix this, because the discriminating information is a property of the system, not of any observation.
2. **Forecast quality is the damping coefficient.** The market damps high-frequency noise exactly to the extent the industry forecasts itself well (a 40% range of quarterly demand shocks produced only a 6% consumption response). If the trade merely extrapolated, the loop would carry enough lag to oscillate visibly. Better industry forecasting is not merely privately profitable; it stabilises the system.
3. **Honest instability about its own assumptions.** The derivation assumes participants expect monotone convergence; the simulation shows the system oscillates. Weymar flags the tension rather than hiding it — and notes that the nine-year endogenous period sits uncomfortably close to half the cocoa-tree cobweb period he had deliberately excluded, so the coupled system may behave differently again.

## Which inventory prices the market

The inventory identity accumulates **producer sales, not production**: what prices the market is commercial stock — released by origin and not yet consumed. Stocks held back at origin are real, count toward the crop, and are absent from the price-setting identity (Brazil's 1957 withholding operation removed nearby supply while every bean still existed). Total physical stock, origin stock, export availability, exchange-certified stock, merchant stock and processor stock are six different state variables, and deciding which subset belongs in the identity is the **first modelling decision** when porting the framework — in our setting: producer, government/strategic, exchange, financing-deal and processor stocks all differ, and hoards (visible or not) may sit entirely outside the price-setting identity until they don't.

## Methodological stances worth inheriting

- **Constructed data, honestly flagged**: none of the required monthly series existed; all were built from quarterly/annual data and dealer letters under stated rules. The defence is an asymmetry — badly constructed data can easily produce a poor fit, but will only very rarely produce a good fit with significant, correctly signed, independently plausible coefficients. Evidence from constructed data is weak against a theory and strong for it.
- **Simulation as the test that t-statistics cannot perform**: specification errors invisible to significance tests (e.g., regressing on current price when the truth is a distributed lag) announce themselves in simulation as phase errors. Amplitude and phase are the diagnostics. And beware the feedback-controller trap: the subsystem is built to track certain variables, so tracking them is worth nothing as evidence; only the variables the controller does *not* directly regulate (price, inventory) count.
- **Report identification failures plainly**: the anchor level and equilibrium coverage trade off through the intercept; sub-sample stability fails a Chow test for stated collinearity reasons; the fitted lag weights were hand-smoothed and re-estimated. All reported as such.

## What we port, in one list

1. Price = boundary-value problem: storage curve gives slopes of the expected-price curve; an anchor expectation gives the level.
2. Coverage (time units), fractional price changes, logs throughout.
3. Expectations as *data* — for low-carry goods, published deficit forecasts play Gill & Duffus's role, with the twist that the stock level itself is unobserved (see README).
4. Convenience-yield anatomy: outage insurance + strategic keep-in-line term (negative yield possible) — and a dealer-market microfoundation candidate in `trading_illiquid.pdf`.
5. The root-selection warning: with near-zero carrying cost, the behavioural case against explosive inventory paths weakens materially.
6. Which stock is in the identity — first decision, not a detail.
7. Attribution hazard and transfer-function thinking as standing discipline for any model we simulate.
