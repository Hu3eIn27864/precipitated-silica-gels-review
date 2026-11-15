"""P27.1: exact 3-D tetrahedral geometry and P1 positivity certificates.

For an affine scalar field on a nondegenerate tetrahedron, its values are
barycentric convex combinations of the four vertex values. Hence nonnegative
nodal values are necessary and sufficient for pointwise nonnegativity.
All geometry and sign checks use exact rational arithmetic.
"""
from fractions import Fraction


def _F(value):
    if isinstance(value, bool):
        raise ValueError("boolean is not a rational value")
    return value if isinstance(value, Fraction) else Fraction(str(value))


def _det3(a, b, c):
    return (a[0] * (b[1] * c[2] - b[2] * c[1])
            - a[1] * (b[0] * c[2] - b[2] * c[0])
            + a[2] * (b[0] * c[1] - b[1] * c[0]))


def tetrahedron_signed_six_volume(vertices):
    """Return det(v1-v0,v2-v0,v3-v0); zero means degenerate geometry."""
    if len(vertices) != 4 or any(len(v) != 3 for v in vertices):
        raise ValueError("a tetrahedron requires four 3-D vertices")
    pts = tuple(tuple(_F(x) for x in v) for v in vertices)
    edges = tuple(tuple(pts[i][k] - pts[0][k] for k in range(3))
                  for i in (1, 2, 3))
    return _det3(*edges)


def verify_tetra_p1_positivity(vertices, nodal_values):
    """Exactly certify P1 scalar nonnegativity on one tetrahedron."""
    try:
        signed_six_volume = tetrahedron_signed_six_volume(vertices)
        if signed_six_volume == 0:
            return {"verified": False, "reason": "degenerate_tetrahedron"}
        if len(nodal_values) != 4:
            return {"verified": False, "reason": "nodal_value_count_mismatch"}
        values = tuple(_F(v) for v in nodal_values)
        if min(values) < 0:
            return {"verified": False, "reason": "negative_vertex_value"}
        return {
            "verified": True,
            "reason": "exact_p1_barycentric_positivity",
            "signed_six_volume": signed_six_volume,
            "volume": abs(signed_six_volume) / 6,
            "minimum_nodal_value": min(values),
            "bernstein_degree_1": values,
        }
    except (TypeError, ValueError, ZeroDivisionError):
        return {"verified": False, "reason": "malformed_tetrahedron_or_values"}


def verify_tetra_p1_mesh(nodes, nodal_values, tetrahedra):
    """Verify every listed tetrahedron; this is local element positivity."""
    if len(nodes) != len(nodal_values):
        return {"verified": False, "cells": (), "reason": "node_value_count_mismatch"}
    results = []
    for cell_id, cell in enumerate(tetrahedra):
        if len(cell) != 4 or len(set(cell)) != 4:
            results.append({"verified": False, "reason": "invalid_connectivity",
                            "cell": cell_id})
            continue
        if any(not isinstance(i, int) or isinstance(i, bool)
               or i < 0 or i >= len(nodes) for i in cell):
            results.append({"verified": False, "reason": "node_index_out_of_range",
                            "cell": cell_id})
            continue
        result = verify_tetra_p1_positivity(
            tuple(nodes[i] for i in cell), tuple(nodal_values[i] for i in cell))
        result["cell"] = cell_id
        results.append(result)
    ok = bool(results) and all(r["verified"] for r in results)
    return {"verified": ok, "cells": tuple(results),
            "reason": "all_elements_certified" if ok else "one_or_more_elements_not_certified"}
