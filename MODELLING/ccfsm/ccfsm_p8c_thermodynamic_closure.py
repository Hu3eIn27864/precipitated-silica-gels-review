"""CCFSM P8c: thermodynamic variable-capacity chemo-hydraulic closure.

The free-energy derivative with respect to fluid capacity is p-Pi_osm,
while Darcy mobility is driven by the mechanical/storage pressure p.
Ideal-mixture Gibbs-Duhem cancellation is the reason these are not
interchanged. This is a semidiscrete reference kernel, not a full PDE solver.
"""
from __future__ import annotations
import math
from ccfsm_p2_chemical_affinity import R_GAS
from ccfsm_p8b_open_drainage import p8b_hydraulic_rhs


def _positive(x, name):
    x=float(x)
    if not math.isfinite(x) or x<=0:
        raise ValueError(f"{name} must be finite and positive")
    return x


def _logmean(x,y):
    if x<=0 or y<=0:
        raise ValueError("activities must be positive")
    if x==y:
        return x
    if abs(x-y)<=1e-8*max(x,y):
        return 0.5*(x+y)
    return (x-y)/(math.log(x)-math.log(y))


def p8c_cell_thermodynamics(theta, pressure_pa, mobile_inventories,
                            network_inventories, chemistry,
                            reference_capacity, reference_pressure_pa,
                            storage_per_pa):
    """Return local energy, chemical potentials and fluid conjugates."""
    theta=_positive(theta,"theta")
    storage=_positive(storage_per_pa,"storage_per_pa")
    tref=_positive(reference_capacity,"reference_capacity")
    p=float(pressure_pa); pref=float(reference_pressure_pa)
    if not math.isfinite(p) or not math.isfinite(pref):
        raise ValueError("pressures must be finite")
    if len(mobile_inventories)!=2 or len(network_inventories)!=2:
        raise ValueError("two mobile and two network inventories required")
    inv=tuple(_positive(v,"inventory") for v in
              (*mobile_inventories,*network_inventories))
    mm,mo,sn,sb=inv
    rt=R_GAS*_positive(chemistry.temperature_k,"temperature")
    cref=_positive(chemistry.reference_concentration,"reference concentration")
    gamma=tuple(float(v) for v in chemistry.activity_coefficients)
    if len(gamma)!=4 or any(not math.isfinite(v) or v<=0 for v in gamma):
        raise ValueError("four positive activity coefficients required")
    eq=tuple(float(v) for v in chemistry.equilibrium_constants)
    if len(eq)!=3 or any(not math.isfinite(v) or v<=0 for v in eq):
        raise ValueError("three positive equilibrium constants required")
    activities=(gamma[0]*mm/(theta*cref),gamma[1]*mo/(theta*cref),
                gamma[2]*sn/cref,gamma[3]*sb/cref)
    mu0=[0.0]
    for k in eq:
        mu0.append(mu0[-1]-rt*math.log(k))
    mu=tuple(mu0[i]+rt*math.log(activities[i]) for i in range(4))
    osmotic=rt*(mm+mo)/theta
    conjugate=p-osmotic
    hydraulic=pref*(theta-tref)+(theta-tref)**2/(2.0*storage)
    mixing=sum(inv[i]*(mu0[i]+rt*(math.log(activities[i])-1.0))
               for i in range(4))
    return {
        "free_energy_j_m3_reference":hydraulic+mixing,
        "chemical_potentials_j_mol":mu,
        "activities":activities,
        "pore_pressure_pa":p,
        "osmotic_pressure_pa":osmotic,
        "fluid_energy_conjugate_pa":conjugate,
        "hydraulic_energy_j_m3_reference":hydraulic,
        "mixing_energy_j_m3_reference":mixing,
    }


