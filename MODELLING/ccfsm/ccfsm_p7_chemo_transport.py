"""CCFSM P7: conservative chemo-transport operator on a fixed Biot flow.

Reference-volume inventories: mobile M/O and immobilized network N/B.
The Darcy flux is prescribed from the P6 linear Biot block. This is a
semidiscrete finite-volume operator, not a time integrator or calibrated model.
"""
from __future__ import annotations
from dataclasses import dataclass
import math
from ccfsm_p2_chemical_affinity import ChemicalParametersP2

@dataclass(frozen=True)
class P7Grid:
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

def p7_rhs(inventories, grid, darcy_flux_faces_m_s, diffusivities_m2_s,
           fluid_capacity, chemistry):
    """Return d(m_M,m_O,s_N,s_B)/dt in reference-volume units.

    There are cells+1 face Darcy fluxes; boundary fluxes are zero.
    Mobile advection is upwinded as (m_i/theta)*Q; mobile diffusion is
    centered with flux -D_i grad(m_i). Network pools are immobile.
    """
    if len(inventories) != 4:
        raise ValueError("four inventories M/O/N/B are required")
    fields = []
    for name, field in zip(("M", "O", "N", "B"), inventories):
        values = _finite_tuple(field, grid.cells, f"{name} inventory")
        if any(v < 0 for v in values):
            raise ValueError("inventories must be nonnegative")
        fields.append(values)
    q = _finite_tuple(darcy_flux_faces_m_s, grid.cells+1, "Darcy face flux")
    if abs(q[0]) > 1e-14 or abs(q[-1]) > 1e-14:
        raise ValueError("closed no-flow boundary requires zero boundary Darcy flux")
    d = _finite_tuple(diffusivities_m2_s, 2, "diffusivities")
    if any(v < 0 for v in d):
        raise ValueError("diffusivities must be nonnegative")
    theta = float(fluid_capacity)
    if not math.isfinite(theta) or theta <= 0:
        raise ValueError("fluid_capacity must be positive and finite")
    c_ref = chemistry.reference_concentration
    gamma = chemistry.activity_coefficients
    reaction = [[0.0]*grid.cells for _ in range(4)]
    for j in range(grid.cells):
        a = (gamma[0]*fields[0][j]/(theta*c_ref),
             gamma[1]*fields[1][j]/(theta*c_ref),
             gamma[2]*fields[2][j]/c_ref,
             gamma[3]*fields[3][j]/c_ref)
        r = [k*c_ref*(a[i]-a[i+1]/K)
             for i,(k,K) in enumerate(zip(chemistry.rate_constants_s,
                                          chemistry.equilibrium_constants))]
        r1,r2,r3 = r
        reaction[0][j],reaction[1][j] = -r1,r1-r2
        reaction[2][j],reaction[3][j] = r2-r3,r3
    out = [list(v) for v in reaction]
    dx = grid.spacing_m
    for species in range(2):
        mobile = fields[species]
        for face in range(1,grid.cells):
            adv = q[face]*(mobile[face-1] if q[face]>=0 else mobile[face])/theta
            diff = -d[species]*(mobile[face]-mobile[face-1])/dx
            flux = adv+diff
            out[species][face-1] -= flux/dx
            out[species][face] += flux/dx
    return tuple(tuple(v) for v in out)

def p7_total_silicon(inventories, grid):
    """Total Si-equivalent inventory per unit cross-sectional area."""
    if len(inventories)!=4 or any(len(f)!=grid.cells for f in inventories):
        raise ValueError("four inventory fields matching grid are required")
    return grid.spacing_m*sum(sum(f) for f in inventories)
