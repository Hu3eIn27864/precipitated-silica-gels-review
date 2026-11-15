"""P27.29: upwind branch-switch boundary quadrature and time-support refinement.

Synthetic linearly sign-changing advective boundary fluxes exercise the
left/right upwind-potential branches in the P27.25 adapter. Composite
accepted-snapshot trapezoids are compared with exact piecewise integrals.
"""
from __future__ import annotations

from ccfsm_p27_25_snapshot_integrals import reconstruct_p27_25_p24_step


def _snapshot(t):
    left = t - 1.0
    right = t - 1.5
    tr = {
        "reaction_dissipation_w_m3_reference": (0.0,),
        "darcy_internal_dissipation_w_m2": 0.0,
        "mobile_species_onsager_diffusive_dissipation_w_m2": (0.0, 0.0),
        "reservoir_hydraulic_power_w_m2": 0.0,
        "mobile_species_advective_face_fluxes_mol_m2_s": (
            (left, right), (0.0, 0.0)),
        "mobile_species_face_fluxes_mol_m2_s": (
            (left, right), (0.0, 0.0)),
        "mobile_species_chemical_potential_j_mol": (
            (5.0, 7.0), (0.0, 0.0)),
        "onsager_reservoir_chemical_potential_left_j_mol": (2.0, 0.0),
        "onsager_reservoir_chemical_potential_right_j_mol": (3.0, 0.0),
    }
    return {"transport_rhs": tr}


def _piecewise_linear_integral(crossing, duration, negative_branch_mu,
                                positive_branch_mu, sign):
    """Integral of sign*mu_upwind*(t-crossing), split at its zero."""
    c, T = float(crossing), float(duration)
    left = sign * negative_branch_mu * (0.5 * (min(c, T) - c) ** 2
                                         - 0.5 * (0.0 - c) ** 2) if c > 0 else 0.0
    # Integrate the negative-flux branch on [0,min(c,T)] directly.
    lo, hi = 0.0, min(c, T)
    neg = sign * negative_branch_mu * (
        0.5 * (hi - c) ** 2 - 0.5 * (lo - c) ** 2)
    lo2, hi2 = max(c, 0.0), T
    pos = 0.0
    if hi2 > lo2:
        pos = sign * positive_branch_mu * (
            0.5 * (hi2 - c) ** 2 - 0.5 * (lo2 - c) ** 2)
    return neg + pos


def audit_p27_29_upwind_branch_refinement(
    duration_s=2.0, area_m2=1.5, support_counts=(1, 2, 3, 4, 8),
    tolerance=1e-12,
):
    """Audit sign switches at t=1 (left) and t=1.5 (right)."""
    duration, area, tol = float(duration_s), float(area_m2), float(tolerance)
    counts = tuple(int(n) for n in support_counts)
    if duration <= 1.5 or area <= 0 or tol <= 0:
        raise ValueError("duration must exceed 1.5 and area/tolerance must be positive")
    if not counts or any(n < 1 for n in counts) or len(set(counts)) != len(counts):
        raise ValueError("support_counts must contain distinct positive integers")

    # Left: negative flux uses cell mu=5, positive flux reservoir mu=2.
    exact_left = _piecewise_linear_integral(1.0, duration, 5.0, 2.0, +1.0)
    # Right: inward power has a minus sign; negative flux uses reservoir mu=3,
    # positive flux uses cell mu=7.
    exact_right = _piecewise_linear_integral(1.5, duration, 3.0, 7.0, -1.0)
    exact_chemical = (exact_left + exact_right) * area
    exact_material = ((0.5 * (duration - 1.0) ** 2 - 0.5 * 1.0 ** 2)
                      - (0.5 * (duration - 1.5) ** 2 - 0.5 * 1.5 ** 2)) * area

    refinements = []
    for n in counts:
        times = tuple(duration * i / n for i in range(n + 1))
        chemical = 0.0
        material = 0.0
        for ta, tb in zip(times[:-1], times[1:]):
            result = reconstruct_p27_25_p24_step(
                _snapshot(ta),
                {"converged": True,
                 "pressure_snapshot_matches_accepted_state": True,
                 "last_snapshot": _snapshot(tb)},
                tb - ta, cell_width_m=1.0, reference_area_m2=area)
            chemical += result["external_work_j"]["mobile_species_chemical_boundary_j"]
            material += sum(result["mobile_species_boundary_transport"][
                "time_integrated_net_inward_mol"])
        refinements.append({
            "subintervals": n,
            "time_support_points": n + 1,
            "left_switch_is_support_point": any(abs(t - 1.0) <= 1e-12 for t in times),
            "right_switch_is_support_point": any(abs(t - 1.5) <= 1e-12 for t in times),
            "chemical_left_j": None,  # separated analytic branch reference below
            "chemical_total_j": chemical,
            "material_total_mol": material,
            "chemical_abs_error_j": abs(chemical - exact_chemical),
            "material_abs_error_mol": abs(material - exact_material),
        })
    return {
        "status": "p27_29_upwind_branch_switch_refinement_audit",
        "duration_s": duration, "reference_area_m2": area,
        "branch_switches_s": {"left": 1.0, "right": 1.5},
        "upwind_rules": {
            "left": "negative flux: left cell potential 5; nonnegative: left reservoir potential 2",
            "right": "negative flux: right reservoir potential 3; nonnegative: right cell potential 7",
        },
        "exact": {
            "chemical_left_j": exact_left * area,
            "chemical_right_j": exact_right * area,
            "chemical_total_j": exact_chemical,
            "material_total_mol": exact_material,
        },
        "refinements": tuple(refinements),
        "interpretation": (
            "A trapezoid interval crossing an upwind sign switch interpolates "
            "across a kink and can incur a branch error. Placing each switch "
            "on the time support splits the branches; subsequent refinement "
            "controls the remaining smooth-branch quadrature error."),
        "not_certified": (
            "full discrete upwind entropy chain rule",
            "actual P24 Newton trajectory integration",
            "solid/bridge and mechanical boundary work",
            "physical reservoir law or physical validation"),
    }
