#!/usr/bin/env python3
"""Curated exploratory fits and pointwise residual diagnostics for Wilhelm & Kind chart readings.

Default analysis includes only primary_exploratory and primary_with_local_reversals.
Optional branches can be added explicitly. These are approximate chart readings,
not experimental raw data; no uncertainty weights or inferential intervals are used.
"""
from __future__ import annotations
import argparse
import csv
import math
from collections import defaultdict
from pathlib import Path

PRIMARY = {"primary_exploratory", "primary_with_local_reversals"}
ALL = PRIMARY | {"sensitivity_only", "figure_table_conflict_branch"}

def fit_one_exponential(points):
    ys = [p["y"] for p in points]
    mean_y = sum(ys) / len(ys)
    sst = sum((y - mean_y) ** 2 for y in ys)
    def evaluate(log_tau):
        tau = math.exp(log_tau)
        g = [1.0 - math.exp(-p["t"] / tau) for p in points]
        denom = sum(v * v for v in g)
        amplitude = sum(v * p["y"] for v, p in zip(g, points)) / denom
        residuals = [p["y"] - amplitude * v for p, v in zip(g, points)]
        sse = sum(r * r for r in residuals)
        return sse, amplitude, tau, residuals
    lo, hi = math.log(0.005), math.log(20000.0)
    ratio = (math.sqrt(5.0) - 1.0) / 2.0
    x1, x2 = hi - ratio * (hi - lo), lo + ratio * (hi - lo)
    f1, f2 = evaluate(x1)[0], evaluate(x2)[0]
    for _ in range(240):
        if f1 <= f2:
            hi, x2, f2 = x2, x1, f1
            x1 = hi - ratio * (hi - lo)
            f1 = evaluate(x1)[0]
        else:
            lo, x1, f1 = x1, x2, f2
            x2 = lo + ratio * (hi - lo)
            f2 = evaluate(x2)[0]
    sse, amplitude, tau, residuals = evaluate((lo + hi) / 2.0)
    r2 = 1.0 - sse / sst if sst > 0 else float("nan")
    rmse = math.sqrt(sse / len(points))
    mae = sum(abs(r) for r in residuals) / len(points)
    max_abs = max(abs(r) for r in residuals)
    if len(residuals) > 1:
        m = sum(residuals) / len(residuals)
        den = sum((r - m) ** 2 for r in residuals)
        lag1 = (sum((residuals[i]-m)*(residuals[i-1]-m) for i in range(1,len(residuals))) / den) if den else float("nan")
    else:
        lag1 = float("nan")
    return amplitude, tau, r2, rmse, mae, max_abs, lag1, residuals

def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--published", required=True)
    ap.add_argument("--fits-output", required=True)
    ap.add_argument("--residuals-output", required=True)
    ap.add_argument("--include-sensitivity", action="store_true")
    ap.add_argument("--include-figure-table-conflict", action="store_true")
    args = ap.parse_args()
    allowed = set(PRIMARY)
    if args.include_sensitivity:
        allowed.add("sensitivity_only")
    if args.include_figure_table_conflict:
        allowed.add("figure_table_conflict_branch")
    rows = read_csv(args.input)
    pub_rows = read_csv(args.published)
    pub = {(r["figure"], r["gel_type"], int(r["temperature_C"])):
           (float(r["maximum_relative_shrinkage"]), float(r["tau_h"])) for r in pub_rows}
    groups = defaultdict(list)
    for r in rows:
        if r["source_type"] != "ai_assisted_approximation" or r["reanalysis_use"] not in allowed:
            continue
        key = (r["figure"], r["panel"], r["condition"], r["series"], r["reanalysis_use"])
        groups[key].append({"t": float(r["time_h"]), "y": float(r["relative_shrinkage"]),
                            "point_index": r["point_index"]})
    fit_fields = ["figure","panel","condition","temperature_C","reanalysis_use","n_points",
                  "first_nonzero_time_h","published_A","published_tau_h","fitted_A","fitted_tau_h",
                  "R2","RMSE","MAE","max_abs_residual","residual_lag1_correlation",
                  "A_fit_over_published","tau_fit_over_published"]
    residual_fields = ["figure","panel","condition","temperature_C","reanalysis_use","point_index",
                       "time_h","observed_shrinkage","fitted_shrinkage","residual"]
    with open(args.fits_output,"w",newline="",encoding="utf-8") as ffit, open(args.residuals_output,"w",newline="",encoding="utf-8") as fres:
        fw, rw = csv.DictWriter(ffit,fieldnames=fit_fields), csv.DictWriter(fres,fieldnames=residual_fields)
        fw.writeheader(); rw.writeheader()
        for key, pts in sorted(groups.items()):
            pts.sort(key=lambda p:(p["t"],int(p["point_index"])))
            fig,panel,condition,series,use = key
            temp = int(series.split()[0])
            gel = "acidic" if condition.startswith("acidic") else "basic"
            apub,tpub = pub[(fig.replace("Figure ",""),gel,temp)]
            a,tau,r2,rmse,mae,maxabs,lag1,resids = fit_one_exponential(pts)
            fw.writerow({"figure":fig,"panel":panel,"condition":condition,"temperature_C":temp,
                "reanalysis_use":use,"n_points":len(pts),
                "first_nonzero_time_h":min(p["t"] for p in pts if p["t"]>0),
                "published_A":apub,"published_tau_h":tpub,"fitted_A":a,"fitted_tau_h":tau,
                "R2":r2,"RMSE":rmse,"MAE":mae,"max_abs_residual":maxabs,
                "residual_lag1_correlation":lag1,"A_fit_over_published":a/apub,
                "tau_fit_over_published":tau/tpub})
            for p,res in zip(pts,resids):
                pred = a*(1-math.exp(-p["t"]/tau))
                rw.writerow({"figure":fig,"panel":panel,"condition":condition,"temperature_C":temp,
                    "reanalysis_use":use,"point_index":p["point_index"],"time_h":p["t"],
                    "observed_shrinkage":p["y"],"fitted_shrinkage":pred,"residual":res})
if __name__ == "__main__":
    main()
