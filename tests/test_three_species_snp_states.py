"""Tests use synthetic genotypes only; original Dryad ZIP is not in Git."""
import importlib.util
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "audit_three_species_snp_states.py"
spec = importlib.util.spec_from_file_location("three_species_snp", SCRIPT)
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


class ThreeSpeciesGenomicsTests(unittest.TestCase):
    def test_repeated_population_code_is_an_individual_row_not_a_dedup_key(self):
        source = (
            b"Title line:Synthetic\n"
            b"locus1\nlocus2\nPOP\n"
            b"A, 0101 0102\nA, 0101 0102\nPOP\n"
            b"B, 0202 0202\nB, 0202 0102\n"
        )
        loci, order, pops = audit.parse(source)
        self.assertEqual(loci, ["locus1", "locus2"])
        self.assertEqual(order, ["A", "B"])
        self.assertEqual(len(pops["A"]), 2)
        self.assertEqual(pops["A"][0], pops["A"][1])
        self.assertEqual(audit.qc(pops["A"])["n"], 2)

    def test_reject_mixed_codes_and_invalid_or_partial_calls(self):
        sample = (
            b"Title line:Synthetic\nsnp1\nPOP\nA, 0101\nB, 0101\n"
        )
        with self.assertRaises(ValueError):
            audit.parse(sample)
        with self.assertRaises(ValueError):
            audit.parse(sample.replace(b"B, 0101", b"A, 0001"))

    def test_fst_fixed_opposites(self):
        a = [[1, 1, 1] for _ in range(8)]
        b = [[3, 3, 3] for _ in range(8)]
        result = audit.fst(a, b)
        self.assertEqual(result["loci"], 3)
        self.assertEqual(result["fst"], 1.0)

    def test_historical_nondetection_not_extinction(self):
        old = [[1, 2], [1, 1]]
        current = [[3, 2], [3, 3]]
        ex = {"G1": [[1, 2]]}
        result = audit.historic(old, current, ex)
        self.assertEqual(result["past_alleles_not_detected_current_at_callable_loci"], 1)
        self.assertEqual(result["past_not_current_found_in_any_ex_situ"], 1)
        self.assertIn("not allele extinction", result["claim"])

    def test_heldout_population_prediction_strictly_excludes_sample(self):
        populations = {
            "A": [[1, 1, 1, 1] for _ in range(8)],
            "B": [[3, 3, 3, 3] for _ in range(8)],
        }
        result = audit.loo_score(populations, ["A", "B"], alpha=0.5)
        self.assertEqual(result["held_out_individuals"], 16)
        self.assertEqual(result["positive_individuals"], 16)
        self.assertGreater(result["mean_gain_nats_per_allele"], 0)
        self.assertEqual(result["evaluated_genotypes"], 64)
        result2 = audit.loo_score(populations, ["A", "B"], alpha=2.0)
        self.assertGreater(result2["mean_gain_nats_per_allele"], 0)

    def test_original_zip_hash_enforced(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "synthetic.zip"
            path.write_bytes(b"not the published archive")
            with self.assertRaises(ValueError):
                audit.analyse_zip(path)


if __name__ == "__main__":
    unittest.main()
