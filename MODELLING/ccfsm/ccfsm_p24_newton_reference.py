"""CCFSM P24: independent damped Newton reference for the P22 step.

The nonlinear unknown is the complete FV state (fluid capacity and M/O/N/B
inventories). Each residual evaluation independently resolves the P19 FE
mechanics through P21, so the FE pressure feedback is inside the nonlinear
residual. The FE displacement is statically condensed by the P19 solve.
The Jacobian is a transparent finite-difference reference, not an analytic
production Jacobian. This is intended for small verification problems.
"""
from __future__ import annotations
import math

from ccfsm_p11_energy_time_integration import P11State, _validate_state
from ccfsm_p21_two_way_pressure_feedback import p21_two_way_pressure_feedback


def _finite(value, name):
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(name + " must be finite")
    return value


def _norm_inf(values):
    return max((abs(float(v)) for v in values), default=0.0)


def _solve_dense(matrix, rhs, pivot_tolerance=1e-14):
    n = len(rhs)
    if n == 0 or len(matrix) != n or any(len(row) != n for row in matrix):
        raise ValueError("Newton Jacobian must be nonempty and square")
    a = [[float(matrix[i][j]) for j in range(n)] + [float(rhs[i])]
         for i in range(n)]
    scale = max(1.0, *(_norm_inf(row[:-1]) for row in a))
    for k in range(n):
        pivot = max(range(k, n), key=lambda i: abs(a[i][k]))
        if abs(a[pivot][k]) <= pivot_tolerance * scale:
            raise ArithmeticError("singular or ill-conditioned Newton Jacobian")
        a[k], a[pivot] = a[pivot], a[k]
        d = a[k][k]
        for j in range(k, n + 1):
            a[k][j] /= d
        for i in range(n):
            if i == k:
                continue
            factor = a[i][k]
            if factor:
                for j in range(k, n + 1):
                    a[i][j] -= factor * a[k][j]
    return [a[i][n] for i in range(n)]


def _pack(theta, inventories):
    return tuple(theta) + tuple(v for row in inventories for v in row)


def _unpack(vector, cells):
    theta = tuple(vector[:cells])
    fields = tuple(tuple(vector[cells + s*cells + j]
                         for j in range(cells)) for s in range(4))
    return theta, fields


def _admissible(vector, cells):
    theta, fields = _unpack(vector, cells)
    return (all(math.isfinite(x) and 0.0 < x <= 1.0 for x in theta)
            and all(math.isfinite(x) and x > 0.0
                    for row in fields for x in row))


