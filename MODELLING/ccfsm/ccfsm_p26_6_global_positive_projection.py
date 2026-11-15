"""P26.6: globally coupled positive quadratic projection.

Dykstra projection in a weighted coefficient norm onto the intersection of
(a) the affine set preserving global first and second moments and
(b) the Cartesian product of cellwise nonnegative quadratic cones.
Cell averages are fixed, hence global mass is preserved identically.
"""
from __future__ import annotations
import csv, json, math
from pathlib import Path
from ccfsm_p26_2_quadratic_projection import _edges, moments, quadratic_minimum
from ccfsm_p26_5_optimal_positive_projection import closest_positive_coefficients


def _solve2(a, b, c, r, s):
    det = a*c-b*b
    scale = max(1.0, abs(a*c), abs(b*b))
    if abs(det) <= 1e-14*scale:
        raise ValueError("global first/second-moment constraints are rank deficient")
    return ((r*c-s*b)/det, (s*a-r*b)/det)


def _affine_project(z, edges, target, weights):
    n=len(edges)-1
    g1=[]; g2=[]
    for l,r in zip(edges,edges[1:]):
        h=r-l; c=.5*(l+r)
        g1.extend((h*h/12.0, 0.0))
        g2.extend((c*h*h/6.0, h**3/180.0))
    invw=[]
    for _ in range(n): invw.extend((1.0/weights[0],1.0/weights[1]))
    d1=sum(v*x for v,x in zip(g1,z))-target[0]
    d2=sum(v*x for v,x in zip(g2,z))-target[1]
    a=sum(v*v*w for v,w in zip(g1,invw))
    b=sum(x*y*w for x,y,w in zip(g1,g2,invw))
    c=sum(v*v*w for v,w in zip(g2,invw))
    lam1,lam2=_solve2(a,b,c,d1,d2)
    return [x-w*(v*lam1+y*lam2) for x,w,v,y in zip(z,invw,g1,g2)]


def _positive_project(z, averages, weights):
    out=[]
    for j,m in enumerate(averages):
        a,b,_=closest_positive_coefficients(m,z[2*j],z[2*j+1],
                                             weights=weights,safety=0.0)
        out.extend((a,b))
    return out


def globally_coupled_positive_projection(target_edges, averages, linear, quadratic,
                                         weights=(1.0,1.0), max_iterations=20000,
                                         tolerance=2e-11):
    """Project onto global moment equalities intersected with cellwise positivity.

    Preserves cell averages (and therefore total mass) exactly. First and
    second global moments are constrained to their input values. Uses Dykstra
    alternating projections; nonconvergence is reported, not called infeasible.
    """
    e=_edges(target_edges,"target_edges"); n=len(e)-1
    u=tuple(float(v) for v in averages); aa=tuple(float(v) for v in linear); bb=tuple(float(v) for v in quadratic)
    w=tuple(float(v) for v in weights)
    if len(u)!=n or len(aa)!=n or len(bb)!=n or not all(math.isfinite(v) for v in u+aa+bb):
        raise ValueError("one finite coefficient triple per target cell required")
    if any(v<0 for v in u): raise ValueError("nonnegative cell averages required")
    if len(w)!=2 or not all(math.isfinite(v) and v>0 for v in w):
        raise ValueError("two finite strictly positive weights required")
    if not isinstance(max_iterations,int) or max_iterations<1: raise ValueError("max_iterations must be positive")
    if not math.isfinite(tolerance) or tolerance<=0: raise ValueError("tolerance must be positive")
    old=moments(e,u,aa,bb); target=(old[1],old[2])
    initial_min=min(u[j]+quadratic_minimum(aa[j],bb[j]) for j in range(n))
    if initial_min >= 0.0:
        # The input already belongs to both constraint sets; do not run an
        # inexact alternating projection on a point that is already feasible.
        diag={"method":"identity: input already satisfies global moments and exact cellwise positivity",
              "iterations":0,"converged":True,"objective":0.0,
              "minimum_cell_value":initial_min,
              "moment_residuals":{"mass":0.0,"first":0.0,"second":0.0},
              "moments_before":{"mass":old[0],"first":old[1],"second":old[2]},
              "moments_after":{"mass":old[0],"first":old[1],"second":old[2]},"weights":w}
        return (u,aa,bb),diag
    z=[v for pair in zip(aa,bb) for v in pair]
    pa=[0.0]*len(z); pc=[0.0]*len(z)
    scale=max(1.0,abs(old[1]),abs(old[2]))
    converged=False
    for iteration in range(1,max_iterations+1):
        xin=[x+p for x,p in zip(z,pa)]
        y=_affine_project(xin,e,target,w)
        pa=[x-yy for x,yy in zip(xin,y)]
        cin=[x+p for x,p in zip(y,pc)]
        zn=_positive_project(cin,u,w)
        pc=[x-zz for x,zz in zip(cin,zn)]
        z=zn
        vals=moments(e,u,z[0::2],z[1::2])
        mr=max(abs(vals[1]-target[0]),abs(vals[2]-target[1]))/scale
        minval=min(u[j]+quadratic_minimum(z[2*j],z[2*j+1]) for j in range(n))
        if mr<=tolerance and minval>=-tolerance*max(1.0,max(u)):
            # Fixed-point cycle movement is also required to be small.
            if iteration>1 and max(abs(x-y) for x,y in zip(z,previous))<=tolerance*max(1.0,max(abs(v) for v in z)):
                converged=True; break
        previous=z.copy()
    if not converged:
        raise ArithmeticError("Dykstra projection did not converge; feasibility is unresolved")
    outa=tuple(z[0::2]); outb=tuple(z[1::2]); new=moments(e,u,outa,outb)
    diag={"method":"Dykstra projection: weighted affine moment set intersected with product of exact cell positivity sets",
          "iterations":iteration,"converged":True,"objective":sum(w[0]*(x-y)**2+w[1]*(v-q)**2 for x,y,v,q in zip(outa,aa,outb,bb)),
          "minimum_cell_value":min(u[j]+quadratic_minimum(outa[j],outb[j]) for j in range(n)),
          "moment_residuals":{"mass":new[0]-old[0],"first":new[1]-old[1],"second":new[2]-old[2]},
          "moments_before":{"mass":old[0],"first":old[1],"second":old[2]},
          "moments_after":{"mass":new[0],"first":new[1],"second":new[2]},
          "weights":w}
    return (u,outa,outb),diag



