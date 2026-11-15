"""P27.7 exact red-refined tetrahedral mesh generation with conformity audit.

P27.6 closes requested depths first. Every parent tetrahedron is then
subdivided by the exact P27.3 eight-child template. P27.5 independently audits
the induced triangulations on all shared coarse faces before success is
reported. All generated coordinates are exact Fractions.
"""
from fractions import Fraction
from itertools import combinations

from ccfsm_p27_3_tetra_p2_subdivision import _child_tetrahedra
from ccfsm_p27_5_tetra_mesh_conformity import audit_tetra_mesh_face_conformity
from ccfsm_p27_6_refinement_closure import close_tetra_refinement_depths


def _f(x):
    return x if isinstance(x, Fraction) else Fraction(x)


def _mid(a, b):
    return tuple((x + y) / 2 for x, y in zip(a, b))


def _refine_barycentric(vertices, depth):
    """Return exact leaf barycentric tetrahedra after uniform red refinement."""
    leaves = [tuple(tuple(_f(x) for x in v) for v in vertices)]
    for _ in range(depth):
        next_leaves = []
        for leaf in leaves:
            next_leaves.extend(_child_tetrahedra(leaf))
        leaves = next_leaves
    return tuple(leaves)


def generate_conforming_red_refined_mesh(
    vertices,
    tetrahedra,
    requested_depths,
    *,
    max_refinement_depth=6,
    max_total_leaf_tetrahedra=250_000,
):
    """Generate exact mesh and P27.5-audit it; never certify on plan alone."""
    try:
        points = tuple(tuple(_f(x) for x in p) for p in vertices)
        tets = tuple(tuple(t) for t in tetrahedra)
        if not points or any(len(p) != 3 for p in points):
            return {"status": "invalid", "reason": "vertices_must_be_nonempty_3d"}
        if not tets or any(
            len(t) != 4 or len(set(t)) != 4
            or any(isinstance(i, bool) or not isinstance(i, int) or i < 0 or i >= len(points) for i in t)
            for t in tets
        ):
            return {"status": "invalid", "reason": "invalid_tetrahedron_connectivity"}
        closure = close_tetra_refinement_depths(
            tets, requested_depths,
            max_refinement_depth=max_refinement_depth,
            max_total_leaf_tetrahedra=max_total_leaf_tetrahedra,
        )
        if closure["status"] != "closed":
            return {"status": closure["status"], "reason": "refinement_closure_not_available", "closure": closure}
        leaf_count = closure["predicted_leaf_tetrahedra"]
        if leaf_count > max_total_leaf_tetrahedra:
            return {"status": "unresolved", "reason": "leaf_element_cap_exceeded", "closure": closure}

        generated_points = []
        point_index = {}
        generated_tets = []
        parent_leaf_records = {}
        parent_leaf_tet_indices = {}

        def add_point(point):
            point = tuple(_f(x) for x in point)
            if point not in point_index:
                point_index[point] = len(generated_points)
                generated_points.append(point)
            return point_index[point]

        for parent_index, parent in enumerate(tets):
            parent_physical = tuple(points[i] for i in parent)
            depth = closure["closed_depths"][parent_index]
            bary_leaves = _refine_barycentric(
                ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)),
                depth,
            )
            records = []
            child_ids = []
            for bary_tet in bary_leaves:
                physical_tet = tuple(
                    tuple(sum(bary_tet[j][k] * parent_physical[k][d] for k in range(4)) for d in range(3))
                    for j in range(4)
                )
                ids = tuple(add_point(p) for p in physical_tet)
                if len(set(ids)) != 4:
                    return {"status": "invalid", "reason": "degenerate_generated_child", "parent_element": parent_index}
                child_ids.append(len(generated_tets))
                generated_tets.append(ids)
                records.append({
                    "path": (),
                    "barycentric_vertices": bary_tet,
                    "bernstein_coefficients": (),
                    "status": "geometry_only",
                })
            parent_leaf_records[parent_index] = {
                "status": "unresolved",
                "leaf_records": tuple(records),
            }
            parent_leaf_tet_indices[parent_index] = tuple(child_ids)

        conformity = audit_tetra_mesh_face_conformity(
            points, tets, parent_leaf_records
        )
        if conformity["status"] != "conforming":
            return {
                "status": "unresolved",
                "reason": "p27_5_post_generation_audit_failed",
                "conformity_audit": conformity,
                "closure": closure,
                "generated_vertex_count": len(generated_points),
                "generated_tetrahedron_count": len(generated_tets),
            }

        # Every generated child has a strictly positive absolute volume iff
        # its exact determinant is nonzero. Preserve signed orientation as
        # supplied by the parent; report, do not silently reorder.
        nonpositive_or_degenerate = []
        for child_index, child in enumerate(generated_tets):
            p0, p1, p2, p3 = (generated_points[i] for i in child)
            a = tuple(p1[d] - p0[d] for d in range(3))
            b = tuple(p2[d] - p0[d] for d in range(3))
            c = tuple(p3[d] - p0[d] for d in range(3))
            det = (
                a[0] * (b[1] * c[2] - b[2] * c[1])
                - a[1] * (b[0] * c[2] - b[2] * c[0])
                + a[2] * (b[0] * c[1] - b[1] * c[0])
            )
            if det == 0:
                nonpositive_or_degenerate.append(child_index)
        if nonpositive_or_degenerate:
            return {"status": "invalid", "reason": "degenerate_generated_children", "child_indices": tuple(nonpositive_or_degenerate)}

        return {
            "status": "generated_conforming_mesh",
            "vertices": tuple(generated_points),
            "tetrahedra": tuple(generated_tets),
            "parent_leaf_tetrahedron_indices": parent_leaf_tet_indices,
            "closed_refinement_depths": closure["closed_depths"],
            "closure": closure,
            "conformity_audit": conformity,
            "exact_coordinate_type": "fractions.Fraction",
            "generated_vertex_count": len(generated_points),
            "generated_tetrahedron_count": len(generated_tets),
            "orientation_note": "nonzero absolute determinants checked; input orientation is not normalized",
            "physical_positivity_certified": False,
        }
    except (KeyError, TypeError, ValueError, ZeroDivisionError, IndexError):
        return {"status": "invalid", "reason": "malformed_mesh_or_refinement_data"}
