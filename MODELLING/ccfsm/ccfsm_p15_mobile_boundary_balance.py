"""CCFSM P15: unified mobile-species advection/Onsager boundary audit.

The audit combines the P13 Onsager diffusive flux with the P14 upwind
advective flux. It verifies a semidiscrete free-energy identity for the
mobile ideal-mixture component only; reactions, Darcy work and mechanics
are deliberately excluded.
"""
from __future__ import annotations
import math

from ccfsm_p2_chemical_affinity import R_GAS
from ccfsm_p10_spatial_coupling import _field, _logmean, _chemistry_validate
from ccfsm_p13_onsager_transport import (
    p13_chemical_potential_transport, _mu0,
)


def p15_mobile_boundary_balance(
    fluid_capacity, inventories, grid, mechanical_parameters, chemistry,
    diffusivities_m2_s, external_pressure_pa,
    external_concentrations_left=(1e-30, 1e-30),
    external_concentrations_right=(1e-30, 1e-30),
):
    """Audit the two mobile species using exactly the P13 face fluxes.

    Positive face flux points left-to-right. The free-energy density per
    reference volume for species i is
      m_i * [mu0_i + RT*(log(gamma_i*c_i/c_ref)-1)].
    Reservoir diffusive chemical power is mu_res,L*Jdiff_L -
    mu_res,R*Jdiff_R. Advective boundary power uses the actual upwind donor.
    """
    n, dx = grid.cells, float(grid.spacing_m)
    theta = _field(fluid_capacity, n, "fluid capacity", positive=True)
    if len(inventories) != 4:
        raise ValueError("four inventory fields M/O/N/B required")
    fields = tuple(_field(f, n, f"inventory {i}", positive=True)
                   for i, f in enumerate(inventories))
    d = _field(diffusivities_m2_s, 2, "diffusivities", nonnegative=True)
    c_left = _field(external_concentrations_left, 2,
                    "left reservoir concentrations", positive=True)
    c_right = _field(external_concentrations_right, 2,
                     "right reservoir concentrations", positive=True)
    cref, rt, _, _, gamma = _chemistry_validate(chemistry)
    base = p13_chemical_potential_transport(
        theta, fields, grid, mechanical_parameters, chemistry, d,
        external_pressure_pa, c_left, c_right)
    q = base["darcy_flux_faces_m_s"]
    mu0 = _mu0(chemistry)
    all_species = []
    for s in range(2):
        c = tuple(fields[s][j]/theta[j] for j in range(n))
        mu = tuple(mu0[s] + rt*math.log(gamma[s]*v/cref) for v in c)
        mu_res_l = mu0[s] + rt*math.log(gamma[s]*c_left[s]/cref)
        mu_res_r = mu0[s] + rt*math.log(gamma[s]*c_right[s]/cref)
        adv = base["mobile_species_advective_face_fluxes_mol_m2_s"][s]
        total = base["mobile_species_face_fluxes_mol_m2_s"][s]
        diff = tuple(total[f]-adv[f] for f in range(n+1))

        # Chain-rule rate of the mobile free energy under transport only.
        theta_dot = tuple(-(q[j+1]-q[j])/dx for j in range(n))
        m_dot = tuple(-(total[j+1]-total[j])/dx for j in range(n))
        energy_rate = dx*sum(
            mu[j]*m_dot[j] - rt*c[j]*theta_dot[j] for j in range(n)
        )

        # P14 upwind production, scaled by RT. Linear standard-state and
        # constant activity terms cancel from internal production.
        adv_diss = 0.0
        for f in range(1, n):
            qf, cl, cr = q[f], c[f-1], c[f]
            if qf > 0:
                adv_diss += rt*qf*(cr-cl-cl*math.log(cr/cl))
            elif qf < 0:
                adv_diss += rt*(-qf)*(cl-cr-cr*math.log(cl/cr))

        # P13 Onsager dissipation, including half-cell reservoir interfaces.
        diff_diss = 0.0
        for f in range(1, n):
            cbar = _logmean(c[f-1], c[f])
            theta_face = 0.5*(theta[f-1]+theta[f])
            mobility = theta_face*d[s]*cbar/rt
            grad_mu = (mu[f]-mu[f-1])/dx
            diff_diss += mobility*grad_mu*grad_mu*dx
        boundary_diff_diss = 0.0
        half = 0.5*dx
        for cell, cres, mures, flux, side in (
            (0, c_left[s], mu_res_l, diff[0], "left"),
            (n-1, c_right[s], mu_res_r, diff[-1], "right"),
        ):
            if d[s] > 0:
                cbar = _logmean(cres, c[cell])
                mobility = theta[cell]*d[s]*cbar/rt
                delta = (mu[cell]-mures) if side == "left" else (mures-mu[cell])
                boundary_diff_diss += mobility*(delta/half)**2*half

        # P14 boundary potential flux generalized to species standard state
        # and constant activity coefficient.
        def advective_density(value):
            return value*(mu0[s] + rt*(math.log(gamma[s]*value/cref)-1.0))
        adv_boundary = q[0]*advective_density(
            c_left[s] if q[0] > 0 else c[0]) - q[-1]*advective_density(
            c[-1] if q[-1] >= 0 else c_right[s])
        reservoir_diff_power = mu_res_l*diff[0] - mu_res_r*diff[-1]
        predicted_rate = (adv_boundary + reservoir_diff_power - adv_diss
                          - diff_diss - boundary_diff_diss)
        residual = energy_rate-predicted_rate
        scale = max(1.0, abs(energy_rate), abs(predicted_rate),
                    abs(adv_boundary), abs(reservoir_diff_power),
                    adv_diss, diff_diss, boundary_diff_diss)
        all_species.append({
            "mobile_free_energy_rate_w_m2": energy_rate,
            "advective_boundary_free_energy_power_w_m2": adv_boundary,
            "reservoir_diffusive_chemical_power_w_m2": reservoir_diff_power,
            "upwind_internal_dissipation_w_m2": adv_diss,
            "onsager_internal_dissipation_w_m2": diff_diss,
            "onsager_reservoir_interface_dissipation_w_m2": boundary_diff_diss,
            "balance_residual_w_m2": residual,
            "balance_identity_verified": abs(residual) <= 2e-10*scale,
            "total_face_flux_mol_m2_s": total,
            "advective_face_flux_mol_m2_s": adv,
            "diffusive_face_flux_mol_m2_s": diff,
        })
    return {
        "species_balances": tuple(all_species),
        "all_mobile_species_balance_identities_verified": all(
            item["balance_identity_verified"] for item in all_species),
        "scope": ("M/O mobile ideal-mixture free energy; P13 Onsager diffusion "
                  "and P14 upwind advection only; reaction, Darcy pressure "
                  "work, mechanics and nonideal/structural energies excluded"),
    }
