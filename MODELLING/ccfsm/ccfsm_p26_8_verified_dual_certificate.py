"""P26.8: rationally verified dual infeasibility certificates for P26 moments.

The cellwise nonnegative quadratic coefficient set is compact. Its support
function is evaluated in closed form. Square roots are enclosed from above
using integer arithmetic, so a positive rational gap is a rigorous separator
for the exact decimal-rational input represented by the supplied values.
"""
from __future__ import annotations
import csv, json, math
from fractions import Fraction
from pathlib import Path
from ccfsm_p26_2_quadratic_projection import _edges


def _F(value):
    if isinstance(value, Fraction): return value
    if isinstance(value, int): return Fraction(value)
    x=float(value)
    if not math.isfinite(x): raise ValueError("all inputs must be finite")
    return Fraction(str(value))


def _sqrt_upper(x: Fraction, digits: int=30) -> Fraction:
    """Exact rational upper bound for sqrt(x), using integer square roots."""
    if x < 0: raise ValueError("square-root argument must be nonnegative")
    if digits < 1 or digits > 100: raise ValueError("digits must be in [1,100]")
    scale=10**digits
    k=math.isqrt((x.numerator*scale*scale)//x.denominator)
    if k*k*x.denominator == x.numerator*scale*scale:
        return Fraction(k,scale)
    return Fraction(k+1,scale)


def cell_support_upper(mean, p, q, sqrt_digits: int=30):
    """Upper bound on max(p*a+q*b) over a cell's exact positivity set.

    The feasible boundary consists of the two endpoint-positivity segments
    joining (0,-6m) to (+/-3m,3m), and the upper ellipse arc
    a=sqrt(12)m sin(phi), b=6m(1+cos(phi)), |phi|<=2pi/3.
    """
    m,p,q=map(_F,(mean,p,q))
    if m<0: raise ValueError("cell average must be nonnegative")
    if m==0: return Fraction(0)
    bottom=-6*m*q
    # Ellipse-arc maximum. The unconstrained maximizer lies on the arc
    # exactly when |P| >= sqrt(3)|Q|, equivalent to |p| >= 3|q|.
    if abs(p) >= 3*abs(q):
        radicand=q*q+p*p/3
        arc=6*m*(q+_sqrt_upper(radicand,sqrt_digits))
    else:
        # The arc maximum is at one of its two endpoints.
        arc=3*m*(abs(p)+q)
    return max(bottom,arc)


def _moments_and_target(edges, averages, linear, quadratic):
    mass=first=second=Fraction(0)
    for l,r,m,a,b in zip(edges,edges[1:],averages,linear,quadratic):
        h=r-l; c=(l+r)/2
        mass += m*h
        first += m*h*c + a*h*h/12
        second += m*h*(c*c+h*h/12) + a*c*h*h/6 + b*h**3/180
    base_first= sum((m*(r-l)*(l+r)/2 for l,r,m in zip(edges,edges[1:],averages)),Fraction(0))
    base_second=sum((m*(r-l)*(((l+r)/2)**2+(r-l)**2/12) for l,r,m in zip(edges,edges[1:],averages)),Fraction(0))
    return (mass,first,second),(first-base_first,second-base_second)


def verify_dual_certificate(target_edges, averages, linear, quadratic,
                             direction, sqrt_digits=30):
    """Recompute a rational lower bound on the strict dual separation gap."""
    ef=tuple(_F(v) for v in target_edges)
    if len(ef)<2 or any(y<=x for x,y in zip(ef,ef[1:])):
        raise ValueError("edges must be strictly increasing")
    n=len(ef)-1
    u=tuple(_F(v) for v in averages); a=tuple(_F(v) for v in linear); b=tuple(_F(v) for v in quadratic)
    if len(u)!=n or len(a)!=n or len(b)!=n: raise ValueError("one coefficient triple per cell required")
    if any(m<0 for m in u): raise ValueError("cell averages must be nonnegative")
    if len(direction)!=2: raise ValueError("direction must have two rational components")
    y1,y2=map(_F,direction)
    if y1==0 and y2==0: raise ValueError("dual direction must be nonzero")
    (_,m1,m2),(t1,t2)=_moments_and_target(ef,u,a,b)
    support=Fraction(0)
    for l,r,m in zip(ef,ef[1:],u):
        h=r-l; c=(l+r)/2
        p=y1*h*h/12 + y2*c*h*h/6
        q=y2*h**3/180
        support += cell_support_upper(m,p,q,sqrt_digits)
    lhs=y1*t1+y2*t2
    gap_lower=lhs-support
    return {"verified":gap_lower>0,"direction":[str(y1),str(y2)],
      "target_modal_moments":[str(t1),str(t2)],"target_dot_direction":str(lhs),
      "support_upper_bound":str(support),"gap_lower_bound":str(gap_lower),
      "gap_lower_numerator":gap_lower.numerator,"gap_lower_denominator":gap_lower.denominator,
      "sqrt_digits":sqrt_digits,"input_interpretation":"exact rational values parsed from decimal string representations",
      "moment_totals":[str(x) for x in (_,m1,m2)],
      "certificate":"strict rational lower bound on target dot direction minus exact support-function upper bound" if gap_lower>0 else "no strict separation certified"}


def search_dual_certificate(target_edges, averages, linear, quadratic,
                            max_direction=12, sqrt_digits=30):
    """Search a finite rational direction set; any returned positive gap verifies."""
    if not isinstance(max_direction,int) or max_direction<1 or max_direction>1000:
        raise ValueError("max_direction must be an integer in [1,1000]")
    candidates=[]
    for i in range(-max_direction,max_direction+1):
        for j in range(-max_direction,max_direction+1):
            if i==0 and j==0: continue
            d=verify_dual_certificate(target_edges,averages,linear,quadratic,(i,j),sqrt_digits)
            if d["verified"]:
                gap=Fraction(d["gap_lower_bound"])
                candidates.append((gap,d))
    if not candidates:
        return {"status":"no_certificate_found","verified":False,
          "search":"integer directions in [-N,N]^2","max_direction":max_direction,
          "meaning":"No direction in the finite search set gave a strictly positive verified gap; this does not prove feasibility."}
    gap,certificate=max(candidates,key=lambda z:z[0])
    return {"status":"certified_infeasible","verified":True,"certificate":certificate,
      "search":"integer directions in [-N,N]^2","max_direction":max_direction}


def run_study(output_dir):
    out=Path(output_dir); out.mkdir(parents=True,exist_ok=True)
    cases=[
      ("zero_inventory_nonzero_modes",(0.,.4,1.),(0.,0.),(1.,0.),(0.,0.)),
      ("positive_means_negative_reconstruction",(0.,.4,1.),(1.,.8),(8.,-7.),(0.,0.)),
      ("zero_modes_control",(0.,.4,1.),(1.,.7),(0.,0.),(0.,0.))]
    rows=[]
    for name,e,u,a,b in cases:
        result=search_dual_certificate(e,u,a,b,max_direction=12)
        rows.append({"case":name,"status":result["status"],"verified":result["verified"],
          "gap_lower_bound":result.get("certificate",{}).get("gap_lower_bound",""),
          "direction":result.get("certificate",{}).get("direction","")})
    with (out/"p26_8_verified_dual_certificates.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    summary={"scope":"1-D exact-decimal-rational dual infeasibility certificates for global first/second moments",
      "cases":rows,"limitations":["certificate applies to the exact rational values parsed from decimal input strings",
      "finite direction search can fail to find an existing separator",
      "square-root support bounds are rigorous rational upper bounds, not floating-point estimates",
      "1-D intervals and quadratic cell polynomials only","no physical validation"]}
    (out/"summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    print(json.dumps(summary,indent=2)); return summary

if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser(); p.add_argument("--output-dir",default="ccfsm-p26-8-results"); run_study(p.parse_args().output_dir)
