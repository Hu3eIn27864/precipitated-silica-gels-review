import unittest
from ccfsm_p26_2_quadratic_projection import limit_quadratic, moments, project_quadratic_moments, quadratic_minimum
class TestP262QuadraticProjection(unittest.TestCase):
    def test_quadratic_polynomial_exact_on_nonmatching_meshes(self):
        se=(0,.08,.24,.51,.76,1); te=(0,.13,.31,.58,.83,1); u=[]; a=[]; b=[]
        for x,y in zip(se,se[1:]):
            h=y-x; c=(x+y)/2; u.append(2+3*c+4*(c*c+h*h/12)); a.append(h*(3+8*c)); b.append(4*h*h)
        um,ua,ub=project_quadratic_moments(se,u,a,b,te)
        for x,y,m,aa,bb in zip(te,te[1:],um,ua,ub):
            h=y-x; c=(x+y)/2
            self.assertAlmostEqual(m,2+3*c+4*(c*c+h*h/12),places=12)
            self.assertAlmostEqual(aa,h*(3+8*c),places=12); self.assertAlmostEqual(bb,4*h*h,places=12)
    def test_preserves_global_three_raw_moments(self):
        se=(0,.08,.24,.51,.76,1); te=(0,.13,.31,.58,.83,1); u=[]; a=[]; b=[]
        for x,y in zip(se,se[1:]):
            h=y-x; c=(x+y)/2; u.append(2+3*c+4*(c*c+h*h/12)); a.append(h*(3+8*c)); b.append(4*h*h)
        dst=project_quadratic_moments(se,u,a,b,te)
        for x,y in zip(moments(se,u,a,b),moments(te,*dst)): self.assertAlmostEqual(x,y,places=12)
    def test_identity_mesh(self):
        e=(0,.2,.5,1); u=(1.,3.,2.); a=(.1,-.2,.3); b=(.04,.02,-.01)
        for old,new in zip((u,a,b),project_quadratic_moments(e,u,a,b,e)):
            for x,y in zip(old,new): self.assertAlmostEqual(x,y,places=12)
    def test_constant_field(self):
        z=(0.,0.,0.); out=project_quadratic_moments((0,.2,.6,1),(4.,4.,4.),z,z,(0,.1,.35,.8,1))
        self.assertTrue(all(abs(x-4)<1e-13 for x in out[0]))
        self.assertTrue(all(abs(x)<1e-13 for row in out[1:] for x in row))
    def test_local_maximum_and_minimum_curvature(self):
        self.assertAlmostEqual(quadratic_minimum(0.,-.6),-.05)
        self.assertAlmostEqual(quadratic_minimum(0.,.6),-.05)
    def test_positivity_limiter_preserves_average_and_bounds_polynomial(self):
        m,a,b=.1,.7,1.2; aa,bb=limit_quadratic(m,a,b,True)
        self.assertGreaterEqual(m+quadratic_minimum(aa,bb),-1e-14)
        self.assertLessEqual(abs(aa),abs(a)); self.assertLessEqual(abs(bb),abs(b))
    def test_positivity_rejects_negative_average(self):
        with self.assertRaises(ValueError):
            project_quadratic_moments((0,.5,1),(-1.,2.),(0.,0.),(0.,0.),(0,.25,.75,1),positivity=True)
    def test_domain_mismatch_and_bad_shapes(self):
        with self.assertRaises(ValueError): project_quadratic_moments((0,.5,1),(1,2),(0,0),(0,0),(0,.4,.9))
        with self.assertRaises(ValueError): project_quadratic_moments((0,.5,1),(1,2),(0,),(0,0),(0,.25,.75,1))
if __name__=="__main__": unittest.main()
