import math
import unittest

from ccfsm_p2_chemical_affinity import ChemicalParametersP2
from ccfsm_p8_variable_capacity import P8Grid
from ccfsm_p9_mechanical_feedback import P9Parameters
from ccfsm_p11_energy_time_integration import (
    P11State, p11_advance, p11_total_free_energy
)


class TestCCFSMP11EnergyTimeIntegration(unittest.TestCase):
    def setUp(self):
        self.grid = P8Grid(3, 0.01)
        self.chem = ChemicalParametersP2(
            100.0, 298.15, (0.2, 0.1, 0.05), (2.0, 0.5, 1.5),
            (1.0, 1.1, 0.9, 1.05))
        self.no_reaction = ChemicalParametersP2(
            100.0, 298.15, (0.0, 0.0, 0.0), (2.0, 0.5, 1.5),
            (1.0, 1.1, 0.9, 1.05))
        self.mech = P9Parameters(
            lame_lambda_pa=2.0e6, shear_modulus_pa=1.0e6,
            biot_modulus_pa=1.0e7, biot_coefficient=0.8,
            bridge_eigenstrain=0.01, bridge_reference=15.0/51.0,
            bridge_regularization=1.0, reference_fluid_capacity=0.3,
            reference_axial_strain=0.0,
            reference_permeability_m2_per_pas=1.0e-12,
            bridge_permeability_sensitivity=2.0,
            strain_permeability_sensitivity=5.0,
            reference_bridge_fraction=15.0/51.0)

    def state(self):
        return P11State(
            (0.30, 0.30, 0.30),
            ((30., 30., 30.), (20., 20., 20.),
             (35., 35., 35.), (15., 15., 15.)), 0.0)

    def test_reaction_step_decreases_discrete_free_energy(self):
        s = self.state()
        e0 = p11_total_free_energy(s, self.grid, self.mech, self.chem)
        result = p11_advance(s, 1e-3, self.grid, self.mech, self.chem,
            (0., 0.), 0.0)
        self.assertLessEqual(result["free_energy_after_j_m2"],
                             result["free_energy_before_j_m2"] + 1e-11)
        self.assertLess(result["free_energy_after_j_m2"], e0)
        self.assertGreater(result["accepted_dt_s"], 0.0)
        self.assertGreaterEqual(result["backtracks"], 0)

    def test_closed_step_preserves_total_silicon_and_fluid_capacity(self):
        s = self.state()
        result = p11_advance(s, 1e-4, self.grid, self.mech, self.no_reaction,
            (0., 0.), 0.0)
        self.assertAlmostEqual(result["total_silicon_after_mol_m2"],
                               result["total_silicon_before_mol_m2"], delta=1e-10)
        self.assertAlmostEqual(result["fluid_capacity_after_m"],
                               result["fluid_capacity_before_m"], delta=1e-12)

    def test_state_remains_strictly_positive_and_bounded(self):
        result = p11_advance(self.state(), 1e-3, self.grid, self.mech,
            self.chem, (0., 0.), 0.0)
        s = result["state"]
        self.assertTrue(all(0.0 < x <= 1.0 for x in s.fluid_capacity))
        self.assertTrue(all(x > 0.0 for f in s.inventories for x in f))
        self.assertTrue(all(math.isfinite(x) for f in s.inventories for x in f))

    def test_zero_reaction_equilibrium_is_stationary(self):
        s = self.state()
        result = p11_advance(s, 1e-3, self.grid, self.mech,
            self.no_reaction, (0., 0.), 0.0)
        self.assertEqual(result["state"].fluid_capacity, s.fluid_capacity)
        self.assertEqual(result["state"].inventories, s.inventories)
        self.assertAlmostEqual(result["free_energy_change_j_m2"], 0.0, delta=1e-12)

    def test_nonzero_applied_traction_is_rejected(self):
        from dataclasses import replace
        loaded = replace(self.mech, applied_axial_traction_pa=1.0e3)
        with self.assertRaises(ValueError):
            p11_advance(self.state(), 1e-4, self.grid, loaded, self.no_reaction,
                (0., 0.), 0.0)

    def test_open_boundary_is_rejected(self):
        s = self.state()
        with self.assertRaises(ValueError):
            p11_advance(s, 1e-4, self.grid, self.mech, self.no_reaction,
                (1e-10, 1e-10), 1e5, (0., 0.), (0., 0.))

    def test_invalid_dt_and_state_are_rejected(self):
        s = self.state()
        with self.assertRaises(ValueError):
            p11_advance(s, 0.0, self.grid, self.mech, self.chem,
                (0., 0.), 0.0)
        bad = P11State((0.3, 0.3, 0.3),
            ((30., 30., 30.), (20., 20., 20.),
             (35., 35., 35.), (15., 15., 0.)), 0.0)
        with self.assertRaises(ValueError):
            p11_total_free_energy(bad, self.grid, self.mech, self.chem)


if __name__ == "__main__":
    unittest.main()
