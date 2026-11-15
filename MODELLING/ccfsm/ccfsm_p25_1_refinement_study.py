"""CCFSM P25.1: conservative cross-mesh refinement and gradient stress tests.

Coarse/fine FV states are compared only after exact-volume cell-average
restriction on nested uniform meshes. This restriction preserves the domain
integral of every FV field. P19 pressure is compared by the same volume
averaging, but is not treated as a conserved inventory. Synthetic reference
study only; not a physical calibration or validation.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

from ccfsm_p11_energy_time_integration import P11State
from ccfsm_p22_iterated_implicit_coupling import p22_iterated_implicit_step
from ccfsm_p23_discrete_balance import p23_audit_accepted_step
from ccfsm_p24_newton_reference import (
    p24_newton_reference_step, p24_compare_with_p22,
)
from ccfsm_p25_refinement_study import reference_inputs


EXTERNAL_PRESSURE_PA = 1.0e5
FINAL_TIME_S = 1.0e-2


def consistent_reference_inputs(cells: int):
    """Build cell-average samples from one mesh-independent linear profile."""
    grid, chemistry, mechanics, _, quad, dbc = reference_inputs(cells)
    x = tuple((j + 0.5) / cells for j in range(cells))
    theta = tuple(0.50 + 0.04 * xi for xi in x)
    fields = tuple(tuple(base + slope * xi for xi in x)
                   for base, slope in ((100.0, 80.0), (80.0, 40.0),
                                       (300.0, 30.0), (100.0, 20.0)))
    state = P11State(theta, fields, 0.0)
    return grid, chemistry, mechanics, state, quad, dbc


def restrict_cell_averages(values, coarse_cells: int):
    """Conservative restriction from a nested uniform fine mesh.

    Fine cell averages are grouped into equal-volume blocks. The returned
    coarse averages preserve the integral exactly up to floating arithmetic.
    """
    values = tuple(float(v) for v in values)
    fine_cells = len(values)
    if not isinstance(coarse_cells, int) or coarse_cells < 1:
        raise ValueError("coarse_cells must be a positive integer")
    if fine_cells < coarse_cells or fine_cells % coarse_cells:
        raise ValueError("fine mesh must be an integer refinement of coarse mesh")
    ratio = fine_cells // coarse_cells
    return tuple(sum(values[i * ratio:(i + 1) * ratio]) / ratio
                 for i in range(coarse_cells))


def restrict_state(fine_state, coarse_cells: int):
    theta = restrict_cell_averages(fine_state.fluid_capacity, coarse_cells)
    fields = tuple(restrict_cell_averages(row, coarse_cells)
                   for row in fine_state.inventories)
    return theta, fields


def _flat(theta, fields):
    return tuple(theta) + tuple(v for row in fields for v in row)


def _norms(coarse, fine_restricted, dx):
    errors = [a - b for a, b in zip(coarse, fine_restricted)]
    linf = max((abs(v) for v in errors), default=0.0)
    l1 = dx * sum(abs(v) for v in errors)
    l2 = math.sqrt(dx * sum(v * v for v in errors))
    scale = max(1e-30, max((abs(v) for v in coarse), default=0.0),
                max((abs(v) for v in fine_restricted), default=0.0))
    return {
        "absolute_linf": linf,
        "relative_linf": linf / scale,
        "absolute_l1": l1,
        "relative_l1": l1 / max(1e-30, dx * sum(abs(v) for v in fine_restricted)),
        "absolute_l2": l2,
        "relative_l2": l2 / max(1e-30, math.sqrt(
            dx * sum(v * v for v in fine_restricted))),
    }


def _solve(solver, state, dt, inputs, **kwargs):
    grid, chemistry, mechanics, _initial_state, quad, dbc = inputs
    common = (state, dt, grid, mechanics, chemistry, (0.0, 0.0),
              EXTERNAL_PRESSURE_PA, quad, dbc)
    if solver == "P22":
        return p22_iterated_implicit_step(
            *common, state_tolerance=1e-11, pressure_tolerance=1e-11,
            max_iterations=180, **kwargs)
    return p24_newton_reference_step(
        *common, tolerance=1e-9, max_iterations=35, **kwargs)


def _advance(solver, inputs, steps, final_time_s=FINAL_TIME_S):
    grid, chemistry, mechanics, initial, quad, dbc = inputs
    state = initial
    iterations = 0
    max_residual = 0.0
    for _ in range(steps):
        result = _solve(solver, state, final_time_s / steps, inputs)
        if not result.get("converged"):
            return {"converged": False, "failure": result.get("failure"),
                    "iterations": result.get("iterations", 0)}
        state = result["state"]
        iterations += result["iterations"]
        residual = result.get("scaled_residual_inf",
                              result.get("state_relative_residual", 0.0))
        max_residual = max(max_residual, residual)
    return {"converged": True, "state": state, "iterations": iterations,
            "max_residual": max_residual, "last_result": result}


def temporal_refinement(cells=4, final_time_s=FINAL_TIME_S):
    inputs = consistent_reference_inputs(cells)
    rows = []
    for solver in ("P22", "P24"):
        solutions = []
        for steps in (1, 2, 4, 8, 16):
            result = _advance(solver, inputs, steps, final_time_s)
            if result["converged"]:
                solutions.append((steps, result))
            else:
                rows.append({"solver": solver, "steps": steps,
                             "status": result["failure"],
                             "iterations": result["iterations"]})
        if len(solutions) == 5:
            reference = _flat(solutions[-1][1]["state"].fluid_capacity,
                              solutions[-1][1]["state"].inventories)
            errors = []
            for steps, result in solutions:
                vector = _flat(result["state"].fluid_capacity,
                               result["state"].inventories)
                e = max(abs(a-b) for a, b in zip(vector, reference)) / max(
                    1e-30, max(abs(v) for v in reference))
                errors.append(e)
                rows.append({
                    "solver": solver, "steps": steps,
                    "dt_s": final_time_s / steps, "status": "converged",
                    "relative_linf_vs_16_steps": e,
                    "iterations_total": result["iterations"],
                    "max_solver_residual": result["max_residual"],
                    "theta_min": min(result["state"].fluid_capacity),
                    "theta_max": max(result["state"].fluid_capacity),
                    "inventory_min": min(v for row in result["state"].inventories
                                         for v in row),
                })
            for i in range(3):
                e_coarse, e_fine = errors[i], errors[i+1]
                rows[-5+i]["observed_pairwise_rate"] = (
                    math.log(e_coarse/e_fine, 2)
                    if e_coarse > 0 and e_fine > 0 else None)
    return rows


def spatial_refinement(final_time_s=FINAL_TIME_S):
    meshes = (1, 2, 4, 8)
    rows = []
    for solver in ("P22", "P24"):
        solutions = {}
        for cells in meshes:
            inputs = consistent_reference_inputs(cells)
            result = _advance(solver, inputs, 1, final_time_s)
            if result["converged"]:
                solutions[cells] = (inputs, result)
            else:
                rows.append({"solver": solver, "cells": cells,
                             "status": result["failure"],
                             "iterations": result["iterations"]})
        if 8 not in solutions:
            continue
        fine_inputs, fine_result = solutions[8]
        fine_state = fine_result["state"]
        fine_theta, fine_fields = fine_state.fluid_capacity, fine_state.inventories
        fine_pressure = fine_result["last_result"]["last_snapshot"][
            "projected_spatial_pressure_cell_pa"]
        errors = []
        for cells in meshes:
            if cells not in solutions:
                continue
            inputs, result = solutions[cells]
            state = result["state"]
            coarse_theta, coarse_fields = state.fluid_capacity, state.inventories
            restricted_theta, restricted_fields = restrict_state(fine_state, cells)
            state_error = _norms(
                _flat(coarse_theta, coarse_fields),
                _flat(restricted_theta, restricted_fields), 1.0/cells)
            pressure = result["last_result"]["last_snapshot"][
                "projected_spatial_pressure_cell_pa"]
            pressure_reference = restrict_cell_averages(fine_pressure, cells)
            pressure_error = _norms(pressure, pressure_reference, 1.0/cells)
            audit = p23_audit_accepted_step(
                inputs[3], result["last_result"], inputs[0],
                inputs[2], inputs[1])
            comparison = None
            if result["last_result"].get("converged"):
                # P22/P24 comparison is separately measured on each identical mesh.
                if solver == "P22":
                    pass
            pressure_span = max(pressure) - min(pressure)
            darcy = result["last_result"]["last_snapshot"]["transport_rhs"][
                "darcy_flux_faces_m_s"]
            row = {
                "solver": solver, "cells": cells, "dx_m": 1.0/cells,
                "status": "converged",
                "state_relative_linf_vs_8": state_error["relative_linf"],
                "state_relative_l2_vs_8": state_error["relative_l2"],
                "state_relative_l1_vs_8": state_error["relative_l1"],
                "pressure_relative_linf_vs_8": pressure_error["relative_linf"],
                "pressure_relative_l2_vs_8": pressure_error["relative_l2"],
                "silicon_balance_relative_residual":
                    audit["silicon_balance_relative_residual"],
                "silicon_balance_verified": audit["silicon_balance_verified"],
                "pressure_span_pa": pressure_span,
                "max_abs_darcy_flux_m_s": max(abs(v) for v in darcy),
                "iterations_total": result["iterations"],
                "max_solver_residual": result["max_residual"],
                "theta_min": min(coarse_theta), "theta_max": max(coarse_theta),
                "inventory_min": min(v for row in coarse_fields for v in row),
            }
            if cells >= 2 and (pressure_span <= 0.0 or
                               max(abs(v) for v in darcy) <= 0.0):
                raise RuntimeError("P25.1 pressure/Darcy gradient stress case was not activated")
            rows.append(row)
            errors.append((cells, state_error["relative_l2"],
                           pressure_error["relative_l2"]))
        for i in range(len(errors)-1):
            n0, e0, p0 = errors[i]
            n1, e1, p1 = errors[i+1]
            row = next(r for r in rows if r.get("solver") == solver
                       and r.get("cells") == n0)
            row["state_pairwise_rate"] = (
                math.log(e0/e1, 2) if e0 > 0 and e1 > 0 else None)
            row["pressure_pairwise_rate"] = (
                math.log(p0/p1, 2) if p0 > 0 and p1 > 0 else None)
    # Cross-solver agreement on the same fine mesh is an independent diagnostic.
    if 8 in solutions:
        pass
    return rows


def solver_agreement(final_time_s=FINAL_TIME_S):
    rows = []
    for cells in (1, 2, 4, 8):
        inputs = consistent_reference_inputs(cells)
        p22 = _advance("P22", inputs, 1, final_time_s)
        p24 = _advance("P24", inputs, 1, final_time_s)
        row = {"cells": cells, "status": "converged" if
               p22["converged"] and p24["converged"] else "solver_failure"}
        if row["status"] == "converged":
            cmp = p24_compare_with_p22(p22["last_result"],
                                       p24["last_result"], inputs[0])
            row.update({
                "state_relative_difference": cmp["state_relative_difference_inf"],
                "pressure_relative_difference":
                    cmp["projected_pressure_relative_difference_inf"],
                "p22_iterations": p22["iterations"],
                "p24_iterations": p24["iterations"],
            })
        rows.append(row)
    return rows


def run_study(output_dir):
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    datasets = {
        "temporal_refinement.csv": temporal_refinement(),
        "spatial_crossmesh_refinement.csv": spatial_refinement(),
        "same_mesh_solver_agreement.csv": solver_agreement(),
    }
    for filename, data in datasets.items():
        if data:
            with (out / filename).open("w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=list(dict.fromkeys(
                    key for row in data for key in row)))
                writer.writeheader()
                writer.writerows(data)
    summary = {
        "scope": "synthetic numerical verification; not physical validation",
        "final_time_s": FINAL_TIME_S,
        "external_pressure_pa": EXTERNAL_PRESSURE_PA,
        "spatial_meshes": [1, 2, 4, 8],
        "temporal_steps": [1, 2, 4, 8, 16],
        "restriction": "nested uniform finite-volume cell-average restriction",
        "datasets": {name: len(data) for name, data in datasets.items()},
        "all_reported_rows": datasets,
    }
    (out / "summary.json").write_text(
        json.dumps(summary, indent=2, allow_nan=False), encoding="utf-8")
    print(json.dumps(summary, indent=2, allow_nan=False))
    return summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="ccfsm-p25-1-results")
    run_study(parser.parse_args().output_dir)


if __name__ == "__main__":
    main()
