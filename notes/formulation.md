# Toward a mathematical formulation

*Working notes — feedback from optimal-control readers actively wanted. Everything here is provisional; the point is to expose the structure clearly enough to be attacked.*

The object of study: joint dynamics of **inventory, price level, price volatility, and dealer bid–offer width/skew** for storable low-carry goods, with and without futures markets, in the presence of published supply/demand-deficit forecasts and (usually) unobserved above-ground stocks. The guiding intuition is an **analogy to HJM**: not the traded-curve no-arbitrage machinery itself (for most such goods there is no traded curve), but its discipline — once you specify the state dynamics and impose cross-sectional consistency, the drifts are no longer free. Here four quantities that are often modelled independently turn out to be linked by three layers of constraint.

## 0. Notation

| symbol | meaning |
|---|---|
| $I_t \ge 0$ | above-ground stock in the price-setting identity (latent; *which* stock belongs is a modelling decision — see the Weymar notes) |
| $q_t$ | consumption rate |
| $Y_t = I_t/q_t$ | coverage (units of time) |
| $Y(t,h) = \mathbb{E}_t[Y_{t+h}]$ | the coverage-forecast curve |
| $D(t,h)$ | deficit forecast curve: expected consumption − supply flow at horizon $h$ (published, noisy) |
| $\pi(t,h) = \mathbb{E}_t[\ln P_{t+h}]$ | expected log-price curve |
| $A_t$ | long-run anchor: price the market believes prevails once coverage normalises |
| $f(\cdot)$ | storage curve: expected fractional price change per unit time as a function of coverage; increasing, concave; normalised $f(Y^e)=0$ in real terms |
| $k$ | direct carrying cost (~20 bps/yr for the goods of interest) |
| $x_i,\ \nu_i(x)$ | dealer $i$ inventory and inventory indifference cost (Cotton–Papanicolaou) |
| $w,\ \varepsilon,\ 1/\tau$ | market width, adverse selection, enquiry intensity in the dealer model |

## 1. Layer one: the storage relation as a term-structure constraint

Weymar's local storage relation is a statement about the *slope* of the expected-price curve:

$$\partial_h \pi(t,h) = f\big(Y(t,h)\big).$$

Integrating against the boundary condition $\pi(t,\infty) = \ln A_t$ gives the pricing formula

$$\boxed{\ \ln P_t \;=\; \ln A_t \;-\; \int_0^\infty f\big(Y(t,s)\big)\,ds\ }\tag{1}$$

(real terms; convergence from $f(Y^e)=0$; Jensen corrections suppressed throughout — they belong in a careful pass). The spot price is a **boundary-value problem**: the storage curve supplies slopes, the anchor supplies the level, and the two are separately necessary. Weymar's demonstration that Working's level-only spread rule violates iterated expectations is, in the HJM analogy, exactly the **consistency (drift) condition**: once $f$ and the dynamics of $Y(t,\cdot)$ are fixed, the drift of every point on the price curve is determined. There are no free drifts left to fit.

What does *not* carry over from HJM: a pinned martingale measure. Without traded futures the constraint set is (i) physical accounting (§2), (ii) tower-consistency of expectations, and (iii) optimality of the agents doing the storing (§3–4). A market price of inventory risk $\lambda_t$ remains free — state-dependent, and tied to the supply of speculative capital, which matters in §5.

## 2. Layer two: transport of the coverage-forecast curve

$Y(t,h)$ is a curve-valued state. In Musiela-style coordinates its dynamics decompose as

$$dY(t,h) \;=\; \partial_h Y(t,h)\,dt \;+\; dM_t(h),$$

with $M_t(\cdot)$ a martingale field of forecast revisions, and — this is the key observability fact — the $h$-slope is (minus) the published deficit curve:

$$\partial_h Y(t,h) \;=\; -\,\frac{D(t,h)}{q_t} \;-\; Y(t,h)\,g_q(t,h),\tag{2}$$

where $g_q$ is expected consumption growth. So for the goods of interest the **shape** of the coverage path is observed (up to forecast noise and bias) while its **level** $Y(t,0)$ is latent, and (1) makes the price a measurement of a functional of that level. This is the mirror image of Weymar's setting (he built the stock series and treated forecasts as data; we receive the flow forecasts and must infer the stock), and it is what makes the whole model a filtering problem (§6).

## 3. The volatility constraint

Itô on (1) using the decomposition in §2 (the shift term integrates by parts to reproduce the required drift):

