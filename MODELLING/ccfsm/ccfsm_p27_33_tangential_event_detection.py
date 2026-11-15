"""P27.33: quadratic candidate search for tangential flux roots.

P27.31's sign-change detector and P27.32's bisection do not cover even-
multiplicity roots. P27.33 fits local quadratics to three consecutive
adaptive samples, evaluates each in-interval vertex with the original flux,
and reports near-zero stationary candidates separately from sign-change roots.
This is a diagnostic detector, not a completeness certificate.
"""
from __future__ import annotations

import math

from ccfsm_p27_31_adaptive_event_detection import adaptive_flux_samples
from ccfsm_p27_32_safeguarded_event_refinement import _brackets, refine_flux_root_bisection


def _finite(value, name):
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(name + " must be finite")
    return value


def quadratic_tangency_candidates(times, values, flux, *, flux_tolerance=1e-10,
                                  curvature_tolerance=1e-14):
    """Find sampled local quadratic vertices that are near-zero in the true flux.

    The quadratic is interpolated through each consecutive triple with
    nonuniform-time divided differences. Only an in-range vertex is evaluated.
    A candidate is retained only when the original callable, not just the
    interpolant, is within flux_tolerance at that vertex.
    """
    if not callable(flux):
        raise ValueError("flux must be callable")
    ts, ys = tuple(map(float, times)), tuple(map(float, values))
    ftol = _finite(flux_tolerance, "flux_tolerance")
    ctol = _finite(curvature_tolerance, "curvature_tolerance")
    if len(ts) != len(ys) or len(ts) < 3 or ftol < 0 or ctol < 0:
        raise ValueError("need at least three paired samples and nonnegative tolerances")
    if any(not math.isfinite(x) for x in ts + ys):
        raise ValueError("sample values must be finite")
    if any(b <= a for a, b in zip(ts[:-1], ts[1:])):
        raise ValueError("sample times must be strictly increasing")

    candidates = []
    for i in range(len(ts)-2):
        x0, x1, x2 = ts[i:i+3]
        y0, y1, y2 = ys[i:i+3]
        d01 = (y1-y0)/(x1-x0)
        d12 = (y2-y1)/(x2-x1)
        a2 = (d12-d01)/(x2-x0)
        if abs(a2) <= ctol:
            continue
        b1 = d01 - a2*(x0+x1)
        vertex = -b1/(2.0*a2)
        if not (x0 <= vertex <= x2):
            continue
        actual = _finite(flux(vertex), "candidate flux")
        if abs(actual) <= ftol:
            item = {"time_s": vertex, "flux_value": actual,
                    "triple_interval_s": (x0, x2),
                    "quadratic_coefficient": a2,
                    "classification": "near_zero_tangential_candidate"}
            if not candidates or abs(vertex-candidates[-1]["time_s"]) > 1e-9:
                candidates.append(item)
    return tuple(candidates)


def audit_p27_33_tangential_event_detection(
    start_s=0.0, end_s=1.0, *, tangency_time_s=0.37,
    initial_intervals=1, curvature_atol=1e-4, curvature_rtol=1e-3,
    max_depth=12, time_tolerance=1e-10, flux_tolerance=1e-10,
):
    """Contrast an even-multiplicity root with a conventional sign-change pair."""
    tangent = lambda t: (t-tangency_time_s)**2
    crossing_pair = lambda t: (t-0.23)*(t-0.81)
    functions = (tangent, crossing_pair)
    sampled = adaptive_flux_samples(
        functions, start_s, end_s, initial_intervals=initial_intervals,
        curvature_atol=curvature_atol, curvature_rtol=curvature_rtol,
        max_depth=max_depth, zero_tolerance=flux_tolerance)
    times = sampled["sample_times_s"]
    tangencies = quadratic_tangency_candidates(
        times, sampled["flux_samples"][0], tangent,
        flux_tolerance=flux_tolerance)
    crossing_brackets = _brackets(
        times, sampled["flux_samples"][1], flux_tolerance)
    refined_crossings = tuple(
        refine_flux_root_bisection(
            crossing_pair, a, b, time_tolerance=time_tolerance,
            flux_tolerance=flux_tolerance)
        for a, b in crossing_brackets if a != b
    )
    return {
        "status": "p27_33_tangential_event_detection_audit",
        "sampled": sampled,
        "tangential_candidates": tangencies,
        "tangential_exact_root_s": tangency_time_s,
        "sign_change_brackets": crossing_brackets,
        "refined_sign_change_roots": refined_crossings,
        "tangential_candidate_found": bool(tangencies),
        "maximum_tangential_candidate_error_s": max(
            (abs(item["time_s"]-tangency_time_s) for item in tangencies),
            default=None),
        "guarantee_scope": (
            "A reported candidate is evaluated in the original flux; a small "
            "residual is evidence for this manufactured case, not a proof of root."),
        "not_certified": (
            "three-point quadratic fits can miss or misclassify nonquadratic tangencies",
            "finite samples do not guarantee discovery of every stationary point",
            "no derivative enclosure or interval arithmetic",
            "no complete upwind entropy proof, P24 trajectory integration, "
            "or physical validation"),
    }
