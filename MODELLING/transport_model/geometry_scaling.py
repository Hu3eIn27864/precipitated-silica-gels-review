"""Geometry-specific first-mode time scales for ideal radial diffusion.

These functions translate a first-mode time constant into an apparent
diffusivity. They do not solve a full transient consolidation problem and do
not identify permeability or a poroelastic material coefficient.
"""
from __future__ import annotations

import math

CYLINDER_ALPHA_01 = 2.404825557695773
SPHERE_ALPHA_1 = math.pi


def _positive_finite(value: float, name: str) -> float:
    value = float(value)
    if not math.isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and > 0")
    return value


def radial_first_mode_time_constant(geometry: str, radius_m: float,
                                    diffusivity_m2_s: float) -> float:
    """Return tau_1 [s] for an ideal, surface-drained radial domain.

    geometry is 'cylinder' (infinite cylinder, radial drainage only) or
    'sphere'. Finite-cylinder end drainage and mixed boundary conditions are
    deliberately not represented.
    """
    radius = _positive_finite(radius_m, "radius_m")
    diffusivity = _positive_finite(diffusivity_m2_s, "diffusivity_m2_s")
    if geometry == "cylinder":
        eigenvalue = CYLINDER_ALPHA_01
    elif geometry == "sphere":
        eigenvalue = SPHERE_ALPHA_1
    else:
        raise ValueError("geometry must be 'cylinder' or 'sphere'")
    return radius * radius / (eigenvalue * eigenvalue * diffusivity)


def apparent_radial_diffusivity(geometry: str, radius_m: float,
                                time_constant_s: float) -> float:
    """Invert the ideal first-mode relation; result is diagnostic D_app."""
    radius = _positive_finite(radius_m, "radius_m")
    tau = _positive_finite(time_constant_s, "time_constant_s")
    if geometry == "cylinder":
        eigenvalue = CYLINDER_ALPHA_01
    elif geometry == "sphere":
        eigenvalue = SPHERE_ALPHA_1
    else:
        raise ValueError("geometry must be 'cylinder' or 'sphere'")
    return radius * radius / (eigenvalue * eigenvalue * tau)

def finite_cylinder_first_mode_time_constant(
        radius_m: float, height_m: float, diffusivity_m2_s: float,
        end_boundary: str = "drained") -> float:
    """First-mode time constant for a finite cylinder with radial drainage.

    Constant isotropic diffusivity, initially uniform field, zero-flux
    symmetry at the axis, and a perfectly drained cylindrical side wall are
    assumed. height_m is the full end-to-end cylinder height. For
    end_boundary='drained' both flat ends are Dirichlet drained surfaces;
    for 'sealed' both ends are no-flux. Mixed or partially drained ends,
    finite external resistance, evolving shape and variable coefficients are
    not represented.

    Separation of variables gives lambda_1^2 = alpha_01^2/R^2 plus
    (pi/H)^2 for drained ends, or just the radial term for sealed ends.
    The returned tau is 1/(D*lambda_1^2).
    """
    radius = _positive_finite(radius_m, "radius_m")
    height = _positive_finite(height_m, "height_m")
    diffusivity = _positive_finite(diffusivity_m2_s, "diffusivity_m2_s")
    if end_boundary not in ("drained", "sealed"):
        raise ValueError("end_boundary must be 'drained' or 'sealed'")
    eigenvalue_squared = (CYLINDER_ALPHA_01 / radius) ** 2
    if end_boundary == "drained":
        eigenvalue_squared += (math.pi / height) ** 2
    return 1.0 / (diffusivity * eigenvalue_squared)
