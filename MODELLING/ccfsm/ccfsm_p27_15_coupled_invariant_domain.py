"""P27.15: coupled FV invariant-domain limiter and acceptance audit."""
from __future__ import annotations
import math

def _finite(value, name):
    x=float(value)
    if not math.isfinite(x): raise ValueError(name+" must be finite")
    return x

def audit_coupled_fv_invariant_domain(fluid_capacity, inventories,
        fluid_capacity_rhs, inventory_rhs, dt_s, *, safety_fraction=0.95,
        theta_lower=0.0, inventory_lower=0.0):
    """Apply one common fraction-to-boundary factor to theta and M/O/N/B."""
    try:
        n=len(fluid_capacity)
        if n<1 or len(fluid_capacity_rhs)!=n or len(inventories)!=4 or len(inventory_rhs)!=4:
            raise ValueError("expected theta and four species arrays")
        if any(len(row)!=n for row in inventories) or any(len(row)!=n for row in inventory_rhs):
            raise ValueError("species arrays must have shape (4,cells)")
        dt=_finite(dt_s,"dt_s"); safety=_finite(safety_fraction,"safety_fraction")
        tl=_finite(theta_lower,"theta_lower"); il=_finite(inventory_lower,"inventory_lower")
        if dt<=0 or not 0<safety<1 or not 0<=tl<1 or il<0:
            return {"status":"invalid_controls","overall_pass":False}
        theta=tuple(_finite(x,"theta") for x in fluid_capacity)
        fields=tuple(tuple(_finite(x,"inventory") for x in row) for row in inventories)
        tr=tuple(_finite(x,"theta_rhs") for x in fluid_capacity_rhs)
        ir=tuple(tuple(_finite(x,"inventory_rhs") for x in row) for row in inventory_rhs)
        if any(not tl<x<=1 for x in theta) or any(x<=il for row in fields for x in row):
            return {"status":"initial_state_outside_invariant_domain","overall_pass":False,"limiting_factor":0.0}
        alpha=1.0; active=[]
        def restrict(label,x,delta,lower,upper=None):
            nonlocal alpha
            bound=None
            if delta<0: bound=safety*(x-lower)/(-delta)
            elif delta>0 and upper is not None: bound=safety*(upper-x)/delta
            if bound is not None:
                if bound<alpha: alpha=max(0.0,bound); active[:]=[label]
                elif math.isclose(bound,alpha,rel_tol=1e-14,abs_tol=1e-15): active.append(label)
        for j,(x,r) in enumerate(zip(theta,tr)): restrict("theta[%d]"%j,x,dt*r,tl,1.0)
        names=("M","O","N","B")
        for s,name in enumerate(names):
            for j,(x,r) in enumerate(zip(fields[s],ir[s])): restrict("%s[%d]"%(name,j),x,dt*r,il)
        alpha=min(1.0,max(0.0,alpha))
        if alpha <= 0.0:
            return {"status":"no_positive_admissible_step","overall_pass":False,
                    "limiting_factor":0.0,"active_constraints":tuple(active)}
        tn=tuple(x+alpha*dt*r for x,r in zip(theta,tr))
        fn=tuple(tuple(x+alpha*dt*r for x,r in zip(fields[s],ir[s])) for s in range(4))
        ok=all(math.isfinite(x) and tl<x<=1 for x in tn) and all(math.isfinite(x) and x>il for row in fn for x in row)
        if not ok: return {"status":"no_positive_admissible_step","overall_pass":False,"limiting_factor":alpha,"active_constraints":tuple(active)}
        full=alpha>=1.0
        return {"status":"full_step_admissible" if full else "limited_step_admissible",
            "overall_pass":True,"limiting_factor":alpha,"accepted_dt_s":alpha*dt,
            "full_step_accepted":full,"active_constraints":tuple(active),
            "fluid_capacity":tn,"inventories":fn,"species_order":names,
            "all_fields_share_one_factor":True,
            "conservative_flux_balance_certified":False,"implicit_residual_converged":False,
            "time_step_stability_certified":False,"physical_ccfsm_positivity_certified":False}
    except (TypeError,ValueError,OverflowError,ZeroDivisionError):
        return {"status":"invalid_or_malformed_input","overall_pass":False}

def audit_p21_rhs_step(snapshot, fluid_capacity, inventories, dt_s, **kwargs):
    """Extract P21 transport RHS and audit its explicit admissible update."""
    if not isinstance(snapshot,dict) or not isinstance(snapshot.get("transport_rhs"),dict):
        return {"status":"missing_p21_transport_rhs","overall_pass":False}
    tr=snapshot["transport_rhs"]
    if "fluid_capacity_dot_s" not in tr or "inventory_dot" not in tr:
        return {"status":"incomplete_p21_transport_rhs","overall_pass":False}
    return audit_coupled_fv_invariant_domain(fluid_capacity,inventories,
        tr["fluid_capacity_dot_s"],tr["inventory_dot"],dt_s,**kwargs)
