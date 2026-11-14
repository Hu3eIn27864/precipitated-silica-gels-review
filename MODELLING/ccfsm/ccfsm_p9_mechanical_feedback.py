"""CCFSM P9: traction-controlled 1D chemo-poroelastic constitutive closure.

This module couples bridge-dependent isotropic eigenstrain, Biot storage,
quasistatic axial equilibrium and a positive structure/strain-dependent
intrinsic permeability. It is a local constitutive closure, not yet a spatial
PDE integrator or an empirically calibrated silica law.
"""
from __future__ import annotations
from dataclasses import dataclass
import math
from ccfsm_p2_chemical_affinity import R_GAS


def _finite(x, name):
    x = float(x)
    if not math.isfinite(x):
        raise ValueError(f"{name} must be finite")
    return x


def _positive(x, name):
    x = _finite(x, name)
    if x <= 0:
        raise ValueError(f"{name} must be positive")
    return x


@dataclass(frozen=True)
class P9Parameters:
    lame_lambda_pa: float
    shear_modulus_pa: float
    biot_modulus_pa: float
    biot_coefficient: float
    bridge_eigenstrain: float
    bridge_reference: float
    bridge_regularization: float
    reference_fluid_capacity: float
    reference_axial_strain: float
    reference_permeability_m2_per_pas: float
    bridge_permeability_sensitivity: float
    strain_permeability_sensitivity: float
    reference_bridge_fraction: float = 0.0
    applied_axial_traction_pa: float = 0.0

    def validate(self):
        vals = (self.lame_lambda_pa, self.shear_modulus_pa,
                self.biot_modulus_pa, self.biot_coefficient,
                self.bridge_eigenstrain, self.bridge_reference,
                self.bridge_regularization, self.reference_fluid_capacity,
                self.reference_axial_strain,
                self.reference_permeability_m2_per_pas,
                self.bridge_permeability_sensitivity,
                self.strain_permeability_sensitivity,
                self.reference_bridge_fraction,
                self.applied_axial_traction_pa)
        if any(not math.isfinite(float(v)) for v in vals):
            raise ValueError("P9 parameters must be finite")
        if self.lame_lambda_pa < 0 or self.shear_modulus_pa <= 0:
            raise ValueError("elastic moduli must be nonnegative/positive")
        if self.biot_modulus_pa <= 0:
            raise ValueError("Biot modulus must be positive")
        if not 0 <= self.biot_coefficient <= 1:
            raise ValueError("Biot coefficient must lie in [0,1]")
        if self.bridge_eigenstrain < 0 or self.bridge_regularization <= 0:
            raise ValueError("bridge coefficient/regularization invalid")
        if not 0 < self.reference_fluid_capacity <= 1:
            raise ValueError("reference fluid capacity must lie in (0,1]")
        if self.reference_permeability_m2_per_pas <= 0:
            raise ValueError("reference permeability must be positive")
        if self.bridge_permeability_sensitivity < 0:
            raise ValueError("bridge permeability sensitivity must be nonnegative")
        if self.strain_permeability_sensitivity < 0:
            raise ValueError("strain permeability sensitivity must be nonnegative")
        if not 0 <= self.reference_bridge_fraction <= 1:
            raise ValueError("reference bridge fraction must lie in [0,1]")


