"""P26.7: dual separation diagnostics for global positive quadratic moments."""
from __future__ import annotations
import csv, json, math
from pathlib import Path
from ccfsm_p26_2_quadratic_projection import _edges, moments

def _golden_max(fun,left,right):
    ratio=(math.sqrt(5.0)-1.0)/2.0
    x1=right-ratio*(right-left); x2=left+ratio*(right-left)
    f1=fun(x1); f2=fun(x2)
    for _ in range(100):
        if right-left<2e-14: break
        if f1>=f2:
            right,x2,f2=x2,x1,f1; x1=right-ratio*(right-left); f1=fun(x1)
        else:
            left,x1,f1=x1,x2,f2; x2=left+ratio*(right-left); f2=fun(x2)
    x=.5*(left+right); return x,fun(x)

def cell_support_function(mean,direction_a,direction_b,samples=1024):
    m=float(mean); p=float(direction_a); q=float(direction_b)
    if not all(math.isfinite(v) for v in (m,p,q)) or m<0: raise ValueError("finite direction and nonnegative mean required")
    if m==0: return 0.0,(0.0,0.0)
    candidates=[(0.0,-6*m),(3*m,3*m),(-3*m,3*m)]
    left=-2*math.pi/3; right=2*math.pi/3
    def point(t): return (math.sqrt(12)*m*math.sin(t),6*m*(1+math.cos(t)))
    def objective(t):
        a,b=point(t); return p*a+q*b
    ts=[left+(right-left)*i/samples for i in range(samples+1)]
    fs=[objective(t) for t in ts]
    for i in range(1,samples):
        if fs[i]>=fs[i-1] and fs[i]>=fs[i+1]:
            t,_=_golden_max(objective,ts[i-1],ts[i+1]); candidates.append(point(t))
    best=max(candidates,key=lambda z:p*z[0]+q*z[1])
    return p*best[0]+q*best[1],best

def _moment_vectors(edges):
    g1=[]; g2=[]
    for l,r in zip(edges,edges[1:]):
        h=r-l; c=.5*(l+r); g1.append((h*h/12,0.0)); g2.append((c*h*h/6,h**3/180))
    return g1,g2

def _support(edges,averages,direction,samples):
    g1,g2=_moment_vectors(edges); total=0.; cells=[]
    for m,(x1,y1),(x2,y2) in zip(averages,g1,g2):
        val,pt=cell_support_function(m,direction[0]*x1+direction[1]*x2,
            direction[0]*y1+direction[1]*y2,samples)
        total+=val; cells.append({"linear":pt[0],"quadratic":pt[1],"support":val})
    return total,cells

def dual_feasibility_diagnostic(target_edges,averages,linear,quadratic,
                                angular_samples=720,boundary_samples=1024,tolerance=1e-9):
    e=_edges(target_edges,"target_edges"); n=len(e)-1
    u=tuple(float(v) for v in averages); a=tuple(float(v) for v in linear); b=tuple(float(v) for v in quadratic)
    if len(u)!=n or len(a)!=n or len(b)!=n or not all(math.isfinite(v) for v in u+a+b):
        raise ValueError("one finite coefficient triple per cell required")
    if any(v<0 for v in u): raise ValueError("nonnegative cell means required")
    if angular_samples<32 or boundary_samples<32: raise ValueError("sampling counts must be >= 32")
    old=moments(e,u,a,b); base=moments(e,u,(0.,)*n,(0.,)*n)
    target=(old[1]-base[1],old[2]-base[2]); scale=max(1.,abs(target[0]),abs(target[1]),sum(u))
    def gap(angle):
        y=(math.cos(angle),math.sin(angle)); support,_=_support(e,u,y,boundary_samples)
        return y[0]*target[0]+y[1]*target[1]-support
    angles=[2*math.pi*i/angular_samples for i in range(angular_samples)]
    vals=[gap(t) for t in angles]; step=2*math.pi/angular_samples
    candidates=[(max(vals),angles[vals.index(max(vals))])]
    for i,v in enumerate(vals):
        if v>=vals[(i-1)%angular_samples] and v>=vals[(i+1)%angular_samples]:
            t,g=_golden_max(gap,angles[i]-step,angles[i]+step); candidates.append((g,t))
    best_gap,angle=max(candidates,key=lambda z:z[0]); direction=(math.cos(angle),math.sin(angle))
    support,cells=_support(e,u,direction,boundary_samples)
    lhs=direction[0]*target[0]+direction[1]*target[1]
    if best_gap>tolerance*scale: status="numerical_separator"; explanation="Strict numerical support-function gap found."
    elif all(m==0 for m in u) and abs(target[0])+abs(target[1])<=tolerance*scale:
        status="feasible"; explanation="Zero means force all nonnegative cell polynomials to vanish."
    else: status="no_separator_found"; explanation="No strict numerical separator found; this does not prove feasibility."
    return {"status":status,"explanation":explanation,"target_modal_moments":target,
      "direction":direction,"target_dot_direction":lhs,"support_value":support,
      "separation_gap":lhs-support,"relative_gap":(lhs-support)/scale,"cell_support_points":cells,
      "angular_samples":angular_samples,"boundary_samples":boundary_samples,
      "certificate_level":"floating-point numerical witness; not interval-certified",
      "moment_targets":{"mass":old[0],"first":old[1],"second":old[2]}}

def run_study(output_dir):
    out=Path(output_dir); out.mkdir(parents=True,exist_ok=True); e=(0.,.4,1.)
    cases=[("feasible_zero_modes",e,(1.,.7),(0.,0.),(0.,0.)),
      ("infeasible_zero_inventory",e,(0.,0.),(1.,0.),(0.,0.)),
      ("candidate_nonnegative",e,(1.,.8),(.2,-.1),(.1,0.))]
    rows=[]
    for name,edges,u,a,b in cases:
        d=dual_feasibility_diagnostic(edges,u,a,b)
        rows.append({"case":name,"status":d["status"],"gap":d["separation_gap"],
          "relative_gap":d["relative_gap"],"direction_1":d["direction"][0],
          "direction_2":d["direction"][1],"certificate_level":d["certificate_level"]})
    with (out/"p26_7_dual_feasibility.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    summary={"scope":"1-D dual support-function feasibility diagnostic","cases":rows,
      "limitations":["floating-point support and angular search, not interval-certified proof",
      "no-separator-found does not prove feasibility","1-D intervals and quadratic reconstructions only","no physical validation"]}
    (out/"summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    print(json.dumps(summary,indent=2)); return summary

if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser(); p.add_argument("--output-dir",default="ccfsm-p26-7-results"); run_study(p.parse_args().output_dir)
