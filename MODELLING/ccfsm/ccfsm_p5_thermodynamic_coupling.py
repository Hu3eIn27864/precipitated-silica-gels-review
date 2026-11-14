"""CCFSM P5 local thermodynamic kernel.

Small-strain, isothermal reference-volume constitutive block. Mobile pools M/O
are stored in pore fluid; network pools N/B are immobilized in the skeleton.
This is not a spatial PDE solver.
"""
from __future__ import annotations
from dataclasses import dataclass
import math
from ccfsm_p2_chemical_affinity import ChemicalParametersP2, R_GAS


@dataclass(frozen=True)
class P5Parameters:
    lame_lambda_pa: float
    shear_modulus_pa: float
    biot_modulus_pa: float
    biot_coefficient: float
    initial_fluid_capacity: float
    bridge_eigenstrain: float
    bridge_reference: float
    bridge_regularization: float
    chemistry: ChemicalParametersP2

    def __post_init__(self):
        vals = (self.lame_lambda_pa, self.shear_modulus_pa,
                self.biot_modulus_pa, self.biot_coefficient,
                self.initial_fluid_capacity, self.bridge_eigenstrain,
                self.bridge_reference, self.bridge_regularization)
        if any(not math.isfinite(float(v)) for v in vals):
            raise ValueError("P5 parameters must be finite")
        if self.lame_lambda_pa < 0 or self.shear_modulus_pa <= 0:
            raise ValueError("elastic moduli must be positive (lambda nonnegative)")
        if self.biot_modulus_pa <= 0:
            raise ValueError("Biot modulus must be positive")
        if not 0 <= self.biot_coefficient <= 1:
            raise ValueError("Biot coefficient must lie in [0, 1]")
        if not 0 < self.initial_fluid_capacity <= 1:
            raise ValueError("initial fluid capacity must lie in (0, 1]")
        if self.bridge_eigenstrain < 0:
            raise ValueError("bridge eigenstrain coefficient must be nonnegative")
        if not 0 <= self.bridge_reference <= 1:
            raise ValueError("bridge reference fraction must lie in [0, 1]")
        if self.bridge_regularization <= 0:
            raise ValueError("bridge regularization must be positive")


@dataclass(frozen=True)
class P5Result:
    theta: float
    pore_pressure_pa: float
    osmotic_pressure_pa: float
    fluid_energy_conjugate_pa: float
    bridge_fraction: float
    stress_pa: tuple[tuple[float, float, float], ...]
    free_energy_j_m3_reference: float
    chemical_potentials_j_mol: tuple[float, float, float, float]
    total_potentials_j_mol: tuple[float, float, float, float]
    reaction_affinities_j_mol: tuple[float, float, float]
    reaction_rates_mol_m3_s: tuple[float, float, float]
    reaction_dissipation_w_m3_reference: float


def _log_mean(x: float, y: float) -> float:
    if x <= 0 or y <= 0:
        raise ValueError("activities must be strictly positive")
    if x == y:
        return x
    # Stable near equality; otherwise use the exact logarithmic mean.
    if abs(x - y) <= 1e-8 * max(x, y):
        return 0.5 * (x + y)
    return (x - y) / (math.log(x) - math.log(y))


