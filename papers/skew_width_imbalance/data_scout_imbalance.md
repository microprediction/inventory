# Data scout: measuring dealer skew & width response to flow imbalance

Goal: public/cheap datasets for an illiquid dealer/RFQ-style market where one can measure
(i) quoted or effective bid/ask width, (ii) quote skew or buy-vs-sell markup asymmetry,
(iii) customer flow imbalance (buys vs sells), at daily+ frequency.

Predictions to test: skew-at-zero-inventory delta = log((1-p)/p)/2h; parameter-free width
multiplier 1/(2*sqrt(p(1-p))); skew sign-flip when imbalance crosses 1/2.

Status: COMPLETE (2026-08-07). Sources visited directly; costs and fields verified where stated.

---

## 1. Municipal bonds — MSRB (EMMA / RTRS)

**Verdict: best fit. Cheap academic access confirmed.**

- Every reported trade carries a **trade type designation: dealer-to-customer (customer bought),
  customer-to-dealer (customer sold), or inter-dealer** — exactly the side flags needed to build
  (a) buy-vs-sell markup asymmetry (skew), (b) effective width (round-trip markup), and
  (c) daily flow imbalance p per CUSIP or per dealer.
- **Academic Historical Transaction Data Product**: full RTRS transaction history **with anonymized
  dealer identifiers** (so dealer-level inventory paths can be reconstructed — lets us separate
  the inventory term from the pure-imbalance skew term, i.e. test skew-at-zero-inventory directly).
  Three-year lag. **$500/year + $500 one-time setup**; MSRB states fees may be waived/reduced for
  academic institutions. Source: https://www.msrb.org/Market-Data-and-Research/Academics
  License agreement PDF: https://www.msrb.org/sites/default/files/2022-08/Historical-Academic-Transaction-Data-Product-License-Agreement.pdf
- Non-academic RTRS Historical Data (no dealer IDs, no lag): $2,500/yr + $2,000 setup.
- **Also on WRDS** ("MSRB" dataset, trade-level with trade type flag, 2005–present) — zero
  marginal cost if the institution subscribes to WRDS.
- EMMA website itself (emma.msrb.org) shows per-CUSIP trade history with the same side flags,
  free, but is a lookup UI, not a bulk feed.
- Literature precedent: Green–Hollifield–Schürhoff (RFS 2007) and Schultz (JFE 2012-era work)
  used MSRB transaction data with dealer identifiers under academic agreements; Hollifield et al.
  reconstruct dealer markups by side — confirms the product supports exactly this measurement.
- History span: RTRS from Jan 2005 (audit-trail era); ~1998–2004 available at lower fidelity.

**Model fit**: quintessential illiquid dealer market, quote-on-demand (effectively RFQ-like),
hundreds of thousands of CUSIPs that trade a few times a month. Predictions testable:
- Skew: regress signed markup asymmetry (dealer sell markup minus dealer buy markdown, both vs
  interdealer midpoint) on log((1-p)/p) where p = share of customer buys in enquiries/trades.
- Skew-at-zero-inventory: condition on anonymized dealers with flat inventory (academic product).
- Width multiplier: round-trip cost vs 1/(2*sqrt(p(1-p))) across CUSIP-days.
- Sign-flip: markup asymmetry should change sign as imbalance crosses 1/2.
Caveat: p is measured from executed trades, not enquiries (RFQ enquiry data is not public).

## 2. Corporate bonds — FINRA TRACE

**Verdict: strong second; same price point; on WRDS for most schools.**

- **Academic Corporate Bond TRACE Data**: transaction-level history with **masked (but
  persistent) dealer identifiers** and buy/sell/interdealer side flags; **36-month delay**;
  **$500/year + $500 setup**, no redistribution. Pricing page:
  https://www.finra.org/filing-reporting/trace/pricing ; product created under Rule 7730
  (Regulatory Notice 16-43). Apply via FINRA data agreements (contact on the pricing page).
- **Enhanced Historical TRACE** (uncapped sizes, side flags, no dealer IDs): $2,000/yr
  ($1,000 setup + $500/yr for tax-exempt orgs). **Available on WRDS** as "TRACE Enhanced"
  (2002–present) — the standard route in the literature; zero marginal cost with WRDS.
