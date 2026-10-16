"""Check the bounded forecast-curve counterexample in formulation.md.

No Monte Carlo or optional dependencies: use the Jacobi diffusion's exact
first two conditional moments, and the generator applied to log price.
The checks illustrate the derivation; they do not certify a general model.
"""

from math import exp, expm1


def f(z):
    """Storage curve f(2+z), increasing and concave for -1 <= z <= 1."""
    return 3 * z - z * z


def log_price(z):
    return -3 * z + z * z / 2  # constant log anchor set to zero


def generator(z):
    return (-z) * (-3 + z) + (1 - z * z) / 2


def expected_log_price_increment(z, t):
    # E[Z_t] = exp(-t) z; d E[Z_t^2]/dt = 1 - 3 E[Z_t^2].
    # expm1 avoids cancellation when checking the short-time drift.
    return -3 * z * expm1(-t) + (1 / 3 - z * z) * (-expm1(-3 * t)) / 2


for z in [-1, -0.5, 0, 0.5, 1]:
    corrected = f(z) + (1 - z * z) / 2
    assert abs(generator(z) - corrected) < 1e-14
    dt = 1e-6
    short_time_drift = expected_log_price_increment(z, dt) / dt
    assert abs(short_time_drift - corrected) < 1e-5
    print(f"z={z:+.1f}: generator={corrected:+.6f}, "
          f"conditional-moment drift={short_time_drift:+.6f}")

# At z=0 the correction is 1/2, whereas the uncorrected drift is zero.
assert f(0) == 0 and generator(0) == 0.5

# Required anchor drift = 1/2 int_h^infty f''(Y_s) v(s) ds,
# where f'' = -2 and v(s) = exp(-2s)(1-z^2).
required = [-exp(-2 * h) / 2 for h in [0, 1, 2]]
assert len(set(required)) == 3
print("Required scalar anchor drift at horizons 0,1,2:", required)
print("PASS: the corrected spot drift holds; one scalar anchor cannot "
      "make the mean-coverage curve tower-consistent at every horizon.")
