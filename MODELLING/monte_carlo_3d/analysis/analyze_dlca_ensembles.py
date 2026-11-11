#!/usr/bin/env python3
"""Summarise independent DLCA runs without treating fit windows as replicates.

Example:
  python3 analysis/analyze_dlca_ensembles.py \
    --system 32:results/n32 --system 64:results/n64 \
    --fit-min 2 --fit-max 5 --output results/ensemble_summary
"""
from __future__ import annotations

import argparse
import csv
import math
import statistics
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


def read_csv(path: Path) -> List[dict]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError(f"Missing CSV header: {path}")
        return list(reader)


def as_int(row: dict, key: str, path: Path) -> int:
    try:
        value = int(row[key])
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError(f"Invalid integer field '{key}' in {path}: {row}") from exc
    return value


def as_float(row: dict, key: str, path: Path, allow_blank: bool = False):
    raw = row.get(key, "")
    if allow_blank and raw == "":
        return None
    if allow_blank and raw.strip().lower() == "nan":
        return None
    try:
        value = float(raw)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Invalid numeric field '{key}' in {path}: {row}") from exc
    if not math.isfinite(value):
        raise ValueError(f"Non-finite field '{key}' in {path}: {row}")
    return value


def sample_sd(values: List[float]):
    return statistics.stdev(values) if len(values) >= 2 else None


def fmt(value):
    return "" if value is None else f"{value:.10g}"


