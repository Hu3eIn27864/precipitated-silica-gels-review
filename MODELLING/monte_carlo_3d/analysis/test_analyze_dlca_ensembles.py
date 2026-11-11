import csv
import tempfile
import unittest
from pathlib import Path

from analyze_dlca_ensembles import load_system


class EnsembleAnalysisTests(unittest.TestCase):
    def write_csv(self, path, fields, rows):
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)

    def test_seed_level_statistics_use_one_fixed_window(self):
        with tempfile.TemporaryDirectory() as directory:
            prefix = Path(directory) / "n10"
            self.write_csv(
                Path(str(prefix) + "_runs.csv"),
                ["seed", "completed", "attempts", "successful_merges",
                 "component_count", "largest_component_size",
                 "largest_component_rg", "unwrapping_consistent"],
                [
                    {"seed": 11, "completed": 1, "attempts": 20,
                     "successful_merges": 9, "component_count": 1,
                     "largest_component_size": 10, "largest_component_rg": 2.5,
                     "unwrapping_consistent": 1},
                    {"seed": 12, "completed": 0, "attempts": 30,
                     "successful_merges": 7, "component_count": 3,
                     "largest_component_size": 6, "largest_component_rg": 1.8,
                     "unwrapping_consistent": 1},
                    {"seed": 13, "completed": 1, "attempts": 25,
                     "successful_merges": 9, "component_count": 1,
                     "largest_component_size": 10, "largest_component_rg": "nan",
                     "unwrapping_consistent": 0},
                ],
            )
            self.write_csv(
                Path(str(prefix) + "_mass_radius.csv"),
                ["seed", "particle_count", "radius", "mean_enclosed_mass"],
                [
                    {"seed": 11, "particle_count": 10, "radius": radius,
                     "mean_enclosed_mass": mass}
                    for radius, mass in [(1.5, 1.2), (2, 1.5), (3, 2.1),
                                         (4, 2.8), (5, 3.2), (8, 4.0)]
                ],
            )
            self.write_csv(
                Path(str(prefix) + "_fit_windows.csv"),
                ["seed", "fit_minimum_radius", "fit_maximum_radius",
                 "exponent", "standard_error", "r_squared", "point_count"],
                [
                    {"seed": 11, "fit_minimum_radius": 2, "fit_maximum_radius": 5,
                     "exponent": 1.72, "standard_error": 0.03,
                     "r_squared": 0.99, "point_count": 4},
                    # A second window for the same seed is deliberately ignored.
                    {"seed": 11, "fit_minimum_radius": 1.5, "fit_maximum_radius": 8,
                     "exponent": 1.9, "standard_error": 0.04,
                     "r_squared": 0.98, "point_count": 8},
                    # Incomplete seed fit rows must not become observations.
                    {"seed": 12, "fit_minimum_radius": 2, "fit_maximum_radius": 5,
                     "exponent": 1.5, "standard_error": 0.1,
                     "r_squared": 0.9, "point_count": 4},
                ],
            )
            rows, summary = load_system(10, prefix, 2.0, 5.0)
            self.assertEqual(len(rows), 3)
            self.assertAlmostEqual(rows[0]["df"], 1.72)
            self.assertIsNone(rows[1]["df"])
            self.assertIsNone(rows[2]["df"])
            self.assertEqual(summary["runs"], 3)
            self.assertEqual(summary["completed_runs"], 2)
            self.assertEqual(summary["unwrapped_completed_runs"], 1)
            self.assertEqual(summary["valid_fit_runs"], 1)
            self.assertAlmostEqual(summary["completion_fraction"], 2 / 3)
            self.assertAlmostEqual(summary["df_mean"], 1.72)
            self.assertIsNone(summary["df_sd"])

    def test_duplicate_run_seed_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            prefix = Path(directory) / "n4"
            self.write_csv(
                Path(str(prefix) + "_runs.csv"),
                ["seed", "completed", "unwrapping_consistent",
                 "largest_component_size", "largest_component_rg"],
                [
                    {"seed": 1, "completed": 0, "unwrapping_consistent": 1,
                     "largest_component_size": 2, "largest_component_rg": 1},
                    {"seed": 1, "completed": 0, "unwrapping_consistent": 1,
                     "largest_component_size": 2, "largest_component_rg": 1},
                ],
            )
            self.write_csv(
                Path(str(prefix) + "_fit_windows.csv"),
                ["seed", "fit_minimum_radius", "fit_maximum_radius",
                 "exponent", "r_squared", "standard_error", "point_count"],
                [],
            )
            with self.assertRaisesRegex(ValueError, "Duplicate seed"):
                load_system(4, prefix, 2.0, 5.0)


if __name__ == "__main__":
    unittest.main()
