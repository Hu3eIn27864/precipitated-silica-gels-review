"""CCFSM P23: discrete audit of an accepted P22 implicit-Euler step.

The silicon balance is a closed FV inventory identity with the P21 mobile
boundary fluxes evaluated at the accepted iterate. The P9 local free-energy
difference and P19 FE mechanical energy/work differences are reported in
separate ledgers: their current reference measures are not yet proven
commensurate, so this module deliberately does not add them or manufacture
an energy residual. Dissipation/rate terms are diagnostics, not a substitute
for the accepted-step energy difference.
"""
from __future__ import annotations

import math

from ccfsm_p11_energy_time_integration import p11_total_free_energy
from ccfsm_p10_spatial_coupling import p10_total_silicon


def _finite(value, name):
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(name + " must be finite")
    return value


def _silicon_inventory(state, grid):
    return p10_total_silicon(state.inventories, grid)


def p23_audit_accepted_step(initial_state, p22_result, grid,
                            mechanical_parameters, chemistry,
                            tolerance=1e-9):
    """Audit conservation and energy changes for one converged P22 step.

    P22's final snapshot is required because it contains the P21 fluxes and
    P19 mechanics evaluated at the accepted state. Open-boundary silicon
    influx is dt*(J_left-J_right), with positive face flux oriented left to
    right. The independent residual is measured from the actual state delta.
    """
    tol = _finite(tolerance, "tolerance")
    if tol <= 0:
        raise ValueError("tolerance must be positive")
    if not isinstance(p22_result, dict) or not p22_result.get("converged"):
        raise ValueError("P23 requires a converged, accepted P22 result")
    accepted = p22_result.get("state")
    dt = _finite(p22_result.get("accepted_dt_s"), "accepted_dt_s")
    snapshot = p22_result.get("last_snapshot")
    if accepted is None or snapshot is None or dt <= 0:
        raise ValueError("accepted state, positive dt, and final snapshot required")
    if not snapshot.get("pressure_feedback_used_for_darcy_and_mobile_advection", True):
        raise ValueError("final snapshot does not certify P21 pressure feedback")
    transport = snapshot.get("transport_rhs")
    if not isinstance(transport, dict):
        raise ValueError("final P21 transport RHS missing")
    face_fluxes = transport.get("mobile_species_face_fluxes_mol_m2_s")
    if face_fluxes is None or len(face_fluxes) != 2:
        raise ValueError("P21 mobile species face fluxes missing")
    if any(len(row) != grid.cells + 1 for row in face_fluxes):
        raise ValueError("mobile species face flux dimensions do not match grid")

    si0 = _silicon_inventory(initial_state, grid)
    si1 = _silicon_inventory(accepted, grid)
    # M and O cross the open boundary; N and B are immobile. Internal
    # face fluxes telescope exactly in the finite-volume sum.
    left_flux = sum(_finite(row[0], "left mobile Si flux")
                    for row in face_fluxes)
    right_flux = sum(_finite(row[-1], "right mobile Si flux")
                     for row in face_fluxes)
    boundary_delta = dt * (left_flux - right_flux)
    observed_delta = si1 - si0
    si_residual = observed_delta - boundary_delta
    si_scale = max(1e-30, abs(si0), abs(si1), abs(boundary_delta))
    si_ok = abs(si_residual) <= tol * si_scale

    # P9's local energy is a 1D per-area quantity. P19's FE energy is
    # returned in joules over supplied quadrature; keep these ledgers apart.
    local_e0 = p11_total_free_energy(
        initial_state, grid, mechanical_parameters, chemistry)
    local_e1 = p11_total_free_energy(
        accepted, grid, mechanical_parameters, chemistry)
    local_delta = local_e1 - local_e0
    mech0 = snapshot.get("spatial_mechanics")
    if mech0 is None:
        raise ValueError("P19 mechanical snapshot missing")
    mech_energy = _finite(mech0.get("stored_energy_j"), "P19 stored energy")
    mech_work = _finite(mech0.get("boundary_traction_work_j"),
                        "P19 boundary traction work")
    reactions = _finite(mech0.get("dirichlet_reaction_residual"),
                         "P19 Dirichlet reaction residual")
    # The P22 snapshot is evaluated at the accepted state. A prior P19
    # energy/work value is not present in the P22 result; do not invent it.
    return {
        "accepted_dt_s": dt,
        "accepted_state_time_s": _finite(accepted.time_s,
                                         "accepted state time"),
        "silicon_inventory_before_mol_m2": si0,
        "silicon_inventory_after_mol_m2": si1,
        "silicon_inventory_change_mol_m2": observed_delta,
        "open_boundary_silicon_influx_mol_m2": boundary_delta,
        "left_mobile_silicon_flux_mol_m2_s": left_flux,
        "right_mobile_silicon_flux_mol_m2_s": right_flux,
        "silicon_balance_residual_mol_m2": si_residual,
        "silicon_balance_relative_residual": abs(si_residual) / si_scale,
        "silicon_balance_verified": si_ok,
        "p9_local_free_energy_before_j_m2": local_e0,
        "p9_local_free_energy_after_j_m2": local_e1,
        "p9_local_free_energy_change_j_m2": local_delta,
        "p19_mechanical_stored_energy_at_accepted_state_j": mech_energy,
        "p19_boundary_traction_work_at_accepted_state_j": mech_work,
        "p19_dirichlet_reaction_residual_at_accepted_state": reactions,
        "p19_free_dof_equilibrium_verified": bool(
            mech0.get("free_dof_equilibrium_verified", False)),
        "mechanical_energy_change_available": False,
        "dirichlet_reaction_work_change_available": False,
        "p16_semidiscrete_rate_is_not_used_as_discrete_energy_change": True,
        "global_energy_balance_residual_available": False,
        "energy_monotonicity_claimed": False,
        "energy_scope": (
            "P9 local FV free-energy difference is computed exactly from the "
            "two states. P19 FE energy and traction work are reported at the "
            "accepted state only; a prior FE snapshot and a dimensionally "
            "consistent FE/FV energy mapping are not yet available. Darcy, "
            "Onsager and reaction rates therefore are not assembled into a "
            "fabricated global discrete energy residual."
        ),
        "scope": (
            "Accepted P22 implicit-Euler step; exact global FV silicon "
            "inventory audit with open-boundary M/O fluxes, plus separate "
            "P9 local and P19 mechanical energy/work diagnostics. "
            "Software verification is not physical validation."
        ),
    }
