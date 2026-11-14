"""CCFSM P8: variable-capacity chemo-hydraulic finite-volume operator.

Reference-volume inventories: mobile M/O and immobilized N/B. Fluid capacity
obeys the same discrete continuity equation as the Darcy flux used in species
advection. The Darcy flux is prescribed; this is not a pressure/mechanics solver.
"""
from __future__ import annotations
from dataclasses import dataclass
import math


@dataclass(frozen=True)
class P8Grid:
    cells: int
    spacing_m: float

    def __post_init__(self):
        if not isinstance(self.cells, int) or self.cells < 1:
            raise ValueError("cells must be a positive integer")
        if not math.isfinite(self.spacing_m) or self.spacing_m <= 0:
            raise ValueError("spacing_m must be finite and positive")

    @property
    def length_m(self):
        return self.cells * self.spacing_m


def _finite_tuple(values, n, name):
    if len(values) != n:
        raise ValueError(f"{name} must contain {n} values")
    out = tuple(float(v) for v in values)
    if any(not math.isfinite(v) for v in out):
        raise ValueError(f"{name} must be finite")
    return out


def p8_rhs(inventories, fluid_capacity, grid, darcy_flux_faces_m_s,
           diffusivities_m2_s, chemistry):
    """Return (d_inventories/dt, d_fluid_capacity/dt).

    Inventories are (m_M,m_O,s_N,s_B), all per reference volume. Fluid
    concentrations are m_M/theta and m_O/theta. There are cells+1 Darcy
    face fluxes; the two exterior faces are closed. Diffusion acts on mobile
    concentrations with flux -theta_face*D*grad(c). Network pools do not move.
    """
    if len(inventories) != 4:
        raise ValueError("four inventories M/O/N/B are required")
    fields = []
    for name, field in zip(("M", "O", "N", "B"), inventories):
        values = _finite_tuple(field, grid.cells, f"{name} inventory")
        if any(v < 0 for v in values):
            raise ValueError("inventories must be nonnegative")
        fields.append(values)

    theta = _finite_tuple(fluid_capacity, grid.cells, "fluid capacity")
    if any(v <= 0 for v in theta):
        raise ValueError("fluid capacity must be strictly positive")
    q = _finite_tuple(darcy_flux_faces_m_s, grid.cells + 1, "Darcy face flux")
    if abs(q[0]) > 1e-14 or abs(q[-1]) > 1e-14:
        raise ValueError("closed no-flow boundary requires zero boundary Darcy flux")
    diffusivities = _finite_tuple(diffusivities_m2_s, 2, "diffusivities")
    if any(v < 0 for v in diffusivities):
        raise ValueError("diffusivities must be nonnegative")

    n, dx = grid.cells, grid.spacing_m
    theta_rhs = [0.0] * n
    mass_rhs = [[0.0] * n for _ in range(4)]

    # Local detailed-balance reaction source. M/O use pore-fluid activities;
    # N/B use network inventories. Mechanical affinity feedback is off.
    c_ref = float(chemistry.reference_concentration)
    gamma = chemistry.activity_coefficients
    rates = chemistry.rate_constants_s
    equilibria = chemistry.equilibrium_constants
    if not math.isfinite(c_ref) or c_ref <= 0:
        raise ValueError("reference concentration must be positive")
    for j in range(n):
        activities = (
            gamma[0] * fields[0][j] / (theta[j] * c_ref),
            gamma[1] * fields[1][j] / (theta[j] * c_ref),
            gamma[2] * fields[2][j] / c_ref,
            gamma[3] * fields[3][j] / c_ref,
        )
        r = tuple(k * c_ref * (activities[i] - activities[i+1] / K)
                  for i, (k, K) in enumerate(zip(rates, equilibria)))
        r1, r2, r3 = r
        mass_rhs[0][j] = -r1
        mass_rhs[1][j] = r1 - r2
        mass_rhs[2][j] = r2 - r3
        mass_rhs[3][j] = r3

    # One oriented internal face flux updates theta and mobile inventories.
    concentrations = (
        tuple(fields[0][j] / theta[j] for j in range(n)),
        tuple(fields[1][j] / theta[j] for j in range(n)),
    )
    for face in range(1, n):
        qf = q[face]
        left, right = face - 1, face
        theta_rhs[left] -= qf / dx
        theta_rhs[right] += qf / dx
        theta_face = 0.5 * (theta[left] + theta[right])
        for species in range(2):
            c = concentrations[species]
            c_up = c[left] if qf >= 0.0 else c[right]
            advective = qf * c_up
            diffusive = -theta_face * diffusivities[species] * (
                c[right] - c[left]
            ) / dx
            flux = advective + diffusive
            mass_rhs[species][left] -= flux / dx
            mass_rhs[species][right] += flux / dx

    return tuple(tuple(field) for field in mass_rhs), tuple(theta_rhs)


def p8_total_silicon(inventories, grid):
    """Total Si-equivalent inventory per unit cross-sectional area."""
    if len(inventories) != 4 or any(len(f) != grid.cells for f in inventories):
        raise ValueError("four inventory fields matching grid are required")
    return grid.spacing_m * sum(sum(field) for field in inventories)


def p8_total_fluid_capacity(fluid_capacity, grid):
    """Integrated fluid capacity per unit cross-sectional area."""
    theta = _finite_tuple(fluid_capacity, grid.cells, "fluid capacity")
    if any(v <= 0 for v in theta):
        raise ValueError("fluid capacity must be strictly positive")
    return grid.spacing_m * sum(theta)
