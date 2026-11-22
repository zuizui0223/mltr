"""Synthetic behavior tests for the frozen genomic prediction benchmark.

No public source observations or real prediction scores are used in these tests.
"""
import importlib.util
import hashlib
import json
from pathlib import Path
import tempfile
import subprocess
import sys
import unittest

try:
    import numpy as np
except ImportError:
    raise unittest.SkipTest("NumPy unavailable; dedicated empirical CI installs it")

SOURCE = Path(__file__).resolve().parents[1] / "scripts" / "analyze_exposito_genomic_fitness.py"
spec = importlib.util.spec_from_file_location("exposito_prediction", SOURCE)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

CONTEXTS = np.array(["mhi", "mhp", "mli", "mlp", "thi", "thp", "tli", "tlp"])


def fixture(n=30):
    i = np.arange(n)
    coords = np.column_stack((25 + (i // 3) * 6 + (i % 3) * .1,
                              -45 + (i // 3) * 6 + (i % 3) * .2))
    fitness = 2 + .15 * (i[:, None] % 7) + .1 * np.arange(1, 9)[None, :]
    return {"ids": np.array([str(100000 + x) for x in i]), "coords": coords,
            "distance": np.abs(i[:, None] - i[None, :]) / 100.,
            "fitness": fitness, "contexts": CONTEXTS.copy()}


class KernelBehaviorTests(unittest.TestCase):
    def test_centering_uses_training_means_for_cross_kernel(self):
        # Hand result: centered train=[[.5,-.5],[-.5,.5]], scale=.5.
        # Cross row [3,1] centers to [1,-1] using ONLY train column means.
        result = module.center_scale(np.array([[2., 1.], [1., 2.]]),
                                     np.array([[3., 1.]]))
        self.assertIsNotNone(result)
        train, cross, scale = result
        np.testing.assert_allclose(train, [[1., -1.], [-1., 1.]])
        np.testing.assert_allclose(cross, [[2., -2.]])
        self.assertAlmostEqual(scale, .5)

    def test_intercept_and_ridge_solution_have_hand_computed_value(self):
        # K+n*lambda*I=[[2,-1],[-1,2]] and centered y=[-1,1].
        result = module.fit_predict(np.array([[1., -1.], [-1., 1.]]),
                                    np.array([[1., -1.], [-1., 1.]]),
                                    np.array([[0.], [2.]]), .5)
        self.assertIsNotNone(result)
        predictions, means = result
        np.testing.assert_allclose(predictions, [[1 / 3], [5 / 3]])
        np.testing.assert_allclose(means, [1.])

    def test_constant_training_target_predicts_the_mean_without_kernel_signal(self):
        result = module.fit_predict(np.zeros((3, 3)), np.zeros((2, 3)),
                                    np.tile([4., 12.], (3, 1)), .1)
        self.assertIsNotNone(result)
        predictions, means = result
        np.testing.assert_allclose(predictions, np.ones((2, 2)))
        np.testing.assert_allclose(means, [4., 12.])

    def test_negative_predictions_are_clipped_for_nonnegative_fitness(self):
        result = module.fit_predict(np.array([[1., -1.], [-1., 1.]]),
                                    np.array([[10., -10.]]),
                                    np.array([[0.], [2.]]), .5)
        self.assertIsNotNone(result)
        np.testing.assert_array_equal(result[0], [[0.]])

    def test_nonpositive_training_mean_is_not_imputed(self):
        with self.assertRaises(ValueError):
            module.fit_predict(np.eye(2), np.ones((1, 2)), np.zeros((2, 1)), .1)

    def test_indefinite_kernel_stops_instead_of_silent_eigenvalue_repair(self):
        with self.assertRaises(ValueError):
            module.check_psd(np.array([[1., 2.], [2., 1.]]))

    def test_kernel_scaling_and_training_only_bandwidth(self):
        data = fixture()
        train, test = np.arange(20), np.arange(20, 30)
        result = module.make_kernels(data["coords"], data["distance"], train, test)
        self.assertIsNotNone(result)
        kernels, diagnostics = result
        for name in ("M0", "M1"):
            np.testing.assert_allclose(kernels[name][0].mean(axis=0), 0, atol=1e-12)
            self.assertAlmostEqual(float(np.diag(kernels[name][0]).mean()), 1.)
        # Alter ONLY test-test distances. Neither training nor cross kernels
        # or the fitted bandwidth may change.
        changed = data["distance"].copy()
        changed[np.ix_(test, test)] *= 100
        other, other_diagnostics = module.make_kernels(data["coords"], changed, train, test)
        self.assertEqual(diagnostics["tau"], other_diagnostics["tau"])
        for name in ("M0", "M1"):
            np.testing.assert_array_equal(kernels[name][0], other[name][0])
            np.testing.assert_array_equal(kernels[name][1], other[name][1])


class InputAndSplitTests(unittest.TestCase):
    def test_numeric_id_sort_keeps_all_arrays_aligned(self):
        data = fixture()
        order = np.arange(30)[::-1]
        shuffled = {"ids": data["ids"][order], "coords": data["coords"][order],
                    "fitness": data["fitness"][order], "contexts": data["contexts"],
                    "distance": data["distance"][np.ix_(order, order)]}
        result = module.validate_arrays(shuffled)
        self.assertIsNotNone(result)
        for key in data:
            np.testing.assert_array_equal(result[key], data[key])

    def test_invalid_source_arrays_fail_before_scoring(self):
        cases = []
        data = fixture(); data["ids"][1] = data["ids"][0]; cases.append(data)
        data = fixture(); data["fitness"][0, 0] = np.nan; cases.append(data)
        data = fixture(); data["fitness"][0, 0] = -1; cases.append(data)
        data = fixture(); data["coords"][0, 0] = 91; cases.append(data)
        data = fixture(); data["distance"][0, 1] = .8; cases.append(data)
        data = fixture(); data["distance"][0, 1] = data["distance"][1, 0] = 0; cases.append(data)
        data = fixture(); data["contexts"] = data["contexts"][::-1]; cases.append(data)
        for i, case in enumerate(cases):
            with self.subTest(case=i):
                with self.assertRaises(ValueError):
                    module.validate_arrays(case)

    def test_accession_splits_cover_each_row_once_and_are_disjoint(self):
        result = module.accession_folds(31, 5, 20261122)
        self.assertIsNotNone(result)
        scored = []
        for train, held in result:
            self.assertFalse(set(train) & set(held))
            self.assertEqual(len(train) + len(held), 31)
            scored.extend(held.tolist())
        self.assertEqual(sorted(scored), list(range(31)))
        self.assertEqual([len(h) for _, h in result], [7, 6, 6, 6, 6])

    def test_spatial_splits_keep_whole_cells_and_use_lexical_size_ties(self):
        cells = np.array([[0, 0]] * 3 + [[1, 0]] * 2 + [[2, 0]] * 2 + [[3, 0]])
        result = module.spatial_folds(cells, 3)
        self.assertIsNotNone(result)
        expected = [[0, 1, 2], [3, 4, 7], [5, 6]]
        for (train, held), want in zip(result, expected):
            self.assertEqual(held.tolist(), want)
            self.assertFalse(set(map(tuple, cells[train])) & set(map(tuple, cells[held])))
        self.assertEqual(sorted(np.concatenate([h for _, h in result]).tolist()), list(range(8)))

    def test_geographic_cells_respect_fixed_boundaries(self):
        result = module.geographic_cells(np.array([[-90., -180.], [-85., -175.],
                                                    [-85.0001, -175.0001]]))
        self.assertIsNotNone(result)
        np.testing.assert_array_equal(result, [[0, 0], [1, 1], [0, 0]])


class NestedPredictionTests(unittest.TestCase):
    def test_heldout_targets_cannot_affect_predictions_or_selected_lambda(self):
        data = fixture()
        train, held = np.arange(24), np.arange(24, 30)
        original = module.fit_outer_fold(data, train, held, "accession", 1)
        self.assertIsNotNone(original)
        changed = {key: value.copy() for key, value in data.items()}
        changed["fitness"][held] *= 10000
        altered = module.fit_outer_fold(changed, train, held, "accession", 1)
        self.assertEqual(original["selected_lambdas"], altered["selected_lambdas"])
        for name in ("Mean", "M0", "M1"):
            np.testing.assert_array_equal(original["predictions"][name], altered["predictions"][name])

    def test_positive_context_multipliers_cancel_in_nested_predictions(self):
        data = fixture()
        train, held = np.arange(24), np.arange(24, 30)
        original = module.fit_outer_fold(data, train, held, "accession", 1)
        self.assertIsNotNone(original)
        changed = {key: value.copy() for key, value in data.items()}
        changed["fitness"] *= np.array([.01, .1, 1., 10., 100., 1000., .2, 2.])[None, :]
        altered = module.fit_outer_fold(changed, train, held, "accession", 1)
        self.assertEqual(original["selected_lambdas"], altered["selected_lambdas"])
        for name in ("M0", "M1"):
            np.testing.assert_allclose(original["predictions"][name], altered["predictions"][name], atol=1e-12)

    def test_spatial_inner_folds_use_the_outer_training_cells_only(self):
        data = fixture()
        train, held = np.arange(24), np.arange(24, 30)
        result = module.fit_outer_fold(data, train, held, "geographic", 1)
        self.assertIsNotNone(result)
        self.assertTrue(all(x["group_overlap"] == 0 for x in result["inner_folds"]))
        self.assertEqual(sum(x["heldout_accessions"] for x in result["inner_folds"]), len(train))

    def test_constant_outcomes_report_zero_loss_and_failed_positive_gate(self):
        data = fixture()
        data["fitness"][:] = np.arange(1., 9.)
        result = module.evaluate(data, "accession")
        self.assertIsNotNone(result)
        self.assertFalse(result["numerical_gate"]["passed"])
        self.assertEqual(result["contrast"]["mean_gain"], 0.)
        self.assertEqual(result["contrast"]["conditional_ci95"], [0., 0.])
        for model in ("Mean", "M0", "M1"):
            self.assertEqual(result["models"][model]["mse"], 0.)
        for fold in result["folds"]:
            self.assertEqual(fold["selected_lambdas"], {"M0": 10., "M1": 10.})
        self.assertNotIn("100000", json.dumps(result))

    def test_cluster_bootstrap_keeps_unequal_group_denominators(self):
        result = module.conditional_interval(np.array([1., 0., 0., 0.]),
                                              np.array([[0, 0], [1, 0], [1, 0], [1, 0]]))
        self.assertIsNotNone(result)
        # Whole-cell draws yield 0, 1/4 or 1, not means of two cell means.
        self.assertEqual(result["point_estimate"], .25)
        self.assertEqual(result["ci95"], [0., 1.])


class InputBindingTests(unittest.TestCase):
    def test_prepared_bytes_must_match_source_audit_before_scoring(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "input.npz"
            path.write_bytes(b"original")
            audit = {"prepared_npz_sha256": hashlib.sha256(b"original").hexdigest()}
            module.verify_source_binding(path, audit)
            path.write_bytes(b"modified")
            with self.assertRaises(ValueError):
                module.verify_source_binding(path, audit)

    def test_missing_prepared_binding_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "input.npz"
            path.write_bytes(b"original")
            with self.assertRaises(ValueError):
                module.verify_source_binding(path, {})

    def test_cli_scores_both_modes_and_preserves_output_on_source_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            prepared, audit, protocol, output = [root / name for name in
                                                 ("prepared.npz", "audit.json", "protocol.md", "result.json")]
            np.savez(prepared, **fixture())
            audit.write_text(json.dumps({
                "prepared_npz_sha256": hashlib.sha256(prepared.read_bytes()).hexdigest(),
                "n_accessions": 30, "n_contexts": 8, "n_response_cells": 240,
                "source_files": [{"name": "synthetic", "sha256": "0" * 64}],
            }))
            protocol.write_text("Synthetic test protocol; never a biological result.\n")
            command = [sys.executable, str(SOURCE), "--prepared", str(prepared),
                       "--source-audit", str(audit), "--protocol", str(protocol),
                       "--output", str(output)]
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, msg=result.stderr)
            self.assertTrue(output.exists())
            report = json.loads(output.read_text())
            self.assertEqual(report["primary"]["response_cells"], 240)
            self.assertEqual(report["geographic_sensitivity"]["response_cells"], 240)
            self.assertEqual(report["provenance"]["protocol_sha256"],
                             hashlib.sha256(protocol.read_bytes()).hexdigest())
            previous = output.read_bytes()
            prepared.write_bytes(prepared.read_bytes() + b"changed")
            failed = subprocess.run(command, capture_output=True, text=True)
            self.assertNotEqual(failed.returncode, 0)
            self.assertEqual(output.read_bytes(), previous)


if __name__ == "__main__":
    unittest.main()
