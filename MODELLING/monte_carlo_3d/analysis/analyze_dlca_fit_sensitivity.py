#!/usr/bin/env python3
"""Quantify DLCA apparent-exponent sensitivity across all available fit windows.

This is a diagnostic: it does not select a scaling regime or establish fractality.
"""
from __future__ import annotations

import argparse
import csv
import math
import statistics
from pathlib import Path


def read_rows(path: Path):
    with path.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError(f"Missing CSV header: {path}")
        return list(reader)


def finite(row, key, path):
    try:
        value = float(row[key])
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError(f"Invalid {key} in {path}: {row}") from exc
    if not math.isfinite(value):
        raise ValueError(f"Non-finite {key} in {path}: {row}")
    return value


def analyse(prefix: Path, particle_count: int):
    runs_path = Path(str(prefix) + "_runs.csv")
    mass_path = Path(str(prefix) + "_mass_radius.csv")
    fits_path = Path(str(prefix) + "_fit_windows.csv")
    runs = read_rows(runs_path)
    mass_rows = read_rows(mass_path)
    fits = read_rows(fits_path)
    valid = {}
    for row in runs:
        try:
            seed = int(row["seed"])
            complete = int(row["completed"])
            unwrapped = int(row["unwrapping_consistent"])
            largest = int(row["largest_component_size"])
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError(f"Invalid run metadata in {runs_path}: {row}") from exc
        if complete not in (0, 1) or unwrapped not in (0, 1):
            raise ValueError(f"Boolean run fields must be 0 or 1: {row}")
        if seed in valid:
            raise ValueError(f"Duplicate seed {seed} in {runs_path}")
        if largest < 0 or largest > particle_count:
            raise ValueError(f"Impossible largest-component size in {runs_path}: {row}")
        valid[seed] = complete == 1 and unwrapped == 1 and largest == particle_count

    radii_by_seed = {}
    reference_grid = None
    for row in mass_rows:
        try:
            seed = int(row["seed"])
            recorded_n = int(row["particle_count"])
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError(f"Invalid mass-radius metadata in {mass_path}: {row}") from exc
        if seed not in valid:
            raise ValueError(f"Mass-radius data for unknown seed {seed}")
        if not valid[seed] or recorded_n != particle_count:
            raise ValueError(f"Mass-radius data attached to invalid run or wrong N: {row}")
        radius = finite(row, "radius", mass_path)
        mass = finite(row, "mean_enclosed_mass", mass_path)
        if radius <= 0 or mass <= 0:
            raise ValueError(f"Mass-radius values must be positive: {row}")
        radii = radii_by_seed.setdefault(seed, set())
        if radius in radii:
            raise ValueError(f"Duplicate radius for seed {seed} in {mass_path}")
        radii.add(radius)
    for seed, radii in radii_by_seed.items():
        if reference_grid is None:
            reference_grid = radii
        elif radii != reference_grid:
            raise ValueError(f"Inconsistent mass-radius grid for seed {seed}")

    grouped = {}
    for row in fits:
        try:
            seed = int(row["seed"])
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError(f"Invalid seed in {fits_path}: {row}") from exc
        if seed not in valid:
            raise ValueError(f"Fit for unknown seed {seed} in {fits_path}")
        if not valid[seed]:
            raise ValueError(f"Fit for incomplete or inconsistently unwrapped run {seed}")
        lo = finite(row, "fit_minimum_radius", fits_path)
        hi = finite(row, "fit_maximum_radius", fits_path)
        exponent = finite(row, "exponent", fits_path)
        r2 = finite(row, "r_squared", fits_path)
        count = int(row["point_count"])
        if lo <= 0 or hi <= lo or count < 3 or not 0 <= r2 <= 1:
            raise ValueError(f"Invalid fit metadata in {fits_path}: {row}")
        if seed not in radii_by_seed:
            raise ValueError(f"Fit for seed {seed} has no source mass-radius curve")
        grid = radii_by_seed[seed]
        expected_count = sum(lo <= radius <= hi for radius in grid)
        if lo not in grid or hi not in grid or count != expected_count:
            raise ValueError(f"Fit window/point count does not match source curve: {row}")
        grouped.setdefault(seed, []).append((lo, hi, exponent, r2, count))

    per_seed = []
    for seed in sorted(valid):
        windows = grouped.get(seed, [])
        if not windows:
            per_seed.append({
                "seed": seed, "valid_window_count": 0,
                "minimum_exponent": "", "maximum_exponent": "",
                "exponent_range": "", "median_exponent": "",
                "minimum_r_squared": "", "maximum_r_squared": "",
            })
            continue
        keys = [(w[0], w[1]) for w in windows]
        if len(set(keys)) != len(keys):
            raise ValueError(f"Duplicate fit window for seed {seed}")
        exponents = [w[2] for w in windows]
        r2s = [w[3] for w in windows]
        per_seed.append({
            "seed": seed, "valid_window_count": len(windows),
            "minimum_exponent": min(exponents),
            "maximum_exponent": max(exponents),
            "exponent_range": max(exponents) - min(exponents),
            "median_exponent": statistics.median(exponents),
            "minimum_r_squared": min(r2s),
            "maximum_r_squared": max(r2s),
        })

    all_ranges = [r["exponent_range"] for r in per_seed
                  if r["valid_window_count"] > 0]
    summary = {
        "particle_count": particle_count,
        "runs": len(valid),
        "eligible_runs": sum(valid.values()),
        "runs_with_fit_windows": len(all_ranges),
        "mean_within_run_exponent_range": (
            statistics.mean(all_ranges) if all_ranges else ""),
        "maximum_within_run_exponent_range": (
            max(all_ranges) if all_ranges else ""),
        "interpretation": "diagnostic_only_no_scaling_window_selected",
    }
    return per_seed, summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--system", action="append", required=True,
                        metavar="N:PREFIX")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    all_runs, summaries = [], []
    seen_sizes = set()
    for item in args.system:
        try:
            n_text, prefix_text = item.split(":", 1)
            n = int(n_text)
        except ValueError as exc:
            raise SystemExit(f"Invalid --system {item!r}; expected N:PREFIX") from exc
        if n <= 0 or not prefix_text or n in seen_sizes:
            raise SystemExit(f"Invalid or duplicate system: {item}")
        seen_sizes.add(n)
        per_seed, summary = analyse(Path(prefix_text), n)
        for row in per_seed:
            all_runs.append({"particle_count": n, **row})
        summaries.append(summary)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    per_path = Path(str(args.output) + "_fit_sensitivity_per_run.csv")
    sum_path = Path(str(args.output) + "_fit_sensitivity_summary.csv")
    with per_path.open("w", newline="", encoding="utf-8") as handle:
        fields = ["particle_count", "seed", "valid_window_count",
                  "minimum_exponent", "maximum_exponent", "exponent_range",
                  "median_exponent", "minimum_r_squared", "maximum_r_squared"]
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(all_runs)
    with sum_path.open("w", newline="", encoding="utf-8") as handle:
        fields = list(summaries[0])
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(summaries)
    print(f"Wrote {per_path} and {sum_path}")
    print("Fit-window ranges are diagnostics, not evidence for a unique scaling regime.")


if __name__ == "__main__":
    main()
