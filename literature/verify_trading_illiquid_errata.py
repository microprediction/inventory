"""Reproduce the corrections in trading_illiquid_errata.md (stdlib only)."""

from math import erf, exp, pi, sqrt


def normal_cdf(x):
    return 0.5 * (1.0 + erf(x / sqrt(2.0)))


def normal_pdf(x):
    return exp(-0.5 * x * x) / sqrt(2.0 * pi)


def unbounded_payoff(t, b):
    return exp(-b + 0.5 * t * t) * (1.0 + b - t * t)


def clipped_quote_payoff(t, b):
    """E[Y exp(1-Y) 1{Y>=0}] for Y~N(1+b,t^2)."""
    d = (1.0 + b - t * t) / t
    return exp(-b + 0.5 * t * t) * (
        (1.0 + b - t * t) * normal_cdf(d) + t * normal_pdf(d)
    )


def main():
    # Slides 24--25: a fully interior numerical instance.
    eps = 0.15
    k_up, k_down = 0.45, 0.05
    slope = (k_up - k_down) / 2.0
    convexity = (k_up + k_down) / 2.0 - eps
    assert abs(slope - 0.2) < 1e-15
    assert abs(convexity - 0.1) < 1e-15
    assert abs((1 + eps + convexity + slope) - 1.45) < 1e-15
    assert abs((1 + eps + convexity - slope) - 1.05) < 1e-15

    # Slides 36 and 38: nu(x)=x^2 at s=x=C0=1 has centered slope 2.
    centered_slope = ((1 + 1) ** 2 - (1 - 1) ** 2) / 2.0
    assert centered_slope == 2.0

    # Slide 49: its two curves are the unbounded Gaussian expectations.
    t = 1.0
    assert abs(unbounded_payoff(t, 0.0) - 0.0) < 1e-15
    assert abs(unbounded_payoff(t, t * t) - exp(-0.5)) < 1e-15

    # Enforcing the nonnegative submitted-quote boundary changes both curves
    # and makes the unbounded optimizer b=t^2 suboptimal.
    red_clipped = clipped_quote_payoff(t, 0.0)
    blue_clipped = clipped_quote_payoff(t, 1.0)
    better_b, better = 0.48106, clipped_quote_payoff(t, 0.48106)
    assert abs(red_clipped - 0.657744623479457) < 1e-14
    assert abs(blue_clipped - 0.6570640470524514) < 1e-14
    assert abs(better - 0.6978566255362583) < 1e-10
    assert better > blue_clipped + 0.04

    print("PASS: slides 24--25 quote identities")
    print("PASS: slides 36/38 factor-four correction")
    print(
        "PASS: slide 49 boundary: "
        f"red {red_clipped:.7f}, blue {blue_clipped:.7f}, "
        f"b={better_b:.5f} gives {better:.7f}"
    )


if __name__ == "__main__":
    main()
