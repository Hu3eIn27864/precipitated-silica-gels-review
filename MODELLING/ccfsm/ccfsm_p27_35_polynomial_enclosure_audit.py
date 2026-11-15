"""P27.35: independent polynomial enclosure checks for P27.34.

Horner evaluation provides a reproducible interval extension for polynomials.
The interval result is compared against dense point evaluations of manufactured
polynomials. Dense sampling is a regression check, not a mathematical proof;
the proof obligation is the interval arithmetic contract and Horner enclosure.
"""
from __future__ import annotations

from ccfsm_p27_34_interval_flux_filter import Interval, classify_flux_interval


def polynomial_interval(coefficients, domain):
    """Enclose a polynomial on domain; coefficients are highest degree first."""
    if not isinstance(domain, Interval):
        raise TypeError("domain must be an Interval")
    coeffs = tuple(float(c) for c in coefficients)
    if not coeffs:
        raise ValueError("at least one coefficient is required")
    import math
    if not all(math.isfinite(c) for c in coeffs):
        raise ValueError("coefficients must be finite")
    value = Interval(coeffs[0])
    for coefficient in coeffs[1:]:
        value = value * domain + coefficient
    return value


def classify_polynomial_interval(coefficients, left, right):
    """Apply the P27.34 zero-exclusion filter to a polynomial."""
    return classify_flux_interval(
        lambda domain: polynomial_interval(coefficients, domain), left, right
    )
