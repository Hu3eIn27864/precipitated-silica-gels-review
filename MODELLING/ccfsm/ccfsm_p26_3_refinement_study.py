"""P26.3: refinement, extrema, positivity and sensitivity study for P26.2."""
from __future__ import annotations
import csv, json, math
from pathlib import Path
from ccfsm_p26_2_quadratic_projection import moments, project_quadratic_moments, quadratic_minimum, limit_quadratic
_GX=(-0.9061798459386640,-0.5384693101056831,0.0,0.5384693101056831,0.9061798459386640)
_GW=(0.2369268850561891,0.4786286704993665,0.5688888888888889,0.4786286704993665,0.2369268850561891)
def profile_value(name,x):
    if name=="smooth_gaussian": return 0.15+0.85*math.exp(-((x-0.43)/0.21)**2)
    if name=="steep_front":
        z=max(-700.0,min(700.0,(x-0.55)/0.025)); return 1e-6+(1-1e-6)/(1+math.exp(-z))
    if name=="local_extrema": return 0.015+0.985*math.sin(5*math.pi*x)**2
    if name=="near_zero_inventory": return 1e-12+1e-6*math.exp(-((x-0.62)/0.06)**2)
    raise ValueError("unknown profile")
def _integrate(left,right,fn):
    mid=.5*(left+right); half=.5*(right-left)
    return sum(half*w*fn(mid+half*z) for z,w in zip(_GX,_GW))
def source_projection(edges,profile):
    averages=[]; linear=[]; quadratic=[]
    for left,right in zip(edges,edges[1:]):
        h=right-left; c=.5*(left+right)
        avg=_integrate(left,right,lambda x:profile_value(profile,x))/h
        aa=12/h*_integrate(left,right,lambda x:((x-c)/h)*profile_value(profile,x))
        bb=180/h*_integrate(left,right,lambda x:(((x-c)/h)**2-1/12)*profile_value(profile,x))
        averages.append(avg); linear.append(aa); quadratic.append(bb)
    return tuple(averages),tuple(linear),tuple(quadratic)
def _poly(x,left,right,m,a,b):
    h=right-left; xi=(x-.5*(left+right))/h
    return m+a*xi+b*(xi*xi-1/12)
def _field_metrics(edges,coeffs,profile):
    av,aa,bb=coeffs; l1=l2=exact2=0.0; linf=0.0; min_value=float("inf")
    for left,right,m,a,b in zip(edges,edges[1:],av,aa,bb):
        h=right-left
        for k in range(41):
            x=left+h*k/40; val=_poly(x,left,right,m,a,b); exact=profile_value(profile,x)
            linf=max(linf,abs(val-exact)); min_value=min(min_value,val)
        l1+=_integrate(left,right,lambda x:abs(_poly(x,left,right,m,a,b)-profile_value(profile,x)))
        l2+=_integrate(left,right,lambda x:(_poly(x,left,right,m,a,b)-profile_value(profile,x))**2)
        exact2+=_integrate(left,right,lambda x:profile_value(profile,x)**2)
    return {"relative_l1":l1/max(1e-30,math.sqrt(exact2)),"relative_l2":math.sqrt(l2/max(1e-30,exact2)),"linf":linf,"minimum_reconstructed":min_value}
def _perturbation_gain(source_edges,source_coeffs,target_edges):
    scale=max(1.0,max(abs(v) for seq in source_coeffs for v in seq)); eps=1e-7
    signs=tuple(tuple((-1.0)**(i+k) for i in range(len(seq))) for k,seq in enumerate(source_coeffs))
    perturbed=tuple(tuple(v+eps*scale*s for v,s in zip(seq,sgn)) for seq,sgn in zip(source_coeffs,signs))
    base=project_quadratic_moments(source_edges,*source_coeffs,target_edges)
    changed=project_quadratic_moments(source_edges,*perturbed,target_edges)
    numerator=max(abs(x-y) for old,new in zip(base,changed) for x,y in zip(old,new))
    return numerator/(eps*scale)
