#!/usr/bin/env python3
"""Reconstruct published single-exponential syneresis fit curves from tabulated fit parameters.

These are model reconstructions, NOT digitised experimental markers or raw observations.
Standard library only.
"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INPUTS = (
    ROOT / "LITERATURE" / "experimental_syneresis_comparison.csv",
    ROOT / "LITERATURE" / "pressure_cell_syneresis_comparison.csv",
)
OUTPUT_DEFAULT = ROOT / "LITERATURE" / "derived" / "published_fit_curve_reconstructions.csv"


def curve_value(t_h: float, smax: float, tau_h: float) -> float:
    """Single-exponential empirical fit: S(t) = Smax * (1 - exp(-t/tau))."""
    import math
    if t_h < 0 or smax < 0 or tau_h <= 0:
        raise ValueError("Require t >= 0, Smax >= 0 and tau > 0")
    return smax * (1.0 - math.exp(-t_h / tau_h))


def read_records(paths=INPUTS):
    for path in paths:
        with path.open(newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                try:
                    smax = float(row["Smax"])
                    tau = float(row["tau_h"])
                except (KeyError, TypeError, ValueError):
                    continue
                if smax < 0 or tau <= 0:
                    continue
                yield row, smax, tau


def reconstruct(output: Path, points_per_tau: int = 41, max_tau: float = 5.0):
    if points_per_tau < 2 or max_tau <= 0:
        raise ValueError("points_per_tau must be >= 2 and max_tau > 0")
    output.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "record_id", "source", "gel_type", "experiment_type",
        "temperature_C", "equivalent_pressure_bar", "pressure_bar_low",
        "pressure_bar_high", "time_h", "syneresis_fraction",
        "Smax_fit", "tau_fit_h", "data_kind", "equation",
    ]
    count = 0
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row, smax, tau in read_records():
            for i in range(points_per_tau):
                t = max_tau * tau * i / (points_per_tau - 1)
                writer.writerow({
                    "record_id": row.get("record_id", ""),
                    "source": row.get("source", ""),
                    "gel_type": row.get("gel_type", ""),
                    "experiment_type": row.get("experiment_type", ""),
                    "temperature_C": row.get("temperature_C", ""),
                    "equivalent_pressure_bar": row.get("equivalent_pressure_bar", ""),
                    "pressure_bar_low": row.get("pressure_bar_low", ""),
                    "pressure_bar_high": row.get("pressure_bar_high", ""),
                    "time_h": f"{t:.9g}",
                    "syneresis_fraction": f"{curve_value(t, smax, tau):.9g}",
                    "Smax_fit": f"{smax:.9g}",
                    "tau_fit_h": f"{tau:.9g}",
                    "data_kind": "published_empirical_fit_reconstruction_not_digitised_data",
                    "equation": "S(t)=Smax*(1-exp(-t/tau))",
                })
                count += 1
    return count


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUTPUT_DEFAULT)
    parser.add_argument("--points-per-tau", type=int, default=41)
    parser.add_argument("--max-tau", type=float, default=5.0,
                        help="End time as a multiple of each record's tau")
    args = parser.parse_args()
    n = reconstruct(args.output, args.points_per_tau, args.max_tau)
    print(f"Wrote {n} reconstructed points to {args.output}")
    print("WARNING: reconstructed fit curves only; no raw experimental points were digitised.")


if __name__ == "__main__":
    main()
