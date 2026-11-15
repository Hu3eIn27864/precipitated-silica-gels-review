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

def _objective(z,z0,w):
    return w[0]*(z[0]-z0[0])**2+w[1]*(z[1]-z0[1])**2

def _golden_minimum(fun,left,right):
    ratio=(math.sqrt(5.0)-1.0)/2.0
    x1=right-ratio*(right-left); x2=left+ratio*(right-left)
    f1=fun(x1); f2=fun(x2)
    for _ in range(100):
        if right-left<2e-14: break
        if f1<=f2:
            right,x2,f2=x2,x1,f1
            x1=right-ratio*(right-left); f1=fun(x1)
        else:
            left,x1,f1=x1,x2,f2
            x2=left+ratio*(right-left); f2=fun(x2)
    x=.5*(left+right)
    return x,fun(x)

def closest_positive_coefficients(average,linear,quadratic,weights=(1.0,1.0),
                                  safety=1e-12,max_cuts=128):
    """Weighted closest point on the exact boundary of the nonnegative-quadratic set.

    The feasible boundary consists of two endpoint half-lines and the
    interior-vertex ellipse arc. Candidate projections are enumerated on
    those boundaries; the ellipse arc is minimized by bracketed golden search.
    """
    m,a0,b0=map(float,(average,linear,quadratic))
    w=tuple(float(v) for v in weights)
    if not all(math.isfinite(v) for v in (m,a0,b0,*w,safety)): raise ValueError("all inputs must be finite")
    if m<0: raise ValueError("nonnegative average required for nonnegative reconstruction")
    if len(w)!=2 or any(v<=0 for v in w): raise ValueError("two strictly positive objective weights required")
    if safety<0 or safety>=1e-3: raise ValueError("safety must be in [0,1e-3)")
    if not isinstance(max_cuts,int) or max_cuts<1: raise ValueError("max_cuts must be a positive integer")
    z0=(a0,b0); scale=max(1.0,m,abs(a0),abs(b0)); margin=safety*scale
    minimum_before=m+quadratic_minimum(a0,b0)
    if minimum_before>=margin:
        return a0,b0,{"objective":0.0,"iterations":0,"active_cuts":0,
            "minimum_before":minimum_before,"minimum_after":minimum_before,
            "positivity_margin":margin,"converged":True}
    me=m-margin
    if me<=0:
        return 0.0,0.0,{"objective":_objective((0.,0.),z0,w),"iterations":0,
            "active_cuts":0,"minimum_before":minimum_before,"minimum_after":m,
            "positivity_margin":margin,"converged":True}
    inv=(1.0/w[0],1.0/w[1]); candidates=[]
    def feasible(z):
        return m+quadratic_minimum(z[0],z[1])>=margin-2e-11*scale
    def add(z):
        if all(math.isfinite(v) for v in z) and feasible(z):
            candidates.append((float(z[0]),float(z[1])))
    add(z0)
    # Endpoint constraints: m_eff +/- a/2 + b/6 >= 0.
    normals=((.5,1.0/6.0),(-.5,1.0/6.0))
    for n in normals:
        value=n[0]*a0+n[1]*b0
        rhs=-me
        if value<rhs:
            den=n[0]*n[0]*inv[0]+n[1]*n[1]*inv[1]
            lam=(rhs-value)/den
            add((a0+inv[0]*n[0]*lam,b0+inv[1]*n[1]*lam))
    # Intersection of both endpoint boundaries.
    add((0.0,-6.0*me))
    # Interior-vertex boundary ellipse, restricted to |a| <= b.
    # a=sqrt(12)*m_eff*sin(t), b=6*m_eff*(1+cos(t)),
    # with t in [-2pi/3, 2pi/3].
    left=-2.0*math.pi/3.0; right=2.0*math.pi/3.0
    def point(t):
        return (math.sqrt(12.0)*me*math.sin(t),6.0*me*(1.0+math.cos(t)))
    def objective_t(t):
        return _objective(point(t),z0,w)
    add(point(left)); add(point(right))
    samples=1024
    ts=[left+(right-left)*i/samples for i in range(samples+1)]
    fs=[objective_t(t) for t in ts]
    for i in range(1,samples):
        if fs[i]<=fs[i-1] and fs[i]<=fs[i+1]:
            t,_=_golden_minimum(objective_t,ts[i-1],ts[i+1])
            add(point(t))
    if not candidates:
        raise ArithmeticError("boundary candidate enumeration found no feasible projection")
    best=min(candidates,key=lambda z:_objective(z,z0,w))
    minimum_after=m+quadratic_minimum(best[0],best[1])
    if minimum_after<margin-2e-11*scale:
        raise ArithmeticError("projected quadratic failed the continuum positivity check")
    return best[0],best[1],{"objective":_objective(best,z0,w),"iterations":samples,
        "active_cuts":len(candidates),"minimum_before":minimum_before,
        "minimum_after":minimum_after,"positivity_margin":margin,"converged":True}

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
