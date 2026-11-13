#!/usr/bin/env python3
"""Finite-volume 1-D pore-pressure diffusion with heterogeneous coefficients.

PDE: S(x) dp/dt = d/dx(lambda(x) dp/dx) + f(x,t).
S is storage compliance [1/Pa], lambda is hydraulic mobility
[m^2/(Pa s)], and f has units 1/time. Cell-centred coefficients
are fixed in time; backward Euler and harmonic face mobility are used.
"""
from __future__ import annotations
import math
from typing import Callable, Optional, Sequence


def _validate_positive_array(values: Sequence[float], name: str) -> list[float]:
    result = [float(value) for value in values]
    if not result:
        raise ValueError(f"{name} must not be empty")
    if any(not math.isfinite(value) or value <= 0.0 for value in result):
        raise ValueError(f"{name} values must be finite and > 0")
    return result


def _solve_tridiagonal(lower: list[float], diagonal: list[float],
                       upper: list[float], rhs: list[float]) -> list[float]:
    """Solve a tridiagonal system with the Thomas algorithm."""
    n = len(diagonal)
    if not (len(lower) == len(upper) == len(rhs) == n):
        raise ValueError("tridiagonal arrays must have equal lengths")
    c, d, b = upper[:], rhs[:], diagonal[:]
    for i in range(1, n):
        if not math.isfinite(b[i - 1]) or abs(b[i - 1]) < 1e-300:
            raise ArithmeticError("singular tridiagonal system")
        factor = lower[i] / b[i - 1]
        b[i] -= factor * c[i - 1]
        d[i] -= factor * d[i - 1]
    if not math.isfinite(b[-1]) or abs(b[-1]) < 1e-300:
        raise ArithmeticError("singular tridiagonal system")
    result = [0.0] * n
    result[-1] = d[-1] / b[-1]
    for i in range(n - 2, -1, -1):
        result[i] = (d[i] - c[i] * result[i + 1]) / b[i]
    return result


