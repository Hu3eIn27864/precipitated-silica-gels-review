import unittest

from ccfsm_p2_chemical_affinity import ChemicalParametersP2
from ccfsm_p3_reaction_diffusion import (
    P3Grid, p3_regularized_bridge_fraction, p3_rhs, p3_total_silicon,
)


class TestCCFSMP3ReactionDiffusion(unittest.TestCase):
    def setUp(self):
        self.grid = P3Grid((3, 2, 2), (1e-6, 2e-6, 3e-6))
        self.params = ChemicalParametersP2(
            100.0, 298.15, (0.2, 0.1, 0.05), (2.0, 0.5, 1.5)
        )
        self.fields = (
            tuple(80.0 - i for i in range(12)),
            tuple(15.0 + 0.2 * i for i in range(12)),
            tuple(4.0 + 0.1 * i for i in range(12)),
            tuple(1.0 + 0.05 * i for i in range(12)),
        )

    def test_global_si_conservation_of_semidiscrete_rhs(self):
        rhs = p3_rhs(self.fields, self.grid, (1e-10, 2e-10, 3e-10, 4e-10),
                     0.35, self.params)
        self.assertAlmostEqual(sum(sum(f) for f in rhs), 0.0, places=10)

    def test_no_flux_diffusion_conserves_each_species_without_reaction(self):
        # Set all reaction rates to zero: only internal face fluxes remain.
        p = ChemicalParametersP2(100.0, 298.15, (0.0, 0.0, 0.0), (2.0, 0.5, 1.5))
        rhs = p3_rhs(self.fields, self.grid, (1e-10, 2e-10, 3e-10, 4e-10),
                     0.35, p)
        for species_rhs in rhs:
            self.assertAlmostEqual(sum(species_rhs), 0.0, places=10)

    def test_uniform_field_has_zero_diffusion_contribution(self):
        uniform = tuple((value,) * self.grid.cell_count
                        for value in (80.0, 15.0, 4.0, 1.0))
        p = ChemicalParametersP2(100.0, 298.15, (0.0, 0.0, 0.0), (2.0, 0.5, 1.5))
        rhs = p3_rhs(uniform, self.grid, (1e-10,)*4, 0.5, p)
        for species_rhs in rhs:
            self.assertTrue(all(abs(v) < 1e-20 for v in species_rhs))

    def test_single_cell_recovers_p2_reaction_rhs(self):
        grid = P3Grid((1, 1, 1), (1.0, 1.0, 1.0))
        state = tuple((v,) for v in (80.0, 15.0, 4.0, 1.0))
        rhs = p3_rhs(state, grid, (1e-9,)*4, 0.4, self.params)
        self.assertAlmostEqual(sum(f[0] for f in rhs), 0.0, places=12)

    def test_porosity_weighted_total(self):
        total = p3_total_silicon(self.fields, self.grid, 0.35)
        self.assertGreater(total, 0.0)
        self.assertAlmostEqual(total, 0.35 * self.grid.cell_volume *
                               sum(sum(f) for f in self.fields))

    def test_regularized_bridge_fraction_bounds_and_empty_network(self):
        self.assertGreaterEqual(p3_regularized_bridge_fraction(2.0, 1.0, 0.1), 0.0)
        self.assertLessEqual(p3_regularized_bridge_fraction(2.0, 1.0, 0.1), 1.0)
        self.assertEqual(p3_regularized_bridge_fraction(0.0, 0.0, 0.1), 0.0)

    def test_rejects_invalid_grid_or_concentration(self):
        with self.assertRaises(ValueError):
            P3Grid((2, 2), (1.0,))
        bad = ((-1.0,), (0.0,), (0.0,), (0.0,))
        with self.assertRaises(ValueError):
            p3_rhs(bad, P3Grid((1,), (1.0,)), (1.0,)*4, 0.4, self.params)

    def test_rejects_nonpositive_diffusivity(self):
        with self.assertRaises(ValueError):
            p3_rhs(tuple((1.0,) for _ in range(4)), P3Grid((1,), (1.0,)),
                   (1.0, 0.0, 1.0, 1.0), 0.4, self.params)


if __name__ == "__main__":
    unittest.main()
