"""Dimensionally explicit hydraulic/mechanical consolidation identities.

Hydraulic conductivity K [m/s] and intrinsic permeability kappa [m^2] are
not interchangeable. For the classical linear-consolidation convention:
    c_v = K*M/gamma_w = kappa*M/mu
where M is the appropriate constrained modulus, gamma_w=rho*g is liquid
unit weight, and mu is dynamic viscosity. No silica-gel constitutive law is
assumed; all quantities are independent inputs.
"""
from __future__ import annotations

import math


def _positive_finite(value: float, name: str) -> float:
    value = float(value)
    if not math.isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and > 0")
    return value


def effective_diffusivity_from_hydraulic_conductivity(
        hydraulic_conductivity_m_s: float, constrained_modulus_pa: float,
        fluid_unit_weight_n_m3: float = 9810.0) -> float:
    """Return c_v [m^2/s] = K [m/s] * M [Pa] / gamma_w [N/m^3]."""
    conductivity = _positive_finite(hydraulic_conductivity_m_s,
                                    "hydraulic_conductivity_m_s")
    modulus = _positive_finite(constrained_modulus_pa,
                               "constrained_modulus_pa")
    unit_weight = _positive_finite(fluid_unit_weight_n_m3,
                                   "fluid_unit_weight_n_m3")
    return conductivity * modulus / unit_weight


def hydraulic_conductivity_from_diffusivity(
        diffusivity_m2_s: float, constrained_modulus_pa: float,
        fluid_unit_weight_n_m3: float = 9810.0) -> float:
    """Invert for K [m/s]; meaningful only if M and gamma_w are known."""
    diffusivity = _positive_finite(diffusivity_m2_s, "diffusivity_m2_s")
    modulus = _positive_finite(constrained_modulus_pa,
                               "constrained_modulus_pa")
    unit_weight = _positive_finite(fluid_unit_weight_n_m3,
                                   "fluid_unit_weight_n_m3")
    return diffusivity * unit_weight / modulus


def effective_diffusivity_from_intrinsic_permeability(
        intrinsic_permeability_m2: float, constrained_modulus_pa: float,
        dynamic_viscosity_pa_s: float) -> float:
    """Return c_v [m^2/s] = kappa [m^2] * M [Pa] / mu [Pa s]."""
    permeability = _positive_finite(intrinsic_permeability_m2,
                                    "intrinsic_permeability_m2")
    modulus = _positive_finite(constrained_modulus_pa,
                               "constrained_modulus_pa")
    viscosity = _positive_finite(dynamic_viscosity_pa_s,
                                 "dynamic_viscosity_pa_s")
    return permeability * modulus / viscosity


def intrinsic_permeability_from_diffusivity(
        diffusivity_m2_s: float, constrained_modulus_pa: float,
        dynamic_viscosity_pa_s: float) -> float:
    """Invert for intrinsic permeability [m^2] if M and mu are known."""
    diffusivity = _positive_finite(diffusivity_m2_s, "diffusivity_m2_s")
    modulus = _positive_finite(constrained_modulus_pa,
                               "constrained_modulus_pa")
    viscosity = _positive_finite(dynamic_viscosity_pa_s,
                                 "dynamic_viscosity_pa_s")
    return diffusivity * viscosity / modulus
