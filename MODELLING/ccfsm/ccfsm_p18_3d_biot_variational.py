"""CCFSM P18: 3D isotropic Biot/eigenstrain variational kernel.

This module separates the 3D constitutive law from dimensional reductions.
It provides plane-strain and laterally traction-free uniaxial reductions.
All strains are infinitesimal and all energies are per reference volume.
"""
from __future__ import annotations
from dataclasses import dataclass
import math


def _finite(value, name):
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    return value


def _solve3(a, b):
    """Small pivoted Gaussian elimination for a 3x3 linear system."""
    m = [[float(a[i][j]) for j in range(3)] + [float(b[i])]
         for i in range(3)]
    for col in range(3):
        pivot = max(range(col, 3), key=lambda row: abs(m[row][col]))
        if abs(m[pivot][col]) <= 1e-30:
            raise ValueError("singular constitutive reduction")
        m[col], m[pivot] = m[pivot], m[col]
        scale = m[col][col]
        m[col] = [v/scale for v in m[col]]
        for row in range(3):
            if row == col:
                continue
            factor = m[row][col]
            m[row] = [m[row][j]-factor*m[col][j] for j in range(4)]
    return tuple(m[i][3] for i in range(3))


@dataclass(frozen=True)
class P18Parameters:
    lame_lambda_pa: float
    shear_modulus_pa: float
    biot_modulus_pa: float
    biot_coefficient: float

    def validate(self):
        vals = (self.lame_lambda_pa, self.shear_modulus_pa,
                self.biot_modulus_pa, self.biot_coefficient)
        if any(not math.isfinite(float(v)) for v in vals):
            raise ValueError("P18 parameters must be finite")
        if self.lame_lambda_pa < 0 or self.shear_modulus_pa <= 0:
            raise ValueError("Lamé/shear moduli must be nonnegative/positive")
        if self.biot_modulus_pa <= 0:
            raise ValueError("Biot modulus must be positive")
        if not 0 <= self.biot_coefficient <= 1:
            raise ValueError("Biot coefficient must lie in [0,1]")


def p18_3d_state(strain, eigenstrain, fluid_content_increment,
                 parameters: P18Parameters):
    """Evaluate 3D energy, pore pressure and symmetric total stress.

    strain is ((exx, exy, exz), (eyx, eyy, eyz), (ezx, ezy, ezz));
    symmetric off-diagonal entries are required.
    """
    parameters.validate()
    if len(strain) != 3 or any(len(row) != 3 for row in strain):
        raise ValueError("strain must be a 3x3 matrix")
    eps = tuple(tuple(_finite(strain[i][j], "strain") for j in range(3))
                for i in range(3))
    for i in range(3):
        for j in range(3):
            if abs(eps[i][j]-eps[j][i]) > 1e-12:
                raise ValueError("small-strain tensor must be symmetric")
    c = _finite(eigenstrain, "eigenstrain")
    zeta = _finite(fluid_content_increment, "fluid content increment")
    p = parameters
    tr_eps = sum(eps[i][i] for i in range(3))
    tr_el = tr_eps-3.0*c
    elastic = [[eps[i][j]-(c if i == j else 0.0)
                for j in range(3)] for i in range(3)]
    pfluid = p.biot_modulus_pa*(zeta-p.biot_coefficient*tr_eps)
    elastic_energy = (0.5*p.lame_lambda_pa*tr_el*tr_el
        +p.shear_modulus_pa*sum(elastic[i][j]**2
                                for i in range(3) for j in range(3)))
    storage_energy = 0.5*p.biot_modulus_pa*(
        zeta-p.biot_coefficient*tr_eps)**2
    stress = tuple(tuple(
        p.lame_lambda_pa*tr_el*(1.0 if i == j else 0.0)
        +2.0*p.shear_modulus_pa*elastic[i][j]
        -p.biot_coefficient*pfluid*(1.0 if i == j else 0.0)
        for j in range(3)) for i in range(3))
    eigen_conjugate = -(3.0*p.lame_lambda_pa+2.0*p.shear_modulus_pa)*tr_el
    return {
        "pore_pressure_pa": pfluid,
        "stress_pa": stress,
        "elastic_energy_j_m3": elastic_energy,
        "biot_storage_energy_j_m3": storage_energy,
        "total_mechanical_energy_j_m3": elastic_energy+storage_energy,
        "trace_strain": tr_eps,
        "elastic_trace": tr_el,
        "eigenstrain_energy_conjugate_pa": eigen_conjugate,
    }


def p18_plane_strain(axial_strain, eigenstrain, fluid_content_increment,
                     parameters: P18Parameters, axial_traction_pa=None):
    """Plane-strain slice: eps_yy=eps_zz=0, eps_xx prescribed or solved."""
    parameters.validate()
    p = parameters
    e = _finite(axial_strain, "axial strain")
    c = _finite(eigenstrain, "eigenstrain")
    z = _finite(fluid_content_increment, "fluid content increment")
    state = p18_3d_state(((e,0,0),(0,0,0),(0,0,0)), c, z, p)
    if axial_traction_pa is not None:
        target = _finite(axial_traction_pa, "axial traction")
        if abs(state["stress_pa"][0][0]-target) > 1e-8*max(1.0,abs(target)):
            raise ValueError("prescribed axial strain does not satisfy traction")
    return state


def p18_uniaxial_stress_free_laterals(eigenstrain,
        fluid_content_increment, axial_traction_pa, parameters: P18Parameters):
    """Solve axial traction with sigma_yy=sigma_zz=0 and eps_yy=eps_zz."""
    parameters.validate()
    p = parameters
    c = _finite(eigenstrain, "eigenstrain")
    z = _finite(fluid_content_increment, "fluid content increment")
    t = _finite(axial_traction_pa, "axial traction")
    lam, g, m, alpha = (p.lame_lambda_pa, p.shear_modulus_pa,
                        p.biot_modulus_pa, p.biot_coefficient)
    h = lam+2*g
    ce = 3*lam+2*g
    # Unknowns (exx, lateral strain l, pore pressure).
    matrix = (
        (h, 2*lam, -alpha),
        (lam, 2*(lam+g), -alpha),
        (m*alpha, 2*m*alpha, 1.0),
    )
    rhs = (t+ce*c, ce*c, m*z)
    e, lateral, pressure = _solve3(matrix, rhs)
    state = p18_3d_state(((e,0,0),(0,lateral,0),(0,0,lateral)),
                         c, z, p)
    return {
        **state,
        "axial_strain": e,
        "lateral_strain": lateral,
        "axial_traction_residual_pa": state["stress_pa"][0][0]-t,
        "lateral_traction_residual_pa": max(
            abs(state["stress_pa"][1][1]), abs(state["stress_pa"][2][2])),
        "pressure_solution_residual_pa": state["pore_pressure_pa"]-pressure,
    }
