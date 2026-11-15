"""P27.23: coupled P9/P10/P13/P19 energy and dissipation ledger.

The ledger integrates P9 free-energy densities over explicit physical cell
volumes, optionally replaces (never adds) the P9 mechanical/Biot terms by a
verified P19 quadrature energy, and audits supplied P13 dissipation channels.
All powers are converted to watts using the reference cross-sectional area.
"""
from __future__ import annotations
import math


def _finite(value, name):
    value=float(value)
    if not math.isfinite(value):
        raise ValueError(name+" must be finite")
    return value


def _sum_finite(values, name):
    return sum(_finite(v,name) for v in values)


def build_p27_23_thermodynamic_ledger(
    p9_cells,
    cell_volumes_m3,
    p13_result,
    *,
    reference_area_m2,
    energy_rate_w,
    external_power_terms_w=None,
    mechanical_energy_owner="p9",
    p19_energy_audit=None,
    chemical_energy_owner="p9",
    potential_convention="stored",
    atol=1e-8,
    rtol=1e-8,
):
    """Build a unit-consistent, non-double-counted energy/dissipation ledger.

    P9 densities [J/m^3] times cell volumes [m^3] give energies [J].
    P10 reaction dissipation [W/m^3] is volume-integrated; P13 Onsager
    diffusion and P10 Darcy internal dissipation [W/m^2] are multiplied by
    reference area [m^2]. The energy rate and external powers are [W].

    P19 ownership requires a successful P27.22 audit whose quadrature volume
    matches the supplied P9 control volumes. The P19 elastic+Biot energy
    replaces P9's corresponding integral; it is never added to it.
    """
    cells=tuple(p9_cells)
    volumes=tuple(_finite(v,"cell volume") for v in cell_volumes_m3)
    if not cells or len(cells)!=len(volumes):
        raise ValueError("P9 cells and cell volumes must have equal nonzero length")
    if any(v<=0 for v in volumes):
        raise ValueError("cell volumes must be positive")
    area=_finite(reference_area_m2,"reference area")
    if area<=0:
        raise ValueError("reference area must be positive")
    rate=_finite(energy_rate_w,"energy rate")
    atol,rtol=_finite(atol,"atol"),_finite(rtol,"rtol")
    if atol<0 or rtol<0:
        raise ValueError("tolerances must be nonnegative")
    if mechanical_energy_owner not in ("p9","p19"):
        raise ValueError("mechanical_energy_owner must be p9 or p19")
    if chemical_energy_owner not in ("p9","external","none"):
        raise ValueError("chemical_energy_owner must be p9, external or none")
    if potential_convention not in ("stored","dead_load_total"):
        raise ValueError("potential_convention must be stored or dead_load_total")

    p9_elastic=p9_storage=p9_chemical=traction_potential=0.0
    traction_values=[]
    for cell,volume in zip(cells,volumes):
        elastic=_finite(cell["elastic_energy_j_m3_reference"],"P9 elastic density")
        storage=_finite(cell["biot_storage_energy_j_m3_reference"],"P9 Biot density")
        chemical=_finite(cell["chemical_energy_j_m3_reference"],"P9 chemical density")
        p9_elastic+=volume*elastic
        p9_storage+=volume*storage
        p9_chemical+=volume*chemical
        if potential_convention=="dead_load_total":
            traction=_finite(cell["applied_axial_traction_pa"],"P9 applied traction")
            strain=_finite(cell["axial_strain"],"P9 axial strain")
            traction_values.append(traction)
            traction_potential-=volume*traction*strain
    if traction_values and any(abs(t-traction_values[0])>atol+rtol*max(abs(t),abs(traction_values[0])) for t in traction_values[1:]):
        raise ValueError("dead-load total potential requires uniform applied traction")

    p9_mechanical=p9_elastic+p9_storage
    p19_elastic=p19_storage=0.0
    if mechanical_energy_owner=="p19":
        if not isinstance(p19_energy_audit,dict) or p19_energy_audit.get("status")!="matched_p9_p19_mechanical_energy":
            raise ValueError("P19 ownership requires a successful P27.22 energy audit")
        reports=tuple(p19_energy_audit.get("point_reports",()))
        if not reports:
            raise ValueError("P27.22 audit must provide quadrature volume reports")
        p19_volume=sum(_finite(q["weight_m3"],"P19 quadrature volume") for q in reports)
        p9_volume=sum(volumes)
        if abs(p19_volume-p9_volume)>atol+rtol*max(abs(p19_volume),abs(p9_volume)):
            raise ValueError("P19 quadrature volume does not match P9 control volumes")
        p19_elastic=_finite(p19_energy_audit["p19_elastic_energy_j"],"P19 elastic energy")
        p19_storage=_finite(p19_energy_audit["p19_biot_storage_energy_j"],"P19 Biot energy")
        p19_total=_finite(p19_energy_audit["p19_stored_energy_j"],"P19 stored energy")
        if abs(p19_total-(p19_elastic+p19_storage))>atol+rtol*max(abs(p19_total),abs(p19_elastic+p19_storage)):
            raise ValueError("P19 stored energy does not equal elastic plus Biot terms")
        if abs(p19_total-p9_mechanical)>atol+rtol*max(abs(p19_total),abs(p9_mechanical)):
            raise ValueError("P27.22 P9/P19 mechanical energy totals do not match")
        selected_mechanical=p19_total
    else:
        selected_mechanical=p9_mechanical

    selected_chemical=p9_chemical if chemical_energy_owner=="p9" else 0.0
    if potential_convention=="dead_load_total":
        if not traction_values:
            raise ValueError("dead-load potential requires traction data")
        selected_potential=selected_mechanical+selected_chemical+traction_potential
    else:
        selected_potential=selected_mechanical+selected_chemical

    if not isinstance(p13_result,dict):
        raise ValueError("p13_result must be a P13 result mapping")
    reaction=tuple(_finite(x,"reaction dissipation") for x in p13_result["reaction_dissipation_w_m3_reference"])
    if len(reaction)!=len(cells):
        raise ValueError("P13 reaction dissipation must match P9 cells")
    if any(x < -atol for x in reaction):
        raise ValueError("negative reaction dissipation violates the local Onsager sign check")
    reaction_power=sum(v*max(0.0,d) for v,d in zip(volumes,reaction))
    darcy_areal=_finite(p13_result["darcy_internal_dissipation_w_m2"],"Darcy dissipation")
    if darcy_areal < -atol:
        raise ValueError("Darcy internal dissipation must be nonnegative")
    onsager=tuple(_finite(x,"Onsager diffusion dissipation") for x in p13_result["mobile_species_onsager_diffusive_dissipation_w_m2"])
    if any(x < -atol for x in onsager):
        raise ValueError("Onsager diffusion dissipation must be nonnegative")
    darcy_power=area*max(0.0,darcy_areal)
    diffusion_power=area*sum(max(0.0,x) for x in onsager)
    total_dissipation=reaction_power+darcy_power+diffusion_power

    powers=external_power_terms_w or {}
    if not isinstance(powers,dict):
        raise ValueError("external_power_terms_w must be a mapping")
    external={str(k):_finite(v,"external power "+str(k)) for k,v in powers.items()}
    external_total=sum(external.values())
    predicted_rate=external_total-total_dissipation
    residual=rate-predicted_rate
    scale=max(1.0,abs(rate),abs(predicted_rate))
    return {
        "status":"audited_energy_rate_balance",
        "energy_unit":"J",
        "power_unit":"W",
        "reference_area_m2":area,
        "cell_volume_total_m3":sum(volumes),
        "mechanical_energy_owner":mechanical_energy_owner,
        "chemical_energy_owner":chemical_energy_owner,
        "potential_convention":potential_convention,
        "p9_elastic_energy_j":p9_elastic,
        "p9_biot_storage_energy_j":p9_storage,
        "p9_mechanical_energy_integral_j":p9_mechanical,
        "p19_elastic_energy_j":p19_elastic,
        "p19_biot_storage_energy_j":p19_storage,
        "selected_mechanical_energy_j":selected_mechanical,
        "selected_chemical_energy_j":selected_chemical,
        "dead_load_potential_j":traction_potential,
        "selected_total_potential_j":selected_potential,
        "reaction_dissipation_w":reaction_power,
        "darcy_internal_dissipation_w":darcy_power,
        "onsager_diffusion_dissipation_w":diffusion_power,
        "total_dissipation_w":total_dissipation,
        "external_power_terms_w":external,
        "external_power_total_w":external_total,
        "energy_rate_w":rate,
        "predicted_energy_rate_w":predicted_rate,
        "balance_residual_w":residual,
        "balance_within_tolerance":abs(residual)<=atol+rtol*scale,
        "dissipation_nonnegative":True,
        "mechanical_energy_counted_once":True,
        "limitations":(
            "P10/P13 upwind-advection entropy closure is not established.",
            "Reservoir chemical and hydraulic power must be supplied explicitly in external_power_terms_w.",
            "P13 inherited Fick diffusion diagnostics are not added; only the Onsager diffusion channel is counted.",
            "No gradient energy, external work beyond supplied powers, or complete P21/P24 discrete energy theorem is certified.",
            "This is a snapshot/ledger audit, not a proof of physical validity or global thermodynamic stability.",
        ),
    }
