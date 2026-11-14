import csv
import unittest
from pathlib import Path

DATA = Path(__file__).with_name("ccfsm_literature_parameter_dataset_2026-11-14.csv")

class LiteratureDatasetTests(unittest.TestCase):
    def test_schema_and_unique_ids(self):
        with DATA.open(encoding="utf-8", newline="") as f:
            rows = list(csv.DictReader(f))
        self.assertGreaterEqual(len(rows), 30)
        required = {"record_id", "source", "year", "variable", "value", "unit",
                    "classification", "process", "ccfsm_use", "notes"}
        self.assertTrue(required.issubset(rows[0].keys()))
        ids = [r["record_id"] for r in rows]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue(all(r["source"] and r["classification"] for r in rows))

    def test_natural_syneresis_only_primary_calibration(self):
        with DATA.open(encoding="utf-8", newline="") as f:
            rows = list(csv.DictReader(f))
        primary = [r for r in rows if r["ccfsm_use"] == "primary_natural_calibration"]
        self.assertEqual(len(primary), 12)
        self.assertTrue(all(r["process"] == "natural_unloaded_syneresis" for r in primary))
        excluded = [r for r in rows if r["classification"] == "X"]
        self.assertTrue(all(r["ccfsm_use"] != "primary_natural_calibration" for r in excluded))

    def test_source_values_are_numeric(self):
        with DATA.open(encoding="utf-8", newline="") as f:
            rows = list(csv.DictReader(f))
        for row in rows:
            float(row["value"])

if __name__ == "__main__":
    unittest.main()
