import csv
import math
import tempfile
import unittest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))
import ccfsm_v05_calibration as c

class V05CalibrationTests(unittest.TestCase):
    def test_exponential_recovers_synthetic_parameters(self):
        pts=[(t,.34*(1-math.exp(-t/2.7))) for t in [0,.2,.5,1,2,4,8,12,20]]
        fit=c.fit_model(pts,"exponential")
        self.assertAlmostEqual(fit["params"]["amplitude"],.34,places=5)
        self.assertAlmostEqual(fit["params"]["tau_h"],2.7,places=3)

    def test_stretched_exponential_recovers_shape(self):
        pts=[(t,.42*(1-math.exp(-(t/3.2)**.72)) ) for t in [0,.2,.5,1,2,4,8,12,20,30]]
        fit=c.fit_model(pts,"stretched_exponential")
        self.assertAlmostEqual(fit["params"]["amplitude"],.42,places=3)
        self.assertAlmostEqual(fit["params"]["tau_h"],3.2,places=1)
        self.assertAlmostEqual(fit["params"]["stretch_exponent"],.72,places=1)

    def test_ccfsm_equal_rate_limit(self):
        pts=[(t,.31*(1-(1+.8*t)*math.exp(-.8*t))) for t in [0,.2,.5,1,2,3,5,8,12]]
        fit=c.fit_model(pts,"ccfsm_two_stage")
        pred=c.predict(fit,[t for t,_ in pts])
        rmse=math.sqrt(sum((y-p)**2 for (_,y),p in zip(pts,pred))/len(pts))
        self.assertLess(rmse,2e-3)

    def test_reader_excludes_forced_panel_and_checks_14_natural_curves(self):
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/"input.csv"
            with path.open("w",newline="",encoding="utf-8-sig") as f:
                w=csv.writer(f,delimiter=";")
                w.writerow(["panel","series","condition","time_h","relative_volume_decrease_or_shrinkage","trace_type"])
                for panel,prefix in [("acidic_pH_below_pH_iso","acid"),("basic_pH_above_pH_iso","basic")]:
                    for j in range(7):
                        for i in range(8):
                            w.writerow([panel,f"{prefix}_{j}","condition",str(i).replace(".",","),str(.3*(1-math.exp(-i/2))).replace(".",","),"combined visible trace"])
                for j in range(7):
                    for i in range(8):
                        w.writerow(["enforced_syneresis_20C",f"top_{j}","forced",i,.2,"forced"])
            curves=c.read_natural_curves(path)
            self.assertEqual(len(curves),14)
            self.assertTrue(all(k[0]!="enforced_syneresis_20C" for k in curves))

    def test_two_stage_amplitude_is_effective_product_and_rates_sorted(self):
        pts=[(t,.25*(1-(.9*math.exp(-.2*t)-.2*math.exp(-.9*t))/.7)) for t in [0,.5,1,2,4,8,12,20,30]]
        fit=c.fit_model(pts,"ccfsm_two_stage")
        p=fit["params"]
        self.assertLessEqual(p["rate_slow_per_h"],p["rate_fast_per_h"])
        self.assertAlmostEqual(p["amplitude_product_eta_qinf"],.25,places=2)

if __name__=="__main__": unittest.main()
