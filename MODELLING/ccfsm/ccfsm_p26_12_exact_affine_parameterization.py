"""P26.12: exact affine parametrization of the global moment constraint space.

The two higher global moments are affine in the 2N modal coefficients.
This module chooses any independent pair of columns as pivots, exposes all
2N-2 remaining coordinates as free rational parameters, and reconstructs
pivot coordinates by exact Fraction arithmetic. A bounded rational-grid
search may find exact positive witnesses; failure is explicitly unresolved.
"""
from __future__ import annotations
from fractions import Fraction
from itertools import product
import csv
import json
from pathlib import Path

from ccfsm_p26_2_quadratic_projection import _edges
from ccfsm_p26_8_verified_dual_certificate import _F
from ccfsm_p26_9_primal_dual_feasibility import _global_moments, _poly_min_exact
from ccfsm_p26_10_exact_moment_witness import _targets, _rationalize
from ccfsm_p26_11_all_pair_exact_witness import _modal_columns, _solve_pair_exact


def _base_moments(edges, means):
    mass = sum((m*(r-l) for l,r,m in zip(edges,edges[1:],means)), Fraction(0))
    first = sum((m*(r-l)*(l+r)/2 for l,r,m in zip(edges,edges[1:],means)), Fraction(0))
    second = sum((m*(r-l)*(((l+r)/2)**2+(r-l)**2/12)
                  for l,r,m in zip(edges,edges[1:],means)), Fraction(0))
    return mass, first, second


def _independent_pivot_pair(columns, requested=None):
    ncoords=len(columns)
    if requested is not None:
        if len(requested)!=2 or any(not isinstance(k,int) for k in requested):
            raise ValueError("pivot_coordinates must contain two integer indices")
        p,q=requested
        if p==q or min(p,q)<0 or max(p,q)>=ncoords:
            raise ValueError("pivot indices must be distinct and in range")
        if _solve_pair_exact(columns[p],columns[q],(Fraction(0),Fraction(0))) is None:
            raise ValueError("requested pivot columns are linearly dependent")
        return p,q
    for p in range(ncoords):
        for q in range(p+1,ncoords):
            if _solve_pair_exact(columns[p],columns[q],(Fraction(0),Fraction(0))) is not None:
                return p,q
    raise ValueError("the two global moment constraints do not have rank two")


def build_exact_affine_parameterization(target_edges, averages, target_moments,
                                         pivot_coordinates=None):
    """Return an exact affine chart z_pivots = c + B*z_free."""
    e=tuple(_F(v) for v in _edges(target_edges,"target_edges"))
    means=tuple(_F(v) for v in averages)
    n=len(e)-1
    if len(means)!=n or any(m<0 for m in means):
        raise ValueError("one nonnegative cell average per interval required")
    if len(target_moments)!=3:
        raise ValueError("target_moments must contain mass, first and second moments")
    target=tuple(_F(v) for v in target_moments)
    mass,base1,base2=_base_moments(e,means)
    if target[0]!=mass:
        raise ValueError("target mass is incompatible with the fixed cell averages")
    modal_rhs=(target[1]-base1,target[2]-base2)
    columns=_modal_columns(e)
    p,q=_independent_pivot_pair(columns,pivot_coordinates)
    free=tuple(k for k in range(2*n) if k not in (p,q))
    pivot_inverse_0=_solve_pair_exact(columns[p],columns[q],modal_rhs)
    if pivot_inverse_0 is None:
        raise ValueError("singular pivot pair")
    # For each free coordinate, its unit contribution is subtracted from RHS.
    coefficients=[]
    for k in free:
        response=_solve_pair_exact(columns[p],columns[q],(-columns[k][0],-columns[k][1]))
        coefficients.append(response)
    return {
      "edges":e,"averages":means,"target_moments":target,
      "pivot_coordinates":(p,q),"free_coordinates":free,
      "pivot_constant":pivot_inverse_0,"pivot_free_coefficients":tuple(coefficients),
      "dimension":2*n-2,"columns":columns,
      "meaning":"Every real/rational coefficient vector satisfying the two global higher-moment equations is represented exactly once by its free coordinates."
    }


def evaluate_exact_affine_parameterization(chart, free_values):
    free=tuple(_F(v) for v in free_values)
    if len(free)!=chart["dimension"]:
        raise ValueError("one value per free affine coordinate required")
    z=[None]*len(chart["columns"])
    for k,v in zip(chart["free_coordinates"],free): z[k]=v
    p,q=chart["pivot_coordinates"]
    pivot=list(chart["pivot_constant"])
    for value,(dp,dq) in zip(free,chart["pivot_free_coefficients"]):
        pivot[0]+=dp*value
        pivot[1]+=dq*value
    z[p],z[q]=pivot
    return tuple(z[0::2]),tuple(z[1::2])


def verify_affine_candidate(chart, linear, quadratic):
    means=chart["averages"]; edges=chart["edges"]; target=chart["target_moments"]
    minima=tuple(_poly_min_exact(m,a,b) for m,a,b in zip(means,linear,quadratic))
    actual=_global_moments(edges,means,linear,quadratic)
    residuals=tuple(x-y for x,y in zip(actual,target))
    exact=all(v==0 for v in residuals)
    positive=all(v>=0 for v in minima)
    return {"verified":exact and positive,"global_moments_exact":exact,
      "cellwise_nonnegative_exact":positive,"moment_residuals_exact":tuple(residuals),
      "minimum_cell_values_exact":minima,"global_moments":actual}


