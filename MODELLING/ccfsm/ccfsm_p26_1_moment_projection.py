"""P26.1: conservative, first-moment-preserving piecewise-linear 1-D FE/FV transfer."""
from __future__ import annotations
import csv, json, math
from pathlib import Path

def _edges(edges, name):
    x=tuple(float(v) for v in edges)
    if len(x)<2 or not all(math.isfinite(v) for v in x) or any(b<=a for a,b in zip(x,x[1:])):
        raise ValueError(f"{name} must be finite and strictly increasing")
    return x

def minmod(a,b):
    if a*b<=0: return 0.0
    return math.copysign(min(abs(a),abs(b)),a)

def limited_linear_slopes(edges, averages, positivity=True):
    """Build monotone minmod slopes; optionally enforce nonnegative edge values."""
    e=_edges(edges,"edges"); u=tuple(float(v) for v in averages); n=len(e)-1
    if len(u)!=n or not all(math.isfinite(v) for v in u): raise ValueError("one finite average per cell required")
    if positivity and any(v<0 for v in u): raise ValueError("positivity limiter requires nonnegative cell averages")
    c=[(a+b)/2 for a,b in zip(e,e[1:])]
    sec=[(u[i+1]-u[i])/(c[i+1]-c[i]) for i in range(n-1)]
    slopes=[]
    for i in range(n):
        if n==1: s=0.0
        elif i==0: s=sec[0]
        elif i==n-1: s=sec[-1]
        else: s=minmod(sec[i-1],sec[i])
        if positivity:
            half=0.5*(e[i+1]-e[i])
            if abs(s)*half>u[i] and s!=0:
                s=math.copysign(u[i]/half,s)
        slopes.append(s)
    return tuple(slopes)

def project_linear_moments(source_edges, source_averages, source_slopes, target_edges, domain_tolerance=1e-12):
    """Project piecewise-linear source reconstructions, preserving 0th and 1st moments per target cell."""
    se=_edges(source_edges,"source_edges"); te=_edges(target_edges,"target_edges")
    u=tuple(float(v) for v in source_averages); s=tuple(float(v) for v in source_slopes)
    if len(u)!=len(se)-1 or len(s)!=len(u) or not all(math.isfinite(v) for v in u+s):
        raise ValueError("one finite average and slope per source cell required")
    scale=max(1.0,*(abs(v) for v in (se[0],se[-1],te[0],te[-1]))); tol=domain_tolerance*scale
    if abs(se[0]-te[0])>tol or abs(se[-1]-te[-1])>tol: raise ValueError("meshes must cover the same domain")
    means=[]; slopes=[]; i=0
    for left,right in zip(te,te[1:]):
        center=0.5*(left+right); width=right-left
        while i<len(u) and se[i+1]<=left: i+=1
        j=i; mass=0.0; centered_first=0.0; covered=0.0
        while j<len(u) and se[j]<right:
            a=max(left,se[j]); b=min(right,se[j+1])
            if b>a:
                cs=0.5*(se[j]+se[j+1])
                mass += u[j]*(b-a)+0.5*s[j]*((b-cs)**2-(a-cs)**2)
                # Integral (x-center)*(u_j+s_j*(x-cs)) dx
                centered_first += 0.5*u[j]*((b-center)**2-(a-center)**2)
                centered_first += s[j]*((b**3-a**3)/3.0-(center+cs)*(b*b-a*a)/2.0+center*cs*(b-a))
                covered += b-a
            if se[j+1]>=right: break
            j+=1
        if abs(covered-width)>10*tol: raise ValueError("target cell not fully covered")
        means.append(mass/width)
        slopes.append(12.0*centered_first/(width**3))
    return tuple(means),tuple(slopes)

def moments(edges, averages, slopes):
    """Return global integral and first spatial moment of a piecewise-linear field."""
    e=_edges(edges,"edges"); u=tuple(averages); s=tuple(slopes)
    if len(u)!=len(e)-1 or len(s)!=len(u): raise ValueError("one average and slope per cell required")
    mass=first=0.0
    for a,b,v,g in zip(e,e[1:],u,s):
        c=0.5*(a+b)
        mass += v*(b-a)
        first += 0.5*v*(b*b-a*a)+g*((b**3-a**3)/3.0-c*(b*b-a*a)/2.0)
    return mass,first

def run_study(output_dir):
    out=Path(output_dir); out.mkdir(parents=True,exist_ok=True)
    se=(0.0,0.08,0.24,0.51,0.76,1.0); te=(0.0,0.13,0.31,0.58,0.83,1.0)
    # Exact cell averages of u(x)=2+3x; reconstruction recovers its exact slope.
    src=tuple(2.0+3.0*(a+b)/2 for a,b in zip(se,se[1:]))
    ss=limited_linear_slopes(se,src,positivity=True)
    dst,ds=project_linear_moments(se,src,ss,te)
    sm,sf=moments(se,src,ss); tm,tf=moments(te,dst,ds)
    rows=[{"target_cell":j,"left":a,"right":b,"average":dst[j],"slope":ds[j]} for j,(a,b) in enumerate(zip(te,te[1:]))]
    with (out/"p26_1_moment_projection.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    summary={"scope":"1-D piecewise-linear overlap transfer preserving cell mass and first centered moment","source_cells":len(src),"target_cells":len(dst),"source_mass":sm,"target_mass":tm,"mass_residual":abs(tm-sm),"source_first_moment":sf,"target_first_moment":tf,"first_moment_residual":abs(tf-sf),"source_slopes":ss,"target_slopes":ds,"limitations":["minmod reconstruction is limited and generally first-order near extrema","1-D intervals only; no 2-D/3-D geometric intersections","synthetic verification, not physical validation"]}
    (out/"summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8"); print(json.dumps(summary,indent=2)); return summary

if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser(); p.add_argument("--output-dir",default="ccfsm-p26-1-results"); run_study(p.parse_args().output_dir)
