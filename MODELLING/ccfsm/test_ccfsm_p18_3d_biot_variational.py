import math
import unittest
from ccfsm_p18_3d_biot_variational import (
    P18Parameters, p18_3d_state, p18_plane_strain,
    p18_uniaxial_stress_free_laterals)


class TestCCFSMP18(unittest.TestCase):
    def setUp(self):
        self.p = P18Parameters(2.0e6, 1.0e6, 1.0e7, 0.8)

    def test_stress_is_energy_derivative_for_each_normal_component(self):
        eps = [0.012, -0.003, 0.004]
        c, z, h = 0.002, 0.006, 1e-7
        def energy(v):
            s = p18_3d_state(((v[0],0,0),(0,v[1],0),(0,0,v[2])),
                             c, z, self.p)
            return s["total_mechanical_energy_j_m3"]
        state = p18_3d_state(((eps[0],0,0),(0,eps[1],0),(0,0,eps[2])),
                             c, z, self.p)
        for i in range(3):
            plus, minus = eps[:], eps[:]
            plus[i] += h
            minus[i] -= h
            derivative = (energy(plus)-energy(minus))/(2*h)
            self.assertAlmostEqual(derivative, state["stress_pa"][i][i],
                                   delta=2e-3)

    def test_shear_stress_energy_conjugacy(self):
        e = ((0.01,0.002,0),(0.002,-0.001,0),(0,0,0.003))
        s = p18_3d_state(e, 0.001, 0.002, self.p)
        self.assertAlmostEqual(s["stress_pa"][0][1],
                               2*self.p.shear_modulus_pa*0.002)

    def test_plane_strain_matches_p17_formula(self):
        e, c, z, t = 0.01, 0.002, 0.006, 25000.0
        p = self.p
        h, ce = p.lame_lambda_pa+2*p.shear_modulus_pa, (
            3*p.lame_lambda_pa+2*p.shear_modulus_pa)
        pressure = p.biot_modulus_pa*(z-p.biot_coefficient*ce*c/h
            -p.biot_coefficient*t/h)/(1+p.biot_modulus_pa*
            p.biot_coefficient**2/h)
        strain = (t+ce*c+p.biot_coefficient*pressure)/h
        r = p18_plane_strain(strain,c,z,p,t)
        self.assertAlmostEqual(r["pore_pressure_pa"],pressure,delta=1e-8)
        self.assertAlmostEqual(r["stress_pa"][0][0],t,delta=1e-7)

    def test_uniaxial_stress_free_lateral_faces(self):
        r = p18_uniaxial_stress_free_laterals(0.002,0.006,25000.,self.p)
        self.assertLess(abs(r["axial_traction_residual_pa"]),1e-7)
        self.assertLess(r["lateral_traction_residual_pa"],1e-7)
        self.assertLess(abs(r["pressure_solution_residual_pa"]),1e-7)
        self.assertTrue(math.isfinite(r["total_mechanical_energy_j_m3"]))

    def test_zero_eigenstrain_zero_load_reference(self):
        r = p18_uniaxial_stress_free_laterals(0.0,0.0,0.0,self.p)
        self.assertAlmostEqual(r["axial_strain"],0.0,delta=1e-14)
        self.assertAlmostEqual(r["lateral_strain"],0.0,delta=1e-14)
        self.assertAlmostEqual(r["pore_pressure_pa"],0.0,delta=1e-14)

    def test_rejects_nonsymmetric_strain(self):
        with self.assertRaises(ValueError):
            p18_3d_state(((0,1,0),(0,0,0),(0,0,0)),0,0,self.p)


if __name__ == "__main__":
    unittest.main()
