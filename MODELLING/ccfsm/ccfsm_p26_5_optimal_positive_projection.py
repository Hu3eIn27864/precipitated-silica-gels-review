"""P26.5: moment-aware closest positivity projection for 1-D quadratic cells.

For each fixed nonnegative cell average, project the two zero-mean modes
onto the convex cone of nonnegative quadratic reconstructions. A cutting-plane
active-set method solves the 2-D convex quadratic program without SciPy.
"""
from __future__ import annotations
import csv,json,math
from pathlib import Path
from ccfsm_p26_2_quadratic_projection import _edges,moments,project_quadratic_moments,quadratic_minimum
from ccfsm_p26_4_positive_target import positive_target_coefficients

def _constraint(xi):
    return float(xi),float(xi)*float(xi)-1.0/12.0

def _objective(z,z0,w):
    return w[0]*(z[0]-z0[0])**2+w[1]*(z[1]-z0[1])**2

def _finite_halfspace_projection(z0,weights,constraints,rhs,tol):
    """Exact 2-D diagonal-metric projection onto finitely many halfspaces."""
    w1,w2=weights; inv=(1.0/w1,1.0/w2)
    candidates=[]
    def feasible(z):
        return all(c[0]*z[0]+c[1]*z[1]>=r-tol for c,r in zip(constraints,rhs))
    if feasible(z0): candidates.append(tuple(z0))
    for c,r in zip(constraints,rhs):
        den=c[0]*c[0]*inv[0]+c[1]*c[1]*inv[1]
        if den<=1e-30: continue
        violation=r-(c[0]*z0[0]+c[1]*z0[1])
        z=(z0[0]+inv[0]*c[0]*violation/den,z0[1]+inv[1]*c[1]*violation/den)
        if feasible(z): candidates.append(z)
    n=len(constraints)
    for i in range(n):
        c1=constraints[i]; r1=rhs[i]
        for j in range(i+1,n):
            c2=constraints[j]; r2=rhs[j]
            det=c1[0]*c2[1]-c1[1]*c2[0]
            if abs(det)<=1e-14: continue
            z=((r1*c2[1]-c1[1]*r2)/det,(c1[0]*r2-r1*c2[0])/det)
            if feasible(z): candidates.append(z)
    if not candidates: return None
    return min(candidates,key=lambda z:_objective(z,z0,weights))

def closest_positive_coefficients(average,linear,quadratic,weights=(1.0,1.0),
                                  safety=1e-12,max_cuts=128):
    """Weighted Euclidean projection of (a,b) onto nonnegative quadratic cone.

    The average is fixed. The continuum constraint is enforced by repeatedly
    adding the exact minimizer of the current quadratic as a cutting plane.
    """
    m,a0,b0=map(float,(average,linear,quadratic))
    w=tuple(float(v) for v in weights)
    if not all(math.isfinite(v) for v in (m,a0,b0,*w,safety)): raise ValueError("all inputs must be finite")
    if m<0: raise ValueError("nonnegative average required for nonnegative reconstruction")
    if len(w)!=2 or any(v<=0 for v in w): raise ValueError("two strictly positive objective weights required")
    if safety<0 or safety>=1e-3: raise ValueError("safety must be in [0,1e-3)")
    if not isinstance(max_cuts,int) or max_cuts<1: raise ValueError("max_cuts must be a positive integer")
    z0=(a0,b0)
    scale=max(1.0,m,abs(a0),abs(b0))
    margin=safety*scale
    if m<=margin:
        return 0.0,0.0,{"objective":_objective((0.,0.),z0,w),"iterations":0,
            "active_cuts":0,"minimum_before":m+quadratic_minimum(a0,b0),
            "minimum_after":m,"positivity_margin":margin,"converged":True}
    cuts=[]
    z=z0
    for iteration in range(1,max_cuts+1):
        xi_candidates=[-.5,.5]
        if z[1]>0:
            xv=-z[0]/(2*z[1])
            if -.5<xv<.5: xi_candidates.append(xv)
        xi=min(xi_candidates,key=lambda x:m+z[0]*x+z[1]*(x*x-1/12))
        minimum=m+z[0]*xi+z[1]*(xi*xi-1/12)
        if minimum>=margin-5e-14*scale:
            return z[0],z[1],{"objective":_objective(z,z0,w),"iterations":iteration-1,
                "active_cuts":len(cuts),"minimum_before":m+quadratic_minimum(a0,b0),
                "minimum_after":m+quadratic_minimum(*z),"positivity_margin":margin,"converged":True}
        c=_constraint(xi)
        if not any(abs(c[0]-q[0])+abs(c[1]-q[1])<1e-14 for q in cuts):
            cuts.append(c)
        rhs=[-m+margin]*len(cuts)
        candidate=_finite_halfspace_projection(z0,w,cuts,rhs,1e-13*scale)
        if candidate is None:
            raise ArithmeticError("finite active-set projection failed to find a feasible point")
        z=candidate
    raise ArithmeticError("cutting-plane projection did not converge within max_cuts")

