import unittest
from fractions import Fraction
from ccfsm_p27_12_oriented_boundary_audit import audit_tetra_mesh_boundary


class TestP2712(unittest.TestCase):
    def test_single_tetrahedron_closed_oriented_boundary(self):
        v=((0,0,0),(1,0,0),(0,1,0),(0,0,1))
        r=audit_tetra_mesh_boundary(v,((0,1,2,3),))
        self.assertEqual(r["status"],"oriented_boundary_audited")
        self.assertTrue(r["closed_boundary"])
        self.assertEqual(r["boundary_triangle_count"],4)
        self.assertEqual(r["boundary_components"][0]["euler_characteristic"],2)
        self.assertEqual(r["boundary_signed_volume"],Fraction(1,6))
        self.assertTrue(r["exact_volume_balance"])

    def test_two_tetrahedra_sharing_face(self):
        v=((0,0,0),(1,0,0),(0,1,0),(0,0,1),(0,0,-1))
        r=audit_tetra_mesh_boundary(v,((0,1,2,3),(1,0,2,4)))
        self.assertEqual(r["status"],"oriented_boundary_audited")
        self.assertEqual(r["boundary_triangle_count"],6)
        self.assertEqual(r["boundary_component_count"],1)
        self.assertEqual(r["boundary_signed_volume"],Fraction(1,3))

    def test_disconnected_components_are_reported_separately(self):
        v=((0,0,0),(1,0,0),(0,1,0),(0,0,1),
           (3,0,0),(4,0,0),(3,1,0),(3,0,1))
        r=audit_tetra_mesh_boundary(v,((0,1,2,3),(4,5,6,7)))
        self.assertEqual(r["status"],"oriented_boundary_audited")
        self.assertEqual(r["boundary_component_count"],2)
        self.assertTrue(all(c["euler_characteristic"]==2
                            for c in r["boundary_components"]))

    def test_exact_volume_balance(self):
        v=((0,0,0),(2,0,0),(0,2,0),(0,0,2))
        r=audit_tetra_mesh_boundary(v,((0,1,2,3),))
        self.assertEqual(r["tetrahedron_signed_volume_sum"],Fraction(4,3))
        self.assertEqual(r["boundary_signed_volume"],Fraction(4,3))
        self.assertEqual(r["volume_balance_residual"],0)

    def test_base_failure_propagates(self):
        v=((0,0,0),(1,0,0),(0,1,0),(0,0,1),
           (0,0,-1),(0,0,2))
        r=audit_tetra_mesh_boundary(v,((0,1,2,3),(1,0,2,4),(0,1,2,5)))
        self.assertEqual(r["status"],"base_audit_failed")


if __name__=="__main__":
    unittest.main()
