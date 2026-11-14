"""Integrity checks for the source-level CCFSM literature inventory."""

import csv
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent
INVENTORY = ROOT / "ccfsm_literature_source_inventory_2026-11-14.csv"


class LiteratureSourceInventoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with INVENTORY.open("r", encoding="utf-8-sig", newline="") as handle:
            cls.rows = list(csv.DictReader(handle))

    def test_inventory_has_expected_schema_and_records(self):
        self.assertGreaterEqual(len(self.rows), 10)
        required = {
            "record_id", "authors", "year", "title", "doi", "system",
            "process_class", "reported_observables", "available_data_form",
            "evidence_class", "current_status", "ccfsm_admissible_use",
            "source_url", "notes",
        }
        self.assertEqual(set(self.rows[0]), required)

    def test_record_ids_are_unique_and_required_fields_present(self):
        ids = [row["record_id"] for row in self.rows]
        self.assertEqual(len(ids), len(set(ids)))
        for row in self.rows:
            for field in ("record_id", "authors", "year", "title", "system",
                          "process_class", "evidence_class", "source_url"):
                self.assertTrue(row[field].strip(), (row["record_id"], field))

    def test_forced_and_drying_sources_are_not_natural_calibration_sources(self):
        by_id = {row["record_id"]: row for row in self.rows}
        for record_id in ("SAHABI_KIND2011", "SCHERER1997",
                          "SMITH_SCHERER_ANDERSON1995"):
            self.assertIn(record_id, by_id)
            self.assertIn("X", by_id[record_id]["evidence_class"])
            self.assertNotIn("primary natural-syneresis calibration",
                             by_id[record_id]["ccfsm_admissible_use"])

    def test_quarch_dissertation_has_no_misattributed_doi(self):
        by_id = {row["record_id"]: row for row in self.rows}
        self.assertEqual(by_id["QUARCH2010"]["doi"], "")
        self.assertIn("1000017100", by_id["QUARCH2010"]["source_url"])


if __name__ == "__main__":
    unittest.main()
