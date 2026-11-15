"""P27.24: two-state discrete energy balance for one accepted P24 step.

All energies/work/dissipation are joules over one fixed physical domain.
Dissipation inputs are step-integrated quantities, not endpoint rates.
The routine never infers missing boundary work or an advection entropy law.
"""
from __future__ import annotations
import math


def _f(value, name):
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(name + " must be finite")
    return value


def _close(a, b, atol, rtol):
    return abs(a-b) <= atol + rtol*max(abs(a), abs(b))


def _energy_snapshot(cells, volumes, *, owner, p19_audit,
                     chemical_owner, potential_convention, atol, rtol):
    elastic = storage = chemical = traction_potential = 0.0
    tractions = []
    for cell, volume in zip(cells, volumes):
        elastic += volume*_f(cell["elastic_energy_j_m3_reference"], "elastic density")
        storage += volume*_f(cell["biot_storage_energy_j_m3_reference"], "Biot density")
        if chemical_owner == "p9":
            chemical += volume*_f(cell["chemical_energy_j_m3_reference"], "chemical density")
        if potential_convention == "dead_load_total":
            traction = _f(cell["applied_axial_traction_pa"], "applied traction")
            strain = _f(cell["axial_strain"], "axial strain")
            tractions.append(traction)
            traction_potential -= volume*traction*strain
    if tractions and any(not _close(x, tractions[0], atol, rtol) for x in tractions[1:]):
        raise ValueError("dead-load total potential requires uniform traction")
    p9_mechanical = elastic + storage
    if owner == "p9":
        mechanical = p9_mechanical
    else:
        if not isinstance(p19_audit, dict) or p19_audit.get("status") != "matched_p9_p19_mechanical_energy":
            raise ValueError("P19 ownership requires a successful P27.22 audit at both states")
        reports = tuple(p19_audit.get("point_reports", ()))
        qvolume = sum(_f(q["weight_m3"], "P19 quadrature volume") for q in reports)
        if not reports or not _close(qvolume, sum(volumes), atol, rtol):
            raise ValueError("P19 quadrature volume does not match fixed P9 domain")
        pe = _f(p19_audit["p19_elastic_energy_j"], "P19 elastic energy")
        ps = _f(p19_audit["p19_biot_storage_energy_j"], "P19 Biot energy")
        pt = _f(p19_audit["p19_stored_energy_j"], "P19 stored energy")
        if not _close(pt, pe+ps, atol, rtol) or not _close(pt, p9_mechanical, atol, rtol):
            raise ValueError("P19/P9 mechanical energy mismatch at state")
        mechanical = pt
    total = mechanical + chemical + (traction_potential if potential_convention == "dead_load_total" else 0.0)
    return {"elastic_p9_j": elastic, "biot_storage_p9_j": storage,
            "p9_mechanical_j": p9_mechanical, "selected_mechanical_j": mechanical,
            "selected_chemical_j": chemical, "dead_load_potential_j": traction_potential,
            "selected_total_energy_j": total}


