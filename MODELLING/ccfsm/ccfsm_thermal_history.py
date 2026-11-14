"""Piecewise-constant temperature-history extension for natural CCFSM.

Rates are supplied for the actual gel temperature in each segment. This
module does not infer gel temperature from bath set-point and does not assign
unmeasured activation energies.
"""
from __future__ import annotations
from dataclasses import dataclass
import math
from typing import Sequence

R_GAS_J_MOL_K = 8.31446261815324


def _finite(value: float, name: str) -> float:
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite.")
    return value


def _positive(value: float, name: str) -> float:
    value = _finite(value, name)
    if value <= 0.0:
        raise ValueError(f"{name} must be strictly positive.")
    return value


def arrhenius_rate_per_hour(
    reference_rate_per_hour: float,
    activation_energy_j_mol: float,
    temperature_k: float,
    reference_temperature_k: float,
) -> float:
    """Evaluate k(T)=k_ref*exp[-Ea/R*(1/T-1/T_ref)] in h^-1.

    Ea is a fit/measurement input, never assigned by this module. Absolute
    temperatures must be supplied in kelvin.
    """
    k_ref = _positive(reference_rate_per_hour, "reference_rate_per_hour")
    ea = _finite(activation_energy_j_mol, "activation_energy_j_mol")
    if ea < 0.0:
        raise ValueError("activation_energy_j_mol must be non-negative.")
    temp = _positive(temperature_k, "temperature_k")
    temp_ref = _positive(reference_temperature_k, "reference_temperature_k")
    exponent = -ea / R_GAS_J_MOL_K * (1.0 / temp - 1.0 / temp_ref)
    return k_ref * math.exp(exponent)


@dataclass(frozen=True)
class NaturalSyneresisState:
    time_hours: float
    intrinsic_potential: float
    observed_shrinkage: float


@dataclass(frozen=True)
class RateSegment:
    """One interval with constant network and hydraulic rates."""
    duration_hours: float
    network_rate_per_hour: float
    hydraulic_rate_per_hour: float

    def __post_init__(self) -> None:
        duration = _finite(self.duration_hours, "duration_hours")
        if duration < 0.0:
            raise ValueError("duration_hours must be non-negative.")
        object.__setattr__(self, "duration_hours", duration)
        object.__setattr__(
            self, "network_rate_per_hour",
            _positive(self.network_rate_per_hour, "network_rate_per_hour"),
        )
        object.__setattr__(
            self, "hydraulic_rate_per_hour",
            _positive(self.hydraulic_rate_per_hour, "hydraulic_rate_per_hour"),
        )


def exact_segment_update(
    q: float,
    shrinkage: float,
    q_infinity: float,
    accessibility: float,
    segment: RateSegment,
) -> tuple[float, float]:
    """Exact state update over one interval with constant rates."""
    q = _finite(q, "q")
    s = _finite(shrinkage, "shrinkage")
    q_inf = _finite(q_infinity, "q_infinity")
    eta = _finite(accessibility, "accessibility")
    if not 0.0 <= q <= q_inf < 1.0:
        raise ValueError("Require 0 <= q <= q_infinity < 1.")
    if not 0.0 < eta <= 1.0:
        raise ValueError("accessibility must lie in (0, 1].")
    if not 0.0 <= s <= eta * q + 1e-13:
        raise ValueError("Require 0 <= shrinkage <= accessibility*q.")

    dt = segment.duration_hours
    kn = segment.network_rate_per_hour
    kh = segment.hydraulic_rate_per_hour
    en = math.exp(-kn * dt)
    eh = math.exp(-kh * dt)
    delta = kh - kn
    if delta == 0.0:
        divided_difference = dt * en
    else:
        divided_difference = en * (-math.expm1(-delta * dt)) / delta

    q_new = q_inf + (q - q_inf) * en
    s_new = (
        eta * q_inf
        + (s - eta * q_inf) * eh
        + eta * kh * (q - q_inf) * divided_difference
    )
    if s_new < 0.0 and s_new > -1e-13:
        s_new = 0.0
    upper = eta * q_new
    if s_new > upper and s_new < upper + 1e-13:
        s_new = upper
    if not 0.0 <= s_new <= upper + 1e-12:
        raise ArithmeticError("Exact update left the invariant region.")
    return q_new, s_new


def simulate_piecewise_constant_rates(
    segments: Sequence[RateSegment],
    q_infinity: float,
    accessibility: float = 1.0,
    q_initial: float = 0.0,
    shrinkage_initial: float = 0.0,
) -> list[NaturalSyneresisState]:
    """Propagate a state through a prescribed piecewise-constant rate history.

    Each segment's rates must already be calculated from the gel's actual
    temperature and chemistry. Result includes the initial state and each
    segment-end state.
    """
    q_inf = _finite(q_infinity, "q_infinity")
    eta = _finite(accessibility, "accessibility")
    q = _finite(q_initial, "q_initial")
    s = _finite(shrinkage_initial, "shrinkage_initial")
    if not 0.0 <= q_inf < 1.0:
        raise ValueError("q_infinity must lie in [0, 1).")
    if not 0.0 < eta <= 1.0:
        raise ValueError("accessibility must lie in (0, 1].")
    if not 0.0 <= q <= q_inf:
        raise ValueError("q_initial must lie in [0, q_infinity].")
    if not 0.0 <= s <= eta * q:
        raise ValueError("shrinkage_initial must lie in [0, accessibility*q_initial].")

    t = 0.0
    states = [NaturalSyneresisState(t, q, s)]
    for segment in segments:
        if not isinstance(segment, RateSegment):
            raise TypeError("segments must contain RateSegment instances.")
        q, s = exact_segment_update(q, s, q_inf, eta, segment)
        t += segment.duration_hours
        states.append(NaturalSyneresisState(t, q, s))
    return states
