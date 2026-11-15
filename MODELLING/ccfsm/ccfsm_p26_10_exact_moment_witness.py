"""P26.10: exact-rational moment correction of positive quadratic witnesses."""
from __future__ import annotations
from fractions import Fraction
import csv, json, math
from pathlib import Path
from ccfsm_p26_2_quadratic_projection import _edges
from ccfsm_p26_6_global_positive_projection import globally_coupled_positive_projection
from ccfsm_p26_8_verified_dual_certificate import search_dual_certificate, _F
from ccfsm_p26_9_primal_dual_feasibility import _poly_min_exact, _global_moments


def _targets(edges, means, linear, quadratic):
    mass, first, second = _global_moments(edges, means, linear, quadratic)
    base1=sum((m*(r-l)*(l+r)/2 for l,r,m in zip(edges,edges[1:],means)),Fraction(0))
    base2=sum((m*(r-l)*(((l+r)/2)**2+(r-l)**2/12) for l,r,m in zip(edges,edges[1:],means)),Fraction(0))
    return (mass,first,second),(first-base1,second-base2)


def _rationalize(value, digits):
    if isinstance(value, Fraction): return value
    if isinstance(value, int): return Fraction(value)
    if not math.isfinite(float(value)): raise ValueError("candidate coefficients must be finite")
    return Fraction(format(float(value), f".{digits}g"))


def exact_moment_correction(target_edges, averages, candidate_linear, candidate_quadratic,
                            target_moments=None, significant_digits=15, pivot_cell=0):
    e=tuple(_F(v) for v in _edges(target_edges,"target_edges")); n=len(e)-1
    u=tuple(_F(v) for v in averages); ca=tuple(candidate_linear); cb=tuple(candidate_quadratic)
    if len(u)!=n or len(ca)!=n or len(cb)!=n: raise ValueError("one candidate coefficient pair per cell required")
    if any(m<0 for m in u): raise ValueError("cell averages must be nonnegative")
    if not isinstance(significant_digits,int) or not 1<=significant_digits<=17: raise ValueError("significant_digits must be in [1,17]")
    if not isinstance(pivot_cell,int) or not 0<=pivot_cell<n: raise ValueError("pivot_cell outside target mesh")
    if target_moments is None:
        target_moments,modal=_targets(e,u,tuple(_F(v) for v in ca),tuple(_F(v) for v in cb))
    else:
        if len(target_moments)!=3: raise ValueError("target_moments must contain mass, first and second moments")
        target_moments=tuple(_F(v) for v in target_moments)
        base1=sum((m*(r-l)*(l+r)/2 for l,r,m in zip(e,e[1:],u)),Fraction(0))
        base2=sum((m*(r-l)*(((l+r)/2)**2+(r-l)**2/12) for l,r,m in zip(e,e[1:],u)),Fraction(0))
        modal=(target_moments[1]-base1,target_moments[2]-base2)
    aa=[_rationalize(v,significant_digits) for v in ca]
    bb=[_rationalize(v,significant_digits) for v in cb]
    hs=[r-l for l,r in zip(e,e[1:])]; cs=[(l+r)/2 for l,r in zip(e,e[1:])]
    g1=[h*h/12 for h in hs]; g2a=[c*h*h/6 for c,h in zip(cs,hs)]; g2b=[h**3/180 for h in hs]
    p=pivot_cell
    aa[p]=(modal[0]-sum((g1[j]*aa[j] for j in range(n) if j!=p),Fraction(0)))/g1[p]
    other=sum((g2a[j]*aa[j]+g2b[j]*bb[j] for j in range(n) if j!=p),Fraction(0))
    bb[p]=(modal[1]-other-g2a[p]*aa[p])/g2b[p]
    mins=[_poly_min_exact(m,a,b) for m,a,b in zip(u,aa,bb)]
    actual=_global_moments(e,u,aa,bb)
    residuals=tuple(x-y for x,y in zip(actual,target_moments))
    positive=all(v>=0 for v in mins); exact=all(v==0 for v in residuals)
    return {"verified":positive and exact,"cellwise_nonnegative_exact":positive,"global_moments_exact":exact,
      "moment_residuals_exact":[str(v) for v in residuals],"minimum_cell_values_exact":[str(v) for v in mins],
      "averages":[str(v) for v in u],"linear":[str(v) for v in aa],"quadratic":[str(v) for v in bb],
      "pivot_cell":p,"significant_digits_nonpivot":significant_digits,
      "global_moments":[str(v) for v in actual],"target_moments":[str(v) for v in target_moments],
      "proof_level":"exact rational global mass/first/second moments and exact continuous cellwise nonnegativity"}


