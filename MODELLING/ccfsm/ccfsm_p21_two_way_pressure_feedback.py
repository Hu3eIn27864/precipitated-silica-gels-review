"""CCFSM P21: conservative two-way pressure feedback for the P20 snapshot.

P19 quadrature pressures are projected to FV cells by positive-weighted
cell averages. The projected pressure and P9 permeability define one Darcy
face-flux field. That same field updates fluid capacity and mobile M/O
advection; P13 Onsager diffusive fluxes and P10 reactions are retained.
This is a staggered snapshot operator, not a monolithic time integrator.
"""
from __future__ import annotations

import math

from ccfsm_p20_staggered_coupling import p20_staggered_coupled_snapshot


def _finite(value, name):
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(name + " must be finite")
    return value


def _project_fe_pressure_to_cells(snapshot, fe_quadrature, cells):
    pressure = snapshot["spatial_p19_pressure_at_fe_points_pa"]
    if len(pressure) != len(fe_quadrature):
        raise ValueError("P19 pressure and FE quadrature lengths differ")
    weighted = [0.0] * cells
    weights = [0.0] * cells
    for item, p in zip(fe_quadrature, pressure):
        idx = item["cell_index"]
        if not isinstance(idx, int) or idx < 0 or idx >= cells:
            raise ValueError("invalid FE cell_index")
        w = _finite(item["weight"], "FE quadrature weight")
        if w <= 0:
            raise ValueError("FE quadrature weights must be positive")
        weighted[idx] += w * _finite(p, "FE pressure")
        weights[idx] += w
    if any(w <= 0 for w in weights):
        raise ValueError("every FV cell needs at least one FE pressure sample")
    return tuple(weighted[j] / weights[j] for j in range(cells)), tuple(weights)


def _darcy_faces(cell_pressure, permeability, spacing, external_pressure):
    n = len(cell_pressure)
    q = [0.0] * (n + 1)
    kf = [0.0] * (n + 1)
    half = 0.5 * spacing
    kf[0], kf[-1] = permeability[0], permeability[-1]
    q[0] = -kf[0] * (cell_pressure[0] - external_pressure) / half
    q[-1] = -kf[-1] * (external_pressure - cell_pressure[-1]) / half
    for f in range(1, n):
        kl, kr = permeability[f-1], permeability[f]
        kf[f] = 2.0 * kl * kr / (kl + kr)
        q[f] = -kf[f] * (cell_pressure[f] - cell_pressure[f-1]) / spacing
    return tuple(q), tuple(kf)


def p21_two_way_pressure_feedback(
    fluid_capacity, inventories, grid, mechanical_parameters, chemistry,
    diffusivities_m2_s, external_pressure_pa, fe_quadrature, dirichlet,
    boundary_quadrature=(),
    external_concentrations_left=(1e-30, 1e-30),
    external_concentrations_right=(1e-30, 1e-30), tolerance=1e-9,
):
    """Return P20 snapshot plus pressure-feedback FV transport RHS.

    FE pressure is projected to each FV cell with the positive FE quadrature
    weights belonging to that cell. P13's Onsager diffusive flux and P10
    reaction rates are kept; only its Darcy-driven advective flux is replaced.
    """
    n, dx = grid.cells, float(grid.spacing_m)
    if n < 1 or dx <= 0 or not math.isfinite(dx):
        raise ValueError("grid must have positive cell count and spacing")
    if len(fluid_capacity) != n or len(inventories) != 4:
        raise ValueError("state fields must match grid and contain M/O/N/B")
    snapshot = p20_staggered_coupled_snapshot(
        fluid_capacity, inventories, grid, mechanical_parameters, chemistry,
        diffusivities_m2_s, external_pressure_pa, fe_quadrature, dirichlet,
        boundary_quadrature, external_concentrations_left,
        external_concentrations_right, tolerance,
    )
    p_cell, projection_weights = _project_fe_pressure_to_cells(
        snapshot, fe_quadrature, n)
    transport = snapshot["transport_rhs"]
    permeability = transport["intrinsic_permeability_m2_per_pas"]
    q, kf = _darcy_faces(p_cell, permeability, dx,
                         _finite(external_pressure_pa, "external pressure"))

    theta_dot = tuple(-(q[j+1] - q[j]) / dx for j in range(n))
    old_q = transport["darcy_flux_faces_m_s"]
    concentrations = transport["mobile_concentrations_mol_m3"]
    old_adv = transport["mobile_species_advective_face_fluxes_mol_m2_s"]
    old_total = transport["mobile_species_face_fluxes_mol_m2_s"]
    rhs = [list(row) for row in transport["inventory_dot"]]
    new_adv, new_total = [], []
    for species in range(2):
        c = concentrations[species]
        cleft = float(external_concentrations_left[species])
        cright = float(external_concentrations_right[species])
        adv = [0.0] * (n + 1)
        adv[0] = q[0] * (cleft if q[0] > 0 else c[0])
        adv[-1] = q[-1] * (c[-1] if q[-1] >= 0 else cright)
        for f in range(1, n):
            adv[f] = q[f] * (c[f-1] if q[f] >= 0 else c[f])
        diff = tuple(old_total[species][f] - old_adv[species][f]
                     for f in range(n + 1))
        total = tuple(adv[f] + diff[f] for f in range(n + 1))
        for j in range(n):
            rhs[species][j] -= (
                (total[j+1] - old_total[species][j+1])
                - (total[j] - old_total[species][j])
            ) / dx
        new_adv.append(tuple(adv))
        new_total.append(total)

    darcy_diss = sum(q[f]**2 / kf[f] * dx for f in range(1, n))
    reservoir_power = _finite(external_pressure_pa, "external pressure") * (q[-1] - q[0])
    old_pressure = tuple(transport["pore_pressure_pa"])
    pressure_delta = tuple(p_cell[j] - old_pressure[j] for j in range(n))
    scale = max(1.0, *(abs(x) for x in p_cell), *(abs(x) for x in old_pressure))
    feedback_transport = {
        **transport,
        "fluid_capacity_dot_s": theta_dot,
        "inventory_dot": tuple(tuple(row) for row in rhs),
        "pore_pressure_pa": p_cell,
        "darcy_flux_faces_m_s": q,
        "permeability_faces_m2_per_pas": kf,
        "mobile_species_advective_face_fluxes_mol_m2_s": tuple(new_adv),
        "mobile_species_face_fluxes_mol_m2_s": tuple(new_total),
        "darcy_internal_dissipation_w_m2": darcy_diss,
        "reservoir_hydraulic_power_w_m2": reservoir_power,
    }
    return {
        **snapshot,
        "transport_rhs": feedback_transport,
        "projected_spatial_pressure_cell_pa": p_cell,
        "pressure_projection_weight_sum_by_cell": projection_weights,
        "pressure_projection_method": "positive FE-quadrature-weighted cell average",
        "pressure_feedback_delta_from_original_p13_cell_pressure_pa": pressure_delta,
        "pressure_feedback_relative_scale": max(abs(x) for x in pressure_delta) / scale,
        "pressure_feedback_used_for_darcy_and_mobile_advection": True,
        "same_darcy_flux_used_for_fluid_and_mobile_advection": True,
        "onsager_diffusive_fluxes_retained": True,
        "reaction_rates_retained_from_p10": True,
        "two_way_coupling_scope": "staggered single-snapshot feedback; no iterative convergence or joint time integration",
    }