$$d\ln P_t \;=\; f\big(Y(t,0)\big)\,dt \;+\; d\ln A_t \;-\; \int_0^\infty f'\big(Y(t,s)\big)\, dM_t(s)\, ds. \tag{3}$$

Hence instantaneous price variance

$$\sigma_P^2(t) \;=\; \sigma_A^2 \;+\; \big\| f'\big(Y(t,\cdot)\big)\big\|^2_{\Sigma_M} \;+\; \text{cross terms},\tag{4}$$

where $\Sigma_M$ is the covariance operator of forecast revisions. **Constraint I: price volatility is a functional of the coverage path**, weighted by the storage curve's slope. Thin coverage ⇒ steep $f'$ ⇒ high volatility and (from concavity of $f$) upside asymmetry; ample coverage ⇒ the flat region ⇒ volatility floors at anchor volatility. This is the theory-of-storage volatility–inventory relation derived rather than assumed, and it makes news impact **state-dependent**: the same deficit-forecast revision moves the price much more when coverage is low.

## 4. Layer three: the dealer market, and the width/skew constraints

The Cotton–Papanicolaou model gives, for a dealer with inventory $x$ facing Poisson enquiries and exponential inside competition: markup $= w + \varepsilon + $ marginal inventory cost; **skew $S(x)$ = slope of $\nu$; discretionary width $C(x)$ = convexity of $\nu$**; and the Bellman consistency

$$e^{-hC(x)}\cosh\big(hS_\delta(x)\big) \;=\; \Omega\, c(x) \;+\; e^{-hC_0},\tag{5}$$

with $c(x)$ the direct holding cost per unit time and $\Omega$ collecting $\tau, h, \varepsilon$ and imbalance terms. That model deliberately assumed zero price volatility and pushed all price risk into the quadratic term of $c(x)$. For low-carry goods this seam is exactly where the storage layer plugs in: the economically correct holding cost is

$$c(x) \;=\; k\,P_t\,|x| \;+\; \tfrac{\gamma}{2}\,\sigma_P^2(t)\,P_t^2\,x^2 \;+\; \text{funding terms},\tag{6}$$

and with $k \approx$ 20 bps/yr the risk term **dominates**. Composing (6) with (4) and (5):

