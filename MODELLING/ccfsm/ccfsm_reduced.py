"""Verified reduced constitutive relations for natural silica-gel syneresis.

This module deliberately implements only the empirically supported scalar
response and dimensionally checked reductions. It does not assign invented
values to chemical, fractal, permeability, or modulus parameters.
"""
from __future__ import annotations

from dataclasses import dataclass
import math


@dataclass(frozen=True)
class NaturalSyneresisFit:
    """Sample-specific fit of S(t) = A * (1 - exp(-t/tau)).

    amplitude is dimensionless relative volume shrinkage.
    tau_hours is the empirical characteristic time in hours.
    """

    amplitude: float
    tau_hours: float

    def __post_init__(self) -> None:
        if not math.isfinite(self.amplitude) or not 0.0 <= self.amplitude < 1.0:
            raise ValueError("amplitude must be finite and lie in [0, 1).")
        if not math.isfinite(self.tau_hours) or self.tau_hours <= 0.0:
            raise ValueError("tau_hours must be finite and strictly positive.")


def _finite_nonnegative(value: float, name: str) -> float:
    value = float(value)
    if not math.isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and non-negative.")
    return value


def shrinkage(time_hours: float, fit: NaturalSyneresisFit) -> float:
    """Return relative volume shrinkage at non-negative elapsed time."""
    t = _finite_nonnegative(time_hours, "time_hours")
    return fit.amplitude * (-math.expm1(-t / fit.tau_hours))


def shrinkage_rate(time_hours: float, fit: NaturalSyneresisFit) -> float:
    """Return dS/dt in h^-1."""
    t = _finite_nonnegative(time_hours, "time_hours")
    return (fit.amplitude / fit.tau_hours) * math.exp(-t / fit.tau_hours)


def exact_relaxation_step(
    current_shrinkage: float,
    dt_hours: float,
    fit: NaturalSyneresisFit,
) -> float:
    """Exact update of dS/dt=(A-S)/tau over a constant-coefficient step.

    The initial value must be in [0, A]. This update is unconditionally stable
    and preserves that interval up to floating-point roundoff.
    """
    s = float(current_shrinkage)
    dt = _finite_nonnegative(dt_hours, "dt_hours")
    if not math.isfinite(s) or s < 0.0 or s > fit.amplitude:
        raise ValueError("current_shrinkage must lie in [0, amplitude].")
    return fit.amplitude + (s - fit.amplitude) * math.exp(-dt / fit.tau_hours)


def solid_volume_fraction(
    initial_solid_fraction: float,
    relative_shrinkage: float,
) -> float:
    """Homogeneous, no-solid-loss result phi=phi0/(1-S).

    This relation is invalid if the solid volume changes, solid is lost, or
    shrinkage is spatially heterogeneous.
    """
    phi0 = float(initial_solid_fraction)
    s = float(relative_shrinkage)
    if not math.isfinite(phi0) or not 0.0 < phi0 <= 1.0:
        raise ValueError("initial_solid_fraction must lie in (0, 1].")
    if not math.isfinite(s) or not 0.0 <= s < 1.0:
        raise ValueError("relative_shrinkage must lie in [0, 1).")
    phi = phi0 / (1.0 - s)
    if phi > 1.0 + 1e-12:
        raise ValueError("Inputs imply a solid fraction greater than one.")
    return min(phi, 1.0)


def hydraulic_relaxation_time_seconds(
    viscosity_pa_s: float,
    drainage_length_m: float,
    intrinsic_permeability_m2: float,
    effective_modulus_pa: float,
    geometry_factor: float = 1.0,
) -> float:
    """Return tau_h = mu*L^2/(C_g*k*K) in seconds.

    This is a first-mode scaling closure, not a permeability estimator.
    A measured tau_h identifies only the composite C_g*k*K/(mu*L^2)
    unless the remaining quantities are independently known.
    """
    values = {
        "viscosity_pa_s": viscosity_pa_s,
        "drainage_length_m": drainage_length_m,
        "intrinsic_permeability_m2": intrinsic_permeability_m2,
        "effective_modulus_pa": effective_modulus_pa,
        "geometry_factor": geometry_factor,
    }
    vals = {}
    for name, value in values.items():
        v = float(value)
        if not math.isfinite(v) or v <= 0.0:
            raise ValueError(f"{name} must be finite and strictly positive.")
        vals[name] = v
    return (
        vals["viscosity_pa_s"] * vals["drainage_length_m"] ** 2
        / (
            vals["geometry_factor"]
            * vals["intrinsic_permeability_m2"]
            * vals["effective_modulus_pa"]
        )
    )


def log_volume_contraction(relative_shrinkage: float) -> float:
    """Return chi=-ln(1-S), the exact logarithmic volume contraction."""
    s = float(relative_shrinkage)
    if not math.isfinite(s) or not 0.0 <= s < 1.0:
        raise ValueError("relative_shrinkage must lie in [0, 1).")
    return -math.log1p(-s)


def apparent_rate_per_hour(fit: NaturalSyneresisFit) -> float:
    """Return the fitted apparent relaxation rate 1/tau in h^-1."""
    return 1.0 / fit.tau_hours


def initial_shrinkage_rate_per_hour(fit: NaturalSyneresisFit) -> float:
    """Return the fitted initial relative-shrinkage rate A/tau in h^-1."""
    return fit.amplitude / fit.tau_hours
