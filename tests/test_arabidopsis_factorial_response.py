"""Offline synthetic-only tests for accession×factorial-action fruit prediction."""
import csv
import hashlib
import importlib.util
import io
import math
import sys
import unittest
from pathlib import Path

FILE=Path(__file__).resolve().parents[1]/"scripts"/"audit_arabidopsis_factorial_response.py"
spec=importlib.util.spec_from_file_location("arab_factorial",FILE)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def toy_csv():
    out=io.StringIO()
    writer=csv.DictWriter(out,fieldnames=m.COLUMNS)
    writer.writeheader()
    for rep in range(1,6):
        for a in ("A","B","C"):
            for water in ("D","W"):
                for microbe in ("L","S"):
                    action=water+"|"+microbe
                    # Strong accession-specific action differences. Each training
                    # fold sees every accession-action combination 4 times.
                    yield_value={
                        ("A","D|L"):9,("A","D|S"):0,("A","W|L"):1,("A","W|S"):16,
                        ("B","D|L"):0,("B","D|S"):16,("B","W|L"):9,("B","W|S"):0,
                        ("C","D|L"):16,("C","D|S"):1,("C","W|L"):0,("C","W|S"):9
                    }
                    writer.writerow(dict(accession=a,water=water,microbe=microbe,
                        replicate=str(rep),tray=str(rep),shelf="A",
                        rack=str(rep),fruit=yield_value[(a,action)],
                        flowering="NA",counter="test"))
    return out.getvalue().encode()


class FactorialResponseTests(unittest.TestCase):
    def test_source_sha_cannot_be_forged_with_untrusted_bytes(self):
        with self.assertRaisesRegex(ValueError,"Git blob"):
            m.checksum(toy_csv())

    def test_parser_retains_all_zero_fruit_and_separately_flags_missing_flowering(self):
        records,qc=m.parse_source(toy_csv(),exact_source=False)
        self.assertEqual(len(records),60)
        self.assertEqual(qc["n_accessions"],3)
        self.assertEqual(qc["n_replicate_racks"],5)
        self.assertEqual(qc["flowering_missing_but_fruit_retained"],60)
        self.assertEqual(set(qc["action_counts"]),m.ALLOWED_ACTIONS)
        self.assertGreater(qc["zero_fruit_records"],0)

    def test_rack_and_replicate_must_match(self):
        source=toy_csv().replace(b",A,1,",b",A,2,",1)
        # Replace the first parsed row's rack directly, without relying on
        # the row order of the CSV fixture.
        rows=list(csv.DictReader(io.StringIO(toy_csv().decode())))
        rows[0]["rack"]="2"
        out=io.StringIO()
        w=csv.DictWriter(out,fieldnames=m.COLUMNS)
        w.writeheader();w.writerows(rows)
        with self.assertRaisesRegex(ValueError,"rack/replicate"):
            m.parse_source(out.getvalue().encode(),exact_source=False)

    def test_all_rack_holdouts_are_accounted_for_and_action_model_has_signal(self):
        records,_=m.parse_source(toy_csv(),exact_source=False)
        report=m.score_folds(records,k_accession=1,k_action=1,bootstrap=100)
        self.assertEqual(report["n_tested"],60)
        self.assertEqual(len(report["folds"]),5)
        self.assertEqual(report["n_accessions"],3)
        self.assertEqual(sum(f["n"] for f in report["folds"]),60)
        self.assertLess(report["heldout_mse"]["P2"],report["heldout_mse"]["P1"])
        self.assertTrue(math.isfinite(report["mean_gain_P2_minus_P1"]))
        self.assertEqual(len(report["accession_resampled_conditional_95_interval"]),2)

    def test_centered_action_offsets_cannot_redefine_genotype_intercept(self):
        records,_=m.parse_source(toy_csv(),exact_source=False)
        training=[row for row in records if row["replicate"] != "5"]
        _mu,base,cell=m.train_models(
            training,k_accession=1,k_action=1,center_action=True
        )
        for genotype in ("A","B","C"):
            sum_weighted=0.0
            n=0
            for action in m.ALLOWED_ACTIONS:
                count=sum(row["accession"] == genotype and row["action"] == action
                          for row in training)
                sum_weighted+=count*cell[(genotype,action)]
                n+=count
            self.assertGreater(n,0)
            self.assertAlmostEqual(sum_weighted/n,0.0,places=12)
        observed=m.score_folds(
            records,k_accession=1,k_action=1,bootstrap=100,
            center_action=True
        )
        self.assertTrue(observed["model_specification"]["center_action_effects"])
        self.assertGreater(observed["mean_gain_P2_minus_P1"],0)

    def test_unsupported_genotype_not_silently_predicted(self):
        records,_=m.parse_source(toy_csv(),exact_source=False)
        fit=m.train_models(records[:40])
        with self.assertRaises(ValueError):
            m.predict_one({"accession":"NEW","action":"D|L"},fit)

    def test_repeated_assignment_is_not_a_unique_specimen_duplicate(self):
        s=toy_csv().decode().splitlines()
        s.append(s[-1])
        rows,qc=m.parse_source(("\n".join(s)+"\n").encode(),exact_source=False)
        self.assertEqual(len(rows),61)
        self.assertEqual(qc["repeated_accession_action_replicate_assignments"],1)
        self.assertEqual(qc["n_accessions"],3)

    def test_smoothing_parameters_must_be_strictly_positive(self):
        records,_=m.parse_source(toy_csv(),exact_source=False)
        with self.assertRaises(ValueError):
            m.train_models(records,k_accession=0)
        with self.assertRaises(ValueError):
            m.train_models(records,k_action=-1)


if __name__=="__main__":
    unittest.main()
