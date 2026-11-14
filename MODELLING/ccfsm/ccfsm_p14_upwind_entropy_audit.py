"""P14: exact finite-volume entropy audit for upwind advection.

For eta(theta,m)=m*(log(m/(theta*c_ref))-1), P14 derives the
semidiscrete balance coupled to theta_dot=-div(q). It isolates reservoir
entropy transport and nonnegative internal upwind entropy production.
This is a component identity, not the complete CCFSM energy theorem.
"""
from __future__ import annotations
import math

def _positive(values, n, name):
    if len(values) != n: raise ValueError(f"{name} must contain {n} values")
    out=tuple(float(v) for v in values)
    if any(not math.isfinite(v) or v<=0 for v in out): raise ValueError(f"{name} must be finite and positive")
    return out

def _finite(values, n, name):
    if len(values) != n: raise ValueError(f"{name} must contain {n} values")
    out=tuple(float(v) for v in values)
    if any(not math.isfinite(v) for v in out): raise ValueError(f"{name} must be finite")
    return out

def _h(c, cref):
    return c*(math.log(c/cref)-1.0)

def p14_upwind_entropy_audit(fluid_capacity, mobile_inventory, darcy_flux_faces_m_s,
                             grid, reservoir_concentrations=(1e-30,1e-30),
                             reference_concentration=1.0):
    """Audit one species: m=theta*c, q positive left-to-right."""
    n,dx=grid.cells,float(grid.spacing_m)
    theta=_positive(fluid_capacity,n,"fluid capacity")
    m=_positive(mobile_inventory,n,"mobile inventory")
    q=_finite(darcy_flux_faces_m_s,n+1,"Darcy face flux")
    cres=_positive(reservoir_concentrations,2,"reservoir concentrations")
    cref=float(reference_concentration)
    if not math.isfinite(cref) or cref<=0: raise ValueError("reference concentration must be positive")
    c=tuple(m[j]/theta[j] for j in range(n))
    face_c=[0.0]*(n+1)
    face_c[0]=cres[0] if q[0]>0 else c[0]
    face_c[-1]=c[-1] if q[-1]>=0 else cres[1]
    for f in range(1,n): face_c[f]=c[f-1] if q[f]>=0 else c[f]
    flux=tuple(q[f]*face_c[f] for f in range(n+1))
    theta_dot=tuple(-(q[j+1]-q[j])/dx for j in range(n))
    m_dot=tuple(-(flux[j+1]-flux[j])/dx for j in range(n))
    entropy_rate=dx*sum(math.log(c[j]/cref)*m_dot[j]-c[j]*theta_dot[j] for j in range(n))
    boundary=q[0]*_h(face_c[0],cref)-q[-1]*_h(face_c[-1],cref)
    internal=0.0
    for f in range(1,n):
        qf,cl,cr=q[f],c[f-1],c[f]
        if qf>0: internal+=qf*(cr-cl-cl*math.log(cr/cl))
        elif qf<0: internal+=(-qf)*(cl-cr-cr*math.log(cl/cr))
    residual=entropy_rate-(boundary-internal)
    scale=max(1.0,abs(entropy_rate),abs(boundary),abs(internal))
    return {"mobile_entropy_j_m2":dx*sum(theta[j]*c[j]*(math.log(c[j]/cref)-1) for j in range(n)),
      "mobile_entropy_rate_w_m2":entropy_rate,
      "advective_boundary_entropy_power_w_m2":boundary,
      "upwind_internal_entropy_production_w_m2":internal,
      "upwind_internal_entropy_production_nonnegative":internal>=0,
      "entropy_balance_residual_w_m2":residual,
      "entropy_balance_identity_verified":abs(residual)<=1e-11*scale,
      "concentration_mol_m3":c,"upwind_face_concentrations_mol_m3":tuple(face_c),
      "advective_inventory_fluxes_mol_m2_s":flux,
      "fluid_capacity_dot_s":theta_dot,"mobile_inventory_dot_mol_m3_s":m_dot,
      "scope":"ideal mobile mixing entropy; advection only; reaction, diffusion, Darcy energy and mechanics excluded"}