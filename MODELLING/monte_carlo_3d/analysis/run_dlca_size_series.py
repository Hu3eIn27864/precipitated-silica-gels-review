#!/usr/bin/env python3
"""Run DLCA ensembles at fixed reduced number density for a size series.

The reference box is scaled as L(N) = L_ref * (N/N_ref)^(1/3).
This preserves initial number density, not a validated experimental volume fraction.
"""
from __future__ import annotations

import argparse
import math
import subprocess
from pathlib import Path


def positive_int(value: str) -> int:
    parsed = int(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("value must be a positive integer")
    return parsed


def nonnegative_int(value: str) -> int:
    parsed = int(value)
    if parsed < 0:
        raise argparse.ArgumentTypeError("value must be a non-negative integer")
    return parsed


def validate_target_q(value: float) -> None:
    if not math.isfinite(value) or value < 0.0:
        raise ValueError("target Q must be finite and >= 0")


def scaled_box_length(particle_count: int, reference_size: int,
                      reference_box: float) -> float:
    return reference_box * (particle_count / reference_size) ** (1.0 / 3.0)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--executable", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--sizes", type=positive_int, nargs="+", default=[32, 64, 128])
    parser.add_argument("--seed-start", type=nonnegative_int, default=1000)
    parser.add_argument("--seed-count", type=positive_int, default=5)
    parser.add_argument("--max-attempts", type=positive_int, default=200000)
    parser.add_argument("--reference-size", type=positive_int, default=32)
    parser.add_argument("--reference-box", type=float, default=15.0)
    parser.add_argument("--contact-distance", type=float, default=1.0)
    parser.add_argument("--maximum-component-step", type=float, default=0.2)
    parser.add_argument("--mobility-exponent", type=float, default=1.0)
    parser.add_argument("--target-q", type=float, default=0.0,
                        help="optional cumulative squared realized-translation target; 0 disables it")
    args = parser.parse_args()

    if not math.isfinite(args.reference_box) or args.reference_box <= 2.0:
        parser.error("--reference-box must be finite and greater than 2.0")
    if not math.isfinite(args.contact_distance) or args.contact_distance <= 0.0:
        parser.error("--contact-distance must be finite and > 0")
    if not math.isfinite(args.maximum_component_step) or args.maximum_component_step <= 0.0:
        parser.error("--maximum-component-step must be finite and > 0")
    if not math.isfinite(args.mobility_exponent) or args.mobility_exponent < 0.0:
        parser.error("--mobility-exponent must be finite and >= 0")
    try:
        validate_target_q(args.target_q)
    except ValueError as exc:
        parser.error(str(exc))
    if args.maximum_component_step * math.sqrt(3.0) > 0.5 * args.contact_distance:
        parser.error("maximum component step violates the DLCA contact-detection bound")
    if len(set(args.sizes)) != len(args.sizes):
        parser.error("--sizes must not contain duplicates")
    if not args.executable.is_file():
        parser.error(f"Executable not found: {args.executable}")
    total_seeds = args.seed_count * len(args.sizes)
    if total_seeds > 0 and args.seed_start + total_seeds - 1 > (2**64 - 1):
        parser.error("Combined seed range overflows uint64")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    for size_index, count in enumerate(args.sizes):
        system_seed_start = args.seed_start + size_index * args.seed_count
        box = scaled_box_length(count, args.reference_size, args.reference_box)
        if box <= 2.0 * args.contact_distance:
            parser.error(f"Calculated box length {box} is too small for the contact distance at N={count}")
        prefix = args.output_dir / f"n{count}"
        command = [
            str(args.executable), str(count), f"{box:.17g}",
            str(system_seed_start), str(args.seed_count),
            str(args.max_attempts), str(prefix), str(args.contact_distance),
            str(args.maximum_component_step), str(args.mobility_exponent),
        ]
        if args.target_q > 0.0:
            command.append(str(args.target_q))
        print("Running:", " ".join(command), flush=True)
        subprocess.run(command, check=True)
    print("All requested ensembles finished. No physical-time interpretation is implied.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
