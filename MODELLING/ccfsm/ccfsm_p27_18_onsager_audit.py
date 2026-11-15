"""P27.18: independent Onsager flux and dissipation reconstruction audit."""
from __future__ import annotations
import math


def _logmean(a,b):
    if not (math.isfinite(a) and math.isfinite(b) and a>0 and b>0):
        raise ValueError("logarithmic-mean arguments must be finite and positive")
    if a == b:
        return a
    z=(b-a)/(b+a)
    if abs(z)<1e-7:
        # Stable expansion: atanh(z)/z = 1+z²/3+z⁴/5+...
        ratio=1.0+z*z/3.0+z**4/5.0
        return 0.5*(a+b)/ratio
    return (b-a)/(math.log(b)-math.log(a))


def _tuple(values,n,name,positive=False,nonnegative=False):
    if len(values)!=n: raise ValueError(name+" length mismatch")
    out=tuple(float(v) for v in values)
    if any(not math.isfinite(v) for v in out): raise ValueError(name+" must be finite")
    if positive and any(v<=0 for v in out): raise ValueError(name+" must be positive")
    if nonnegative and any(v<0 for v in out): raise ValueError(name+" must be nonnegative")
    return out


def reconstruct_onsager_species_flux(concentration, chemical_potential, theta,
        diffusivity, rt, dx, reservoir_concentration_left,
        reservoir_concentration_right, reservoir_mu_left, reservoir_mu_right):
    """Reconstruct n+1 oriented fluxes and integrated dissipation for one species."""
    n=len(theta)
    c=_tuple(concentration,n,"concentration",positive=True)
    mu=_tuple(chemical_potential,n,"chemical potential")
    th=_tuple(theta,n,"fluid capacity",positive=True)
    d=float(diffusivity); rt=float(rt); dx=float(dx)
    if not math.isfinite(d) or d<0 or not math.isfinite(rt) or rt<=0 or not math.isfinite(dx) or dx<=0:
        raise ValueError("invalid diffusivity, RT or spacing")
    crl=float(reservoir_concentration_left); crr=float(reservoir_concentration_right)
    mul=float(reservoir_mu_left); mur=float(reservoir_mu_right)
    if not all(math.isfinite(v) for v in (crl,crr,mul,mur)) or crl<=0 or crr<=0:
        raise ValueError("invalid reservoir data")
    flux=[0.0]*(n+1); diss=0.0
    if d==0:
        return {"diffusive_face_flux":tuple(flux),"dissipation_w_m2":0.0}
    # Boundary half cells: oriented positive from left to right.
    ml=th[0]*d*_logmean(crl,c[0])/rt
    gl=(mu[0]-mul)/(0.5*dx)
    flux[0]=-ml*gl
    diss+=ml*gl*gl*(0.5*dx)
    mr=th[-1]*d*_logmean(c[-1],crr)/rt
    gr=(mur-mu[-1])/(0.5*dx)
    flux[-1]=-mr*gr
    diss+=mr*gr*gr*(0.5*dx)
    for f in range(1,n):
        mf=0.5*(th[f-1]+th[f])*d*_logmean(c[f-1],c[f])/rt
        grad=(mu[f]-mu[f-1])/dx
        flux[f]=-mf*grad
        diss+=mf*grad*grad*dx
    return {"diffusive_face_flux":tuple(flux),"dissipation_w_m2":diss}


