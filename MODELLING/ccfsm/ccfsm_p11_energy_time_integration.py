"""CCFSM P11: positivity-controlled, energy-monitored time stepping.

The method is an adaptive, line-search explicit Euler integrator for the
P10 semidiscrete finite-volume ODE. It is intentionally restricted to
closed boundaries. A step is accepted only if all state variables remain
strictly positive (and theta <= 1) and the P9 cell free energy does not rise
beyond roundoff tolerance. This is an algorithmic acceptance property, not
an unconditional energy-stability or convergence theorem.
"""
from __future__ import annotations

from dataclasses import dataclass
import math

from ccfsm_p10_spatial_coupling import (
    p10_coupled_rhs, p10_total_fluid_capacity, p10_total_silicon
)
from ccfsm_p9_mechanical_feedback import p9_field_closure


@dataclass(frozen=True)
class P11State:
    fluid_capacity: tuple[float, ...]
    inventories: tuple[tuple[float, ...], ...]
    time_s: float = 0.0


def _validate_state(state, cells):
    if not isinstance(state, P11State):
        raise TypeError("state must be P11State")
    if len(state.fluid_capacity) != cells or len(state.inventories) != 4:
        raise ValueError("state dimensions do not match grid")
    theta = tuple(float(v) for v in state.fluid_capacity)
    fields = tuple(tuple(float(v) for v in f) for f in state.inventories)
    if any(len(f) != cells for f in fields):
        raise ValueError("inventory field length does not match grid")
    if any(not math.isfinite(v) or v <= 0.0 or v > 1.0 for v in theta):
        raise ValueError("fluid capacities must lie in (0,1]")
    if any(not math.isfinite(v) or v <= 0.0 for f in fields for v in f):
        raise ValueError("all four inventories must be finite and positive")
    if not math.isfinite(float(state.time_s)):
        raise ValueError("time must be finite")
    return theta, fields


def p11_total_free_energy(state, grid, mechanical_parameters, chemistry):
    """Integrate the P9 local stored free-energy density over the 1D grid."""
    theta, fields = _validate_state(state, grid.cells)
    mech = p9_field_closure(theta, fields, chemistry, mechanical_parameters)
    return grid.spacing_m * sum(
        cell["free_energy_j_m3_reference"] for cell in mech["cells"]
    )


def _positive_step_bound(values, rates, upper_bound=None):
    bound = math.inf
    for i, (value, rate) in enumerate(zip(values, rates)):
        if rate < 0.0:
            bound = min(bound, 0.9 * value / (-rate))
        if upper_bound is not None and rate > 0.0:
            bound = min(bound, 0.9 * (upper_bound-value) / rate)
    return bound


def p11_advance(state: P11State, dt_s, grid, mechanical_parameters, chemistry,
                diffusivities_m2_s, external_pressure_pa,
                external_concentrations_left=(0.0, 0.0),
                external_concentrations_right=(0.0, 0.0),
                max_backtracks=40, energy_rtol=1e-11):
    """Advance one accepted adaptive step; reject open-boundary states.

    The initial requested dt is reduced by positivity bounds and, if needed,
    by an energy backtracking line search. Reservoir fluxes must vanish at
    both ends to within a scale-aware tolerance. The caller may repeat this
    routine to integrate over a requested time interval.
    """
    theta, fields = _validate_state(state, grid.cells)
    if abs(float(mechanical_parameters.applied_axial_traction_pa)) > 1e-14:
        raise ValueError("P11 currently requires zero applied axial traction; mechanical boundary work is not included")
    dt = float(dt_s)
    if not math.isfinite(dt) or dt <= 0.0:
        raise ValueError("dt_s must be finite and positive")
    if not isinstance(max_backtracks, int) or max_backtracks < 0:
        raise ValueError("max_backtracks must be a nonnegative integer")
    if not math.isfinite(energy_rtol) or energy_rtol < 0.0:
        raise ValueError("energy_rtol must be finite and nonnegative")

    rhs = p10_coupled_rhs(
        theta, fields, grid, mechanical_parameters, chemistry,
        diffusivities_m2_s, external_pressure_pa,
        external_concentrations_left, external_concentrations_right
    )
    q = rhs["darcy_flux_faces_m_s"]
    bflux = rhs["mobile_species_boundary_fluxes_mol_m2_s"]
    scale_q = max(1.0, *(abs(v) for v in q))
    scale_j = max(1.0, *(abs(v) for pair in bflux for v in pair))
    if abs(q[0]) > 1e-12*scale_q or abs(q[-1]) > 1e-12*scale_q:
        raise ValueError("P11 energy-monitored step requires zero hydraulic boundary flux")
    if any(abs(v) > 1e-12*scale_j for pair in bflux for v in pair):
        raise ValueError("P11 energy-monitored step requires zero mobile-Si boundary flux")

    theta_dot = rhs["fluid_capacity_dot_s"]
    inv_dot = rhs["inventory_dot"]
    flat_state = list(theta) + [v for f in fields for v in f]
    flat_rate = list(theta_dot) + [v for f in inv_dot for v in f]
    dt = min(dt, _positive_step_bound(theta, theta_dot, upper_bound=1.0))
    dt = min(dt, _positive_step_bound(
        [v for f in fields for v in f],
        [v for f in inv_dot for v in f]
    ))
    if not math.isfinite(dt) or dt <= 0.0:
        raise RuntimeError("no positive admissible time step exists")

    energy_before = p11_total_free_energy(
        state, grid, mechanical_parameters, chemistry
    )
    si_before = p10_total_silicon(fields, grid)
    fluid_before = p10_total_fluid_capacity(theta, grid)
    last_energy = math.inf

    for backtrack in range(max_backtracks + 1):
        candidate = [x + dt*f for x, f in zip(flat_state, flat_rate)]
        n = grid.cells
        th_new = tuple(candidate[:n])
        inv_flat = candidate[n:]
        inv_new = tuple(tuple(inv_flat[k*n:(k+1)*n]) for k in range(4))
        if (all(math.isfinite(v) and 0.0 < v <= 1.0 for v in th_new)
                and all(math.isfinite(v) and v > 0.0
                        for f in inv_new for v in f)):
            trial = P11State(th_new, inv_new, state.time_s + dt)
            last_energy = p11_total_free_energy(
                trial, grid, mechanical_parameters, chemistry
            )
            allowance = energy_rtol * max(1.0, abs(energy_before))
            if last_energy <= energy_before + allowance:
                return {
                    "state": trial,
                    "accepted_dt_s": dt,
                    "backtracks": backtrack,
                    "free_energy_before_j_m2": energy_before,
                    "free_energy_after_j_m2": last_energy,
                    "free_energy_change_j_m2": last_energy-energy_before,
                    "total_silicon_before_mol_m2": si_before,
                    "total_silicon_after_mol_m2": p10_total_silicon(inv_new, grid),
                    "fluid_capacity_before_m": fluid_before,
                    "fluid_capacity_after_m": p10_total_fluid_capacity(th_new, grid),
                    "darcy_flux_faces_m_s": q,
                    "boundary_fluxes_mol_m2_s": bflux,
                    "method": "adaptive explicit Euler with positivity bound and energy backtracking",
                }
        dt *= 0.5
    raise RuntimeError(
        "P11 could not find an admissible energy-nonincreasing step; "
        f"last trial energy={last_energy!r}, initial energy={energy_before!r}"
    )
