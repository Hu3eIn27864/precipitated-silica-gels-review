"""P27.19: cross-component thermodynamic consistency ledger."""
from __future__ import annotations
import math


def _finite_map(values, name, nonnegative=False):
    if not isinstance(values, dict) or not values:
        raise ValueError(name + " must be a non-empty mapping")
    out = {}
    for key, value in values.items():
        if not isinstance(key, str) or not key.strip():
            raise ValueError(name + " keys must be non-empty strings")
        v = float(value)
        if not math.isfinite(v) or (nonnegative and v < 0):
            raise ValueError(name + " values must be finite" + (" and nonnegative" if nonnegative else ""))
        out[key] = v
    return out


def audit_thermodynamic_ledger(energy_rate_components_w_m2,
        dissipation_components_w_m2, external_power_components_w_m2, *,
        onsager_audit=None, reaction_affinity_rate_pairs=(),
        darcy_faces_m_s=None, darcy_permeability_faces_m2_per_pas=None,
        pressure_gradient_faces_pa_m=None, atol=1e-10, rtol=1e-8):
    """Check E_dot=P_external-D; all powers are W/m² on one reference area."""
    try:
        er = _finite_map(energy_rate_components_w_m2, "energy rates")
        ds = _finite_map(dissipation_components_w_m2, "dissipations", True)
        pw = _finite_map(external_power_components_w_m2, "external powers")
        atol, rtol = float(atol), float(rtol)
        if not math.isfinite(atol) or not math.isfinite(rtol) or atol < 0 or rtol < 0:
            raise ValueError("invalid tolerances")
        edot, diss, power = sum(er.values()), sum(ds.values()), sum(pw.values())
        predicted = power - diss
        residual = edot - predicted
        scale = max(1.0, abs(edot), abs(predicted),
                    sum(abs(v) for v in er.values()),
                    sum(abs(v) for v in ds.values()), sum(abs(v) for v in pw.values()))
        tol = atol + rtol*scale
        balance_pass = abs(residual) <= tol
        products = []
        for pair in reaction_affinity_rate_pairs:
            if len(pair) != 2:
                raise ValueError("reaction pairs must be (rate, affinity)")
            rate, affinity = float(pair[0]), float(pair[1])
            if not math.isfinite(rate) or not math.isfinite(affinity):
                raise ValueError("reaction data must be finite")
            products.append(rate*affinity)
        reaction_pass = all(v >= -tol for v in products)
        onsager_pass = None if onsager_audit is None else (
            isinstance(onsager_audit, dict) and onsager_audit.get("overall_pass") is True)
        darcy = None
        arrays = (darcy_faces_m_s, darcy_permeability_faces_m2_per_pas, pressure_gradient_faces_pa_m)
        if any(v is not None for v in arrays):
            if any(v is None for v in arrays):
                raise ValueError("all Darcy arrays are required together")
            q, k, g = (tuple(float(v) for v in a) for a in arrays)
            if len(q) < 3 or len(q) != len(k) or len(q) != len(g):
                raise ValueError("Darcy arrays must have equal length >= 3")
            if any(not math.isfinite(v) for v in q+k+g) or any(v <= 0 for v in k):
                raise ValueError("invalid Darcy data")
            defects = tuple(q[i]+k[i]*g[i] for i in range(1, len(q)-1))
            dscale = max(1.0, *(abs(q[i]) for i in range(1, len(q)-1)),
                         *(abs(k[i]*g[i]) for i in range(1, len(q)-1)))
            dtol = atol+rtol*dscale
            darcy = {"interior_constitutive_max_abs_error": max(abs(v) for v in defects),
                     "tolerance": dtol,
                     "constitutive_pass": max(abs(v) for v in defects) <= dtol,
                     "interior_dissipation_sum_q2_over_k": sum(
                         q[i]*q[i]/k[i] for i in range(1, len(q)-1))}
        checks = [balance_pass, reaction_pass]
        if onsager_pass is not None: checks.append(onsager_pass)
        if darcy is not None: checks.append(darcy["constitutive_pass"])
        passed = all(checks)
        return {"status": "thermodynamic_ledger_passed" if passed else "thermodynamic_ledger_failed",
                "overall_pass": passed, "energy_rate_components_w_m2": er,
                "dissipation_components_w_m2": ds, "external_power_components_w_m2": pw,
                "energy_rate_sum_w_m2": edot, "dissipation_sum_w_m2": diss,
                "external_power_sum_w_m2": power, "predicted_energy_rate_w_m2": predicted,
                "independent_balance_residual_w_m2": residual,
                "balance_tolerance_w_m2": tol, "balance_pass": balance_pass,
                "reaction_rate_affinity_products": tuple(products),
                "reaction_dissipation_pass": reaction_pass, "onsager_gate_pass": onsager_pass,
                "darcy_check": darcy, "physical_thermodynamic_closure_certified": False,
                "scope": "algebraic consistency of caller-supplied component rates, powers and dissipations"}
    except (TypeError, ValueError, OverflowError, ZeroDivisionError, AttributeError):
        return {"status": "invalid_or_malformed_input", "overall_pass": False}
