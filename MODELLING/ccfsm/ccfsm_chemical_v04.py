"""CCFSM v0.4 chemical submodel: dissolved silica -> oligomers -> network Si.

Natural, mechanically unloaded precipitated-silica gels only.
Concentrations are mol Si-equivalent m^-3; time is seconds.
All kinetic coefficients are user-supplied and deliberately uncalibrated.
"""
from dataclasses import dataclass
import math

R_GAS = 8.31446261815324
T_REF_K = 298.15


def _finite(x, name):
    x = float(x)
    if not math.isfinite(x):
        raise ValueError(f"{name} must be finite")
    return x


def _positive(x, name):
    x = _finite(x, name)
    if x <= 0:
        raise ValueError(f"{name} must be positive")
    return x


def _nonnegative(x, name):
    x = _finite(x, name)
    if x < 0:
        raise ValueError(f"{name} must be nonnegative")
    return x


def _bounded(x, lo, hi, name):
    x = _finite(x, name)
    if not lo <= x <= hi:
        raise ValueError(f"{name} must lie in [{lo}, {hi}]")
    return x


def arrhenius_rate(rate_ref_s, activation_energy_j_mol, temperature_k,
                   reference_temperature_k=T_REF_K):
    """Return k(T)=k_ref exp[-Ea/R(1/T-1/Tref)] in s^-1."""
    k = _nonnegative(rate_ref_s, "rate_ref_s")
    ea = _nonnegative(activation_energy_j_mol, "activation_energy_j_mol")
    t = _positive(temperature_k, "temperature_k")
    tref = _positive(reference_temperature_k, "reference_temperature_k")
    exponent = -ea / R_GAS * (1.0 / t - 1.0 / tref)
    return k * math.exp(max(-700.0, min(700.0, exponent)))


@dataclass(frozen=True)
class ChemicalEnvironment:
    """Instantaneous measured/externally computed chemical conditions.

    pH is activity-based. ionic_strength_mol_kg is molality.
    silica_solubility_mol_m3 must be supplied for the current T, pH and
    electrolyte composition; it is not silently estimated by this module.
    pKw is supplied because it varies with temperature/electrolyte.
    """
    pH: float
    temperature_k: float
    ionic_strength_mol_kg: float
    silica_solubility_mol_m3: float
    pKw: float = 14.0
    pKa_monomer: float = 9.5

    def __post_init__(self):
        _finite(self.pH, "pH")
        _positive(self.temperature_k, "temperature_k")
        _nonnegative(self.ionic_strength_mol_kg, "ionic_strength_mol_kg")
        _positive(self.silica_solubility_mol_m3, "silica_solubility_mol_m3")
        _positive(self.pKw, "pKw")
        _finite(self.pKa_monomer, "pKa_monomer")


@dataclass(frozen=True)
class ChemicalParameters:
    """Kinetic and closure parameters; no defaults imply fitted silica values."""
    reference_silica_concentration_mol_m3: float
    oligomerization_rate_ref_s: float
    network_growth_rate_ref_s: float
    dissolution_rate_ref_s: float
    bridge_formation_rate_ref_s: float
    bridge_hydrolysis_rate_ref_s: float
    activation_energy_oligomerization_j_mol: float = 0.0
    activation_energy_network_growth_j_mol: float = 0.0
    activation_energy_dissolution_j_mol: float = 0.0
    activation_energy_bridge_formation_j_mol: float = 0.0
    activation_energy_bridge_hydrolysis_j_mol: float = 0.0
    acid_catalysis_weight: float = 1.0
    acid_activity_reference: float = 1.0e-3
    acid_catalysis_order: float = 1.0
    silanolate_pair_weight: float = 0.0
    base_catalysis_weight: float = 1.0
    hydroxide_activity_reference: float = 1.0e-5
    base_catalysis_order: float = 1.0
    ionic_strength_reference_mol_kg: float = 0.1
    ionic_strength_exponent: float = 0.0
    supersaturation_order: float = 1.0
    oligomerization_order: float = 1.0
    dissolution_base_weight: float = 0.0
    dissolution_acid_weight: float = 0.0
    bridge_hydrolysis_base_weight: float = 0.0
    bridge_hydrolysis_acid_weight: float = 0.0
    load_bearing_fraction: float = 1.0

    def __post_init__(self):
        _positive(self.reference_silica_concentration_mol_m3,
                  "reference_silica_concentration_mol_m3")
        for name in (
            "oligomerization_rate_ref_s", "network_growth_rate_ref_s",
            "dissolution_rate_ref_s", "bridge_formation_rate_ref_s",
            "bridge_hydrolysis_rate_ref_s",
            "activation_energy_oligomerization_j_mol",
            "activation_energy_network_growth_j_mol",
            "activation_energy_dissolution_j_mol",
            "activation_energy_bridge_formation_j_mol",
            "activation_energy_bridge_hydrolysis_j_mol",
            "acid_catalysis_weight", "silanolate_pair_weight",
            "base_catalysis_weight", "ionic_strength_exponent",
            "dissolution_base_weight", "dissolution_acid_weight",
            "bridge_hydrolysis_base_weight", "bridge_hydrolysis_acid_weight",
        ):
            _nonnegative(getattr(self, name), name)
        for name in ("acid_activity_reference", "hydroxide_activity_reference",
                     "ionic_strength_reference_mol_kg",
                     "supersaturation_order", "oligomerization_order"):
            _positive(getattr(self, name), name)
        _bounded(self.load_bearing_fraction, 0.0, 1.0,
                 "load_bearing_fraction")
        if (self.acid_catalysis_weight + self.silanolate_pair_weight
                + self.base_catalysis_weight) <= 0:
            raise ValueError("at least one condensation pH-channel weight must be positive")


