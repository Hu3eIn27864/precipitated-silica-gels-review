"""P26.18: compare independently verified certificates across rational representations and meshes."""
from __future__ import annotations
from fractions import Fraction
from ccfsm_p26_17_independent_certificate import verify_certificate_report, _F, _moments


def _signature(report):
    inputs=report["inputs"]
    edges=tuple(_F(v) for v in inputs["edges"])
    means=tuple(_F(v) for v in inputs["averages"])
    linear=tuple(_F(v) for v in inputs["linear"])
    quadratic=tuple(_F(v) for v in inputs["quadratic"])
    n=len(means)
    if len(edges)!=n+1 or len(linear)!=n or len(quadratic)!=n:
        raise ValueError("input dimensions do not match mesh")
    if any(r<=l for l,r in zip(edges,edges[1:])) or any(m<0 for m in means):
        raise ValueError("invalid mesh or negative cell mean")
    return _moments(edges,means,linear,quadratic)


def compare_certificate_reports(report_a, report_b):
    """Compare proof status and exact global target moments, not local functions."""
    va=verify_certificate_report(report_a)
    vb=verify_certificate_report(report_b)
    if va.get("status")=="invalid_report" or va.get("status")=="invalid_certificate":
        return {"status":"invalid_input_report_a","verified":False,"detail":va}
    if vb.get("status")=="invalid_report" or vb.get("status")=="invalid_certificate":
        return {"status":"invalid_input_report_b","verified":False,"detail":vb}
    try:
        sig_a=_signature(report_a); sig_b=_signature(report_b)
    except (KeyError,TypeError,ValueError,ZeroDivisionError) as exc:
        return {"status":"invalid_input","verified":False,"reason":str(exc)}
    if sig_a!=sig_b:
        return {"status":"different_global_targets","verified":False,
                "target_moments_a":list(map(str,sig_a)),
                "target_moments_b":list(map(str,sig_b))}
    status_a=report_a.get("status"); status_b=report_b.get("status")
    if status_a!=status_b:
        return {"status":"inconclusive_status_mismatch","verified":False,
                "shared_target_moments":list(map(str,sig_a)),
                "status_a":status_a,"status_b":status_b}
    if status_a=="unresolved":
        return {"status":"same_target_but_unresolved","verified":False,
                "shared_target_moments":list(map(str,sig_a))}
    if not va.get("verified") or not vb.get("verified"):
        return {"status":"certificate_verification_failed","verified":False,
                "verification_a":va,"verification_b":vb}
    return {"status":"equivalent_global_moment_certificates","verified":True,
            "certificate_status":status_a,
            "shared_target_moments":list(map(str,sig_a)),
            "mesh_cell_counts":[len(report_a["inputs"]["averages"]),
                                len(report_b["inputs"]["averages"])],
            "scope":"equivalence of exact global moment targets and independently verified proof status only"}


def rational_input_fingerprint(inputs):
    """Canonical exact-rational signature; decimal and fraction aliases collapse."""
    edges=tuple(_F(v) for v in inputs["edges"])
    means=tuple(_F(v) for v in inputs["averages"])
    linear=tuple(_F(v) for v in inputs["linear"])
    quadratic=tuple(_F(v) for v in inputs["quadratic"])
    if len(edges)!=len(means)+1 or len(linear)!=len(means) or len(quadratic)!=len(means):
        raise ValueError("input dimensions do not match mesh")
    if any(r<=l for l,r in zip(edges,edges[1:])) or any(m<0 for m in means):
        raise ValueError("invalid mesh or negative cell mean")
    canonical=(edges,means,linear,quadratic)
    return tuple(tuple(str(v) for v in row) for row in canonical)
