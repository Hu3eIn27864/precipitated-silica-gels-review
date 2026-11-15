import unittest
from fractions import Fraction as F

from ccfsm_p27_14_3d_field_positivity import audit_tetra_scalar_field_3d


class TestP2714(unittest.TestCase):
    def setUp(self):
        self.vertices = ((0,0,0),(1,0,0),(0,1,0),(0,0,1))
        self.tetrahedra = ((0,1,2,3),)

    def test_exact_p1_nonnegative_and_margin(self):
        r = audit_tetra_scalar_field_3d(
            self.vertices, self.tetrahedra,
            ({"degree":1,"vertex_values":(1,2,3,4)},),
            min_certified_margin=F(1))
        self.assertTrue(r["overall_pass"])
        self.assertEqual(r["minimum_certified_lower_margin"], F(1))
        self.assertFalse(r["physical_ccfsm_positivity_certified"])

    def test_p1_negative_vertex_is_not_passed(self):
        r = audit_tetra_scalar_field_3d(
            self.vertices, self.tetrahedra,
            ({"degree":1,"vertex_values":(1,-1,3,4)},))
        self.assertEqual(r["status"], "field_positivity_unresolved")
        self.assertFalse(r["overall_pass"])

    def test_p2_subdivision_and_independent_verification(self):
        v=(F(17,16),F(17,16),F(1,16),F(1,16))
        e=(F(1,16),F(5,16),F(5,16),F(5,16),F(5,16),F(1,16))
        r=audit_tetra_scalar_field_3d(
            self.vertices,self.tetrahedra,
            ({"degree":2,"vertex_values":v,"edge_midpoint_values":e},),
            p2_max_depth=4)
        self.assertTrue(r["overall_pass"])
        self.assertTrue(r["cell_results"][0]["certificate_verified"])
        self.assertGreaterEqual(r["minimum_certified_lower_margin"],0)

    def test_p2_unresolved_is_not_negative_or_pass(self):
        v=(F(17,16),F(17,16),F(1,16),F(1,16))
        e=(F(1,16),F(5,16),F(5,16),F(5,16),F(5,16),F(1,16))
        r=audit_tetra_scalar_field_3d(
            self.vertices,self.tetrahedra,
            ({"degree":2,"vertex_values":v,"edge_midpoint_values":e},),
            p2_max_depth=0)
        self.assertEqual(r["status"],"field_positivity_unresolved")
        self.assertFalse(r["overall_pass"])

    def test_mesh_gate_precedes_field_audit(self):
        bad=((0,1,2,3),(0,1,2,3))
        r=audit_tetra_scalar_field_3d(
            self.vertices,bad,
            ({"degree":1,"vertex_values":(1,1,1,1)},)*2)
        self.assertEqual(r["status"],"mesh_gate_failed")

    def test_margin_threshold_is_separate_from_nonnegativity(self):
        r=audit_tetra_scalar_field_3d(
            self.vertices,self.tetrahedra,
            ({"degree":1,"vertex_values":(F(1,10),1,1,1)},),
            min_certified_margin=F(1,5))
        self.assertEqual(r["status"],"field_nonnegative_but_margin_below_threshold")
        self.assertTrue(r["all_cells_certified_nonnegative"])
        self.assertFalse(r["overall_pass"])

    def test_bad_cell_count_and_degree(self):
        r=audit_tetra_scalar_field_3d(self.vertices,self.tetrahedra,())
        self.assertEqual(r["status"],"cell_field_count_mismatch")
        r=audit_tetra_scalar_field_3d(
            self.vertices,self.tetrahedra,({"degree":3},))
        self.assertEqual(r["status"],"field_positivity_unresolved")


if __name__ == "__main__":
    unittest.main()
