# Parked ideas

Things worth returning to that we are deliberately not pursuing yet, to avoid crossing too many streams at once.

## Coupling from the past (Propp–Wilson) for the storage equilibrium

The general-equilibrium storage model defines a Markov chain in the coverage state, and the object of empirical interest is its stationary law (price distribution, spike frequency, hoard duration). Three reasons CFTP might earn its keep here rather than being a gimmick:

1. **The interesting regime is exactly where naive simulation is worst.** Near the explosiveness boundary the chain is near-unit-root, mixing is slow, and burn-in bias is severe. Perfect sampling sidesteps burn-in entirely.
2. **The regime structure supplies the bounding chains.** Monotone CFTP needs a partially ordered state space with extremal states; the stockout floor ($Y=0$) and the financing/capital ceiling on speculative positions are natural bottom and top processes. Classical competitive-storage transition maps are monotone in the stock, which is the condition monotone CFTP needs. Caveat to check: with the extrapolative anchor in the state (trend variable), monotonicity of the full map is not obvious and may fail.
3. **Coalescence time as a stability diagnostic.** If the system is genuinely explosive absent the capital ceiling, CFTP fails informatively: expected coalescence time diverges as $k \to 0$ or extrapolation gain $\beta$ rises. Time-to-coalesce is then a computable distance-to-instability — a numerical probe of the stability boundary in §5 of `formulation.md` that doesn't require linearisation.

Status: parked. Revisit when the simulator (work item 2 in `formulation.md` §8) exists, since the same transition kernel serves both.
