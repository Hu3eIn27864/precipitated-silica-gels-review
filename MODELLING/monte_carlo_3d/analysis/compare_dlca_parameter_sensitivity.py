#!/usr/bin/env python3
"""Paired seed-level comparison of DLCA parameter variants against a baseline.

The script preserves all seed outcomes. Structural deltas are calculated only
for pairs for which the corresponding observable is defined in both runs.
"""
from __future__ import annotations

import argparse
import csv
import math
import statistics
from pathlib import Path

from analyze_dlca_ensembles import load_system


def mean_or_blank(values):
    return statistics.mean(values) if values else ""


def sd_or_blank(values):
    return statistics.stdev(values) if len(values) >= 2 else ""


def compare_rows(baseline_rows, variant_rows, variant_name):
    base = {row["seed"]: row for row in baseline_rows}
    variant = {row["seed"]: row for row in variant_rows}
    if set(base) != set(variant):
        missing = sorted(set(base) - set(variant))
        extra = sorted(set(variant) - set(base))
        raise ValueError(
            f"Seed sets differ for {variant_name}; missing={missing}, extra={extra}"
        )

    paired = []
    for seed in sorted(base):
        b, v = base[seed], variant[seed]
        delta_largest = (
            v["largest_component_fraction"] - b["largest_component_fraction"]
        )
        b_rg, v_rg = b["largest_component_rg"], v["largest_component_rg"]
        b_df, v_df = b["df"], v["df"]
        rg_valid = b_rg is not None and v_rg is not None
        df_valid = b_df is not None and v_df is not None
        paired.append({
            "variant": variant_name,
            "seed": seed,
            "baseline_completed": b["completed"],
            "variant_completed": v["completed"],
            "baseline_unwrapped": b["unwrapping_consistent"],
            "variant_unwrapped": v["unwrapping_consistent"],
            "baseline_largest_fraction": b["largest_component_fraction"],
            "variant_largest_fraction": v["largest_component_fraction"],
            "delta_largest_fraction": delta_largest,
            "rg_pair_valid": int(rg_valid),
            "baseline_rg": "" if b_rg is None else b_rg,
            "variant_rg": "" if v_rg is None else v_rg,
            "delta_rg": (v_rg - b_rg) if rg_valid else "",
            "df_pair_valid": int(df_valid),
            "baseline_df": "" if b_df is None else b_df,
            "variant_df": "" if v_df is None else v_df,
            "delta_df": (v_df - b_df) if df_valid else "",
        })

    rg_deltas = [r["delta_rg"] for r in paired if r["rg_pair_valid"]]
    df_deltas = [r["delta_df"] for r in paired if r["df_pair_valid"]]
    largest_deltas = [r["delta_largest_fraction"] for r in paired]
    summary = {
        "variant": variant_name,
        "paired_seeds": len(paired),
        "baseline_completed": sum(r["baseline_completed"] for r in paired),
        "variant_completed": sum(r["variant_completed"] for r in paired),
        "both_completed": sum(
            r["baseline_completed"] == 1 and r["variant_completed"] == 1
            for r in paired
        ),
        "both_unwrapped_completed": sum(
            r["baseline_completed"] == 1 and r["variant_completed"] == 1
            and r["baseline_unwrapped"] == 1 and r["variant_unwrapped"] == 1
            for r in paired
        ),
        "valid_rg_pairs": len(rg_deltas),
        "valid_df_pairs": len(df_deltas),
        "delta_largest_fraction_mean": mean_or_blank(largest_deltas),
        "delta_largest_fraction_sd": sd_or_blank(largest_deltas),
        "delta_rg_mean": mean_or_blank(rg_deltas),
        "delta_rg_sd": sd_or_blank(rg_deltas),
        "delta_df_mean": mean_or_blank(df_deltas),
        "delta_df_sd": sd_or_blank(df_deltas),
    }
    return paired, summary


def parse_system(value):
    if "=" not in value:
        raise argparse.ArgumentTypeError("Expected NAME=N:PREFIX")
    name, system = value.split("=", 1)
    if not name or ":" not in system:
        raise argparse.ArgumentTypeError("Expected NAME=N:PREFIX")
    n_text, prefix = system.split(":", 1)
    try:
        n = int(n_text)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("N must be an integer") from exc
    if n <= 0 or not prefix:
        raise argparse.ArgumentTypeError("N and prefix must be positive/non-empty")
    return name, n, Path(prefix)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", required=True, metavar="N:PREFIX")
    parser.add_argument("--variant", action="append", required=True,
                        type=parse_system, metavar="NAME=N:PREFIX")
    parser.add_argument("--fit-min", type=float, required=True)
    parser.add_argument("--fit-max", type=float, required=True)
    parser.add_argument("--output", type=Path, required=True,
                        help="output prefix for *_paired_per_seed.csv and *_paired_summary.csv")
    args = parser.parse_args()
    if not (math.isfinite(args.fit_min) and math.isfinite(args.fit_max)
            and 0 < args.fit_min < args.fit_max):
        parser.error("Fit bounds must be finite, positive, and increasing")

    try:
        n_text, baseline_prefix = args.baseline.split(":", 1)
        n = int(n_text)
        if n <= 0 or not baseline_prefix:
            raise ValueError
    except ValueError:
        parser.error("--baseline must be N:PREFIX with positive N")

    baseline_rows, _ = load_system(n, Path(baseline_prefix),
                                   args.fit_min, args.fit_max)
    names = [item[0] for item in args.variant]
    if len(names) != len(set(names)) or "baseline" in names:
        parser.error("Variant names must be unique and cannot be 'baseline'")

    all_rows, summaries = [], []
    for name, variant_n, prefix in args.variant:
        if variant_n != n:
            parser.error(f"Variant {name} has N={variant_n}; baseline has N={n}")
        variant_rows, _ = load_system(n, prefix, args.fit_min, args.fit_max)
        rows, summary = compare_rows(baseline_rows, variant_rows, name)
        all_rows.extend(rows)
        summaries.append(summary)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    per_fields = [
        "variant", "seed", "baseline_completed", "variant_completed",
        "baseline_unwrapped", "variant_unwrapped",
        "baseline_largest_fraction", "variant_largest_fraction",
        "delta_largest_fraction", "rg_pair_valid", "baseline_rg",
        "variant_rg", "delta_rg", "df_pair_valid", "baseline_df",
        "variant_df", "delta_df",
    ]
    summary_fields = list(summaries[0].keys())
    for suffix, rows, fields in (
        ("_paired_per_seed.csv", all_rows, per_fields),
        ("_paired_summary.csv", summaries, summary_fields),
    ):
        path = Path(str(args.output) + suffix)
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)
        print(f"Wrote {path}")
    print("Positive deltas mean the variant exceeds the baseline.")
    print("Rg and exponent deltas use only pairs with both observables valid.")
    print("Incomplete or unwrapped-invalid seeds remain in the per-seed output.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