def solve_1d_pressure_diffusion(
    storage_compliance_pa_inv: Sequence[float],
    mobility_m2_pa_s: Sequence[float],
    thickness_m: float,
    dt_s: float,
    n_steps: int,
    initial_pressure_pa: float = 1.0,
    *,
    initial_pressure_profile_pa: Optional[Sequence[float]] = None,
    source_term_s_inv: Optional[Callable[[float, float], float]] = None,
) -> dict[str, list]:
    """Solve a double-drained slab with optional manufactured forcing.

    ``source_term_s_inv(x, t)`` returns f in
    S(x)*dp/dt = d/dx(lambda(x)*dp/dx) + f(x,t), evaluated at cell centres
    and the new time level (backward Euler). ``initial_pressure_profile_pa``
    overrides the uniform initial pressure and must contain one value/cell.
    Returned mean pressure is storage weighted; boundary outflow is the sum
    of outward Darcy fluxes [m/s].
    """
    storage = _validate_positive_array(storage_compliance_pa_inv, "storage_compliance_pa_inv")
    mobility = _validate_positive_array(mobility_m2_pa_s, "mobility_m2_pa_s")
    if len(storage) != len(mobility):
        raise ValueError("storage and mobility arrays must have equal lengths")
    if not math.isfinite(thickness_m) or thickness_m <= 0.0:
        raise ValueError("thickness_m must be finite and > 0")
    if not math.isfinite(dt_s) or dt_s <= 0.0:
        raise ValueError("dt_s must be finite and > 0")
    if not isinstance(n_steps, int) or n_steps < 1:
        raise ValueError("n_steps must be an integer >= 1")
    if not math.isfinite(initial_pressure_pa) or initial_pressure_pa <= 0.0:
        raise ValueError("initial_pressure_pa must be finite and > 0")

    n = len(storage)
    dx = thickness_m / n
    x_centres = [(i + 0.5) * dx for i in range(n)]
    if initial_pressure_profile_pa is None:
        pressure = [initial_pressure_pa] * n
    else:
        pressure = [float(v) for v in initial_pressure_profile_pa]
        if len(pressure) != n or any(not math.isfinite(v) for v in pressure):
            raise ValueError("initial pressure profile must have n finite values")

    capacity = [s * dx for s in storage]
    face_g = [0.0] * (n + 1)
    face_g[0] = 2.0 * mobility[0] / dx
    face_g[n] = 2.0 * mobility[-1] / dx
    for face in range(1, n):
        left, right = mobility[face - 1], mobility[face]
        face_g[face] = (2.0 * left * right / (left + right)) / dx

    lower, upper, diagonal = [0.0]*n, [0.0]*n, [0.0]*n
    for i in range(n):
        lower[i] = -face_g[i] if i > 0 else 0.0
        upper[i] = -face_g[i + 1] if i < n - 1 else 0.0
        diagonal[i] = capacity[i] / dt_s + face_g[i] + face_g[i + 1]

    times = [0.0]
    mean_pressure = [sum(capacity[i]*pressure[i] for i in range(n))/sum(capacity)]
    profiles, boundary_flux, balance_residual = [pressure[:]], [0.0], [0.0]
    total_capacity = sum(capacity)

    for step in range(1, n_steps + 1):
        old_storage = sum(capacity[i] * pressure[i] for i in range(n))
        t_new = step * dt_s
        rhs = [capacity[i] * pressure[i] / dt_s for i in range(n)]
        source_values = []
        if source_term_s_inv is not None:
            for x in x_centres:
                source = float(source_term_s_inv(x, t_new))
                if not math.isfinite(source):
                    raise ValueError("source term must return finite values")
                source_values.append(source)
            for i, source in enumerate(source_values):
                rhs[i] += dx * source
        pressure = _solve_tridiagonal(lower, diagonal, upper, rhs)
        outflow = face_g[0] * pressure[0] + face_g[n] * pressure[-1]
        new_storage = sum(capacity[i] * pressure[i] for i in range(n))
        source_integral = dx * sum(source_values)
        residual = (new_storage - old_storage) + dt_s * outflow - dt_s * source_integral
        times.append(t_new)
        mean_pressure.append(new_storage / total_capacity)
        profiles.append(pressure[:])
        boundary_flux.append(outflow)
        balance_residual.append(residual)

    return {"times_s": times, "mean_pressure_pa": mean_pressure,
            "profiles_pa": profiles, "boundary_outflow_m_s": boundary_flux,
            "balance_residual_m": balance_residual}


if __name__ == "__main__":
    import argparse
    import csv
    from pathlib import Path
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-cells", type=int, default=100)
    parser.add_argument("--thickness-m", type=float, required=True)
    parser.add_argument("--storage-compliance", type=float, required=True)
    parser.add_argument("--mobility", type=float, required=True)
    parser.add_argument("--dt-s", type=float, required=True)
    parser.add_argument("--n-steps", type=int, required=True)
    parser.add_argument("--output", type=Path, default=Path("heterogeneous_1d.csv"))
    args = parser.parse_args()
    if args.n_cells < 2:
        parser.error("--n-cells must be >= 2")
    result = solve_1d_pressure_diffusion(
        [args.storage_compliance]*args.n_cells, [args.mobility]*args.n_cells,
        args.thickness_m, args.dt_s, args.n_steps)
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["time_s", "mean_pressure_pa", "degree_consolidation",
                         "boundary_outflow_m_s", "balance_residual_m"])
        for t, p, q, r in zip(result["times_s"], result["mean_pressure_pa"],
                              result["boundary_outflow_m_s"], result["balance_residual_m"]):
            writer.writerow([t, p, 1.0-p, q, r])
    print(f"Wrote {len(result['times_s'])} rows to {args.output}")
    print("Fixed-coefficient heterogeneous Darcy-storage slab; no material calibration.")
