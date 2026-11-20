"""Synthetic-only tests for source-locked 2019 drought seed-production estimates.

No original fruit rows or seed-per-fruit accession calibration values embedded.
"""
from __future__ import annotations

import csv
import importlib.util
import io
import sys
import unittest
from pathlib import Path

SCRIPTS=Path(__file__).resolve().parents[1]/"scripts"
sys.path.insert(0,str(SCRIPTS))
spec=importlib.util.spec_from_file_location("arab_original_seeds",SCRIPTS/"audit_arabidopsis_original_seed_fitness.py")
audit=importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


def mock_seed():
    stream=io.StringIO()
    writer=csv.DictWriter(stream,fieldnames=audit.SEED_COLUMNS)
    writer.writeheader()
    writer.writerow({"genotype":"A","Seed wet":"40","Seed dry":"20"})
    writer.writerow({"genotype":"B","Seed wet":"30.5","Seed dry":"25"})
    writer.writerow({"genotype":"C","Seed wet":"","Seed dry":"15"})
    return stream.getvalue().encode("utf-8")


def mock_fruits():
    items=[]
    for genotype in ("A","B","C"):
        for rack in range(1,6):
            for water,microbe in (("D","L"),("D","S"),("W","L"),("W","S")):
                fruit=(0 if genotype=="A" and water=="D" and rack==1
                       else 10 if water=="W" else 5)
                items.append({
                    "accession":genotype,"water":water,"microbe":microbe,
                    "rack":str(rack),"fruit":str(fruit)
                })
    items[7]["fruit"]=""  # one missing outcome in otherwise calibrated genotype A
    return items


class OriginalSeedEstimatesTests(unittest.TestCase):
    def test_source_hash_and_exact_header_are_mandatory(self):
        with self.assertRaisesRegex(ValueError,"hash/size"):
            audit.parse_seed_calibration(mock_seed(),strict=True)
        changed=mock_seed().replace(b"Seed wet",b"Seed unknown")
        with self.assertRaisesRegex(ValueError,"source columns"):
            audit.parse_seed_calibration(changed,strict=False)

    def test_missing_watering_calibration_is_none_never_zero(self):
        table,qc=audit.parse_seed_calibration(mock_seed(),strict=False)
        self.assertEqual(qc["n_genotypes"],3)
        self.assertEqual(qc["wet_observed"],2)
        self.assertEqual(qc["drought_observed"],3)
        self.assertEqual(qc["both_observed"],2)
        self.assertEqual(table["A"]["W"],40)
        self.assertIsNone(table["C"]["W"])
        self.assertEqual(table["B"]["D"],25)

    def test_reject_duplicate_or_nonpositive_seed_factors(self):
        duplicated=mock_seed()+b"A,21,15\n"
        with self.assertRaisesRegex(ValueError,"duplicated"):
            audit.parse_seed_calibration(duplicated,strict=False)
        wrong=mock_seed().replace(b"A,40,20",b"A,-3,20")
        with self.assertRaisesRegex(ValueError,"invalid seed-per-fruit"):
            audit.parse_seed_calibration(wrong,strict=False)

    def test_complete_water_pair_required_and_zero_fruit_is_retained(self):
        table,_=audit.parse_seed_calibration(mock_seed(),strict=False)
        rows,qc=audit.eligible_joint_rows(mock_fruits(),table,strict=False)
        self.assertEqual(qc["n_accessions_original"],3)
        self.assertEqual(qc["n_complete_seed_accessions"],2)
        self.assertEqual(qc["n_dropped_seed_incomplete_accessions"],1)
        self.assertEqual(len(rows),39)
        self.assertEqual(qc["n_original_fruit_missing_in_complete_cohort"],1)
        self.assertEqual(qc["n_dropped_design_rows_from_incomplete_seed_accessions"],20)
        test=[x for x in rows if x["accession"]=="A" and x["action"]=="D|L" and x["replicate"]=="1"][0]
        self.assertEqual(test["estimated_seed_count"],0)
        example=[x for x in rows if x["accession"]=="B" and x["action"]=="W|L" and x["replicate"]=="1"][0]
        self.assertEqual(example["estimated_seed_count"],305.0)

    def test_numeric_scale_and_centering_preserve_distinct_score_contracts(self):
        table,_=audit.parse_seed_calibration(mock_seed(),strict=False)
        rows,_=audit.eligible_joint_rows(mock_fruits(),table,strict=False)
        seed_raw=audit.score_on_outcome(rows,"estimated_seed_count","raw",True,100)
        seed_sqrt=audit.score_on_outcome(rows,"estimated_seed_count","sqrt",True,100)
        matched_fruit=audit.score_on_outcome(rows,"fruit","sqrt",True,100)
        self.assertEqual(seed_raw["n_tested"],39)
        self.assertTrue(seed_raw["model_specification"]["center_action_effects"])
        self.assertEqual(seed_raw["model_specification"]["outcome"],"raw_estimated_seed_count")
        self.assertEqual(seed_sqrt["model_specification"]["outcome"],"sqrt_estimated_seed_count")
        self.assertEqual(matched_fruit["model_specification"]["outcome"],"sqrt_fruit")
        self.assertEqual(len(seed_raw["folds"]),5)

    def test_ambiguous_genotype_join_fails_closed(self):
        table,_=audit.parse_seed_calibration(mock_seed(),strict=False)
        table.pop("C")
        with self.assertRaisesRegex(ValueError,"ID sets disagree"):
            audit.eligible_joint_rows(mock_fruits(),table,strict=False)


if __name__=="__main__":
    unittest.main()
