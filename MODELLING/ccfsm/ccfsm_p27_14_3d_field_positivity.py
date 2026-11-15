"""P27.14: integrated exact 3-D scalar positivity and coefficient-margin audit.

The module first requires the P27.13 mesh gates, then checks cellwise P1
nodal data or P2 tetrahedral Bernstein/subdivision certificates. It reports
certified lower margins separately from unresolved/negative cases. This is
a discrete scalar-field audit, not a proof of coupled CCFSM state invariance,
time-step stability, FE coercivity, or physical validity.
"""
from fractions import Fraction

from ccfsm_p27_13_integrated_mesh_audit import audit_tetra_mesh_3d
from ccfsm_p27_1_tetra_p1_positivity import verify_tetra_p1_positivity
from ccfsm_p27_3_tetra_p2_subdivision import certify_tetra_p2_by_subdivision
from ccfsm_p27_4_tetra_p2_certificate_verifier import verify_p27_3_certificate


def audit_tetra_scalar_field_3d(
    vertices, tetrahedra, cell_fields, *, p2_max_depth=6,
    min_certified_margin=0,
):
    """Audit one P1 or P2 scalar polynomial per tetrahedron.

    Each cell_fields entry is either
      {"degree": 1, "vertex_values": (v0,v1,v2,v3)}
    or
      {"degree": 2, "vertex_values": (...), "edge_midpoint_values": (...)}.
    P2 edge order is (01,02,03,12,13,23), matching P27.2.
    """
    try:
        threshold = (min_certified_margin if isinstance(min_certified_margin, Fraction)
                     else Fraction(str(min_certified_margin)))
        if threshold < 0:
            return {"status": "invalid_margin_threshold", "overall_pass": False}
        if not isinstance(p2_max_depth, int) or isinstance(p2_max_depth, bool) or p2_max_depth < 0:
            return {"status": "invalid_subdivision_depth", "overall_pass": False}
        mesh = audit_tetra_mesh_3d(vertices, tetrahedra)
        if not mesh.get("overall_pass"):
            return {
                "status": "mesh_gate_failed", "overall_pass": False,
                "mesh_audit": mesh, "cell_results": (),
                "physical_ccfsm_positivity_certified": False,
            }
        if len(cell_fields) != len(tetrahedra):
            return {"status": "cell_field_count_mismatch", "overall_pass": False,
                    "mesh_audit": mesh, "cell_results": ()}

        results = []
        margins = []
        for cell_id, (cell, data) in enumerate(zip(tetrahedra, cell_fields)):
            if not isinstance(data, dict):
                results.append({"cell": cell_id, "status": "unresolved",
                                "reason": "malformed_cell_field"})
                continue
            points = tuple(vertices[i] for i in cell)
            degree = data.get("degree")
            if degree == 1:
                check = verify_tetra_p1_positivity(points, data.get("vertex_values", ()))
                if check.get("verified"):
                    margin = check["minimum_nodal_value"]
                    status = "certified_nonnegative" if margin >= 0 else "certified_negative"
                    results.append({"cell": cell_id, "degree": 1, "status": status,
                                    "certified_lower_margin": margin,
                                    "minimum_nodal_value": margin})
                    margins.append(margin)
                else:
                    results.append({"cell": cell_id, "degree": 1, "status": "unresolved",
                                    "reason": check.get("reason", "p1_check_failed")})
            elif degree == 2:
                vv = data.get("vertex_values", ())
                ev = data.get("edge_midpoint_values", ())
                cert = certify_tetra_p2_by_subdivision(
                    points, vv, ev, max_depth=p2_max_depth)
                verified = verify_p27_3_certificate(points, vv, ev, cert)
                if not verified.get("verified"):
                    results.append({"cell": cell_id, "degree": 2, "status": "unresolved",
                                    "reason": "independent_certificate_verification_failed",
                                    "verifier": verified})
                    continue
                status = cert["status"]
                margin = None
                if status == "certified_nonnegative":
                    leaf_mins = [min(record["bernstein_coefficients"])
                                 for record in cert["leaf_records"]]
                    margin = min(leaf_mins)
                    margins.append(margin)
                results.append({
                    "cell": cell_id, "degree": 2, "status": status,
                    "certified_lower_margin": margin,
                    "certificate_verified": True,
                    "certificate": cert,
                })
            else:
                results.append({"cell": cell_id, "status": "unresolved",
                                "reason": "unsupported_polynomial_degree"})
        all_positive = len(results) == len(tetrahedra) and all(
            item.get("status") == "certified_nonnegative" for item in results)
        margin_pass = all_positive and all(value >= threshold for value in margins)
        if all_positive and margin_pass:
            status = "field_nonnegative_and_margin_certified"
        elif all_positive:
            status = "field_nonnegative_but_margin_below_threshold"
        elif any(item.get("status") == "certified_negative_point"
                 or item.get("status") == "certified_negative" for item in results):
            status = "field_negative_witness_found"
        else:
            status = "field_positivity_unresolved"
        return {
            "status": status, "overall_pass": margin_pass,
            "mesh_audit": mesh, "cell_results": tuple(results),
            "minimum_certified_lower_margin": min(margins) if margins else None,
            "required_minimum_margin": threshold,
            "all_cells_certified_nonnegative": all_positive,
            "margin_threshold_passed": margin_pass,
            "exact_rational_arithmetic": True,
            "p2_certificates_independently_verified": all(
                item.get("degree") != 2 or item.get("certificate_verified", False)
                for item in results if item.get("degree") is not None),
            "coupled_ccfsm_state_invariance_certified": False,
            "time_step_stability_certified": False,
            "finite_element_coercivity_certified": False,
            "physical_ccfsm_positivity_certified": False,
        }
    except (TypeError, ValueError, ZeroDivisionError, KeyError, IndexError):
        return {"status": "invalid_or_malformed_input", "overall_pass": False,
                "physical_ccfsm_positivity_certified": False}
