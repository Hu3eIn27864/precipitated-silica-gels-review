"""P26.4: positivity-preserving target-cell quadratic reconstruction."""
from __future__ import annotations
import csv,json,math
from pathlib import Path
from ccfsm_p26_2_quadratic_projection import _edges,moments,project_quadratic_moments,quadratic_minimum

def _validate(edges,averages,linear,quadratic):
    e=_edges(edges,"target_edges"); n=len(e)-1
    u=tuple(float(v) for v in averages); a=tuple(float(v) for v in linear); b=tuple(float(v) for v in quadratic)
    if len(u)!=n or len(a)!=n or len(b)!=n: raise ValueError("one finite coefficient triple per target cell required")
    if not all(math.isfinite(v) for v in u+a+b): raise ValueError("target coefficients must be finite")
    if any(v<0 for v in u): raise ValueError("nonnegative target averages are required for positivity")
    return e,u,a,b

def positive_target_coefficients(average,linear,quadratic,safety=64.0*math.ulp(1.0)):
    """Largest admissible common scaling of zero-mean modes; mean stays fixed."""
    m,a,b=map(float,(average,linear,quadratic))
    if not all(math.isfinite(v) for v in (m,a,b)): raise ValueError("coefficients must be finite")
    if m<0: raise ValueError("negative cell average is incompatible with nonnegative reconstruction")
    if not math.isfinite(safety) or safety<0 or safety>=1: raise ValueError("safety must be finite and in [0,1)")
    d=quadratic_minimum(a,b); before=m+d
    if before>=0: return a,b,1.0,before,before
    if m==0: return 0.0,0.0,0.0,before,0.0
    theta=max(0.0,min(1.0,m/(-d)))*(1.0-safety)
    ap,bp=theta*a,theta*b
    after=m+quadratic_minimum(ap,bp)
    return ap,bp,theta,before,after

def limit_target_reconstruction(target_edges,averages,linear,quadratic):
    e,u,a,b=_validate(target_edges,averages,linear,quadratic)
    oa=[]; ob=[]; factors=[]; before=[]; after=[]
    for m,x,y in zip(u,a,b):
        xp,yp,t,lo,lp=positive_target_coefficients(m,x,y)
        oa.append(xp); ob.append(yp); factors.append(t); before.append(lo); after.append(lp)
    result=(u,tuple(oa),tuple(ob))
    old_m=moments(e,u,a,b); new_m=moments(e,*result)
    diag={"limiter_factors":tuple(factors),"minimum_before":tuple(before),
        "minimum_after":tuple(after),"limited_cells":sum(t<1 for t in factors),
        "target_cells":len(u),"minimum_target_value":min(after),
        "absolute_moment_changes":{"mass":abs(new_m[0]-old_m[0]),"first":abs(new_m[1]-old_m[1]),"second":abs(new_m[2]-old_m[2])},
        "relative_moment_changes":{"mass":abs(new_m[0]-old_m[0])/max(1e-30,abs(old_m[0])),
            "first":abs(new_m[1]-old_m[1])/max(1e-30,abs(old_m[1])),
            "second":abs(new_m[2]-old_m[2])/max(1e-30,abs(old_m[2]))}}
    return result,diag

def project_positive_quadratic(source_edges,source_averages,source_linear,source_quadratic,target_edges):
    raw=project_quadratic_moments(source_edges,source_averages,source_linear,source_quadratic,target_edges,positivity=False)
    limited,diag=limit_target_reconstruction(target_edges,*raw)
    before=moments(target_edges,*raw); after=moments(target_edges,*limited)
    diag.update({"moments_before":{"mass":before[0],"first":before[1],"second":before[2]},
        "moments_after":{"mass":after[0],"first":after[1],"second":after[2]},
        "absolute_moment_changes":{"mass":abs(after[0]-before[0]),"first":abs(after[1]-before[1]),"second":abs(after[2]-before[2])},
        "relative_moment_changes":{"mass":abs(after[0]-before[0])/max(1e-30,abs(before[0])),
            "first":abs(after[1]-before[1])/max(1e-30,abs(before[1])),
            "second":abs(after[2]-before[2])/max(1e-30,abs(before[2]))}})
    return limited,diag

def run_study(output_dir):
    out=Path(output_dir); out.mkdir(parents=True,exist_ok=True)
    cases=[("edge_undershoot",1.,4.,0.),("interior_undershoot",.2,0.,2.),
        ("mixed_modes",.15,.8,1.1),("zero_mean",0.,0.,0.),("already_positive",1.,.2,.1)]
    rows=[]
    for name,m,a,b in cases:
        result,diag=limit_target_reconstruction((0.,1.),(m,),(a,),(b,))
        old=moments((0,1),(m,),(a,),(b,)); new=moments((0,1),*result)
        rows.append({"case":name,"average_before":m,"linear_before":a,"quadratic_before":b,
            "linear_after":result[1][0],"quadratic_after":result[2][0],"limiter_factor":diag["limiter_factors"][0],
            "minimum_before":diag["minimum_before"][0],"minimum_after":diag["minimum_after"][0],
            "mass_before":old[0],"mass_after":new[0],"first_moment_before":old[1],"first_moment_after":new[1],
            "second_moment_before":old[2],"second_moment_after":new[2]})
    with (out/"p26_4_positive_target_cases.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    summary={"scope":"1-D target-cell positivity limiter for piecewise quadratic projections","cases":len(rows),
        "limited_cases":sum(r["limiter_factor"]<1 for r in rows),"minimum_after":min(r["minimum_after"] for r in rows),
        "maximum_absolute_mass_change":max(abs(r["mass_after"]-r["mass_before"]) for r in rows),
        "maximum_absolute_first_moment_change":max(abs(r["first_moment_after"]-r["first_moment_before"]) for r in rows),
        "maximum_absolute_second_moment_change":max(abs(r["second_moment_after"]-r["second_moment_before"]) for r in rows),
        "method":"largest admissible common scaling of both zero-mean modes; cell average unchanged",
        "limitations":["radial contraction is not the global closest-point projection in coefficient space",
            "mass is preserved cellwise; first and second moments may change","negative cell averages are rejected",
            "roundoff safety may introduce a tiny positive margin","1-D intervals and quadratic fields only; no physical validation or 2-D/3-D geometry"]}
    (out/"summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8"); print(json.dumps(summary,indent=2)); return summary
if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser(); p.add_argument("--output-dir",default="ccfsm-p26-4-results"); run_study(p.parse_args().output_dir)
