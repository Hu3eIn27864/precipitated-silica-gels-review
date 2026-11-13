#!/usr/bin/env python3
"""Verification for exact interface-aware storage and hydraulic resistance."""
import math
import unittest
from interface_aware_1d import solve_interface_aware
from layered_reference import two_layer_mean_pressure_ratio


class InterfaceAwareTests(unittest.TestCase):
    def test_uniform_material_matches_homogeneous_reference(self):
        r=solve_interface_aware([0.0,1.0],[1.0],[1.0],80,1.0,2e-5,100)
        exact=(8.0/math.pi**2)*sum(math.exp(-(2*k+1)**2*math.pi**2*0.002)/(2*k+1)**2 for k in range(500))
        self.assertAlmostEqual(r["mean_pressure_pa"][-1],exact,delta=2e-4)

    def test_off_grid_interface_matches_fixed_interface_series(self):
        a=0.37; L=1.0; t=0.005
        exact=two_layer_mean_pressure_ratio(t,1.0,1.0,2.0,0.15,L,a,180)
        errors=[]
        for n in (40,80,160):
            r=solve_interface_aware([0.0,a,L],[1.0,2.0],[1.0,0.15],
                                    n,L,2e-6,round(t/2e-6))
            errors.append(abs(r["mean_pressure_pa"][-1]-exact))
        self.assertLess(errors[1],errors[0])
        self.assertLess(errors[2],errors[1])
        self.assertLess(errors[-1],8e-4)

    def test_exact_cell_storage_and_crossed_face_resistance(self):
        # Interface x=.37 cuts the cell [0.35,.40] and the centre-to-centre
        # segment [0.3625,.3875]. Both integrals are exact.
        r=solve_interface_aware([0,.37,1],[1,2],[1,.1],40,1,1e-4,1)
        cap=r["cell_capacity_pa_inv_m"]
        self.assertAlmostEqual(cap[14],.02*1.0 + .005*2.0,places=14)
        resistance=.0075/1.0 + .0175/.1
        self.assertAlmostEqual(r["face_conductance_m_pa_s"][15],1/resistance,places=12)

    def test_global_conservation_and_positive_solution(self):
        r=solve_interface_aware([0,.37,.72,1],[1,2,.7],[1,.15,.6],
                                73,1,1e-5,100)
        self.assertLess(max(abs(v) for v in r["balance_residual_m"][1:]),2e-12)
        self.assertTrue(all(v>=0 for row in r["profiles_pa"] for v in row))
        self.assertTrue(all(b<a for a,b in zip(r["mean_pressure_pa"],r["mean_pressure_pa"][1:])))

    def test_invalid_layer_partition_rejected(self):
        with self.assertRaises(ValueError):
            solve_interface_aware([0,.5,.4,1],[1,2,3],[1,1,1],20,1,1e-4,1)


if __name__=="__main__":
    unittest.main()
