import math
import unittest

from ccfsm_p6_convexity import mobile_entropy_hessian_form, bridge_eigenstrain_norm_bound


class TestCCFSMP6Convexity(unittest.TestCase):
    def test_mobile_entropy_hessian_is_nonnegative(self):
        cases = [((30.0,20.0),0.36,(1.0,-2.0),0.03,8.314462618*298.15),
                 ((1e-4,2e-3),0.2,(-1e-5,7e-4),-0.01,2500.0),
                 ((4.0,9.0),1.0,(2.0,4.5),0.5,100.0)]
        for args in cases:
            self.assertGreaterEqual(mobile_entropy_hessian_form(*args), 0.0)

    def test_exact_scaling_null_direction(self):
        m, theta, scale = (30.0,20.0), 0.4, 0.17
        value = mobile_entropy_hessian_form(m,theta,(scale*m[0],scale*m[1]),scale*theta,2500.0)
        self.assertAlmostEqual(value, 0.0, delta=1e-25)

    def test_hessian_scales_linearly_with_rt(self):
        args=((3.0,7.0),0.5,(0.2,-0.4),0.01)
        self.assertAlmostEqual(mobile_entropy_hessian_form(*args,300.0),
                               3*mobile_entropy_hessian_form(*args,100.0),delta=1e-12)

    def test_eigenstrain_bound_is_sharp_and_contains_samples(self):
        beta,b0=0.03,0.35
        bound=bridge_eigenstrain_norm_bound(beta,b0)
        self.assertAlmostEqual(bound,math.sqrt(3)*beta*max(b0,1-b0))
        for b in (0.0,b0,0.5,1.0):
            self.assertLessEqual(math.sqrt(3)*abs(beta*(b-b0)),bound+1e-15)

    def test_rejects_invalid_arguments(self):
        with self.assertRaises(ValueError):
            mobile_entropy_hessian_form((1.0,0.0),1.0,(1.0,1.0),0.0,1.0)
        with self.assertRaises(ValueError):
            bridge_eigenstrain_norm_bound(-1.0,0.5)
        with self.assertRaises(ValueError):
            bridge_eigenstrain_norm_bound(1.0,1.2)


if __name__ == "__main__":
    unittest.main()