@dataclass(frozen=True)
class ChemicalState:
    time_s: float
    monomeric_silica_mol_m3: float
    soluble_oligomer_silica_mol_m3: float
    network_silicon_mol_m3: float
    bridge_fraction: float


@dataclass(frozen=True)
class ChemicalRates:
    oligomerization_mol_m3_s: float
    network_growth_mol_m3_s: float
    dissolution_mol_m3_s: float
    bridge_fraction_rate_s: float
    effective_bridge_density_mol_m3: float
    effective_bridge_density_rate_mol_m3_s: float


def _pow_ratio(value, reference, exponent):
    # Log clipping avoids overflow for very acidic/basic pH inputs.
    log_value = exponent * math.log(value / reference)
    return math.exp(max(-700.0, min(700.0, log_value)))


def acid_base_activity_factors(env, p):
    """Return acid, silanolate-pair, base and combined pH factors.

    The pair term 4 alpha(1-alpha) is a bounded speciation proxy, not a
    complete oligomer/surface speciation model. pKa is an input parameter.
    """
    a_h = 10.0 ** max(-300.0, min(300.0, -env.pH))
    a_oh = 10.0 ** max(-300.0, min(300.0, env.pH - env.pKw))
    alpha = 1.0 / (1.0 + 10.0 ** max(-300.0, min(300.0, env.pKa_monomer-env.pH)))
    f_acid = _pow_ratio(a_h, p.acid_activity_reference,
                        p.acid_catalysis_order)
    f_pair = 4.0 * alpha * (1.0 - alpha)
    f_base = _pow_ratio(a_oh, p.hydroxide_activity_reference,
                        p.base_catalysis_order)
    f_ph = (p.acid_catalysis_weight*f_acid
            + p.silanolate_pair_weight*f_pair
            + p.base_catalysis_weight*f_base)
    return f_acid, f_pair, f_base, f_ph