def assess_global_feasibility(target_edges, averages, linear, quadratic,
                              weights=(1.0,1.0), max_iterations=20000,
                              tolerance=2e-11):
    """Classify feasibility without turning generic solver failure into a proof.

    For one cell, the two global moment equalities uniquely determine both
    modal coefficients; positivity can therefore be certified directly.
    For multiple cells, Dykstra success is a numerical feasible witness,
    while nonconvergence is reported as unresolved.
    """
    e=_edges(target_edges,"target_edges"); n=len(e)-1
    u=tuple(float(v) for v in averages); a=tuple(float(v) for v in linear); b=tuple(float(v) for v in quadratic)
    if len(u)!=n or len(a)!=n or len(b)!=n:
        raise ValueError("one finite coefficient triple per cell required")
    if n==1:
        minimum=u[0]+quadratic_minimum(a[0],b[0])
        if minimum >= -tolerance*max(1.0,u[0],abs(a[0]),abs(b[0])):
            return {"status":"feasible","certificate":"single-cell moment map uniquely fixes the supplied coefficients","minimum_cell_value":minimum}
        return {"status":"certified_infeasible","certificate":"single-cell first and second global moments uniquely determine the supplied modal coefficients, whose polynomial has a negative minimum","minimum_cell_value":minimum}
    try:
        result,diag=globally_coupled_positive_projection(e,u,a,b,weights,max_iterations,tolerance)
        return {"status":"feasible","certificate":"numerical feasible witness from converged Dykstra projection","minimum_cell_value":diag["minimum_cell_value"],"moment_residuals":diag["moment_residuals"],"iterations":diag["iterations"],"result":result}
    except ArithmeticError as exc:
        return {"status":"unresolved","certificate":"iteration did not converge; no infeasibility conclusion is justified","detail":str(exc)}


def run_study(output_dir):
    out=Path(output_dir); out.mkdir(parents=True,exist_ok=True)
    edges=(0.0,0.3,0.7,1.0); averages=(1.0,0.8,1.2)
    linear=(3.0,-2.0,2.5); quadratic=(0.0,2.5,0.0)
    projection_error=None
    try:
        result,diag=globally_coupled_positive_projection(edges,averages,linear,quadratic)
        feasibility_status="feasible"
    except ArithmeticError as exc:
        # A failed numerical projection is a valid unresolved outcome, not a
        # reason to fabricate a projected state or abort the reproducible study.
        projection_error=str(exc)
        result=(averages,linear,quadratic)
        feasibility_status="unresolved"
        diag={"method":"Dykstra candidate projection","iterations":20000,"converged":False,
              "minimum_cell_value":min(averages[j]+quadratic_minimum(linear[j],quadratic[j]) for j in range(len(averages))),
              "moment_residuals":{"mass":0.0,"first":0.0,"second":0.0},
              "projection_error":projection_error}
    rows=[]
    for j,(l,r) in enumerate(zip(edges,edges[1:])):
        rows.append({"cell":j,"left":l,"right":r,"average":averages[j],
                     "linear_before":linear[j],"quadratic_before":quadratic[j],
                     "linear_after":result[1][j],"quadratic_after":result[2][j],
                     "minimum_after":averages[j]+quadratic_minimum(result[1][j],result[2][j]),
                     "status":feasibility_status})
    with (out/"p26_6_global_positive_projection.csv").open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)
    impossible=assess_global_feasibility((0.0,1.0),(0.1,),(1.0,),(0.0,))
    summary={"scope":"1-D global moment-constrained positive quadratic projection",
             "cells":len(averages),"feasibility_checks":{"synthetic_feasible_case":feasibility_status,"single_cell_infeasible_case":impossible["status"]},
             **diag,"projection_error":projection_error,
             "limitations":["Dykstra nonconvergence leaves feasibility unresolved; it is not an infeasibility certificate",
             "floating-point stopping tolerances; no formal exact-arithmetic guarantee",
             "fixed cell averages; 1-D intervals and quadratic reconstructions only",
             "no 2-D/3-D extension and no physical validation"]}
    (out/"summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    print(json.dumps(summary,indent=2)); return summary


if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser(); p.add_argument("--output-dir",default="ccfsm-p26-6-results")
    run_study(p.parse_args().output_dir)
