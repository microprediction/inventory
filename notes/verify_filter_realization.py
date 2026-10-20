"""Regression checks for filter_realization.md; Python standard library only."""

from fractions import Fraction
from math import exp


def exact_rank(matrix):
    """Row reduction without floating-point rank thresholds."""
    a = [list(row) for row in matrix]
    rank = 0
    for col in range(len(a[0])):
        pivot = next((i for i in range(rank, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        v = a[rank][col]
        a[rank] = [x / v for x in a[rank]]
        for i in range(rank + 1, len(a)):
            v = a[i][col]
            a[i] = [x - v * y for x, y in zip(a[i], a[rank])]
        rank += 1
    return rank


def sensor(x):
    return 1 / (1 + x)


def posterior_mean(points, weights, observed, sigma):
    masses = [w * exp(-0.5 * ((observed - sensor(x)) / sigma) ** 2)
              for x, w in zip(points, weights)]
    return sum(x * w for x, w in zip(points, masses)) / sum(masses)


def main():
    # Subtract values at theta=0 to remove constants exactly.  Full rank
    # proves independence on these grids, hence of the sampled functions.
    # The accompanying pole proof handles arbitrary history length.
    for n in range(1, 9):
        points = [Fraction(j, n) for j in range(1, n + 1)]
        matrix = [[sensor(theta / (2 ** k)) - 1
                   for k in range(1, n + 1)] for theta in points]
        assert exact_rank(matrix) == n
        print(f'PASS: {n} posterior score directions independent modulo constants')

    mean_a = posterior_mean([0.5], [1.0], 1.0, 0.2)
    mean_b = posterior_mean([0.0, 1.0], [0.5, 0.5], 1.0, 0.2)
    expected_b = exp(-25 / 8) / (1 + exp(-25 / 8))
    assert abs(mean_a - 0.5) < 1e-15
    assert abs(mean_b - expected_b) < 1e-15
    assert abs(mean_a - mean_b) > 0.45

    # Their pre-observation conditional-mean forecasts are identical at
    # every horizon, not just at the current time.
    for h in (0, 1, 2, 8, 32):
        curve_a = 0.5 / (2 ** h)
        curve_b = sum(x * w for x, w in zip([0.0, 1.0], [0.5, 0.5])) / (2 ** h)
        assert curve_a == curve_b
    print(f'PASS: identical forecast curves, different updates: {mean_a} vs {mean_b}')


if __name__ == '__main__':
    main()
