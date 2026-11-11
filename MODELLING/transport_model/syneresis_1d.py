#!/usr/bin/env python3
"""Minimal 1-D pore-pressure diffusion benchmark for syneresis-like consolidation.

This is a linear, constant-coefficient Terzaghi-type slab model, NOT a
chemically specific silica-gel model. It assumes a homogeneous slab drained
at both faces, constant consolidation diffusivity cv, and a prescribed
ultimate shrinkage S_inf. It is intended for code verification and bounded
sensitivity studies before fitting any silica data.

No third-party packages are required.
"""
from __future__ import annotations
import argparse
import csv
import math
from pathlib import Path

def average_degree_of_consolidation(time_s: float, cv_m2_s: float,
                                    drainage_length_m: float,
                                    terms: int = 1000) -> float:
    """Average 1-D degree of consolidation for a double-drained slab."""
    if time_s < 0:
        raise ValueError("time_s must be >= 0")
    if cv_m2_s <= 0 or drainage_length_m <= 0:
        raise ValueError("cv_m2_s and drainage_length_m must be > 0")
    if terms < 1:
        raise ValueError("terms must be >= 1")
    if time_s == 0:
        return 0.0
    factor = 4.0 * cv_m2_s * time_s / (math.pi ** 2 * drainage_length_m ** 2)
    remaining = 0.0
    for m in range(terms):
        odd = 2 * m + 1
        remaining += math.exp(-(odd ** 2) * factor) / (odd ** 2)
    return min(1.0, max(0.0, 1.0 - (8.0 / math.pi ** 2) * remaining))

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cv", type=float, required=True, help="cv [m^2/s]")
    parser.add_argument("--drainage-length", type=float, required=True,
                        help="Maximum drainage path [m]")
    parser.add_argument("--ultimate-shrinkage", type=float, default=0.20)
    parser.add_argument("--t-end-hours", type=float, default=72.0)
    parser.add_argument("--npoints", type=int, default=201)
    parser.add_argument("--terms", type=int, default=1000)
    parser.add_argument("--output", type=Path, default=Path("syneresis_1d.csv"))
    args = parser.parse_args()
    if not 0.0 <= args.ultimate_shrinkage <= 1.0:
        parser.error("--ultimate-shrinkage must lie between 0 and 1")
    if args.t_end_hours <= 0 or args.npoints < 2:
        parser.error("--t-end-hours must be > 0 and --npoints >= 2")
    t_end_s = args.t_end_hours * 3600.0
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["time_s", "time_h", "degree_consolidation",
                         "relative_volume_decrease"])
        for i in range(args.npoints):
            t_s = t_end_s * i / (args.npoints - 1)
            degree = average_degree_of_consolidation(
                t_s, args.cv, args.drainage_length, args.terms)
            writer.writerow([f"{t_s:.9g}", f"{t_s/3600.0:.9g}",
                             f"{degree:.9g}",
                             f"{args.ultimate_shrinkage*degree:.9g}"])
    print(f"Wrote {args.npoints} rows to {args.output}")
    print("Linear 1-D double-drained slab; constant cv.")
    print("Fitted cv is not a uniquely measured permeability or modulus.")

if __name__ == "__main__":
    main()