def audit_p24_discrete_energy_step(
    initial_cells, final_cells, cell_volumes_m3, dt_s, *,
    integrated_dissipation_j, external_work_j=None,
    mechanical_energy_owner="p9", p19_initial_audit=None,
    p19_final_audit=None, chemical_energy_owner="p9",
    potential_convention="stored", unclosed_energy_terms=(
        "P10/P13 upwind-advection entropy closure is not established",
    ), atol=1e-8, rtol=1e-8,
):
    """Audit E[n+1]-E[n] = W_external - D over one fixed-domain P24 step.

    integrated_dissipation_j must contain nonnegative step-integrated
    reaction_j, darcy_j and onsager_diffusion_j. Optional advection_j is
    counted only when independently supplied by the caller.
    """
    before, after, volumes = tuple(initial_cells), tuple(final_cells), tuple(cell_volumes_m3)
    if not before or len(before) != len(after) or len(before) != len(volumes):
        raise ValueError("initial/final cells and volumes need equal nonzero length")
    volumes = tuple(_f(v, "cell volume") for v in volumes)
    if any(v <= 0 for v in volumes):
        raise ValueError("cell volumes must be positive")
    dt, atol, rtol = _f(dt_s, "dt_s"), _f(atol, "atol"), _f(rtol, "rtol")
    if dt <= 0 or atol < 0 or rtol < 0:
        raise ValueError("dt must be positive and tolerances nonnegative")
    if mechanical_energy_owner not in ("p9", "p19"):
        raise ValueError("mechanical_energy_owner must be p9 or p19")
    if chemical_energy_owner not in ("p9", "external", "none"):
        raise ValueError("invalid chemical_energy_owner")
    if potential_convention not in ("stored", "dead_load_total"):
        raise ValueError("invalid potential_convention")
    e0 = _energy_snapshot(before, volumes, owner=mechanical_energy_owner,
        p19_audit=p19_initial_audit, chemical_owner=chemical_energy_owner,
        potential_convention=potential_convention, atol=atol, rtol=rtol)
    e1 = _energy_snapshot(after, volumes, owner=mechanical_energy_owner,
        p19_audit=p19_final_audit, chemical_owner=chemical_energy_owner,
        potential_convention=potential_convention, atol=atol, rtol=rtol)
    if not isinstance(integrated_dissipation_j, dict):
        raise ValueError("integrated_dissipation_j must be a mapping")
    required = ("reaction_j", "darcy_j", "onsager_diffusion_j")
    diss = {}
    for key in required:
        value = _f(integrated_dissipation_j[key], key)
        if value < -atol:
            raise ValueError(key + " must be nonnegative")
        diss[key] = max(0.0, value)
    if "advection_j" in integrated_dissipation_j:
        value = _f(integrated_dissipation_j["advection_j"], "advection_j")
        if value < -atol:
            raise ValueError("advection_j must be nonnegative")
        diss["advection_j"] = max(0.0, value)
    total_diss = sum(diss.values())
    works = external_work_j or {}
    if not isinstance(works, dict):
        raise ValueError("external_work_j must be a mapping")
    work = {str(k): _f(v, "external work "+str(k)) for k, v in works.items()}
    total_work = sum(work.values())
    delta = e1["selected_total_energy_j"] - e0["selected_total_energy_j"]
    predicted = total_work - total_diss
    residual = delta - predicted
    scale = max(1.0, abs(delta), abs(predicted), abs(e0["selected_total_energy_j"]),
                abs(e1["selected_total_energy_j"]))
    unclosed = tuple(str(x) for x in unclosed_energy_terms)
    return {
        "status": "audited_p24_two_state_energy_balance",
        "dt_s": dt, "energy_unit": "J", "work_unit": "J",
        "dissipation_unit": "J", "cell_volume_total_m3": sum(volumes),
        "mechanical_energy_owner": mechanical_energy_owner,
        "chemical_energy_owner": chemical_energy_owner,
        "potential_convention": potential_convention,
        "initial_energy": e0, "final_energy": e1,
        "energy_change_j": delta,
        "integrated_dissipation_terms_j": diss,
        "total_integrated_dissipation_j": total_diss,
        "external_work_terms_j": work, "total_external_work_j": total_work,
        "predicted_energy_change_j": predicted,
        "discrete_energy_residual_j": residual,
        "residual_within_tolerance": abs(residual) <= atol + rtol*scale,
        "full_energy_closure_certified": False,\n        "caller_declared_all_energy_terms_closed": not unclosed,
        "unclosed_energy_terms": unclosed,
        "mechanical_energy_counted_once": True,
        "dissipation_nonnegative": True,
        "interpretation": "A small residual verifies this supplied discrete ledger only; it does not prove P24 solver-level energy stability or physical validity.",
    }
