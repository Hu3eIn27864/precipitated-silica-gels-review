"""CCFSM P12: explicit open-boundary energy-budget audit.

P12 exposes stored-energy rate, hydraulic reservoir power, mobile-Si
boundary fluxes and a transparent boundary chemical-power estimate.
It deliberately labels the budget incomplete: P10 uses concentration-based
Fick diffusion and upwind advection, so a thermodynamically exact discrete
reservoir chemical-work identity has not yet been established.
"""
from __future__ import annotations
import math

from ccfsm_p10_spatial_coupling import p10_coupled_rhs
from ccfsm_p11_energy_time_integration import P11State, p11_total_free_energy, _validate_state
from ccfsm_p9_mechanical_feedback import p9_field_closure
from ccfsm_p2_chemical_affinity import R_GAS


def p12_energy_budget_audit(state: P11State, grid, mechanical_parameters,
                            chemistry, diffusivities_m2_s,
                            external_pressure_pa,
                            external_concentrations_left=(0.0, 0.0),
                            external_concentrations_right=(0.0, 0.0)):
    """Return a diagnostic semidiscrete energy/boundary-work ledger.

    Sign convention: positive hydraulic power is work delivered by the
    pressure reservoir to the gel. Positive chemical boundary power is
    likewise estimated as work delivered to the gel. The latter uses an
    upwind/interface chemical-potential estimate and is NOT an exact discrete
    entropy flux for the current P10 Fick/upwind operator.
    """
    theta, fields = _validate_state(state, grid.cells)
    traction = float(mechanical_parameters.applied_axial_traction_pa)
    rhs = p10_coupled_rhs(
        theta, fields, grid, mechanical_parameters, chemistry,
        diffusivities_m2_s, external_pressure_pa,
        external_concentrations_left, external_concentrations_right
    )
    mech = p9_field_closure(theta, fields, chemistry, mechanical_parameters)
    dx = grid.spacing_m
    energy = p11_total_free_energy(state, grid, mechanical_parameters, chemistry)

    # Chain-rule rate of P9 stored energy along the P10 semidiscrete vector.
    energy_rate = 0.0
    for j, cell in enumerate(mech["cells"]):
        energy_rate += dx * (
            cell["fluid_energy_conjugate_pa"] * rhs["fluid_capacity_dot_s"][j]
            + sum(cell["total_chemical_potentials_j_mol"][i]
                  * rhs["inventory_dot"][i][j] for i in range(4))
        )

    q = rhs["darcy_flux_faces_m_s"]
    pext = float(external_pressure_pa)
    hydraulic_power = pext * (q[-1] - q[0])

    # Standard chemical potentials are consistent with the P2/P9 activity
    # convention. Network pools N/B have no boundary transport.
    rt = R_GAS * float(chemistry.temperature_k)
    mu0 = [0.0]
    for k in chemistry.equilibrium_constants:
        mu0.append(mu0[-1] - rt * math.log(float(k)))
    gamma = tuple(float(v) for v in chemistry.activity_coefficients)
    cL = tuple(float(v) for v in external_concentrations_left)
    cR = tuple(float(v) for v in external_concentrations_right)
    boundary = rhs["mobile_species_boundary_fluxes_mol_m2_s"]
    chemical_power_terms = []
    for species in range(2):
        left_flux, right_flux = boundary[species]
        c_edge_left = fields[species][0] / theta[0]
        c_edge_right = fields[species][-1] / theta[-1]
        # Positive left-face flux points into the domain; positive right-face
        # flux points out. Upwind chemical potential at the donor side.
        a_left_res = gamma[species] * cL[species] / float(chemistry.reference_concentration)
        a_right_res = gamma[species] * cR[species] / float(chemistry.reference_concentration)
        a_left_gel = gamma[species] * c_edge_left / float(chemistry.reference_concentration)
        a_right_gel = gamma[species] * c_edge_right / float(chemistry.reference_concentration)
        mu_left_res = mu0[species] + rt * math.log(a_left_res) if a_left_res > 0 else None
        mu_right_res = mu0[species] + rt * math.log(a_right_res) if a_right_res > 0 else None
        mu_left_gel = mu0[species] + rt * math.log(a_left_gel)
        mu_right_gel = mu0[species] + rt * math.log(a_right_gel)
        # Flux is positive left-to-right at both faces. Inward left and inward
        # right are opposite signs; use donor-side chemical potential.
        left_donor_mu = mu_left_res if left_flux > 0 and mu_left_res is not None else mu_left_gel
        right_donor_mu = mu_right_gel if right_flux > 0 else (
            mu_right_res if mu_right_res is not None else mu_right_gel)
        left_power = left_donor_mu * left_flux
        right_power = -right_donor_mu * right_flux
        chemical_power_terms.append((left_power, right_power))

    chemical_power = sum(sum(pair) for pair in chemical_power_terms)
    boundary_power_estimate = hydraulic_power + chemical_power
    residual = energy_rate - boundary_power_estimate

    closed_hydraulic = abs(q[0]) <= 1e-14 and abs(q[-1]) <= 1e-14
    closed_silicon = all(abs(v) <= 1e-14 for pair in boundary for v in pair)
    no_mechanical_work = abs(traction) <= 1e-14
    complete = closed_hydraulic and closed_silicon and no_mechanical_work

    return {
        "stored_free_energy_j_m2": energy,
        "stored_free_energy_rate_w_m2": energy_rate,
        "hydraulic_reservoir_power_w_m2": hydraulic_power,
        "mobile_silicon_boundary_power_estimate_w_m2": chemical_power,
        "mobile_silicon_boundary_power_by_species_w_m2": tuple(chemical_power_terms),
        "total_boundary_power_estimate_w_m2": boundary_power_estimate,
        "unclosed_energy_rate_residual_w_m2": residual,
        "darcy_internal_dissipation_w_m2": rhs["darcy_internal_dissipation_w_m2"],
        "diffusion_dissipation_w_m2": rhs["diffusion_dissipation_w_m2"],
        "reaction_dissipation_w_m2": dx * sum(rhs["reaction_dissipation_w_m3_reference"]),
        "hydraulic_boundary_fluxes_m_s": (q[0], q[-1]),
        "mobile_silicon_boundary_fluxes_mol_m2_s": boundary,
        "applied_axial_traction_pa": traction,
        "mechanical_work_included": False,
        "boundary_chemical_power_is_exact_discrete_entropy_flux": False,
        "complete_energy_identity_established": complete,
        "status": ("closed, zero-traction reference case: no boundary work"
                   if complete else
                   "diagnostic only: exact reservoir entropy flux and/or mechanical work remain incomplete"),
    }
