import unittest
from ccfsm_p26_1_moment_projection import limited_linear_slopes, moments, project_linear_moments

class TestP261MomentProjection(unittest.TestCase):
    def test_linear_field_exact_on_nonmatching_meshes(self):
        se=(0,.08,.24,.51,.76,1); te=(0,.13,.31,.58,.83,1)
        src=tuple(2+3*(a+b)/2 for a,b in zip(se,se[1:]))
        ss=limited_linear_slopes(se,src)
        self.assertTrue(all(abs(s-3)<1e-13 for s in ss))
        dst,ds=project_linear_moments(se,src,ss,te)
        for a,b,u,s in zip(te,te[1:],dst,ds):
            self.assertAlmostEqual(u,2+3*(a+b)/2,places=13)
            self.assertAlmostEqual(s,3,places=12)
    def test_preserves_global_mass_and_first_moment(self):
        se=(0,.08,.24,.51,.76,1); te=(0,.13,.31,.58,.83,1)
        src=tuple(2+3*(a+b)/2 for a,b in zip(se,se[1:])); ss=limited_linear_slopes(se,src)
        dst,ds=project_linear_moments(se,src,ss,te)
        sm,sf=moments(se,src,ss); tm,tf=moments(te,dst,ds)
        self.assertAlmostEqual(sm,tm,places=13); self.assertAlmostEqual(sf,tf,places=13)
    def test_constant_field(self):
        se=(0,.2,.6,1); te=(0,.1,.35,.8,1); src=(4.,)*3
        ss=limited_linear_slopes(se,src); dst,ds=project_linear_moments(se,src,ss,te)
        self.assertTrue(all(abs(x-4)<1e-14 for x in dst)); self.assertTrue(all(abs(x)<1e-14 for x in ds))
    def test_identity_mesh(self):
        e=(0,.2,.5,1); u=(1.,3.,2.); s=(.5,-.2,.3)
        out, slopes=project_linear_moments(e,u,s,e)
        self.assertEqual(out,u)
        for actual, expected in zip(slopes,s): self.assertAlmostEqual(actual,expected,places=12)
    def test_positivity_limiter_bounds_reconstruction(self):
        e=(0,.2,.5,1); u=(.1,2.,.2); s=limited_linear_slopes(e,u,positivity=True)
        for a,b,v,g in zip(e,e[1:],u,s):
            c=(a+b)/2
            self.assertGreaterEqual(v-abs(g)*(b-a)/2,-1e-14)
    def test_rejects_negative_averages_with_positivity(self):
        with self.assertRaises(ValueError): limited_linear_slopes((0,.5,1),(-1.,2.))
    def test_rejects_domain_mismatch(self):
        with self.assertRaises(ValueError): project_linear_moments((0,.5,1),(1,2),(0,0),(0,.4,.9))
    def test_rejects_bad_slope_length(self):
        with self.assertRaises(ValueError): project_linear_moments((0,.5,1),(1,2),(0,),(0,.25,.75,1))
if __name__=="__main__": unittest.main()
