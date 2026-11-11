#!/usr/bin/env python3
"""Dimensional scaling for a minimal saturated poroelastic consolidation model.

This module is a bookkeeping/identifiability utility, not a calibrated silica
constitutive model. Under the simplifying assumptions of an incompressible
pore liquid, Biot coefficient approximately one, and a linear constrained
skeleton modulus M, the hydraulic diffusivity is cv = kappa*M/mu.

The permeability kappa and modulus M are not separately identifiable from cv
(or one characteristic consolidation time) without independent measurements.
No material parameter defaults are supplied.
"""
from __future__ import annotations

import math


def _positive_finite(name: str, value: float) -> float:
    value = float(value)
    if not math.isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and > 0")
    return value


def consolidation_diffusivity_m2_s(
    intrinsic_permeability_m2: float,
    constrained_modulus_pa: float,
    dynamic_viscosity_pa_s: float,
) -> float:
    """Return cv = kappa*M/mu [m^2/s] for the stated linear assumptions."""
    kappa = _positive_finite("intrinsic_permeability_m2", intrinsic_permeability_m2)
    modulus = _positive_finite("constrained_modulus_pa", constrained_modulus_pa)
    viscosity = _positive_finite("dynamic_viscosity_pa_s", dynamic_viscosity_pa_s)
    return kappa * modulus / viscosity


def characteristic_time_s(
    drainage_length_m: float,
    intrinsic_permeability_m2: float,
    constrained_modulus_pa: float,
    dynamic_viscosity_pa_s: float,
) -> float:
    """Return the diffusion scaling time L_d^2/cv [s]."""
    length = _positive_finite("drainage_length_m", drainage_length_m)
    cv = consolidation_diffusivity_m2_s(
        intrinsic_permeability_m2,
        constrained_modulus_pa,
        dynamic_viscosity_pa_s,
    )
    return length * length / cv


def permeability_for_characteristic_time_m2(
    target_time_s: float,
    drainage_length_m: float,
    constrained_modulus_pa: float,
    dynamic_viscosity_pa_s: float,
) -> float:
    """Return the kappa implied by a chosen time and M; not a measurement."""
    time = _positive_finite("target_time_s", target_time_s)
    length = _positive_finite("drainage_length_m", drainage_length_m)
    modulus = _positive_finite("constrained_modulus_pa", constrained_modulus_pa)
    viscosity = _positive_finite("dynamic_viscosity_pa_s", dynamic_viscosity_pa_s)
    return length * length * viscosity / (time * modulus)


def dimensionless_time(
    elapsed_time_s: float,
    drainage_length_m: float,
    intrinsic_permeability_m2: float,
    constrained_modulus_pa: float,
    dynamic_viscosity_pa_s: float,
) -> float:
    """Return Tv = cv*t/L_d^2, dimensionless."""
    elapsed = float(elapsed_time_s)
    if not math.isfinite(elapsed) or elapsed < 0.0:
        raise ValueError("elapsed_time_s must be finite and >= 0")
    length = _positive_finite("drainage_length_m", drainage_length_m)
    cv = consolidation_diffusivity_m2_s(
        intrinsic_permeability_m2,
        constrained_modulus_pa,
        dynamic_viscosity_pa_s,
    )
    return cv * elapsed / (length * length)