def run_study(output_dir,cells=(16,32,64,128)):
    out=Path(output_dir); out.mkdir(parents=True,exist_ok=True)
    profiles=("smooth_gaussian","steep_front","local_extrema","near_zero_inventory"); rows=[]
    for profile in profiles:
        for n in cells:
            se=tuple(i/n for i in range(n+1)); nt=n+3; te=tuple((i/nt)**1.12 for i in range(nt+1))
            src=source_projection(se,profile); src_m=moments(se,*src); gain=_perturbation_gain(se,src,te)
            for limited in (False,True):
                effective_src=tuple(
                    tuple((limit_quadratic(m,a,b,True)[k-1] if k>0 else m)
                          for m,a,b in zip(*src))
                    for k in range(3)
                ) if limited else src
                dst=project_quadratic_moments(se,*src,te,positivity=limited); dst_m=moments(te,*dst)
                effective_m=moments(se,*effective_src)
                residual=[abs(y-x)/max(1e-30,abs(x)) for x,y in zip(effective_m,dst_m)]
                limiter_m=moments(se,*src)
                limiter_shift=[(y-x)/max(1e-30,abs(x)) for x,y in zip(limiter_m,effective_m)]
                met=_field_metrics(te,dst,profile)
                src_min=min(m+quadratic_minimum(a,b) for m,a,b in zip(*src))
                lim_min=min(m+quadratic_minimum(a,b) for m,a,b in zip(*effective_src))
                rows.append({"profile":profile,"source_cells":n,"target_cells":nt,"positivity_limiter":limited,
                    "relative_l1":met["relative_l1"],"relative_l2":met["relative_l2"],"linf":met["linf"],
                    "minimum_target_reconstruction":met["minimum_reconstructed"],
                    "minimum_source_reconstruction_unlimited":src_min,"minimum_source_reconstruction_limited":lim_min,
                    "relative_mass_residual":residual[0],"relative_first_moment_residual":residual[1],
                    "relative_second_moment_residual":residual[2],"max_relative_moment_residual":max(residual),
                    "limiter_relative_mass_change":limiter_shift[0],
                    "limiter_relative_first_moment_change":limiter_shift[1],
                    "limiter_relative_second_moment_change":limiter_shift[2],
                    "empirical_perturbation_gain":gain})
    with (out/"p26_3_refinement_metrics.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    grouped={}
    for profile in profiles:
        g=[r for r in rows if r["profile"]==profile]
        grouped[profile]={"max_relative_moment_residual":max(r["max_relative_moment_residual"] for r in g),
            "max_perturbation_gain":max(r["empirical_perturbation_gain"] for r in g),
            "minimum_target_reconstruction_unlimited":min(r["minimum_target_reconstruction"] for r in g if not r["positivity_limiter"]),
            "minimum_target_reconstruction_limited":min(r["minimum_target_reconstruction"] for r in g if r["positivity_limiter"]),
            "max_abs_limiter_first_moment_change":max(abs(r["limiter_relative_first_moment_change"]) for r in g),
            "max_abs_limiter_second_moment_change":max(abs(r["limiter_relative_second_moment_change"]) for r in g),
            "finest_mesh_relative_l2_unlimited":next(r["relative_l2"] for r in g if r["source_cells"]==max(cells) and not r["positivity_limiter"]),
            "finest_mesh_relative_l2_limited":next(r["relative_l2"] for r in g if r["source_cells"]==max(cells) and r["positivity_limiter"])}
    summary={"scope":"1-D P26.2 quadratic moment projection under nonmatching mesh refinement",
        "source_cell_counts":list(cells),"target_cell_rule":"N_target=N_source+3, graded x=(i/N_target)^1.12",
        "profiles":list(profiles),"cases":len(rows),
        "max_relative_moment_residual":max(r["max_relative_moment_residual"] for r in rows),
        "minimum_target_reconstruction_unlimited":min(r["minimum_target_reconstruction"] for r in rows if not r["positivity_limiter"]),
        "minimum_target_reconstruction_limited":min(r["minimum_target_reconstruction"] for r in rows if r["positivity_limiter"]),
        "maximum_empirical_perturbation_gain":max(r["empirical_perturbation_gain"] for r in rows),
        "by_profile":grouped,"interpretation_limits":[
            "perturbation gain is an empirical infinity-norm sensitivity indicator, not a matrix condition number",
            "L-infinity error uses dense within-cell sampling; L1/L2 use five-point Gaussian quadrature",
            "source positivity limiting does not guarantee a nonnegative projected target polynomial",
            "moment conservation is relative to the reconstructed source field, not the unknown continuum field",
            "synthetic profiles and 1-D intervals only; no physical validation or 2-D/3-D geometry"]}
    (out/"summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8"); print(json.dumps(summary,indent=2)); return summary
if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser(); p.add_argument("--output-dir",default="ccfsm-p26-3-results"); run_study(p.parse_args().output_dir)
