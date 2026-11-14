import math
import unittest
from ccfsm_p2_chemical_affinity import ChemicalParametersP2
from ccfsm_p9_mechanical_feedback import P9Parameters, p9_cell_closure, p9_field_closure


class TestCCFSMP9MechanicalFeedback(unittest.TestCase):
    def setUp(self):
        self.chem = ChemicalParametersP2(
            100.0, 298.15, (0.2, 0.1, 0.05), (2.0, 0.5, 1.5),
            (1.0, 1.1, 0.9, 1.05))
        self.par = P9Parameters(
            lame_lambda_pa=2.0e6, shear_modulus_pa=1.0e6,
            biot_modulus_pa=1.0e7, biot_coefficient=0.8,
            bridge_eigenstrain=0.01, bridge_reference=15.0/51.0,
            bridge_regularization=1.0, reference_fluid_capacity=0.3,
            reference_axial_strain=0.0,
            reference_permeability_m2_per_pas=1.0e-12,
            bridge_permeability_sensitivity=2.0,
            strain_permeability_sensitivity=5.0,
            reference_bridge_fraction=0.2)

    def state(self, theta=0.3, sn=35.0, sb=15.0):
        return p9_cell_closure(theta, (30.0, 20.0), (sn, sb),
                               self.chem, self.par)

    def test_unloaded_reference_state_has_zero_pressure_and_strain(self):
        r = self.state()
        self.assertAlmostEqual(r["pore_pressure_pa"], 0.0, delta=1e-10)
        self.assertAlmostEqual(r["axial_strain"], 0.0, delta=1e-12)
        self.assertAlmostEqual(r["total_axial_stress_pa"], 0.0, delta=1e-10)

    def test_biot_fluid_content_identity(self):
        r = self.state(theta=0.31)
        self.assertAlmostEqual(r["fluid_content_residual"], 0.0, delta=1e-14)

    def test_variational_axial_stress_matches_energy_derivative(self):
        theta, sn, sb = 0.31, 34.0, 18.0
        r = p9_cell_closure(theta, (30., 20.), (sn, sb), self.chem, self.par)
        eps, eigen = r["axial_strain"], r["chemical_eigenstrain"]
        p = self.par
        h = 1e-7
        def mechanical_energy(e):
            trace = e-3.0*eigen
            diag = (e-eigen, -eigen, -eigen)
            zeta = theta-p.reference_fluid_capacity
            storage = 0.5*p.biot_modulus_pa*(zeta-p.biot_coefficient*e)**2
            elastic = (0.5*p.lame_lambda_pa*trace**2
                       +p.shear_modulus_pa*sum(x*x for x in diag))
            return elastic+storage
        derivative = (mechanical_energy(eps+h)-mechanical_energy(eps-h))/(2*h)
        self.assertAlmostEqual(derivative, r["total_axial_stress_pa"], delta=2e-3)

    def test_mechanical_equilibrium_matches_traction(self):
        p = P9Parameters(**{**self.par.__dict__,
                            "applied_axial_traction_pa": 2.5e4})
        r = p9_cell_closure(0.31, (30., 20.), (35., 15.), self.chem, p)
        self.assertAlmostEqual(r["total_axial_stress_pa"], 2.5e4, delta=1e-8)

    def test_permeability_is_positive_and_finite(self):
        r = self.state(theta=0.31, sb=25.0)
        self.assertGreater(r["intrinsic_permeability_m2_per_pas"], 0.0)
        self.assertTrue(math.isfinite(r["intrinsic_permeability_m2_per_pas"]))

    def test_bridge_increase_reduces_permeability_at_fixed_state(self):
        low = self.state(sb=10.0)
        high = self.state(sb=25.0)
        self.assertLess(high["intrinsic_permeability_m2_per_pas"],
                        low["intrinsic_permeability_m2_per_pas"])

    def test_field_closure_preserves_cell_order(self):
        fields = ((30., 31.), (20., 21.), (35., 34.), (15., 16.))
        r = p9_field_closure((0.30, 0.31), fields, self.chem, self.par)
        self.assertEqual(len(r["cells"]), 2)
        self.assertEqual(r["pore_pressure_pa"],
                         tuple(c["pore_pressure_pa"] for c in r["cells"]))

    def test_mechanical_potential_correction_only_network_pools(self):
        r = self.state()
        corr = r["mechanical_chemical_potential_correction_j_mol"]
        self.assertEqual(corr[:2], (0.0, 0.0))
        self.assertTrue(all(math.isfinite(x) for x in corr))

    def test_invalid_fluid_capacity_and_parameters_rejected(self):
        with self.assertRaises(ValueError):
            self.state(theta=0.0)
        with self.assertRaises(ValueError):
            self.state(theta=1.1)
        bad = P9Parameters(**{**self.par.__dict__,
                              "reference_permeability_m2_per_pas": 0.0})
        with self.assertRaises(ValueError):
            p9_cell_closure(0.3, (30., 20.), (35., 15.), self.chem, bad)


if __name__ == "__main__":
    unittest.main()
