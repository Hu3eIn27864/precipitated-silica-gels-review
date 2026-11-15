"""P26.2: conservative quadratic 1-D FE/FV transfer preserving moments 0, 1 and 2."""
from __future__ import annotations
import csv, json, math
from pathlib import Path
_GX=(-math.sqrt(3.0/5.0),0.0,math.sqrt(3.0/5.0)); _GW=(5.0/9.0,8.0/9.0,5.0/9.0)
def _edges(edges,name):
    x=tuple(float(v) for v in edges)
    if len(x)<2 or not all(math.isfinite(v) for v in x) or any(b<=a for a,b in zip(x,x[1:])): raise ValueError(f"{name} must be finite and strictly increasing")
    return x
def quadratic_minimum(a,b):
    def f(x): return a*x+b*(x*x-1.0/12.0)
    vals=[f(-.5),f(.5)]
    if b>0:
        v=-a/(2*b)
        if -.5<v<.5: vals.append(f(v))
    return min(vals)
def limit_quadratic(average,linear,quadratic,positivity=True):
    m,a,b=map(float,(average,linear,quadratic))
    if not all(math.isfinite(v) for v in (m,a,b)): raise ValueError("coefficients must be finite")
    if positivity and m<0: raise ValueError("positivity limiter requires nonnegative cell average")
    if not positivity: return a,b
    d=quadratic_minimum(a,b)
    if m+d>=0 or d>=0: return a,b
    t=max(0.0,min(1.0,m/(-d)))
    return t*a,t*b
def _value(x,left,right,m,a,b):
    h=right-left; xi=(x-.5*(left+right))/h
    return m+a*xi+b*(xi*xi-1/12.0)
def _integrate(lo,hi,sl,sr,coeff,center,width):
    mid=.5*(lo+hi); half=.5*(hi-lo); mass=first=second=0.0
    for z,w in zip(_GX,_GW):
        x=mid+half*z; u=_value(x,sl,sr,*coeff); eta=(x-center)/width; v=half*w*u
        mass+=v; first+=v*eta; second+=v*(eta*eta-1/12.0)
    return mass,first,second
def project_quadratic_moments(source_edges,source_averages,source_linear,source_quadratic,target_edges,positivity=False,domain_tolerance=1e-12):
    se=_edges(source_edges,"source_edges"); te=_edges(target_edges,"target_edges")
    u=tuple(float(v) for v in source_averages); a=tuple(float(v) for v in source_linear); b=tuple(float(v) for v in source_quadratic); n=len(se)-1
    if len(u)!=n or len(a)!=n or len(b)!=n or not all(math.isfinite(v) for v in u+a+b): raise ValueError("one finite coefficient triple per source cell required")
    if positivity and any(v<0 for v in u): raise ValueError("positivity requires nonnegative source averages")
    coeff=[limit_quadratic(m,x,y,True) if positivity else (x,y) for m,x,y in zip(u,a,b)]
    scale=max(1.0,abs(se[0]),abs(se[-1]),abs(te[0]),abs(te[-1])); tol=domain_tolerance*scale
    if abs(se[0]-te[0])>tol or abs(se[-1]-te[-1])>tol: raise ValueError("meshes must cover the same domain")
    om=[]; oa=[]; ob=[]; i=0
    for left,right in zip(te,te[1:]):
        h=right-left; c=.5*(left+right)
        while i<n and se[i+1]<=left: i+=1
        j=i; mass=first=second=covered=0.0
        while j<n and se[j]<right:
            lo=max(left,se[j]); hi=min(right,se[j+1])
            if hi>lo:
                mm,ff,ss=_integrate(lo,hi,se[j],se[j+1],(u[j],*coeff[j]),c,h)
                mass+=mm; first+=ff; second+=ss; covered+=hi-lo
            if se[j+1]>=right: break
            j+=1
        if abs(covered-h)>10*tol: raise ValueError("target cell not fully covered")
        om.append(mass/h); oa.append(12*first/h); ob.append(180*second/h)
    return tuple(om),tuple(oa),tuple(ob)
def moments(edges,averages,linear,quadratic):
    e=_edges(edges,"edges"); u=tuple(averages); a=tuple(linear); b=tuple(quadratic)
    if len(u)!=len(e)-1 or len(a)!=len(u) or len(b)!=len(u): raise ValueError("one coefficient triple per cell required")
    mass=first=second=0.0
    for l,r,m,x,y in zip(e,e[1:],u,a,b):
        h=r-l; c=.5*(l+r); mass+=m*h
        first+=m*h*c+x*h*h/12
        second+=m*h*(c*c+h*h/12)+x*c*h*h/6+y*h**3/180
    return mass,first,second
def run_study(output_dir):
    out=Path(output_dir); out.mkdir(parents=True,exist_ok=True)
    se=(0,.08,.24,.51,.76,1); te=(0,.13,.31,.58,.83,1); u=[]; a=[]; b=[]
    for l,r in zip(se,se[1:]):
        h=r-l; c=.5*(l+r); u.append(2+3*c+4*(c*c+h*h/12)); a.append(h*(3+8*c)); b.append(4*h*h)
    dm,da,db=project_quadratic_moments(se,u,a,b,te); sm,sf,ss=moments(se,u,a,b); tm,tf,ts=moments(te,dm,da,db)
    rows=[{"target_cell":j,"left":l,"right":r,"average":dm[j],"linear_coefficient":da[j],"quadratic_coefficient":db[j]} for j,(l,r) in enumerate(zip(te,te[1:]))]
    with (out/"p26_2_quadratic_projection.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    summary={"scope":"1-D piecewise-quadratic overlap transfer preserving moments 0, 1 and 2 per target cell","source_cells":len(u),"target_cells":len(dm),"source_moments":{"zeroth":sm,"first":sf,"second":ss},"target_moments":{"zeroth":tm,"first":tf,"second":ts},"absolute_residuals":{"zeroth":abs(tm-sm),"first":abs(tf-sf),"second":abs(ts-ss)},"limitations":["quadratic coefficients supplied by caller; no automatic high-order reconstruction","positivity limiter scales both zero-mean modes and can reduce local order","1-D intervals only; no 2-D/3-D geometric intersections","synthetic polynomial verification, not physical validation"]}
    (out/"summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8"); print(json.dumps(summary,indent=2)); return summary
if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser(); p.add_argument("--output-dir",default="ccfsm-p26-2-results"); run_study(p.parse_args().output_dir)