def p5_evaluate(
    strain: tuple[tuple[float, float, float], ...],
    fluid_content_increment: float,
    mobile_inventories: tuple[float, float],
    network_inventories: tuple[float, float],
    parameters: P5Parameters,
) -> P5Result:
    """Evaluate local P5 energy, stress, potentials, and reaction dissipation.

    Inventories m_M,m_O,s_N,s_B are mol Si-equivalent / m^3 reference.
    Strain is a symmetric small-strain 3x3 tensor (dimensionless).
    """
    if len(strain) != 3 or any(len(row) != 3 for row in strain):
        raise ValueError("strain must be a 3x3 tensor")
    eps = tuple(tuple(float(v) for v in row) for row in strain)
    if any(not math.isfinite(v) for row in eps for v in row):
        raise ValueError("strain entries must be finite")
    for i in range(3):
        for j in range(3):
            if abs(eps[i][j] - eps[j][i]) > 1e-10:
                raise ValueError("strain tensor must be symmetric")
    zeta = float(fluid_content_increment)
    if not math.isfinite(zeta):
        raise ValueError("fluid content increment must be finite")
    if len(mobile_inventories) != 2 or len(network_inventories) != 2:
        raise ValueError("two mobile and two network inventories are required")
    inventories = tuple(float(v) for v in (*mobile_inventories, *network_inventories))
    if any(not math.isfinite(v) or v <= 0 for v in inventories):
        raise ValueError("P5 interior inventories must be finite and positive")

    theta = parameters.initial_fluid_capacity + zeta
    if theta <= 0:
        raise ValueError("fluid capacity theta must remain positive")
    m_m, m_o, s_n, s_b = inventories
    c_ref = parameters.chemistry.reference_concentration
    gamma = parameters.chemistry.activity_coefficients
    temperature = parameters.chemistry.temperature_k
    rt = R_GAS * temperature
    activities = (
        gamma[0] * m_m / (theta * c_ref),
        gamma[1] * m_o / (theta * c_ref),
        gamma[2] * s_n / c_ref,
        gamma[3] * s_b / c_ref,
    )
    mu0 = [0.0]
    for equilibrium in parameters.chemistry.equilibrium_constants:
        mu0.append(mu0[-1] - rt * math.log(equilibrium))
    mu_chem = tuple(mu0[i] + rt * math.log(activities[i]) for i in range(4))

    trace = sum(eps[i][i] for i in range(3))
    b_den = s_n + s_b + parameters.bridge_regularization
    bridge_fraction = s_b / b_den
    beta = parameters.bridge_eigenstrain
    eigen = beta * (bridge_fraction - parameters.bridge_reference)
    elastic_strain = tuple(tuple(
        eps[i][j] - (eigen if i == j else 0.0)
        for j in range(3)
    ) for i in range(3))
    elastic_trace = sum(elastic_strain[i][i] for i in range(3))
    lam, shear = parameters.lame_lambda_pa, parameters.shear_modulus_pa
    elastic_stress = tuple(tuple(
        2.0 * shear * elastic_strain[i][j]
        + (lam * elastic_trace if i == j else 0.0)
        for j in range(3)
    ) for i in range(3))
    pressure = parameters.biot_modulus_pa * (
        zeta - parameters.biot_coefficient * trace
    )
    # Mobile ideal-mixture energy depends on theta via a_i=m_i/(theta*c_ref).
    # Thus dPsi/dtheta = p - RT*(c_M+c_O); Darcy still uses mechanical p.
    osmotic_pressure = rt * (m_m + m_o) / theta
    fluid_energy_conjugate = pressure - osmotic_pressure
    stress = tuple(tuple(
        elastic_stress[i][j] - (
            parameters.biot_coefficient * pressure if i == j else 0.0
        ) for j in range(3)
    ) for i in range(3))

    elastic_energy = shear * sum(
        elastic_strain[i][j] ** 2 for i in range(3) for j in range(3)
    ) + 0.5 * lam * elastic_trace ** 2
    storage_energy = 0.5 * parameters.biot_modulus_pa * (
        zeta - parameters.biot_coefficient * trace
    ) ** 2
    chemical_energy = sum(
        inventories[i] * (mu0[i] + rt * (math.log(activities[i]) - 1.0))
        for i in range(4)
    )
    free_energy = elastic_energy + storage_energy + chemical_energy

    # d(psi_el)/db = -beta * trace(C : (epsilon - epsilon_ch)).
    dpsi_db = -beta * sum(elastic_stress[i][i] for i in range(3))
    db_ds_n = -s_b / (b_den * b_den)
    db_ds_b = (s_n + parameters.bridge_regularization) / (b_den * b_den)
    mu_mech = (0.0, 0.0, dpsi_db * db_ds_n, dpsi_db * db_ds_b)
    mu_total = tuple(mu_chem[i] + mu_mech[i] for i in range(4))
    affinities = tuple(mu_total[i] - mu_total[i + 1] for i in range(3))

    rates = []
    dissipation = 0.0
    for i, (k, equilibrium) in enumerate(zip(
        parameters.chemistry.rate_constants_s,
        parameters.chemistry.equilibrium_constants
    )):
        x, y = activities[i], activities[i + 1] / equilibrium
        mobility = _log_mean(x, y)
        rate = k * c_ref * mobility * affinities[i] / rt
        rates.append(rate)
        dissipation += rate * affinities[i]

    return P5Result(
        theta, pressure, osmotic_pressure, fluid_energy_conjugate,
        bridge_fraction, stress, free_energy,
        mu_chem, mu_total, affinities, tuple(rates), dissipation
    )
