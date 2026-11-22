"""Synthetic-only and committed-aggregate checks for Exposito context concentration."""
from __future__ import annotations

import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "audit_exposito_context_leverage.py"
spec = importlib.util.spec_from_file_location("exposito_context_leverage", SCRIPT)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def fixture():
    model_contexts = {
        "Mean": {c: 2.0 for c in m.CONTEXTS},
        "M0": {c: 1.0 for c in m.CONTEXTS},
        "M1": {c: (.5 if c == "mlp" else .9) for c in m.CONTEXTS},
    }
    models = {
        name: {"context_mse": values, "mse": sum(values.values()) / 8}
        for name, values in model_contexts.items()
    }
    gain = {c: models["M0"]["context_mse"][c] - models["M1"]["context_mse"][c]
            for c in m.CONTEXTS}
    groups = {}
    for key, split in m.MODES:
        groups[key] = {
            "split": split, "accessions": 514, "response_cells": 4112,
            "models": copy.deepcopy(models),
            "contrast": {"context_gains": gain, "mean_gain": sum(gain.values()) / 8,
                         "conditional_ci95": [-.1, .2]},
            "numerical_gate": {"passed": False},
        }
    return {"study_doi": "10.1038/s41586-019-1520-9", **groups}


class ExpositoContextLeverageTests(unittest.TestCase):
    def test_focal_share_and_baseline_variance_are_separate_quantities(self):
        actual = m.audit(fixture())["modes"]["primary"]
        self.assertAlmostEqual(actual["pooled_gain_M0_minus_M1"], .15)
        self.assertAlmostEqual(actual["focal_context_gain"], .5)
        self.assertAlmostEqual(actual["focal_share_of_signed_pooled_gain_percent"], 100 * 5 / 12)
        self.assertAlmostEqual(actual["focal_share_of_M0_pooled_loss_percent"], 12.5)
        self.assertAlmostEqual(actual["other_seven_contexts"]["mean_gain"], .1)
        self.assertAlmostEqual(actual["other_seven_contexts"]["M0_relative_error_reduction_percent"], 10.0)
        self.assertEqual(actual["n_positive_contexts"], 8)

    def test_score_only_context_deletion_never_claims_refitting(self):
        actual = m.audit(fixture())["modes"]["primary"]
        self.assertAlmostEqual(
            actual["delete_one_context_from_existing_score_without_refitting"]["mlp"], .1)
        self.assertIn("not new heldout predictions", actual["scope"])

    def test_score_consistency_mismatches_are_errors(self):
        for mutation in ("pooled_M0", "pooled_gain", "context_gain", "pooled_M1"):
            source = fixture()
            p = source["primary"]
            if mutation == "pooled_M0":
                p["models"]["M0"]["mse"] += .01
            if mutation == "pooled_M1":
                p["models"]["M1"]["mse"] -= .01
            if mutation == "pooled_gain":
                p["contrast"]["mean_gain"] += .01
            if mutation == "context_gain":
                p["contrast"]["context_gains"]["mlp"] += .01
            with self.subTest(mutation=mutation), self.assertRaisesRegex(ValueError, "algebra"):
                m.audit(source)

    def test_missing_or_relabelled_context_is_not_repaired(self):
        source = fixture()
        del source["primary"]["models"]["M0"]["context_mse"]["mlp"]
        with self.assertRaisesRegex(ValueError, "context identities"):
            m.audit(source)

    def test_wrong_source_population_or_study_rejected(self):
        source = fixture()
        source["study_doi"] = "different study"
        with self.assertRaisesRegex(ValueError, "wrong source study"):
            m.audit(source)
        source = fixture()
        source["primary"]["accessions"] = 400
        with self.assertRaisesRegex(ValueError, "wrong cohort"):
            m.audit(source)

    def test_original_stability_verdict_cannot_be_silently_reversed(self):
        source = fixture()
        source["primary"]["numerical_gate"]["passed"] = True
        with self.assertRaisesRegex(ValueError, "status changed"):
            m.audit(source)

    def test_signed_shares_can_exceed_100_percent_and_are_not_clipped(self):
        source = fixture()
        for mode, _split in m.MODES:
            group = source[mode]
            for c in m.CONTEXTS:
                if c == "mlp":
                    continue
                group["models"]["M1"]["context_mse"][c] = 1.1
                group["contrast"]["context_gains"][c] = -.1
            group["models"]["M1"]["mse"] = (
                sum(group["models"]["M1"]["context_mse"].values()) / 8)
            group["contrast"]["mean_gain"] = (
                sum(group["contrast"]["context_gains"].values()) / 8)
        actual = m.audit(source)["modes"]["primary"]
        self.assertLess(actual["pooled_gain_M0_minus_M1"], 0)
        self.assertLess(actual["focal_share_of_signed_pooled_gain_percent"], -100)

    def test_zero_total_gain_reports_undefined_share_not_nan(self):
        source = fixture()
        for mode, _split in m.MODES:
            g = source[mode]
            g["models"]["M1"]["context_mse"] = {
                c: 1.0 for c in m.CONTEXTS}
            g["models"]["M1"]["mse"] = 1.0
            g["contrast"]["context_gains"] = {c: 0.0 for c in m.CONTEXTS}
            g["contrast"]["mean_gain"] = 0.0
        actual = m.audit(source)["modes"]["primary"]
        self.assertIsNone(actual["focal_share_of_signed_pooled_gain_percent"])
        self.assertEqual(actual["pooled_gain_M0_minus_M1"], 0.0)

    def test_source_git_blob_pin_rejects_modified_published_results(self):
        path = ROOT / m.SOURCE_REL
        _report, binding = m.read_pinned_report(path)
        self.assertEqual(binding["git_blob_sha1"], m.SOURCE_GIT_BLOB)
        with tempfile.TemporaryDirectory() as folder:
            fake = Path(folder) / "changed.json"
            fake.write_bytes(path.read_bytes() + b" ")
            with self.assertRaisesRegex(ValueError, "source Git blob mismatch"):
                m.read_pinned_report(fake)

    def test_actual_committed_aggregate_matches_regression_contract(self):
        source, _binding = m.read_pinned_report(ROOT / m.SOURCE_REL)
        result = m.audit(source)
        p = result["modes"]["primary"]
        g = result["modes"]["geographic_sensitivity"]
        self.assertAlmostEqual(p["focal_share_of_signed_pooled_gain_percent"], 89.85756591303811, places=7)
        self.assertAlmostEqual(g["focal_share_of_signed_pooled_gain_percent"], 93.52557853564254, places=7)
        self.assertAlmostEqual(p["other_seven_contexts"]["mean_gain"], .000676639958297333, places=12)
        self.assertAlmostEqual(g["other_seven_contexts"]["mean_gain"], .00026926979263112945, places=12)
        self.assertFalse(p["recorded_primary_stability_gate_passed"])
        self.assertFalse(g["recorded_primary_stability_gate_passed"])
        self.assertEqual(result["status"], "POST_HOC_CONTEXT_LEVERAGE_ACCOUNTING_NOT_CONFIRMATORY")


if __name__ == "__main__":
    unittest.main()
