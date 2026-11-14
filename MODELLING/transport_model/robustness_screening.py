"""Deterministic worst-case robustness screen for two-layer designs.

Perturbs interface location and layer storage, and evaluates alternative
modal subsets. This is a bounded scenario screen, not a probabilistic
uncertainty propagation or an experimental recommendation.
"""
from __future__ import annotations
import math
from identifiability import log_rate_sensitivity


def screen_robustness(design, interface_fraction, interface_offsets=(0.0,),
                      storage_scale_scenarios=((1.0, 1.0),),
                      mode_scenarios=((0, 1, 2),), n_modes=3):
    """Evaluate rank/conditioning over explicit deterministic scenarios.

    interface_fraction is measured from the left boundary. Offsets are
    absolute fractions of total thickness. Storage scenarios contain one
    positive multiplier per layer. Mode scenarios are increasing zero-based
    indices among the first n_modes eigenmodes (allowing omissions).
    """
    widths = [float(v) for v in design["widths"]]
    if len(widths) != 2 or any(not math.isfinite(v) or v <= 0 for v in widths):
        raise ValueError("design must contain two finite positive layer widths")
    if not 0.0 < interface_fraction < 1.0:
        raise ValueError("interface_fraction must lie strictly between 0 and 1")
    if not interface_offsets or not storage_scale_scenarios or not mode_scenarios:
        raise ValueError("each scenario collection must be nonempty")
    total = sum(widths)
    base_storage = [float(v) for v in design["storage"]]
    if len(base_storage) != 2 or any(not math.isfinite(v) or v <= 0 for v in base_storage):
        raise ValueError("two finite positive layer storage values are required")
    rows = []
    for offset in interface_offsets:
        fraction = interface_fraction + float(offset)
        if not math.isfinite(fraction) or not 0.0 < fraction < 1.0:
            raise ValueError("perturbed interface location leaves specimen bounds")
        for scales in storage_scale_scenarios:
            if len(scales) != 2 or any(not math.isfinite(float(v)) or float(v) <= 0 for v in scales):
                raise ValueError("each storage scenario needs two finite positive multipliers")
            perturbed = dict(design)
            perturbed["widths"] = [total*fraction, total*(1.0-fraction)]
            perturbed["storage"] = [base_storage[i]*float(scales[i]) for i in range(2)]
            for modes in mode_scenarios:
                result = log_rate_sensitivity([perturbed], n_modes=n_modes,
                                              mode_indices=modes)
                rows.append({"interface_fraction": fraction,
                             "storage_scales": [float(v) for v in scales],
                             "mode_indices": list(modes),
                             "rank": result["rank"],
                             "condition_number": result["condition_number"],
                             "smallest_singular_value": result["singular_values"][1],
                             "largest_singular_value": result["singular_values"][0],
                             "n_observations": result["n_observations"]})
    finite_conditions = [r["condition_number"] for r in rows if math.isfinite(r["condition_number"])]
    summary = {"scenario_count": len(rows),
               "minimum_rank": min(r["rank"] for r in rows),
               "rank_two_fraction": sum(r["rank"] == 2 for r in rows)/len(rows),
               "worst_condition_number": max(finite_conditions) if finite_conditions else math.inf,
               "minimum_smallest_singular_value": min(r["smallest_singular_value"] for r in rows)}
    return {"summary": summary, "scenarios": rows}
