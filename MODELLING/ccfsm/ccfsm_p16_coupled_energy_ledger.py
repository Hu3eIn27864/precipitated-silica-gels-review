"""CCFSM P16: coupled semidiscrete energy ledger and mechanical closure audit.

P16 combines P15 mobile transport, P10 detailed-balance reactions, and
Darcy pressure work. It separately tests whether the P9 mechanical stress
is variationally conjugate to the elastic/storage energy actually stored.
A closed ledger based on declared P9 conjugates is not, by itself, proof
that the constitutive mechanical closure is variationally consistent.
"""
from __future__ import annotations
import math

from ccfsm_p10_spatial_coupling import p10_coupled_rhs, _field
from ccfsm_p13_onsager_transport import p13_chemical_potential_transport
from ccfsm_p15_mobile_boundary_balance import p15_mobile_boundary_balance
from ccfsm_p9_mechanical_feedback import p9_field_closure


def p16_coupled_energy_ledger(
    fluid_capacity, inventories, grid, mechanical_parameters, chemistry,
    diffusivities_m2_s, external_pressure_pa,
    external_concentrations_left=(1e-30, 1e-30),
    external_concentrations_right=(1e-30, 1e-30),
    tolerance=5e-9,
):
    """Return chain-rule ledger, dissipation split, and P9 mechanics audit.

    All powers are per unit cross-sectional area. Positive hydraulic
    reservoir power is p_ext*(q_left-q_right), consistent with the
    positive-left-to-right Darcy face flux convention.
    """
    n, dx = grid.cells, float(grid.spacing_m)
    theta = _field(fluid_capacity, n, "fluid capacity", positive=True)
    fields = tuple(_field(f, n, f"inventory {i}", positive=True)
                   for i, f in enumerate(inventories))
    d = _field(diffusivities_m2_s, 2, "diffusivities", nonnegative=True)
    pext = float(external_pressure_pa)
    tol = float(tolerance)
    if not math.isfinite(pext) or not math.isfinite(tol) or tol <= 0:
        raise ValueError("pressure must be finite and tolerance positive")

    rhs = p13_chemical_potential_transport(
        theta, fields, grid, mechanical_parameters, chemistry, d, pext,
        external_concentrations_left, external_concentrations_right)
    mech = p9_field_closure(theta, fields, chemistry, mechanical_parameters)
    base = p10_coupled_rhs(
        theta, fields, grid, mechanical_parameters, chemistry, d, pext,
        external_concentrations_left, external_concentrations_right)
    mobile = p15_mobile_boundary_balance(
        theta, fields, grid, mechanical_parameters, chemistry, d, pext,
        external_concentrations_left, external_concentrations_right)

    # Full chain rule along the P13 semidiscrete state vector, using the
    # conjugates explicitly returned by the P9 local energy closure.
    chain_rate = 0.0
    pressure_only_rate = 0.0
    for j, cell in enumerate(mech["cells"]):
        thdot = rhs["fluid_capacity_dot_s"][j]
        pressure_only_rate += dx*cell["pore_pressure_pa"]*thdot
        chain_rate += dx*(
            cell["fluid_energy_conjugate_pa"]*thdot
            + sum(cell["total_chemical_potentials_j_mol"][i]
                  * rhs["inventory_dot"][i][j] for i in range(4))
        )

    mobile_transport_rate = sum(
        item["mobile_free_energy_rate_w_m2"]
        for item in mobile["species_balances"])

    reaction_power = 0.0
    reaction_dissipation = 0.0
    for j, cell in enumerate(mech["cells"]):
        rates = tuple(base["reaction_rates_mol_m3_s"][i][j]
                      for i in range(3))
        mu = cell["total_chemical_potentials_j_mol"]
        reaction_power += dx*(
            mu[0]*(-rates[0])
            + mu[1]*(rates[0]-rates[1])
            + mu[2]*(rates[1]-rates[2])
            + mu[3]*rates[2])
        reaction_dissipation += dx*base[
            "reaction_dissipation_w_m3_reference"][j]

    q = rhs["darcy_flux_faces_m_s"]
    k = rhs["permeability_faces_m2_per_pas"]
    darcy_dissipation = 0.0
    for f in range(n+1):
        length = 0.5*dx if f in (0, n) else dx
        darcy_dissipation += q[f]*q[f]/k[f]*length
    hydraulic_reservoir_power = pext*(q[0]-q[-1])
    hydraulic_residual = (
        pressure_only_rate - hydraulic_reservoir_power + darcy_dissipation)

    assembled_rate = (mobile_transport_rate + reaction_power
                      + pressure_only_rate)
    ledger_residual = chain_rate-assembled_rate
    predicted_open_balance = (
        mobile_transport_rate + reaction_power
        + hydraulic_reservoir_power - darcy_dissipation)
    open_balance_residual = chain_rate-predicted_open_balance

    # Variational check of P9 elastic + Biot storage energy against its
    # axial stress law, for fixed theta and inventories. P17 makes the
    # constitutive stress exactly this energy derivative.
    mechanical_residuals = []
    for cell in mech["cells"]:
        eps = cell["axial_strain"]
        eigen = cell["chemical_eigenstrain"]
        pressure = cell["pore_pressure_pa"]
        p = mechanical_parameters
        d_energy_deps = (
            p.lame_lambda_pa*(eps-3.0*eigen)
            + 2.0*p.shear_modulus_pa*(eps-eigen)
            - p.biot_coefficient*pressure)
        mechanical_residuals.append(
            d_energy_deps-p.applied_axial_traction_pa)

    scale = max(1.0, abs(chain_rate), abs(assembled_rate),
                abs(predicted_open_balance), abs(mobile_transport_rate),
                abs(reaction_power), abs(hydraulic_reservoir_power),
                darcy_dissipation)
    mechanical_scale = max(
        1.0, abs(float(mechanical_parameters.applied_axial_traction_pa)),
        *(abs(v) for v in mechanical_residuals))
    mechanics_ok = all(abs(v) <= tol*mechanical_scale
                       for v in mechanical_residuals)
    ledger_ok = abs(ledger_residual) <= tol*scale
    hydraulic_ok = abs(hydraulic_residual) <= tol*scale
    zero_traction = abs(float(
        mechanical_parameters.applied_axial_traction_pa)) <= tol
    return {
        "stored_energy_chain_rule_rate_w_m2": chain_rate,
        "mobile_transport_rate_w_m2": mobile_transport_rate,
        "reaction_chemical_power_w_m2": reaction_power,
        "reaction_dissipation_w_m2": reaction_dissipation,
        "hydraulic_pressure_storage_rate_w_m2": pressure_only_rate,
        "hydraulic_reservoir_power_w_m2": hydraulic_reservoir_power,
        "darcy_dissipation_all_faces_w_m2": darcy_dissipation,
        "hydraulic_balance_residual_w_m2": hydraulic_residual,
        "assembled_energy_rate_w_m2": assembled_rate,
        "open_boundary_energy_rate_prediction_w_m2": predicted_open_balance,
        "chain_rule_decomposition_residual_w_m2": ledger_residual,
        "open_boundary_energy_balance_residual_w_m2": open_balance_residual,
        "reaction_dissipation_nonnegative": reaction_dissipation >= -tol*scale,
        "darcy_dissipation_nonnegative": darcy_dissipation >= -tol*scale,
        "mobile_transport_component_verified": mobile[
            "all_mobile_species_balance_identities_verified"],
        "hydraulic_pressure_work_identity_verified": hydraulic_ok,
        "declared_conjugate_chain_rule_decomposition_verified": ledger_ok,
        "mechanical_energy_stationarity_residual_pa": tuple(mechanical_residuals),
        "p9_mechanical_variational_closure_verified": mechanics_ok,
        "mechanical_boundary_work_included": False,
        "zero_external_traction": zero_traction,
        "complete_thermodynamic_energy_theorem_established": False,
        "scope": (
            "Semidiscrete 1D audit along P13 RHS: P15 mobile M/O transport, "
            "P10 detailed-balance M/O/N/B reactions, P9 declared fluid and "
            "chemical conjugates, and Darcy pressure work. Mechanical "
            "variational consistency is audited separately; no global PDE "
            "theorem or physical calibration is claimed."
        ),
    }
