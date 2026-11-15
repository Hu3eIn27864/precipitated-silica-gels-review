"""P27.3: exact adaptive tetrahedral subdivision for P2 Bernstein positivity.

A failed Bernstein test is inconclusive. This module bisects a tetrahedron
into four corner tetrahedra and four tetrahedra partitioning the central
octahedron. All barycentric coordinates and polynomial restrictions are exact
Fractions. A certificate is accepted only when every leaf has nonnegative
degree-2 Bernstein coefficients.
"""
from fractions import Fraction

from ccfsm_p27_1_tetra_p1_positivity import tetrahedron_signed_six_volume, _F
from ccfsm_p27_2_tetra_p2_bernstein import EDGE_ORDER, quadratic_tetra_bernstein_coefficients

_IDENTITY = tuple(tuple(Fraction(int(i == j)) for i in range(4)) for j in range(4))


def _midpoint(a, b):
    return tuple((x + y) / 2 for x, y in zip(a, b))


def _evaluate(coefficients, lam):
    value = sum(coefficients[i] * lam[i] ** 2 for i in range(4))
    for k, (i, j) in enumerate(EDGE_ORDER):
        value += 2 * coefficients[4 + k] * lam[i] * lam[j]
    return value


def _child_tetrahedra(vertices):
    """Eight exact barycentric children; central octahedron split on m01--m23."""
    mids = {(i, j): _midpoint(vertices[i], vertices[j]) for i, j in EDGE_ORDER}
    m = mids
    return (
        (vertices[0], m[0, 1], m[0, 2], m[0, 3]),
        (vertices[1], m[0, 1], m[1, 2], m[1, 3]),
        (vertices[2], m[0, 2], m[1, 2], m[2, 3]),
        (vertices[3], m[0, 3], m[1, 3], m[2, 3]),
        (m[0, 1], m[0, 2], m[0, 3], m[2, 3]),
        (m[0, 1], m[0, 3], m[1, 3], m[2, 3]),
        (m[0, 1], m[1, 3], m[1, 2], m[2, 3]),
        (m[0, 1], m[1, 2], m[0, 2], m[2, 3]),
    )


def _restricted_coefficients(parent_coefficients, child_vertices):
    vertex_values = tuple(_evaluate(parent_coefficients, v) for v in child_vertices)
    edge_values = tuple(
        _evaluate(parent_coefficients, _midpoint(child_vertices[i], child_vertices[j]))
        for i, j in EDGE_ORDER
    )
    return quadratic_tetra_bernstein_coefficients(vertex_values, edge_values)


def certify_tetra_p2_by_subdivision(
    vertices, vertex_values, edge_midpoint_values, max_depth=6
):
    """Return certified_nonnegative, certified_negative_point, or unresolved.

    max_depth=0 performs only the original-element Bernstein test.
    A negative exact value at any subdivision vertex is a rigorous
    counterexample. Negative Bernstein coefficients alone are never treated
    as proof of negativity.
    """
    try:
        if not isinstance(max_depth, int) or isinstance(max_depth, bool) or max_depth < 0:
            return {"status": "unresolved", "reason": "invalid_max_depth"}
        if tetrahedron_signed_six_volume(vertices) == 0:
            return {"status": "unresolved", "reason": "degenerate_tetrahedron"}
        root_coefficients = quadratic_tetra_bernstein_coefficients(
            vertex_values, edge_midpoint_values
        )
        root_vertices = _IDENTITY
        visited = 0
        leaf_count = 0
        deepest = 0
        unresolved_leaves = []

        def visit(coefficients, bary_vertices, depth, path):
            nonlocal visited, leaf_count, deepest
            visited += 1
            deepest = max(deepest, depth)
            vertex_values_here = tuple(_evaluate(coefficients, v) for v in _IDENTITY)
            # Coefficients are in the local child basis; local vertices are e_i.
            negative_vertices = tuple(i for i, value in enumerate(vertex_values_here) if value < 0)
            if negative_vertices:
                i = negative_vertices[0]
                original_bary = bary_vertices[i]
                leaf_count += 1
                return {
                    "status": "certified_negative_point",
                    "path": path,
                    "local_vertex": i,
                    "barycentric_point": original_bary,
                    "value": vertex_values_here[i],
                }
            if min(coefficients) >= 0:
                leaf_count += 1
                return None
            if depth >= max_depth:
                leaf_count += 1
                unresolved_leaves.append(path)
                return None
            for child_index, child_vertices in enumerate(_child_tetrahedra(bary_vertices)):
                child_coefficients = _restricted_coefficients(coefficients, child_vertices)
                result = visit(child_coefficients, child_vertices, depth + 1,
                               path + (child_index,))
                if result is not None:
                    return result
            return None

        counterexample = visit(root_coefficients, root_vertices, 0, ())
        if counterexample is not None:
            return {
                **counterexample,
                "visited_cells": visited,
                "maximum_depth_reached": deepest,
                "reason": "exact_negative_point_found",
            }
        if not unresolved_leaves:
            return {
                "status": "certified_nonnegative",
                "reason": "all_subdivision_leaf_bernstein_coefficients_nonnegative",
                "visited_cells": visited,
                "leaf_count": leaf_count,
                "maximum_depth_reached": deepest,
                "max_depth": max_depth,
            }
        return {
            "status": "unresolved",
            "reason": "bernstein_certificate_not_resolved_at_max_depth",
            "visited_cells": visited,
            "leaf_count": leaf_count,
            "maximum_depth_reached": deepest,
            "max_depth": max_depth,
            "unresolved_leaf_paths": tuple(unresolved_leaves),
        }
    except (TypeError, ValueError, ZeroDivisionError, KeyError):
        return {"status": "unresolved", "reason": "malformed_tetrahedron_or_polynomial_data"}
