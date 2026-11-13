"""Independent eigenfunction reference for a fixed two-layer drained slab.

Solves S(x) dp/dt = d/dx(lambda(x) dp/dx), with p(0)=p(L)=0,
continuity of p and lambda*dp/dx at x=a, and uniform initial pressure.
Standard-library only; this is code verification, not a silica model.
"""
from __future__ import annotations
import math


def _bisect_root(fn, left: float, right: float, *, tol: float = 1e-13) -> float:
    fl, fr = fn(left), fn(right)
    if fl == 0.0:
        return left
    if fr == 0.0:
        return right
    if fl * fr > 0.0:
        raise ValueError("root interval does not bracket a sign change")
    for _ in range(100):
        mid = 0.5 * (left + right)
        fm = fn(mid)
        if abs(fm) < 1e-14 or right - left < tol * max(1.0, abs(mid)):
            return mid
        if fl * fm <= 0.0:
            right, fr = mid, fm
        else:
            left, fl = mid, fm
    return 0.5 * (left + right)


def two_layer_eigenvalues(
    storage_left: float, mobility_left: float,
    storage_right: float, mobility_right: float,
    thickness: float, interface_x: float, n_modes: int = 80,
) -> list[float]:
    """Return first eigen-decay rates sigma [1/s], in ascending order."""
    vals = (storage_left, mobility_left, storage_right, mobility_right,
            thickness, interface_x)
    if any(not math.isfinite(v) or v <= 0.0 for v in vals):
        raise ValueError("coefficients, thickness and interface must be finite and > 0")
    if interface_x >= thickness:
        raise ValueError("interface_x must lie strictly inside the slab")
    if not isinstance(n_modes, int) or n_modes < 1:
        raise ValueError("n_modes must be an integer >= 1")
    a, b = interface_x, thickness - interface_x
    d1, d2 = mobility_left / storage_left, mobility_right / storage_right
    optical_length = a / math.sqrt(d1) + b / math.sqrt(d2)

    # Determinant form of the interface condition avoids cotangent poles.
    # Equivalent to lambda1*k1*cot(k1*a) + lambda2*k2*cot(k2*b) = 0.
    def determinant(q: float) -> float:
        k1, k2 = q / math.sqrt(d1), q / math.sqrt(d2)
        return (mobility_left*k1*math.cos(k1*a)*math.sin(k2*b)
                + mobility_right*k2*math.sin(k1*a)*math.cos(k2*b))

    dq = math.pi / (80.0 * optical_length)
    qmax = (n_modes + 3.0) * math.pi / optical_length
    roots: list[float] = []
    q0 = 1e-10 / optical_length
    f0 = determinant(q0)
    q = q0 + dq
    while q <= qmax and len(roots) < n_modes:
        f1 = determinant(q)
        if f0 * f1 < 0.0:
            root = _bisect_root(determinant, q - dq, q)
            if not roots or root - roots[-1] > 1e-8 / optical_length:
                roots.append(root)
        q0, f0 = q, f1
        q += dq
    if len(roots) < n_modes:
        raise ArithmeticError(f"found only {len(roots)} of {n_modes} requested eigenvalues")
    return [q*q for q in roots]


def two_layer_mean_pressure_ratio(
    time_s: float, storage_left: float, mobility_left: float,
    storage_right: float, mobility_right: float, thickness: float,
    interface_x: float, n_modes: int = 100,
) -> float:
    """Storage-weighted mean pressure / initial pressure for uniform p(x,0)."""
    if not math.isfinite(time_s) or time_s < 0.0:
        raise ValueError("time_s must be finite and >= 0")
    if time_s == 0.0:
        return 1.0
    rates = two_layer_eigenvalues(storage_left, mobility_left,
                                  storage_right, mobility_right,
                                  thickness, interface_x, n_modes)
    a, b = interface_x, thickness - interface_x
    total_capacity = storage_left*a + storage_right*b
    ratio = 0.0
    for sigma in rates:
        k1 = math.sqrt(sigma*storage_left/mobility_left)
        k2 = math.sqrt(sigma*storage_right/mobility_right)
        s2 = math.sin(k2*b)
        if abs(s2) < 1e-14:
            continue
        amp2 = math.sin(k1*a)/s2
        integral_left = (1.0-math.cos(k1*a))/k1
        integral_right = amp2*(1.0-math.cos(k2*b))/k2
        weighted_integral = (storage_left*integral_left
                             + storage_right*integral_right)
        norm_left = a/2.0-math.sin(2.0*k1*a)/(4.0*k1)
        norm_right = amp2*amp2*(b/2.0-math.sin(2.0*k2*b)/(4.0*k2))
        weighted_norm = storage_left*norm_left + storage_right*norm_right
        ratio += (weighted_integral**2/(weighted_norm*total_capacity)
                  * math.exp(-sigma*time_s))
    return ratio
