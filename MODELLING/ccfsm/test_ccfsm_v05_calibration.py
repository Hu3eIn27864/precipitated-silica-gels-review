import csv, math, tempfile, unittest
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).parent))
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

    def test_natural_reader_filters_to_seven_curated_primary_series(self):
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/"natural.csv"
            with path.open("w",newline="",encoding="utf-8") as f:
                w=csv.writer(f); w.writerow(["figure","panel","condition","series","source_type","time_h","relative_shrinkage","reanalysis_use","digitization_note"])
                for j in range(7):
                    for i in range(8):
                        w.writerow(["Figure 8","a","acidic, pH < pHiso",f"{20+j} °C", "ai_assisted_approximation",i,.3*(1-math.exp(-i/2)),"primary_exploratory","unverified approximate reading"])
                for use in ["sensitivity_only","figure_table_conflict_branch"]:
                    for i in range(8):
                        w.writerow(["Figure 8","a","acidic, pH < pHiso","40 °C","ai_assisted_approximation",i,.3*(1-math.exp(-i/2)),use,"excluded branch"])
            curves=c.read_natural_curves(path)
            self.assertEqual(len(curves),7)
            self.assertEqual(next(iter(curves.values()))["source_type"],"ai_assisted_approximation")

    def test_pressure_cell_file_is_audited_but_not_admitted_as_natural(self):
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/"pressure.csv"
            with path.open("w",newline="",encoding="utf-8") as f:
                w=csv.writer(f,delimiter=";"); w.writerow(["panel","series","condition"])
                for panel,prefix in [("acidic_pH_below_pH_iso","acid"),("basic_pH_above_pH_iso","basic"),("enforced_syneresis_20C","top")]:
                    n=7
                    for j in range(n): w.writerow([panel,f"{prefix}_{j}",f"Δp={j+1} bar"])
            self.assertEqual(c.audit_pressure_file(path),{"pressure_cell_curves":21,"natural_calibration_curves":0})
            with self.assertRaises(ValueError): c.read_natural_curves(path)

    def test_two_stage_amplitude_product_and_sorted_rates(self):
        pts=[(t,.25*(1-(.9*math.exp(-.2*t)-.2*math.exp(-.9*t))/.7)) for t in [0,.5,1,2,4,8,12,20,30]]
        fit=c.fit_model(pts,"ccfsm_two_stage"); p=fit["params"]
        self.assertLessEqual(p["rate_slow_per_h"],p["rate_fast_per_h"])
        self.assertAlmostEqual(p["amplitude_product_eta_qinf"],.25,places=2)

if __name__=="__main__": unittest.main()
