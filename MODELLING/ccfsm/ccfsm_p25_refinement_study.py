"""CCFSM P25: bounded time/space and nonlinear-solver refinement study.

The study is a numerical verification harness, not a physical calibration.
It uses a manufactured, spatially varying small reference state and the
existing P19-P24 operators. Results are written as CSV for CI artifacts.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

from ccfsm_p2_chemical_affinity import ChemicalParametersP2
from ccfsm_p8_variable_capacity import P8Grid
from ccfsm_p9_mechanical_feedback import P9Parameters
from ccfsm_p11_energy_time_integration import P11State
from ccfsm_p22_iterated_implicit_coupling import p22_iterated_implicit_step
from ccfsm_p23_discrete_balance import p23_audit_accepted_step
from ccfsm_p24_newton_reference import (
    p24_newton_reference_step, p24_compare_with_p22,
)


def reference_inputs(cells: int):
    if not isinstance(cells, int) or cells < 1:
        raise ValueError("cells must be a positive integer")
    dx = 1.0 / cells
    grid = P8Grid(cells, dx)
    chemistry = ChemicalParametersP2(
        1000.0, 298.15, (0.01, 0.01, 0.01), (1.0, 1.0, 1.0))
    mechanics = P9Parameters(
        2e6, 1e6, 1e7, 0.8, 0.01, 0.2, 1e-12, 0.5, 0.0,
        1e-12, 0.0, 0.0, 0.2, 0.0)
    theta = tuple(0.51 + 0.005*j/max(1, cells-1) for j in range(cells))
    fields = tuple(tuple(base + slope*j/max(1, cells-1)
                         for j in range(cells))
                   for base, slope in ((100.0, 10.0), (80.0, 5.0),
                                       (300.0, 10.0), (100.0, 5.0)))
    state = P11State(theta, fields, 0.0)

    # 1D axial displacement embedded in the 3D P19 Voigt representation.
    # Every transverse DOF and the left axial DOF are fixed; the right axial
    # DOF is free. Each FV cell receives one positive-weight FE quadrature point.
    ndof = 3 * (cells + 1)
    quadrature = []
    for j in range(cells):
        B = [[0.0] * ndof for _ in range(6)]
        B[0][3*j] = -1.0 / dx
        B[0][3*(j+1)] = 1.0 / dx
        quadrature.append({
            "cell_index": j, "B": B, "weight": dx,
            "eigenstrain": 0.0, "fluid_content_increment": 0.0,
        })
    dirichlet = {i: 0.0 for i in range(ndof)
                 if i % 3 in (1, 2) or i == 0}
    return grid, chemistry, mechanics, state, tuple(quadrature), dirichlet


def _flat(state):
    return tuple(state.fluid_capacity) + tuple(
        x for row in state.inventories for x in row)


def _relative_inf(a, b):
    return max((abs(x-y) for x, y in zip(a, b)), default=0.0) / max(
        1e-30, *(abs(x) for x in a), *(abs(x) for x in b))


def _run_step(solver, state, dt, args, **kwargs):
    grid, chemistry, mechanics, quad, dbc = args
    common = (state, dt, grid, mechanics, chemistry, (0.0, 0.0),
              0.0, quad, dbc)
    if solver == "P22":
        return p22_iterated_implicit_step(
            *common, state_tolerance=1e-8, pressure_tolerance=1e-8,
            max_iterations=150, **kwargs)
    return p24_newton_reference_step(
        *common, tolerance=1e-9, max_iterations=30, **kwargs)


def temporal_refinement(cells=2, final_time_s=1e-12):
    base = reference_inputs(cells)
    grid, chemistry, mechanics, state, quad, dbc = base
    args = (grid, chemistry, mechanics, quad, dbc)
    rows = []
    for solver in ("P22", "P24"):
        solutions = []
        for subdivisions in (1, 2, 4):
            dt = final_time_s / subdivisions
            current = state
            iterations = 0
            residual = 0.0
            for _ in range(subdivisions):
                result = _run_step(solver, current, dt, args)
                if not result.get("converged"):
                    rows.append({
                        "solver": solver, "cells": cells,
                        "substeps": subdivisions, "dt_s": dt,
                        "status": result.get("failure", "not_converged"),
                        "iterations": result.get("iterations", 0),
                    })
                    current = None
                    break
                current = result["state"]
                iterations += result["iterations"]
                residual = max(residual, result.get(
                    "scaled_residual_inf",
                    result.get("state_relative_residual", 0.0)))
            if current is not None:
                solutions.append((subdivisions, current, iterations, residual))
        if len(solutions) == 3:
            finest = _flat(solutions[-1][1])
            for subdivisions, solution, iterations, residual in solutions:
                rows.append({
                    "solver": solver, "cells": cells,
                    "substeps": subdivisions,
                    "dt_s": final_time_s / subdivisions,
                    "status": "converged",
                    "relative_error_vs_finest": _relative_inf(_flat(solution), finest),
                    "iterations_total": iterations,
                    "max_solver_residual": residual,
                    "theta_min": min(solution.fluid_capacity),
                    "theta_max": max(solution.fluid_capacity),
                    "inventory_min": min(x for row in solution.inventories for x in row),
                })
    return rows


def spatial_refinement(final_time_s=1e-12):
    rows = []
    for cells in (1, 2, 4):
        grid, chemistry, mechanics, state, quad, dbc = reference_inputs(cells)
        args = (grid, chemistry, mechanics, quad, dbc)
        p22 = _run_step("P22", state, final_time_s, args)
        p24 = _run_step("P24", state, final_time_s, args)
        row = {"cells": cells, "status": "converged" if
               p22.get("converged") and p24.get("converged") else "solver_failure"}
        row["p22_iterations"] = p22.get("iterations")
        row["p24_iterations"] = p24.get("iterations")
        row["p22_residual"] = p22.get("state_relative_residual")
        row["p24_residual"] = p24.get("scaled_residual_inf")
        if row["status"] == "converged":
            comparison = p24_compare_with_p22(p22, p24, grid)
            audit = p23_audit_accepted_step(
                state, p22, grid, mechanics, chemistry)
            row.update({
                "p22_p24_state_relative_difference":
                    comparison["state_relative_difference_inf"],
                "p22_p24_pressure_relative_difference":
                    comparison["projected_pressure_relative_difference_inf"],
                "silicon_balance_relative_residual":
                    audit["silicon_balance_relative_residual"],
                "silicon_balance_verified": audit["silicon_balance_verified"],
                "theta_min": min(p22["state"].fluid_capacity),
                "theta_max": max(p22["state"].fluid_capacity),
                "inventory_min": min(x for r in p22["state"].inventories for x in r),
            })
        rows.append(row)
    return rows


def nonlinear_robustness(cells=2, dt_s=1e-12):
    grid, chemistry, mechanics, state, quad, dbc = reference_inputs(cells)
    args = (grid, chemistry, mechanics, quad, dbc)
    rows = []
    for fd in (1e-4, 1e-6, 1e-8):
        result = _run_step("P24", state, dt_s, args,
                           finite_difference_step=fd)
        rows.append({
            "study": "P24_FD_step", "setting": fd,
            "status": "converged" if result.get("converged") else result.get("failure"),
            "iterations": result.get("iterations"),
            "residual": result.get("scaled_residual_inf"),
            "theta_min": min(result["state"].fluid_capacity)
                        if result.get("converged") else None,
        })
    for relaxation in (0.2, 0.5, 1.0):
        result = _run_step("P22", state, dt_s, args,
                           relaxation=relaxation)
        rows.append({
            "study": "P22_relaxation", "setting": relaxation,
            "status": "converged" if result.get("converged") else result.get("failure"),
            "iterations": result.get("iterations"),
            "residual": result.get("state_relative_residual"),
            "pressure_residual": result.get("pressure_relative_residual"),
            "theta_min": min(result["state"].fluid_capacity)
                        if result.get("converged") else None,
        })
    return rows


def run_study(output_dir):
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    datasets = {
        "temporal_refinement.csv": temporal_refinement(),
        "spatial_refinement.csv": spatial_refinement(),
        "nonlinear_robustness.csv": nonlinear_robustness(),
    }
    for filename, rows in datasets.items():
        if not rows:
            continue
        with (out / filename).open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(dict.fromkeys(
                key for row in rows for key in row)))
            writer.writeheader()
            writer.writerows(rows)
    summary = {
        "scope": "synthetic numerical reference cases; not physical validation",
        "spatial_cells": [1, 2, 4],
        "temporal_substeps": [1, 2, 4],
        "fd_steps": [1e-4, 1e-6, 1e-8],
        "picard_relaxations": [0.2, 0.5, 1.0],
        "datasets": {name: len(rows) for name, rows in datasets.items()},
        "all_reported_rows": datasets,
    }
    (out / "summary.json").write_text(
        json.dumps(summary, indent=2, allow_nan=False), encoding="utf-8")
    return summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="ccfsm-p25-results")
    args = parser.parse_args()
    summary = run_study(args.output_dir)
    print(json.dumps(summary, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
