"""P26.15: exact global primal-dual feasibility decision for P26 moments."""
from __future__ import annotations
import csv, json, math
from pathlib import Path
from fractions import Fraction
from ccfsm_p26_8_verified_dual_certificate import verify_dual_certificate
from ccfsm_p26_14_global_convex_feasibility import solve_global_convex_feasibility


def search_global_dual_separator(target_edges, averages, linear, quadratic,
                                 max_direction=24, sqrt_digits=40):
    """Enumerate primitive integer directions by expanding L-infinity shells."""
    if not isinstance(max_direction,int) or not 1<=max_direction<=1000:
        raise ValueError("max_direction must be an integer in [1,1000]")
    if not isinstance(sqrt_digits,int) or not 1<=sqrt_digits<=100:
        raise ValueError("sqrt_digits must be an integer in [1,100]")
    checked=0; best=None; first_shell=None
    for radius in range(1,max_direction+1):
        for i in range(-radius,radius+1):
            for j in range(-radius,radius+1):
                if max(abs(i),abs(j))!=radius or (i==0 and j==0): continue
                if math.gcd(abs(i),abs(j))!=1: continue
                checked+=1
                cert=verify_dual_certificate(target_edges,averages,linear,quadratic,
                    (Fraction(i),Fraction(j)),sqrt_digits=sqrt_digits)
                if cert["verified"]:
                    gap=Fraction(cert["gap_lower_bound"])
                    if first_shell is None: first_shell=radius
                    if best is None or gap>best[0]: best=(gap,radius,cert)
    if best is None:
        return {"status":"no_certificate_found","verified":False,
            "search":"primitive integer directions by expanding L-infinity shells",
            "max_direction":max_direction,"directions_checked":checked,
            "first_certifying_shell":None,"sqrt_digits":sqrt_digits,
            "meaning":"No strict separator in the finite direction set; this does not prove feasibility."}
    gap,radius,cert=best
    return {"status":"certified_infeasible","verified":True,"certificate":cert,
        "search":"primitive integer directions by expanding L-infinity shells",
        "max_direction":max_direction,"directions_checked":checked,
        "first_certifying_shell":first_shell,"best_certificate_shell":radius,
        "sqrt_digits":sqrt_digits,
        "meaning":"A strict rational dual separation gap proves no admissible nonnegative cellwise quadratic profile matches the prescribed moments."}


def assess_global_primal_dual_feasibility(target_edges,averages,linear,quadratic,
        weights=(1.0,1.0),max_direction=24,sqrt_digits=40,max_iterations=20000,
        projection_tolerance=2e-11,denominators=(1,10,100),offset_radius=1,
        max_candidates=20000):
    """Return exact infeasibility, exact feasibility, or unresolved."""
    dual=search_global_dual_separator(target_edges,averages,linear,quadratic,
        max_direction=max_direction,sqrt_digits=sqrt_digits)
    if dual["verified"]:
        return {"status":"certified_infeasible","verified":True,
            "proof_level":"exact rational strict dual separation",
            "dual_certificate":dual,"primal_attempted":False,"meaning":dual["meaning"]}
    primal=solve_global_convex_feasibility(target_edges,averages,linear,quadratic,
        weights=weights,max_iterations=max_iterations,tolerance=projection_tolerance,
        denominators=denominators,offset_radius=offset_radius,max_candidates=max_candidates)
    if primal["status"]=="feasible_exact_primal_witness" and primal["verified"]:
        return {"status":"feasible_exact_primal_witness","verified":True,
            "proof_level":primal["proof_level"],"primal_witness":primal,
            "dual_search":dual,
            "meaning":"An exact rational profile satisfies all prescribed global moments and is continuously nonnegative in every cell."}
    return {"status":"unresolved","verified":False,"proof_level":"none",
        "dual_search":dual,"primal_search":primal,
        "meaning":"Neither a strict dual separator nor an exact rational primal witness was obtained. No feasibility or infeasibility conclusion is justified."}


def run_study(output_dir):
    out=Path(output_dir); out.mkdir(parents=True,exist_ok=True)
    cases=[
      ("zero_inventory_nonzero_modes",(0.,.4,1.),(0.,0.),(1.,0.),(0.,0.)),
      ("positive_constant_two_cells",(0.,.5,1.),(2.,2.),(0.,0.),(0.,0.)),
      ("positive_nonconstant_profile",(0.,.4,1.),(1.,.8),(0.,0.),(0.,0.))]
    rows=[]
    for name,e,u,a,b in cases:
        r=assess_global_primal_dual_feasibility(e,u,a,b,max_direction=12,
            denominators=(1,),offset_radius=0)
        rows.append({"case":name,"status":r["status"],"verified":r["verified"],
                     "proof_level":r["proof_level"]})
    with (out/"p26_15_global_primal_dual.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    summary={"scope":"1-D fixed-cell-mean globally moment-constrained nonnegative quadratic profiles",
        "cases":rows,"status_semantics":{
        "certified_infeasible":"exact rational strict dual separator",
        "feasible_exact_primal_witness":"exact rational global moments and continuous cellwise positivity",
        "unresolved":"neither exact certificate found; no decision"},
        "limitations":["dual search is finite and may miss a separator",
        "no separator in finite search is not proof of feasibility",
        "1-D intervals, fixed nonnegative means and quadratic profiles only",
        "Dykstra projection generates primal candidates only",
        "no experimental or physical validation"]}
    (out/"summary.json").write_text(json.dumps(summary,indent=2,default=str),encoding="utf-8")
    print(json.dumps(summary,indent=2,default=str)); return summary


if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser(); p.add_argument("--output-dir",default="ccfsm-p26-15-results")
    run_study(p.parse_args().output_dir)
