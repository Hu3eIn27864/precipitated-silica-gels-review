import unittest

from run_dlca_size_series import nonnegative_int, positive_int, scaled_box_length


class SizeSeriesRunnerTests(unittest.TestCase):
    def test_box_scaling_preserves_number_density(self):
        reference = scaled_box_length(32, 32, 15.0)
        doubled = scaled_box_length(64, 32, 15.0)
        self.assertAlmostEqual(reference, 15.0)
        self.assertAlmostEqual(doubled / reference, 2.0 ** (1.0 / 3.0))
        self.assertAlmostEqual(64 / doubled**3, 32 / reference**3)

    def test_seed_start_can_be_zero(self):
        self.assertEqual(nonnegative_int("0"), 0)

    def test_sizes_must_be_positive(self):
        with self.assertRaises(Exception):
            positive_int("0")


if __name__ == "__main__":
    unittest.main()
