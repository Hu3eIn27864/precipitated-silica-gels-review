import math
import unittest

from ccfsm_p2_chemical_affinity import (
    ChemicalParametersP2, ChemicalStateP2, chemical_free_energy_density,
    evaluate_p2_rates, p2_rhs,
)


class TestCCFSMP2ChemicalAffinity(unittest.TestCase):
    def setUp(self):
        self.p = ChemicalParametersP2(
            reference_concentration=100.0,
            temperature_k=298.15,
            rate_constants_s=(0.2, 0.1, 0.05),
            equilibrium_constants=(2.0, 0.5, 1.5),
        )
        self.y = ChemicalStateP2(80.0, 15.0, 4.0, 1.0)

    def test_silicon_mass_conservation_rhs(self):
        rhs = p2_rhs(self.y, self.p)
        self.assertAlmostEqual(sum(rhs), 0.0, places=12)

    def test_rates_and_affinities_have_same_sign(self):
        result = evaluate_p2_rates(self.y, self.p)
        for rate, affinity in zip(result.reaction_rates, result.affinities_j_mol):
            self.assertGreaterEqual(rate * affinity, -1e-12)

    def test_nonnegative_dissipation(self):
        result = evaluate_p2_rates(self.y, self.p)
        self.assertGreaterEqual(result.chemical_dissipation_w_m3, 0.0)
        self.assertAlmostEqual(result.free_energy_rate_w_m3,
                               -result.entropy_production_w_m3)

    def test_equilibrium_reaction_has_zero_rate(self):
        # a_right = K*a_left for the first reaction
        y = ChemicalStateP2(50.0, 100.0, 0.0, 0.0)
        result = evaluate_p2_rates(y, self.p)
        self.assertAlmostEqual(result.reaction_rates[0], 0.0, places=12)
        self.assertAlmostEqual(result.affinities_j_mol[0], 0.0, places=12)

    def test_bridge_fraction_bounds(self):
        self.assertAlmostEqual(self.y.bridge_fraction, 0.2)
        self.assertIsNone(ChemicalStateP2(1.0, 0.0, 0.0, 0.0).bridge_fraction)

    def test_total_silicon_state(self):
        self.assertAlmostEqual(self.y.total_silicon, 100.0)

    def test_free_energy_finite_for_zero_pools(self):
        y = ChemicalStateP2(100.0, 0.0, 0.0, 0.0)
        self.assertTrue(math.isfinite(chemical_free_energy_density(y, self.p)))

    def test_rejects_negative_concentrations(self):
        with self.assertRaises(ValueError):
            ChemicalStateP2(1.0, -1.0, 0.0, 0.0)

    def test_rejects_invalid_parameters(self):
        with self.assertRaises(ValueError):
            ChemicalParametersP2(100.0, 298.15, (1.0, 2.0), (1.0, 1.0, 1.0))

    def test_activity_coefficients_affect_affinity(self):
        p2 = ChemicalParametersP2(
            100.0, 298.15, (0.2, 0.1, 0.05), (2.0, 0.5, 1.5),
            (0.5, 1.0, 1.0, 1.0))
        a = evaluate_p2_rates(self.y, self.p)
        b = evaluate_p2_rates(self.y, p2)
        self.assertNotEqual(a.affinities_j_mol[0], b.affinities_j_mol[0])


if __name__ == "__main__":
    unittest.main()
