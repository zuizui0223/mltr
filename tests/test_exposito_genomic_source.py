"""Synthetic source-admission tests; no published phenotype values embedded."""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "prepare_exposito_genomic_fitness.py"
source = None
if MODULE_PATH.exists():
    spec = importlib.util.spec_from_file_location("exposito_source", MODULE_PATH)
    source = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = source
    spec.loader.exec_module(source)

CONTEXTS = ("mhi", "mhp", "mli", "mlp", "thi", "thp", "tli", "tlp")


def synthetic_records():
    accessions = [
        {"id": 30, "name": "C", "country": "ZZ", "latitude": 3, "longitude": 33},
        {"id": 10, "name": "A", "country": "ZZ", "latitude": 1, "longitude": 11},
        {"id": 20, "name": "B", "country": "ZZ", "latitude": 2, "longitude": 22},
    ]
    values = {10: [1, 2, 3, 4, 5, 6, 7, 8], 20: [0] * 8,
              30: [9, 10, 11, 12, 13, 14, 15, 16]}
    summaries = []
    for identifier in (30, 20, 10):
        for context, value in reversed(list(zip(CONTEXTS, values[identifier]))):
            summaries.append({"id": identifier,
                              "site": "madrid" if context[0] == "m" else "tuebingen",
                              "water": context[1], "indpop": context[2],
                              "Fitness": value})
    return accessions, summaries


def aligned_distance():
    return np.array([[0, .2, .3], [.2, 0, .4], [.3, .4, 0]])


class ExpositoSourceTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(source, "The production source implementation is not present yet")

    def prepare(self, accessions=None, summaries=None, matrix=None,
                row_ids=("10", "20", "30"), column_ids=("10", "20", "30")):
        default_accessions, default_summaries = synthetic_records()
        return source.prepare_from_records(
            default_accessions if accessions is None else accessions,
            default_summaries if summaries is None else summaries,
            row_ids, column_ids,
            aligned_distance() if matrix is None else matrix,
        )

    def test_labels_align_independently_reordered_rows_columns_and_phenotypes(self):
        # A positional join, lexicographic context bug or coordinate swap must fail.
        matrix = np.array([[.4, 0, .3], [.2, .3, 0], [0, .4, .2]])
        arrays, audit = self.prepare(matrix=matrix, row_ids=("30", "10", "20"),
                                     column_ids=("20", "30", "10"))
        self.assertEqual(arrays["ids"].tolist(), ["10", "20", "30"])
        self.assertEqual(arrays["contexts"].tolist(), list(CONTEXTS))
        np.testing.assert_array_equal(arrays["coords"], [[1, 11], [2, 22], [3, 33]])
        np.testing.assert_array_equal(arrays["distance"], [[0, .2, .3], [.2, 0, .4], [.3, .4, 0]])
        np.testing.assert_array_equal(arrays["fitness"],
                                      [[1, 2, 3, 4, 5, 6, 7, 8], [0] * 8,
                                       [9, 10, 11, 12, 13, 14, 15, 16]])
        self.assertEqual(audit["n_response_cells"], 24)

    def test_missing_context_and_missing_distance_are_reported_but_zeros_survive(self):
        # Treating reproductive zero as missing, imputing an absent context, or
        # admitting a subject without a labelled distance record must fail.
        accessions, summaries = synthetic_records()
        summaries = [r for r in summaries if not (
            r["id"] == 30 and r["site"] == "madrid" and r["water"] == "l" and r["indpop"] == "p")]
        accessions.append({"id": 40, "name": "D", "country": "ZZ", "latitude": 4, "longitude": 44})
        summaries += [dict(r, id=40) for r in summaries if r["id"] == 10]
        arrays, audit = self.prepare(accessions=accessions, summaries=summaries)
        self.assertEqual(arrays["ids"].tolist(), ["10", "20"])
        np.testing.assert_array_equal(arrays["fitness"][1], np.zeros(8))
        excluded = {row["id"]: row for row in audit["excluded_accessions"]}
        self.assertEqual(set(excluded), {"30", "40"})
        self.assertEqual(excluded["30"]["missing_contexts"], ["mlp"])
        self.assertIn("missing_genetic_distance", excluded["40"]["reasons"])

    def test_duplicate_accession_metadata_is_rejected(self):
        accessions, summaries = synthetic_records()
        accessions.append(dict(accessions[0], latitude=12))
        with self.assertRaisesRegex(ValueError, "duplicate.*accession"):
            self.prepare(accessions=accessions, summaries=summaries)

    def test_duplicate_accession_context_is_rejected_even_if_value_matches(self):
        _, summaries = synthetic_records()
        summaries.append(dict(summaries[0]))
        with self.assertRaisesRegex(ValueError, "duplicate.*context"):
            self.prepare(summaries=summaries)

    def test_unlabelled_or_ambiguous_genetic_axes_fail_closed(self):
        cases = [(("10", "10", "30"), ("10", "20", "30")),
                 (("10", "20", "30"), ("10", "20", "20")),
                 (("10", "20", "30"), ("10", "20", "40"))]
        for rows, columns in cases:
            with self.subTest(rows=rows, columns=columns), self.assertRaises(ValueError):
                self.prepare(row_ids=rows, column_ids=columns)

    def test_invalid_distances_are_rejected_before_cohort_output(self):
        mutations = []
        a = aligned_distance(); a[0, 1] = np.nan; mutations.append(a)
        a = aligned_distance(); a[0, 1] = a[1, 0] = -.2; mutations.append(a)
        a = aligned_distance(); a[0, 1] = .25; mutations.append(a)
        a = aligned_distance(); a[0, 0] = .01; mutations.append(a)
        for index, matrix in enumerate(mutations):
            with self.subTest(case=index), self.assertRaises(ValueError):
                self.prepare(matrix=matrix)

    def test_identical_measured_profiles_cannot_be_admitted_as_unseen_genotypes(self):
        matrix = aligned_distance(); matrix[0, 1] = matrix[1, 0] = 0
        with self.assertRaisesRegex(ValueError, "off-diagonal zero"):
            self.prepare(matrix=matrix)

    def test_invalid_response_and_coordinates_do_not_silently_become_zeros(self):
        accessions, summaries = synthetic_records()
        bad_summary = copy.deepcopy(summaries); bad_summary[0]["Fitness"] = -1
        with self.assertRaisesRegex(ValueError, "Fitness"):
            self.prepare(summaries=bad_summary)
        bad_meta = copy.deepcopy(accessions); bad_meta[0]["latitude"] = np.nan
        with self.assertRaisesRegex(ValueError, "coordinate"):
            self.prepare(accessions=bad_meta)

    def test_exact_hash_check_rejects_equal_length_altered_bytes(self):
        # A size-only check or an optional hash gate would miss this alteration.
        raw = b"synthetic source A"
        digest = hashlib.sha256(raw).hexdigest()
        source.verify_source_bytes(raw, expected_sha256=digest,
                                   expected_size=len(raw), label="synthetic")
        with self.assertRaisesRegex(ValueError, "hash"):
            source.verify_source_bytes(b"synthetic source B", expected_sha256=digest,
                                       expected_size=len(raw), label="synthetic")

    def test_written_npz_is_bound_to_audit_and_keeps_only_declared_arrays(self):
        arrays, audit = self.prepare()
        with tempfile.TemporaryDirectory() as directory:
            npz = Path(directory) / "prepared.npz"
            report = Path(directory) / "audit.json"
            source.write_outputs(arrays, audit, npz, report)
            written = json.loads(report.read_text())
            self.assertEqual(written["prepared_npz_sha256"], hashlib.sha256(npz.read_bytes()).hexdigest())
            self.assertEqual(written["n_accessions"], 3)
            with np.load(npz, allow_pickle=False) as loaded:
                self.assertEqual(set(loaded.files), {"ids", "coords", "distance", "fitness", "contexts"})
                np.testing.assert_array_equal(loaded["fitness"], arrays["fitness"])


if __name__ == "__main__":
    unittest.main()
