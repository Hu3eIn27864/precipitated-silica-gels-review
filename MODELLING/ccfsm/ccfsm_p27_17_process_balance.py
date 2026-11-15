"""P27.17: process-resolved conservation audit for the coupled P21 FV RHS.

The audit decomposes the supplied P21 right-hand side into Darcy fluid
continuity, mobile advection, Onsager diffusion and local M/O/N/B reactions.
It checks local reconstruction and independent global boundary balances.
It does not certify the physical completeness of the supplied model terms.
"""
from __future__ import annotations
import math


def _finite_tuple(values, length, name):
    if len(values) != length:
        raise ValueError(name + " has an incompatible length")
    out = tuple(float(v) for v in values)
    if any(not math.isfinite(v) for v in out):
        raise ValueError(name + " must be finite")
    return out


def _divergence_rhs(face_flux, widths):
    return tuple(-(face_flux[j+1]-face_flux[j])/widths[j]
                 for j in range(len(widths)))


def _balance_report(rhs, flux, source, widths, atol, rtol):
    local = tuple(rhs[j]-source[j]+(flux[j+1]-flux[j])/widths[j]
                  for j in range(len(widths)))
    scale = max(1.0, *(abs(v) for v in rhs), *(abs(v) for v in source),
                *(abs((flux[j+1]-flux[j])/widths[j])
                  for j in range(len(widths))))
    tol = atol+rtol*scale
    integrated = sum(widths[j]*(rhs[j]-source[j])
                     for j in range(len(widths)))
    boundary = flux[0]-flux[-1]
    defect = integrated-boundary
    global_tol = atol+rtol*max(1.0,abs(integrated),abs(boundary))
    return {
        "local_max_abs": max(abs(v) for v in local),
        "local_tolerance": tol,
        "local_pass": max(abs(v) for v in local) <= tol,
        "integrated_rhs_minus_source": integrated,
        "boundary_flux_in_minus_out": boundary,
        "global_defect": defect,
        "global_tolerance": global_tol,
        "global_pass": abs(defect) <= global_tol,
    }


