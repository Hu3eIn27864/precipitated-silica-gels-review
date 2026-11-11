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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--executable", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--sizes", type=positive_int, nargs="+", default=[32, 64, 128])
    parser.add_argument("--seed-start", type=positive_int, default=1000)
    parser.add_argument("--seed-count", type=positive_int, default=5)
    parser.add_argument("--max-attempts", type=positive_int, default=200000)
    parser.add_argument("--reference-size", type=positive_int, default=32)
    parser.add_argument("--reference-box", type=float, default=15.0)
    args = parser.parse_args()

    if not math.isfinite(args.reference_box) or args.reference_box <= 2.0:
        parser.error("--reference-box must be finite and greater than 2.0")
    if len(set(args.sizes)) != len(args.sizes):
        parser.error("--sizes must not contain duplicates")
    if not args.executable.is_file():
        parser.error(f"Executable not found: {args.executable}")
    if args.seed_start + args.seed_count - 1 > (2**64 - 1):
        parser.error("Seed range overflows uint64")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    for count in args.sizes:
        box = args.reference_box * (count / args.reference_size) ** (1.0 / 3.0)
        if box <= 2.0:
            parser.error(f"Calculated box length {box} is too small for N={count}")
        prefix = args.output_dir / f"n{count}"
        command = [
            str(args.executable), str(count), f"{box:.17g}",
            str(args.seed_start), str(args.seed_count),
            str(args.max_attempts), str(prefix),
        ]
        print("Running:", " ".join(command), flush=True)
        subprocess.run(command, check=True)
    print("All requested ensembles finished. No physical-time interpretation is implied.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