def load_system(particle_count: int, prefix: Path,
                fit_min: float, fit_max: float) -> Tuple[List[dict], dict]:
    runs_path = Path(str(prefix) + "_runs.csv")
    mass_path = Path(str(prefix) + "_mass_radius.csv")
    fits_path = Path(str(prefix) + "_fit_windows.csv")
    runs = read_csv(runs_path)
    mass_rows = read_csv(mass_path)
    fit_rows = read_csv(fits_path)

    # Validate the underlying mass-radius observations before trusting derived fits.
    radii_by_seed: Dict[int, set] = {}
    reference_radii = None
    for row in mass_rows:
        seed = as_int(row, "seed", mass_path)
        recorded_count = as_int(row, "particle_count", mass_path)
        if recorded_count != particle_count:
            raise ValueError(
                f"Particle count mismatch for seed {seed} in {mass_path}: "
                f"expected {particle_count}, found {recorded_count}"
            )
        radius = as_float(row, "radius", mass_path)
        mass = as_float(row, "mean_enclosed_mass", mass_path)
        if radius <= 0.0 or mass <= 0.0:
            raise ValueError(f"Mass-radius values must be positive in {mass_path}: {row}")
        radii = radii_by_seed.setdefault(seed, set())
        if radius in radii:
            raise ValueError(f"Duplicate radius {radius} for seed {seed} in {mass_path}")
        radii.add(radius)
    for seed, radii in radii_by_seed.items():
        if reference_radii is None:
            reference_radii = radii
        elif radii != reference_radii:
            raise ValueError(
                f"Inconsistent mass-radius grid for seed {seed} in {mass_path}"
            )

    # Cross-check observations against the run manifest. The driver emits
    # mass-radius data and fits only for completed, consistently unwrapped
    # aggregates; reject orphaned or impossible derived data.
    run_by_seed: Dict[int, dict] = {}
    for row in runs:
        seed = as_int(row, "seed", runs_path)
        if seed in run_by_seed:
            raise ValueError(f"Duplicate seed {seed} in {runs_path}")
        completed = as_int(row, "completed", runs_path)
        unwrapped = as_int(row, "unwrapping_consistent", runs_path)
        if completed not in (0, 1) or unwrapped not in (0, 1):
            raise ValueError(f"Boolean fields must be 0 or 1 in {runs_path}: {row}")
        run_by_seed[seed] = row

    for seed in radii_by_seed:
        if seed not in run_by_seed:
            raise ValueError(f"Mass-radius data for unknown seed {seed} in {mass_path}")
        run = run_by_seed[seed]
        if as_int(run, "completed", runs_path) != 1 or \
           as_int(run, "unwrapping_consistent", runs_path) != 1:
            raise ValueError(
                f"Mass-radius data require a completed, consistently unwrapped run "
                f"for seed {seed} in {runs_path}"
            )

    by_seed: Dict[int, dict] = {}
    for row in fit_rows:
        seed = as_int(row, "seed", fits_path)
        lo = as_float(row, "fit_minimum_radius", fits_path)
        hi = as_float(row, "fit_maximum_radius", fits_path)
        if math.isclose(lo, fit_min, rel_tol=1e-10, abs_tol=1e-12) and \
           math.isclose(hi, fit_max, rel_tol=1e-10, abs_tol=1e-12):
            if seed in by_seed:
                raise ValueError(f"Multiple rows for seed {seed} and requested fit window in {fits_path}")
            if seed not in run_by_seed:
                raise ValueError(f"Fit row for unknown seed {seed} in {fits_path}")
            run = run_by_seed[seed]
            if as_int(run, "completed", runs_path) != 1 or \
               as_int(run, "unwrapping_consistent", runs_path) != 1:
                raise ValueError(
                    f"Fit row requires a completed, consistently unwrapped run "
                    f"for seed {seed} in {runs_path}"
                )
            if seed not in radii_by_seed:
                raise ValueError(
                    f"Fit row for seed {seed} has no corresponding mass-radius data in {mass_path}"
                )
            point_count = as_int(row, "point_count", fits_path)
            expected_points = sum(
                1 for radius in radii_by_seed[seed]
                if radius >= fit_min and radius <= fit_max
            )
            if point_count != expected_points:
                raise ValueError(
                    f"Fit point count mismatch for seed {seed}: "
                    f"fit reports {point_count}, mass-radius data contain {expected_points}"
                )
            by_seed[seed] = {
                "df": as_float(row, "exponent", fits_path),
                "fit_r_squared": as_float(row, "r_squared", fits_path),
                "fit_standard_error": as_float(row, "standard_error", fits_path),
                "fit_point_count": point_count,
            }

    output_rows = []
    seen = set()
    for row in runs:
        seed = as_int(row, "seed", runs_path)
        if seed in seen:
            raise ValueError(f"Duplicate seed {seed} in {runs_path}")
        seen.add(seed)
        completed = as_int(row, "completed", runs_path)
        unwrapped = as_int(row, "unwrapping_consistent", runs_path)
        if completed not in (0, 1) or unwrapped not in (0, 1):
            raise ValueError(f"Boolean fields must be 0 or 1 in {runs_path}: {row}")
        largest = as_int(row, "largest_component_size", runs_path)
        if largest < 0 or largest > particle_count:
            raise ValueError(
                f"largest_component_size must lie in [0, {particle_count}] "
                f"in {runs_path}: {row}"
            )
        if completed == 1 and largest != particle_count:
            raise ValueError(
                f"Completed run must contain all {particle_count} particles "
                f"in its largest component in {runs_path}: {row}"
            )
        rg = as_float(row, "largest_component_rg", runs_path, allow_blank=True)
        fit = by_seed.get(seed) if completed == 1 and unwrapped == 1 else None
        output_rows.append({
            "particle_count": particle_count,
            "seed": seed,
            "completed": completed,
            "attempts": as_int(row, "attempts", runs_path),
            "unwrapping_consistent": unwrapped,
            "largest_component_size": largest,
            "largest_component_fraction": largest / particle_count,
            "largest_component_rg": rg,
            "df": fit["df"] if fit else None,
            "fit_r_squared": fit["fit_r_squared"] if fit else None,
            "fit_standard_error": fit["fit_standard_error"] if fit else None,
            "fit_point_count": fit["fit_point_count"] if fit else None,
        })

    n = len(output_rows)
    completed_rows = [r for r in output_rows if r["completed"] == 1]
    unwrapped_rows = [r for r in completed_rows if r["unwrapping_consistent"] == 1]
    valid_fits = [r for r in unwrapped_rows if r["df"] is not None]
    dfs = [r["df"] for r in valid_fits]
    rgs = [r["largest_component_rg"] for r in unwrapped_rows
           if r["largest_component_rg"] is not None]
    fractions = [r["largest_component_fraction"] for r in output_rows]
    summary = {
        "particle_count": particle_count,
        "runs": n,
        "completed_runs": len(completed_rows),
        "unwrapped_completed_runs": len(unwrapped_rows),
        "valid_fit_runs": len(valid_fits),
        "completion_fraction": len(completed_rows) / n if n else None,
        "unwrapped_fraction_of_completed": len(unwrapped_rows) / len(completed_rows)
            if completed_rows else None,
        "valid_fit_fraction_of_unwrapped": len(valid_fits) / len(unwrapped_rows)
            if unwrapped_rows else None,
        "largest_component_fraction_mean": statistics.mean(fractions) if fractions else None,
        "largest_component_rg_mean": statistics.mean(rgs) if rgs else None,
        "largest_component_rg_sd": sample_sd(rgs),
        "df_mean": statistics.mean(dfs) if dfs else None,
        "df_sd": sample_sd(dfs),
        "df_median": statistics.median(dfs) if dfs else None,
        "df_min": min(dfs) if dfs else None,
        "df_max": max(dfs) if dfs else None,
        "fit_minimum_radius": fit_min,
        "fit_maximum_radius": fit_max,
    }
    return output_rows, summary


