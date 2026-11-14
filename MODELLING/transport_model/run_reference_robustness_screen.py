#!/usr/bin/env python3
"""Reproduce a bounded synthetic robustness screen; prints JSON to stdout."""
from __future__ import annotations
import json
from robustness_screening import screen_robustness


def main():
    design = {
        "storage": [1.0, 1.2],
        "mobility": [1.0, 0.65],
        "widths": [0.4, 0.6],
        "contact_resistances": [0.08],
    }
    result = screen_robustness(
        design,
        interface_fraction=0.4,
        interface_offsets=(-0.05, 0.0, 0.05),
        storage_scale_scenarios=((0.9, 1.1), (1.0, 1.0), (1.1, 0.9)),
        mode_scenarios=((0, 1, 2), (0, 2), (0, 1), (1, 2), (1,)),
        n_modes=3,
    )
    # Report the worst-conditioned full-rank scenario separately from
    # rank-deficient scenarios, whose condition number is infinite.
    full_rank = [row for row in result["scenarios"] if row["rank"] == 2]
    worst = max(full_rank, key=lambda row: row["condition_number"])
    result["worst_full_rank_scenario"] = worst
    result["input"] = {
        "design": design,
        "interface_fraction": 0.4,
        "interface_offsets": [-0.05, 0.0, 0.05],
        "storage_scale_scenarios": [[0.9, 1.1], [1.0, 1.0], [1.1, 0.9]],
        "mode_scenarios": [[0, 1, 2], [0, 2], [0, 1], [1, 2], [1]],
        "n_modes": 3,
    }
    print(json.dumps(result, indent=2, sort_keys=True, allow_nan=False))


if __name__ == "__main__":
    main()
