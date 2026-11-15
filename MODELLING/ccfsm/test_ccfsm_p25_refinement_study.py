import unittest

from ccfsm_p25_refinement_study import (
    reference_inputs, _flat, _relative_inf,
)


class TestP25RefinementStudy(unittest.TestCase):
    def test_reference_mesh_has_one_positive_fe_point_per_fv_cell(self):
        for cells in (1, 2, 4):
            grid, chemistry, mechanics, state, quad, dbc = reference_inputs(cells)
            self.assertEqual(grid.cells, cells)
            self.assertEqual(len(quad), cells)
            self.assertTrue(all(item["weight"] > 0 for item in quad))
            self.assertEqual(len(quad[0]["B"][0]), 3 * (cells + 1))
            self.assertEqual(len(state.fluid_capacity), cells)
            self.assertEqual(len(dbc), 2 * (cells + 1) + 1)

    def test_relative_error_is_zero_for_identical_states(self):
        _, _, _, state, _, _ = reference_inputs(2)
        self.assertEqual(_relative_inf(_flat(state), _flat(state)), 0.0)

    def test_reference_states_are_admissible_and_spatially_nonuniform(self):
        for cells in (1, 2, 4):
            _, _, _, state, _, _ = reference_inputs(cells)
            self.assertTrue(all(0 < x <= 1 for x in state.fluid_capacity))
            self.assertTrue(all(x > 0 for row in state.inventories for x in row))
        _, _, _, state, _, _ = reference_inputs(4)
        self.assertNotEqual(state.fluid_capacity[0], state.fluid_capacity[-1])


if __name__ == "__main__":
    unittest.main()
