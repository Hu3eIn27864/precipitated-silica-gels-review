#!/usr/bin/env python3
"""Interface-aware 1-D finite volumes for piecewise-constant material layers.

The physical layer boundaries are explicit. Cell storage is integrated over
all layer intersections; every centre-to-centre and boundary-to-centre
hydraulic resistance is integrated exactly in series. Backward Euler solves
S(x) p_t = (lambda(x) p_x)_x on a double-drained slab.

Cell pressures are representative centre values (mass-lumped FV). This
standard cell-centred formulation is conservative and exactly locates
material interfaces in capacities and face resistances.
"""
from __future__ import annotations
import math
from typing import Sequence
from heterogeneous_1d import _solve_tridiagonal


def _validate_layers(boundaries: Sequence[float], storage: Sequence[float],
                     mobility: Sequence[float], thickness: float):
    x = [float(v) for v in boundaries]
    s = [float(v) for v in storage]
    lam = [float(v) for v in mobility]
    if not math.isfinite(thickness) or thickness <= 0:
        raise ValueError("thickness must be finite and > 0")
    if len(x) < 2 or len(s) != len(x)-1 or len(lam) != len(s):
        raise ValueError("need n+1 boundaries and n storage/mobility values")
    if any(not math.isfinite(v) for v in x) or x[0] != 0.0 or x[-1] != thickness:
        raise ValueError("boundaries must start at 0 and end at thickness")
    if any(b <= a for a,b in zip(x,x[1:])):
        raise ValueError("layer boundaries must be strictly increasing")
    if any(not math.isfinite(v) or v <= 0 for v in s+lam):
        raise ValueError("storage and mobility must be finite and > 0")
    return x,s,lam


def _integrate_piecewise(a: float, b: float, boundaries: list[float],
                         values: list[float], transform=lambda v:v) -> float:
    if b < a:
        raise ValueError("integration interval must be ordered")
    total=0.0
    for i, value in enumerate(values):
        left=max(a,boundaries[i]); right=min(b,boundaries[i+1])
        if right > left:
            total += (right-left)*transform(value)
    return total


def solve_interface_aware(
    layer_boundaries_m: Sequence[float],
    storage_compliance_pa_inv: Sequence[float],
    mobility_m2_pa_s: Sequence[float],
    n_cells: int, thickness_m: float, dt_s: float, n_steps: int,
    initial_pressure_pa: float = 1.0,
    initial_pressure_profile_pa: Sequence[float] | None = None,
) -> dict[str,list]:
    """Solve using exact layer-overlap storage and integrated Darcy resistance.

    Returns cell-centre pressure profiles, storage-weighted mean pressure,
    outward boundary flux and global conservation residual. Supply either a
    scalar uniform initial pressure or an explicit cell-centred profile.
    """
    x,s,lam=_validate_layers(layer_boundaries_m,storage_compliance_pa_inv,
                             mobility_m2_pa_s,thickness_m)
    if not isinstance(n_cells,int) or isinstance(n_cells,bool) or n_cells < 2:
        raise ValueError("n_cells must be >= 2")
    if not math.isfinite(dt_s) or dt_s <= 0: raise ValueError("dt_s must be > 0")
    if not isinstance(n_steps,int) or isinstance(n_steps,bool) or n_steps < 1:
        raise ValueError("n_steps must be >= 1")
    dx=thickness_m/n_cells
    centres=[(i+0.5)*dx for i in range(n_cells)]
    edges=[i*dx for i in range(n_cells+1)]
    capacity=[_integrate_piecewise(edges[i],edges[i+1],x,s) for i in range(n_cells)]
    conductance=[0.0]*(n_cells+1)
    conductance[0]=1.0/_integrate_piecewise(0.0,centres[0],x,lam,lambda v:1.0/v)
    conductance[n_cells]=1.0/_integrate_piecewise(centres[-1],thickness_m,x,lam,lambda v:1.0/v)
    for j in range(1,n_cells):
        resistance=_integrate_piecewise(centres[j-1],centres[j],x,lam,lambda v:1.0/v)
        conductance[j]=1.0/resistance
    lower=[0.0]*n_cells; upper=[0.0]*n_cells; diagonal=[0.0]*n_cells
    for i in range(n_cells):
        lower[i]=-conductance[i] if i else 0.0
        upper[i]=-conductance[i+1] if i<n_cells-1 else 0.0
        diagonal[i]=capacity[i]/dt_s+conductance[i]+conductance[i+1]
    if initial_pressure_profile_pa is None:
        if not math.isfinite(initial_pressure_pa):
            raise ValueError("initial pressure must be finite")
        p=[float(initial_pressure_pa)]*n_cells
    else:
        p=[float(v) for v in initial_pressure_profile_pa]
        if len(p)!=n_cells or any(not math.isfinite(v) for v in p):
            raise ValueError("initial pressure profile must contain n_cells finite values")
    total_capacity=sum(capacity)
    times=[0.0]; profiles=[p[:]]
    means=[sum(c*v for c,v in zip(capacity,p))/total_capacity]
    fluxes=[0.0]; residuals=[0.0]
    for step in range(1,n_steps+1):
        old=sum(c*v for c,v in zip(capacity,p))
        rhs=[capacity[i]*p[i]/dt_s for i in range(n_cells)]
        p=_solve_tridiagonal(lower,diagonal,upper,rhs)
        out=conductance[0]*p[0]+conductance[-1]*p[-1]
        new=sum(c*v for c,v in zip(capacity,p))
        times.append(step*dt_s); profiles.append(p[:])
        means.append(new/total_capacity); fluxes.append(out)
        residuals.append(new-old+dt_s*out)
    return {"times_s":times,"profiles_pa":profiles,"mean_pressure_pa":means,
            "boundary_outflow_m_s":fluxes,"balance_residual_m":residuals,
            "cell_capacity_pa_inv_m":capacity,"face_conductance_m_pa_s":conductance,
            "cell_centres_m":centres}
