"""P27.27: analytic closed/open boundary reference cases for P27.25.

Synthetic, time-constant boundary data make the expected material transfer,
chemical boundary work and hydraulic reservoir work analytically exact.
This is an adapter-level sign/unit verification, not a physical validation.
"""
from __future__ import annotations

from ccfsm_p27_25_snapshot_integrals import reconstruct_p27_25_p24_step


def _snapshot(*, adv_m, total_m, adv_o=(0.0, 0.0), total_o=(0.0, 0.0),
              mu_m_cell=(6.0, 7.0), mu_o_cell=(2.0, 3.0),
              mu_left=(5.0, 4.0), mu_right=(11.0, 8.0),
              hydraulic=0.0):
    transport = {
        "reaction_dissipation_w_m3_reference": (0.0,),
        "darcy_internal_dissipation_w_m2": 0.0,
        "mobile_species_onsager_diffusive_dissipation_w_m2": (0.0, 0.0),
        "reservoir_hydraulic_power_w_m2": float(hydraulic),
        "mobile_species_advective_face_fluxes_mol_m2_s": (tuple(adv_m), tuple(adv_o)),
        "mobile_species_face_fluxes_mol_m2_s": (tuple(total_m), tuple(total_o)),
        "mobile_species_chemical_potential_j_mol": (tuple(mu_m_cell), tuple(mu_o_cell)),
        "onsager_reservoir_chemical_potential_left_j_mol": tuple(mu_left),
        "onsager_reservoir_chemical_potential_right_j_mol": tuple(mu_right),
    }
    return {"transport_rhs": transport}


def _run_case(initial, final, dt_s, area_m2):
    return reconstruct_p27_25_p24_step(
        initial,
        {"converged": True, "pressure_snapshot_matches_accepted_state": True,
         "last_snapshot": final},
        dt_s, cell_width_m=1.0, reference_area_m2=area_m2,
    )


def audit_p27_27_boundary_reference_cases(tolerance=1e-10):
    """Run exact constant-in-time closed and open boundary reference cases."""
    tol = float(tolerance)
    if tol <= 0:
        raise ValueError("tolerance must be positive")

    closed = _snapshot(adv_m=(0.0, 0.0), total_m=(0.0, 0.0),
                       hydraulic=0.0)
    closed_result = _run_case(closed, closed, 3.0, 2.0)

    # M species: left advective inflow +2, right advective outflow +1.
    # Diffusive boundary fluxes are +0.5 (left) and -0.25 (right).
    # Chemical power = 5*0.5 - 11*(-0.25) + 5*2 - 7*1 = 8.25 W/m².
    opened = _snapshot(adv_m=(2.0, 1.0), total_m=(2.5, 0.75),
                       hydraulic=4.0)
    open_result = _run_case(opened, opened, 3.0, 2.0)

    expected = {
        "closed_chemical_j": 0.0,
        "closed_hydraulic_j": 0.0,
        "closed_M_transfer_mol": 0.0,
        "closed_O_transfer_mol": 0.0,
        "open_chemical_j": 8.25 * 2.0 * 3.0,
        "open_hydraulic_j": 4.0 * 2.0 * 3.0,
        "open_M_transfer_mol": (2.5 - 0.75) * 2.0 * 3.0,
        "open_O_transfer_mol": 0.0,
    }
    observed = {
        "closed_chemical_j": closed_result["external_work_j"]["mobile_species_chemical_boundary_j"],
        "closed_hydraulic_j": closed_result["external_work_j"]["reservoir_hydraulic_j"],
        "closed_M_transfer_mol": closed_result["mobile_species_boundary_transport"]["time_integrated_net_inward_mol"][0],
        "closed_O_transfer_mol": closed_result["mobile_species_boundary_transport"]["time_integrated_net_inward_mol"][1],
        "open_chemical_j": open_result["external_work_j"]["mobile_species_chemical_boundary_j"],
        "open_hydraulic_j": open_result["external_work_j"]["reservoir_hydraulic_j"],
        "open_M_transfer_mol": open_result["mobile_species_boundary_transport"]["time_integrated_net_inward_mol"][0],
        "open_O_transfer_mol": open_result["mobile_species_boundary_transport"]["time_integrated_net_inward_mol"][1],
    }
    errors = {key: abs(observed[key] - expected[key]) for key in expected}
    return {
        "status": "p27_27_analytic_boundary_reference_audit",
        "cases": ("closed_zero_flux", "open_constant_flux"),
        "expected": expected,
        "observed": observed,
        "absolute_errors": errors,
        "tolerance": tol,
        "passed": all(error <= tol for error in errors.values()),
        "reference_scope": "constant-in-time synthetic boundary fluxes and potentials",
        "not_certified": (
            "physical reservoir constitutive law",
            "full upwind entropy chain rule",
            "time-varying P24 trajectory quadrature",
            "solid/bridge chemical work and mechanical boundary work",
        ),
    }
