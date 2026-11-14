#!/usr/bin/env python3
"""Branch-separated sensitivity analysis of approximate natural-syneresis curves.

Fits one exponential and one stretched exponential independently to each
curation branch. This is a descriptive robustness screen, not physical
parameter identification. No pressure-cell data are read.
"""
import argparse, csv, math
from collections import defaultdict
from pathlib import Path

def read_rows(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))

def fit_shape(points, beta, bounds):
    lo, hi = map(math.log, bounds)
    gr = (math.sqrt(5.0) - 1.0) / 2.0
    def evaluate(x):
        tau = math.exp(x)
        shape = [0.0 if t == 0 else 1.0-math.exp(-((t/tau)**beta)) for t, _ in points]
        den = sum(v*v for v in shape)
        amp = min(1.0, max(0.0, sum(v*y for v, (_, y) in zip(shape, points))/den))
        sse = sum((y-amp*v)**2 for v, (_, y) in zip(shape, points))
        return sse, amp, tau
    x1, x2 = hi-gr*(hi-lo), lo+gr*(hi-lo)
    f1, f2 = evaluate(x1)[0], evaluate(x2)[0]
    for _ in range(180):
        if f1 <= f2:
            hi, x2, f2 = x2, x1, f1
            x1 = hi-gr*(hi-lo); f1 = evaluate(x1)[0]
        else:
            lo, x1, f1 = x1, x2, f2
            x2 = lo+gr*(hi-lo); f2 = evaluate(x2)[0]
    sse, amp, tau = evaluate((lo+hi)/2)
    return amp, tau, sse

def aicc(sse, n, k):
    if n <= k+1: return float("inf")
    return n*math.log(max(sse/n, 1e-300))+2*k+2*k*(k+1)/(n-k-1)

def fit_curve(points):
    points = sorted(points)
    times = [t for t, _ in points if t > 0]
    bounds = (max(1e-5, min(times)/1000), max(times)*1000)
    ae, te, se = fit_shape(points, 1.0, bounds)
    best = None
    for j in range(109):
        beta = 0.3 + 0.025*j
        a, tau, sse = fit_shape(points, beta, bounds)
        if best is None or sse < best[0]:
            best = (sse, a, tau, beta)
    ss, ast, tst, beta = best
    n = len(points)
    return {
        "n_points": n, "exp_A": ae, "exp_tau_h": te,
        "exp_RMSE": math.sqrt(se/n), "exp_AICc": aicc(se,n,2),
        "stretch_A": ast, "stretch_tau_h": tst, "stretch_beta": beta,
        "stretch_RMSE": math.sqrt(ss/n), "stretch_AICc": aicc(ss,n,3),
        "delta_AICc_stretch_minus_exp": aicc(ss,n,3)-aicc(se,n,2),
        "stretch_beta_at_search_boundary": beta <= 0.300001 or beta >= 2.999999,
        "stretch_amplitude_at_boundary": ast >= 0.999999,
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--input",required=True)
    ap.add_argument("--output",required=True)
    args=ap.parse_args()
    rows=read_rows(args.input)
    groups=defaultdict(list)
    for r in rows:
        if r.get("source_type") != "ai_assisted_approximation": continue
        key=(r["figure"],r["panel"],r["condition"],r["series"],r["reanalysis_use"])
        groups[key].append((float(r["time_h"]),float(r["relative_shrinkage"])))
    out=[]
    for key, pts in sorted(groups.items()):
        result=fit_curve(pts)
        fig,panel,condition,series,branch=key
        out.append({"figure":fig,"panel":panel,"condition":condition,"temperature":series,
                    "evidence_branch":branch,**result})
    Path(args.output).parent.mkdir(parents=True,exist_ok=True)
    with open(args.output,"w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(out[0]))
        w.writeheader(); w.writerows(out)
    print(f"rows={len(rows)}; curves={len(out)}; output={args.output}")

if __name__=="__main__": main()
