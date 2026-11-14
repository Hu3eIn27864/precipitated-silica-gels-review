"""Two-timescale reduced model for natural syneresis of precipitated silica gels.

Separates generation of intrinsic network contraction potential q from
hydraulic relaxation of observed bulk shrinkage S. Rates are in h^-1;
hydraulic input properties are otherwise SI. This is a falsifiable reduced
closure, not a full finite-strain Biot solver or a fitted target-system law.
"""
from __future__ import annotations
from dataclasses import dataclass
import math
from typing import Tuple


def _positive_finite(value: float, name: str) -> float:
    value = float(value)
    if not math.isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and strictly positive.")
    return value


def _nonnegative_finite(value: float, name: str) -> float:
    value = float(value)
    if not math.isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and non-negative.")
    return value


@dataclass(frozen=True)
class TwoTimescaleNaturalSyneresis:
    """Lumped network-generation / hydraulic-relaxation model.

    q(t): intrinsic stress-free, fully drained volume-shrinkage potential.
    S(t): observed bulk relative volume shrinkage.
    accessibility: fraction of q accessible under natural interface
    conditions; it is not an externally applied load.

    Monotone-trajectory admissibility:
      0 <= S(0) <= accessibility*q(0)
        <= accessibility*q_infinity < 1.
    """
    q_infinity: float
    network_rate_per_hour: float
    hydraulic_rate_per_hour: float
    q_initial: float = 0.0
    shrinkage_initial: float = 0.0
    accessibility: float = 1.0

    def __post_init__(self) -> None:
        q_inf = float(self.q_infinity)
        q0 = float(self.q_initial)
        s0 = float(self.shrinkage_initial)
        access = float(self.accessibility)
        if not math.isfinite(q_inf) or not 0.0 <= q_inf < 1.0:
            raise ValueError("q_infinity must be finite and lie in [0, 1).")
        if not math.isfinite(q0) or not 0.0 <= q0 <= q_inf:
            raise ValueError("q_initial must lie in [0, q_infinity].")
        if not math.isfinite(access) or not 0.0 < access <= 1.0:
            raise ValueError("accessibility must lie in (0, 1].")
        if not math.isfinite(s0) or not 0.0 <= s0 <= access * q0:
            raise ValueError(
                "shrinkage_initial must lie in [0, accessibility*q_initial]."
            )
        kn = _positive_finite(self.network_rate_per_hour, "network_rate_per_hour")
        kh = _positive_finite(self.hydraulic_rate_per_hour, "hydraulic_rate_per_hour")
        # Normalise numeric-like values even though the dataclass is frozen.
        for name, value in (
            ("q_infinity", q_inf), ("q_initial", q0),
            ("shrinkage_initial", s0), ("accessibility", access),
            ("network_rate_per_hour", kn), ("hydraulic_rate_per_hour", kh),
        ):
            object.__setattr__(self, name, value)

    def intrinsic_potential(self, time_hours: float) -> float:
        """Return q(t), the evolving stress-free contraction potential."""
        t = _nonnegative_finite(time_hours, "time_hours")
        return self.q_infinity + (
            self.q_initial - self.q_infinity
        ) * math.exp(-self.network_rate_per_hour * t)

    def shrinkage(self, time_hours: float) -> float:
        """Return observed relative volume shrinkage S(t)."""
        t = _nonnegative_finite(time_hours, "time_hours")
        kn = self.network_rate_per_hour
        kh = self.hydraulic_rate_per_hour
        delta = kh - kn
        e_h = math.exp(-kh * t)
        e_n = math.exp(-kn * t)
        # Stable divided difference, including equal-rate limit t*exp(-k*t).
        if delta == 0.0:
            divided_difference = t * e_n
        else:
            divided_difference = e_n * (-math.expm1(-delta * t)) / delta
        q_inf_a = self.accessibility * self.q_infinity
        q0_a = self.accessibility * self.q_initial
        return (
            q_inf_a
            + (self.shrinkage_initial - q_inf_a) * e_h
            + kh * (q0_a - q_inf_a) * divided_difference
        )

    def shrinkage_rate(self, time_hours: float) -> float:
        """Return dS/dt in h^-1."""
        t = _nonnegative_finite(time_hours, "time_hours")
        gap = self.accessibility * self.intrinsic_potential(t) - self.shrinkage(t)
        if gap < 0.0 and gap > -1e-13:
            gap = 0.0  # roundoff only
        if gap < 0.0:
            raise ArithmeticError("Computed state violates S <= accessibility*q.")
        return self.hydraulic_rate_per_hour * gap

    def asymptotic_slow_rate_per_hour(self) -> float:
        """Return min(k_network, k_hydraulic), the slow tail exponent."""
        return min(self.network_rate_per_hour, self.hydraulic_rate_per_hour)


def hydraulic_rate_from_properties_per_hour(
    viscosity_pa_s: float,
    drainage_length_m: float,
    intrinsic_permeability_m2: float,
    effective_modulus_pa: float,
    geometry_factor: float = 1.0,
) -> float:
    """Compute k_h = 3600*C_g*kappa*K/(mu*L_d^2) in h^-1.

    First-mode scaling only; not an estimator from shrinkage data alone.
    """
    mu = _positive_finite(viscosity_pa_s, "viscosity_pa_s")
    length = _positive_finite(drainage_length_m, "drainage_length_m")
    permeability = _positive_finite(intrinsic_permeability_m2, "intrinsic_permeability_m2")
    modulus = _positive_finite(effective_modulus_pa, "effective_modulus_pa")
    geometry = _positive_finite(geometry_factor, "geometry_factor")
    rate_per_second = geometry * permeability * modulus / (mu * length**2)
    return 3600.0 * rate_per_second


def isotropic_natural_stretch(q: float) -> float:
    """Return lambda_nat=(1-q)^(1/3); det(F_nat)=1-q exactly."""
    q = float(q)
    if not math.isfinite(q) or not 0.0 <= q < 1.0:
        raise ValueError("q must be finite and lie in [0, 1).")
    return (1.0 - q) ** (1.0 / 3.0)


def recover_unordered_rate_pair(
    rate_sum_per_hour: float, rate_product_per_hour2: float
) -> Tuple[float, float]:
    """Recover unordered positive {k_network, k_hydraulic} from sum/product."""
    total = _positive_finite(rate_sum_per_hour, "rate_sum_per_hour")
    product = _positive_finite(rate_product_per_hour2, "rate_product_per_hour2")
    discriminant = total * total - 4.0 * product
    tolerance = 1e-12 * max(total * total, 4.0 * product)
    if discriminant < -tolerance:
        raise ValueError("No real positive rate pair has these invariants.")
    root = math.sqrt(max(discriminant, 0.0))
    high = 0.5 * (total + root)
    low = product / high  # avoids cancellation for a small root
    if low <= 0.0:
        raise ValueError("The implied rate pair is not strictly positive.")
    return low, high
