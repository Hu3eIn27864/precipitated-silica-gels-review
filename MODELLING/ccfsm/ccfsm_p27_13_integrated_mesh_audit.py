"""P27.13 integrated exact 3D tetrahedral mesh audit.

Aggregates the P27.8--P27.12 gates into one report. A passing result means
these specified discrete checks passed; it is not a complete proof of global
simplicial embedding, FE stability, or physical CCFSM positivity.
"""
from ccfsm_p27_8_tetra_geometry_audit import normalize_and_audit_tetra_mesh
from ccfsm_p27_12_oriented_boundary_audit import audit_tetra_mesh_boundary


def audit_tetra_mesh_3d(vertices, tetrahedra, *, min_quality_ratio=0):
    """Run the integrated P27.8--P27.12 audit and return explicit gate results."""
    geometry = normalize_and_audit_tetra_mesh(
        vertices, tetrahedra, min_quality_ratio=min_quality_ratio)
    if geometry.get("status") != "oriented_quality_audited":
        return {
            "status": "mesh_geometry_gate_failed",
            "overall_pass": False,
            "gate_results": {
                "P27.8_geometry_quality": geometry.get("status", "failed"),
                "P27.9_global_incidence": "not_run",
                "P27.10_local_links": "not_run",
                "P27.11_geometric_embedding": "not_run",
                "P27.12_oriented_boundary": "not_run",
            },
            "geometry_audit": geometry,
            "all_required_gates_passed": False,
            "physical_ccfsm_positivity_certified": False,
        }

    # Pass the normalized positive-orientation mesh into the downstream chain.
    boundary = audit_tetra_mesh_boundary(
        geometry["vertices"], geometry["tetrahedra"],
        min_quality_ratio=min_quality_ratio)
    if boundary.get("status") != "oriented_boundary_audited":
        status = boundary.get("status", "failed")
        # On a boundary-stage failure P27.12 returns the successful P27.11
        # report directly; on an earlier failure it wraps it as base_audit.
        embedding_failed_or_passed = boundary.get(
            "geometric_embedding_audit", boundary.get("base_audit", {}))
        links = embedding_failed_or_passed.get("base_link_audit", {})
        incidence = links.get("base_incidence_audit", {})
        p9_status = incidence.get("status", "not_run")
        p10_status = links.get("status", "not_run")
        p11_status = embedding_failed_or_passed.get("status", "not_run")
        return {
            "status": "integrated_mesh_audit_failed",
            "overall_pass": False,
            "gate_results": {
                "P27.8_geometry_quality": "passed",
                "P27.9_global_incidence": p9_status,
                "P27.10_local_links": p10_status,
                "P27.11_geometric_embedding": p11_status,
                "P27.12_oriented_boundary": status,
            },
            "geometry_audit": geometry,
            "boundary_audit": boundary,
            "all_required_gates_passed": False,
            "physical_ccfsm_positivity_certified": False,
        }

    embedding = boundary["geometric_embedding_audit"]
    links = embedding["base_link_audit"]
    incidence = links["base_incidence_audit"]
    gates = {
        "P27.8_geometry_quality": "passed",
        "P27.9_global_incidence": incidence.get("status", "not_passed"),
        "P27.10_local_links": links.get("status", "not_passed"),
        "P27.11_geometric_embedding": embedding.get("status", "not_passed"),
        "P27.12_oriented_boundary": boundary.get("status", "not_passed"),
    }
    passed = all(value in (
        "passed", "incidence_audited", "locally_manifold_audited",
        "geometric_embedding_audited", "oriented_boundary_audited")
        for value in gates.values())
    return {
        "status": "integrated_mesh_audited" if passed else "integrated_mesh_audit_failed",
        "overall_pass": passed,
        "gate_results": gates,
        "mesh_summary": {
            "vertex_count": len(geometry["vertices"]),
            "tetrahedron_count": len(geometry["tetrahedra"]),
            "minimum_quality_ratio": geometry["minimum_quality_ratio"],
            "maximum_quality_ratio": geometry["maximum_quality_ratio"],
            "negative_orientation_flips": geometry["negative_orientation_flips"],
            "face_connected_component_count": incidence["component_count"],
            "boundary_component_count": boundary["boundary_component_count"],
            "boundary_triangle_count": boundary["boundary_triangle_count"],
            "boundary_edge_count": boundary["boundary_edge_count"],
            "boundary_signed_volume": boundary["boundary_signed_volume"],
            "tetrahedron_signed_volume_sum": boundary["tetrahedron_signed_volume_sum"],
            "exact_volume_balance": boundary["exact_volume_balance"],
        },
        "geometry_audit": geometry,
        "incidence_audit": incidence,
        "local_link_audit": links,
        "embedding_audit": embedding,
        "oriented_boundary_audit": boundary,
        "all_required_gates_passed": passed,
        "exact_arithmetic_for_geometry_and_volume": True,
        "pairwise_embedding_check_complexity": "O(number_of_tetrahedra^2)",
        "boundary_self_intersection_fully_certified": False,
        "all_lower_dimensional_nonincident_intersections_checked": False,
        "finite_element_conditioning_certified": False,
        "physical_ccfsm_positivity_certified": False,
        "discrete_energy_closure_certified": False,
        "physical_validation_certified": False,
    }
