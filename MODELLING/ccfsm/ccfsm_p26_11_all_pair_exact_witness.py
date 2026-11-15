"""P26.11: exhaustive two-coordinate rational correction of global moments."""
from __future__ import annotations
from fractions import Fraction
from itertools import combinations
import csv, json
from pathlib import Path
from ccfsm_p26_2_quadratic_projection import _edges
from ccfsm_p26_9_primal_dual_feasibility import _poly_min_exact, _global_moments
from ccfsm_p26_10_exact_moment_witness import _targets, _rationalize
from ccfsm_p26_8_verified_dual_certificate import _F


def _modal_columns(edges):
    cols=[]
    for l,r in zip(edges,edges[1:]):
        h=r-l; c=(l+r)/2
        cols.extend(((h*h/12,c*h*h/6),(Fraction(0),h**3/180)))
    return cols


def _solve_pair_exact(ci,cj,rhs):
    det=ci[0]*cj[1]-cj[0]*ci[1]
    if det==0: return None
    return ((rhs[0]*cj[1]-cj[0]*rhs[1])/det,
            (ci[0]*rhs[1]-rhs[0]*ci[1])/det)


def exact_two_coordinate_correction(target_edges,averages,candidate_linear,candidate_quadratic,
                                    target_moments=None,pivot_coordinates=(0,1),significant_digits=15):
    e=tuple(_F(v) for v in _edges(target_edges,"target_edges")); n=len(e)-1
    means=tuple(_F(v) for v in averages); a0=tuple(candidate_linear); b0=tuple(candidate_quadratic)
    if len(means)!=n or len(a0)!=n or len(b0)!=n: raise ValueError("one candidate coefficient pair per target cell required")
    if any(m<0 for m in means): raise ValueError("cell averages must be nonnegative")
    if not isinstance(significant_digits,int) or not 1<=significant_digits<=17: raise ValueError("significant_digits must be in [1,17]")
    if len(pivot_coordinates)!=2 or any(not isinstance(k,int) for k in pivot_coordinates): raise ValueError("two integer pivot coordinates required")
    p,q=pivot_coordinates
    if p==q or min(p,q)<0 or max(p,q)>=2*n: raise ValueError("pivot indices must be distinct and in [0,2N)")
    if target_moments is None: target_moments,_=_targets(e,means,tuple(_F(v) for v in a0),tuple(_F(v) for v in b0))
    else:
        if len(target_moments)!=3: raise ValueError("target_moments must contain mass, first and second moments")
        target_moments=tuple(_F(v) for v in target_moments)
    flat=[]
    for j in range(n): flat.extend((_rationalize(a0[j],significant_digits),_rationalize(b0[j],significant_digits)))
    cols=_modal_columns(e)
    base_first=sum((m*(r-l)*(l+r)/2 for l,r,m in zip(e,e[1:],means)),Fraction(0))
    base_second=sum((m*(r-l)*(((l+r)/2)**2+(r-l)**2/12) for l,r,m in zip(e,e[1:],means)),Fraction(0))
    modal_target=(target_moments[1]-base_first,target_moments[2]-base_second)
    rhs=(modal_target[0]-sum(cols[k][0]*v for k,v in enumerate(flat) if k not in (p,q)),
         modal_target[1]-sum(cols[k][1]*v for k,v in enumerate(flat) if k not in (p,q)))
    solved=_solve_pair_exact(cols[p],cols[q],rhs)
    if solved is None: return {"verified":False,"status":"singular_pivot_pair","pivot_coordinates":[p,q]}
    flat[p],flat[q]=solved
    aa,bb=tuple(flat[0::2]),tuple(flat[1::2])
    mins=[_poly_min_exact(m,a,b) for m,a,b in zip(means,aa,bb)]
    actual=_global_moments(e,means,aa,bb)
    residuals=tuple(x-y for x,y in zip(actual,target_moments))
    positive=all(v>=0 for v in mins); exact=all(v==0 for v in residuals)
    return {"verified":positive and exact,"cellwise_nonnegative_exact":positive,"global_moments_exact":exact,
      "pivot_coordinates":[p,q],"pivot_labels":[f"{'a' if k%2==0 else 'b'}_{k//2}" for k in (p,q)],
      "significant_digits_nonpivot":significant_digits,"linear":[str(v) for v in aa],"quadratic":[str(v) for v in bb],
      "minimum_cell_values_exact":[str(v) for v in mins],"moment_residuals_exact":[str(v) for v in residuals],
      "global_moments":[str(v) for v in actual],"target_moments":[str(v) for v in target_moments],
      "proof_level":"exact rational mass/first/second moments and exact continuous cellwise nonnegativity"}


