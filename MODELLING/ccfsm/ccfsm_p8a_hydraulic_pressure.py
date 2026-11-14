"""CCFSM P8a: closed 1D pressure-storage-Darcy block coupled to P8 transport."""
from __future__ import annotations
from dataclasses import dataclass
import math
from ccfsm_p8_variable_capacity import P8Grid, p8_rhs


def _values(values, n, name, positive=False, nonnegative=False):
    if len(values) != n:
        raise ValueError(f"{name} must contain {n} values")
    result = tuple(float(x) for x in values)
    if any(not math.isfinite(x) for x in result):
        raise ValueError(f"{name} must be finite")
    if positive and any(x <= 0 for x in result):
        raise ValueError(f"{name} must be strictly positive")
    if nonnegative and any(x < 0 for x in result):
        raise ValueError(f"{name} must be nonnegative")
    return result


@dataclass(frozen=True)
class P8aHydraulicParameters:
    storage_per_pa: tuple
    permeability_m2_per_pas: tuple
    theta_reference: tuple
    pressure_reference_pa: float

    def validate(self, cells):
        storage = _values(self.storage_per_pa, cells, "storage", positive=True)
        permeability = _values(self.permeability_m2_per_pas, cells,
                               "permeability", positive=True)
        theta0 = _values(self.theta_reference, cells, "reference capacity",
                         positive=True)
        pref = float(self.pressure_reference_pa)
        if not math.isfinite(pref):
            raise ValueError("reference pressure must be finite")
        return storage, permeability, theta0, pref


def p8a_hydraulic_rhs(pressure_pa, grid, parameters):
    """Return (theta, pressure_dot, theta_dot, Darcy face flux).

    theta = theta_ref + storage*(p-p_ref); Q=-K grad(p), harmonic K
    at internal faces, and zero exterior face flux. Units: Q m/s.
    """
    n = grid.cells
    p = _values(pressure_pa, n, "pressure")
    storage, permeability, theta0, pref = parameters.validate(n)
    theta = tuple(theta0[j] + storage[j] * (p[j] - pref) for j in range(n))
    if any(x <= 0 for x in theta):
        raise ValueError("pressure state produces nonpositive fluid capacity")
    q = [0.0] * (n + 1)
    theta_dot = [0.0] * n
    for face in range(1, n):
        left, right = face - 1, face
        kl, kr = permeability[left], permeability[right]
        kface = 2.0 * kl * kr / (kl + kr)
        q[face] = -kface * (p[right] - p[left]) / grid.spacing_m
        theta_dot[left] -= q[face] / grid.spacing_m
        theta_dot[right] += q[face] / grid.spacing_m
    pressure_dot = tuple(theta_dot[j] / storage[j] for j in range(n))
    return theta, pressure_dot, tuple(theta_dot), tuple(q)


def p8a_coupled_rhs(inventories, pressure_pa, grid, parameters,
                    diffusivities_m2_s, chemistry):
    """Return mobile/network inventory RHS plus pressure/capacity/Darcy RHS."""
    theta, pressure_dot, theta_dot, q = p8a_hydraulic_rhs(
        pressure_pa, grid, parameters
    )
    inventory_dot, theta_dot_transport = p8_rhs(
        inventories, theta, grid, q, diffusivities_m2_s, chemistry
    )
    if any(abs(a-b) > 1e-12 for a, b in zip(theta_dot, theta_dot_transport)):
        raise ArithmeticError("hydraulic and transport fluid balances disagree")
    return {
        "inventory_dot": inventory_dot,
        "pressure_dot_pa_s": pressure_dot,
        "fluid_capacity": theta,
        "fluid_capacity_dot_s": theta_dot,
        "darcy_flux_faces_m_s": q,
    }


def p8a_pressure_dissipation(pressure_pa, grid, parameters):
    """Return the nonnegative discrete integral sum K_face*(grad p)^2*dx."""
    p = _values(pressure_pa, grid.cells, "pressure")
    _, permeability, _, _ = parameters.validate(grid.cells)
    total = 0.0
    for face in range(1, grid.cells):
        left, right = face-1, face
        kface = 2*permeability[left]*permeability[right]/(
            permeability[left]+permeability[right])
        grad = (p[right]-p[left])/grid.spacing_m
        total += kface * grad*grad * grid.spacing_m
    return total