def evaluate_chemical_rates(state, environment, parameters):
    """Evaluate conservative Si-transfer rates and effective bridge evolution."""
    if not isinstance(state, ChemicalState):
        raise TypeError("state must be ChemicalState")
    if not isinstance(environment, ChemicalEnvironment):
        raise TypeError("environment must be ChemicalEnvironment")
    if not isinstance(parameters, ChemicalParameters):
        raise TypeError("parameters must be ChemicalParameters")

    cm = _nonnegative(state.monomeric_silica_mol_m3, "monomeric silica")
    co = _nonnegative(state.soluble_oligomer_silica_mol_m3, "soluble oligomer silica")
    cn = _nonnegative(state.network_silicon_mol_m3, "network silicon")
    beta = _bounded(state.bridge_fraction, 0.0, 1.0, "bridge_fraction")
    c_ref = parameters.reference_silica_concentration_mol_m3

    f_acid, f_pair, f_base, f_ph = acid_base_activity_factors(
        environment, parameters)
    f_ionic = (1.0 + environment.ionic_strength_mol_kg
               / parameters.ionic_strength_reference_mol_kg) ** parameters.ionic_strength_exponent
    omega = max(cm / environment.silica_solubility_mol_m3 - 1.0, 0.0)

    k_olig = arrhenius_rate(parameters.oligomerization_rate_ref_s,
        parameters.activation_energy_oligomerization_j_mol,
        environment.temperature_k)
    k_net = arrhenius_rate(parameters.network_growth_rate_ref_s,
        parameters.activation_energy_network_growth_j_mol,
        environment.temperature_k)
    k_diss = arrhenius_rate(parameters.dissolution_rate_ref_s,
        parameters.activation_energy_dissolution_j_mol,
        environment.temperature_k)
    k_bform = arrhenius_rate(parameters.bridge_formation_rate_ref_s,
        parameters.activation_energy_bridge_formation_j_mol,
        environment.temperature_k)
    k_bhyd = arrhenius_rate(parameters.bridge_hydrolysis_rate_ref_s,
        parameters.activation_energy_bridge_hydrolysis_j_mol,
        environment.temperature_k)

    r_olig = (k_olig*c_ref*(omega**parameters.supersaturation_order)
              *(cm/c_ref)**parameters.oligomerization_order
              * f_ph*f_ionic)
    r_net = k_net * co * f_ph * f_ionic
    f_diss = (1.0
        + parameters.dissolution_base_weight*f_base
        + parameters.dissolution_acid_weight*f_acid)
    r_diss = k_diss * cn * f_diss

    f_bridge_hydrolysis = (1.0
        + parameters.bridge_hydrolysis_base_weight*f_base
        + parameters.bridge_hydrolysis_acid_weight*f_acid)
    dbeta = (k_bform*f_ph*f_ionic*(1.0-beta)
             - k_bhyd*f_bridge_hydrolysis*beta)

    f_load = parameters.load_bearing_fraction
    bridge_density = f_load * cn * beta
    dnetwork = r_net-r_diss
    dbridge_density = f_load*(dnetwork*beta + cn*dbeta)

    return ChemicalRates(
        oligomerization_mol_m3_s=r_olig,
        network_growth_mol_m3_s=r_net,
        dissolution_mol_m3_s=r_diss,
        bridge_fraction_rate_s=dbeta,
        effective_bridge_density_mol_m3=bridge_density,
        effective_bridge_density_rate_mol_m3_s=dbridge_density,
    )


def chemical_rhs(state, environment, parameters):
    """Return derivatives (dc_m/dt, dc_o/dt, dc_n/dt, d_beta/dt)."""
    rates = evaluate_chemical_rates(state, environment, parameters)
    return (
        -rates.oligomerization_mol_m3_s + rates.dissolution_mol_m3_s,
        rates.oligomerization_mol_m3_s - rates.network_growth_mol_m3_s,
        rates.network_growth_mol_m3_s - rates.dissolution_mol_m3_s,
        rates.bridge_fraction_rate_s,
    )


def simulate_chemical_network(parameters, environment, duration_s, time_step_s,
                              initial_monomeric_silica_mol_m3,
                              initial_soluble_oligomer_silica_mol_m3=0.0,
                              initial_network_silicon_mol_m3=0.0,
                              initial_bridge_fraction=0.0):
    """Integrate the constant-environment chemical subsystem with RK4.

    For changing pH/T/I/solubility, call this function sequentially over
    measured protocol segments; do not substitute bath temperature for gel T.
    The solver fails rather than clipping states if a step leaves the
    nonnegative/conservative state domain.
    """
    duration = _nonnegative(duration_s, "duration_s")
    hmax = _positive(time_step_s, "time_step_s")
    y = (
        _nonnegative(initial_monomeric_silica_mol_m3, "initial monomer"),
        _nonnegative(initial_soluble_oligomer_silica_mol_m3, "initial oligomer"),
        _nonnegative(initial_network_silicon_mol_m3, "initial network silicon"),
        _bounded(initial_bridge_fraction, 0.0, 1.0, "initial bridge fraction"),
    )
    t = 0.0
    out = [ChemicalState(t, *y)]

    def rhs(v):
        state = ChemicalState(t, *v)
        return chemical_rhs(state, environment, parameters)

    while t < duration:
        h = min(hmax, duration-t)
        k1 = rhs(y)
        k2 = rhs(tuple(a+h*b/2 for a,b in zip(y,k1)))
        k3 = rhs(tuple(a+h*b/2 for a,b in zip(y,k2)))
        k4 = rhs(tuple(a+h*b for a,b in zip(y,k3)))
        yn = tuple(a+h*(b+2*c+2*d+e)/6
                   for a,b,c,d,e in zip(y,k1,k2,k3,k4))
        if min(yn[:3]) < -1e-10 or not -1e-10 <= yn[3] <= 1.0+1e-10:
            raise ArithmeticError("chemical state left admissible region; reduce time_step_s")
        y = tuple(max(0.0, v) for v in yn[:3]) + (min(1.0, max(0.0, yn[3])),)
        t += h
        out.append(ChemicalState(t, *y))
    return out
