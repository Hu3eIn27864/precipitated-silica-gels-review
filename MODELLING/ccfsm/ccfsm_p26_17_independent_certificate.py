"""P26.17: portable primal-dual certificate reports and independent verification."""
from __future__ import annotations
from fractions import Fraction
import hashlib
import json
import math

def _F(value):
    if isinstance(value, Fraction): return value
    if isinstance(value, bool): raise ValueError("boolean is not a rational certificate value")
    return Fraction(str(value))

def _s(value): return str(_F(value))

def _canonical_payload(report):
    return json.dumps(report, sort_keys=True, separators=(",", ":"), ensure_ascii=False)

def _fingerprint(report):
    payload=dict(report); payload.pop("sha256",None)
    return hashlib.sha256(_canonical_payload(payload).encode("utf-8")).hexdigest()

def _jsonable(value):
    if isinstance(value,Fraction): return str(value)
    if isinstance(value,dict): return {str(k):_jsonable(v) for k,v in value.items()}
    if isinstance(value,(tuple,list)): return [_jsonable(v) for v in value]
    if isinstance(value,(str,int,float,bool)) or value is None: return value
    raise TypeError("unsupported report value: "+type(value).__name__)

def _moments(edges,means,linear,quadratic):
    mass=first=second=Fraction(0)
    for left,right,mean,a,b in zip(edges,edges[1:],means,linear,quadratic):
        h=right-left; c=(left+right)/2
        mass+=mean*h
        first+=mean*h*c+a*h*h/12
        second+=mean*h*(c*c+h*h/12)+a*c*h*h/6+b*h**3/180
    return mass,first,second

