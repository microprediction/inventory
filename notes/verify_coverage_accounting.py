"""Exact-form and finite-difference checks for formulation.md equation (2).

Run with python3 notes/verify_coverage_accounting.py (stdlib only).
This checks accounting identities, not the proposed economic closure.
"""

from math import exp, isclose, log


def check_growing_consumption():
    # I(h)=exp(-h), q(h)=exp(h), d(h)=exp(-h).
    # Supply=q-d is nonnegative for h>=0, and inventory remains positive.
    step = 1e-5
    for h in (0.0, 0.25, log(2.0), 2.0):
        inventory, consumption, deficit = exp(-h), exp(h), exp(-h)
        coverage = inventory / consumption
        exact = -2.0 * coverage
        corrected = -deficit / consumption - coverage
        difference = (exp(-2.0 * (h + step)) - exp(-2.0 * (h - step))) / (2.0 * step)
        assert consumption - deficit >= 0.0
        assert inventory > 0.0
        assert isclose(corrected, exact, abs_tol=1e-14)
        assert isclose(difference, exact, rel_tol=1e-8, abs_tol=1e-10)

    h = log(2.0)
    old = -exp(-h) - exp(-2.0 * h)  # Incorrectly divide by q(0)=1.
    exact = -2.0 * exp(-2.0 * h)
    assert isclose(old, -0.75, abs_tol=1e-14)
    assert isclose(exact, -0.5, abs_tol=1e-14)
    assert abs(old - exact) > 0.2
    print(f"Growing consumption at h=log(2): old={old}, corrected={exact}")


def check_constant_consumption():
    # I(h)=exp(-h), q(h)=2, d(h)=exp(-h), supply=2-d>=0.
    for h in (0.0, 0.25, 1.0, 2.0):
        exact = -exp(-h) / 2.0
        corrected = -exp(-h) / 2.0  # g=0, future q=current q=2.
        assert isclose(corrected, exact, abs_tol=1e-14)
        step = 1e-5
        difference = (exp(-(h + step)) - exp(-(h - step))) / (4.0 * step)
        assert isclose(difference, exact, rel_tol=1e-8, abs_tol=1e-10)
    print("Constant consumption: the D/q(0) special case holds.")


def check_ratio_of_expectations():
    # Two equally likely future states: E[d/q] != E[d]/E[q].
    deficits, consumption = (1.0, 3.0), (1.0, 2.0)
    expectation_of_ratio = sum(d / q for d, q in zip(deficits, consumption)) / 2.0
    ratio_of_expectations = sum(deficits) / sum(consumption)
    assert isclose(expectation_of_ratio, 1.25, abs_tol=1e-14)
    assert isclose(ratio_of_expectations, 4.0 / 3.0, abs_tol=1e-14)
    assert not isclose(expectation_of_ratio, ratio_of_expectations)
    print("Random consumption: E[d/q]=1.25 != E[d]/E[q]=4/3.")


if __name__ == "__main__":
    check_growing_consumption()
    check_constant_consumption()
    check_ratio_of_expectations()
    print("PASS: coverage slopes use future consumption and conditional joint moments.")
