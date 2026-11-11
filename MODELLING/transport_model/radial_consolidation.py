"""Finite-volume radial diffusion/consolidation benchmarks.

Dimensionless equation: du/dFo = x**(1-d) d/dx(x**(d-1) du/dx),
where Fo = c_v*t/R**2 and d is 2 (infinite cylinder) or 3 (sphere).
The centre is symmetric (zero flux); the outer surface is perfectly drained
(u=0). This is a linear constant-coefficient benchmark, not a silica-specific
constitutive model.
"""
from __future__ import annotations

import math

_CYLINDER_J0_ROOTS = (
    2.404825557695773, 5.520078110286311, 8.653727912911013,
    11.791534439014281, 14.930917708487787, 18.071063967910924,
    21.21163662987926, 24.352471530749302, 27.493479132040254,
    30.634606468431976,
)


def analytical_radial_average(geometry: str, fourier_number: float,
                              terms: int = 10) -> float:
    """Volume-averaged u/u0 from the radial eigenfunction series."""
    try:
        fo = float(fourier_number)
    except (TypeError, ValueError) as exc:
        raise ValueError("fourier_number must be finite and >= 0") from exc
    if not math.isfinite(fo) or fo < 0.0:
        raise ValueError("fourier_number must be finite and >= 0")
    if not isinstance(terms, int) or terms < 1:
        raise ValueError("terms must be a positive integer")
    if geometry not in ("cylinder", "sphere"):
        raise ValueError("geometry must be 'cylinder' or 'sphere'")
    if fo == 0.0:
        return 1.0
    if geometry == "cylinder":
        if terms > len(_CYLINDER_J0_ROOTS):
            raise ValueError(f"terms must be <= {len(_CYLINDER_J0_ROOTS)} for cylinder")
        return sum(4.0 / (root * root) * math.exp(-root * root * fo)
                   for root in _CYLINDER_J0_ROOTS[:terms])
    return sum(6.0 / (n * n * math.pi * math.pi)
               * math.exp(-n * n * math.pi * math.pi * fo)
               for n in range(1, terms + 1))


def _thomas_solve(lower: list[float], diagonal: list[float],
                  upper: list[float], rhs: list[float]) -> list[float]:
    """Solve a tridiagonal system; arrays have equal length."""
    n = len(diagonal)
    c_prime = [0.0] * n
    d_prime = [0.0] * n
    c_prime[0] = upper[0] / diagonal[0] if n > 1 else 0.0
    d_prime[0] = rhs[0] / diagonal[0]
    for i in range(1, n):
        pivot = diagonal[i] - lower[i] * c_prime[i - 1]
        if pivot <= 0.0 or not math.isfinite(pivot):
            raise ArithmeticError("non-positive pivot in radial diffusion solve")
        c_prime[i] = upper[i] / pivot if i < n - 1 else 0.0
        d_prime[i] = (rhs[i] - lower[i] * d_prime[i - 1]) / pivot
    solution = [0.0] * n
    solution[-1] = d_prime[-1]
    for i in range(n - 2, -1, -1):
        solution[i] = d_prime[i] - c_prime[i] * solution[i + 1]
    return solution


def solve_radial_average(geometry: str, fourier_times: list[float],
                         n_cells: int = 100,
                         max_fourier_step: float = 0.01) -> list[float]:
    """Solve for volume-averaged excess pressure ratio at requested Fo values.

    Uses cell-centred conservative finite volumes and backward Euler. Times
    must be nonnegative, finite and nondecreasing. Returns u_bar/u0 at each
    requested time; degree of consolidation is 1 - this value.
    """
    dimensions = {"cylinder": 2, "sphere": 3}
    if geometry not in dimensions:
        raise ValueError("geometry must be 'cylinder' or 'sphere'")
    if not isinstance(n_cells, int) or n_cells < 3:
        raise ValueError("n_cells must be an integer >= 3")
    try:
        dt_max = float(max_fourier_step)
        times = [float(value) for value in fourier_times]
    except (TypeError, ValueError) as exc:
        raise ValueError("times and max_fourier_step must be numeric") from exc
    if not math.isfinite(dt_max) or dt_max <= 0.0:
        raise ValueError("max_fourier_step must be finite and > 0")
    if any(not math.isfinite(t) or t < 0.0 for t in times):
        raise ValueError("Fourier times must be finite and >= 0")
    if any(times[i] < times[i - 1] for i in range(1, len(times))):
        raise ValueError("Fourier times must be nondecreasing")

    dimension = dimensions[geometry]
    dx = 1.0 / n_cells
    faces = [i * dx for i in range(n_cells + 1)]
    shell_measure = [
        (faces[i + 1] ** dimension - faces[i] ** dimension) / dimension
        for i in range(n_cells)
    ]

    # Face conductances in the integrated radial conservation equation.
    left_conductance = [0.0] * n_cells
    right_conductance = [0.0] * n_cells
    for i in range(1, n_cells):
        left_conductance[i] = faces[i] ** (dimension - 1) / dx
    for i in range(n_cells - 1):
        right_conductance[i] = faces[i + 1] ** (dimension - 1) / dx
    # Dirichlet u(1)=0; the outer cell centre is dx/2 from the boundary.
    right_conductance[-1] = 1.0 / (0.5 * dx)

    pressure = [1.0] * n_cells
    current_time = 0.0
    averages = []
    total_measure = sum(shell_measure)
    for target_time in times:
        interval = target_time - current_time
        steps = max(1, math.ceil(interval / dt_max)) if interval > 0.0 else 0
        dt = interval / steps if steps else 0.0
        for _ in range(steps):
            lower = [-dt * value for value in left_conductance]
            upper = [-dt * value for value in right_conductance]
            diagonal = [
                shell_measure[i] + dt * (
                    left_conductance[i] + right_conductance[i])
                for i in range(n_cells)
            ]
            rhs = [shell_measure[i] * pressure[i] for i in range(n_cells)]
            pressure = _thomas_solve(lower, diagonal, upper, rhs)
        current_time = target_time
        averages.append(sum(shell_measure[i] * pressure[i]
                            for i in range(n_cells)) / total_measure)
    return averages
