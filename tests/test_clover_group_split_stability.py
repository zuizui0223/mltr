"""Synthetic-only tests for repeat-group-split stability of frozen M0/M1.

The published Dryad source is NOT committed or embedded in test fixtures.
"""
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
    raise unittest.SkipTest("Dedicated clover CI provides numpy and sklearn")

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
source = SCRIPTS / "audit_clover_group_split_stability.py"
spec = importlib.util.spec_from_file_location("clover_split_stability", source)
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


def fake_records():
    rng = random.Random(20261119)
    gardens = ("Lafayette", "Montpellier", "Toronto", "Uppsala")
    records = []
    for pop in range(24):
        for i in range(8):
            haps = [rng.choice((0.0, 0.5, 1.0)) for _ in range(5)]
            garden = gardens[(pop + i) % 4]
            prob = 0.25 + 0.35 * int(garden == "Montpellier") + 0.1 * haps[0]
            records.append({
                "garden": garden,
                "population": f"synthetic-pop-{pop}",
                "lat": 10.0 + pop / 2, "lon": 45.0 - pop,
                "haps": haps, "y": int(rng.random() < prob),
            })
    return records


class SplitStabilityTests(unittest.TestCase):
    def test_same_origin_population_never_enters_both_sides(self):
        records = fake_records()
        with self.assertRaisesRegex(ValueError, "origin population leakage"):
            audit.heldout_contrast(records, np.array([0, 1, 2]), np.array([3, 4]))

    def test_reference_and_random_splits_are_deterministic(self):
        records = fake_records()
        a = audit.evaluate_split_stability(records, n_repeats=4, seed=71)
        b = audit.evaluate_split_stability(records, n_repeats=4, seed=71)
        self.assertEqual(a, b)
        self.assertEqual(len(a["reference_fixed_5fold"]["per_fold_gain_nats"]), 5)
        random_result = a["repeated_group_shuffle_80_20"]
        self.assertEqual(random_result["repeats"], 4)
        self.assertEqual(random_result["negative_repeats"] +
                         random_result["positive_repeats"], 4)
        self.assertTrue(np.isfinite(random_result["individual_mean_gain_distribution"]["mean"]))

    def test_split_quantiles_are_descriptive_not_inferential(self):
        data = audit.summary([-0.02, -0.01, 0.01, 0.03])
        self.assertLess(data["q025"], 0)
        self.assertGreater(data["q975"], 0)
        self.assertEqual(data["median"], 0.0)

    def test_invalid_repeat_range_and_untrusted_archive_fail_closed(self):
        with self.assertRaises(ValueError):
            audit.evaluate_split_stability(fake_records(), n_repeats=0)
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "unverified.zip"
            path.write_bytes(b"not a source dataset")
            with self.assertRaises(ValueError):
                audit.analyse(path, repeats=2)


if __name__ == "__main__":
    unittest.main()
