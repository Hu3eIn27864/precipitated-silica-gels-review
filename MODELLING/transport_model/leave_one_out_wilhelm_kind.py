#!/usr/bin/env python3
"""Leave-one-out sensitivity analysis for AI-assisted unverified chart readings."""
from __future__ import annotations
import argparse
import csv
from collections import defaultdict
from fit_wilhelm_kind_approximate_curves import fit_one_exponential


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--summary-output", required=True)
    parser.add_argument("--detail-output", required=True)
    args = parser.parse_args()
    groups = defaultdict(list)
    with open(args.input, newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row["source_type"] != "ai_assisted_approximation":
                continue
            key = (row["figure"], row["panel"], row["condition"], row["series"])
            groups[key].append({"index": int(row["point_index"]),
                                "time": float(row["time_h"]),
                                "value": float(row["relative_shrinkage"])})
    summary_fields = ["figure","panel","condition","temperature_C","n_points",
        "baseline_A","baseline_tau_h","baseline_R2","LOO_A_min","LOO_A_max",
        "LOO_tau_min_h","LOO_tau_max_h","A_range_percent_of_baseline",
        "tau_range_percent_of_baseline","most_influential_point_index_by_tau",
        "influential_point_time_h","influential_point_value",
        "tau_change_when_omitted_percent"]
    detail_fields = ["figure","panel","condition","temperature_C","omitted_point_index",
        "omitted_time_h","omitted_relative_shrinkage","remaining_points","LOO_A",
        "LOO_tau_h","LOO_R2","delta_A","delta_tau_h","relative_delta_A_percent",
        "relative_delta_tau_percent"]
    with open(args.summary_output,"w",newline="",encoding="utf-8") as sf, open(args.detail_output,"w",newline="",encoding="utf-8") as df:
        sw,dw=csv.DictWriter(sf,fieldnames=summary_fields),csv.DictWriter(df,fieldnames=detail_fields)
        sw.writeheader(); dw.writeheader()
        for key in sorted(groups):
            pts=sorted(groups[key],key=lambda p:p["index"])
            base=fit_one_exponential([(p["time"],p["value"]) for p in pts])
            results=[]
            for i, omitted in enumerate(pts):
                subset=[p for j,p in enumerate(pts) if j!=i]
                fit=fit_one_exponential([(p["time"],p["value"]) for p in subset])
                da,dt=fit[0]-base[0],fit[1]-base[1]
                ra,rt=100*da/base[0],100*dt/base[1]
                results.append((omitted,fit,da,dt,ra,rt))
                dw.writerow(dict(zip(detail_fields,[key[0],key[1],key[2],int(key[3].split()[0]),
                    omitted["index"],omitted["time"],omitted["value"],len(subset),
                    f"{fit[0]:.8f}",f"{fit[1]:.8f}",f"{fit[2]:.8f}",f"{da:.8f}",
                    f"{dt:.8f}",f"{ra:.3f}",f"{rt:.3f}"])))
            amin,amax=min(x[1][0] for x in results),max(x[1][0] for x in results)
            tmin,tmax=min(x[1][1] for x in results),max(x[1][1] for x in results)
            influential=max(results,key=lambda x:abs(x[5]))
            sw.writerow(dict(zip(summary_fields,[key[0],key[1],key[2],int(key[3].split()[0]),
                len(pts),f"{base[0]:.6f}",f"{base[1]:.6f}",f"{base[2]:.6f}",
                f"{amin:.6f}",f"{amax:.6f}",f"{tmin:.6f}",f"{tmax:.6f}",
                f"{100*(amax-amin)/base[0]:.2f}",f"{100*(tmax-tmin)/base[1]:.2f}",
                influential[0]["index"],influential[0]["time"],influential[0]["value"],
                f"{influential[5]:.2f}"])))

if __name__ == "__main__":
    main()
