"""P26.16: stability and completeness audit for exact dual searches."""
from __future__ import annotations
import csv, json
from pathlib import Path
from fractions import Fraction
from ccfsm_p26_8_verified_dual_certificate import _sqrt_upper, verify_dual_certificate
from ccfsm_p26_15_global_primal_dual import search_global_dual_separator

def audit_sqrt_enclosure(value, digit_levels=(4, 8, 16, 32, 48)):
    x = Fraction(value)
    if x < 0: raise ValueError("square-root argument must be nonnegative")
    levels = tuple(digit_levels)
    if not levels or any(not isinstance(d, int) or d < 1 or d > 100 for d in levels):
        raise ValueError("digit_levels must contain integers in [1,100]")
    if tuple(sorted(set(levels))) != levels: raise ValueError("digit_levels must be strictly increasing")
    rows, previous = [], None
    for digits in levels:
        upper = _sqrt_upper(x, digits)
        if previous is not None and upper > previous:
            raise ArithmeticError("nested decimal square-root upper bounds must not increase")
        rows.append({"digits": digits, "upper": str(upper),
                     "exact_square_check": upper * upper == x,
                     "error_bound": str(Fraction(1, 10**digits))})
        previous = upper
    return {"radicand": str(x), "rows": rows, "monotone_nonincreasing": True}

def audit_fixed_direction(target_edges, averages, linear, quadratic, direction,
                          digit_levels=(4, 8, 16, 32, 48)):
    levels = tuple(digit_levels)
    if not levels or tuple(sorted(set(levels))) != levels:
        raise ValueError("digit_levels must be strictly increasing")
    rows, previous_gap = [], None
    for digits in levels:
        cert = verify_dual_certificate(target_edges, averages, linear, quadratic,
                                       direction, sqrt_digits=digits)
        gap = Fraction(cert["gap_lower_bound"])
        if previous_gap is not None and gap < previous_gap:
            raise ArithmeticError("certified gap lower bound must not decrease with precision")
        rows.append({"sqrt_digits": digits, "verified": cert["verified"],
                     "gap_lower_bound": str(gap), "direction": cert["direction"],
                     "support_upper_bound": cert["support_upper_bound"]})
        previous_gap = gap
    return {"rows": rows, "gap_lower_bound_monotone": True,
            "verified_at_all_levels": all(r["verified"] for r in rows)}

def audit_direction_radii(target_edges, averages, linear, quadratic,
                          direction_bounds=(1, 2, 4, 8, 16), sqrt_digits=40):
    bounds = tuple(direction_bounds)
    if not bounds or any(not isinstance(n, int) or n < 1 or n > 1000 for n in bounds):
        raise ValueError("direction_bounds must be integers in [1,1000]")
    if tuple(sorted(set(bounds))) != bounds: raise ValueError("direction_bounds must be strictly increasing")
    rows, previous = [], None
    for bound in bounds:
        result = search_global_dual_separator(target_edges, averages, linear, quadratic,
                                              max_direction=bound, sqrt_digits=sqrt_digits)
        gap = Fraction(result["certificate"]["gap_lower_bound"]) if result["verified"] else None
        if previous is not None and gap is not None and gap < previous:
            raise ArithmeticError("best certified gap cannot decrease on nested direction sets")
        rows.append({"max_direction": bound, "directions_checked": result["directions_checked"],
                     "status": result["status"], "verified": result["verified"],
                     "first_certifying_shell": result["first_certifying_shell"],
                     "best_certificate_shell": result.get("best_certificate_shell"),
                     "direction": result.get("certificate", {}).get("direction"),
                     "gap_lower_bound": str(gap) if gap is not None else None})
        if gap is not None: previous = gap
    return {"rows": rows, "nested_search": True,
            "certificate_found_by_largest_radius": bool(rows[-1]["verified"])}

def support_gap_error_bound(averages, sqrt_digits):
    if not isinstance(sqrt_digits, int) or not 1 <= sqrt_digits <= 100:
        raise ValueError("sqrt_digits must be an integer in [1,100]")
    means = tuple(Fraction(x) for x in averages)
    if any(m < 0 for m in means): raise ValueError("cell averages must be nonnegative")
    return 6 * sum(means, Fraction(0)) / (10**sqrt_digits)

def run_study(output_dir):
    out = Path(output_dir); out.mkdir(parents=True, exist_ok=True)
    cases = [
        ("zero_inventory_nonzero_modes", (0, Fraction(2,5), 1), (0,0), (1,0), (0,0)),
        ("positive_means_zero_modes", (0, Fraction(2,5), 1), (1,Fraction(7,10)), (0,0), (0,0)),
        ("positive_means_negative_modes", (0, Fraction(2,5), 1), (1,Fraction(4,5)), (8,-7), (0,0)),
    ]
    rows, details = [], {}
    for name, edges, means, linear, quadratic in cases:
        audit = audit_direction_radii(edges, means, linear, quadratic)
        details[name] = audit
        rows.append({"case": name, "status_at_max_radius": audit["rows"][-1]["status"],
                     "first_certifying_shell": next((r["first_certifying_shell"] for r in audit["rows"] if r["verified"]), None),
                     "max_radius": audit["rows"][-1]["max_direction"],
                     "directions_checked": audit["rows"][-1]["directions_checked"]})
    with (out / "p26_16_dual_search_stability.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    sqrt_audit = audit_sqrt_enclosure(Fraction(7,12))
    fixed = audit_fixed_direction((0, Fraction(2,5), 1), (0,0), (1,0), (0,0), (1,0))
    summary = {
        "scope": "exact rational dual certificates for 1-D fixed-mean quadratic profiles",
        "direction_radius_audits": details, "sqrt_enclosure_audit": sqrt_audit,
        "fixed_direction_precision_audit": fixed,
        "support_overestimate_bound_example": str(support_gap_error_bound((0,0), 40)),
        "mathematical_completeness": {
            "infinite_search": "If the target moment vector lies outside the compact convex attainable set, strict separation gives a positive gap. Continuity of the support function makes the strict-separator directions an open set; rational directions are dense, and every rational direction can be scaled to a primitive integer pair. Thus exhaustive enumeration of all primitive integer directions eventually finds a separator.",
            "finite_search": "Any finite L-infinity radius can miss the open set of separating directions. No certificate within a finite radius is not a feasibility proof.",
            "inside_set": "If the target lies in the attainable set, no strict separating direction exists."},
        "limitations": ["completeness concerns infinite exact-arithmetic enumeration, not a finite computation",
            "decimal square-root upper bounds certify the exact rationalized input data",
            "the precision error bound concerns only support overestimation from square-root enclosure",
            "1-D intervals, fixed nonnegative cell means, and quadratic profiles only",
            "no physical or experimental validation"]}
    (out / "summary.json").write_text(json.dumps(summary, indent=2, default=str), encoding="utf-8")
    print(json.dumps(summary, indent=2, default=str)); return summary

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(); p.add_argument("--output-dir", default="ccfsm-p26-16-results")
    run_study(p.parse_args().output_dir)
