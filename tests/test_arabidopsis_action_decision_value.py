"""Synthetic-only tests of experimental action-choice value (no real fruit rows)."""
from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

SRC=Path(__file__).resolve().parents[1]/"scripts"
sys.path.insert(0,str(SRC))
spec=importlib.util.spec_from_file_location("action_decision",SRC/"audit_arabidopsis_action_decision_value.py")
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def synthetic(invariant=False):
    outcome={
        "A":{"D|L":100.0,"D|S":0.0,"W|L":0.0,"W|S":0.0},
        "B":{"D|L":0.0,"D|S":0.0,"W|L":0.0,"W|S":100.0},
        "C":{"D|L":0.0,"D|S":0.0,"W|L":100.0,"W|S":0.0}
    }
    return [
        {
            "accession":acc,"replicate":str(rack),"action":action,
            "value":1.0 if invariant else outcome[acc][action],
            "fruit":1 if invariant else int(outcome[acc][action])**2,
        }
        for rack in range(1,6)
        for acc in ("A","B","C")
        for action in m.ACTION_ORDER
    ]


class DecisionValueTests(unittest.TestCase):
    def test_complete_panel_and_deterministic_tie(self):
        panel=synthetic()[:4]
        self.assertTrue(m.complete_panel(panel))
        self.assertFalse(m.complete_panel(panel[:3]))
        self.assertFalse(m.complete_panel(panel+[panel[0]]))
        self.assertFalse(m.complete_panel([panel[0],panel[1],panel[2],panel[2]]))
        self.assertEqual(m.choose_action({key:0 for key in m.ACTION_ORDER}),"D|L")
        with self.assertRaises(ValueError):
            m.choose_action({"D|L": 1.0})

    def test_when_action_responses_differ_choice_value_can_improve(self):
        report=m.evaluate_policy(synthetic(),bootstrap_draws=50)
        self.assertEqual(report["n_panels"],15)
        self.assertEqual(report["n_design_excluded_panels"],0)
        self.assertEqual(report["n_source_rows_in_complete_panels"],60)
        self.assertGreater(report["n_action_changes"],0)
        self.assertGreater(report["mean_gain_sqrt_fruit_per_panel"],0)
        self.assertEqual(len(report["by_heldout_rack"]),5)
        self.assertEqual(report["accession_cluster_uncertainty"]["n_accession_clusters"],3)
        self.assertNotIn("sample_id",str(report))

    def test_empty_decision_signal_cannot_be_promoted(self):
        report=m.evaluate_policy(synthetic(invariant=True),bootstrap_draws=40)
        self.assertEqual(report["n_action_changes"],0)
        self.assertEqual(report["mean_gain_sqrt_fruit_per_panel"],0)
        self.assertEqual(report["status"],"DECISION_VALUE_NOT_SUPPORTED_UNDER_FROZEN_GATE")

    def test_incomplete_and_duplicated_action_panels_are_excluded_without_outcome_selection(self):
        records=synthetic()
        removed=records.pop(3)  # one missing treatment from first complete panel
        records.append(dict(records[0]))  # duplicate in the same accession/rack
        result=m.evaluate_policy(records,bootstrap_draws=40)
        self.assertEqual(result["n_panels"],14)
        self.assertEqual(result["n_design_excluded_panels"],1)
        self.assertEqual(result["n_source_rows_excluded_by_design"],4)
        self.assertEqual(result["n_source_rows_in_complete_panels"],56)

    def test_reject_unfrozen_shrinkage_and_missing_racks(self):
        with self.assertRaisesRegex(ValueError,"pseudo"):
            m.evaluate_policy(synthetic(),pseudo=3.0)
        with self.assertRaisesRegex(ValueError,"rack"):
            m.evaluate_policy([r for r in synthetic() if r["replicate"]!="5"])

    def test_accession_bootstrap_retains_clusters(self):
        clusters={"A":[2.,3.],"B":[-3.,-2.],"C":[1.,2.]}
        a=m.bootstrap_accession_gain(clusters,draws=200,seed=101)
        b=m.bootstrap_accession_gain(clusters,draws=200,seed=101)
        self.assertEqual(a,b)
        self.assertEqual(a["n_accession_clusters"],3)
        self.assertEqual(a["n_positive_accessions"],2)
        self.assertEqual(a["n_negative_accessions"],1)
        self.assertEqual(len(a["conditional_95ci"]),2)


if __name__=="__main__":
    unittest.main()
