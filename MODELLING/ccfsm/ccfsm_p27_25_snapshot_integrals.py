"""P27.25: reconstruct step-integrated transport work/dissipation from P21 snapshots.

Uses trapezoidal time quadrature between the initial P21 snapshot and the
accepted P24 final snapshot. Geometry is explicit (1-D length dx, area A).
Chemical boundary power is evaluated from the P13 reservoir potentials and
the actual split advective/diffusive boundary fluxes. This is a quadrature
audit, not an exact discrete chain-rule identity.
"""
from __future__ import annotations
import math


def _f(x, name):
    x = float(x)
    if not math.isfinite(x):
        raise ValueError(name + " must be finite")
    return x


def _transport(snapshot):
    if not isinstance(snapshot, dict) or not isinstance(snapshot.get("transport_rhs"), dict):
        raise ValueError("snapshot must contain transport_rhs")
    return snapshot["transport_rhs"]


def _boundary_chemical_power(transport):
    adv = transport["mobile_species_advective_face_fluxes_mol_m2_s"]
    total = transport["mobile_species_face_fluxes_mol_m2_s"]
    mu_cell = transport["mobile_species_chemical_potential_j_mol"]
    mu_left = transport["onsager_reservoir_chemical_potential_left_j_mol"]
    mu_right = transport["onsager_reservoir_chemical_potential_right_j_mol"]
    power = 0.0
    material = []
    for s in range(2):
        # Diffusion is total minus upwind advection at each boundary.
        a_l, a_r = _f(adv[s][0], "left advective flux"), _f(adv[s][-1], "right advective flux")
        t_l, t_r = _f(total[s][0], "left total flux"), _f(total[s][-1], "right total flux")
        d_l, d_r = t_l-a_l, t_r-a_r
        # Positive flux points left-to-right; inward power has + at left, - at right.
        mu_al = _f(mu_left[s] if a_l >= 0 else mu_cell[s][0], "left upwind potential")
        mu_ar = _f(mu_cell[s][-1] if a_r >= 0 else mu_right[s], "right upwind potential")
        chemical = (_f(mu_left[s], "left reservoir potential")*d_l
                    - _f(mu_right[s], "right reservoir potential")*d_r
                    + mu_al*a_l - mu_ar*a_r)
        power += chemical
        material.append({"left_net_flux_mol_m2_s": t_l,
                         "right_net_flux_mol_m2_s": t_r,
                         "net_inward_rate_mol_m2_s": t_l-t_r,
                         "advective_left_mol_m2_s": a_l,
                         "advective_right_mol_m2_s": a_r,
                         "diffusive_left_mol_m2_s": d_l,
                         "diffusive_right_mol_m2_s": d_r,
                         "chemical_boundary_power_w_m2": chemical})
    return power, tuple(material)