def find_exact_positive_witness(target_edges, averages, linear, quadratic,
                                target_moments=None, digit_choices=(17,15,13,11,9,7,5,3)):
    e=tuple(_F(v) for v in _edges(target_edges,"target_edges")); u=tuple(_F(v) for v in averages)
    a0=tuple(_F(v) for v in linear); b0=tuple(_F(v) for v in quadratic)
    if target_moments is None: target_moments,_=_targets(e,u,a0,b0)
    else: target_moments=tuple(_F(v) for v in target_moments)
    direct=exact_moment_correction(e,u,a0,b0,target_moments,17,0)
    if direct["verified"]:
        direct["method"]="original rational-decimal coefficients already satisfy all constraints"
        return direct
    successes=[]
    for digits in digit_choices:
        for pivot in range(len(e)-1):
            trial=exact_moment_correction(e,u,linear,quadratic,target_moments,digits,pivot)
            if trial["verified"]:
                margin=min(Fraction(v) for v in trial["minimum_cell_values_exact"])
                successes.append((margin,trial))
    if successes:
        best=max(successes,key=lambda item:item[0])[1]
        best["method"]="rationalized Dykstra candidate with exact two-coefficient pivot correction"
        best["search"]={"digit_choices":list(digit_choices),"pivot_cells_tested":len(e)-1}
        return best
    return {"verified":False,"status":"no_exact_positive_witness_found","method":"finite rationalization/pivot search",
      "search":{"digit_choices":list(digit_choices),"pivot_cells_tested":len(e)-1},
      "meaning":"No witness was found in this finite correction search; this is not an infeasibility proof."}


def assess_exact_moment_feasibility(target_edges, averages, linear, quadratic,
                                    weights=(1.0,1.0), max_iterations=20000,
                                    tolerance=2e-11, max_direction=12,
                                    digit_choices=(17,15,13,11,9,7,5,3)):
    e=tuple(_F(v) for v in _edges(target_edges,"target_edges")); n=len(e)-1
    u=tuple(_F(v) for v in averages); a=tuple(_F(v) for v in linear); b=tuple(_F(v) for v in quadratic)
    if len(u)!=n or len(a)!=n or len(b)!=n: raise ValueError("one coefficient triple per cell required")
    if any(m<0 for m in u): raise ValueError("cell averages must be nonnegative")
    target,_=_targets(e,u,a,b)
    dual=search_dual_certificate(e,u,a,b,max_direction)
    if dual["verified"]:
        return {"status":"certified_infeasible","proof_level":"rational dual separation",
          "dual_certificate":dual["certificate"],"primal_attempted":False}
    direct=find_exact_positive_witness(e,u,a,b,target,(17,))
    if direct["verified"]:
        return {"status":"feasible_exact_primal_witness","proof_level":direct["proof_level"],
          "witness":direct,"dual_search":dual,"projection_attempted":False}
    try:
        candidate,diag=globally_coupled_positive_projection(e,u,a,b,weights,max_iterations,tolerance)
    except (ArithmeticError,ValueError) as exc:
        return {"status":"unresolved","proof_level":"none","dual_search":dual,"primal_error":str(exc),
          "meaning":"No dual separator was found and the numerical projection did not provide a candidate."}
    witness=find_exact_positive_witness(e,u,candidate[1],candidate[2],target,digit_choices)
    if witness["verified"]:
        return {"status":"feasible_exact_primal_witness","proof_level":witness["proof_level"],
          "witness":witness,"projection_diagnostics":diag,"dual_search":dual}
    return {"status":"unresolved","proof_level":"none","candidate_search":witness,
      "projection_diagnostics":diag,"dual_search":dual,
      "meaning":"The finite rational correction search found no positive exact-moment witness; feasibility remains undecided."}


def run_study(output_dir):
    out=Path(output_dir); out.mkdir(parents=True,exist_ok=True)
    cases=[
      ("already_positive",(0.,.4,1.),(1.,.8),(0.,0.),(0.,0.)),
      ("zero_inventory_nonzero_modes",(0.,.4,1.),(0.,0.),(1.,0.),(0.,0.)),
      ("projection_stress",(0.,.3,.7,1.),(1.,.8,1.2),(3.,-2.,2.5),(0.,2.5,0.))]
    rows=[]
    for name,e,u,a,b in cases:
        r=assess_exact_moment_feasibility(e,u,a,b)
        rows.append({"case":name,"status":r["status"],"proof_level":r["proof_level"]})
    with (out/"p26_10_exact_moment_witnesses.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    summary={"scope":"1-D fixed-cell-mean globally moment-constrained nonnegative quadratic reconstruction",
      "cases":rows,"key_guarantee":"accepted primal witnesses satisfy global mass, first moment and second moment exactly as rational numbers and are continuously nonnegative in every cell",
      "status_semantics":{"feasible_exact_primal_witness":"exact rational primal witness","certified_infeasible":"strict rational dual separation",
       "unresolved":"finite rational correction search or numerical projection did not yield a witness; no infeasibility claim"},
      "limitations":["finite choices of decimal precision and pivot cells may miss an existing exact positive witness",
       "Dykstra is a floating-point candidate generator, not an exact feasibility solver",
       "dual search is finite and may miss an existing separator",
       "1-D intervals, fixed cell means and piecewise quadratic reconstructions only","no physical validation"]}
    (out/"summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    print(json.dumps(summary,indent=2)); return summary


if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser(); p.add_argument("--output-dir",default="ccfsm-p26-10-results")
    run_study(p.parse_args().output_dir)
