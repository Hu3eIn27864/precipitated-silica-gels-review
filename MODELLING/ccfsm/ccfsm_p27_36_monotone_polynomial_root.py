"""P27.36: derivative-sign root isolation for polynomial event candidates.

A root is classified as unique only when an outward-rounded interval enclosure
of the derivative has a strict sign on the full interval and endpoint
polynomial enclosures have opposite strict signs. The conclusion is conditional
on the interval-arithmetic enclosure contract inherited from P27.34/P27.35.
"""
from __future__ import annotations

import math

from ccfsm_p27_34_interval_flux_filter import Interval
from ccfsm_p27_35_polynomial_enclosure_audit import polynomial_interval


def polynomial_derivative_coefficients(coefficients):
    """Return derivative coefficients in descending-power order."""
    coeffs = tuple(float(c) for c in coefficients)
    if not coeffs:
        raise ValueError("at least one coefficient is required")
    if not all(math.isfinite(c) for c in coeffs):
        raise ValueError("coefficients must be finite")
    degree = len(coeffs) - 1
    if degree == 0:
        return (0.0,)
    return tuple((degree - i) * c for i, c in enumerate(coeffs[:-1]))


def classify_monotone_polynomial_root(coefficients, left, right):
    """Classify roots using a derivative enclosure and strict endpoint signs.

    Returns certified_unique_root when the derivative enclosure excludes zero
    and endpoint enclosures have opposite signs; certified_no_root when the
    derivative has a strict sign and endpoint signs agree. All other cases
    remain unresolved. Endpoint roots are deliberately not included.
    """
    left, right = float(left), float(right)
    if not (math.isfinite(left) and math.isfinite(right) and left < right):
        raise ValueError("require finite left < right")

    coeffs = tuple(float(c) for c in coefficients)
    if not coeffs:
        raise ValueError("at least one coefficient is required")
    if not all(math.isfinite(c) for c in coeffs):
        raise ValueError("coefficients must be finite")

    derivative = polynomial_derivative_coefficients(coeffs)
    derivative_enclosure = polynomial_interval(
        derivative, Interval(left, right)
    )
    if derivative_enclosure.lo > 0.0:
        monotonicity = "strictly_increasing"
    elif derivative_enclosure.hi < 0.0:
        monotonicity = "strictly_decreasing"
    else:
        return {
            "status": "unresolved_derivative_contains_zero",
            "root_count": None,
            "derivative_enclosure": (derivative_enclosure.lo, derivative_enclosure.hi),
            "endpoint_enclosures": None,
            "monotonicity": "unresolved",
        }

    left_value = polynomial_interval(coeffs, Interval(left))
    right_value = polynomial_interval(coeffs, Interval(right))

    def strict_sign(interval):
        if interval.lo > 0.0:
            return 1
        if interval.hi < 0.0:
            return -1
        return 0

    left_sign = strict_sign(left_value)
    right_sign = strict_sign(right_value)
    endpoint_data = (
        (left_value.lo, left_value.hi),
        (right_value.lo, right_value.hi),
    )
    if left_sign == 0 or right_sign == 0:
        status, count = "unresolved_endpoint_sign", None
    elif left_sign != right_sign:
        status, count = "certified_unique_root", 1
    else:
        status, count = "certified_no_root", 0

    return {
        "status": status,
        "root_count": count,
        "derivative_enclosure": (derivative_enclosure.lo, derivative_enclosure.hi),
        "endpoint_enclosures": endpoint_data,
        "monotonicity": monotonicity,
        "assumption": "outward-rounded interval extensions enclose polynomial and derivative",
    }
