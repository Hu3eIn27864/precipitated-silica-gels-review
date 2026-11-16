"""P27.43: independent exact-rational checker for interval certificates.

The checker treats every supplied finite endpoint as a binary64 value (using
Python's float conversion), interprets that value as its exact dyadic rational,
and recomputes the exact real range of the requested interval operation.
It then checks that the proposed finite binary64 result interval contains that
range. It does not trust the interval producer or its rounding algorithm.

This is a real-arithmetic enclosure checker, not a bit-level proof of IEEE-754,
not a proof that a producer evaluated the intended expression, and not a
physical validation of CCFSM.
"""
from __future__ import annotations

import math
from collections.abc import Mapping
from fractions import Fraction
from typing import Any


CERTIFICATE_SCHEMA = "ccfsm.interval-certificate.v1"
_REQUIRED_KEYS = {"schema", "operation", "lhs", "rhs", "result"}
_SUPPORTED_OPERATIONS = {"add", "mul", "div"}


class CertificateError(ValueError):
    """Raised when a certificate is malformed or outside the supported domain."""


def _binary64(value: Any, field: str) -> float:
    """Normalize a JSON-like numeric endpoint to one finite binary64 value."""
    if not isinstance(value, float):
        raise CertificateError(f"{field} must be a JSON floating-point number")
    try:
        result = float(value)
    except (OverflowError, ValueError) as exc:
        raise CertificateError(f"{field} cannot be represented as binary64") from exc
    if not math.isfinite(result):
        raise CertificateError(f"{field} must be finite")
    return result


def _interval(value: Any, field: str) -> tuple[float, float, Fraction, Fraction]:
    if not isinstance(value, (list, tuple)) or len(value) != 2:
        raise CertificateError(f"{field} must contain exactly [lower, upper]")
    lower = _binary64(value[0], f"{field}[0]")
    upper = _binary64(value[1], f"{field}[1]")
    if lower > upper:
        raise CertificateError(f"{field} endpoints must be ordered")
    return (
        lower,
        upper,
        Fraction.from_float(lower),
        Fraction.from_float(upper),
    )


def _fraction_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def _exact_range(
    operation: str,
    lhs: tuple[Fraction, Fraction],
    rhs: tuple[Fraction, Fraction],
) -> tuple[Fraction, Fraction]:
    a, b = lhs
    c, d = rhs
    if operation == "add":
        return a + c, b + d
    if operation == "div" and c <= 0 <= d:
        raise CertificateError("division denominator interval contains zero")
    if operation == "mul":
        corners = (a * c, a * d, b * c, b * d)
    elif operation == "div":
        corners = (a / c, a / d, b / c, b / d)
    else:
        raise CertificateError(f"unsupported operation: {operation}")
    return min(corners), max(corners)


def verify_interval_certificate(certificate: Mapping[str, Any]) -> dict[str, Any]:
    """Check a finite binary64 interval-operation certificate exactly.

    Required certificate shape:

        {
          "schema": "ccfsm.interval-certificate.v1",
          "operation": "add" | "mul" | "div",
          "lhs": [lower, upper],
          "rhs": [lower, upper],
          "result": [lower, upper]
        }

    Endpoints are normalized to binary64, then converted to exact dyadic
    Fractions. Malformed inputs raise CertificateError. A well-formed but
    unsound enclosure returns valid=false with exact discrepancy margins.
    """
    if not isinstance(certificate, Mapping):
        raise CertificateError("certificate must be a mapping/object")
    keys = set(certificate.keys())
    if not all(isinstance(key, str) for key in keys):
        raise CertificateError("certificate keys must be strings")
    if keys != _REQUIRED_KEYS:
        missing = sorted(_REQUIRED_KEYS - keys)
        extra = sorted(keys - _REQUIRED_KEYS)
        raise CertificateError(
            f"certificate keys mismatch; missing={missing}, extra={extra}"
        )
    if certificate["schema"] != CERTIFICATE_SCHEMA:
        raise CertificateError("unsupported certificate schema")

    operation = certificate["operation"]
    if not isinstance(operation, str) or operation not in _SUPPORTED_OPERATIONS:
        raise CertificateError(f"unsupported operation: {operation!r}")

    lhs = _interval(certificate["lhs"], "lhs")
    rhs = _interval(certificate["rhs"], "rhs")
    result = _interval(certificate["result"], "result")

    exact_lower, exact_upper = _exact_range(
        operation,
        (lhs[2], lhs[3]),
        (rhs[2], rhs[3]),
    )
    result_lower = Fraction.from_float(result[0])
    result_upper = Fraction.from_float(result[1])
    lower_margin = exact_lower - result_lower
    upper_margin = result_upper - exact_upper
    lower_ok = lower_margin >= 0
    upper_ok = upper_margin >= 0

    return {
        "schema": CERTIFICATE_SCHEMA,
        "valid": lower_ok and upper_ok,
        "operation": operation,
        "exact_lower": _fraction_text(exact_lower),
        "exact_upper": _fraction_text(exact_upper),
        "lower_margin": _fraction_text(lower_margin),
        "upper_margin": _fraction_text(upper_margin),
        "lower_enclosed": lower_ok,
        "upper_enclosed": upper_ok,
        "meaning": (
            "exact real range of the operation on the supplied binary64 "
            "endpoint intervals"
        ),
    }
