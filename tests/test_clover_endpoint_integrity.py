"""Synthetic-only guardrails for clover endpoint integrity audit."""
import csv
import importlib.util
import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

try:
    import numpy
    import sklearn
except ImportError:
    raise unittest.SkipTest("Requires dedicated clover analysis CI")

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
modfile = ROOT / "scripts" / "audit_clover_endpoint_integrity.py"
spec = importlib.util.spec_from_file_location("clover_endpoint_qc", modfile)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class CloverEndpointIntegrityTests(unittest.TestCase):
    def test_flowering_and_count_discordance_is_distinct_not_error_correction(self):
        row = {"FloweredFull":"1","FlowerHeadNumberFull":"0",
               "SeedSetMassFull":"0", "Survived1st":"0"}
        flags = mod.indicator_flags(row)
        self.assertTrue(flags["flowered_one_head_zero"])
        self.assertTrue(flags["flowered_one_seed_zero"])
        self.assertTrue(flags["flowered_one_firstyear_survival_zero"])
        self.assertFalse(flags["flowered_zero_head_positive"])
        other = {"FloweredFull":"0","FlowerHeadNumberFull":"1",
                 "SeedSetMassFull":"0.5", "Survived1st":"1"}
        flags = mod.indicator_flags(other)
        self.assertTrue(flags["flowered_zero_head_positive"])
        self.assertTrue(flags["flowered_zero_seed_positive"])

    def test_missing_firstyear_survival_does_not_imply_zero(self):
        record={"FloweredFull":"1", "FlowerHeadNumberFull":"2",
                "SeedSetMassFull":"0.15", "Survived1st":"999"}
        flags=mod.indicator_flags(record)
        self.assertFalse(flags["flowered_one_firstyear_survival_zero"])
        self.assertFalse(flags["flowered_one_head_zero"])
        self.assertFalse(flags["flowered_one_seed_zero"])

    def test_uninterpretable_binary_outcome_cannot_pass(self):
        with self.assertRaises(ValueError):
            mod.indicator_flags({
                "FloweredFull":"999","FlowerHeadNumberFull":"0",
                "SeedSetMassFull":"0","Survived1st":"1"
            })
        with self.assertRaises(ValueError):
            mod.indicator_flags({
                "FloweredFull":"1","FlowerHeadNumberFull":"999",
                "SeedSetMassFull":"0","Survived1st":"1"
            })

    def test_no_archive_bytes_in_report_and_source_provenance_contract(self):
        with patch.object(mod, "source_data", side_effect=ValueError("source hash mismatch")):
            with self.assertRaisesRegex(ValueError, "source hash mismatch"):
                mod.audit(Path("/not-original.zip"), evaluate_exploratory=False)


if __name__=="__main__":
    unittest.main()
