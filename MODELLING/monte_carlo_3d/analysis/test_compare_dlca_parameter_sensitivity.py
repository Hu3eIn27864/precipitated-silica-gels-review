import unittest

from compare_dlca_parameter_sensitivity import compare_rows


def row(seed, completed=1, unwrapped=1, largest=10, rg=2.0, df=1.7):
    return {
        "seed": seed,
        "completed": completed,
        "attempts": 500 if completed else 1000,
        "unwrapping_consistent": unwrapped,
        "largest_component_fraction": largest / 10,
        "largest_component_rg": rg,
        "df": df,
    }


class PairedSensitivityTests(unittest.TestCase):
    def test_paired_deltas_and_valid_pair_counts(self):
        baseline = [row(10), row(11, completed=0, unwrapped=1, largest=6,
                                rg=None, df=None)]
        variant = [row(10, largest=8, rg=2.5, df=1.9),
                   row(11, completed=1, unwrapped=1, largest=9,
                       rg=3.0, df=1.8)]
        per_seed, summary = compare_rows(baseline, variant, "step_test")
        self.assertEqual(len(per_seed), 2)
        self.assertAlmostEqual(per_seed[0]["delta_largest_fraction"], -0.2)
        self.assertAlmostEqual(per_seed[0]["delta_rg"], 0.5)
        self.assertAlmostEqual(per_seed[0]["delta_df"], 0.2)
        self.assertEqual(per_seed[1]["rg_pair_valid"], 0)
        self.assertEqual(per_seed[1]["df_pair_valid"], 0)
        self.assertEqual(summary["both_completed"], 1)
        self.assertEqual(summary["valid_rg_pairs"], 1)
        self.assertEqual(summary["valid_df_pairs"], 1)

    def test_seed_mismatch_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Seed sets differ"):
            compare_rows([row(1)], [row(2)], "bad_variant")

    def test_incomplete_runs_still_contribute_largest_fraction(self):
        baseline = [row(4, completed=0, largest=3, rg=None, df=None)]
        variant = [row(4, completed=0, largest=5, rg=None, df=None)]
        per_seed, summary = compare_rows(baseline, variant, "unfinished")
        self.assertAlmostEqual(per_seed[0]["delta_largest_fraction"], 0.2)
        self.assertEqual(summary["both_completed"], 0)
        self.assertEqual(summary["valid_df_pairs"], 0)
        self.assertEqual(summary["valid_rg_pairs"], 0)


if __name__ == "__main__":
    unittest.main()
