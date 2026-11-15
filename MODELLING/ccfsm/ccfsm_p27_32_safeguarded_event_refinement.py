"""P27.32: safeguarded bisection refinement of adaptive flux-event brackets.

P27.31 supplies an adaptive sample grid. P27.32 refines each observed
sign-changing bracket by bisection and reports the final bracket width and
flux residual. Certification is conditional on continuity and a valid sign
bracket; adaptive sampling itself is not a proof that every root was found.
"""
from __future__ import annotations

import math

from ccfsm_p27_31_adaptive_event_detection import adaptive_flux_samples


def _finite(value, name):
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(name + " must be finite")
    return value


def refine_flux_root_bisection(
    flux, left_s, right_s, *, time_tolerance=1e-10,
    flux_tolerance=1e-10, max_iterations=100,
):
    """Refine one continuous sign-changing bracket by safeguarded bisection."""
    if not callable(flux):
        raise ValueError("flux must be callable")
    a, b = _finite(left_s, "left_s"), _finite(right_s, "right_s")
    xtol, ftol = (_finite(time_tolerance, "time_tolerance"),
                  _finite(flux_tolerance, "flux_tolerance"))
    limit = int(max_iterations)
    if b <= a or xtol <= 0 or ftol < 0 or limit < 1:
        raise ValueError("invalid bracket, tolerance, or iteration limit")

    fa = _finite(flux(a), "left flux")
    fb = _finite(flux(b), "right flux")
    if abs(fa) <= ftol:
        return {"root_s": a, "bracket_s": (a, a), "bracket_width_s": 0.0,
                "flux_residual": abs(fa), "iterations": 0,
                "converged": True, "termination": "left_endpoint"}
    if abs(fb) <= ftol:
        return {"root_s": b, "bracket_s": (b, b), "bracket_width_s": 0.0,
                "flux_residual": abs(fb), "iterations": 0,
                "converged": True, "termination": "right_endpoint"}
    if fa * fb >= 0.0:
        raise ValueError("root refinement requires a strict sign-changing bracket")

    best_t, best_f = (a, fa) if abs(fa) < abs(fb) else (b, fb)
    for iteration in range(1, limit + 1):
        mid = a + 0.5 * (b - a)
        fm = _finite(flux(mid), "midpoint flux")
        if abs(fm) < abs(best_f):
            best_t, best_f = mid, fm
        if fm == 0.0:
            return {"root_s": mid, "bracket_s": (mid, mid),
                    "bracket_width_s": 0.0, "flux_residual": 0.0,
                    "iterations": iteration, "converged": True,
                    "termination": "exact_midpoint"}
        if fa * fm < 0.0:
            b, fb = mid, fm
        else:
            a, fa = mid, fm
        if b-a <= xtol:
            return {"root_s": best_t, "bracket_s": (a, b),
                    "bracket_width_s": b-a, "flux_residual": abs(best_f),
                    "iterations": iteration, "converged": True,
                    "termination": "time_bracket"}
    return {"root_s": best_t, "bracket_s": (a, b),
            "bracket_width_s": b-a, "flux_residual": abs(best_f),
            "iterations": limit, "converged": False,
            "termination": "iteration_limit"}


def _brackets(times, values, flux_tolerance):
    found = []
    for a, b, fa, fb in zip(times[:-1], times[1:], values[:-1], values[1:]):
        if abs(fa) <= flux_tolerance:
            found.append((a, a))
        elif fa * fb < 0.0:
            found.append((a, b))
        elif abs(fb) <= flux_tolerance:
            found.append((b, b))
    unique = []
    for bracket in found:
        if not unique or bracket != unique[-1]:
            unique.append(bracket)
    return tuple(unique)


def audit_p27_32_safeguarded_event_refinement(
    start_s=0.0, end_s=2.0, *, initial_intervals=1,
    curvature_atol=1e-4, curvature_rtol=1e-3, max_depth=12,
    time_tolerance=1e-10, flux_tolerance=1e-10, max_iterations=100,
):
    """Refine all brackets exposed by P27.31 for a manufactured flux set."""
    functions = (
        lambda t: (t-0.35)*(t-0.75),
        lambda t: t-1.0,
        lambda t: t-1.5,
    )
    sampled = adaptive_flux_samples(
        functions, start_s, end_s, initial_intervals=initial_intervals,
        curvature_atol=curvature_atol, curvature_rtol=curvature_rtol,
        max_depth=max_depth, zero_tolerance=flux_tolerance)
    times = sampled["sample_times_s"]
    results = []
    for fn, values in zip(functions, sampled["flux_samples"]):
        roots = []
        for a, b in _brackets(times, values, flux_tolerance):
            if a == b:
                roots.append({"root_s": a, "bracket_s": (a, a),
                              "bracket_width_s": 0.0, "flux_residual": abs(fn(a)),
                              "iterations": 0, "converged": True,
                              "termination": "sampled_zero"})
            else:
                roots.append(refine_flux_root_bisection(
                    fn, a, b, time_tolerance=time_tolerance,
                    flux_tolerance=flux_tolerance,
                    max_iterations=max_iterations))
        results.append(tuple(roots))
    exact = ((0.35, 0.75), (1.0,), (1.5,))
    return {
        "status": "p27_32_safeguarded_event_refinement_audit",
        "sampled": sampled,
        "refined_roots_by_flux": tuple(results),
        "manufactured_exact_roots_s": exact,
        "all_brackets_converged": all(
            root["converged"] for group in results for root in group),
        "maximum_final_bracket_width_s": max(
            (root["bracket_width_s"] for group in results for root in group),
            default=0.0),
        "maximum_flux_residual": max(
            (root["flux_residual"] for group in results for root in group),
            default=0.0),
        "guarantee_scope": (
            "Bisection preserves a strict sign-changing bracket for a continuous "
            "scalar flux; reported bracket width is an a posteriori time enclosure."),
        "not_certified": (
            "adaptive sampling may miss roots not exposed as brackets",
            "continuity is assumed, not verified by finite samples",
            "floating-point interval arithmetic is not used",
            "no full discrete entropy proof, P24 trajectory integration, "
            "or physical validation"),
    }
