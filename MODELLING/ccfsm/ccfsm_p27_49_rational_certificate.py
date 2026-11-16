"""P27.49 exact-rational payload helpers for the Python/Lean bridge.

This module serializes the exact dyadic rationals represented by binary64
inputs. It does not certify a root-isolation claim; the Lean checker must
recompute every interval and sign condition.
"""
from __future__ import annotations

import json
import math
from fractions import Fraction
from typing import Any

SCHEMA = "ccfsm.root-isolation-certificate.v1"


def binary64_fraction(value: Any) -> Fraction:
    """Return the exact rational represented after binary64 conversion."""
    if isinstance(value, bool):
        raise ValueError("boolean is not a numeric coefficient")
    try:
        number = float(value)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("value must be convertible to finite binary64") from exc
    if not math.isfinite(number):
        raise ValueError("value must be finite")
    numerator, denominator = number.as_integer_ratio()
    return Fraction(numerator, denominator)


def rational_payload(value: Fraction) -> dict[str, str]:
    """Encode a rational canonically using decimal strings."""
    value = Fraction(value)
    return {"num": str(value.numerator), "den": str(value.denominator)}


def _canonical_integer_text(value: Any, field: str) -> int:
    if not isinstance(value, str):
        raise ValueError(f"{field} must be a decimal string")
    try:
        parsed = int(value, 10)
    except ValueError as exc:
        raise ValueError(f"{field} must be a decimal integer") from exc
    if str(parsed) != value:
        raise ValueError(f"{field} is not in canonical integer form")
    return parsed


def parse_rational_payload(payload: Any) -> Fraction:
    """Parse only reduced rationals with positive denominator."""
    if not isinstance(payload, dict) or set(payload) != {"num", "den"}:
        raise ValueError("rational must contain exactly num and den")
    numerator = _canonical_integer_text(payload["num"], "num")
    denominator = _canonical_integer_text(payload["den"], "den")
    if denominator <= 0:
        raise ValueError("denominator must be positive")
    value = Fraction(numerator, denominator)
    if value.numerator != numerator or value.denominator != denominator:
        raise ValueError("rational must be reduced; zero must be encoded as 0/1")
    return value


def descending_binary64_to_ascending_payload(coefficients: Any) -> list[dict[str, str]]:
    """Convert Python's descending-power binary64 coefficients to Lean order."""
    try:
        values = tuple(coefficients)
    except TypeError as exc:
        raise ValueError("coefficients must be iterable") from exc
    if not values:
        raise ValueError("at least one coefficient is required")
    exact = [binary64_fraction(value) for value in values]
    exact.reverse()
    return [rational_payload(value) for value in exact]


def polynomial_payload(coefficients: Any, left: Any, right: Any) -> dict[str, Any]:
    """Create the canonical Lean-facing polynomial/domain payload."""
    left_q = binary64_fraction(left)
    right_q = binary64_fraction(right)
    if not left_q < right_q:
        raise ValueError("require exact left < right")
    return {
        "schema": SCHEMA,
        "coefficient_order": "ascending_degree",
        "coefficients": descending_binary64_to_ascending_payload(coefficients),
        "domain": {
            "left": rational_payload(left_q),
            "right": rational_payload(right_q),
        },
    }


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def loads_certificate_json(source: str) -> dict[str, Any]:
    """Parse JSON while rejecting duplicate object keys and non-object roots."""
    try:
        value = json.loads(source, object_pairs_hook=_reject_duplicate_keys)
    except (json.JSONDecodeError, TypeError) as exc:
        raise ValueError("invalid certificate JSON") from exc
    if not isinstance(value, dict):
        raise ValueError("certificate root must be an object")
    return value


def validate_polynomial_payload(payload: Any) -> tuple[tuple[Fraction, ...], Fraction, Fraction]:
    """Validate the schema and return exact coefficients and interval bounds."""
    if not isinstance(payload, dict):
        raise ValueError("certificate must be an object")
    if payload.get("schema") != SCHEMA:
        raise ValueError("unknown certificate schema")
    if payload.get("coefficient_order") != "ascending_degree":
        raise ValueError("coefficient order must be ascending_degree")
    if set(payload) != {"schema", "coefficient_order", "coefficients", "domain"}:
        raise ValueError("unexpected or missing certificate fields")
    coefficients = payload["coefficients"]
    if not isinstance(coefficients, list) or not coefficients:
        raise ValueError("coefficients must be a nonempty list")
    exact_coefficients = tuple(parse_rational_payload(item) for item in coefficients)
    domain = payload["domain"]
    if not isinstance(domain, dict) or set(domain) != {"left", "right"}:
        raise ValueError("domain must contain exactly left and right")
    left = parse_rational_payload(domain["left"])
    right = parse_rational_payload(domain["right"])
    if not left < right:
        raise ValueError("require exact left < right")
    return exact_coefficients, left, right