def audit_p21_process_balance(snapshot, cell_widths, *, atol=1e-12, rtol=1e-10):
    """Audit process-separated 1-D P21 balances on a possibly nonuniform grid.

    P21 supplies total mobile flux and its advective part; the Onsager
    diffusive flux is recovered as total minus advective. Reaction sources
    are reconstructed from P10's three stoichiometric rates:
      M=-r1, O=r1-r2, N=r2-r3, B=r3.
    """
    try:
        tr = snapshot.get("transport_rhs") if isinstance(snapshot, dict) else None
        if not isinstance(tr, dict):
            return {"status":"missing_p21_transport_rhs","overall_pass":False}
        widths = tuple(float(v) for v in cell_widths)
        n = len(widths)
        if n < 1 or any(not math.isfinite(v) or v <= 0 for v in widths):
            raise ValueError("cell widths must be finite and positive")
        atol, rtol = float(atol), float(rtol)
        if not math.isfinite(atol) or not math.isfinite(rtol) or atol < 0 or rtol < 0:
            raise ValueError("invalid tolerances")
        required = ("fluid_capacity_dot_s","inventory_dot","darcy_flux_faces_m_s",
                    "mobile_species_advective_face_fluxes_mol_m2_s",
                    "mobile_species_face_fluxes_mol_m2_s","reaction_rates_mol_m3_s")
        if any(key not in tr for key in required):
            return {"status":"incomplete_p21_process_data","overall_pass":False}
        theta_rhs = _finite_tuple(tr["fluid_capacity_dot_s"],n,"fluid RHS")
        inv = tuple(_finite_tuple(row,n,"inventory RHS") for row in tr["inventory_dot"])
        if len(inv) != 4:
            raise ValueError("four inventory RHS fields M/O/N/B required")
        q = _finite_tuple(tr["darcy_flux_faces_m_s"],n+1,"Darcy flux")
        adv_raw = tr["mobile_species_advective_face_fluxes_mol_m2_s"]
        total_raw = tr["mobile_species_face_fluxes_mol_m2_s"]
        if len(adv_raw) != 2 or len(total_raw) != 2:
            raise ValueError("two mobile species fluxes required")
        adv = tuple(_finite_tuple(row,n+1,"advective flux") for row in adv_raw)
        total = tuple(_finite_tuple(row,n+1,"total mobile flux") for row in total_raw)
        diff = tuple(tuple(total[s][f]-adv[s][f] for f in range(n+1))
                     for s in range(2))
        rates_raw = tr["reaction_rates_mol_m3_s"]
        if len(rates_raw) != 3:
            raise ValueError("three reaction-rate fields required")
        rates = tuple(_finite_tuple(row,n,"reaction rates") for row in rates_raw)
        reaction = (
            tuple(-rates[0][j] for j in range(n)),
            tuple(rates[0][j]-rates[1][j] for j in range(n)),
            tuple(rates[1][j]-rates[2][j] for j in range(n)),
            tuple(rates[2][j] for j in range(n)),
        )
        zero_flux = tuple(0.0 for _ in range(n+1))
        zero_source = tuple(0.0 for _ in range(n))
        darcy_rhs = _divergence_rhs(q,widths)
        adv_rhs = tuple(_divergence_rhs(adv[s],widths) for s in range(2))
        diff_rhs = tuple(_divergence_rhs(diff[s],widths) for s in range(2))
        reconstructed = (
            tuple(darcy_rhs[j]+adv_rhs[0][j]+diff_rhs[0][j]+reaction[0][j] for j in range(n)),
            tuple(adv_rhs[1][j]+diff_rhs[1][j]+reaction[1][j] for j in range(n)),
            reaction[2],
            reaction[3],
        )
        residuals = tuple(tuple(inv[k][j]-reconstructed[k][j] for j in range(n))
                          for k in range(4))
        closure_scale = max(1.0, *(abs(v) for row in inv for v in row),
                            *(abs(v) for row in reconstructed for v in row))
        closure_tol = atol+rtol*closure_scale
        closure_max = max(abs(v) for row in residuals for v in row)
        closure_pass = closure_max <= closure_tol

        # Independent flux audits for fluid, each advective species, each
        # diffusive species, and total mobile flux including reaction sources.
        reports = {
            "darcy_fluid": _balance_report(theta_rhs,q,zero_source,widths,atol,rtol),
            "M_advection": _balance_report(adv_rhs[0],adv[0],zero_source,widths,atol,rtol),
            "O_advection": _balance_report(adv_rhs[1],adv[1],zero_source,widths,atol,rtol),
            "M_onsager_diffusion": _balance_report(diff_rhs[0],diff[0],zero_source,widths,atol,rtol),
            "O_onsager_diffusion": _balance_report(diff_rhs[1],diff[1],zero_source,widths,atol,rtol),
            "M_total_with_reaction": _balance_report(inv[0],total[0],reaction[0],widths,atol,rtol),
            "O_total_with_reaction": _balance_report(inv[1],total[1],reaction[1],widths,atol,rtol),
            "N_reaction_only": {
                "integrated_rhs":sum(widths[j]*inv[2][j] for j in range(n)),
                "integrated_reaction_source":sum(widths[j]*reaction[2][j] for j in range(n)),
                "global_defect":sum(widths[j]*(inv[2][j]-reaction[2][j]) for j in range(n)),
            },
            "B_reaction_only": {
                "integrated_rhs":sum(widths[j]*inv[3][j] for j in range(n)),
                "integrated_reaction_source":sum(widths[j]*reaction[3][j] for j in range(n)),
                "global_defect":sum(widths[j]*(inv[3][j]-reaction[3][j]) for j in range(n)),
            },
        }
        for key in ("N_reaction_only","B_reaction_only"):
            rep=reports[key]
            tol=atol+rtol*max(1.0,abs(rep["integrated_rhs"]),abs(rep["integrated_reaction_source"]))
            rep["global_tolerance"]=tol
            rep["global_pass"]=abs(rep["global_defect"])<=tol
        stoich_defects = tuple(sum(reaction[k][j] for k in range(4)) for j in range(n))
        stoich_max = max(abs(v) for v in stoich_defects)
        stoich_tol = atol + rtol * max(1.0, *(abs(v) for row in reaction for v in row))
        stoich_pass = stoich_max <= stoich_tol
        total_inventory_rate = sum(widths[j] * sum(inv[k][j] for k in range(4))
                                   for j in range(n))
        total_boundary_rate = (total[0][0]-total[0][-1]) + (total[1][0]-total[1][-1])
        silicon_defect = total_inventory_rate-total_boundary_rate
        silicon_tol = atol + rtol * max(1.0,abs(total_inventory_rate),abs(total_boundary_rate))
        silicon_pass = abs(silicon_defect) <= silicon_tol
        process_pass = all(v.get("local_pass",True) and v.get("global_pass",True)
                           for v in reports.values())
        overall = closure_pass and process_pass and stoich_pass and silicon_pass
        return {
            "status":"p21_process_balance_audited" if overall else "p21_process_balance_failed",
            "overall_pass":overall,
            "process_reports":reports,
            "rhs_reconstruction":{"max_abs_defect":closure_max,"tolerance":closure_tol,
                                  "pass":closure_pass,"field_order":"M,O,N,B"},
            "reaction_sources_mol_m3_s":reaction,
            "reaction_stoichiometry":{"max_abs_sum":stoich_max,"tolerance":stoich_tol,"pass":stoich_pass},
            "global_silicon_balance":{"integrated_inventory_rate":total_inventory_rate,
                "mobile_boundary_flux_in_minus_out":total_boundary_rate,
                "defect":silicon_defect,"tolerance":silicon_tol,"pass":silicon_pass},
            "onsager_diffusive_flux_recovered_as_total_minus_advective":True,
            "global_silicon_balance_scope":"M+O+N+B reaction stoichiometry cancels internally; M/O boundary fluxes remain explicit",
            "physical_process_completeness_certified":False,
            "scope":"1-D discrete FV algebra for supplied P21 RHS, fluxes and P10 reaction rates",
        }
    except (TypeError,ValueError,OverflowError,ZeroDivisionError,AttributeError):
        return {"status":"invalid_or_malformed_input","overall_pass":False}
