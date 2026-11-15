"""P27.2: exact sufficient Bernstein positivity certificate for P2 tetrahedra.

The ten degree-2 simplex Bernstein basis functions are nonnegative and sum
to one. Nonnegative Bernstein coefficients therefore certify pointwise
nonnegativity. Failure to obtain this certificate is inconclusive.
"""
from fractions import Fraction

from ccfsm_p27_1_tetra_p1_positivity import tetrahedron_signed_six_volume, _F

EDGE_ORDER = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))


def quadratic_tetra_bernstein_coefficients(vertex_values, edge_midpoint_values):
    """Convert the four vertices and six edge-midpoint values to P2 Bernstein coefficients."""
    if len(vertex_values) != 4 or len(edge_midpoint_values) != 6:
        raise ValueError("P2 tetrahedron requires 4 vertex and 6 edge-midpoint values")
    vertices = tuple(_F(v) for v in vertex_values)
    midpoints = tuple(_F(v) for v in edge_midpoint_values)
    edges = tuple(2 * midpoints[k] - (vertices[i] + vertices[j]) / 2
                  for k, (i, j) in enumerate(EDGE_ORDER))
    return vertices + edges


def verify_tetra_p2_bernstein_positivity(vertices, vertex_values, edge_midpoint_values):
    """Return an exact sufficient P2 positivity certificate or an inconclusive result."""
    try:
        six_volume = tetrahedron_signed_six_volume(vertices)
        if six_volume == 0:
            return {"certified": False, "reason": "degenerate_tetrahedron"}
        coefficients = quadratic_tetra_bernstein_coefficients(
            vertex_values, edge_midpoint_values)
        negative = tuple(i for i, value in enumerate(coefficients) if value < 0)
        if negative:
            return {
                "certified": False,
                "reason": "negative_bernstein_coefficient_not_certified",
                "negative_coefficient_indices": negative,
                "bernstein_coefficients": coefficients,
            }
        return {
            "certified": True,
            "reason": "all_degree_2_bernstein_coefficients_nonnegative",
            "signed_six_volume": six_volume,
            "bernstein_coefficients": coefficients,
            "minimum_bernstein_coefficient": min(coefficients),
        }
    except (TypeError, ValueError, ZeroDivisionError):
        return {"certified": False, "reason": "malformed_p2_tetrahedron_data"}
