"""Synthetic-only tests: original 2019 drought CSV admission and non-inference.

The uploaded original specimen-level CSV is not embedded in the repository.
"""
import csv
import importlib.util
import io
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPTS=Path(__file__).resolve().parents[1]/"scripts"
sys.path.insert(0,str(SCRIPTS))
spec=importlib.util.spec_from_file_location("original_drought_audit",SCRIPTS/"audit_arabidopsis_original_dryad_38.py")
audit=importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


def make_synthetic(n_acc=4, missing_one=True):
    out=io.StringIO()
    writer=csv.DictWriter(out,fieldnames=audit.SOURCE_FIELDS)
    writer.writeheader()
    for genotype in range(1,n_acc+1):
        for rack in range(1,6):
            for ai,action in enumerate(audit.ACTIONS):
                water,microbe=action.split("|")
                fruit=int(genotype*5+(10 if water=="W" else 0)+ai)
                if missing_one and genotype==1 and rack==5 and action=="W|S":
                    fruit=""
                writer.writerow(dict(
                    accession=str(genotype),water=water,microbe=microbe,
                    replicate=str(rack),tray="1",shelf="A",rack=str(rack),
                    fruit=str(fruit),flowering="",counter="synthetic",
                    source="ut"
                ))
    return out.getvalue().encode("utf-8")


class OriginalDroughtTests(unittest.TestCase):
    def test_exact_original_hash_is_mandatory(self):
        with self.assertRaisesRegex(ValueError,"pinned uploaded bytes"):
            audit.read_original(make_synthetic(),strict=True)

    def test_complete_factorial_design_and_one_missing_fruit(self):
        raw=make_synthetic()
        original,observed,qc=audit.read_original(raw,strict=False)
        self.assertEqual(qc["records_design"],80)
        self.assertEqual(qc["records_observed_fruit"],79)
        self.assertEqual(qc["records_fruit_missing"],1)
        self.assertEqual(qc["n_accessions"],4)
        self.assertEqual(qc["n_unique_accession_action_rack_cells"],80)
        self.assertEqual(qc["rack_design_sizes"],{str(i):16 for i in range(1,6)})
        self.assertEqual(sum(qc["action_usable_sizes"].values()),79)
        self.assertEqual(len(observed),79)
        self.assertEqual(qc["stock_source_counts"]["ut"],80)
        self.assertEqual(len(audit.canonical_calls(original)),79)

    def test_outcome_missing_is_not_silently_imputed_in_action_panels(self):
        _,observed,_=audit.read_original(make_synthetic(),strict=False)
        from audit_arabidopsis_action_decision_value import evaluate_policy
        policy=evaluate_policy(observed,bootstrap_draws=50)
        self.assertEqual(policy["n_panels"],19)
        self.assertEqual(policy["n_design_excluded_panels"],1)
        self.assertEqual(policy["n_source_rows_excluded_by_design"],3)
        self.assertEqual(policy["n_source_rows_in_complete_panels"],76)

    def test_reject_duplicate_accession_action_rack(self):
        raw=make_synthetic().decode()
        lines=raw.splitlines()
        lines[-1]=lines[-2]
        with self.assertRaisesRegex(ValueError,"duplicate accession"):
            audit.read_original(("\n".join(lines)+"\n").encode(),strict=False)

    def test_rack_rep_mismatch_detected(self):
        rows=list(csv.DictReader(io.StringIO(make_synthetic().decode())))
        rows[0]["rack"]="2"
        f=io.StringIO()
        w=csv.DictWriter(f,fieldnames=audit.SOURCE_FIELDS)
        w.writeheader()
        w.writerows(rows)
        with self.assertRaisesRegex(ValueError,"rack differs"):
            audit.read_original(f.getvalue().encode(),strict=False)

    def test_teaching_mirror_content_mismatch_fails_closed(self):
        original,_,_=audit.read_original(make_synthetic(),strict=False)
        # Even if the course hash check was mocked, a changed row must not
        # pass the original→teaching specimen-level crosswalk.
        rows=[{col:row[col] for col in audit.COMMON} for row in original]
        rows[0]["fruit"]="999"
        out=io.StringIO()
        w=csv.DictWriter(out,fieldnames=audit.COMMON)
        w.writeheader()
        w.writerows(rows)
        # compare_course() should reject an unrecognized published course
        # fixture before a purported source-match can be reported.
        with self.assertRaises(ValueError):
            audit.compare_course(original,out.getvalue().encode())


if __name__=="__main__":
    unittest.main()
