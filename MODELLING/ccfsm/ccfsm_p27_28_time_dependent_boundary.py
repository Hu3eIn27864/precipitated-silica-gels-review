"""P27.28: time-dependent analytic boundary references for the P27.25 adapter.

Endpoint trapezoids are compared with exact polynomial time integrals.
This quantifies separate material-transfer and boundary-work quadrature
errors on synthetic data; it is not a P24 trajectory or physical validation.
"""
from __future__ import annotations

from ccfsm_p27_25_snapshot_integrals import reconstruct_p27_25_p24_step


def _poly_value(coefficients, t):
    return sum(float(c) * t**i for i, c in enumerate(coefficients))


def _poly_integral(coefficients, duration):
    return sum(float(c) * duration**(i + 1) / (i + 1)
               for i, c in enumerate(coefficients))


def _product_integral(left, right, duration):
    product = [0.0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            product[i + j] += float(a) * float(b)
    return _poly_integral(product, duration)


def _snapshot(t, *, flux_left, flux_right, mu_left, mu_right, hydraulic):
    # No advection: total mobile flux is purely diffusive at both faces.
    tr = {
        "reaction_dissipation_w_m3_reference": (0.0,),
        "darcy_internal_dissipation_w_m2": 0.0,
        "mobile_species_onsager_diffusive_dissipation_w_m2": (0.0, 0.0),
        "reservoir_hydraulic_power_w_m2": _poly_value(hydraulic, t),
        "mobile_species_advective_face_fluxes_mol_m2_s": ((0.0, 0.0), (0.0, 0.0)),
        "mobile_species_face_fluxes_mol_m2_s": (
            (_poly_value(flux_left, t), _poly_value(flux_right, t)),
            (0.0, 0.0)),
        "mobile_species_chemical_potential_j_mol": ((0.0, 0.0), (0.0, 0.0)),
        "onsager_reservoir_chemical_potential_left_j_mol": (
            _poly_value(mu_left, t), 0.0),
        "onsager_reservoir_chemical_potential_right_j_mol": (
            _poly_value(mu_right, t), 0.0),
    }
    return {"transport_rhs": tr}


def audit_p27_28_time_dependent_boundary_case(
    duration_s=2.0, area_m2=1.5, tolerance=1e-12,
):
    """Compare P27.25 endpoint trapezoids to exact polynomial integrals."""
    duration, area, tol = float(duration_s), float(area_m2), float(tolerance)
    if duration <= 0 or area <= 0 or tol <= 0:
        raise ValueError("duration, area and tolerance must be positive")

    # Quadratic diffusive fluxes and linear reservoir potentials. Their
    # products are cubic, so endpoint trapezoids have a measurable error.
    flux_left = (1.0, 0.2, 0.1)
    flux_right = (0.4, -0.1, 0.05)
    mu_left = (5.0, 0.3)
    mu_right = (3.0, -0.2)
    hydraulic = (2.0, 0.5, 0.2)

    initial = _snapshot(0.0, flux_left=flux_left, flux_right=flux_right,
                        mu_left=mu_left, mu_right=mu_right, hydraulic=hydraulic)
    final = _snapshot(duration, flux_left=flux_left, flux_right=flux_right,
                      mu_left=mu_left, mu_right=mu_right, hydraulic=hydraulic)
    reconstructed = reconstruct_p27_25_p24_step(
        initial, {"converged": True,
                  "pressure_snapshot_matches_accepted_state": True,
                  "last_snapshot": final},
        duration, cell_width_m=1.0, reference_area_m2=area)

    exact_material_rate = (_poly_integral(flux_left, duration)
                           - _poly_integral(flux_right, duration))
    exact_material = exact_material_rate * area
    exact_chemical_rate = (_product_integral(mu_left, flux_left, duration)
                           - _product_integral(mu_right, flux_right, duration))
    exact_chemical = exact_chemical_rate * area
    exact_hydraulic = _poly_integral(hydraulic, duration) * area

    observed_material = reconstructed[
        "mobile_species_boundary_transport"]["time_integrated_net_inward_mol"][0]
    observed_chemical = reconstructed["external_work_j"][
        "mobile_species_chemical_boundary_j"]
    observed_hydraulic = reconstructed["external_work_j"]["reservoir_hydraulic_j"]

    expected = {"material_M_mol": exact_material,
                "chemical_boundary_work_j": exact_chemical,
                "hydraulic_boundary_work_j": exact_hydraulic}
    observed = {"material_M_mol": observed_material,
                "chemical_boundary_work_j": observed_chemical,
                "hydraulic_boundary_work_j": observed_hydraulic}
    signed = {key: observed[key] - expected[key] for key in expected}
    absolute = {key: abs(value) for key, value in signed.items()}
    return {
        "status": "p27_28_time_dependent_boundary_quadrature_audit",
        "duration_s": duration, "reference_area_m2": area,
        "time_dependence": "quadratic fluxes; linear potentials; cubic chemical power",
        "exact": expected, "trapezoidal_reconstruction": observed,
        "signed_error": signed, "absolute_error": absolute,
        "material_error_budget_mol": {"M": absolute["material_M_mol"], "O": 0.0},
        "energy_error_budget_j": {
            "chemical_boundary": absolute["chemical_boundary_work_j"],
            "hydraulic_boundary": absolute["hydraulic_boundary_work_j"]},
        "tolerance": tol,
        "within_tolerance": all(value <= tol for value in absolute.values()),
        "quadrature_order_note": (
            "The two-endpoint trapezoid is exact for linear rates, but not "
            "for quadratic material fluxes or cubic potential-flux products."),
        "not_certified": (
            "actual P24 trajectory integration",
            "full upwind entropy chain rule",
            "solid/bridge chemical work and mechanical boundary work",
            "physical reservoir constitutive law and physical validation"),
    }
