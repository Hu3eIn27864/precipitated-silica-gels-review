#!/usr/bin/env python3
"""Run a bounded, paired-seed, one-factor-at-a-time DLCA sensitivity matrix."""
from __future__ import annotations

import argparse
import csv
import math
import subprocess
import sys
from pathlib import Path

VARIANTS = (
    ("baseline", 1.0, 0.2, 1.0),
    ("contact_0p9", 0.9, 0.2, 1.0),
    ("contact_1p1", 1.1, 0.2, 1.0),
    ("step_0p1", 1.0, 0.1, 1.0),
    ("step_0p28", 1.0, 0.28, 1.0),
    ("mobility_0p5", 1.0, 0.2, 0.5),
    ("mobility_1p5", 1.0, 0.2, 1.5),
)


def validate_variant(contact: float, step: float, mobility: float) -> None:
    values = (contact, step, mobility)
    if not all(math.isfinite(x) for x in values):
        raise ValueError("all parameters must be finite")
    if contact <= 0 or step <= 0 or mobility < 0:
        raise ValueError("contact and step must be > 0; mobility must be >= 0")
    if step * math.sqrt(3.0) > 0.5 * contact:
        raise ValueError("step violates the conservative swept-contact bound")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--executable", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--seed-start", type=int, default=3000)
    parser.add_argument("--seed-count", type=int, default=3)
    parser.add_argument("--max-attempts", type=int, default=50000)
    parser.add_argument("--particle-count", type=int, default=32)
    parser.add_argument("--reference-box", type=float, default=15.0)
    args = parser.parse_args()

    if not args.executable.is_file():
        parser.error(f"Executable not found: {args.executable}")
    if args.seed_start < 0 or args.seed_count <= 0 or args.max_attempts <= 0:
        parser.error("seed start must be >= 0; seed count and attempts must be > 0")
    if args.particle_count <= 0 or not math.isfinite(args.reference_box) or args.reference_box <= 0:
        parser.error("particle count and reference box must be positive")

    runner = Path(__file__).with_name("run_dlca_size_series.py")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    manifest = args.output_dir / "parameter_manifest.csv"
    with manifest.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["variant", "particle_count", "box_length", "seed_start",
                         "seed_count", "maximum_attempts", "contact_distance",
                         "maximum_component_step", "mobility_exponent"])
        for name, contact, step, mobility in VARIANTS:
            validate_variant(contact, step, mobility)
            box = args.reference_box
            if box <= 2.0 * contact:
                parser.error(f"box length too small for {name}")
            output = args.output_dir / name
            command = [
                sys.executable, str(runner),
                "--executable", str(args.executable.resolve()),
                "--output-dir", str(output.resolve()),
                "--sizes", str(args.particle_count),
                "--seed-start", str(args.seed_start),
                "--seed-count", str(args.seed_count),
                "--max-attempts", str(args.max_attempts),
                "--reference-size", str(args.particle_count),
                "--reference-box", str(args.reference_box),
                "--contact-distance", str(contact),
                "--maximum-component-step", str(step),
                "--mobility-exponent", str(mobility),
            ]
            print(f"Variant {name}: {' '.join(command)}", flush=True)
            subprocess.run(command, check=True)
            writer.writerow([name, args.particle_count, box, args.seed_start,
                             args.seed_count, args.max_attempts, contact, step, mobility])
            handle.flush()
    print(f"Completed requested matrix; manifest: {manifest}")
    print("No physical-time or silica-calibration interpretation is implied.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
