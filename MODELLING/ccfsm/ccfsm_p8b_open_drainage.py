"""CCFSM P8b: open-boundary drainage and mobile silicon export.

1D semidiscrete finite-volume reference model. External pressure and external
mobile-species concentrations are prescribed reservoir data. N/B remain
immobilized. No moving interface or capillary constitutive law is included.
"""
from __future__ import annotations
import math
from ccfsm_p8a_hydraulic_pressure import P8aHydraulicParameters
from ccfsm_p8_variable_capacity import P8Grid


def _finite(values, n, name, positive=False, nonnegative=False):
    if len(values) != n:
        raise ValueError(f"{name} must contain {n} values")
    out = tuple(float(v) for v in values)
    if any(not math.isfinite(v) for v in out):
        raise ValueError(f"{name} must be finite")
    if positive and any(v <= 0 for v in out):
        raise ValueError(f"{name} must be positive")
    if nonnegative and any(v < 0 for v in out):
        raise ValueError(f"{name} must be nonnegative")
    return out


def p8b_hydraulic_rhs(pressure_pa, grid, parameters, external_pressure_pa):
    n, dx = grid.cells, grid.spacing_m
    p = _finite(pressure_pa, n, "pressure")
    storage, permeability, theta0, pref = parameters.validate(n)
    pext = float(external_pressure_pa)
    if not math.isfinite(pext):
        raise ValueError("external pressure must be finite")
    theta = tuple(theta0[j] + storage[j]*(p[j]-pref) for j in range(n))
    if any(v <= 0 for v in theta):
        raise ValueError("pressure state produces nonpositive fluid capacity")

    q = [0.0]*(n+1)
    half = 0.5*dx
    q[0] = -permeability[0]*(p[0]-pext)/half
    q[-1] = -permeability[-1]*(pext-p[-1])/half
    theta_dot = [0.0]*n
    for face in range(1,n):
        l,r=face-1,face
        kf=2*permeability[l]*permeability[r]/(permeability[l]+permeability[r])
        q[face]=-kf*(p[r]-p[l])/dx
    for j in range(n):
        theta_dot[j]=-(q[j+1]-q[j])/dx
    pdot=tuple(theta_dot[j]/storage[j] for j in range(n))
    return theta,pdot,tuple(theta_dot),tuple(q)


def p8b_coupled_rhs(inventories, pressure_pa, grid, parameters,
                    diffusivities_m2_s, chemistry, external_pressure_pa,
                    external_concentrations_left=(0.0,0.0),
                    external_concentrations_right=(0.0,0.0)):
    if len(inventories)!=4:
        raise ValueError("four inventories M/O/N/B are required")
    fields=tuple(_finite(f,grid.cells,f"inventory {i}",nonnegative=True)
                 for i,f in enumerate(inventories))
    theta,pdot,theta_dot,q=p8b_hydraulic_rhs(
        pressure_pa,grid,parameters,external_pressure_pa)
    d=_finite(diffusivities_m2_s,2,"diffusivities",nonnegative=True)
    cL=_finite(external_concentrations_left,2,"left external concentrations",
               nonnegative=True)
    cR=_finite(external_concentrations_right,2,"right external concentrations",
               nonnegative=True)
    n,dx=grid.cells,grid.spacing_m
    cref=float(chemistry.reference_concentration)
    if not math.isfinite(cref) or cref<=0:
        raise ValueError("reference concentration must be positive")
    gamma=chemistry.activity_coefficients
    rates=chemistry.rate_constants_s
    eq=chemistry.equilibrium_constants
    rhs=[[0.0]*n for _ in range(4)]
    for j in range(n):
        a=(gamma[0]*fields[0][j]/(theta[j]*cref),
           gamma[1]*fields[1][j]/(theta[j]*cref),
           gamma[2]*fields[2][j]/cref,
           gamma[3]*fields[3][j]/cref)
        r=tuple(k*cref*(a[i]-a[i+1]/K)
                for i,(k,K) in enumerate(zip(rates,eq)))
        r1,r2,r3=r
        rhs[0][j]+=-r1
        rhs[1][j]+=r1-r2
        rhs[2][j]+=r2-r3
        rhs[3][j]+=r3

    concentrations=(
        tuple(fields[0][j]/theta[j] for j in range(n)),
        tuple(fields[1][j]/theta[j] for j in range(n)))
    boundary_fluxes=[]
    for species in range(2):
        c=concentrations[species]
        # Oriented flux positive in +x direction. Upwind reservoir value
        # is selected only when the flow enters the gel.
        ql,qr=q[0],q[-1]
        cup_l=cL[species] if ql>0 else c[0]
        cup_r=c[-1] if qr>=0 else cR[species]
        fl=ql*cup_l-theta[0]*d[species]*(c[0]-cL[species])/(0.5*dx)
        fr=qr*cup_r-theta[-1]*d[species]*(cR[species]-c[-1])/(0.5*dx)
        flux=[0.0]*(n+1)
        flux[0],flux[-1]=fl,fr
        for face in range(1,n):
            l,r=face-1,face
            qf=q[face]
            cup=c[l] if qf>=0 else c[r]
            thetaf=0.5*(theta[l]+theta[r])
            flux[face]=qf*cup-thetaf*d[species]*(c[r]-c[l])/dx
        for j in range(n):
            rhs[species][j]-=(flux[j+1]-flux[j])/dx
        boundary_fluxes.append((fl,fr))

    return {
        "inventory_dot":tuple(tuple(f) for f in rhs),
        "pressure_dot_pa_s":pdot,
        "fluid_capacity":theta,
        "fluid_capacity_dot_s":theta_dot,
        "darcy_flux_faces_m_s":q,
        "mobile_species_boundary_fluxes_mol_m2_s":tuple(boundary_fluxes),
        "net_outward_fluid_flux_m_s":q[-1]-q[0],
        "net_outward_mobile_si_flux_mol_m2_s":sum(fr-fl for fl,fr in boundary_fluxes),
    }


def p8b_pressure_dissipation(pressure_pa,grid,parameters,external_pressure_pa):
    p=_finite(pressure_pa,grid.cells,"pressure")
    _,k,_,_=parameters.validate(grid.cells)
    pe=float(external_pressure_pa)
    if not math.isfinite(pe):
        raise ValueError("external pressure must be finite")
    dx=grid.spacing_m
    value=k[0]*(p[0]-pe)**2/(0.5*dx)+k[-1]*(pe-p[-1])**2/(0.5*dx)
    for face in range(1,grid.cells):
        l,r=face-1,face
        kf=2*k[l]*k[r]/(k[l]+k[r])
        value+=kf*((p[r]-p[l])/dx)**2*dx
    return value
