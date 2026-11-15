"""P27.4: independent exact verifier for P27.3 tetrahedral P2 certificates.

This module intentionally does not import the P27.3 constructor or P27.2
conversion routine. It replays the dyadic subdivision and recomputes every
leaf coefficient from the root nodal data.
"""
from fractions import Fraction as F

EDGES = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
IDENTITY = tuple(tuple(F(int(i == j)) for j in range(4)) for i in range(4))


def _f(x):
    if isinstance(x, F):
        return x
    return F(x)


def _mid(a, b):
    return tuple((x + y) / 2 for x, y in zip(a, b))


def _children(v):
    m = {e: _mid(v[e[0]], v[e[1]]) for e in EDGES}
    return (
        (v[0], m[0, 1], m[0, 2], m[0, 3]),
        (v[1], m[0, 1], m[1, 2], m[1, 3]),
        (v[2], m[0, 2], m[1, 2], m[2, 3]),
        (v[3], m[0, 3], m[1, 3], m[2, 3]),
        (m[0, 1], m[0, 2], m[0, 3], m[2, 3]),
        (m[0, 1], m[0, 3], m[1, 3], m[2, 3]),
        (m[0, 1], m[1, 3], m[1, 2], m[2, 3]),
        (m[0, 1], m[1, 2], m[0, 2], m[2, 3]),
    )


def _coefficients(vertex_values, edge_midpoint_values):
    if len(vertex_values) != 4 or len(edge_midpoint_values) != 6:
        raise ValueError("expected 4 vertex and 6 edge-midpoint values")
    v = tuple(_f(x) for x in vertex_values)
    m = tuple(_f(x) for x in edge_midpoint_values)
    return v + tuple(2*m[k] - (v[i] + v[j])/2
                     for k, (i, j) in enumerate(EDGES))


def _eval(c, lam):
    return sum(c[i]*lam[i]**2 for i in range(4)) + sum(
        2*c[4+k]*lam[i]*lam[j] for k, (i, j) in enumerate(EDGES))


def _restrict(c, child):
    vv = tuple(_eval(c, p) for p in child)
    mm = tuple(_eval(c, _mid(child[i], child[j])) for i, j in EDGES)
    return _coefficients(vv, mm)


def _volume6(vertices):
    a, b, c, d = vertices
    x = tuple(_f(b[i])-_f(a[i]) for i in range(3))
    y = tuple(_f(c[i])-_f(a[i]) for i in range(3))
    z = tuple(_f(d[i])-_f(a[i]) for i in range(3))
    return (x[0]*(y[1]*z[2]-y[2]*z[1])
            - x[1]*(y[0]*z[2]-y[2]*z[0])
            + x[2]*(y[0]*z[1]-y[1]*z[0]))


def verify_p27_3_certificate(vertices, vertex_values, edge_midpoint_values,
                             certificate):
    """Independently verify a P27.3 result; fail closed on any mismatch."""
    try:
        if len(vertices) != 4 or any(len(p) != 3 for p in vertices):
            return {"verified": False, "reason": "malformed_tetrahedron"}
        if _volume6(vertices) == 0:
            return {"verified": False, "reason": "degenerate_tetrahedron"}
        root = _coefficients(vertex_values, edge_midpoint_values)
        status = certificate["status"]
        if status == "certified_negative_point":
            lam = tuple(_f(x) for x in certificate["barycentric_point"])
            value = _f(certificate["value"])
            if len(lam) != 4 or sum(lam) != 1 or min(lam) < 0:
                return {"verified": False, "reason": "invalid_barycentric_witness"}
            actual = _eval(root, lam)
            if actual != value or actual >= 0:
                return {"verified": False, "reason": "negative_witness_mismatch"}
            return {"verified": True, "status": status, "verified_value": actual}

        if status not in ("certified_nonnegative", "unresolved"):
            return {"verified": False, "reason": "unknown_status"}
        if certificate.get("max_depth") is None:
            return {"verified": False, "reason": "missing_max_depth"}
        max_depth = certificate["max_depth"]
        if not isinstance(max_depth, int) or isinstance(max_depth, bool) or max_depth < 0:
            return {"verified": False, "reason": "invalid_max_depth"}
        records = certificate.get("leaf_records")
        if not isinstance(records, (tuple, list)) or not records:
            return {"verified": False, "reason": "missing_leaf_records"}
        by_path = {}
        for record in records:
            path = tuple(record["path"])
            if path in by_path or any(not isinstance(i, int) or i < 0 or i > 7 for i in path):
                return {"verified": False, "reason": "duplicate_or_invalid_path"}
            by_path[path] = record
        seen = set()
        unresolved = []

        def replay(path, coeff):
            if path in by_path:
                rec = by_path[path]
                if path in seen:
                    raise ValueError("duplicate leaf")
                seen.add(path)
                supplied = tuple(_f(x) for x in rec["bernstein_coefficients"])
                if supplied != coeff:
                    raise ValueError("leaf coefficient mismatch")
                if rec["status"] == "nonnegative":
                    if min(coeff) < 0:
                        raise ValueError("negative coefficient marked certified")
                elif rec["status"] == "unresolved":
                    if min(coeff) >= 0:
                        raise ValueError("unresolved leaf already certifiable")
                    unresolved.append(path)
                else:
                    raise ValueError("invalid leaf status")
                return
            if len(path) >= max_depth:
                raise ValueError("missing terminal leaf")
            for k, child in enumerate(_children(IDENTITY)):
                replay(path + (k,), _restrict(coeff, child))

        replay((), root)
        if seen != set(by_path):
            return {"verified": False, "reason": "unreachable_or_extra_leaf"}
        if status == "certified_nonnegative" and unresolved:
            return {"verified": False, "reason": "unresolved_leaf_in_positive_certificate"}
        if status == "unresolved" and not unresolved:
            return {"verified": False, "reason": "unresolved_status_without_unresolved_leaf"}
        return {"verified": True, "status": status, "leaf_count": len(seen),
                "unresolved_leaf_paths": tuple(unresolved)}
    except (KeyError, TypeError, ValueError, ZeroDivisionError, IndexError):
        return {"verified": False, "reason": "malformed_or_inconsistent_certificate"}
