"""Minimal permeability--skeleton coupling identities for consolidation.

This module deliberately contains no fitted or assumed constitutive law for
silica gels. Permeability k and constrained modulus M remain independent
inputs; the effective coefficient c_v follows the classical identity
c_v = k*M/gamma_w under the stated linear-consolidation convention.
"""
from __future__ import annotations

import math


def _positive_finite(value: float, name: str) -> float:
    value = float(value)
    if not math.isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and > 0")
    return value


def effective_consolidation_diffusivity(
        permeability_m2: float, constrained_modulus_pa: float,
        fluid_unit_weight_n_m3: float = 9810.0) -> float:
    """Return c_v [m^2/s] = k [m^2] * M [Pa] / gamma_w [N/m^3].

    M must be the modulus appropriate to the adopted one-dimensional
    constrained response. The default unit weight is a water reference value,
    not a silica-gel measurement; pass the actual pore-liquid value when known.
    """
    permeability = _positive_finite(permeability_m2, "permeability_m2")
    modulus = _positive_finite(constrained_modulus_pa,
                               "constrained_modulus_pa")
    unit_weight = _positive_finite(fluid_unit_weight_n_m3,
                                   "fluid_unit_weight_n_m3")
    return permeability * modulus / unit_weight


def permeability_from_diffusivity(
        diffusivity_m2_s: float, constrained_modulus_pa: float,
        fluid_unit_weight_n_m3: float = 9810.0) -> float:
    """Algebraic inversion; only meaningful if M is independently known."""
    diffusivity = _positive_finite(diffusivity_m2_s, "diffusivity_m2_s")
    modulus = _positive_finite(constrained_modulus_pa,
                               "constrained_modulus_pa")
    unit_weight = _positive_finite(fluid_unit_weight_n_m3,
                                   "fluid_unit_weight_n_m3")
    return diffusivity * unit_weight / modulus
