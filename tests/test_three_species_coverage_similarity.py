"""Unit tests using synthetic SNP genotypes only; no raw Dryad data committed."""
import importlib.util
import math
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
spec = importlib.util.spec_from_file_location("coverage_similarity", SCRIPTS / "audit_three_species_coverage_similarity.py")
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


class CoverageAndSimilarityTests(unittest.TestCase):
    def test_common_coverage_panel_uses_every_region(self):
        grouped = {
            "A": [[1, 0, 1], [2, 0, 1], [1, 1, 0], [1, 1, 1]],
            "B": [[3, 1, 0], [3, 1, 1], [3, 0, 0], [3, 1, 0]],
        }
        self.assertEqual(audit.common_locus_panel(grouped, 0.75), [True, False, False])
        self.assertEqual(audit.common_locus_panel(grouped, 1.0), [True, False, False])
        with self.assertRaises(ValueError):
            audit.common_locus_panel(grouped, 1.5)

    def test_identity_requires_shared_called_loci(self):
        a = [1, 2, 3, 0]
        b = [1, 2, 1, 3]
        self.assertIsNone(audit.shared_genotype_identity(a, b))
        self.assertAlmostEqual(audit.shared_genotype_identity(a, b, 3), 2/3)

    def test_identical_near_neighbor_is_not_automatically_same_individual(self):
        grouped = {"A": [[1]*8 for _ in range(8)], "B": [[3]*8 for _ in range(8)]}
        identity = audit.similarity_inventory(grouped, 0.95, min_shared=8)
        self.assertEqual(identity["within_pairs_above_cut"], 56)
        normal = audit.score_held_out(grouped, fraction=0.75)
        self.assertEqual(normal["evaluated_individuals"], 16)
        self.assertGreater(normal["mean_gain_nats_per_allele"], 0)
        guarded = audit.score_held_out(grouped, fraction=0.75,
                                      remove_similar_at=0.95, min_shared=8)
        self.assertEqual(guarded["unevaluable_individuals"], 16)
        self.assertIsNone(guarded["mean_gain_nats_per_allele"])

    def test_low_coverage_not_promoted_as_positive(self):
        grouped = {"A": [[1, 0] for _ in range(8)], "B": [[3, 0] for _ in range(8)]}
        actual = audit.score_held_out(grouped, fraction=1.0)
        self.assertEqual(actual["loci_panel"], 1)
        self.assertEqual(actual["evaluated_genotypes"], 16)
        no_panel = audit.score_held_out({"A": [[0,0]], "B": [[0,0]]}, fraction=1.0)
        self.assertEqual(no_panel["status"], "NO_QUALIFYING_SNP_PANEL")

    def test_missingness_predictor_is_separate_from_allele_outcome(self):
        group = {"A": [[1,1]*4 for _ in range(8)],
                 "B": [[3,0]*4 for _ in range(8)]}
        result = audit.missingness_score(group)
        self.assertEqual(result["individuals"], 16)
        self.assertTrue(math.isfinite(result["gain_nats_per_binary_SNP_call"]))
        self.assertGreater(result["gain_nats_per_binary_SNP_call"], 0)

    def test_original_archive_hash_is_mandatory(self):
        with tempfile.TemporaryDirectory() as temp:
            bad = Path(temp)/"raw.zip"
            bad.write_bytes(b"unverified original")
            with self.assertRaises(ValueError):
                audit.analyse(bad)


if __name__ == "__main__":
    unittest.main()
