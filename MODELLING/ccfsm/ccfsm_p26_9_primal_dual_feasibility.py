"""P26.9: primal-dual feasibility orchestration for positive quadratic remapping."""
from __future__ import annotations
from fractions import Fraction
import csv, json
from pathlib import Path
from ccfsm_p26_2_quadratic_projection import _edges
from ccfsm_p26_6_global_positive_projection import globally_coupled_positive_projection
from ccfsm_p26_8_verified_dual_certificate import search_dual_certificate, _F


def _poly_min_exact(m, a, b):
    vals = [m-a/2+b/6, m+a/2+b/6]
    if b > 0:
        x = -a/(2*b)
        if Fraction(-1, 2) <= x <= Fraction(1, 2):
            vals.append(m-a*a/(4*b)-b/12)
    return min(vals)


def _global_moments(edges, means, linear, quadratic):
    mass = first = second = Fraction(0)
    for l, r, m, a, b in zip(edges, edges[1:], means, linear, quadratic):
        h=r-l; c=(l+r)/2
        mass += m*h
        first += m*h*c + a*h*h/12
        second += m*h*(c*c+h*h/12) + a*c*h*h/6 + b*h**3/180
    return mass, first, second


def verify_primal_witness(target_edges, averages, linear, quadratic,
                          target_moments, tolerance=Fraction(1, 10**9)):
    e=tuple(_F(v) for v in target_edges); n=len(e)-1
    u,a,b=(tuple(_F(v) for v in seq) for seq in (averages,linear,quadratic))
    if len(u)!=n or len(a)!=n or len(b)!=n: raise ValueError("one coefficient triple per cell required")
    if any(m<0 for m in u): raise ValueError("cell averages must be nonnegative")
    tol=_F(tolerance)
    if tol<0: raise ValueError("tolerance must be nonnegative")
    mins=[_poly_min_exact(m,aa,bb) for m,aa,bb in zip(u,a,b)]
    actual=_global_moments(e,u,a,b)
    if len(target_moments)!=3: raise ValueError("target_moments must contain mass, first and second moments")
    target=tuple(_F(v) for v in target_moments)
    residuals=tuple(x-y for x,y in zip(actual,target))
    bounds=tuple(tol*max(Fraction(1),abs(y)) for y in target)
    positivity=all(v>=0 for v in mins); moments_ok=all(abs(r)<=bound for r,bound in zip(residuals,bounds))
    return {"verified":positivity and moments_ok,"cellwise_nonnegative_exact":positivity,
      "moment_residuals_exact":[str(v) for v in residuals],"moment_residual_bounds":[str(v) for v in bounds],
      "minimum_cell_values_exact":[str(v) for v in mins],"mass_exact":str(actual[0]),
      "target_moments_exact":[str(v) for v in target],
      "verification":"exact rational positivity and exact rational residual-bound comparison"}


def assess_primal_dual_feasibility(target_edges, averages, linear, quadratic,
                                   weights=(1.0,1.0), max_iterations=20000,
                                   tolerance=2e-11, max_direction=12, dual_sqrt_digits=30):
    e=tuple(_F(v) for v in _edges(target_edges,"target_edges")); n=len(e)-1
    u=tuple(_F(v) for v in averages); a=tuple(_F(v) for v in linear); b=tuple(_F(v) for v in quadratic)
    if len(u)!=n or len(a)!=n or len(b)!=n: raise ValueError("one coefficient triple per cell required")
    if any(m<0 for m in u): raise ValueError("cell averages must be nonnegative")
    original=_global_moments(e,u,a,b)
    dual=search_dual_certificate(e,u,a,b,max_direction,dual_sqrt_digits)
    if dual["verified"]:
        return {"status":"certified_infeasible","proof_level":"rigorous rational dual separation",
          "dual_certificate":dual["certificate"],"primal_attempted":False,
          "meaning":"No cellwise nonnegative quadratic reconstruction with these fixed means can match both target higher moments."}
    try:
        result,diag=globally_coupled_positive_projection(e,u,a,b,weights,max_iterations,tolerance)
    except (ArithmeticError,ValueError) as exc:
        return {"status":"unresolved","proof_level":"none","dual_search":dual,"primal_error":str(exc),
          "meaning":"No dual separator was found in the finite search and no primal witness was obtained."}
    witness=verify_primal_witness(e,result[0],result[1],result[2],original,Fraction(str(tolerance)))
    if witness["verified"]:
        return {"status":"feasible_verified_primal_witness",
          "proof_level":"exact rational positivity; rationally bounded moment residuals",
          "primal_witness":{"averages":[str(_F(v)) for v in result[0]],
            "linear":[str(_F(v)) for v in result[1]],"quadratic":[str(_F(v)) for v in result[2]],
            "verification":witness},"projection_diagnostics":diag,"dual_search":dual,
          "meaning":"A cellwise nonnegative rational-decimal reconstruction was verified; global moments match within the stated rational tolerance."}
    return {"status":"unresolved","proof_level":"none","primal_candidate_verification":witness,
      "projection_diagnostics":diag,"dual_search":dual,
      "meaning":"The numerical projection returned a candidate, but independent rational witness checks did not pass."}


def run_study(output_dir):
    out=Path(output_dir); out.mkdir(parents=True,exist_ok=True)
    cases=[
      ("already_positive",(0.,.4,1.),(1.,.8),(0.,0.),(0.,0.)),
      ("zero_inventory_nonzero_modes",(0.,.4,1.),(0.,0.),(1.,0.),(0.,0.)),
      ("projection_stress",(0.,.3,.7,1.),(1.,.8,1.2),(3.,-2.,2.5),(0.,2.5,0.))]
    rows=[]
    for name,e,u,a,b in cases:
        r=assess_primal_dual_feasibility(e,u,a,b)
        rows.append({"case":name,"status":r["status"],"proof_level":r["proof_level"]})
    with (out/"p26_9_primal_dual_feasibility.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    summary={"scope":"1-D fixed-cell-mean, globally moment-constrained nonnegative quadratic reconstruction",
      "cases":rows,"status_semantics":{
       "certified_infeasible":"rigorous rational dual separator",
       "feasible_verified_primal_witness":"exact rational cellwise positivity and rationally bounded global-moment residuals",
       "unresolved":"neither a dual proof nor an independently verified primal witness"},
      "limitations":["finite dual direction search can miss an existing separator",
       "primal global-moment equalities are verified within an explicit rational tolerance, not necessarily exactly",
       "1-D intervals, fixed cell means and quadratic reconstructions only",
       "floating-point Dykstra projection proposes the candidate; rational post-verification checks returned decimal coefficients",
       "no 2-D/3-D extension and no physical validation"]}
    (out/"summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    print(json.dumps(summary,indent=2)); return summary


if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser(); p.add_argument("--output-dir",default="ccfsm-p26-9-results")
    run_study(p.parse_args().output_dir)