def find_exact_positive_witness_all_pairs(target_edges,averages,linear,quadratic,target_moments=None,
                                          digit_choices=(17,15,13,11,9,7,5,3)):
    e=tuple(_F(v) for v in _edges(target_edges,"target_edges")); n=len(e)-1
    means=tuple(_F(v) for v in averages); a0=tuple(linear); b0=tuple(quadratic)
    if len(means)!=n or len(a0)!=n or len(b0)!=n: raise ValueError("one candidate coefficient pair per target cell required")
    if target_moments is None: target_moments,_=_targets(e,means,tuple(_F(v) for v in a0),tuple(_F(v) for v in b0))
    else: target_moments=tuple(_F(v) for v in target_moments)
    if not digit_choices or any(not isinstance(d,int) or not 1<=d<=17 for d in digit_choices):
        raise ValueError("digit_choices must be nonempty integers in [1,17]")
    best=None; tested=nonsingular=0
    for digits in digit_choices:
        for p,q in combinations(range(2*n),2):
            tested+=1
            trial=exact_two_coordinate_correction(e,means,a0,b0,target_moments,(p,q),digits)
            if trial.get("status")=="singular_pivot_pair": continue
            nonsingular+=1
            if trial["verified"]:
                margin=min(Fraction(v) for v in trial["minimum_cell_values_exact"])
                flat=trial["linear"]+trial["quadratic"]
                original=tuple(x for pair in zip(a0,b0) for x in pair)
                distance=sum((Fraction(v)-_F(x))**2 for v,x in zip(flat,original))
                key=(margin,-distance)
                if best is None or key>best[0]: best=(key,trial)
    if best:
        out=best[1]; out.update({"status":"feasible_exact_primal_witness",
          "method":"all nonsingular modal-coordinate pairs with exact rational 2x2 correction",
          "search":{"digit_choices":list(digit_choices),"coordinate_pairs_tested":tested,"nonsingular_pairs_tested":nonsingular}})
        return out
    return {"verified":False,"status":"no_exact_positive_witness_found",
      "method":"finite precision list with exhaustive two-coordinate pivot-pair enumeration",
      "search":{"digit_choices":list(digit_choices),"coordinate_pairs_tested":tested,"nonsingular_pairs_tested":nonsingular},
      "meaning":"No exact positive witness was found in this finite rational search; this is not an infeasibility proof."}


def run_study(output_dir):
    out=Path(output_dir); out.mkdir(parents=True,exist_ok=True)
    cases=[
      ("positive_two_cell",(0.,.5,1.),(2.,2.),(.1,-.1),(.1,.1)),
      ("zero_inventory_modes",(0.,.4,1.),(0.,0.),(1.,0.),(0.,0.)),
      ("three_cell_stress",(0.,.3,.7,1.),(1.,.8,1.2),(3.,-2.,2.5),(0.,2.5,0.))]
    rows=[]
    for name,e,u,a,b in cases:
        r=find_exact_positive_witness_all_pairs(e,u,a,b)
        rows.append({"case":name,"status":r["status"],"coordinate_pairs_tested":r["search"]["coordinate_pairs_tested"],
                     "nonsingular_pairs_tested":r["search"]["nonsingular_pairs_tested"]})
    with (out/"p26_11_all_pair_exact_witnesses.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    summary={"scope":"1-D fixed-cell-mean globally moment-constrained nonnegative quadratic reconstruction",
      "cases":rows,"method":"enumerate all nonsingular pairs among 2N modal coordinates for each selected decimal precision; solve both pivots exactly over rational numbers",
      "guarantee":"accepted witnesses have exact rational mass, first and second moments and exact continuous nonnegativity in every cell",
      "limitations":["finite precision choices do not exhaust all rational or real feasible points",
       "pivot enumeration is exhaustive only for the selected rationalized candidates",
       "floating-point candidate generation does not establish feasibility","finite dual direction search may miss a separator",
       "1-D intervals, fixed cell means and piecewise quadratic reconstruction only","no physical validation"]}
    (out/"summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    print(json.dumps(summary,indent=2)); return summary


if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser(); p.add_argument("--output-dir",default="ccfsm-p26-11-results")
    run_study(p.parse_args().output_dir)
