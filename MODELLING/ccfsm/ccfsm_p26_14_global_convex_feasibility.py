"""P26.14: globally coupled convex feasibility with exact conic verification."""
from __future__ import annotations
from fractions import Fraction
from ccfsm_p26_6_global_positive_projection import globally_coupled_positive_projection
from ccfsm_p26_8_verified_dual_certificate import _F
from ccfsm_p26_10_exact_moment_witness import _targets
from ccfsm_p26_12_exact_affine_parameterization import search_rational_positive_witness, build_exact_affine_parameterization
from ccfsm_p26_13_markov_lukacs_socp import verify_global_candidate


def solve_global_convex_feasibility(target_edges, averages, linear, quadratic,
        weights=(1.0,1.0), max_iterations=20000, tolerance=2e-11,
        denominators=(1,10,100), offset_radius=1, max_candidates=20000):
    """Numerical convex candidate generation followed by exact rational proof."""
    edges=tuple(_F(v) for v in target_edges)
    means=tuple(_F(v) for v in averages)
    a0=tuple(_F(v) for v in linear); b0=tuple(_F(v) for v in quadratic)
    if len(edges)!=len(means)+1 or len(a0)!=len(means) or len(b0)!=len(means):
        raise ValueError("one mean and modal coefficient pair per target cell required")
    if not means or any(v<0 for v in means):
        raise ValueError("at least one cell and nonnegative fixed means required")
    if len(weights)!=2 or any(not float(v)>0 for v in weights):
        raise ValueError("two positive modal weights required")
    target,_modal_rhs=_targets(edges,means,a0,b0)
    try:
        projected,projection=globally_coupled_positive_projection(
            edges,means,a0,b0,weights=weights,max_iterations=max_iterations,tolerance=tolerance)
    except (ArithmeticError,ValueError) as exc:
        return {"status":"unresolved","verified":False,"stage":"numerical_convex_projection",
                "reason":str(exc),"meaning":"No numerical candidate; not an infeasibility proof.",
                "target_moments_exact":target}
    _,pa,pb=projected
    rational=search_rational_positive_witness(
        edges,means,pa,pb,target_moments=target,denominators=denominators,
        offset_radius=offset_radius,max_candidates=max_candidates,significant_digits=15)
    if rational["status"]!="feasible_exact_primal_witness":
        return {"status":"unresolved","verified":False,"stage":"exact_rational_reconstruction",
                "meaning":"No exact rational witness found within the finite search budget; feasibility unresolved.",
                "projection":projection,"rational_search":rational["search"],"target_moments_exact":target}
    chart=build_exact_affine_parameterization(edges,means,target)
    exact=verify_global_candidate(chart,rational["linear"],rational["quadratic"])
    if not exact["verified"]:
        raise ArithmeticError("internal error: exact conic verification rejected rational witness")
    return {"status":"feasible_exact_primal_witness","verified":True,
            "stage":"exact_markov_lukacs_verification","linear":rational["linear"],
            "quadratic":rational["quadratic"],"free_coordinates":rational["free_coordinates"],
            "pivot_coordinates":rational["pivot_coordinates"],"target_moments_exact":target,
            "exact_certificate":exact,"projection":projection,"rational_search":rational["search"],
            "proof_level":"exact rational three moments and continuous cellwise nonnegativity"}


def run_study():
    ok=solve_global_convex_feasibility((0,Fraction(1,2),1),(2,2),(0,0),(0,0),
                                      denominators=(1,),offset_radius=0)
    no=solve_global_convex_feasibility((0,1),(Fraction(1,10),),(1,),(0,),
                                      denominators=(1,),offset_radius=0)
    return {"scope":"1-D fixed-mean globally moment-constrained piecewise quadratics",
            "cases":[{"case":"positive_constant_two_cells","status":ok["status"],"verified":ok["verified"]},
                     {"case":"fixed_negative_single_cell","status":no["status"],"verified":no["verified"]}],
            "method":"Dykstra candidate projection + P26.12 exact affine rational reconstruction + P26.13 Markov-Lukacs certificates",
            "decision_rule":"Only exact rational primal witnesses are feasible; all failures are unresolved, never infeasible.",
            "limitations":["finite rational search is incomplete","no dual infeasibility certificate; see P26.8/P26.9",
                           "1-D, fixed nonnegative means, quadratic profiles only","numerical projection is candidate generation, not proof",
                           "no physical validation"]}


if __name__=="__main__":
    import json
    print(json.dumps(run_study(),indent=2,default=str))
