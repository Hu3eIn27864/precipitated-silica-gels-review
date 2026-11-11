import csv
import importlib.util
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("analyze_dlca_fit_sensitivity.py")
SPEC = importlib.util.spec_from_file_location("fit_sensitivity", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class FitSensitivityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.prefix = Path(self.temp.name) / "n8"
        with Path(str(self.prefix) + "_runs.csv").open("w", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(["seed", "completed", "unwrapping_consistent",
                             "largest_component_size"])
            writer.writerow([11, 1, 1, 8])
            writer.writerow([12, 0, 1, 5])
        with Path(str(self.prefix) + "_mass_radius.csv").open("w", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(["seed", "particle_count", "radius", "mean_enclosed_mass"])
            for radius, mass in [(1.5, 1.2), (2.0, 1.8), (2.5, 2.4), (3.0, 3.1), (4.0, 4.0)]:
                writer.writerow([11, 8, radius, mass])
        with Path(str(self.prefix) + "_fit_windows.csv").open("w", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(["seed", "fit_minimum_radius", "fit_maximum_radius",
                             "exponent", "standard_error", "r_squared", "point_count"])
            writer.writerow([11, 1.5, 3.0, 1.8, 0.1, 0.99, 4])
            writer.writerow([11, 2.0, 4.0, 2.1, 0.2, 0.97, 3])

    def tearDown(self):
        self.temp.cleanup()

    def test_reports_within_seed_fit_window_range(self):
        per_seed, summary = MODULE.analyse(self.prefix, 8)
        self.assertEqual(per_seed[0]["valid_window_count"], 2)
        self.assertAlmostEqual(per_seed[0]["exponent_range"], 0.3)
        self.assertEqual(per_seed[1]["valid_window_count"], 0)
        self.assertEqual(summary["eligible_runs"], 1)
        self.assertEqual(summary["runs_with_fit_windows"], 1)

    def test_rejects_fit_attached_to_incomplete_run(self):
        path = Path(str(self.prefix) + "_fit_windows.csv")
        with path.open("a") as handle:
            handle.write("12,1.5,3.0,1.7,0.1,0.98,4\n")
        with self.assertRaisesRegex(ValueError, "incomplete"):
            MODULE.analyse(self.prefix, 8)

    def test_rejects_duplicate_windows(self):
        path = Path(str(self.prefix) + "_fit_windows.csv")
        with path.open("a") as handle:
            handle.write("11,1.5,3.0,1.9,0.1,0.99,4\n")
        with self.assertRaisesRegex(ValueError, "Duplicate fit window"):
            MODULE.analyse(self.prefix, 8)


if __name__ == "__main__":
    unittest.main()
