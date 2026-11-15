import unittest

from ccfsm_p25_1_refinement_study import (
    consistent_reference_inputs, restrict_cell_averages, restrict_state,
)


class TestP251CrossMesh(unittest.TestCase):
    def test_restriction_preserves_integral(self):
        fine = (1.0, 2.0, 4.0, 8.0, 3.0, 5.0, 7.0, 9.0)
        coarse = restrict_cell_averages(fine, 2)
        fine_mean = sum(fine) / len(fine)
        coarse_mean = sum(coarse) / len(coarse)
        self.assertAlmostEqual(fine_mean, coarse_mean, places=14)

    def test_restriction_is_identity_on_same_mesh(self):
        values = (1.0, 2.0, 4.0, 8.0)
        self.assertEqual(restrict_cell_averages(values, 4), values)

    def test_rejects_non_nested_meshes(self):
        with self.assertRaises(ValueError):
            restrict_cell_averages((1.0, 2.0, 3.0), 2)

    def test_mesh_independent_initial_profile(self):
        coarse = consistent_reference_inputs(2)[3]
        fine = consistent_reference_inputs(8)[3]
        theta, fields = restrict_state(fine, 2)
        for a, b in zip(coarse.fluid_capacity, theta):
            self.assertAlmostEqual(a, b, places=14)
        for coarse_row, fine_row in zip(coarse.inventories, fields):
            for a, b in zip(coarse_row, fine_row):
                self.assertAlmostEqual(a, b, places=12)

    def test_initial_profile_has_nonzero_spatial_gradient(self):
        state = consistent_reference_inputs(8)[3]
        self.assertGreater(state.fluid_capacity[-1], state.fluid_capacity[0])
        self.assertGreater(state.inventories[0][-1], state.inventories[0][0])


if __name__ == "__main__":
    unittest.main()