def audit_onsager_diffusion(concentrations, chemical_potentials, fluid_capacity,
        diffusivities_m2_s, rt_j_mol, dx_m, reservoir_concentrations_left,
        reservoir_concentrations_right, reservoir_mu_left, reservoir_mu_right,
        stored_total_fluxes, stored_advective_fluxes, stored_dissipation_w_m2,
        *, atol=1e-12, rtol=1e-10):
    """Compare independent chemical-potential reconstruction to stored P13/P21 data."""
    try:
        if len(fluid_capacity)<1: raise ValueError("empty grid")
        n=len(fluid_capacity)
        th=_tuple(fluid_capacity,n,"fluid capacity",positive=True)
        d=_tuple(diffusivities_m2_s,2,"diffusivities",nonnegative=True)
        rt=float(rt_j_mol); dx=float(dx_m)
        if not math.isfinite(rt) or rt<=0 or not math.isfinite(dx) or dx<=0:
            raise ValueError("invalid RT or spacing")
        atol=float(atol); rtol=float(rtol)
        if not math.isfinite(atol) or not math.isfinite(rtol) or atol<0 or rtol<0:
            raise ValueError("invalid tolerances")
        if any(len(x)!=2 for x in (concentrations,chemical_potentials,
                reservoir_concentrations_left,reservoir_concentrations_right,
                reservoir_mu_left,reservoir_mu_right,stored_total_fluxes,
                stored_advective_fluxes,stored_dissipation_w_m2)):
            raise ValueError("two mobile species required")
        reports=[]; overall=True
        for s in range(2):
            c=_tuple(concentrations[s],n,"concentration",positive=True)
            mu=_tuple(chemical_potentials[s],n,"chemical potential")
            total=_tuple(stored_total_fluxes[s],n+1,"stored total flux")
            adv=_tuple(stored_advective_fluxes[s],n+1,"stored advective flux")
            stored_diss=float(stored_dissipation_w_m2[s])
            if not math.isfinite(stored_diss) or stored_diss<0: raise ValueError("invalid stored dissipation")
            rec=reconstruct_onsager_species_flux(c,mu,th,d[s],rt,dx,
                reservoir_concentrations_left[s],reservoir_concentrations_right[s],
                reservoir_mu_left[s],reservoir_mu_right[s])
            observed=tuple(total[f]-adv[f] for f in range(n+1))
            expected=rec["diffusive_face_flux"]
            defects=tuple(observed[f]-expected[f] for f in range(n+1))
            scale=max(1.0,*(abs(v) for v in observed),*(abs(v) for v in expected))
            tol=atol+rtol*scale
            flux_max=max(abs(v) for v in defects)
            diss=rec["dissipation_w_m2"]
            dtol=atol+rtol*max(1.0,abs(diss),abs(stored_diss))
            derror=stored_diss-diss
            nonnegative=diss>=0.0
            passed=flux_max<=tol and abs(derror)<=dtol and nonnegative
            reports.append({"species_index":s,"reconstructed_diffusive_flux":expected,
                "observed_total_minus_advection_flux":observed,"face_flux_max_abs_error":flux_max,
                "face_flux_tolerance":tol,"face_flux_pass":flux_max<=tol,
                "reconstructed_dissipation_w_m2":diss,
                "stored_dissipation_w_m2":stored_diss,"dissipation_error":derror,
                "dissipation_tolerance":dtol,"dissipation_nonnegative":nonnegative,
                "dissipation_pass":abs(derror)<=dtol,"overall_pass":passed})
            overall=overall and passed
        return {"status":"onsager_independent_audit_passed" if overall else "onsager_independent_audit_failed",
            "overall_pass":overall,"species_reports":tuple(reports),
            "reconstruction":"logarithmic-mean Onsager mobility on interior and reservoir half-cell faces",
            "boundary_faces_included":True,"physical_onsager_law_certified":False,
            "scope":"independent algebraic reconstruction from supplied concentrations, chemical potentials and coefficients"}
    except (TypeError,ValueError,OverflowError,ZeroDivisionError,AttributeError):
        return {"status":"invalid_or_malformed_input","overall_pass":False}


def audit_p13_onsager_snapshot(snapshot, *, atol=1e-12, rtol=1e-10):
    """Run P27.18 directly on the diagnostic payload emitted by P13."""
    if not isinstance(snapshot,dict):
        return {"status":"invalid_or_malformed_input","overall_pass":False}
    keys=("mobile_species_concentration_mol_m3","mobile_species_chemical_potential_j_mol",
          "onsager_fluid_capacity","onsager_diffusivities_m2_s","onsager_rt_j_mol",
          "onsager_grid_spacing_m","onsager_reservoir_concentration_left_mol_m3",
          "onsager_reservoir_concentration_right_mol_m3",
          "onsager_reservoir_chemical_potential_left_j_mol",
          "onsager_reservoir_chemical_potential_right_j_mol",
          "mobile_species_face_fluxes_mol_m2_s",
          "mobile_species_advective_face_fluxes_mol_m2_s",
          "mobile_species_onsager_diffusive_dissipation_w_m2")
    if any(k not in snapshot for k in keys):
        return {"status":"incomplete_p13_onsager_diagnostics","overall_pass":False}
    return audit_onsager_diffusion(
        snapshot["mobile_species_concentration_mol_m3"],
        snapshot["mobile_species_chemical_potential_j_mol"],
        snapshot["onsager_fluid_capacity"],snapshot["onsager_diffusivities_m2_s"],
        snapshot["onsager_rt_j_mol"],snapshot["onsager_grid_spacing_m"],
        snapshot["onsager_reservoir_concentration_left_mol_m3"],
        snapshot["onsager_reservoir_concentration_right_mol_m3"],
        snapshot["onsager_reservoir_chemical_potential_left_j_mol"],
        snapshot["onsager_reservoir_chemical_potential_right_j_mol"],
        snapshot["mobile_species_face_fluxes_mol_m2_s"],
        snapshot["mobile_species_advective_face_fluxes_mol_m2_s"],
        snapshot["mobile_species_onsager_diffusive_dissipation_w_m2"],
        atol=atol,rtol=rtol)
