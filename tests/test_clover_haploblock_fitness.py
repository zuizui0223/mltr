"""Synthetic-only tests of haploblock garden response prediction.

CI without NumPy/scikit-learn skips these tests; the dedicated sklearn CI
installs both and executes them. Never commit real Dryad sample-level rows.
"""
import csv
import importlib.util
import random
import sys
import tempfile
import unittest
from pathlib import Path

try:
    import numpy as np
    import sklearn
except ImportError:
    raise unittest.SkipTest("NumPy/sklearn unavailable; dedicated clover CI installs them")

SOURCE = Path(__file__).resolve().parents[1] / "scripts" / "analyze_clover_haploblock_fitness.py"
spec = importlib.util.spec_from_file_location("clover_fit", SOURCE)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class CloverHaploblockTests(unittest.TestCase):
    def write_example(self, path):
        rng = random.Random(20261119)
        gardens = ("Toronto", "Montpellier", "Lafayette", "Uppsula")
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=module.REQUIRED)
            writer.writeheader()
            for pop in range(40):
                for row in range(12):
                    garden = gardens[(pop + row) % 4]
                    haps = [rng.choice([0.0, 0.5, 1.0]) for _ in module.HAPS]
                    prob = 0.2 + (0.35 if haps[0] == 1.0 else 0) + (
                        0.2 if garden == "Toronto" else 0
                    )
                    record = {
                        "Garden": garden, "File": f"s-{pop:02d}-{row:02d}.bam",
                        "Population": f"population-{pop:02d}",
                        "Latitude": 25 + pop * 0.5, "Longitude": -105 + pop,
                        "FloweredFull": int(rng.random() < prob)
                    }
                    record.update(zip(module.HAPS, haps))
                    writer.writerow(record)

    def test_population_disjoint_prediction_and_no_sample_leakage_in_output(self):
        with tempfile.TemporaryDirectory() as temp:
            original = Path(temp) / "DatasetA_commongarden.csv"
            self.write_example(original)
            report = module.analyse(original)
            self.assertEqual(report["source_quality"]["complete_case_rows"], 480)
            self.assertEqual(report["source_quality"]["complete_origin_populations"], 40)
            self.assertEqual(len(report["folds"]), 5)
            self.assertEqual(set(report["models"]), {"M0", "M1", "M2"})
            self.assertEqual(len(report["contrasts"]["M1_minus_M0"]["conditional_population_bootstrap_ci_95"]), 2)
            self.assertNotIn("s-00-00.bam", str(report))
            self.assertNotIn("population-00", str(report))
            for fold in report["folds"]:
                self.assertGreater(fold["heldout_origin_populations"], 0)

    def test_invalid_haploblock_dosage_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            original = Path(temp) / "DatasetA_commongarden.csv"
            self.write_example(original)
            text = original.read_text()
            self.assertIn(",0.5,", text)
            original.write_text(text.replace(",0.5,", ",0.33,", 1))
            with self.assertRaises(ValueError):
                module.read_source(original)

    def test_missing_sentinel_excluded_using_same_models(self):
        with tempfile.TemporaryDirectory() as temp:
            original = Path(temp) / "DatasetA_commongarden.csv"
            self.write_example(original)
            rows = list(csv.DictReader(original.open(newline="")))
            rows[0]["Hb7a1"] = "999"
            with original.open("w", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=module.REQUIRED)
                writer.writeheader()
                writer.writerows(rows)
            selected, quality = module.read_source(original)
            self.assertEqual(len(selected), 479)
            self.assertEqual(quality["exclusion_counts"]["missing_complete_case_field"], 1)

    def test_duplicate_bam_sample_id_is_not_silently_deduplicated(self):
        with tempfile.TemporaryDirectory() as temp:
            original = Path(temp) / "DatasetA_commongarden.csv"
            self.write_example(original)
            rows = list(csv.DictReader(original.open(newline="")))
            rows[1]["File"] = rows[0]["File"]
            with original.open("w", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=module.REQUIRED)
                writer.writeheader()
                writer.writerows(rows)
            with self.assertRaises(ValueError):
                module.read_source(original)


if __name__ == "__main__":
    unittest.main()