def _sqrt_upper(x,digits):
    if x<0 or not isinstance(digits,int) or not 1<=digits<=100:
        raise ValueError("invalid square-root enclosure input")
    scale=10**digits
    k=math.isqrt((x.numerator*scale*scale)//x.denominator)
    if k*k*x.denominator==x.numerator*scale*scale: return Fraction(k,scale)
    return Fraction(k+1,scale)

def _cell_support_upper(mean,p,q,digits):
    if mean<0: raise ValueError("negative cell mean")
    if mean==0: return Fraction(0)
    bottom=-6*mean*q
    if q>=0 or abs(p)>=3*abs(q):
        arc=6*mean*(q+_sqrt_upper(q*q+p*p/3,digits))
    else: arc=3*mean*(abs(p)+q)
    return max(bottom,arc)

def _dual_gap(inputs,direction,digits):
    edges=tuple(map(_F,inputs["edges"])); means=tuple(map(_F,inputs["averages"]))
    base_a=tuple(map(_F,inputs["linear"])); base_b=tuple(map(_F,inputs["quadratic"]))
    y1,y2=map(_F,direction)
    if y1==0 and y2==0: raise ValueError("zero dual direction")
    _,first,second=_moments(edges,means,base_a,base_b)
    base_first=sum((m*(r-l)*(l+r)/2 for l,r,m in zip(edges,edges[1:],means)),Fraction(0))
    base_second=sum((m*(r-l)*(((l+r)/2)**2+(r-l)**2/12)
                     for l,r,m in zip(edges,edges[1:],means)),Fraction(0))
    t1,t2=first-base_first,second-base_second
    support=Fraction(0)
    for left,right,mean in zip(edges,edges[1:],means):
        h=right-left; c=(left+right)/2
        p=y1*h*h/12+y2*c*h*h/6
        q=y2*h**3/180
        support+=_cell_support_upper(mean,p,q,digits)
    return y1*t1+y2*t2-support

def _verify_primal(inputs,certificate):
    edges=tuple(map(_F,inputs["edges"])); means=tuple(map(_F,inputs["averages"]))
    base_a=tuple(map(_F,inputs["linear"])); base_b=tuple(map(_F,inputs["quadratic"]))
    a=tuple(map(_F,certificate["linear"])); b=tuple(map(_F,certificate["quadratic"]))
    n=len(means)
    if len(edges)!=n+1 or len(a)!=n or len(b)!=n or len(base_a)!=n or len(base_b)!=n:
        raise ValueError("primal vector dimensions do not match mesh")
    if any(r<=l for l,r in zip(edges,edges[1:])) or any(m<0 for m in means):
        raise ValueError("invalid mesh or cell mean")
    target=_moments(edges,means,base_a,base_b); actual=_moments(edges,means,a,b)
    if actual!=target: raise ValueError("primal witness does not reproduce all three global moments")
    cells=certificate["cell_sos"]
    if len(cells)!=n: raise ValueError("one SOS certificate per cell is required")
    for j,(m,aj,bj,cell) in enumerate(zip(means,a,b,cells)):
        lam=_F(cell["lambda"])
        q00=_F(cell["Q"][0][0]); q01=_F(cell["Q"][0][1])
        q10=_F(cell["Q"][1][0]); q11=_F(cell["Q"][1][1]); det=_F(cell["determinant"])
        if q01!=q10: raise ValueError("cell %d Gram matrix is not symmetric"%j)
        actual_det=q00*q11-q01*q01
        if lam<0 or q00<0 or q11<0 or actual_det<0:
            raise ValueError("cell %d SOS Gram matrix is not PSD"%j)
        if det!=actual_det: raise ValueError("cell %d determinant does not match Gram matrix"%j)
        if (q00+lam/4,2*q01,q11-lam)!=(m-bj/12,aj,bj):
            raise ValueError("cell %d SOS coefficient identity fails"%j)
    return {"verified":True,"proof":"exact rational global mass/first/second moments and per-cell Markov-Lukacs PSD identities",
            "global_moments":list(map(str,actual)),"cells_verified":n}

def build_certificate_report(inputs,assessment):
    canonical={"edges":[_s(v) for v in inputs["edges"]],
               "averages":[_s(v) for v in inputs["averages"]],
               "linear":[_s(v) for v in inputs["linear"]],
               "quadratic":[_s(v) for v in inputs["quadratic"]]}
    status=assessment.get("status","unresolved")
    report={"schema":"ccfsm-p26.17-certificate-report-v1","inputs":canonical,
            "status":status,"certificate":None,"diagnostics":{}}
    if status=="feasible_exact_primal_witness":
        witness=assessment["primal_witness"]; exact=witness["exact_certificate"]
        report["certificate"]={"kind":"primal_markov_lukacs",
            "linear":[_s(v) for v in witness["linear"]],
            "quadratic":[_s(v) for v in witness["quadratic"]],
            "cell_sos":_jsonable(exact["cell_certificates"])}
        report["diagnostics"]={"proof_level":assessment.get("proof_level","")}
    elif status=="certified_infeasible":
        dual=assessment.get("dual_certificate",assessment); cert=dual["certificate"]
        report["certificate"]={"kind":"dual_strict_separator",
            "direction":[_s(v) for v in cert["direction"]],"sqrt_digits":int(cert["sqrt_digits"])}
        report["diagnostics"]={"search_radius":dual.get("max_direction"),
                               "directions_checked":dual.get("directions_checked")}
    else:
        report["status"]="unresolved"
        report["diagnostics"]={"reason":"No independently checkable exact primal or strict dual certificate was produced."}
    report["sha256"]=_fingerprint(report)
    return report

def verify_certificate_report(report):
    if not isinstance(report,dict) or report.get("schema")!="ccfsm-p26.17-certificate-report-v1":
        return {"verified":False,"status":"invalid_report","reason":"unsupported schema"}
    if report.get("sha256")!=_fingerprint(report):
        return {"verified":False,"status":"invalid_report","reason":"SHA-256 integrity fingerprint mismatch"}
    inputs=report.get("inputs")
    if not isinstance(inputs,dict):
        return {"verified":False,"status":"invalid_report","reason":"missing canonical inputs"}
    try:
        kind=(report.get("certificate") or {}).get("kind")
        if report.get("status")=="feasible_exact_primal_witness" and kind=="primal_markov_lukacs":
            result=_verify_primal(inputs,report["certificate"])
            return {"verified":True,"status":"feasible_exact_primal_witness",
                    "integrity_sha256":report["sha256"],**result}
        if report.get("status")=="certified_infeasible" and kind=="dual_strict_separator":
            cert=report["certificate"]
            gap=_dual_gap(inputs,cert["direction"],cert["sqrt_digits"])
            if gap<=0: raise ValueError("recomputed rational dual lower gap is not strictly positive")
            return {"verified":True,"status":"certified_infeasible",
                    "proof":"strict rational dual separation; support evaluated with integer square-root upper bounds",
                    "gap_lower_bound":str(gap),"direction":list(map(_s,cert["direction"])),
                    "integrity_sha256":report["sha256"]}
        if report.get("status")=="unresolved" and report.get("certificate") is None:
            return {"verified":False,"status":"unresolved",
                    "meaning":"Structurally valid report; no proof of feasibility or infeasibility.",
                    "integrity_sha256":report["sha256"]}
        raise ValueError("status and certificate kind are inconsistent")
    except (KeyError,TypeError,ValueError,ZeroDivisionError) as exc:
        return {"verified":False,"status":"invalid_certificate","reason":str(exc)}

def write_certificate_report(path,inputs,assessment):
    report=build_certificate_report(inputs,assessment)
    with open(path,"w",encoding="utf-8") as f:
        json.dump(report,f,indent=2,sort_keys=True,ensure_ascii=False); f.write("\n")
    return report