def p24_newton_reference_step(
    state, dt_s, grid, mechanical_parameters, chemistry, diffusivities_m2_s,
    external_pressure_pa, fe_quadrature, dirichlet, boundary_quadrature=(),
    external_concentrations_left=(1e-30, 1e-30),
    external_concentrations_right=(1e-30, 1e-30),
    tolerance=1e-10, max_iterations=30, finite_difference_step=1e-6,
    minimum_line_search=2.0**-20,
):
    """Solve x-x_old-dt*F_P21(x)=0 with a damped finite-difference Newton.

    Returns no accepted state on failure. Positivity and theta<=1 are
    enforced by a backtracking line search. The final P21/P19 snapshot is
    recomputed at the converged state.
    """
    theta0, fields0 = _validate_state(state, grid.cells)
    dt = _finite(dt_s, "dt_s")
    tol = _finite(tolerance, "tolerance")
    fd = _finite(finite_difference_step, "finite_difference_step")
    min_ls = _finite(minimum_line_search, "minimum_line_search")
    if dt <= 0 or tol <= 0 or fd <= 0 or not 0 < min_ls <= 1:
        raise ValueError("dt, tolerance, FD step and line-search floor must be positive")
    if int(max_iterations) != max_iterations or max_iterations < 1:
        raise ValueError("max_iterations must be a positive integer")

    cells = grid.cells
    x0 = _pack(theta0, fields0)
    x = list(x0)
    scales = [max(1.0, abs(v)) for v in x0]
    history = []

    def evaluate(candidate):
        if not _admissible(candidate, cells):
            raise ValueError("candidate state violates admissibility")
        theta, fields = _unpack(candidate, cells)
        snap = p21_two_way_pressure_feedback(
            theta, fields, grid, mechanical_parameters, chemistry,
            diffusivities_m2_s, external_pressure_pa, fe_quadrature,
            dirichlet, boundary_quadrature, external_concentrations_left,
            external_concentrations_right)
        tr = snap["transport_rhs"]
        target = [x0[j] + dt*tr["fluid_capacity_dot_s"][j]
                  for j in range(cells)]
        for s in range(4):
            target.extend(x0[cells+s*cells+j] +
                          dt*tr["inventory_dot"][s][j] for j in range(cells))
        residual = [(candidate[j]-target[j])/scales[j]
                    for j in range(len(candidate))]
        return residual, snap

    converged = False
    snapshot = None
    residual_norm = math.inf
    for iteration in range(1, int(max_iterations)+1):
        residual, snapshot = evaluate(x)
        residual_norm = _norm_inf(residual)
        history.append({"iteration": iteration,
                        "scaled_residual_inf": residual_norm,
                        "line_search_factor": 0.0})
        if residual_norm <= tol:
            converged = True
            break

        nvar = len(x)
        jac = [[0.0]*nvar for _ in range(nvar)]
        for col in range(nvar):
            h = fd * max(1.0, abs(x[col]))
            trial = list(x)
            trial[col] += h
            if not _admissible(trial, cells):
                trial[col] = x[col] - h
            if not _admissible(trial, cells):
                raise ArithmeticError("cannot form admissible FD Jacobian perturbation")
            actual_h = trial[col] - x[col]
            rtrial, _ = evaluate(trial)
            for row in range(nvar):
                jac[row][col] = (rtrial[row]-residual[row])/actual_h

        delta = _solve_dense(jac, [-v for v in residual])
        factor = 1.0
        accepted_line_search = False
        while factor >= min_ls:
            trial = [x[j] + factor*delta[j] for j in range(nvar)]
            if _admissible(trial, cells):
                trial_residual, _ = evaluate(trial)
                trial_norm = _norm_inf(trial_residual)
                if trial_norm < residual_norm:
                    x = trial
                    history[-1]["line_search_factor"] = factor
                    accepted_line_search = True
                    break
            factor *= 0.5
        if not accepted_line_search:
            return {
                "converged": False, "state": None,
                "failure": "newton_line_search_failed",
                "iterations": iteration, "scaled_residual_inf": residual_norm,
                "iteration_history": tuple(history),
                "method": "finite-difference damped Newton with P19 statically condensed",
            }

    if not converged:
        return {
            "converged": False, "state": None,
            "failure": "newton_iteration_limit_reached",
            "iterations": len(history), "scaled_residual_inf": residual_norm,
            "iteration_history": tuple(history),
            "method": "finite-difference damped Newton with P19 statically condensed",
        }

    theta, fields = _unpack(x, cells)
    accepted = P11State(theta, fields, float(state.time_s)+dt)
    # Re-evaluate at the exact returned state; no stale Jacobian/snapshot.
    _, snapshot = evaluate(x)
    return {
        "converged": True, "state": accepted, "accepted_dt_s": dt,
        "iterations": len(history), "scaled_residual_inf": residual_norm,
        "iteration_history": tuple(history),
        "last_snapshot": snapshot,
        "positivity_verified": _admissible(x, cells),
        "pressure_snapshot_matches_accepted_state": True,
        "method": "finite-difference damped Newton with P19 statically condensed",
        "jacobian_method": "forward finite differences",
        "mechanics_treatment": "P19 equilibrium re-solved in every residual evaluation",
        "energy_monotonicity_claimed": False,
    }


def p24_compare_with_p22(p22_result, p24_result, grid):
    """Compare two converged solutions of the same accepted implicit step."""
    if not isinstance(p22_result, dict) or not p22_result.get("converged"):
        raise ValueError("P22 result must be converged")
    if not isinstance(p24_result, dict) or not p24_result.get("converged"):
        raise ValueError("P24 result must be converged")
    a, b = p22_result["state"], p24_result["state"]
    va, vb = _pack(a.fluid_capacity, a.inventories), _pack(
        b.fluid_capacity, b.inventories)
    if len(va) != len(vb) or len(va) != 5*grid.cells:
        raise ValueError("solver states do not match the comparison grid")
    state_error = _norm_inf([x-y for x, y in zip(va, vb)])
    state_scale = max(1e-30, _norm_inf(va), _norm_inf(vb))
    pa = p22_result["last_snapshot"]["projected_spatial_pressure_cell_pa"]
    pb = p24_result["last_snapshot"]["projected_spatial_pressure_cell_pa"]
    pressure_error = _norm_inf([x-y for x, y in zip(pa, pb)])
    pressure_scale = max(1e-30, _norm_inf(pa), _norm_inf(pb))
    return {
        "state_difference_inf": state_error,
        "state_relative_difference_inf": state_error/state_scale,
        "projected_pressure_difference_inf_pa": pressure_error,
        "projected_pressure_relative_difference_inf": pressure_error/pressure_scale,
        "same_accepted_time": math.isclose(a.time_s, b.time_s, rel_tol=1e-12, abs_tol=1e-15),
        "comparison_scope": "same P21 implicit-Euler residual; P22 Picard versus P24 finite-difference Newton",
        "physical_validation_claimed": False,
    }
