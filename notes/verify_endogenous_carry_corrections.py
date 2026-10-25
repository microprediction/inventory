#!/usr/bin/env python3
"""Regression checks for notes/spread_as_endogenous_carry.tex.

The checks use only the Python standard library and isolate the three exact
claims corrected in the note: the imbalance factorisation, the zero-cost
case, and compatibility of the two finite differences of one potential.
"""

from math import acosh, cosh, exp, isclose, log, sqrt


def assert_close(actual: float, expected: float, *, tol: float = 2e-14) -> None:
    if not isclose(actual, expected, rel_tol=tol, abs_tol=tol):
        raise AssertionError(f"{actual:.17g} != {expected:.17g}")


def check_imbalance_identity() -> None:
    for p in (0.2, 0.35, 0.5, 0.65, 0.8):
        for h in (0.4, 1.0, 2.3):
            delta = log(p / (1.0 - p)) / (2.0 * h)
            D = 2.0 * sqrt(p * (1.0 - p))
            for S in (-1.2, -0.1, 0.0, 0.7, 1.4):
                lhs = p * exp(-h * S) + (1.0 - p) * exp(h * S)
                rhs = D * cosh(h * (S - delta))
                assert_close(lhs, rhs)

    # The former sign fails decisively under the note's seller-probability
    # convention: at p=.8, h=1, S=delta the exact mixture is .8, not 1.7.
    p, h = 0.8, 1.0
    delta = log(p / (1.0 - p)) / (2.0 * h)
    wrong_delta = -delta
    lhs = p * exp(-h * delta) + (1.0 - p) * exp(h * delta)
    wrong_rhs = 2.0 * sqrt(p * (1.0 - p)) * cosh(h * (delta - wrong_delta))
    assert_close(lhs, 0.8)
    assert_close(wrong_rhs, 1.7)


def check_clock_and_zero_cost() -> None:
    for p in (0.1, 0.3, 0.5, 0.7, 0.9):
        D = 2.0 * sqrt(p * (1.0 - p))
        M = 1.0 / D
        assert_close(M * D, 1.0)
        assert_close(M * 0.0, 0.0)


def check_potential_compatibility() -> None:
    # For nu(j)=C0*j^2 at unit spacing, C(j)=C0 and S(j)=2*C0*j.
    C0 = 0.17
    nu = {j: C0 * j * j for j in range(-5, 6)}

    def S(j: int) -> float:
        return (nu[j + 1] - nu[j - 1]) / 2.0

    def C(j: int) -> float:
        return (nu[j + 1] - 2.0 * nu[j] + nu[j - 1]) / 2.0

    for j in range(-3, 4):
        assert_close(C(j), C0)
        assert_close(S(j + 1) - S(j), C(j + 1) + C(j))
        assert_close(S(j), 2.0 * C0 * j)

    # Constant C therefore makes the Bellman-compatible centered cost
    # proportional to cosh(h*S)-1, not exactly quadratic away from zero.
    h = 1.0
    c1 = cosh(h * S(1)) - 1.0
    c2 = cosh(h * S(2)) - 1.0
    if isclose(c2, 4.0 * c1, rel_tol=1e-6, abs_tol=1e-12):
        raise AssertionError("cosh-shaped compatible cost was exactly quadratic")

    # Pointwise inversion supplies only |S| and so cannot choose the branch.
    magnitude = acosh(1.0 + c1) / h
    assert_close(magnitude, abs(S(1)))
    assert_close(cosh(h * magnitude), cosh(-h * magnitude))


if __name__ == "__main__":
    check_imbalance_identity()
    check_clock_and_zero_cost()
    check_potential_compatibility()
    print("PASS: imbalance, zero-cost, and potential-compatibility checks")
