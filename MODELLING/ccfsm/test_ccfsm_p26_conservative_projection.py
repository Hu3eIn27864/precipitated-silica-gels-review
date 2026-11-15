import unittest
from ccfsm_p26_conservative_projection import conservative_overlap_projection, integral, quadrature_to_cell_averages

class TestP26ConservativeProjection(unittest.TestCase):
    def test_nonmatching_mesh_preserves_integral(self):
        se=(0,.1,.33,.7,1); te=(0,.2,.4,.65,.9,1); v=(2.15,2.645,3.545,4.55)
        self.assertAlmostEqual(integral(se,v),integral(te,conservative_overlap_projection(se,v,te)),places=13)
    def test_constant_field(self):
        r=conservative_overlap_projection((0,.2,.6,1),(7.25,)*3,(0,.1,.35,.8,1))
        for x in r: self.assertAlmostEqual(x,7.25,places=14)
    def test_identity(self):
        e=(0,.2,.5,1); v=(1.,3.,2.)
        self.assertEqual(conservative_overlap_projection(e,v,e),v)
    def test_positive(self):
        self.assertTrue(all(x>0 for x in conservative_overlap_projection((0,.3,1),(1.,4.),(0,.1,.6,1))))
    def test_domain_mismatch_rejected(self):
        with self.assertRaises(ValueError): conservative_overlap_projection((0,.5,1),(1,2),(0,.4,.9))
    def test_bad_edges_rejected(self):
        with self.assertRaises(ValueError): conservative_overlap_projection((0,.7,.6,1),(1,2,3),(0,.5,1))
    def test_quadrature_reduction(self):
        self.assertEqual(quadrature_to_cell_averages((0,.5,1),(2.,4.,6.,8.),(1.,3.,2.,2.),(0,0,1,1)),(3.5,7.))
    def test_quadrature_validation(self):
        with self.assertRaises(ValueError): quadrature_to_cell_averages((0,.5,1),(1,2),(1,0),(0,1))
        with self.assertRaises(ValueError): quadrature_to_cell_averages((0,.5,1),(1,),(1,),(0,))
if __name__=="__main__": unittest.main()
