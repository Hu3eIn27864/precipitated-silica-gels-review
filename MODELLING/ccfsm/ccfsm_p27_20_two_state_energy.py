"""P27.20: two-state, dimensionally consistent energy-rate snapshot adapter.

The caller supplies a declared FV free-energy density. P19 mechanical energy
and traction-work diagnostics are read from two P19 solve results. No energy
functional is inferred from concentrations or chemical potentials.
"""
from __future__ import annotations
import math


def _finite(value, name, *, positive=False):
    x = float(value)
    if not math.isfinite(x) or (positive and x <= 0.0):
        raise ValueError(name + " must be finite" + (" and positive" if positive else ""))
    return x


def _field(values, name):
    out = tuple(_finite(v, name) for v in values)
    if not out:
        raise ValueError(name + " must be non-empty")
    return out


def _p19_scalar(snapshot, key):
    if not isinstance(snapshot, dict) or key not in snapshot:
        raise ValueError("P19 snapshot missing " + key)
    return _finite(snapshot[key], "P19 " + key)


def build_two_state_energy_snapshot(
    *,
    time_old_s,
    time_new_s,
    cell_widths_old_m,
    cell_widths_new_m,
    fv_free_energy_density_old_j_m3,
    fv_free_energy_density_new_j_m3,
    cross_section_area_m2,
    p19_old,
    p19_new,
    use_endpoint_traction_work_difference=False,
    atol=1e-12,
    rtol=1e-10,
):
    """Return mean rates (W/m²) from two aligned 1-D FV/P19 states.

    FV free-energy density is supplied by the caller in J/m³. Cell widths
    and reference cross-section convert its integral to J. P19's stored
    energy is already in J. Endpoint traction-work difference is included
    only when explicitly enabled; it represents path work only under a
    compatible loading path (e.g. unchanged traction).
    """
    try:
        t0, t1 = _finite(time_old_s, "old time"), _finite(time_new_s, "new time")
        dt = t1-t0
        if dt <= 0:
            raise ValueError("new time must be later than old time")
        area = _finite(cross_section_area_m2, "cross-section area", positive=True)
        dx0, dx1 = _field(cell_widths_old_m, "old cell widths"), _field(cell_widths_new_m, "new cell widths")
        e0, e1 = (_field(fv_free_energy_density_old_j_m3, "old FV energy density"),
                  _field(fv_free_energy_density_new_j_m3, "new FV energy density"))
        if not (len(dx0) == len(dx1) == len(e0) == len(e1)):
            raise ValueError("both states must use the same number of FV cells")
        if any(v <= 0 for v in dx0+dx1):
            raise ValueError("cell widths must be positive")
        tol = float(atol) + float(rtol)*max(1.0, *(abs(v) for v in dx0+dx1))
        if any(abs(a-b) > tol for a,b in zip(dx0,dx1)):
            raise ValueError("FV meshes must be identical; remap conservatively first")
        fv_old = area*sum(dx*v for dx,v in zip(dx0,e0))
        fv_new = area*sum(dx*v for dx,v in zip(dx1,e1))
        mech_old = _p19_scalar(p19_old, "stored_energy_j")
        mech_new = _p19_scalar(p19_new, "stored_energy_j")
        if mech_old < 0 or mech_new < 0:
            raise ValueError("P19 stored energies must be nonnegative")
        fv_delta, mech_delta = fv_new-fv_old, mech_new-mech_old
        rates = {
            "fv_free_energy": fv_delta/(dt*area),
            "p19_mechanical_biot_stored_energy": mech_delta/(dt*area),
        }
        traction = None
        if use_endpoint_traction_work_difference:
            w0 = _p19_scalar(p19_old, "boundary_traction_work_j")
            w1 = _p19_scalar(p19_new, "boundary_traction_work_j")
            traction = (w1-w0)/(dt*area)
        return {
            "status": "two_state_energy_snapshot_built",
            "overall_valid": True,
            "time_increment_s": dt,
            "reference_area_m2": area,
            "fv_energy_old_j": fv_old,
            "fv_energy_new_j": fv_new,
            "fv_energy_increment_j": fv_delta,
            "p19_stored_energy_old_j": mech_old,
            "p19_stored_energy_new_j": mech_new,
            "p19_stored_energy_increment_j": mech_delta,
            "energy_rate_components_w_m2": rates,
            "mean_energy_rate_w_m2": sum(rates.values()),
            "endpoint_traction_work_rate_w_m2": traction,
            "external_power_components_w_m2": (
                {"p19_boundary_traction": traction} if traction is not None else {}),
            "ledger_ready": traction is not None,
            "scope": "two-state endpoint energy differences; caller-supplied FV free-energy density",
            "physical_energy_functional_certified": False,
            "path_work_certified": False,
        }
    except (TypeError, ValueError, OverflowError, ZeroDivisionError, AttributeError):
        return {"status": "invalid_or_incompatible_two_state_input", "overall_valid": False}
