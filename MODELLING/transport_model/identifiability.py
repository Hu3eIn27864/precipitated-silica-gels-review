"""Local identifiability diagnostics for bulk mobility and contact resistance.

The two fitted log-parameters are a common multiplier on all layer mobilities
and a common multiplier on all strictly-positive interface resistances.
Observations are selected log modal decay rates from independent geometries.
This is a design diagnostic, not a silica parameter estimator.
"""
from __future__ import annotations
import math
from multilayer_reference import multilayer_eigenvalues


def _rates(design, mobility_scale, contact_scale, n_modes):
    storage = [float(v) for v in design["storage"]]
    mobility = [float(v) * mobility_scale for v in design["mobility"]]
    widths = [float(v) for v in design["widths"]]
    contacts = [float(v) for v in design["contact_resistances"]]
    if not contacts or any(v <= 0.0 for v in contacts):
        raise ValueError("all contact resistances must be strictly positive for log sensitivities")
    return multilayer_eigenvalues(storage, mobility, widths, n_modes,
                                  [v * contact_scale for v in contacts])


def log_rate_sensitivity(designs, n_modes=2, step=1e-4, mode_indices=None):
    """Return log-rate Jacobian and 2-parameter rank/conditioning diagnostics.

    Each design maps storage, mobility, widths and positive contact_resistances.
    Optional sigma_log_rates weights rows. mode_indices selects zero-based,
    strictly increasing eigenmode indices among the first n_modes modes.
    """
    if not designs:
        raise ValueError("at least one design is required")
    if not isinstance(n_modes, int) or isinstance(n_modes, bool) or n_modes < 1:
        raise ValueError("n_modes must be an integer >= 1")
    if not math.isfinite(step) or step <= 0.0 or step >= 0.1:
        raise ValueError("step must be finite and in (0, 0.1)")
    if mode_indices is None:
        indices = list(range(n_modes))
    else:
        indices = list(mode_indices)
        if (not indices or any(not isinstance(i, int) or isinstance(i, bool) or i < 0
                               for i in indices) or
                indices != sorted(set(indices))):
            raise ValueError("mode_indices must be nonempty, unique, increasing nonnegative integers")
        if indices[-1] >= n_modes:
            raise ValueError("mode_indices must be smaller than n_modes")
    rows = []
    for design in designs:
        plus_m = _rates(design, math.exp(step), 1.0, n_modes)
        minus_m = _rates(design, math.exp(-step), 1.0, n_modes)
        plus_r = _rates(design, 1.0, math.exp(step), n_modes)
        minus_r = _rates(design, 1.0, math.exp(-step), n_modes)
        sigmas = design.get("sigma_log_rates", [1.0] * n_modes)
        if len(sigmas) != n_modes or any(not math.isfinite(float(v)) or float(v) <= 0.0 for v in sigmas):
            raise ValueError("sigma_log_rates must contain n_modes finite positive values")
        for i in indices:
            weight = float(sigmas[i])
            rows.append([
                (math.log(plus_m[i]) - math.log(minus_m[i])) / (2.0 * step * weight),
                (math.log(plus_r[i]) - math.log(minus_r[i])) / (2.0 * step * weight),
            ])

    a = sum(row[0] * row[0] for row in rows)
    b = sum(row[0] * row[1] for row in rows)
    c = sum(row[1] * row[1] for row in rows)
    trace = a + c
    # Stable eigenvalue calculation: direct trace-discriminant subtraction
    # loses the small eigenvalue when the two sensitivity columns are nearly
    # collinear. For a two-column matrix, det(J'J) is the sum of squared
    # 2x2 minors (Cauchy-Binet), which avoids that catastrophic cancellation.
    eig_max = max(0.0, 0.5 * (trace + math.hypot(a - c, 2.0 * b)))
    gram_determinant = sum(
        (rows[i][0] * rows[j][1] - rows[j][0] * rows[i][1]) ** 2
        for i in range(len(rows)) for j in range(i + 1, len(rows)))
    eig_min = gram_determinant / eig_max if eig_max > 0.0 else 0.0
    singular_values = [math.sqrt(eig_max), math.sqrt(max(0.0, eig_min))]
    tol = 1e-10 * max(1.0, singular_values[0])
    rank = sum(v > tol for v in singular_values)
    condition = (singular_values[0] / singular_values[1]
                 if rank == 2 else math.inf)
    return {"jacobian": rows, "singular_values": singular_values,
            "rank": rank, "condition_number": condition,
            "n_observations": len(rows), "mode_indices": indices,
            "parameter_names": ["log_bulk_mobility_scale", "log_contact_resistance_scale"],
            "finite_difference_step": step}
