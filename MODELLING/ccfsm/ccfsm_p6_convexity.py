"""CCFSM P6 analytical convexity certificates.

These routines encode exact quadratic-form identities; they are not a PDE
solver or a numerical proof of existence for the nonlinear P5 system.
"""
from __future__ import annotations

import math


def mobile_entropy_hessian_form(mobile_inventories, theta, variation_mobile,
                                variation_theta, rt):
    """Return D²f[h,h] = RT sum_i m_i (h_i/m_i-h_theta/theta)^2."""
    if len(mobile_inventories) != 2 or len(variation_mobile) != 2:
        raise ValueError("exactly two mobile pools and variations are required")
    values = (*mobile_inventories, theta, *variation_mobile, variation_theta, rt)
    if any(not math.isfinite(float(v)) for v in values):
        raise ValueError("all arguments must be finite")
    if any(float(v) <= 0 for v in mobile_inventories) or theta <= 0 or rt <= 0:
        raise ValueError("inventories, theta, and RT must be positive")
    return rt * sum(m * (h/m - variation_theta/theta)**2
                    for m, h in zip(mobile_inventories, variation_mobile))


def bridge_eigenstrain_norm_bound(beta, b0):
    """Sharp Frobenius-norm bound for beta*(b-b0)*I, with b in [0,1]."""
    if not math.isfinite(beta) or not math.isfinite(b0):
        raise ValueError("beta and b0 must be finite")
    if beta < 0 or not 0 <= b0 <= 1:
        raise ValueError("beta must be nonnegative and b0 must lie in [0,1]")
    return math.sqrt(3.0) * beta * max(b0, 1.0-b0)
