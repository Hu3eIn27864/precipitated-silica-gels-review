"""P27.26: independent manufactured-reference checks for P27.25.

The routines here deliberately do not call the P27.25 reconstruction code.
They provide exact polynomial references and a generic trapezoidal comparator
for synthetic time histories; they are verification helpers, not a physical
model or a proof of solver-level energy closure.
"""
from __future__ import annotations

import math


def _finite(value, name):
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(name + " must be finite")
    return value


def polynomial_integral(coefficients, t0, t1):
    """Exact integral of sum(c[k] * t**k) over [t0, t1]."""
    a, b = _finite(t0, "t0"), _finite(t1, "t1")
    if b <= a:
        raise ValueError("t1 must exceed t0")
    coeffs = tuple(_finite(c, "coefficient") for c in coefficients)
    if not coeffs:
        raise ValueError("at least one polynomial coefficient is required")
    return sum(c * (b ** (k + 1) - a ** (k + 1)) / (k + 1)
               for k, c in enumerate(coeffs))


def trapezoid_samples(times, values):
    """Composite trapezoid integral of supplied samples on a strict time grid."""
    ts = tuple(_finite(t, "time") for t in times)
    ys = tuple(_finite(y, "value") for y in values)
    if len(ts) < 2 or len(ts) != len(ys):
        raise ValueError("times and values need equal length >= 2")
    if any(ts[i + 1] <= ts[i] for i in range(len(ts) - 1)):
        raise ValueError("times must be strictly increasing")
    return sum(0.5 * (ys[i] + ys[i + 1]) * (ts[i + 1] - ts[i])
               for i in range(len(ts) - 1))


def manufactured_quadrature_report(coefficients, t0, t1, subdivisions):
    """Compare composite trapezoid against an exact polynomial integral."""
    n = int(subdivisions)
    if n < 1 or n != subdivisions:
        raise ValueError("subdivisions must be a positive integer")
    a, b = _finite(t0, "t0"), _finite(t1, "t1")
    exact = polynomial_integral(coefficients, a, b)
    times = tuple(a + (b - a) * i / n for i in range(n + 1))
    values = tuple(sum(float(c) * t ** k for k, c in enumerate(coefficients))
                   for t in times)
    approx = trapezoid_samples(times, values)
    return {"exact_integral": exact, "trapezoid_integral": approx,
            "absolute_error": abs(approx - exact),
            "subdivisions": n, "order_claimed": None,
            "interpretation": "manufactured quadrature error only"}
