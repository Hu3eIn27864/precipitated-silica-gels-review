"""CCFSM P26: conservative FE-quadrature/FV transfer on nonmatching 1-D meshes."""
from __future__ import annotations
import csv, json, math
from pathlib import Path

def _edges(edges, name):
    x=tuple(float(v) for v in edges)
    if len(x)<2 or not all(math.isfinite(v) for v in x) or any(b<=a for a,b in zip(x,x[1:])):
        raise ValueError(f"{name} must be finite and strictly increasing")
    return x

def quadrature_to_cell_averages(cell_edges, values, weights, cell_indices):
    e=_edges(cell_edges,"cell_edges"); v,w,idx=tuple(values),tuple(weights),tuple(cell_indices)
    n=len(e)-1
    if not v or len(v)!=len(w) or len(v)!=len(idx): raise ValueError("quadrature arrays must have equal nonzero length")
    sums=[0.0]*n; ws=[0.0]*n
    for value,weight,k in zip(v,w,idx):
        value=float(value); weight=float(weight)
        if not math.isfinite(value) or not math.isfinite(weight) or weight<=0: raise ValueError("finite values and positive weights required")
        if not isinstance(k,int) or k<0 or k>=n: raise ValueError("quadrature cell index out of range")
        sums[k]+=weight*value; ws[k]+=weight
    if any(a<=0 for a in ws): raise ValueError("every source cell needs positive quadrature weight")
    return tuple(a/b for a,b in zip(sums,ws))

def conservative_overlap_projection(source_edges, source_averages, target_edges, domain_tolerance=1e-12):
    se=_edges(source_edges,"source_edges"); te=_edges(target_edges,"target_edges")
    sv=tuple(float(v) for v in source_averages)
    if len(sv)!=len(se)-1 or not all(math.isfinite(v) for v in sv): raise ValueError("one finite average per source cell required")
    scale=max(1.0,*(abs(v) for v in (se[0],se[-1],te[0],te[-1])))
    tol=domain_tolerance*scale
    if abs(se[0]-te[0])>tol or abs(se[-1]-te[-1])>tol: raise ValueError("meshes must cover the same domain")
    out=[]; i=0
    for left,right in zip(te,te[1:]):
        while i<len(sv) and se[i+1]<=left+tol: i+=1
        j=i; integ=0.0; covered=0.0
        while j<len(sv) and se[j]<right-tol:
            overlap=max(0.0,min(right,se[j+1])-max(left,se[j]))
            integ+=overlap*sv[j]; covered+=overlap
            if se[j+1]>=right-tol: break
            j+=1
        if abs(covered-(right-left))>10*tol: raise ValueError("target cell not fully covered")
        out.append(integ/(right-left))
    return tuple(out)

def integral(edges, averages):
    e=_edges(edges,"edges"); v=tuple(averages)
    if len(v)!=len(e)-1: raise ValueError("one average per cell required")
    return sum((b-a)*x for a,b,x in zip(e,e[1:],v))

def run_study(output_dir):
    out=Path(output_dir); out.mkdir(parents=True,exist_ok=True)
    se=(0.0,0.10,0.33,0.70,1.0); te=(0.0,0.20,0.40,0.65,0.90,1.0)
    src=tuple(2+3*(a+b)/2 for a,b in zip(se,se[1:]))
    dst=conservative_overlap_projection(se,src,te)
    rows=[{"target_cell":j,"left":a,"right":b,"projected_average":dst[j],"cell_integral":(b-a)*dst[j]} for j,(a,b) in enumerate(zip(te,te[1:]))]
    with (out/"nonmatching_projection.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    si=integral(se,src); ti=integral(te,dst)
    summary={"scope":"1-D positive overlap projection of piecewise-constant source-cell averages","source_cells":len(src),"target_cells":len(dst),"source_integral":si,"target_integral":ti,"relative_integral_residual":abs(ti-si)/max(1.0,abs(si)),"limitations":["not arbitrary 2-D/3-D intersections","piecewise-constant source reconstruction","synthetic geometry; no physical validation"]}
    (out/"summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8"); print(json.dumps(summary,indent=2)); return summary

if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser(); p.add_argument("--output-dir",default="ccfsm-p26-results"); run_study(p.parse_args().output_dir)
