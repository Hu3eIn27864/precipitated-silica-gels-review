"""CCFSM P2: thermodynamically dissipative reversible Si-pool kinetics.

Concentrations are mol Si-equivalent / m^3. This is a local, closed,
well-mixed reference block, not a calibrated silica constitutive law.
"""
from __future__ import annotations

from dataclasses import dataclass
import math

R_GAS = 8.31446261815324


def _finite(value, name):
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    return value


def _positive(value, name):
    value = _finite(value, name)
    if value <= 0.0:
        raise ValueError(f"{name} must be positive")
    return value


def _nonnegative(value, name):
    value = _finite(value, name)
    if value < 0.0:
        raise ValueError(f"{name} must be nonnegative")
    return value


@dataclass(frozen=True)
class ChemicalStateP2:
    monomer: float
    oligomer: float
    network: float
    bridge: float

    def __post_init__(self):
        for name in ("monomer", "oligomer", "network", "bridge"):
            _nonnegative(getattr(self, name), name)

    @property
    def total_silicon(self) -> float:
        return self.monomer + self.oligomer + self.network + self.bridge

    @property
    def bridge_fraction(self) -> float | None:
        network_total = self.network + self.bridge
        return None if network_total == 0.0 else self.bridge / network_total


@dataclass(frozen=True)
class ChemicalParametersP2:
    reference_concentration: float
    temperature_k: float
    rate_constants_s: tuple[float, float, float]
    equilibrium_constants: tuple[float, float, float]
    activity_coefficients: tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0)

    def __post_init__(self):
        _positive(self.reference_concentration, "reference_concentration")
        _positive(self.temperature_k, "temperature_k")
        if len(self.rate_constants_s) != 3 or len(self.equilibrium_constants) != 3:
            raise ValueError("exactly three reaction constants are required")
        if len(self.activity_coefficients) != 4:
            raise ValueError("exactly four activity coefficients are required")
        for value in self.rate_constants_s:
            _nonnegative(value, "rate constant")
        for value in self.equilibrium_constants:
            _positive(value, "equilibrium constant")
        for value in self.activity_coefficients:
            _positive(value, "activity coefficient")


@dataclass(frozen=True)
class ChemicalRatesP2:
    reaction_rates: tuple[float, float, float]
    affinities_j_mol: tuple[float, float, float]
    entropy_production_w_m3: float
    free_energy_rate_w_m3: float


def evaluate_p2_rates(state: ChemicalStateP2, parameters: ChemicalParametersP2) -> ChemicalRatesP2:
    """Evaluate detailed-balance rates and chemical affinities.

    For reaction i -> i+1:
      r_i = k_i*c_ref*(a_i - a_(i+1)/K_i)
      A_i = R*T*ln(K_i*a_i/a_(i+1)).
    The zero-concentration boundary is handled by the continuous limiting
    product r*A = 0 when both directional activities vanish.
    """
    if not isinstance(state, ChemicalStateP2):
        raise TypeError("state must be ChemicalStateP2")
    if not isinstance(parameters, ChemicalParametersP2):
        raise TypeError("parameters must be ChemicalParametersP2")
    concentrations = (state.monomer, state.oligomer, state.network, state.bridge)
    activities = tuple(g * c / parameters.reference_concentration
                       for g, c in zip(parameters.activity_coefficients, concentrations))
    rates = []
    affinities = []
    dissipation = 0.0
    rt = R_GAS * parameters.temperature_k
    for i, (k, equilibrium) in enumerate(zip(
            parameters.rate_constants_s, parameters.equilibrium_constants)):
        left, right = activities[i], activities[i + 1] / equilibrium
        rate = k * parameters.reference_concentration * (left - right)
        if left > 0.0 and right > 0.0:
            affinity = rt * math.log(left / right)
            product = rate * affinity
        elif left == right:
            affinity, product = 0.0, 0.0
        else:
            # Affinity diverges logarithmically at a pure boundary while
            # the product has a finite zero limit for the vanishing side.
            affinity = (math.inf if left > right else -math.inf)
            product = math.inf
        rates.append(rate)
        affinities.append(affinity)
        dissipation += product
    return ChemicalRatesP2(tuple(rates), tuple(affinities),
                           dissipation, -dissipation)


def p2_rhs(state: ChemicalStateP2, parameters: ChemicalParametersP2) -> tuple[float, float, float, float]:
    """Return d(c_M,c_O,c_N,c_B)/dt in mol Si-equivalent m^-3 s^-1."""
    r1, r2, r3 = evaluate_p2_rates(state, parameters).reaction_rates
    return (-r1, r1-r2, r2-r3, r3)


def chemical_free_energy_density(state: ChemicalStateP2,
                                 parameters: ChemicalParametersP2) -> float:
    """Ideal-mixture free energy density up to standard-state constants.

    Returns RT*sum(c_i*(ln(a_i)-1)); zero pools use their continuous 0 ln 0 limit.
    Standard chemical potentials are encoded by the supplied equilibrium
    constants and omitted here because their linear terms are state-dependent
    but fixed by the selected reference convention.
    """
    concentrations = (state.monomer, state.oligomer, state.network, state.bridge)
    activities = tuple(g*c/parameters.reference_concentration
                       for g, c in zip(parameters.activity_coefficients, concentrations))
    total = 0.0
    for c, activity in zip(concentrations, activities):
        if c > 0.0:
            total += c * (math.log(activity) - 1.0)
    return R_GAS * parameters.temperature_k * total


def verify_p2_state(state: ChemicalStateP2, initial_total_silicon: float,
                    tolerance: float = 1e-10) -> bool:
    """Check nonnegativity and local closed-system Si conservation."""
    total = _nonnegative(initial_total_silicon, "initial_total_silicon")
    tol = _nonnegative(tolerance, "tolerance")
    return abs(state.total_silicon-total) <= tol * max(1.0, total)