- Fields per record: CUSIP, date/time, price, yield, size (capped in standard, uncapped in
  enhanced), **RPT_SIDE / buy-sell indicator, contra-party type (customer vs dealer)**.
- Literature: O'Hara–Zhou and Hendershott–Madhavan (electronic vs voice RFQ) use Enhanced
  TRACE; Hendershott–Madhavan additionally used proprietary MarketAxess RFQ data (enquiries,
  not public). Goldstein–Hotchkiss, Di Maggio–Kermani–Song use the academic version with
  masked dealer IDs for inventory work.

**Model fit**: dealer/RFQ market; more liquid than munis on average but the long tail of bonds
is very illiquid. Same three predictions testable as for munis; enhanced TRACE on WRDS is the
fastest path (no dealer IDs -> aggregate skew tests), academic TRACE ($500) adds dealer-level
inventory conditioning.

## 3. StockX (sneaker/streetwear resale)

**Verdict: uniquely direct measurement of a two-sided quote board on physical illiquid goods,
but access is the bottleneck.**

- Every product-size variant displays a **standing highest bid and lowest ask** — a literal
  observable quote pair on a physical good — plus last-sale history. Width and midpoint skew
  (relative to subsequent sale prices) are directly measurable; flow imbalance inferable from
  whether sales cross at the standing ask (buyer-initiated) vs the standing bid (seller-initiated).
- **Official Public API** (developer.stockx.com): Market Data endpoint returns "the highest Bid
  and lowest Ask amount for all variants of a given product" + sales endpoints. OAuth2; access
  requires applying through the Developer Portal and is oriented at **approved sellers/partners**
  — approval is discretionary, no published academic track; free once approved. Docs:
  https://developer.stockx.com/portal/getting-started/ , /portal/api-reference .
- Scraping: pages are JS-rendered; ToS prohibits scraping; widely done anyway via unofficial
  endpoints — not an "accepted" academic route, flag as legal-risk.
- **Ready-made dataset**: "StockX Sneaker Size-Day Dataset" (IEEE DataPort, DOI
  10.21227/mdj8-4y59, Rice Univ.): **daily lowest ask / highest bid / last sale** for 50 models
  x sizes, 136,980 size-day records, May–Sep 2025. Requires an IEEE DataPort subscription (many
  universities have one). Short span but zero collection effort.
- Academic literature using StockX bid/ask microstructure: thin — mostly an HBS teaching case and
  forecasting exercises; a genuine microstructure test here would be novel.

**Model fit**: caveat — StockX is a consignment order book, not a single dealer; quotes are the
best of many participants (though professional resellers act as de facto market makers). Good
for the **width multiplier** prediction (spread vs 1/sqrt(p(1-p)) across product-days) and the
**skew sign-flip** at market level; weak for inventory conditioning (no participant IDs).
Effort: low if the IEEE dataset suffices; medium-high (application or own 2–3 month scrape) otherwise.

## 4. iBuyers in residential real estate

**Verdict: conceptually perfect (a literal dealer in houses) but data assembly is heavy;
better cited than replicated.**

