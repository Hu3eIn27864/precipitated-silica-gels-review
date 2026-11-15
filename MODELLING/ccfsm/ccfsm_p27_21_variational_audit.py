"""P27.21: variational audit of the existing P9 local free-energy density.

The audit independently finite-differences the P9-reported stored free-energy
density with respect to theta and the four inventories, then compares those
derivatives with P9's reported conjugates. It deliberately exposes mismatch
under dead-load traction: the reported stored energy excludes the external
traction potential, so it need not have the total-potential envelope
derivatives for nonzero applied traction.
"""
from __future__ import annotations
import math
from ccfsm_p9_mechanical_feedback import p9_cell_closure


def _finite(x, name):
    v = float(x)
    if not math.isfinite(v):
        raise ValueError(name + " must be finite")
    return v


def _energy(theta, inventories, chemistry, parameters):
    cell = p9_cell_closure(theta, inventories[:2], inventories[2:], chemistry, parameters)
    return float(cell["free_energy_j_m3_reference"]), cell


def audit_p9_free_energy_variations(
    fluid_capacity,
    inventories,
    chemistry,
    mechanical_parameters,
    *,
    relative_step=2e-6,
    atol=2e-5,
    rtol=2e-5,
):
    """Compare FD derivatives of P9 stored energy to reported conjugates.

    Inventory order is (M,O,N,B). Derivatives dpsi/dn have J/mol;
    dpsi/dtheta has Pa (=J/m³). One-sided differences are used near the
    positive inventory/theta domain boundary.
    """
    try:
        theta = _finite(fluid_capacity, "fluid capacity")
        if not 0.0 < theta <= 1.0:
            raise ValueError("fluid capacity must lie in (0,1]")
        if len(inventories) != 4:
            raise ValueError("four inventories M,O,N,B are required")
        n = tuple(_finite(v, "inventory") for v in inventories)
        if any(v <= 0.0 for v in n):
            raise ValueError("inventories must be positive")
        hrel = _finite(relative_step, "relative step")
        atol, rtol = _finite(atol, "absolute tolerance"), _finite(rtol, "relative tolerance")
        if hrel <= 0 or atol < 0 or rtol < 0:
            raise ValueError("invalid finite-difference step or tolerance")
        psi, base = _energy(theta, n, chemistry, mechanical_parameters)
        if not math.isfinite(psi):
            raise ValueError("base free energy is non-finite")
        derivatives = {}
        targets = {}
        # Theta derivative. theta is dimensionless; derivative has Pa units.
        ht = hrel*max(1.0, abs(theta))
        lo, hi = max(1e-12, theta-ht), min(1.0, theta+ht)
        if hi <= lo:
            raise ValueError("cannot form theta finite difference")
        ep, _ = _energy(hi, n, chemistry, mechanical_parameters)
        em, _ = _energy(lo, n, chemistry, mechanical_parameters)
        derivatives["fluid_capacity_theta"] = (ep-em)/(hi-lo)
        targets["fluid_capacity_theta"] = _finite(base["fluid_energy_conjugate_pa"], "fluid conjugate")
        # Inventory derivatives; J/m³ divided by mol/m³ gives J/mol.
        names = ("M", "O", "N", "B")
        for i, name in enumerate(names):
            step = hrel*max(abs(n[i]), 1e-8)
            plus, minus = list(n), list(n)
            plus[i] += step
            if n[i] > step:
                minus[i] -= step
                ep, _ = _energy(theta, tuple(plus), chemistry, mechanical_parameters)
                em, _ = _energy(theta, tuple(minus), chemistry, mechanical_parameters)
                derivative = (ep-em)/(2.0*step)
            else:
                ep, _ = _energy(theta, tuple(plus), chemistry, mechanical_parameters)
                derivative = (ep-psi)/step
            derivatives["inventory_"+name] = derivative
            targets["inventory_"+name] = _finite(
                base["total_chemical_potentials_j_mol"][i], "chemical potential")
        defects = {}
        checks = {}
        for key, fd in derivatives.items():
            target = targets[key]
            defect = fd-target
            tol = atol+rtol*max(1.0, abs(fd), abs(target))
            defects[key] = defect
            checks[key] = {"finite_difference": fd, "reported_conjugate": target,
                           "absolute_defect": abs(defect), "tolerance": tol,
                           "pass": abs(defect) <= tol}
        passed = all(v["pass"] for v in checks.values())
        traction = float(mechanical_parameters.applied_axial_traction_pa)
        return {
            "status": "p9_variational_derivatives_consistent" if passed else "p9_variational_derivative_defect",
            "overall_pass": passed,
            "stored_free_energy_j_m3_reference": psi,
            "energy_decomposition_j_m3_reference": {
                "elastic": float(base["elastic_energy_j_m3_reference"]),
                "biot_storage": float(base["biot_storage_energy_j_m3_reference"]),
                "chemical": float(base["chemical_energy_j_m3_reference"]),
            },
            "decomposition_sum_defect_j_m3": psi - sum((
                float(base["elastic_energy_j_m3_reference"]),
                float(base["biot_storage_energy_j_m3_reference"]),
                float(base["chemical_energy_j_m3_reference"]))),
            "derivative_checks": checks,
            "maximum_absolute_derivative_defect": max(v["absolute_defect"] for v in checks.values()),
            "applied_axial_traction_pa": traction,
            "external_traction_potential_included_in_reported_energy": False,
            "traction_potential_warning": (
                "For nonzero dead-load traction, stored-energy derivatives need not equal "
                "the reported total-potential conjugates; include and differentiate the "
                "external traction potential consistently before claiming a variational closure."
                if traction != 0.0 else None),
            "common_free_energy_across_P10_P13_P19_certified": False,
            "scope": "local P9 finite-difference derivative audit of its reported stored energy",
        }
    except (TypeError, ValueError, OverflowError, ZeroDivisionError, AttributeError, IndexError):
        return {"status": "invalid_or_malformed_input", "overall_pass": False}