def p9_cell_closure(fluid_capacity, mobile_inventories, network_inventories,
                    chemistry, parameters: P9Parameters):
    """Solve local Biot/eigenstrain equilibrium under prescribed axial traction.

    Geometry: 1D bar with axial strain eps, zero lateral total strain, isotropic
    chemical eigenstrain eps_ch*I. Total axial stress equals applied traction.
    Fluid content zeta=theta-theta_ref and p=M*(zeta-alpha*eps).
    """
    parameters.validate()
    theta = _positive(fluid_capacity, "fluid capacity")
    if theta > 1.0:
        raise ValueError("fluid capacity cannot exceed one")
    if len(mobile_inventories) != 2 or len(network_inventories) != 2:
        raise ValueError("two mobile and two network inventories required")
    inv = tuple(_positive(v, "inventory") for v in
                (*mobile_inventories, *network_inventories))
    mm, mo, sn, sb = inv
    p = parameters
    beta_den = sn + sb + p.bridge_regularization
    bridge_fraction = sb / beta_den
    eigen = p.bridge_eigenstrain * (bridge_fraction-p.bridge_reference)
    h = p.lame_lambda_pa + 2.0*p.shear_modulus_pa
    alpha, modulus = p.biot_coefficient, p.biot_modulus_pa
    zeta = theta-p.reference_fluid_capacity
    # Solve p=M*(zeta-alpha*(eigen+(traction+alpha*p)/H)).
    denom = 1.0 + modulus*alpha*alpha/h
    pressure = modulus*(zeta-alpha*eigen-alpha*p.applied_axial_traction_pa/h)/denom
    axial_strain = eigen+(p.applied_axial_traction_pa+alpha*pressure)/h
    effective_stress = h*(axial_strain-eigen)
    total_stress = effective_stress-alpha*pressure
    fluid_content_residual = zeta-(pressure/modulus+alpha*axial_strain)

    # Full 3D isotropic elastic energy evaluated at (eps_xx,0,0).
    elastic_trace = axial_strain-3.0*eigen
    e_diag = (axial_strain-eigen, -eigen, -eigen)
    elastic_energy = (0.5*p.lame_lambda_pa*elastic_trace**2
                      + p.shear_modulus_pa*sum(x*x for x in e_diag))
    storage_energy = 0.5*modulus*(zeta-alpha*axial_strain)**2
    rt = R_GAS*_positive(chemistry.temperature_k, "temperature")
    cref = _positive(chemistry.reference_concentration, "reference concentration")
    gamma = tuple(float(x) for x in chemistry.activity_coefficients)
    eq = tuple(float(x) for x in chemistry.equilibrium_constants)
    if len(gamma) != 4 or any(not math.isfinite(x) or x <= 0 for x in gamma):
        raise ValueError("four positive activity coefficients required")
    if len(eq) != 3 or any(not math.isfinite(x) or x <= 0 for x in eq):
        raise ValueError("three positive equilibrium constants required")
    activities = (gamma[0]*mm/(theta*cref), gamma[1]*mo/(theta*cref),
                  gamma[2]*sn/cref, gamma[3]*sb/cref)
    mu0 = [0.0]
    for k in eq:
        mu0.append(mu0[-1]-rt*math.log(k))
    mu_chem = tuple(mu0[i]+rt*math.log(activities[i]) for i in range(4))
    chemical_energy = sum(inv[i]*(mu0[i]+rt*(math.log(activities[i])-1.0))
                          for i in range(4))

    # Envelope derivative of elastic energy with respect to bridge fraction.
    # The external traction potential is not included in stored free energy.
    trace_elastic_stress = (3.0*p.lame_lambda_pa+2.0*p.shear_modulus_pa)*elastic_trace
    dpsi_db = -p.bridge_eigenstrain*trace_elastic_stress
    db_dsn = -sb/(beta_den*beta_den)
    db_dsb = (sn+p.bridge_regularization)/(beta_den*beta_den)
    mu_mech = (0.0, 0.0, dpsi_db*db_dsn, dpsi_db*db_dsb)
    mu_total = tuple(mu_chem[i]+mu_mech[i] for i in range(4))

    # Phenomenological positive permeability law; sensitivities are hypotheses.
    log_k_ratio = (-p.bridge_permeability_sensitivity*
                   (bridge_fraction-p.reference_bridge_fraction)
                   + p.strain_permeability_sensitivity*
                   (axial_strain-p.reference_axial_strain))
    permeability = p.reference_permeability_m2_per_pas*math.exp(
        max(-700.0, min(700.0, log_k_ratio)))
    osmotic = rt*(mm+mo)/theta
    return {
        "fluid_capacity": theta,
        "fluid_content_increment": zeta,
        "pore_pressure_pa": pressure,
        "axial_strain": axial_strain,
        "chemical_eigenstrain": eigen,
        "bridge_fraction": bridge_fraction,
        "effective_axial_stress_pa": effective_stress,
        "total_axial_stress_pa": total_stress,
        "applied_axial_traction_pa": p.applied_axial_traction_pa,
        "fluid_content_residual": fluid_content_residual,
        "intrinsic_permeability_m2_per_pas": permeability,
        "log_permeability_ratio": log_k_ratio,
        "elastic_energy_j_m3_reference": elastic_energy,
        "biot_storage_energy_j_m3_reference": storage_energy,
        "chemical_energy_j_m3_reference": chemical_energy,
        "free_energy_j_m3_reference": elastic_energy+storage_energy+chemical_energy,
        "chemical_potentials_j_mol": mu_chem,
        "mechanical_chemical_potential_correction_j_mol": mu_mech,
        "total_chemical_potentials_j_mol": mu_total,
        "osmotic_pressure_pa": osmotic,
        "fluid_energy_conjugate_pa": pressure-osmotic,
    }


def p9_field_closure(fluid_capacity, inventories, chemistry, parameters):
    """Evaluate the P9 local closure cellwise for four inventory fields."""
    n = len(fluid_capacity)
    if n == 0 or len(inventories) != 4 or any(len(f) != n for f in inventories):
        raise ValueError("P9 fields must contain four equally sized nonempty arrays")
    cells = tuple(p9_cell_closure(fluid_capacity[j],
        (inventories[0][j], inventories[1][j]),
        (inventories[2][j], inventories[3][j]), chemistry, parameters)
        for j in range(n))
    return {
        "cells": cells,
        "pore_pressure_pa": tuple(c["pore_pressure_pa"] for c in cells),
        "axial_strain": tuple(c["axial_strain"] for c in cells),
        "intrinsic_permeability_m2_per_pas": tuple(
            c["intrinsic_permeability_m2_per_pas"] for c in cells),
        "bridge_fraction": tuple(c["bridge_fraction"] for c in cells),
        "total_axial_stress_pa": tuple(c["total_axial_stress_pa"] for c in cells),
    }
