"""P27.37: adaptive subdivision for polynomial root isolation.

Each leaf interval is classified by P27.36. Subdivision continues only while
the leaf is unresolved and depth/width limits permit. Certified claims remain
conditional on the outward-rounded interval enclosure contract.
"""
from __future__ import annotations

import math

from ccfsm_p27_36_monotone_polynomial_root import (
    classify_monotone_polynomial_root,
)


def isolate_polynomial_roots(
    coefficients, left, right, *, max_depth=12, min_width=1.0e-8
):
    """Partition an interval into certified and unresolved polynomial leaves.

    The returned unique-root leaves each contain exactly one interior root;
    no-root leaves contain none. Unresolved leaves are not counted as roots.
    The aggregate upper bound is None whenever any unresolved leaf remains.
    """
    coeffs = tuple(float(c) for c in coefficients)
    if not coeffs or not all(math.isfinite(c) for c in coeffs):
        raise ValueError("coefficients must be nonempty and finite")

    left, right = float(left), float(right)
    if not (math.isfinite(left) and math.isfinite(right) and left < right):
        raise ValueError("require finite left < right")
    if isinstance(max_depth, bool) or not isinstance(max_depth, int) or max_depth < 0:
        raise ValueError("max_depth must be a nonnegative integer")
    min_width = float(min_width)
    if not math.isfinite(min_width) or min_width <= 0.0:
        raise ValueError("min_width must be finite and positive")

    leaves = []

    def visit(a, b, depth):
        result = classify_monotone_polynomial_root(coeffs, a, b)
        status = result["status"]
        width = b - a
        if status in ("certified_unique_root", "certified_no_root"):
            leaves.append({
                "interval": (a, b),
                "status": status,
                "root_count": result["root_count"],
                "depth": depth,
                "monotonicity": result.get("monotonicity"),
            })
            return

        if depth >= max_depth or width <= min_width:
            leaves.append({
                "interval": (a, b),
                "status": "unresolved_subdivision_limit",
                "root_count": None,
                "depth": depth,
                "reason": status,
            })
            return

        midpoint = a + 0.5 * width
        if not (a < midpoint < b):
            leaves.append({
                "interval": (a, b),
                "status": "unresolved_floating_point_resolution",
                "root_count": None,
                "depth": depth,
                "reason": status,
            })
            return
        visit(a, midpoint, depth + 1)
        visit(midpoint, b, depth + 1)

    visit(left, right, 0)
    unique_count = sum(
        leaf["root_count"] for leaf in leaves
        if leaf["status"] == "certified_unique_root"
    )
    has_unresolved = any(
        leaf["root_count"] is None for leaf in leaves
    )
    no_root_count = sum(
        leaf["root_count"] for leaf in leaves
        if leaf["status"] == "certified_no_root"
    )
    return {
        "domain": (left, right),
        "leaves": leaves,
        "certified_unique_root_count": unique_count,
        "certified_no_root_leaf_count": no_root_count,
        "unresolved_leaf_count": sum(leaf["root_count"] is None for leaf in leaves),
        "root_count_bounds": (unique_count, None if has_unresolved else unique_count),
        "complete": not has_unresolved,
        "assumption": "P27.36 interval-enclosure contract holds for polynomial and derivative",
    }
