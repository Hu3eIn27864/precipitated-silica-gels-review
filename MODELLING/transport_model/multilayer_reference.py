"""Transfer-matrix eigenvalue reference for piecewise-constant multilayers.

For S p_t = (lambda p_x)_x, each layer has constant positive S and lambda.
The state [p, q=lambda*p_x] is propagated exactly across each layer.
This module is an independent linear benchmark, not a silica constitutive model.
"""
from __future__ import annotations
import math


def _propagate(q: float, storage: float, mobility: float, width: float,
               state: tuple[float, float]) -> tuple[float, float]:
    k = q * math.sqrt(storage / mobility)
    c, s = math.cos(k * width), math.sin(k * width)
    p, flux = state
    return (c*p + s*flux/(mobility*k),
            -mobility*k*s*p + c*flux)


def multilayer_characteristic(q: float, storage: list[float],
                              mobility: list[float], widths: list[float]) -> float:
    state = (0.0, 1.0)  # p(0)=0, arbitrary nonzero initial flux
    for si, li, wi in zip(storage, mobility, widths):
        state = _propagate(q, si, li, wi, state)
    return state[0]  # drained right boundary requires p(L)=0


def multilayer_eigenvalues(storage: list[float], mobility: list[float],
                           widths: list[float], n_modes: int = 8) -> list[float]:
    if not storage or not (len(storage) == len(mobility) == len(widths)):
        raise ValueError("storage, mobility and widths must have equal nonzero lengths")
    if any(not math.isfinite(v) or v <= 0 for seq in (storage, mobility, widths) for v in seq):
        raise ValueError("all layer properties and widths must be finite and > 0")
    if not isinstance(n_modes, int) or n_modes < 1:
        raise ValueError("n_modes must be an integer >= 1")
    optical = sum(w*math.sqrt(s/l) for s, l, w in zip(storage, mobility, widths))
    step = math.pi/(100.0*optical)
    qmax = (n_modes+2)*math.pi/optical
    roots = []
    q0 = 1e-10/optical
    f0 = multilayer_characteristic(q0, storage, mobility, widths)
    q = q0+step
    while q <= qmax and len(roots) < n_modes:
        f1 = multilayer_characteristic(q, storage, mobility, widths)
        if f0*f1 < 0:
            lo, hi, flo = q-step, q, f0
            for _ in range(90):
                mid = 0.5*(lo+hi)
                fm = multilayer_characteristic(mid, storage, mobility, widths)
                if flo*fm <= 0:
                    hi = mid
                else:
                    lo, flo = mid, fm
            root = 0.5*(lo+hi)
            if not roots or root-roots[-1] > 1e-8/optical:
                roots.append(root)
        q0, f0, q = q, f1, q+step
    if len(roots) != n_modes:
        raise ArithmeticError(f"found {len(roots)} of {n_modes} requested modes")
    return [r*r for r in roots]