def reconstruct_p27_25_p24_step(
    initial_p21_snapshot, accepted_p24_result, dt_s, *,
    cell_width_m, reference_area_m2,
):
    """Reconstruct trapezoidal step integrals from accepted P21/P24 snapshots."""
    dt, dx, area = (_f(dt_s, "dt_s"), _f(cell_width_m, "cell_width_m"),
                    _f(reference_area_m2, "reference_area_m2"))
    if min(dt, dx, area) <= 0:
        raise ValueError("dt, cell width and reference area must be positive")
    if not isinstance(accepted_p24_result, dict) or not accepted_p24_result.get("converged"):
        raise ValueError("accepted P24 result must be converged")
    if not accepted_p24_result.get("pressure_snapshot_matches_accepted_state"):
        raise ValueError("P24 snapshot must match accepted state")
    t0, t1 = _transport(initial_p21_snapshot), _transport(accepted_p24_result.get("last_snapshot"))
    n = len(t0["reaction_dissipation_w_m3_reference"])
    if n < 1 or len(t1["reaction_dissipation_w_m3_reference"]) != n:
        raise ValueError("initial/final snapshot cell counts differ")
    for key in ("mobile_species_onsager_diffusive_dissipation_w_m2",
                "mobile_species_advective_face_fluxes_mol_m2_s",
                "mobile_species_face_fluxes_mol_m2_s",
                "mobile_species_chemical_potential_j_mol"):
        if len(t0[key]) != 2 or len(t1[key]) != 2:
            raise ValueError("two mobile species required in both snapshots")
    def avg(a, b, name):
        if len(a) != len(b):
            raise ValueError(name + " shapes differ")
        return tuple(0.5*(_f(x, name)+_f(y, name)) for x, y in zip(a, b))
    r0, r1 = t0["reaction_dissipation_w_m3_reference"], t1["reaction_dissipation_w_m3_reference"]
    reaction_rate = sum(avg(r0, r1, "reaction dissipation"))*dx*area
    if reaction_rate < -1e-10:
        raise ValueError("negative reconstructed reaction dissipation")
    darcy_rate = 0.5*(_f(t0["darcy_internal_dissipation_w_m2"], "initial Darcy")
                      + _f(t1["darcy_internal_dissipation_w_m2"], "final Darcy"))*area
    onsager_rate = sum(avg(t0["mobile_species_onsager_diffusive_dissipation_w_m2"],
                           t1["mobile_species_onsager_diffusive_dissipation_w_m2"],
                           "Onsager dissipation"))*area
    hydraulic_rate = 0.5*(_f(t0["reservoir_hydraulic_power_w_m2"], "initial hydraulic power")
                           + _f(t1["reservoir_hydraulic_power_w_m2"], "final hydraulic power"))*area
    chem0, mat0 = _boundary_chemical_power(t0)
    chem1, mat1 = _boundary_chemical_power(t1)
    chemical_rate = 0.5*(chem0+chem1)*area
    diss = {"reaction_j": max(0.0, reaction_rate)*dt,
            "darcy_j": max(0.0, darcy_rate)*dt,
            "onsager_diffusion_j": max(0.0, onsager_rate)*dt}
    if min(reaction_rate, darcy_rate, onsager_rate) < -1e-10:
        raise ValueError("negative dissipation reconstructed from P21 snapshots")
    work = {"reservoir_hydraulic_j": hydraulic_rate*dt,
            "mobile_species_chemical_boundary_j": chemical_rate*dt}
    return {
        "status": "reconstructed_p24_step_integrals_trapezoidal",
        "quadrature": "trapezoidal in time using initial P21 and accepted final P24 snapshots",
        "dt_s": dt, "cell_width_m": dx, "reference_area_m2": area,
        "reaction_dissipation_rate_w": reaction_rate,
        "darcy_internal_dissipation_rate_w": darcy_rate,
        "onsager_diffusion_dissipation_rate_w": onsager_rate,
        "reservoir_hydraulic_power_w": hydraulic_rate,
        "mobile_species_chemical_boundary_power_w": chemical_rate,
        "integrated_dissipation_j": diss,
        "external_work_j": work,
        "mobile_species_boundary_transport": {
            "initial": mat0, "final": mat1,
            "time_integrated_net_inward_mol": tuple(
                0.5*(mat0[s]["net_inward_rate_mol_m2_s"]+
                     mat1[s]["net_inward_rate_mol_m2_s"])*area*dt for s in range(2)),
        },
        "advection_entropy_closure_certified": False,
        "time_quadrature_is_exact": False,
        "limitations": (
            "Trapezoidal snapshot integration is not the exact P24 residual quadrature.",
            "The mobile boundary chemical work is a potential-weighted flux estimate; the full upwind entropy/chain-rule inequality remains unproved.",
            "Solid/bridge chemical reservoirs, mechanical Dirichlet reaction work, and any other external work are not inferred.",
            "No solver-level energy monotonicity or physical validation is certified.",
        ),
    }
