#!/usr/bin/env python3
"""Independent replay of the frozen Exposito benchmark; imports no project code.

Numerics are implemented directly from the committed protocol. This verification
uses dense linear solves, retains no sample-level output, and fits no alternatives.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import time

import numpy as np


PROTOCOL_SHA256 = "9dec1cdbe003cd4d586ad1bc122e261b61761b5b25aa8366452601ddc3b0b1f6"
INPUT_SHA256_ALLOWLIST = {
    "82cdfbcbdf60ae8fc5dd0fcb5872feba7019e0917a3fd02aebbfdb7434c41ec5",
    "cf0838bb2e026a9cc571d61a3cb7db8da0a7a26310c791ce3e3f22f103a928c5",
}
CONTEXTS = ["mhi", "mhp", "mli", "mlp", "thi", "thp", "tli", "tlp"]
LAMBDAS = (0.01, 0.1, 1.0, 10.0)
MODELS = ("mean", "M0", "M1")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ids_digest(ids: np.ndarray, indices: np.ndarray) -> str:
    values = sorted((str(ids[j]) for j in indices), key=int)
    return hashlib.sha256(("\n".join(values) + "\n").encode()).hexdigest()


def random_sets(indices: np.ndarray, nfold: int, seed: int) -> list[np.ndarray]:
    ordered = np.sort(np.asarray(indices, dtype=int))
    randomized = np.random.default_rng(seed).permutation(ordered)
    return [np.sort(x) for x in np.array_split(randomized, nfold)]


def cell_sets(indices: np.ndarray, cells: np.ndarray, nfold: int) -> list[np.ndarray]:
    groups: dict[tuple[int, int], list[int]] = defaultdict(list)
    for j in np.sort(indices):
        groups[tuple(int(v) for v in cells[j])].append(int(j))
    if len(groups) < nfold:
        raise ValueError("Too few geographic cells for frozen grouped CV")
    ordered = sorted(groups, key=lambda key: (-len(groups[key]), key))
    buckets: list[list[int]] = [[] for _ in range(nfold)]
    sizes = [0] * nfold
    for key in ordered:
        chosen = min(range(nfold), key=lambda f: (sizes[f], f))
        buckets[chosen].extend(groups[key])
        sizes[chosen] += len(groups[key])
    return [np.asarray(sorted(bucket), dtype=int) for bucket in buckets]


def training_standardize(train: np.ndarray, test: np.ndarray):
    mean = train.mean(axis=0)
    sd = train.std(axis=0, ddof=0)
    variable = sd > 0
    a = np.zeros_like(train, dtype=float)
    b = np.zeros_like(test, dtype=float)
    a[:, variable] = (train[:, variable] - mean[variable]) / sd[variable]
    b[:, variable] = (test[:, variable] - mean[variable]) / sd[variable]
    return a, b


def polynomial(z: np.ndarray) -> np.ndarray:
    lat, lon = z[:, 0], z[:, 1]
    return np.column_stack((lat, lon, lat**2, lat * lon, lon**2))


def center_kernel(train: np.ndarray, test: np.ndarray):
    column_means = train.mean(axis=0)
    row_means = train.mean(axis=1)
    grand = train.mean()
    centered_train = train - row_means[:, None] - column_means[None, :] + grand
    centered_test = test - test.mean(axis=1)[:, None] - column_means[None, :] + grand
    return centered_train, centered_test


def unit_diagonal(train: np.ndarray, test: np.ndarray):
    scale = float(np.trace(train) / len(train))
    if scale < 0:
        raise ValueError("Negative mean diagonal in a purported kernel")
    if scale == 0:
        return np.zeros_like(train), np.zeros_like(test)
    return train / scale, test / scale


def construct_kernels(coords, distance, train_indices, test_indices, checks):
    z_train, z_test = training_standardize(coords[train_indices], coords[test_indices])
    x_train, x_test = training_standardize(polynomial(z_train), polynomial(z_test))
    geo = unit_diagonal(*center_kernel(x_train @ x_train.T, x_test @ x_train.T))

    d_train = distance[np.ix_(train_indices, train_indices)]
    d_test = distance[np.ix_(test_indices, train_indices)]
    off_diagonal = d_train[~np.eye(len(train_indices), dtype=bool)]
    positive = off_diagonal[off_diagonal > 0]
    if len(positive) == 0:
        raise ValueError("No positive training genetic distances")
    tau = float(np.median(positive))
    g_train = np.exp(-d_train / tau)
    g_test = np.exp(-d_test / tau)
    genetic = unit_diagonal(*center_kernel(g_train, g_test))
    eig = np.linalg.eigvalsh(genetic[0])
    tolerance = 1e-8 * max(1.0, float(eig[-1]))
    if float(eig[0]) < -tolerance:
        raise ValueError("Frozen genetic-kernel PSD gate failed")
    checks.append({"n_train": len(train_indices), "tau": tau,
                   "minimum_eigenvalue": float(eig[0]),
                   "maximum_eigenvalue": float(eig[-1]), "tolerance": tolerance})
    mixed = unit_diagonal(geo[0] + genetic[0], geo[1] + genetic[1])
    return {"M0": geo, "M1": mixed}


def relative_targets(fitness, train_indices, test_indices):
    mean = fitness[train_indices].mean(axis=0)
    if not np.isfinite(mean).all() or np.any(mean <= 0):
        raise ValueError("Frozen positive training target mean gate failed")
    return fitness[train_indices] / mean - 1.0, fitness[test_indices] / mean, mean


def predict(kernel_pair, centered_target, lam):
    train_kernel, test_kernel = kernel_pair
    n = len(centered_target)
    lhs = train_kernel + np.eye(n) * (n * lam)
    alpha = np.linalg.solve(lhs, centered_target)
    return np.maximum(0.0, 1.0 + test_kernel @ alpha)


def paired_interval(delta, cells, mode):
    rng = np.random.default_rng(20261123)
    accession_delta = delta.mean(axis=1)
    if mode == "primary":
        draws = rng.integers(0, len(accession_delta), size=(2000, len(accession_delta)))
        replicates = accession_delta[draws].mean(axis=1)
    else:
        _, membership = np.unique(cells, axis=0, return_inverse=True)
        counts = np.bincount(membership)
        totals = np.bincount(membership, weights=accession_delta)
        g = len(counts)
        draws = rng.integers(0, g, size=(2000, g))
        replicates = totals[draws].sum(axis=1) / counts[draws].sum(axis=1)
    endpoints = np.quantile(replicates, [0.025, 0.975], method="linear")
    return {"lower": float(endpoints[0]), "upper": float(endpoints[1]),
            "draws": 2000, "seed": 20261123,
            "method": "paired conditional percentile; linear quantiles",
            "resampling_unit": "accession" if mode == "primary" else "geographic_cell"}


def run_mode(mode, ids, coords, distance, fitness, cells):
    n = len(ids)
    all_indices = np.arange(n)
    if mode == "primary":
        outer_sets = random_sets(all_indices, 5, 20261122)
    else:
        outer_sets = cell_sets(all_indices, cells, 5)
    squared_errors = {name: np.full_like(fitness, np.nan) for name in MODELS}
    coverage = np.zeros(n, dtype=int)
    fold_records = []
    psd_checks = []

    for outer_number, test in enumerate(outer_sets, start=1):
        train = np.setdiff1d(all_indices, test)
        if mode == "primary":
            inner_sets = random_sets(train, 3, 20261122 + outer_number)
        else:
            inner_sets = cell_sets(train, cells, 3)
        inner_sse = {name: np.zeros(len(LAMBDAS), dtype=float) for name in ("M0", "M1")}
        inner_count = 0
        for valid in inner_sets:
            fit_indices = np.setdiff1d(train, valid)
            kernels = construct_kernels(coords, distance, fit_indices, valid, psd_checks)
            centered, target, _ = relative_targets(fitness, fit_indices, valid)
            for name in ("M0", "M1"):
                for j, lam in enumerate(LAMBDAS):
                    residual = predict(kernels[name], centered, lam) - target
                    inner_sse[name][j] += float(np.sum(residual**2))
            inner_count += target.size

        validation_losses = {name: scores / inner_count for name, scores in inner_sse.items()}
        chosen = {}
        for name, losses in validation_losses.items():
            best = float(losses.min())
            tied = [lam for lam, value in zip(LAMBDAS, losses) if abs(float(value) - best) <= 1e-12]
            chosen[name] = max(tied)

        outer_kernels = construct_kernels(coords, distance, train, test, psd_checks)
        centered, target, target_means = relative_targets(fitness, train, test)
        squared_errors["mean"][test] = (1.0 - target)**2
        for name in ("M0", "M1"):
            squared_errors[name][test] = (predict(outer_kernels[name], centered, chosen[name]) - target)**2
        coverage[test] += 1
        losses = {name: float(errors[test].mean()) for name, errors in squared_errors.items()}
        fold_records.append({
            "fold": outer_number, "n_train": len(train), "n_test": len(test),
            "heldout_sorted_id_sha256": ids_digest(ids, test),
            "inner_n_valid": [len(v) for v in inner_sets],
            "inner_heldout_sorted_id_sha256": [ids_digest(ids, v) for v in inner_sets],
            "selected_lambda": chosen,
            "pooled_inner_mse_by_lambda": {name: {str(lam): float(value) for lam, value in zip(LAMBDAS, values)}
                                           for name, values in validation_losses.items()},
            "training_target_means": target_means.tolist(),
            "mse": losses, "gain_M0_minus_M1": losses["M0"] - losses["M1"],
        })
        print(f"{mode}: completed outer fold {outer_number}/5", flush=True)

    if not np.all(coverage == 1) or not all(np.isfinite(e).all() for e in squared_errors.values()):
        raise AssertionError("Incomplete or duplicated out-of-fold predictions")
    losses = {name: float(errors.mean()) for name, errors in squared_errors.items()}
    by_context = {}
    for j, context in enumerate(CONTEXTS):
        item = {name: float(errors[:, j].mean()) for name, errors in squared_errors.items()}
        item["gain_M0_minus_M1"] = item["M0"] - item["M1"]
        by_context[context] = item
    by_site = {}
    for site, columns in (("Madrid", slice(0, 4)), ("Tuebingen", slice(4, 8))):
        item = {name: float(errors[:, columns].mean()) for name, errors in squared_errors.items()}
        item["gain_M0_minus_M1"] = item["M0"] - item["M1"]
        by_site[site] = item
    gain = losses["M0"] - losses["M1"]
    interval = paired_interval(squared_errors["M0"] - squared_errors["M1"], cells, mode)
    result = {"n_accessions": n, "n_contexts": 8, "pooled_mse": losses,
              "gain_M0_minus_M1": gain, "paired_gain_interval": interval,
              "by_context": by_context, "by_site": by_site, "folds": fold_records,
              "training_genetic_kernel_checks": {
                  "number_of_fits": len(psd_checks),
                  "minimum_observed_eigenvalue": min(x["minimum_eigenvalue"] for x in psd_checks),
                  "maximum_observed_eigenvalue": max(x["maximum_eigenvalue"] for x in psd_checks),
                  "minimum_tau": min(x["tau"] for x in psd_checks),
                  "maximum_tau": max(x["tau"] for x in psd_checks),
                  "all_passed": True}}
    if mode == "primary":
        criteria = {
            "positive_pooled_gain": gain > 0,
            "positive_interval_lower_endpoint": interval["lower"] > 0,
            "positive_gain_every_outer_fold": all(x["gain_M0_minus_M1"] > 0 for x in fold_records),
            "positive_gain_both_sites": all(x["gain_M0_minus_M1"] > 0 for x in by_site.values()),
            "M1_beats_mean": losses["M1"] < losses["mean"],
        }
        result["primary_numerical_gate"] = {"passed": all(criteria.values()), "conditions": criteria}
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--protocol", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    actual_input_sha256 = sha256(args.input)
    if sha256(args.protocol) != PROTOCOL_SHA256 or actual_input_sha256 not in INPUT_SHA256_ALLOWLIST:
        raise ValueError("Input or frozen protocol checksum mismatch")
    with np.load(args.input, allow_pickle=False) as data:
        ids = data["ids"].copy()
        coords = data["coords"].astype(float)
        distance = data["distance"].astype(float)
        fitness = data["fitness"].astype(float)
        contexts = data["contexts"].tolist()
    assert ids.shape == (514,) and coords.shape == (514, 2)
    assert distance.shape == (514, 514) and fitness.shape == (514, 8)
    assert contexts == CONTEXTS
    assert len(set(ids)) == 514
    ordering = np.argsort(np.asarray([int(x) for x in ids]))
    ids, coords, fitness = ids[ordering], coords[ordering], fitness[ordering]
    distance = distance[np.ix_(ordering, ordering)]
    assert all(np.isfinite(x).all() for x in (coords, distance, fitness))
    assert np.all(distance >= 0) and np.all(fitness >= 0)
    assert np.array_equal(distance, distance.T) and np.all(np.diag(distance) == 0)
    assert np.all(distance[~np.eye(514, dtype=bool)] > 0)
    assert np.all(np.abs(coords[:, 0]) <= 90) and np.all(np.abs(coords[:, 1]) <= 180)
    cells = np.floor((coords + np.array([90.0, 180.0])) / 5.0).astype(int)
    started = time.perf_counter()
    results = {
        "purpose": "Independent computational replay, not an independent biological replicate",
        "protocol_commit": "8bd3a0ef77a6800fe5493a15461e1064fc8c30fa",
        "protocol_sha256": PROTOCOL_SHA256, "input_sha256": actual_input_sha256,
        "script_sha256": sha256(Path(__file__)),
        "python_version": platform.python_version(), "numpy_version": np.__version__,
        "linear_solver": "numpy.linalg.solve; no production imports",
        "thread_configuration": {key: os.environ.get(key) for key in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS")},
        "cohort_sorted_id_sha256": ids_digest(ids, np.arange(len(ids))),
        "geographic_cell_count": int(len(np.unique(cells, axis=0))),
    }
    for mode in ("primary", "geographic"):
        results[mode] = run_mode(mode, ids, coords, distance, fitness, cells)
    results["elapsed_seconds"] = time.perf_counter() - started
    results["finished_utc"] = datetime.now(timezone.utc).isoformat()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(results, indent=2, allow_nan=False) + "\n")
    print(f"Independent replay complete: {args.output}", flush=True)


if __name__ == "__main__":
    main()
