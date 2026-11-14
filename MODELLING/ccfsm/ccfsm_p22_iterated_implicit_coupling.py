"""CCFSM P22: damped Picard iteration for an implicit staggered P21 step.

This module solves x^{k+1}=x^n+dt*F_P21(x^k) with under-relaxation.
Each iterate recomputes P19 mechanics through P21 and feeds the projected
mechanical pressure into Darcy and mobile advection. It is a fixed-point
solver for one implicit-Euler step, not a monolithic Newton method.
"""
from __future__ import annotations
import math

from ccfsm_p11_energy_time_integration import P11State, _validate_state
from ccfsm_p21_two_way_pressure_feedback import p21_two_way_pressure_feedback


def _finite(x, name):
    x = float(x)
    if not math.isfinite(x):
        raise ValueError(name + " must be finite")
    return x


def _relative_change(a, b, floor=1e-30):
    return max((abs(x-y) for x, y in zip(a, b)), default=0.0) / max(
        floor, *(abs(x) for x in a), *(abs(x) for x in b))


def _admissible_relaxation(current, target, lower, upper=None):
    omega = 1.0
    for i, (x, y) in enumerate(zip(current, target)):
        d = y-x
        if d < 0:
            omega = min(omega, 0.95*(x-lower)/(-d))
        if upper is not None and d > 0:
            omega = min(omega, 0.95*(upper-x)/d)
    return max(0.0, min(1.0, omega))


def p22_iterated_implicit_step(
    state, dt_s, grid, mechanical_parameters, chemistry, diffusivities_m2_s,
    external_pressure_pa, fe_quadrature, dirichlet, boundary_quadrature=(),
    external_concentrations_left=(1e-30, 1e-30),
    external_concentrations_right=(1e-30, 1e-30),
    relaxation=0.5, max_iterations=100, state_tolerance=1e-9,
    pressure_tolerance=1e-8, minimum_relaxation=1e-8,
):
    """Perform one implicit-Euler step by damped Picard iteration.

    The returned state is accepted only when both normalized state and
    projected-P19-pressure changes meet tolerances. Nonconvergence is
    reported explicitly and never silently accepted.
    """
    theta0, fields0 = _validate_state(state, grid.cells)
    dt = _finite(dt_s, "dt_s")
    omega0 = _finite(relaxation, "relaxation")
    st_tol = _finite(state_tolerance, "state_tolerance")
    p_tol = _finite(pressure_tolerance, "pressure_tolerance")
    min_omega = _finite(minimum_relaxation, "minimum_relaxation")
    if dt <= 0 or not 0 < omega0 <= 1 or max_iterations < 1:
        raise ValueError("dt, relaxation, and max_iterations must be positive")
    if st_tol <= 0 or p_tol <= 0 or not 0 < min_omega <= 1:
        raise ValueError("tolerances and minimum_relaxation must be positive")

    theta = tuple(theta0)
    fields = tuple(tuple(v) for v in fields0)
    previous_pressure = None
    history = []
    last_snapshot = None
    converged = False
    state_residual = pressure_residual = math.inf

    for iteration in range(1, max_iterations+1):
        last_snapshot = p21_two_way_pressure_feedback(
            theta, fields, grid, mechanical_parameters, chemistry,
            diffusivities_m2_s, external_pressure_pa, fe_quadrature,
            dirichlet, boundary_quadrature, external_concentrations_left,
            external_concentrations_right)
        tr = last_snapshot["transport_rhs"]
        pressure = tuple(last_snapshot["projected_spatial_pressure_cell_pa"])
        pressure_residual = (math.inf if previous_pressure is None else
                             _relative_change(pressure, previous_pressure))
        target_theta = tuple(theta0[j] + dt*tr["fluid_capacity_dot_s"][j]
                             for j in range(grid.cells))
        target_fields = tuple(tuple(
            fields0[s][j] + dt*tr["inventory_dot"][s][j]
            for j in range(grid.cells)) for s in range(4))

        current_flat = list(theta) + [v for row in fields for v in row]
        target_flat = list(target_theta) + [v for row in target_fields for v in row]
        lower = [0.0]*(grid.cells*5)
        upper = [1.0]*grid.cells + [None]*(grid.cells*4)
        omega = min(omega0, _admissible_relaxation(
            current_flat, target_flat, lower, None))
        if omega < min_omega:
            return {
                "converged": False, "iterations": iteration,
                "failure": "positivity_limiter_reached_minimum_relaxation",
                "state": None, "last_iterate_fluid_capacity": theta,
                "last_iterate_inventories": fields,
                "state_relative_residual": state_residual,
                "pressure_relative_residual": pressure_residual,
                "iteration_history": tuple(history),
                "last_snapshot": last_snapshot,
            }
        updated = [x + omega*(y-x) for x, y in zip(current_flat, target_flat)]
        n = grid.cells
        theta_new = tuple(updated[:n])
        flat = updated[n:]
        fields_new = tuple(tuple(flat[s*n:(s+1)*n]) for s in range(4))
        if any(not math.isfinite(x) or not 0 < x <= 1 for x in theta_new):
            raise ArithmeticError("internal positivity limiter failed for fluid capacity")
        if any(not math.isfinite(x) or x <= 0 for row in fields_new for x in row):
            raise ArithmeticError("internal positivity limiter failed for inventories")

        state_residual = _relative_change(updated, current_flat)
        history.append({
            "iteration": iteration, "relaxation_used": omega,
            "state_relative_residual": state_residual,
            "pressure_relative_residual": pressure_residual,
        })
        theta, fields = theta_new, fields_new
        if (previous_pressure is not None and state_residual <= st_tol
                and pressure_residual <= p_tol):
            converged = True
            break
        previous_pressure = pressure

    if not converged:
        return {
            "converged": False, "iterations": len(history),
            "failure": "picard_iteration_limit_reached",
            "state": None, "last_iterate_fluid_capacity": theta,
            "last_iterate_inventories": fields,
            "state_relative_residual": state_residual,
            "pressure_relative_residual": pressure_residual,
            "iteration_history": tuple(history),
            "last_snapshot": last_snapshot,
        }

    accepted = P11State(theta, fields, float(state.time_s)+dt)
    return {
        "converged": True, "iterations": len(history), "state": accepted,
        "accepted_dt_s": dt, "method": "damped Picard iteration for implicit Euler",
        "state_relative_residual": state_residual,
        "pressure_relative_residual": pressure_residual,
        "iteration_history": tuple(history),
        "last_snapshot": last_snapshot,
        "positivity_verified": True,
        "implicit_step_equation": "x_new = x_old + dt * F_P21(x_new)",
        "energy_monotonicity_claimed": False,
    }
