"""P27.34: outward-rounded interval enclosure filter for flux-root candidates.

The filter can certify exclusion of zero on an interval when a caller supplies
a valid interval extension of the original flux. Inclusion of zero is only
"unresolved": it does not prove existence of a root, especially for tangencies.
"""
from __future__ import annotations

import math


def _down(x):
    return math.nextafter(float(x), -math.inf)


def _up(x):
    return math.nextafter(float(x), math.inf)


class Interval:
    """Closed floating-point interval with one-step outward rounding."""

    __slots__ = ("lo", "hi")

    def __init__(self, lo, hi=None):
        lo = float(lo)
        hi = lo if hi is None else float(hi)
        if not (math.isfinite(lo) and math.isfinite(hi) and lo <= hi):
            raise ValueError("interval endpoints must be finite and ordered")
        self.lo, self.hi = lo, hi

    def __repr__(self):
        return f"Interval({self.lo!r}, {self.hi!r})"

    @staticmethod
    def _coerce(other):
        return other if isinstance(other, Interval) else Interval(other)

    def __add__(self, other):
        b = self._coerce(other)
        return Interval(_down(self.lo+b.lo), _up(self.hi+b.hi))

    __radd__ = __add__

    def __neg__(self):
        return Interval(_down(-self.hi), _up(-self.lo))

    def __sub__(self, other):
        return self + (-self._coerce(other))

    def __rsub__(self, other):
        return self._coerce(other) - self

    def __mul__(self, other):
        b = self._coerce(other)
        vals = (self.lo*b.lo, self.lo*b.hi, self.hi*b.lo, self.hi*b.hi)
        if not all(math.isfinite(v) for v in vals):
            raise ValueError("interval multiplication overflow")
        return Interval(_down(min(vals)), _up(max(vals)))

    __rmul__ = __mul__

    def reciprocal(self):
        if self.lo <= 0.0 <= self.hi:
            raise ZeroDivisionError("divisor interval contains zero")
        vals = (1.0/self.lo, 1.0/self.hi)
        return Interval(_down(min(vals)), _up(max(vals)))

    def __truediv__(self, other):
        return self * self._coerce(other).reciprocal()

    def __rtruediv__(self, other):
        return self._coerce(other) / self

    def square(self):
        if self.lo <= 0.0 <= self.hi:
            return Interval(0.0, _up(max(self.lo*self.lo, self.hi*self.hi)))
        vals = (self.lo*self.lo, self.hi*self.hi)
        return Interval(max(0.0, _down(min(vals))), _up(max(vals)))

    def contains_zero(self):
        return self.lo <= 0.0 <= self.hi


def enclose_flux(interval_flux, left, right):
    """Evaluate a caller-provided interval extension on [left, right]."""
    if not callable(interval_flux):
        raise ValueError("interval_flux must be callable")
    left, right = float(left), float(right)
    if not (math.isfinite(left) and math.isfinite(right) and left < right):
        raise ValueError("require finite left < right")
    result = interval_flux(Interval(left, right))
    if not isinstance(result, Interval):
        raise TypeError("interval_flux must return an Interval")
    return result


def classify_flux_interval(interval_flux, left, right):
    """Return certified exclusion or unresolved status for a candidate interval.

    Soundness is conditional on interval_flux being a mathematically valid
    enclosure of every pointwise flux value over the complete input interval.
    """
    enclosure = enclose_flux(interval_flux, left, right)
    if enclosure.contains_zero():
        status = "unresolved_zero_inclusion"
    else:
        status = "certified_zero_excluded"
    return {
        "interval_s": (float(left), float(right)),
        "flux_enclosure": (enclosure.lo, enclosure.hi),
        "status": status,
        "root_existence_proved": False,
        "assumption": "caller-supplied interval extension encloses the original flux",
    }
