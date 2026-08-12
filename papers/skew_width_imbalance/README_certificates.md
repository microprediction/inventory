# Certificate suite for "skew_width_imbalance"

Eight scripts, layered by epistemic strength. Dependencies: numpy, scipy,
sympy, mpmath (all standard); humpday is optional (verify_optimality
falls back to scipy differential evolution without it).

Run any script with `python3 <name>.py`; each prints PASS/FAIL per check
and exits nonzero on failure.

## The ladder

1. **verify_symbolic.py** (~5 s) -- every purely algebraic identity in
   the paper reduced to zero EXACTLY in sympy under the log-odds
   parameterization q = e^t/(e^t + e^-t). No floating point. 12 checks.

2. **verify_interval.py** (~3 min) -- validated numerics. A Krawczyk
   interval-Newton certificate with outward-rounded arithmetic (mpmath.iv)
   proves existence, local uniqueness, and interiority of the consistency
   solution and its balanced image at the flagship configuration
   (q = 0.6, c = 0.0015 x^2, N = 8, eps = 0.15), then, by tiling
   q in [0.55, 0.605] into 220 slabs and running the operator with q as
   an interval parameter (mean-value form), proves the same for EVERY q
   in that range. These are machine-checked theorems, not observations.
   6 checks.

3. **verify_optimality.py** (~2 min) -- the consistency solution is the
   average-reward OPTIMUM of the finite MDP, attacked with competitors
   that never see nu: an exact policy-iteration fixed point (Howard
   certificate, proof-strength on the finite lattice), a derivative-free
   search racing the full humpday roster over the raw 16-dimensional
   quote vector, thousands of random perturbations, an 8-configuration
   sweep, the zero-carry selection question, the floor-binding regime
   where the theorem map fails, the interior-spike counterexample, and a
   150-draw fuzz over random admissible configurations. 14 checks.

4. **verify_diagrams.py** (~30 s) -- every commutative diagram of the
   symmetry certified from DIRECTLY OPTIMIZED strategies only: all four
   corners (imbalanced, balanced-at-Mc, overhead-frame, parity image)
   are obtained by exact policy iteration from flat cold starts, never
   from the consistency solver, and the tilt square, time-change
   diagram, overhead square (equal gain; overhead width = physical
   width + 2 gamma), and parity square commute between the independent
   optima at 1e-15. The CWLS corner and flat-book skew are certified as
   optimality statements the same way. 6 checks.

5. **verify_all_claims.py** (~1 min) -- claim-by-claim floating-point
   battery keyed to paper sections (model, symmetry, CWLS, uses,
   hardening), including deliberate failure cases showing where
   exactness breaks once quotes clip. Every configuration asserts the
   interior-quote assumption rather than assuming it. 38 checks.

6. **verify_width_response.py** (~10 s) -- the two-frames statement
   (imbalanced width = balanced-at-Mc width, exactly) and the closed
   width-response formula gamma hC0/(2 - hC0), verified to ~1 percent
   across q in [0.55, 0.7].

7. **verify_moving_price.py** (~1 min) -- the moving-price equivalence
   behind Remark 2: cash P&L decomposes pathwise into model P&L plus the
   inventory-weighted price increment, whose time average vanishes at
   the root-T rate and whose presence changes no policy comparison
   (checked for optimal and suboptimal policies alike); by Ito isometry
   its variance is sigma^2 T E[x^2], so a mean-variance dealer's price
   risk in the moving frame is exactly the quadratic carrying cost.
   4 checks.

8. **verify_local_exponentiality.py** (~10 s) -- the local-exponentiality
   remark: skew error scales linearly with the hazard's relative
   variation across visited strikes.

## Scope

The suite certifies identities, implementations, and finite-lattice
optimality, and PROVES existence, local uniqueness, and interiority on
the stated q-interval at the certificate cost. It does not establish
global uniqueness over the whole interior region, unbounded-lattice
behavior, or asymptotic statements; the manuscript scopes those
explicitly as assumptions or approximations.
