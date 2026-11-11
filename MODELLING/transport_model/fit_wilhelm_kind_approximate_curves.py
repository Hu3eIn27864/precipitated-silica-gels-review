#!/usr/bin/env python3
"""Exploratory single-exponential fits to AI-assisted, unverified chart readings.

Model: y(t) = A * (1 - exp(-t/tau)).
No weighting is applied because point-level uncertainties are unavailable.
The fit is descriptive only and must not be treated as experimental validation.
"""
from __future__ import annotations
import argparse
import csv
import math
from collections import defaultdict
from pathlib import Path


def fit_one_exponential(points):
    ys = [p[1] for p in points]
    mean_y = sum(ys) / len(ys)
    sst = sum((y - mean_y) ** 2 for y in ys)

    def evaluate(log_tau):
        tau = math.exp(log_tau)
        g = [1.0 - math.exp(-t / tau) for t, _ in points]
        denom = sum(v * v for v in g)
        amplitude = sum(v * y for v, (_, y) in zip(g, points)) / denom
        sse = sum((y - amplitude * v) ** 2 for v, (_, y) in zip(g, points))
        return sse, amplitude, tau

    # Golden-section minimisation in log(tau); broad bounds cover both figures.
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
    sse, amplitude, tau = evaluate((lo + hi) / 2.0)
    r2 = 1.0 - sse / sst if sst > 0 else float("nan")
    rmse = math.sqrt(sse / len(points))
    return amplitude, tau, r2, rmse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    groups = defaultdict(list)
    with open(args.input, newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row["source_type"] != "ai_assisted_approximation":
                continue
            key = (row["figure"], row["panel"], row["condition"], row["series"])
            groups[key].append((float(row["time_h"]), float(row["relative_shrinkage"])))

    published = {
        ("Figure 8", "a", "acidic, pH < pHiso", "20 °C"): (0.20, 21.3),
        ("Figure 8", "a", "acidic, pH < pHiso", "40 °C"): (0.20, 11.7),
        ("Figure 8", "a", "acidic, pH < pHiso", "60 °C"): (0.20, 5.0),
        ("Figure 8", "b", "basic, pH > pHiso", "20 °C"): (0.30, 50.1),
        ("Figure 8", "b", "basic, pH > pHiso", "40 °C"): (0.39, 32.0),
        ("Figure 8", "b", "basic, pH > pHiso", "60 °C"): (0.51, 27.5),
        ("Figure 10", "a", "acidic, pH < pHiso", "20 °C"): (0.37, 0.40),
        ("Figure 10", "a", "acidic, pH < pHiso", "40 °C"): (0.41, 0.64),
        ("Figure 10", "a", "acidic, pH < pHiso", "60 °C"): (0.48, 0.77),
        ("Figure 10", "b", "basic, pH > pHiso", "20 °C"): (0.30, 0.67),
        ("Figure 10", "b", "basic, pH > pHiso", "40 °C"): (0.39, 0.57),
        ("Figure 10", "b", "basic, pH > pHiso", "60 °C"): (0.51, 0.95),
    }
    fields = ["figure", "panel", "condition", "temperature_C", "n_points",
              "first_nonzero_time_h", "published_A", "published_tau_h",
              "fitted_A", "fitted_tau_h", "R2", "RMSE",
              "fitted_to_published_A_ratio", "fitted_to_published_tau_ratio",
              "data_status"]
    with open(args.output, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for key in sorted(groups):
            points = sorted(groups[key])
            a_pub, tau_pub = published[key]
            a_fit, tau_fit, r2, rmse = fit_one_exponential(points)
            writer.writerow({
                "figure": key[0], "panel": key[1], "condition": key[2],
                "temperature_C": int(key[3].split()[0]), "n_points": len(points),
                "first_nonzero_time_h": f"{next(t for t, y in points if t > 0):.4f}",
                "published_A": f"{a_pub:.4f}", "published_tau_h": f"{tau_pub:.4f}",
                "fitted_A": f"{a_fit:.6f}", "fitted_tau_h": f"{tau_fit:.6f}",
                "R2": f"{r2:.6f}", "RMSE": f"{rmse:.6f}",
                "fitted_to_published_A_ratio": f"{a_fit/a_pub:.6f}",
                "fitted_to_published_tau_ratio": f"{tau_fit/tau_pub:.6f}",
                "data_status": "AI-assisted unverified approximation; exploratory fit only",
            })


if __name__ == "__main__":
    main()