def limit_target_reconstruction_optimal(target_edges,averages,linear,quadratic,weights=(1.,1.)):
    e=_edges(target_edges,"target_edges"); n=len(e)-1
    u=tuple(float(v) for v in averages); a=tuple(float(v) for v in linear); b=tuple(float(v) for v in quadratic)
    if len(u)!=n or len(a)!=n or len(b)!=n or not all(math.isfinite(v) for v in u+a+b):
        raise ValueError("one finite coefficient triple per target cell required")
    if any(v<0 for v in u): raise ValueError("nonnegative target averages required")
    oa=[]; ob=[]; objectives=[]; iterations=[]; before=[]; after=[]
    for m,x,y in zip(u,a,b):
        xp,yp,d=closest_positive_coefficients(m,x,y,weights=weights)
        oa.append(xp); ob.append(yp); objectives.append(d["objective"]); iterations.append(d["iterations"])
        before.append(d["minimum_before"]); after.append(d["minimum_after"])
    result=(u,tuple(oa),tuple(ob))
    old=moments(e,u,a,b); new=moments(e,*result)
    diag={"method":"weighted closest-point projection onto nonnegative quadratic cell cone",
        "objective_weights":tuple(weights),"objectives":tuple(objectives),"iterations":tuple(iterations),
        "minimum_before":tuple(before),"minimum_after":tuple(after),
        "limited_cells":sum(v>1e-14 for v in objectives),"target_cells":n,
        "minimum_target_value":min(after),
        "absolute_moment_changes":{"mass":abs(new[0]-old[0]),"first":abs(new[1]-old[1]),"second":abs(new[2]-old[2])},
        "relative_moment_changes":{"mass":abs(new[0]-old[0])/max(1e-30,abs(old[0])),
            "first":abs(new[1]-old[1])/max(1e-30,abs(old[1])),"second":abs(new[2]-old[2])/max(1e-30,abs(old[2]))}}
    return result,diag

def project_optimal_positive_quadratic(source_edges,source_averages,source_linear,source_quadratic,target_edges,weights=(1.,1.)):
    raw=project_quadratic_moments(source_edges,source_averages,source_linear,source_quadratic,target_edges,positivity=False)
    result,diag=limit_target_reconstruction_optimal(target_edges,*raw,weights=weights)
    old=moments(target_edges,*raw); new=moments(target_edges,*result)
    diag["moments_before"]={"mass":old[0],"first":old[1],"second":old[2]}
    diag["moments_after"]={"mass":new[0],"first":new[1],"second":new[2]}
    return result,diag

def run_study(output_dir):
    out=Path(output_dir); out.mkdir(parents=True,exist_ok=True)
    cases=[("edge_undershoot",1.,4.,0.),("interior_undershoot",.2,0.,3.),
        ("mixed_modes",.15,.8,1.1),("zero_mean",0.,.5,1.),("already_positive",1.,.2,.1)]
    rows=[]
    for name,m,a,b in cases:
        radial=positive_target_coefficients(m,a,b)
        opt=closest_positive_coefficients(m,a,b)
        def val(z): return m+quadratic_minimum(z[0],z[1])
        # A one-cell interval [0,1] makes raw/global moments transparent.
        old=moments((0,1),(m,),(a,),(b,))
        radial_m=moments((0,1),(m,),(radial[0],),(radial[1],))
        opt_m=moments((0,1),(m,),(opt[0],),(opt[1],))
        rows.append({"case":name,"average":m,"linear_before":a,"quadratic_before":b,
            "radial_linear":radial[0],"radial_quadratic":radial[1],"radial_minimum":val(radial[:2]),
            "optimal_linear":opt[0],"optimal_quadratic":opt[1],"optimal_minimum":val(opt[:2]),
            "optimal_objective":_objective(opt[:2],(a,b),(1.,1.)),
            "radial_first_moment_change":abs(radial_m[1]-old[1]),
            "optimal_first_moment_change":abs(opt_m[1]-old[1]),
            "radial_second_moment_change":abs(radial_m[2]-old[2]),
            "optimal_second_moment_change":abs(opt_m[2]-old[2]),
            "radial_mass_change":abs(radial_m[0]-old[0]),"optimal_mass_change":abs(opt_m[0]-old[0])})
    csv_path=out/"p26_5_optimal_positive_projection.csv"
    with csv_path.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    summary={"scope":"1-D cellwise weighted closest-point projection of quadratic modes under continuum nonnegativity",
        "cases":len(rows),"minimum_after":min(r["optimal_minimum"] for r in rows),
        "maximum_absolute_mass_change":max(r["optimal_mass_change"] for r in rows),
        "radial_total_first_moment_change":sum(r["radial_first_moment_change"] for r in rows),
        "optimal_total_first_moment_change":sum(r["optimal_first_moment_change"] for r in rows),
        "radial_total_second_moment_change":sum(r["radial_second_moment_change"] for r in rows),
        "optimal_total_second_moment_change":sum(r["optimal_second_moment_change"] for r in rows),
        "cases_improved_first_moment":sum(r["optimal_first_moment_change"]<r["radial_first_moment_change"]-1e-12 for r in rows),
        "cases_improved_second_moment":sum(r["optimal_second_moment_change"]<r["radial_second_moment_change"]-1e-12 for r in rows),
        "method":"cutting-plane solution of a 2-D convex quadratic program; fixed cell average; positive weights",
        "limitations":["objective is coefficient-space distance, not directly a global moment-error objective",
            "local cellwise optimization does not enforce global first/second moment constraints",
            "cutting-plane solver uses floating-point tolerances and bounded iterations",
            "1-D intervals and quadratic fields only; no physical validation or 2-D/3-D geometry"]}
    (out/"summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    print(json.dumps(summary,indent=2)); return summary
if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser(); p.add_argument("--output-dir",default="ccfsm-p26-5-results"); run_study(p.parse_args().output_dir)