$$\text{coverage } Y \;\xrightarrow{\ f'\ }\; \sigma_P \;\xrightarrow{\ (6)\ }\; c(x) \;\xrightarrow{\ (5)\ }\; \text{quoted width and skew}.$$

**Constraint II: dealer width is a forward-looking measurement of the latent coverage state**, and width, volatility and inventory cannot move independently. Corollaries: (a) in normal times, low-carry goods should show tight, inventory-*insensitive* spreads — the dealer indifferent to inventory is the same agent who lets stocks wander, so tight spreads and large inventory excursions are one parameter seen from two sides; (b) *departures* — sudden widening or persistent skew — are highly informative precisely because the baseline predicts their absence.

## 5. Aggregation, market clearing, and the explosiveness boundary

**Aggregation (conjecture to prove).** Treat dealers as a mean field with inventory distribution $\mu_t$; the market width $w$ is itself an equilibrium object (each dealer's "inside competition" is the others), so the stationary quoting policy is a mean-field-game fixed point. Conjecture: in the symmetric stationary MFG, the mean dealer skew equals the storage-relation drift over the inter-trade timescale — i.e. **the dealer layer implements $f$ at the short end**, and the storage curve is micro-founded as the aggregation of $\nu_i'$ across the holder population, with the outage-insurance convenience yield emerging as the option value of answering enquiries from stock. If true, $f$ is not an exogenous curve but a derived object, and its steep region maps to the region where dealer fill-probabilities bind.

**Closure.** Consumption responds to price with elasticity $-\eta$ through a lag kernel; supply is exogenous at business frequencies (byproduct goods barely respond to own price); speculative storage demand comes from inverting the storage relation given expected drift; and the anchor is partly extrapolative, $d\ln A_t = \beta\,(\text{trend of }\ln P)\,dt + \dots$ (Weymar's eighty-month filter, his one positive feedback loop).

**Instability.** Linearise around $(Y^*, A^*)$. The damping of the coverage mode is proportional to $\eta\, f'(Y^*)$ plus terms in $k$; the anti-damping is proportional to the extrapolation gain $\beta$. Two things now go wrong at once for low-carry goods:

1. $k \to 0$ widens the flat region of $f$, so over a large range of coverage $f'(Y^*) \approx 0$: the restoring force vanishes and the price–inventory system is locally a random walk driven by anchor revisions.
2. With $f' \approx 0$, **any** $\beta > 0$ is locally destabilising: hoarding that lifts the trend lifts the anchor, which lifts the price, which validates the hoard. Weymar could discard the explosive root of his inventory ODE on the behavioural ground that carrying losing stock forever is absurd; at 20 bps/yr that argument has almost no force. This is the interesting danger flagged in the README, now located precisely: *the stabiliser that fails is the slope of the storage curve times the carrying cost, and the destabiliser that survives is expectation extrapolation.*

The true stabilisers are then boundary phenomena only: the stockout floor $Y \ge 0$ where $f$ steepens violently (Deaton–Laroque nonnegativity), and a **capital/credit ceiling** on speculative positions (limits-to-arbitrage; empirically it is financing, not storage cost, that ends hoards — the 2015 exchange-financed hoard, the 1985 buffer-stock collapse). The state space therefore splits into three regimes: squeeze (steep $f$), an indeterminate near-unit-root band, and a bubble regime terminated by financing. The theorem to aim at: the stability boundary as a surface in $(k, \beta, \eta, g, \kappa)$ — carrying cost, extrapolation gain, demand elasticity, industry forecast quality (Weymar: the damping coefficient of the system), and capital supply — with the claim that $k \approx 20$ bps places these goods on the unstable side absent capital constraints.

**The right existing mathematics** (see `../literature/map_control.md` §7): the $k \to 0$ limit is a **cheap-control singular limit** — in LQ language the penalty on the state's holding cost vanishes, the Riccati solution degenerates, and optimal trajectories develop boundary layers and near–bang-bang behaviour (Kwakernaak–Sivan 1972; Francis 1979). And "explosive optimal inventory" has a sharp formalisation as **loss of the turnpike property** (Trélat–Zuazua 2015): a well-posed inventory economy should exhibit long stays near the static optimum; as $k \to 0$ the static problem's solution escapes to infinity and the turnpike disappears. On the equilibrium side, Bobenrieth–Bobenrieth–Wright (2013) get explosive *price* runs inside rational storage with positive carry (`../literature/map_theory.md` §2) — the quantity-side analogue at $k \approx 0$ appears open.

## 6. The filtering formulation

State: $\big(Y(t,0),\ \theta_t,\ A_t,\ \text{trend state},\ \text{dealer moments}\big)$ where $\theta_t$ is a finite-dimensional parameterisation of the coverage-path shape (whose $h$-slope is pinned by the published deficit curve via (2)). Observations:

1. assessed mid price — measurement of the level through (1);
2. assessed bid/offer width (and any observable skew) — measurement through (4)–(6);
3. the deficit forecast curve itself — direct but biased/noisy measurement of $\partial_h Y$;
4. occasional stock revelations (surveys, disclosures, exchange stocks where they exist) — sparse direct measurements of $Y(t,0)$.

The filter is necessarily nonlinear ($f$ is nonlinear exactly where it matters) — particle or unscented. Identifiability inherits Weymar's warning: $(A^e, Y^e)$ trade off through the intercept of (1), so priors from storage-cost arithmetic must pin the corner (his own discipline: bracket parameters from first principles before estimating). The finite-dimensional-realisation question from the HJM literature (Björk–Christensen) has a precise analogue: **for which pairs (storage curve, forecast process) is a finite-dimensional coverage family invariant** — i.e. when is the filter exactly finite-dimensional? Working's "current inventory is a sufficient statistic" special case is precisely the one-dimensional realisation.

## 7. Falsifiable implications

1. Assessed width should co-move with, and *lead*, realised volatility (both are functions of latent coverage; quotes are forward-looking).
2. Price impact of deficit-forecast revisions should be state-dependent, scaled by the filtered $f'(Y)$ — large near squeezes, near-zero in the flat region.
3. Persistent dealer skew should forecast drift at the inter-trade horizon.
4. Cross-sectional: lower $k$ ⇒ longer near-unit-root spells, fatter spike distributions, and weaker inventory-sensitivity of spreads in normal times.
5. Where a futures cousin exists, the model-implied expected-price curve minus the futures curve estimates the hedging-premium term structure — Weymar's proposed-but-never-executed extension, now runnable.

## 8. Immediate work items

1. Prove (or break) the aggregation conjecture of §5 in a symmetric stationary MFG.
2. A small simulator: latent coverage driven by deficit forecasts, pricing via (1), dealer layer via (5)–(6); exhibit the stability boundary in $(k,\beta)$ and the three-regime phase portrait.
3. Assemble assessed price + bid/offer + forecast series for one assessment-priced good and run the filter of §6 in its simplest form.
