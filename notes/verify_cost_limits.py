"""Regression checks for the LQ limits discussed in formulation.md.

Uses only closed-form scalar Riccati solutions and the standard library.
"""

from math import isclose, sqrt


def integrator_gain(k: float, r: float) -> float:
    """Optimal feedback magnitude for x_dot = u, cost int(k*x^2+r*u^2)."""
    return sqrt(k / r)


def stable_plant_solution(k: float, r: float) -> tuple[float, float, float]:
    """Return (P, gain, closed-loop pole) for x_dot = -x + u."""
    p = r * (-1.0 + sqrt(1.0 + k / r))
    gain = p / r
    return p, gain, -1.0 - gain


def main() -> None:
    # Vanishing state weight: slower regulation, not a boundary layer.
    state_gains = [integrator_gain(k, 1.0) for k in (1.0, 0.01, 0.0001)]
    assert all(isclose(a, b) for a, b in zip(state_gains, (1.0, 0.1, 0.01)))
    assert all(isclose(1.0 / g, t) for g, t in zip(state_gains, (1.0, 10.0, 100.0)))

    # Classical cheap control: vanishing input weight and diverging gain.
    control_gains = [integrator_gain(1.0, r) for r in (1.0, 0.01, 0.0001)]
    assert all(isclose(a, b) for a, b in zip(control_gains, (1.0, 10.0, 100.0)))

    # Stable uncontrolled dynamics are a counterexample to inevitable explosion.
    stable = [stable_plant_solution(k, 1.0) for k in (1.0, 0.01, 0.0001, 0.0)]
    assert all(p >= 0.0 and gain >= 0.0 and pole <= -1.0 for p, gain, pole in stable)
    assert stable[-1] == (0.0, 0.0, -1.0)

    # At a static equilibrium u=x, (k+r)x^2 still has the unique minimum x=0
    # when k=0 and r>0; a static optimizer need not escape to infinity.
    r = 1.0
    assert all((0.0 + r) * x * x > 0.0 for x in (-2.0, -1.0, 1.0, 2.0))

    print("PASS: state-cost, cheap-control, and stable-plant limits")


if __name__ == "__main__":
    main()
