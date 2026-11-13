#!/usr/bin/env python3
"""One-way 1-D pressure diffusion with prescribed time-dependent mobility.

Solves S(x) dp/dt = d/dx(lambda(x,t) dp/dx) on a fixed, double-drained
slab. Storage compliance S is fixed; hydraulic mobility lambda=kappa/mu
may be prescribed at each backward-Euler step. This isolates the effect of
aging permeability without silently changing the conservative storage term.

This is a numerical sensitivity model, not a calibrated silica constitutive
law. It does not model time-dependent modulus, moving boundaries, changing
porosity/storage, or pressure-to-structure feedback.
"""
from __future__ import annotations
import math
from typing import Sequence


def _positive(values: Sequence[float], name: str) -> list[float]:
    out = [float(v) for v in values]
    if not out or any(not math.isfinite(v) or v <= 0.0 for v in out):
        raise ValueError(f"{name} must contain finite positive values")
    return out


def _thomas(lower: list[float], diagonal: list[float],
            upper: list[float], rhs: list[float]) -> list[float]:
    n = len(diagonal)
    b, c, d = diagonal[:], upper[:], rhs[:]
    for i in range(1, n):
        if not math.isfinite(b[i-1]) or abs(b[i-1]) < 1e-300:
            raise ArithmeticError("singular tridiagonal system")
        factor = lower[i] / b[i-1]
        b[i] -= factor*c[i-1]
        d[i] -= factor*d[i-1]
    if not math.isfinite(b[-1]) or abs(b[-1]) < 1e-300:
        raise ArithmeticError("singular tridiagonal system")
    x = [0.0]*n
    x[-1] = d[-1]/b[-1]
    for i in range(n-2, -1, -1):
        x[i] = (d[i]-c[i]*x[i+1])/b[i]
    return x


def solve_1d_time_dependent_mobility(
    storage_compliance_pa_inv: Sequence[float],
    mobility_schedule_m2_pa_s: Sequence[Sequence[float]],
    thickness_m: float,
    dt_s: float,
    initial_pressure_pa: float = 1.0,
    left_boundary_resistance_pa_s_m: float = 0.0,
    right_boundary_resistance_pa_s_m: float = 0.0,
) -> dict[str, list]:
    """Solve using one mobility field per time step (evaluated at t[n+1]).

    The schedule length defines the number of steps. Each mobility field
    must have one positive value per cell. The fixed storage field is
    intentionally not time-dependent in this first extension.

    Boundary resistances are area-specific hydraulic resistances [Pa s/m],
    defined by q = p_boundary / R_b for outward superficial flux q [m/s].
    They are placed in series with the half-cell Darcy resistance. A value
    of zero recovers a perfectly drained p=0 boundary. These are lumped
    external resistances (e.g. membrane/support/cake), not gel permeability.
    """
    storage = _positive(storage_compliance_pa_inv, "storage_compliance_pa_inv")
    if not math.isfinite(thickness_m) or thickness_m <= 0:
        raise ValueError("thickness_m must be finite and > 0")
    if not math.isfinite(dt_s) or dt_s <= 0:
        raise ValueError("dt_s must be finite and > 0")
    if not math.isfinite(initial_pressure_pa) or initial_pressure_pa <= 0:
        raise ValueError("initial_pressure_pa must be finite and > 0")
    if not mobility_schedule_m2_pa_s:
        raise ValueError("mobility schedule must contain at least one step")
    for value, name in ((left_boundary_resistance_pa_s_m, "left_boundary_resistance_pa_s_m"),
                        (right_boundary_resistance_pa_s_m, "right_boundary_resistance_pa_s_m")):
        if not math.isfinite(value) or value < 0.0:
            raise ValueError(f"{name} must be finite and >= 0")

    n = len(storage)
    dx = thickness_m/n
    capacity = [s*dx for s in storage]
    total_capacity = sum(capacity)
    pressure = [initial_pressure_pa]*n
    times = [0.0]
    means = [initial_pressure_pa]
    profiles = [pressure[:]]
    outflows = [0.0]
    residuals = [0.0]

    for step, raw_mobility in enumerate(mobility_schedule_m2_pa_s, start=1):
        mobility = _positive(raw_mobility, f"mobility_schedule[{step-1}]")
        if len(mobility) != n:
            raise ValueError("each mobility field must match the storage grid")
        face_g = [0.0]*(n+1)
        face_g[0] = 1.0 / (dx/(2.0*mobility[0]) + left_boundary_resistance_pa_s_m)
        face_g[n] = 1.0 / (dx/(2.0*mobility[-1]) + right_boundary_resistance_pa_s_m)
        for j in range(1, n):
            left, right = mobility[j-1], mobility[j]
            face_g[j] = (2.0*left*right/(left+right))/dx

        lower, upper, diagonal = [0.0]*n, [0.0]*n, [0.0]*n
        for j in range(n):
            lower[j] = -face_g[j] if j > 0 else 0.0
            upper[j] = -face_g[j+1] if j < n-1 else 0.0
            diagonal[j] = capacity[j]/dt_s + face_g[j]+face_g[j+1]
        old_storage = sum(capacity[j]*pressure[j] for j in range(n))
        rhs = [capacity[j]*pressure[j]/dt_s for j in range(n)]
        pressure = _thomas(lower, diagonal, upper, rhs)
        new_storage = sum(capacity[j]*pressure[j] for j in range(n))
        outflow = face_g[0]*pressure[0]+face_g[n]*pressure[-1]
        residual = new_storage-old_storage+dt_s*outflow
        times.append(step*dt_s)
        means.append(new_storage/total_capacity)
        profiles.append(pressure[:])
        outflows.append(outflow)
        residuals.append(residual)

    return {"times_s": times, "mean_pressure_pa": means,
            "profiles_pa": profiles, "boundary_outflow_m_s": outflows,
            "balance_residual_m": residuals}