def search_rational_positive_witness(target_edges, averages, candidate_linear, candidate_quadratic,
                                     target_moments=None, pivot_coordinates=None,
                                     denominators=(1,2,3), offset_radius=1,
                                     max_candidates=20000, significant_digits=15):
    """Enumerate a finite rational grid in the full affine chart.

    Grid points are anchor_free + k/d, with each integer k in
    [-offset_radius, offset_radius]. Cartesian combinations cover coupled
    changes in all free directions. The candidate cap is a resource limit.
    """
    e=tuple(_F(v) for v in _edges(target_edges,"target_edges"))
    means=tuple(_F(v) for v in averages)
    a0=tuple(candidate_linear); b0=tuple(candidate_quadratic); n=len(e)-1
    if len(means)!=n or len(a0)!=n or len(b0)!=n:
        raise ValueError("one candidate coefficient pair per cell required")
    if not isinstance(offset_radius,int) or offset_radius<0:
        raise ValueError("offset_radius must be a nonnegative integer")
    if not isinstance(max_candidates,int) or max_candidates<1:
        raise ValueError("max_candidates must be positive")
    if not denominators or any(not isinstance(d,int) or d<1 for d in denominators):
        raise ValueError("denominators must be positive integers")
    if target_moments is None:
        target_moments,_=_targets(e,means,tuple(_F(v) for v in a0),tuple(_F(v) for v in b0))
    else: target_moments=tuple(_F(v) for v in target_moments)
    chart=build_exact_affine_parameterization(e,means,target_moments,pivot_coordinates)
    interleaved=tuple(_rationalize(v,significant_digits) for pair in zip(a0,b0) for v in pair)
    anchor=tuple(interleaved[k] for k in chart["free_coordinates"])
    best=None; tested=0; seen=set(); truncated=False
    offsets=tuple(range(-offset_radius,offset_radius+1))
    for denominator in denominators:
        axes=tuple(tuple(anchor_i+Fraction(k,denominator) for k in offsets)
                   for anchor_i in anchor)
        combinations=product(*axes) if axes else [()]
        for free in combinations:
            free=tuple(free)
            if free in seen: continue
            seen.add(free)
            if tested>=max_candidates:
                truncated=True; break
            tested+=1
            linear,quadratic=evaluate_exact_affine_parameterization(chart,free)
            check=verify_affine_candidate(chart,linear,quadratic)
            if check["verified"]:
                margin=min(check["minimum_cell_values_exact"])
                distance=sum((x-y)**2 for x,y in zip(
                    tuple(v for pair in zip(linear,quadratic) for v in pair),interleaved))
                key=(margin,-distance)
                if best is None or key>best[0]:
                    best=(key,linear,quadratic,free,check)
        if truncated: break
    if best:
        _,linear,quadratic,free,check=best
        return {"status":"feasible_exact_primal_witness","verified":True,
          "linear":tuple(linear),"quadratic":tuple(quadratic),"free_coordinates":free,
          "pivot_coordinates":chart["pivot_coordinates"],"verification":check,
          "search":{"candidates_tested":tested,"denominators":tuple(denominators),
                    "offset_radius":offset_radius,"truncated_by_candidate_cap":truncated},
          "proof_level":"exact rational mass, first and second moments and continuous cellwise nonnegativity"}
    return {"status":"unresolved","verified":False,
      "meaning":"No positive witness was found in the finite rational grid explored; this is not an infeasibility proof.",
      "pivot_coordinates":chart["pivot_coordinates"],
      "search":{"candidates_tested":tested,"denominators":tuple(denominators),
                "offset_radius":offset_radius,"truncated_by_candidate_cap":truncated}}


def run_study(output_dir):
    out=Path(output_dir); out.mkdir(parents=True,exist_ok=True)
    cases=[
      ("two_cell_interior",(0,Fraction(1,2),1),(2,2),(.1,-.1),(.1,.1)),
      ("one_cell_zero_dimensional",(0,1),(2,),(.1,),(.1,)),
      ("zero_inventory_incompatible",(0,Fraction(1,2),1),(0,0),(1,0),(0,0))]
    rows=[]
    for name,e,u,a,b in cases:
        r=search_rational_positive_witness(e,u,a,b,denominators=(1,2),offset_radius=1,max_candidates=1000)
        rows.append({"case":name,"status":r["status"],"candidates_tested":r["search"]["candidates_tested"],
                     "pivot_coordinates":str(r["pivot_coordinates"])})
    with (out/"p26_12_affine_parameterization.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    summary={"scope":"exact affine space of 1-D fixed-cell-mean quadratic reconstructions satisfying prescribed global moments",
      "cases":rows,"parameter_dimension":"2N-2 when the two higher-moment constraints have rank two",
      "guarantee":"the affine chart is a bijection between all coefficient vectors satisfying the two global higher-moment equalities and their free-coordinate vectors; accepted witnesses additionally pass exact continuous cellwise positivity",
      "limitations":["finite rational-grid search is not a complete positivity-feasibility algorithm",
       "nonempty real feasible sets need not contain rational points",
       "candidate cap may truncate enumeration","1-D piecewise quadratic reconstruction only",
       "no 2-D/3-D extension and no physical validation"]}
    (out/"summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    print(json.dumps(summary,indent=2)); return summary


if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser(); p.add_argument("--output-dir",default="ccfsm-p26-12-results")
    run_study(p.parse_args().output_dir)
