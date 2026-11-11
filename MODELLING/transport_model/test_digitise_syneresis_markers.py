import math
import unittest
from digitise_syneresis_markers import convert, fit_axis

class DigitisationTests(unittest.TestCase):
    def test_linear_axis(self):
        model=(0.5, -1.0, "linear")
        value, uncertainty=convert(4.0, 0.2, model)
        self.assertAlmostEqual(value,1.0)
        self.assertAlmostEqual(uncertainty,0.1)

    def test_log10_axis(self):
        model=(0.5, 0.0, "log10")
        value, uncertainty=convert(2.0, 0.1, model)
        self.assertAlmostEqual(value,10.0)
        self.assertAlmostEqual(uncertainty,math.log(10)*10*0.05)

    def test_fit_axis(self):
        rows=[
            {"figure_panel":"8a","axis":"x","pixel":"100","value":"0","scale":"linear"},
            {"figure_panel":"8a","axis":"x","pixel":"200","value":"10","scale":"linear"},
        ]
        model=fit_axis(rows,"8a","x")
        self.assertAlmostEqual(convert(150,0,model)[0],5.0)

if __name__ == "__main__":
    unittest.main()
