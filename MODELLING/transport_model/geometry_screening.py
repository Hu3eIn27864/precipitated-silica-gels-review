"""Deterministic screening of specimen thickness/interface-position designs."""
from __future__ import annotations
from identifiability import log_rate_sensitivity


def screen_geometries(thicknesses, interface_fractions, storage, mobility,
                      contact_resistance, n_modes=3, sigma_log_rates=None):
    """Rank two-layer geometries by local information on two global scales.

    Thicknesses and interface fractions are dimensionless in a consistent
    chosen unit system. Fractions locate the interface from the left boundary.
    This is a mathematical design screen, not an experimentally validated
    optimum; practical constraints and model discrepancy are not represented.
    """
    if not thicknesses or not interface_fractions:
        raise ValueError("provide thicknesses and interface fractions")
    if len(storage) != 2 or len(mobility) != 2:
        raise ValueError("the screening helper currently requires two layers")
    if any(t <= 0 for t in thicknesses):
        raise ValueError("thicknesses must be positive")
    if any(not 0.0 < f < 1.0 for f in interface_fractions):
        raise ValueError("interface fractions must lie strictly between 0 and 1")
    if contact_resistance <= 0:
        raise ValueError("contact resistance must be positive")
    results = []
    for thickness in thicknesses:
        for fraction in interface_fractions:
            design = {
                "storage": list(storage),
                "mobility": list(mobility),
                "widths": [thickness*fraction, thickness*(1.0-fraction)],
                "contact_resistances": [contact_resistance],
            }
            if sigma_log_rates is not None:
                design["sigma_log_rates"] = list(sigma_log_rates)
            diagnostic = log_rate_sensitivity([design], n_modes=n_modes)
            singular = diagnostic["singular_values"]
            results.append({
                "thickness": float(thickness),
                "interface_fraction": float(fraction),
                "rank": diagnostic["rank"],
                "condition_number": diagnostic["condition_number"],
                "smallest_singular_value": singular[1],
                "largest_singular_value": singular[0],
                "information_determinant": singular[0]**2 * singular[1]**2,
            })
    return sorted(results, key=lambda item: (
        item["rank"] == 2,
        item["smallest_singular_value"],
        item["information_determinant"]), reverse=True)