def p8c_coupled_rhs(inventories, pressure_pa, grid, hydraulic_parameters,
                    diffusivities_m2_s, chemistry, external_pressure_pa,
                    external_concentrations_left=(0.0,0.0),
                    external_concentrations_right=(0.0,0.0)):
    """Thermodynamic reaction/diffusion with P8b open hydraulic boundaries."""
    n,dx=grid.cells,grid.spacing_m
    if len(inventories)!=4:
        raise ValueError("four inventory fields M/O/N/B required")
    fields=[]
    for i,f in enumerate(inventories):
        if len(f)!=n: raise ValueError("inventory field length mismatch")
        vals=tuple(float(v) for v in f)
        if any(not math.isfinite(v) or v<=0 for v in vals):
            raise ValueError("P8c interior inventories must be positive")
        fields.append(vals)
    theta,pdot,tdot,q=p8b_hydraulic_rhs(
        pressure_pa,grid,hydraulic_parameters,external_pressure_pa)
    d=tuple(float(v) for v in diffusivities_m2_s)
    if len(d)!=2 or any(not math.isfinite(v) or v<0 for v in d):
        raise ValueError("two nonnegative diffusivities required")
    cL=tuple(float(v) for v in external_concentrations_left)
    cR=tuple(float(v) for v in external_concentrations_right)
    if len(cL)!=2 or len(cR)!=2 or any(
        not math.isfinite(v) or v<0 for v in (*cL,*cR)):
        raise ValueError("external concentrations must be nonnegative pairs")
    cref=_positive(chemistry.reference_concentration,"reference concentration")
    rt=R_GAS*_positive(chemistry.temperature_k,"temperature")
    rates_k=tuple(float(v) for v in chemistry.rate_constants_s)
    eq=tuple(float(v) for v in chemistry.equilibrium_constants)
    if len(rates_k)!=3 or any(not math.isfinite(v) or v<0 for v in rates_k):
        raise ValueError("three nonnegative reaction rates required")
    if len(eq)!=3 or len(chemistry.activity_coefficients)!=4:
        raise ValueError("chemistry parameter dimensions invalid")

    rhs=[[0.0]*n for _ in range(4)]
    cell_data=[]
    reaction_diss=[0.0]*n
    for j in range(n):
        td=p8c_cell_thermodynamics(theta[j],float(pressure_pa[j]),
             (fields[0][j],fields[1][j]),(fields[2][j],fields[3][j]),
             chemistry,hydraulic_parameters.theta_reference[j],
             hydraulic_parameters.pressure_reference_pa,
             hydraulic_parameters.storage_per_pa[j])
        mu=td["chemical_potentials_j_mol"]
        a=td["activities"]
        rr=[]
        for i in range(3):
            affinity=mu[i]-mu[i+1]
            y=a[i+1]/eq[i]
            rate=rates_k[i]*cref*_logmean(a[i],y)*affinity/rt
            rr.append(rate)
            reaction_diss[j]+=rate*affinity
        r1,r2,r3=rr
        rhs[0][j]-=r1
        rhs[1][j]+=r1-r2
        rhs[2][j]+=r2-r3
        rhs[3][j]+=r3
        cell_data.append(td)

    concentrations=(tuple(fields[0][j]/theta[j] for j in range(n)),
                    tuple(fields[1][j]/theta[j] for j in range(n)))
    boundary=[]
    for species in range(2):
        c=concentrations[species]
        flux=[0.0]*(n+1)
        ql,qr=q[0],q[-1]
        cup_l=cL[species] if ql>0 else c[0]
        cup_r=c[-1] if qr>=0 else cR[species]
        flux[0]=ql*cup_l-theta[0]*d[species]*(c[0]-cL[species])/(0.5*dx)
        flux[-1]=qr*cup_r-theta[-1]*d[species]*(cR[species]-c[-1])/(0.5*dx)
        for face in range(1,n):
            l,r=face-1,face
            qf=q[face]
            cup=c[l] if qf>=0 else c[r]
            tf=0.5*(theta[l]+theta[r])
            flux[face]=qf*cup-tf*d[species]*(c[r]-c[l])/dx
        for j in range(n):
            rhs[species][j]-=(flux[j+1]-flux[j])/dx
        boundary.append((flux[0],flux[-1]))

    return {
        "inventory_dot":tuple(tuple(f) for f in rhs),
        "pressure_dot_pa_s":pdot,
        "fluid_capacity":theta,
        "fluid_capacity_dot_s":tdot,
        "darcy_flux_faces_m_s":q,
        "cell_thermodynamics":tuple(cell_data),
        "reaction_dissipation_w_m3_reference":tuple(reaction_diss),
        "mobile_species_boundary_fluxes_mol_m2_s":tuple(boundary),
    }
