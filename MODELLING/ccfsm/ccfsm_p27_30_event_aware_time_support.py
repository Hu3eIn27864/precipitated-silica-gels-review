"""P27.30: event-aware time support for sign-changing upwind boundary fluxes.

Flux zero crossings are detected from sampled boundary-flux histories by
piecewise-linear root interpolation. The event times are inserted into a
uniform base grid before P27.25 step reconstruction. Synthetic references
compare event-aligned and uniform supports; this is not a full entropy proof.
"""
from __future__ import annotations

from ccfsm_p27_25_snapshot_integrals import reconstruct_p27_25_p24_step


def _fluxes(t):
    return (float(t) - 1.0, float(t) - 1.5)


def _snapshot(t):
    left, right = _fluxes(t)
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


def detect_zero_crossings(sample_times, flux_samples, *, tolerance=1e-12):
    """Return linearly interpolated interior roots for each flux history."""
    times = tuple(float(t) for t in sample_times)
    if len(times) < 2 or any(b <= a for a, b in zip(times[:-1], times[1:])):
        raise ValueError("sample_times must be strictly increasing with at least two points")
    if tolerance <= 0:
        raise ValueError("tolerance must be positive")
    roots_by_flux = []
    for samples in flux_samples:
        values = tuple(float(v) for v in samples)
        if len(values) != len(times):
            raise ValueError("each flux history must match sample_times")
        roots = []
        for ta, tb, fa, fb in zip(times[:-1], times[1:], values[:-1], values[1:]):
            if abs(fa) <= tolerance:
                root = ta
            elif fa * fb < 0.0:
                root = ta - fa * (tb - ta) / (fb - fa)
            elif abs(fb) <= tolerance:
                root = tb
            else:
                continue
            if times[0] + tolerance < root < times[-1] - tolerance:
                if not roots or abs(root - roots[-1]) > tolerance:
                    roots.append(root)
        roots_by_flux.append(tuple(roots))
    return tuple(roots_by_flux)


def _piecewise_reference(duration, area):
    # Exact piecewise integrals for jL=t-1 and jR=t-1.5 with
    # the P27.29 upwind potentials and right-face sign convention.
    left = 5.0 * (-0.5) + 2.0 * (0.5 * (duration - 1.0) ** 2)
    right = 3.0 * (0.5 * 1.5 ** 2) - 7.0 * (
        0.5 * (duration - 1.5) ** 2)
    material = (0.5 * (duration - 1.0) ** 2 - 0.5
                - (0.5 * (duration - 1.5) ** 2 - 0.5 * 1.5 ** 2))
    return {"chemical_left_j": left * area,
            "chemical_right_j": right * area,
            "chemical_total_j": (left + right) * area,
            "material_total_mol": material * area}


def _evaluate_support(times, area):
    chemical = material = left_work = right_work = 0.0
    for ta, tb in zip(times[:-1], times[1:]):
        a, b = _snapshot(ta), _snapshot(tb)
        result = reconstruct_p27_25_p24_step(
            a, {"converged": True,
                "pressure_snapshot_matches_accepted_state": True,
                "last_snapshot": b},
            tb - ta, cell_width_m=1.0, reference_area_m2=area)
        chemical += result["external_work_j"]["mobile_species_chemical_boundary_j"]
        material += sum(result["mobile_species_boundary_transport"][
            "time_integrated_net_inward_mol"])
        # Side diagnostics use the same upwind branch convention as P27.29.
        for side, target in (("left", "left"), ("right", "right")):
            fa, fb = _fluxes(ta), _fluxes(tb)
            if side == "left":
                pa = (2.0 if fa[0] >= 0 else 5.0) * fa[0]
                pb = (2.0 if fb[0] >= 0 else 5.0) * fb[0]
                left_work += 0.5 * (pa + pb) * (tb - ta) * area
            else:
                pa = -(7.0 if fa[1] >= 0 else 3.0) * fa[1]
                pb = -(7.0 if fb[1] >= 0 else 3.0) * fb[1]
                right_work += 0.5 * (pa + pb) * (tb - ta) * area
    return {"chemical_total_j": chemical, "chemical_left_j": left_work,
            "chemical_right_j": right_work, "material_total_mol": material}


def audit_p27_30_event_aware_time_support(
    duration_s=2.0, area_m2=1.5, uniform_subintervals=3,
    detection_subintervals=4, tolerance=1e-12,
):
    """Compare a uniform grid with its event-enriched counterpart."""
    duration, area = float(duration_s), float(area_m2)
    n, nd, tol = int(uniform_subintervals), int(detection_subintervals), float(tolerance)
    if duration <= 1.5 or area <= 0 or tol <= 0 or n < 1 or nd < 1:
        raise ValueError("duration must exceed 1.5; area, counts and tolerance must be positive")
    detection_times = tuple(duration * i / nd for i in range(nd + 1))
    sampled = tuple(tuple(_fluxes(t)[k] for t in detection_times) for k in range(2))
    events_by_flux = detect_zero_crossings(detection_times, sampled, tolerance=tol)
    events = tuple(sorted({r for group in events_by_flux for r in group}))
    uniform = tuple(duration * i / n for i in range(n + 1))
    event_aligned = tuple(sorted(set(uniform).union(events)))
    exact = _piecewise_reference(duration, area)

    def row(name, times):
        observed = _evaluate_support(times, area)
        return {"method": name, "subintervals": len(times) - 1,
                "time_support_points": len(times), "support_times_s": times,
                "observed": observed,
                "chemical_abs_error_j": abs(observed["chemical_total_j"] - exact["chemical_total_j"]),
                "material_abs_error_mol": abs(observed["material_total_mol"] - exact["material_total_mol"])}

    uniform_row = row("uniform", uniform)
    event_row = row("event_aligned", event_aligned)
    return {
        "status": "p27_30_event_aware_upwind_time_support_audit",
        "duration_s": duration, "reference_area_m2": area,
        "detected_events_by_flux_s": events_by_flux,
        "inserted_event_times_s": events,
        "exact": exact,
        "comparisons": (uniform_row, event_row),
        "event_detection": "piecewise-linear interpolation between supplied flux samples",
        "interpretation": (
            "Detected zero crossings are inserted into the base time grid, "
            "so no event-aligned interval straddles a detected upwind branch switch. "
            "The remaining quadrature error is assessed independently."),
        "not_certified": (
            "missed multiple roots between detection samples",
            "full discrete upwind entropy chain rule",
            "actual P24 Newton trajectory integration",
            "solid/bridge and mechanical boundary work",
            "physical reservoir law or physical validation"),
    }
