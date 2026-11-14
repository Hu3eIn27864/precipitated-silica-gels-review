"""Minimal P1 bridge-fraction closure used by the CCFSM specification.

This module is a mathematical reference implementation, not a calibrated
constitutive law for precipitated silica.  The mobility interpolation is
only admissible when both endpoint mobilities are positive.
"""
from __future__ import annotations

import math


def bridge_fraction(t: float, b0: float, b_eq: float, k_b: float) -> float:
    """Exact solution of db/dt = k_b * (b_eq - b).

    The normalized bridge fraction and its equilibrium value must lie in
    [0, 1], time must be nonnegative, and k_b must be positive.
    """
    values = (t, b0, b_eq, k_b)
    if not all(math.isfinite(value) for value in values):
        raise ValueError("all inputs must be finite")
    if t < 0:
        raise ValueError("t must be nonnegative")
    if not 0.0 <= b0 <= 1.0:
        raise ValueError("b0 must lie in [0, 1]")
    if not 0.0 <= b_eq <= 1.0:
        raise ValueError("b_eq must lie in [0, 1]")
    if k_b <= 0:
        raise ValueError("k_b must be positive")
    return b_eq + (b0 - b_eq) * math.exp(-k_b * t)


def darcy_mobility(b: float, mobility_0: float, mobility_1: float) -> float:
    """Affine scalar mobility interpolation (placeholder closure).

    Both endpoint mobilities must be strictly positive.  This function does
    not assert that real silica permeability is linear in bridge density.
    """
    values = (b, mobility_0, mobility_1)
    if not all(math.isfinite(value) for value in values):
        raise ValueError("all inputs must be finite")
    if not 0.0 <= b <= 1.0:
        raise ValueError("b must lie in [0, 1]")
    if mobility_0 <= 0 or mobility_1 <= 0:
        raise ValueError("endpoint mobilities must be positive")
    return (1.0 - b) * mobility_0 + b * mobility_1