def parse_system(value: str) -> Tuple[int, Path]:
    if ":" not in value:
        raise argparse.ArgumentTypeError("System must be PARTICLE_COUNT:PREFIX")
    count_text, prefix_text = value.split(":", 1)
    try:
        count = int(count_text)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Particle count must be an integer") from exc
    if count <= 0 or not prefix_text:
        raise argparse.ArgumentTypeError("Particle count and prefix must be positive/non-empty")
    return count, Path(prefix_text)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--system", action="append", type=parse_system, required=True,
                        help="particle count and common output prefix, e.g. 32:results/n32")
    parser.add_argument("--fit-min", type=float, required=True)
    parser.add_argument("--fit-max", type=float, required=True)
    parser.add_argument("--output", type=Path, required=True,
                        help="output prefix for *_per_run.csv and *_summary.csv")
    args = parser.parse_args()
    if not (math.isfinite(args.fit_min) and math.isfinite(args.fit_max)
            and 0 < args.fit_min < args.fit_max):
        parser.error("Fit bounds must be finite, positive, and increasing")

    all_rows: List[dict] = []
    summaries = []
    for count, prefix in args.system:
        rows, summary = load_system(count, prefix, args.fit_min, args.fit_max)
        all_rows.extend(rows)
        summaries.append(summary)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    per_run_fields = [
        "particle_count", "seed", "completed", "attempts", "unwrapping_consistent",
        "largest_component_size", "largest_component_fraction",
        "largest_component_rg", "df", "fit_r_squared",
        "fit_standard_error", "fit_point_count",
    ]
    summary_fields = list(summaries[0].keys()) if summaries else []
    for suffix, rows, fields in (
        ("_per_run.csv", all_rows, per_run_fields),
        ("_summary.csv", summaries, summary_fields),
    ):
        path = Path(str(args.output) + suffix)
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            for row in rows:
                writer.writerow({key: fmt(value) if isinstance(value, float) else
                                 ("" if value is None else value)
                                 for key, value in row.items()})
        print(f"Wrote {path}")
    print("Statistics use independent run seeds; fit-window rows are not pooled.")
    print("The requested fit interval is fixed across all systems.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
