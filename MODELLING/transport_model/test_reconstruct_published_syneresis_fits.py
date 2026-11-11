import math
import unittest

from reconstruct_published_syneresis_fits import curve_value


class PublishedFitReconstructionTests(unittest.TestCase):
    def test_initial_condition(self):
        self.assertEqual(curve_value(0.0, 0.4, 2.0), 0.0)

    def test_one_time_constant(self):
        self.assertAlmostEqual(curve_value(2.0, 0.4, 2.0),
                               0.4 * (1.0 - math.exp(-1.0)))

    def test_long_time_limit(self):
        self.assertAlmostEqual(curve_value(1000.0, 0.4, 2.0), 0.4)

    def test_invalid_parameters_rejected(self):
        for args in [(-1.0, 0.4, 2.0), (1.0, -0.1, 2.0), (1.0, 0.4, 0.0)]:
            with self.assertRaises(ValueError):
                curve_value(*args)


if __name__ == "__main__":
    unittest.main()
