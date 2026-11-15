"""P27.31: adaptive midpoint sampling for hidden upwind flux events.

P27.30 detects roots only in supplied samples. P27.31 adds bounded recursive
midpoint sampling driven by sign changes and midpoint curvature defects, then
uses the P27.30 interpolator to localize detected roots. This is a numerical
event-finding heuristic, not a certified root-isolation algorithm.
"""
from __future__ import annotations

import math

from ccfsm_p27_30_event_aware_time_support import detect_zero_crossings


def _finite(value, name):
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(name + " must be finite")
    return value


def adaptive_flux_samples(
    flux_functions, start_s, end_s, *, initial_intervals=1,
    curvature_atol=1e-4, curvature_rtol=1e-3, max_depth=12,
    zero_tolerance=1e-12,
):
    """Adaptively sample flux callables; return one shared time grid and values.

    Each callable has signature f(time_s)->flux. An interval is bisected when
    a midpoint changes sign relative to either endpoint or its deviation from
    the endpoint-linear midpoint exceeds atol + rtol*local_scale. A detected
    sign-changing bracket is refined to max_depth for root localization.
    """
    start, end = _finite(start_s, "start_s"), _finite(end_s, "end_s")
    atol, rtol, ztol = (_finite(curvature_atol, "curvature_atol"),
                        _finite(curvature_rtol, "curvature_rtol"),
                        _finite(zero_tolerance, "zero_tolerance"))
    n, depth_limit = int(initial_intervals), int(max_depth)
    if end <= start or n < 1 or depth_limit < 1 or atol < 0 or rtol < 0 or ztol <= 0:
        raise ValueError("invalid interval, refinement, or tolerance settings")
    functions = tuple(flux_functions)
    if not functions or any(not callable(fn) for fn in functions):
        raise ValueError("flux_functions must contain callable functions")

    cache = {}

    def evaluate(t):
        if t not in cache:
            vals = tuple(_finite(fn(t), "flux value") for fn in functions)
            cache[t] = vals
        return cache[t]

    accepted_times = set()

    def refine(a, b, va, vb, depth):
        # Do not evaluate beyond the requested recursion depth. In particular,
        # max_depth=0 would leave only the supplied base grid.
        if depth >= depth_limit:
            return
        mid = 0.5 * (a + b)
        vm = evaluate(mid)
        split = any(
            ((fa < -ztol and fm > ztol) or (fa > ztol and fm < -ztol)
             or (fm < -ztol and fb > ztol) or (fm > ztol and fb < -ztol)
             or abs(fm - 0.5 * (fa + fb)) >
                atol + rtol * max(abs(fa), abs(fm), abs(fb), 1.0))
            for fa, fm, fb in zip(va, vm, vb)
        )
        if split:
            accepted_times.add(mid)
            refine(a, mid, va, vm, depth + 1)
            refine(mid, b, vm, vb, depth + 1)

    base = tuple(start + (end - start) * i / n for i in range(n + 1))
    accepted_times.update(base)
    for t in base:
        evaluate(t)
    for a, b in zip(base[:-1], base[1:]):
        refine(a, b, cache[a], cache[b], 0)
    # Midpoints inspected but not needed for refinement remain in the
    # evaluation cache only; they are not reported as accepted grid nodes.
    times = tuple(sorted(accepted_times))
    histories = tuple(tuple(cache[t][k] for t in times)
                      for k in range(len(functions)))
    return {
        "sample_times_s": times,
        "flux_samples": histories,
        "evaluations": len(times),
        "initial_intervals": n,
        "max_depth": depth_limit,
        "sampling_rule": "recursive midpoint sign/curvature refinement",
    }


def audit_p27_31_adaptive_event_detection(
    start_s=0.0, end_s=2.0, *, initial_intervals=1,
    curvature_atol=1e-4, curvature_rtol=1e-3, max_depth=12,
    zero_tolerance=1e-10,
):
    """Demonstrate detection of two roots hidden inside a same-sign bracket."""
    # A smooth manufactured flux with two roots but positive endpoint values.
    hidden_pair = lambda t: (t - 0.35) * (t - 0.75)
    linear_left = lambda t: t - 1.0
    linear_right = lambda t: t - 1.5
    sampled = adaptive_flux_samples(
        (hidden_pair, linear_left, linear_right), start_s, end_s,
        initial_intervals=initial_intervals,
        curvature_atol=curvature_atol, curvature_rtol=curvature_rtol,
        max_depth=max_depth, zero_tolerance=zero_tolerance)
    roots = detect_zero_crossings(
        sampled["sample_times_s"], sampled["flux_samples"],
        tolerance=zero_tolerance)
    return {
        "status": "p27_31_adaptive_flux_event_detection_audit",
        "sampled": sampled,
        "detected_roots_by_flux_s": roots,
        "manufactured_exact_roots_s": ((0.35, 0.75), (1.0,), (1.5,)),
        "hidden_pair_endpoint_values": (hidden_pair(float(start_s)),
                                        hidden_pair(float(end_s))),
        "root_abs_errors_s": tuple(
            tuple(abs(a - b) for a, b in zip(found, exact))
            if len(found) == len(exact) else ()
            for found, exact in zip(roots, ((0.35, 0.75), (1.0,), (1.5,)))),
        "interpretation": (
            "Midpoint curvature refinement exposed a two-root event pair "
            "whose coarse-interval endpoint fluxes have the same sign."),
        "not_certified": (
            "arbitrary oscillatory fluxes or roots hidden beyond max_depth",
            "rigorous interval-arithmetic root isolation",
            "full discrete upwind entropy chain rule",
            "actual P24 Newton trajectory integration",
            "physical reservoir law or physical validation"),
    }
