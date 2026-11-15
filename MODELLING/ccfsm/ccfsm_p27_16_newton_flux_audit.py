"""P27.16: Newton invariant-domain integration and FV flux-balance audit."""
from __future__ import annotations
import math
from ccfsm_p27_15_coupled_invariant_domain import audit_coupled_fv_invariant_domain

def limit_newton_direction(fluid_capacity, inventories, delta_theta, delta_inventories, *, safety_fraction=0.95):
    """Limit one complete Newton direction with P27.15's shared scalar alpha."""
    n=len(fluid_capacity)
    if len(delta_theta)!=n or len(inventories)!=4 or len(delta_inventories)!=4:
        return {"status":"invalid_or_malformed_input","overall_pass":False}
    if any(len(row)!=n for row in inventories) or any(len(row)!=n for row in delta_inventories):
        return {"status":"invalid_or_malformed_input","overall_pass":False}
    return audit_coupled_fv_invariant_domain(fluid_capacity,inventories,delta_theta,delta_inventories,1.0,
        safety_fraction=safety_fraction,theta_lower=0.0,inventory_lower=0.0)

def audit_fv_flux_balance(rhs_fields, face_flux_fields, source_fields, cell_widths, *, atol=1e-12, rtol=1e-10):
    """Audit rhs=-div(face_flux)+source and its global telescoping identity."""
    try:
        n=len(cell_widths)
        if n<1 or len(rhs_fields)<1 or not(len(rhs_fields)==len(face_flux_fields)==len(source_fields)):
            raise ValueError("incompatible field counts")
        widths=tuple(float(v) for v in cell_widths)
        if any(not math.isfinite(v) or v<=0 for v in widths): raise ValueError("invalid cell widths")
        atol,rtol=float(atol),float(rtol)
        if not math.isfinite(atol) or not math.isfinite(rtol) or atol<0 or rtol<0: raise ValueError("invalid tolerances")
        reports=[]; overall=True
        for k,(rhs,flux,source) in enumerate(zip(rhs_fields,face_flux_fields,source_fields)):
            if len(rhs)!=n or len(source)!=n or len(flux)!=n+1: raise ValueError("field shape mismatch")
            rr=tuple(float(v) for v in rhs); ff=tuple(float(v) for v in flux); ss=tuple(float(v) for v in source)
            if any(not math.isfinite(v) for v in rr+ff+ss): raise ValueError("nonfinite field")
            local=tuple(rr[j]-ss[j]+(ff[j+1]-ff[j])/widths[j] for j in range(n))
            scale=max(1.0,*(abs(v) for v in rr),*(abs(v) for v in ss),*(abs((ff[j+1]-ff[j])/widths[j]) for j in range(n)))
            lt=atol+rtol*scale; lok=max(abs(v) for v in local)<=lt
            integrated=sum(widths[j]*(rr[j]-ss[j]) for j in range(n)); boundary=ff[0]-ff[-1]
            defect=integrated-boundary; gt=atol+rtol*max(1.0,abs(integrated),abs(boundary)); gok=abs(defect)<=gt
            reports.append({"field_index":k,"local_balance_max_abs":max(abs(v) for v in local),
                "local_tolerance":lt,"local_balance_pass":lok,"integrated_rhs_minus_source":integrated,
                "boundary_flux_in_minus_out":boundary,"global_balance_defect":defect,
                "global_tolerance":gt,"global_balance_pass":gok})
            overall=overall and lok and gok
        return {"status":"flux_balance_audited" if overall else "flux_balance_failed","overall_pass":overall,
            "fields":tuple(reports),"sign_convention":"positive flux left-to-right; rhs=-div(flux)+source",
            "conservation_scope":"discrete 1-D finite-volume algebra for supplied RHS, fluxes and sources",
            "physical_conservation_certified":False}
    except (TypeError,ValueError,OverflowError,ZeroDivisionError):
        return {"status":"invalid_or_malformed_input","overall_pass":False}

def audit_p21_flux_balance(snapshot, cell_widths, cell_sources, *, atol=1e-12, rtol=1e-10):
    """Audit P21 theta/M/O flux divergence; N/B are source-only in P21."""
    try:
        if not isinstance(snapshot,dict) or not isinstance(snapshot.get("transport_rhs"),dict):
            return {"status":"missing_p21_transport_rhs","overall_pass":False}
        tr=snapshot["transport_rhs"]
        required=("fluid_capacity_dot_s","inventory_dot","darcy_flux_faces_m_s","mobile_species_face_fluxes_mol_m2_s")
        if any(k not in tr for k in required): return {"status":"incomplete_p21_flux_data","overall_pass":False}
        n=len(cell_widths)
        if len(cell_sources)!=5 or any(len(row)!=n for row in cell_sources):
            return {"status":"invalid_or_malformed_input","overall_pass":False}
        mobile=tuple(tuple(row) for row in tr["mobile_species_face_fluxes_mol_m2_s"])
        if len(mobile)!=2: return {"status":"incomplete_p21_flux_data","overall_pass":False}
        zero=tuple(0.0 for _ in range(n+1))
        return audit_fv_flux_balance((tr["fluid_capacity_dot_s"],)+tuple(tr["inventory_dot"]),
            (tuple(tr["darcy_flux_faces_m_s"]),mobile[0],mobile[1],zero,zero),
            cell_sources,cell_widths,atol=atol,rtol=rtol)
    except (TypeError,ValueError,OverflowError,ZeroDivisionError):
        return {"status":"invalid_or_malformed_input","overall_pass":False}
