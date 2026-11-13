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
    interface_contact_resistance_pa_s_m: Sequence[float] | None = None,
) -> dict[str,list]:
    """Solve with exact layer storage, bulk resistance and interface contacts.

    Returns cell-centre pressure profiles, storage-weighted mean pressure,
    outward boundary flux and global conservation residual. Supply either a
    scalar uniform initial pressure or an explicit cell-centred profile.

    interface_contact_resistance_pa_s_m contains one nonnegative area-specific
    resistance (Pa s/m) per internal interface. It is added to the bulk series
    resistance when that interface lies between adjacent cell centres. A
    nonzero contact resistance at a cell centre is rejected: this formulation
    needs a two-sided interface pressure degree of freedom for that geometry.
    """
    x,s,lam=_validate_layers(layer_boundaries_m,storage_compliance_pa_inv,
                             mobility_m2_pa_s,thickness_m)
    if not isinstance(n_cells,int) or isinstance(n_cells,bool) or n_cells < 2:
        raise ValueError("n_cells must be >= 2")
    if not math.isfinite(dt_s) or dt_s <= 0: raise ValueError("dt_s must be > 0")
    if not isinstance(n_steps,int) or isinstance(n_steps,bool) or n_steps < 1:
        raise ValueError("n_steps must be >= 1")
    if interface_contact_resistance_pa_s_m is None:
        contacts=[0.0]*(len(x)-2)
    else:
        contacts=[float(v) for v in interface_contact_resistance_pa_s_m]
        if len(contacts)!=len(x)-2 or any(not math.isfinite(v) or v<0 for v in contacts):
            raise ValueError("need one finite nonnegative contact resistance per internal interface")
    # A positive contact resistance introduces two massless pressure traces
    # at the physical interface. The associated control volumes are split at
    # the interface, even when it coincides with an original cell centre.
    if any(rc > 0.0 for rc in contacts):
        dx=thickness_m/n_cells
        original_centres=[(i+0.5)*dx for i in range(n_cells)]
        contact_map={x[i+1]:contacts[i] for i in range(len(contacts)) if contacts[i]>0.0}
        nodes=[]
        original_to_node={}
        for i,xc in enumerate(original_centres):
            if any(math.isclose(xc,a,rel_tol=0.0,abs_tol=1e-13*thickness_m)
                   for a in contact_map):
                a=min(contact_map,key=lambda v:abs(v-xc))
                nodes.extend([(a,"minus",i),(a,"plus",i)])
            else:
                nodes.append((xc,"cell",i))
        for a in contact_map:
            if not any(math.isclose(a,xc,rel_tol=0.0,abs_tol=1e-13*thickness_m)
                       for xc in original_centres):
                nodes.extend([(a,"minus",None),(a,"plus",None)])
        nodes.sort(key=lambda z:(z[0],0 if z[1]=="minus" else 1 if z[1]=="plus" else 0))
        # Voronoi capacities: a duplicated interface coordinate splits its
        # control volume exactly at the interface into left/right half volumes.
        unique=sorted(set(z[0] for z in nodes))
        group_bounds={}
        for k,a in enumerate(unique):
            left=0.0 if k==0 else 0.5*(unique[k-1]+a)
            right=thickness_m if k==len(unique)-1 else 0.5*(a+unique[k+1])
            group_bounds[a]=(left,right)
        node_capacity=[]
        for a,side,_ in nodes:
            left,right=group_bounds[a]
            if side=="minus": right=a
            elif side=="plus": left=a
            node_capacity.append(_integrate_piecewise(left,right,x,s))
        m=len(nodes)
        link=[0.0]*(m-1)
        for j in range(m-1):
            xa,sa,_=nodes[j]; xb,sb,_=nodes[j+1]
            if xa==xb:
                link[j]=1.0/contact_map[xa]
            else:
                resistance=_integrate_piecewise(xa,xb,x,lam,lambda v:1.0/v)
                link[j]=1.0/resistance
        left_boundary=1.0/_integrate_piecewise(0.0,nodes[0][0],x,lam,lambda v:1.0/v)
        right_boundary=1.0/_integrate_piecewise(nodes[-1][0],thickness_m,x,lam,lambda v:1.0/v)
        lower=[0.0]*m; upper=[0.0]*m; diagonal=[0.0]*m
        for j in range(m):
            gl=left_boundary if j==0 else link[j-1]
            gr=right_boundary if j==m-1 else link[j]
            lower[j]=-gl if j else 0.0
            upper[j]=-gr if j<m-1 else 0.0
            diagonal[j]=node_capacity[j]/dt_s+gl+gr
        if initial_pressure_profile_pa is None:
            if not math.isfinite(initial_pressure_pa):
                raise ValueError("initial pressure must be finite")
            pn=[float(initial_pressure_pa)]*m
        else:
            original=[float(v) for v in initial_pressure_profile_pa]
            if len(original)!=n_cells or any(not math.isfinite(v) for v in original):
                raise ValueError("initial pressure profile must contain n_cells finite values")
            pn=[]
            for a,side,i in nodes:
                if i is not None:
                    pn.append(original[i])
                else:
                    # Interface lies between original centres: linear interpolation
                    # supplies the initial trace without changing the evolution law.
                    pos=max(0,min(n_cells-2,int(a/dx)))
                    frac=(a-original_centres[pos])/(original_centres[pos+1]-original_centres[pos])
                    pn.append(original[pos]+frac*(original[pos+1]-original[pos]))
        total_capacity=sum(node_capacity)
        times=[0.0]; node_profiles=[pn[:]]
        def project(values):
            out=[]
            for i,xc in enumerate(original_centres):
                matches=[j for j,z in enumerate(nodes) if z[2]==i]
                out.append(sum(values[j] for j in matches)/len(matches))
            return out
        profiles=[project(pn)]
        means=[sum(c0*v for c0,v in zip(node_capacity,pn))/total_capacity]
        fluxes=[0.0]; residuals=[0.0]
        for step in range(1,n_steps+1):
            old=sum(c0*v for c0,v in zip(node_capacity,pn))
            rhs=[node_capacity[j]*pn[j]/dt_s for j in range(m)]
            pn=_solve_tridiagonal(lower,diagonal,upper,rhs)
            out=left_boundary*pn[0]+right_boundary*pn[-1]
            new=sum(c0*v for c0,v in zip(node_capacity,pn))
            times.append(step*dt_s); node_profiles.append(pn[:])
            profiles.append(project(pn)); means.append(new/total_capacity)
            fluxes.append(out); residuals.append(new-old+dt_s*out)
        return {"times_s":times,"profiles_pa":profiles,"node_profiles_pa":node_profiles,
                "node_coordinates_m":[z[0] for z in nodes],
                "node_sides":[z[1] for z in nodes],
                "mean_pressure_pa":means,"boundary_outflow_m_s":fluxes,
                "balance_residual_m":residuals,
                "cell_capacity_pa_inv_m":node_capacity,
                "face_conductance_m_pa_s":[left_boundary]+link+[right_boundary],
                "cell_centres_m":original_centres,
                "interface_contact_resistance_pa_s_m":contacts}
    dx=thickness_m/n_cells
    centres=[(i+0.5)*dx for i in range(n_cells)]
    edges=[i*dx for i in range(n_cells+1)]
    capacity=[_integrate_piecewise(edges[i],edges[i+1],x,s) for i in range(n_cells)]
    conductance=[0.0]*(n_cells+1)
    for interface, rc in zip(x[1:-1],contacts):
        if rc > 0 and any(math.isclose(interface, xc, rel_tol=0.0, abs_tol=1e-13*thickness_m)
                          for xc in centres):
            raise ValueError("nonzero contact resistance at a cell centre requires an interface degree of freedom")
    conductance[0]=1.0/_integrate_piecewise(0.0,centres[0],x,lam,lambda v:1.0/v)
    conductance[n_cells]=1.0/_integrate_piecewise(centres[-1],thickness_m,x,lam,lambda v:1.0/v)
    for j in range(1,n_cells):
        resistance=_integrate_piecewise(centres[j-1],centres[j],x,lam,lambda v:1.0/v)
        resistance += sum(rc for interface,rc in zip(x[1:-1],contacts)
                          if centres[j-1] < interface < centres[j])
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
            "cell_centres_m":centres,"interface_contact_resistance_pa_s_m":contacts}
