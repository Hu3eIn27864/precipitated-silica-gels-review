"""Synthetic inverse recovery for common bulk-mobility/contact-resistance scales.

This is a deterministic two-parameter least-squares demonstrator, not a
general inverse solver and not a silica-gel parameter estimator.
"""
from __future__ import annotations
import math
from multilayer_reference import multilayer_eigenvalues


def _predict(design, log_mobility, log_contact, n_modes):
    storage = [float(v) for v in design["storage"]]
    mobility = [float(v) * math.exp(log_mobility) for v in design["mobility"]]
    widths = [float(v) for v in design["widths"]]
    contacts = [float(v) for v in design["contact_resistances"]]
    if not contacts or any(v <= 0.0 for v in contacts):
        raise ValueError("all contact resistances must be strictly positive")
    return [math.log(v) for v in multilayer_eigenvalues(
        storage, mobility, widths, n_modes,
        [v * math.exp(log_contact) for v in contacts])]


def _observations(records, n_modes):
    rows = []
    for record in records:
        values = [float(v) for v in record["log_rates"]]
        sigmas = [float(v) for v in record.get("sigma_log_rates", [1.0]*n_modes)]
        if len(values) != n_modes or len(sigmas) != n_modes:
            raise ValueError("each record must provide n_modes log_rates and uncertainties")
        if any(not math.isfinite(v) for v in values):
            raise ValueError("observed log rates must be finite")
        if any(not math.isfinite(v) or v <= 0 for v in sigmas):
            raise ValueError("uncertainties must be finite and positive")
        rows.extend(zip(values, sigmas))
    if not rows:
        raise ValueError("at least one observation is required")
    return rows


def recover_common_scales(records, n_modes=2, initial=(0.0, 0.0),
                          max_iterations=50, tolerance=1e-10):
    """Recover common positive mobility/contact multipliers from log modal rates.

    Each record contains a design (storage, mobility, widths,
    contact_resistances) plus observed log_rates and optional sigma_log_rates.
    Raises ValueError for rank-deficient/ill-conditioned designs or invalid
    input. Returns multipliers, weighted residual norm and convergence data.
    """
    if not records:
        raise ValueError("at least one design record is required")
    if not isinstance(n_modes, int) or isinstance(n_modes, bool) or n_modes < 1:
        raise ValueError("n_modes must be an integer >= 1")
    if not isinstance(max_iterations, int) or max_iterations < 1:
        raise ValueError("max_iterations must be a positive integer")
    if not math.isfinite(tolerance) or tolerance <= 0:
        raise ValueError("tolerance must be finite and positive")
    x = [float(initial[0]), float(initial[1])]
    if len(initial) != 2 or any(not math.isfinite(v) for v in x):
        raise ValueError("initial must contain two finite log-scales")
    observed = _observations(records, n_modes)

    def evaluate(params):
        predicted = []
        for rec in records:
            predicted.extend(_predict(rec, params[0], params[1], n_modes))
        return [(p-y)/s for p, (y, s) in zip(predicted, observed)]

    def jacobian(params, h=1e-5):
        cols = []
        for j in range(2):
            xp, xm = params[:], params[:]
            xp[j] += h
            xm[j] -= h
            rp, rm = evaluate(xp), evaluate(xm)
            cols.append([(a-b)/(2*h) for a, b in zip(rp, rm)])
        return list(zip(cols[0], cols[1]))

    def objective(residual):
        return sum(v*v for v in residual)

    for iteration in range(max_iterations + 1):
        residual = evaluate(x)
        J = jacobian(x)
        a = sum(row[0]**2 for row in J)
        b = sum(row[0]*row[1] for row in J)
        c = sum(row[1]**2 for row in J)
        det = a*c-b*b
        scale = max(1.0, (a+c)*(a+c))
        if det <= 1e-12*scale:
            raise ValueError("design is rank-deficient or too ill-conditioned")
        if iteration == max_iterations:
            break
        g0 = sum(row[0]*r for row, r in zip(J, residual))
        g1 = sum(row[1]*r for row, r in zip(J, residual))
        d0 = (-c*g0+b*g1)/det
        d1 = (b*g0-a*g1)/det
        if max(abs(d0), abs(d1)) < tolerance:
            return {"mobility_scale": math.exp(x[0]),
                    "contact_resistance_scale": math.exp(x[1]),
                    "weighted_residual_norm": math.sqrt(objective(residual)),
                    "iterations": iteration, "converged": True}
        old = objective(residual)
        accepted = False
        alpha = 1.0
        for _ in range(24):
            candidate = [x[0]+alpha*d0, x[1]+alpha*d1]
            trial = evaluate(candidate)
            if objective(trial) < old:
                x = candidate
                accepted = True
                break
            alpha *= 0.5
        if not accepted:
            if old < tolerance*tolerance:
                return {"mobility_scale": math.exp(x[0]),
                        "contact_resistance_scale": math.exp(x[1]),
                        "weighted_residual_norm": math.sqrt(old),
                        "iterations": iteration, "converged": True}
            raise ArithmeticError("Gauss-Newton line search did not reduce residual")
    residual = evaluate(x)
    norm = math.sqrt(objective(residual))
    if norm < tolerance:
        return {"mobility_scale": math.exp(x[0]),
                "contact_resistance_scale": math.exp(x[1]),
                "weighted_residual_norm": norm,
                "iterations": max_iterations, "converged": True}
    raise ArithmeticError("parameter recovery did not converge")
