"""Regression tests for the P27.20 two-state energy adapter."""
import unittest
from ccfsm_p27_20_two_state_energy import build_two_state_energy_snapshot


class P2720Tests(unittest.TestCase):
    def setUp(self):
        self.base = dict(
            time_old_s=0.0, time_new_s=2.0,
            cell_widths_old_m=(0.5, 0.5), cell_widths_new_m=(0.5, 0.5),
            fv_free_energy_density_old_j_m3=(2.0, 4.0),
            fv_free_energy_density_new_j_m3=(3.0, 5.0),
            cross_section_area_m2=2.0,
            p19_old={"stored_energy_j": 10.0, "boundary_traction_work_j": 4.0},
            p19_new={"stored_energy_j": 14.0, "boundary_traction_work_j": 8.0},
        )

    def test_energy_increments_and_units(self):
        r = build_two_state_energy_snapshot(**self.base)
        self.assertTrue(r["overall_valid"])
        self.assertAlmostEqual(r["fv_energy_old_j"], 6.0)
        self.assertAlmostEqual(r["fv_energy_new_j"], 8.0)
        self.assertAlmostEqual(r["energy_rate_components_w_m2"]["fv_free_energy"], 0.5)
        self.assertAlmostEqual(r["energy_rate_components_w_m2"]["p19_mechanical_biot_stored_energy"], 1.0)
        self.assertAlmostEqual(r["mean_energy_rate_w_m2"], 1.5)

    def test_traction_work_is_opt_in(self):
        r = build_two_state_energy_snapshot(**self.base)
        self.assertIsNone(r["endpoint_traction_work_rate_w_m2"])
        self.assertFalse(r["ledger_ready"])
        r = build_two_state_energy_snapshot(**self.base, use_endpoint_traction_work_difference=True)
        self.assertAlmostEqual(r["endpoint_traction_work_rate_w_m2"], 1.0)
        self.assertTrue(r["ledger_ready"])

    def test_nonuniform_grid_integral(self):
        args = dict(self.base)
        args.update(cell_widths_old_m=(0.25, 0.75), cell_widths_new_m=(0.25, 0.75))
        r = build_two_state_energy_snapshot(**args)
        self.assertAlmostEqual(r["fv_energy_old_j"], 7.0)
        self.assertAlmostEqual(r["fv_energy_new_j"], 9.0)

    def test_mesh_mismatch_rejected(self):
        args = dict(self.base)
        args["cell_widths_new_m"] = (0.4, 0.6)
        r = build_two_state_energy_snapshot(**args)
        self.assertFalse(r["overall_valid"])

    def test_cell_count_mismatch_rejected(self):
        args = dict(self.base)
        args["fv_free_energy_density_new_j_m3"] = (3.0,)
        r = build_two_state_energy_snapshot(**args)
        self.assertFalse(r["overall_valid"])

    def test_time_and_area_validation(self):
        args = dict(self.base)
        args["time_new_s"] = 0.0
        self.assertFalse(build_two_state_energy_snapshot(**args)["overall_valid"])
        args = dict(self.base)
        args["cross_section_area_m2"] = -1.0
        self.assertFalse(build_two_state_energy_snapshot(**args)["overall_valid"])

    def test_p19_energy_required_and_nonnegative(self):
        args = dict(self.base)
        args["p19_new"] = {"stored_energy_j": -1.0}
        self.assertFalse(build_two_state_energy_snapshot(**args)["overall_valid"])


if __name__ == "__main__":
    unittest.main()
