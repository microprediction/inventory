# Correction package: skew_width_imbalance (2026-08-12)

## What was wrong

The submitted Theorem 1 stated the compression as: balanced problem at carrying
cost M(q)c, "under the correspondence: skew translated by δ, AND
non-discretionary width Δ widened to Δ + γ." The widening and the multiplier
are the same factor e^{hγ} read in two frames (overhead frame vs cost frame),
not simultaneous corrections; the submitted proof itself moves the factor to
the cost side, after which nothing remains to widen. Corollary 2 and §6 then
treated γ as the physical, parameter-free width response, which is incorrect.

Numerical demonstration (verify_width_response.py, run at the submitted
certificate's own configuration): the imbalanced dealer's half-width equals
the balanced-at-M(q)c dealer's at every inventory to 4e-16; her width response
over the balanced-at-c dealer is 1.3e-3 at q = 0.6, versus γ = 2.0e-2.

The proof of Theorem 1 and the submitted certificate
(verify_local_exponentiality.py) are unaffected: both operate in the cost
frame only, and the ν-level equivalence they establish is correct. All skew
results (δ, zero-inventory skew, sign flip, first-order vs second-order) are
unaffected. M(q) as an effective-carry multiplier is unaffected.

## What replaces it

The width response flows entirely through the multiplied carry: the imbalanced
quotes are those of the balanced dealer at cost M(q)c, so the response is that
problem's convexity response to a proportional carry increase. In the
small-skew quadratic-cost regime this has the closed leading-order form

    ΔC(0) = γ · hC(0) / (2 − hC(0)) + O((q − 1/2)^4),

from d C0 / d log(cost scale) = C0/(2 − hC0). The even, sign-definite γ-shape
in the imbalance survives; the coefficient is roughly half the ratio of
discretionary to market width, so the response involves one further observable,
the quoted discretionary width C(0), rather than being pinned by w alone.
Verified within ~1% across q ∈ [0.55, 0.70] on the lattice, at two different
cost configurations.

For empirical work this sharpens rather than weakens the test: a regression of
the width response on 2(q − 1/2)^2 should find slope ≈ C(0), not 2w — a more
distinctive fingerprint of the carry channel.

## Changes to the manuscript (7 edits)

1. Abstract: "translation ... widening ... multiplication" list replaced by
   "translation together with a multiplication of effective carry —
   equivalently, at unchanged cost, a widening of the overhead: one correction
   read in two frames."
2. Introduction: same fix to the corresponding sentence.
3. Theorem 1: correspondence is the skew translation; the widening stated as
   the equivalent unchanged-cost frame, with the explicit warning that the two
   are not simultaneous.
4. Remark after Theorem 1: "translated by δ and evaluated at cost M(q)c —
   equivalently, at overhead widened by γ."
5. Corollary 2 (orders): interpretation rewritten; width response identified
   as the convexity response with pointer to the new equation; "no parameter
   beyond w" now claimed for the skew only.
6. New paragraph + equation (widthresponse) in Section 5 deriving the closed
   form, with the certificate reference.
7. §6 Uses / testing: the width prediction restated via the new formula with
   C(0) as the further observable; "widened ... through the carry channel,
   proportional to the discretionary width rather than the market width."

New file: verify_width_response.py (certificate for both corrected claims).

## Suggested venues for the correction

- SIFIN: send corrected manuscript to the handling editor now (draft note in
  editor_note.txt), or hold for the referee-response round.
- arXiv: post v2 when convenient; keep v1 as the record of the submitted text.
- SSRN: upload revision.

Downstream repo items (not in this package): notes/spread_as_endogenous_carry
H7 and papers/skew_width_imbalance/data_scout_imbalance.md width tests inherit
the same correction; tracked in revision_notes.md §5.