- Buchak–Matvos–Piskorski–Seru, "Why Is Intermediating Houses So Difficult? Evidence from
  iBuyers" (NBER WP 28252; later JPE) identify iBuyer purchases/sales by matching buyer/seller
  entity names in **CoreLogic deeds records** — a commercial dataset (institutional license,
  typically $10k+; some schools have it). No public replication dataset located on the NBER or
  Stanford GSB pages (https://www.nber.org/papers/w28252).
- Free route exists but is laborious: county recorder deed records are public; iBuyer entities
  (recognizable LLC grantee/grantor names) can be matched purchase-to-resale to get markdown
  (buy vs AVM) and markup (resale vs buy) per house. County-by-county scraping, months of work.
- Zillow Research (https://www.zillow.com/research/data/ — blocks bots but free CSVs in-browser)
  provides monthly metro/ZIP indicators usable as the **imbalance** proxy (sale-to-list ratio,
  share of listings with price cut, days-to-pending, inventory), not transaction-level data and
  nothing on the discontinued Zillow Offers program.
- Frequency: monthly at best; spread is realized round-trip (buy->sell over months), not quoted.

**Model fit**: dealer with inventory, quotes-on-demand (an iBuyer offer IS an RFQ response) —
excellent narrative fit; but only the dealer's executed buys (accepted offers) are visible, no
declined quotes, and imbalance proxies are coarse. Effort: high. Keep as a motivating example /
citation, not a primary empirical test.

## 5. Prediction markets — Kalshi and Polymarket

**Verdict: best free/instant option. Kalshi in particular gives quoted width + taker-side flow,
daily or hourly, no auth, no cost. VERIFIED against live API docs.**

**Kalshi** (docs.kalshi.com):
- `GET /markets/{ticker}/candlesticks` returns, per 1-min/1-hour/1-day bar: **yes_bid OHLC,
  yes_ask OHLC**, trade-price OHLC, volume, open interest. Quoted width history for every
  market, directly. (https://docs.kalshi.com/api-reference/market/get-market-candlesticks.md)
- `GET /markets/trades` returns every trade with **taker_outcome_side / taker_book_side** —
  i.e., signed customer flow, hence imbalance p per market-day. No authentication required
  (spec shows security: []), cursor pagination, min_ts/max_ts filters.
  (https://docs.kalshi.com/api-reference/market/get-trades.md)
- Orderbook endpoints for current depth; markets settled before a historical cutoff move to a
  separate historical endpoint (still documented/available).
- Thin event markets frequently have a single professional maker on each side — close to a
  dealer market in practice; CFTC-regulated exchange, clean licensing for research use.

**Polymarket** (docs.polymarket.com): public no-auth endpoints for order book snapshots,
prices-history timeseries, klines, and recent trades (maker/taker identified); complete fill
history is on-chain (Polygon) and queryable free via Dune. More markets and longer thin tail
than Kalshi, but historical *quote* (bid/ask) series must be reconstructed from on-chain fills
or third-party archives — more effort than Kalshi's native bid/ask candlesticks.

**Model fit**: two-sided quotes + signed flow + extreme illiquidity in tail markets. Tests:
width vs 1/(2*sqrt(p(1-p))) across market-days (parameter-free!); quote-midpoint skew vs
log((1-p)/p); sign-flip when taker imbalance crosses 1/2. Inventory of the (unobserved) maker
is not directly visible, but at-listing (t=0, presumably flat inventory) skew vs early enquiry
imbalance approximates the zero-inventory prediction. Caveat for the paper: CLOB not RFQ, and
prices bounded in [0,1] (width scaling near extremes needs care). Effort: low (a weekend of
API pulls).

## 6. NFT markets

**Verdict: viable but the tooling regressed; medium effort, free.**

- **Reservoir API is dead**: new signups disabled and full shutdown 15 Oct 2025; the company
  pivoted (site redirects to Relay). Codebase open-sourced (self-hosting an indexer is heavy).
- Alternatives: **Alchemy / OpenSea APIs** (current best bid & floor ask per collection/token,
  free tiers) and **Dune** (free tier SQL over on-chain Seaport/Blur bid, listing, and fill
  events — full history reconstructible, including side of each fill: bid-hit vs ask-lift).
- Measurable: collection-level top-bid/floor-ask width, its skew around later sale prices, and
  signed fill imbalance; token-level markets are extremely illiquid (good for the theory).
- Caveats: market activity collapsed post-2022 (sample relevance), wash trading, and quotes come
  from many participants (though a handful of bid-pool market makers dominate — semi-dealer).
Effort: medium (SQL archaeology on Dune). Cost: free.

## 7. Crypto OTC / RFQ

**Verdict: confirmed no public data; move on.**

- OTC desks (RFQ) publish nothing — no quotes, no flow. Paradigm (institutional RFQ network
  for crypto derivatives) prints blocks to Deribit's public tape, but without enquiry/quote data.
- Fallback: **Binance historical dumps, free** at https://data.binance.vision/ — daily/monthly
  zips of trades and aggTrades (with buyer-is-maker flag => taker side => imbalance), klines,
  and for futures bookTicker (best bid/ask) and partial bookDepth. Everything needed is there,
  but it is a liquid central LOB — useful only as a robustness/contrast dataset, not the
  illiquid-dealer setting of the paper.

## 8. Quick verdicts: cars, wine, watches

- **Used-car wholesale**: Manheim data is dealer-licensed and paid; only the free monthly
  Manheim index (aggregate) is public. Copart shows per-lot bids pre-sale but no bulk sold-price
  feed and no dealer two-sided quotes. **No side-flagged flow anywhere. Skip.**
- **Fine wine (Liv-ex)**: structurally attractive — a B2B exchange for an illiquid physical
  good with a **visible highest live bid / lowest live offer** per wine (used for their index
  mid-prices). Data feed exists (datafeed.liv-ex.com) but is commercial; no published academic
  program; papers mostly use free Liv-ex *indices*, not bid/offer records. **Worth one email to
  Liv-ex research team; otherwise skip.**
- **Watches (Chrono24 / WatchCharts)**: listings are ask-only — no bid side, no flow flags;
  WatchCharts API is paid and one-sided. **Poor fit. Skip.**

## 9. Wildcard find: single-dealer trading-card quotes (buylist vs retail)

**Verdict: arguably the purest public single-dealer two-sided quote data in existence;
unconventional but novel.**

- Large card dealers (e.g. Card Kingdom for Magic: the Gathering) publicly post, for tens of
  thousands of distinct illiquid physical goods, BOTH a **buylist price (the dealer's bid)** and
  a **retail price (the dealer's ask)** — plus displayed inventory counts and buylist quantity
  caps. One identified dealer, quotes on demand, inventory-managed: literally the model.
- History: MTGGoldfish tracks daily retail and buylist price history with spread ("daily price
  history, trend stats, spread, highest buylist"); premium (~$6/mo) allows price-history
  downloads; TCGSentry tracks "live buylist price and its full history" for Card Kingdom.
- Measurable: width = retail - buylist per card-day; skew = movement of the bid/ask pair around
  a market reference (e.g. TCGplayer market price); imbalance/inventory = changes in displayed
  stock counts and buylist caps. Buylist caps ("buying up to N") are an explicit revealed
  inventory target — a direct window on the inventory term.
- Caveats: no explicit customer-flow prints (flow inferred from inventory deltas); scraping ToS
  gray zone for the raw sites (MTGGoldfish premium download is the clean route); niche market
  may raise referee eyebrows. Effort: low-medium. Cost: ~free.

---

## Ranked summary table

| # | Dataset | Width | Skew | Imbalance | Freq / span | Access & cost | Model fit (RFQ/dealer, inventory) | Effort |
|---|---------|-------|------|-----------|-------------|---------------|-----------------------------------|--------|
| 1 | MSRB muni transactions | effective (round-trip markup) | yes: buy vs sell markup vs interdealer mid | yes: customer-buy vs customer-sell counts | trade-level; 2005–now (3y lag on academic product) | $500/yr + $500 setup academic (fee waivable); or free via WRDS | excellent: quote-on-demand dealer market; anonymized dealer IDs => inventory paths | medium |
| 2 | Kalshi API | quoted (yes_bid/yes_ask OHLC per day/hour/min) | yes: quote placement vs trades/settlement | yes: taker_outcome_side per trade | minute–daily; several years | free, public, no auth | good: CLOB but thin markets ~ single maker; no maker inventory | low |
| 3 | FINRA TRACE (enhanced/academic) | effective | yes (side flags) | yes | trade-level; 2002–now | free via WRDS (enhanced); $500/yr academic (dealer IDs, 36m lag) | very good; masked dealer IDs => inventory | medium |
| 4 | Card-dealer buylist/retail (sec. 9) | quoted, single dealer | yes (bid/ask vs market ref) | inferred from inventory deltas + buylist caps | daily; ~10y via trackers | ~$6/mo (MTGGoldfish premium) or scrape | excellent structurally: one dealer, two-sided quotes, visible inventory targets | low-med |
| 5 | Polymarket + Dune | reconstructed quotes; current books free | partial | yes (taker side on-chain) | tick; 2020–now | free | good (thin CLOB) | medium |
| 6 | StockX | quoted (best bid/ask per size) | market-level | inferred (cross side) | daily; IEEE set May–Sep 2025, longer if API granted | IEEE DataPort sub or discretionary API approval | fair: consignment book, not one dealer | med-high |
| 7 | NFT (Dune/Alchemy/OpenSea) | top bid / floor ask | market-level | yes (fill side) | tick; 2021–now | free | fair; relevance/wash-trading issues | medium |
| 8 | iBuyer housing | realized round-trip | markdown vs markup | coarse metro proxies (Zillow CSVs) | monthly; 2015–now | CoreLogic $$$ or county-deed scraping | conceptually perfect dealer; data heavy | high |
| 9 | Binance dumps | quoted (bookTicker) | yes | yes (taker flag) | tick; 2017–now | free | poor (liquid LOB, not dealer) — contrast only | low |
| 10 | Liv-ex wine | live best bid/offer exists | ? | ? | daily | commercial feed; email for academic terms | good structurally, access unknown | unknown |
| — | Used cars, watches, crypto OTC | — | — | — | — | — | no two-sided public quotes / no flow flags | skip |

## Recommended shortlist & acquisition plans

### A. MSRB municipal transaction data (primary, headline test)
Why: side-flagged trades in a canonical illiquid quote-on-demand dealer market; anonymized
dealer IDs allow conditioning on (near-)zero dealer inventory — the paper's sharpest prediction
(skew at zero inventory driven purely by imbalance) is testable nowhere else this cheaply.
Plan:
1. Check WRDS first: wrds-www.wharton.upenn.edu -> "MSRB" dataset (trade type flag, 2005–now).
   If institution has WRDS, start here same-day (no dealer IDs on WRDS, but all three aggregate
   tests run immediately).
2. In parallel, request the Academic Historical Transaction Data Product (dealer-ID version):
   https://www.msrb.org/Market-Data-and-Research/Academics — download the request guide, sign
   the license (PDF above), pay $500+$500 (ask for the academic fee waiver explicitly).
3. Build per-CUSIP-day: p = buys/(buys+sells); markup/markdown vs same-day interdealer prints;
   test delta = log((1-p)/p)/2h, width ratio 1/(2*sqrt(p(1-p))), and the sign-flip at p=1/2.

### B. Kalshi (fast, free, quoted — not just effective — spreads)
Why: the only source with directly *quoted* bid/ask history AND signed taker flow, free, today;
ideal for the parameter-free width-multiplier plot and the skew sign-flip figure.
Plan:
1. No signup needed. Pull `GET /trade-api/v2/markets` (all tickers incl. settled), then per
   market `GET .../candlesticks?period_interval=1440` (daily yes_bid/yes_ask OHLC) and
   `GET /markets/trades?ticker=...` (taker side). Docs: https://docs.kalshi.com .
2. Restrict to thin markets (low open interest / few trades per day) to approximate the
   single-dealer regime; compute daily p from taker sides, width from ask-bid close.
3. Watch the [0,1] price bounds: work in log-odds space, matching the model's h-units.

### C. (Optional novelty) single-dealer card quotes
Why: a literal identified dealer posting bid and ask with visible inventory on thousands of
illiquid goods; makes a memorable illustrative figure even if the headline stats come from A/B.
Plan: MTGGoldfish premium account -> historical retail+buylist downloads for a card sample;
cross-check with TCGSentry Card Kingdom buylist history; use inventory-count deltas as flow.

## Which predictions map where

- **Skew at zero inventory ~ log((1-p)/p)/2h**: MSRB/TRACE academic products (dealer-ID
  inventory conditioning); Kalshi at market open (maker starts flat).
- **Parameter-free width multiplier 1/(2*sqrt(p(1-p)))**: Kalshi (quoted width, cleanest);
  StockX/cards (quoted); MSRB/TRACE (effective width via round-trip markups).
- **Skew sign-flip at p = 1/2**: all of A–C; visually sharpest in Kalshi and MSRB.

*Access mechanics above verified by direct visits on 2026-08-06/07 (MSRB academics page, FINRA
pricing page, Kalshi API reference incl. candlestick/trade field lists, Polymarket llms.txt
endpoint index, data.binance.vision, Reservoir shutdown notices, IEEE DataPort record).*
