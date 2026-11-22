#!/usr/bin/env python3
"""Frozen conditional genomic prediction of published fitness summaries.

The predictor operates on accession-level published targets, not independent
plant observations. It does not infer causal variants, treatment policy value,
or exact MLTR transport. See the committed 2026-11-22 protocol for the estimand.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import platform
import re

import numpy as np

CONTEXTS = ("mhi", "mhp", "mli", "mlp", "thi", "thp", "tli", "tlp")
LAMBDAS = (.01, .1, 1., 10.)
SPLIT_SEED = 20261122
BOOTSTRAP_SEED = 20261123
BOOTSTRAP_DRAWS = 2000
MODELS = ("Mean", "M0", "M1")


def center_scale(train_kernel, cross_kernel):
    """Center a kernel around training samples and give it unit mean diagonal."""
    train = np.asarray(train_kernel, dtype=float)
    cross = np.asarray(cross_kernel, dtype=float)
    column_mean = train.mean(axis=0)
    grand_mean = float(train.mean())
    centered = train - train.mean(axis=1)[:, None] - column_mean[None, :] + grand_mean
    centered_cross = cross - cross.mean(axis=1)[:, None] - column_mean[None, :] + grand_mean
    scale = float(np.trace(centered) / len(centered))
    if scale <= 1e-14:
        return np.zeros_like(centered), np.zeros_like(centered_cross), 0.0
    return centered / scale, centered_cross / scale, scale


def fit_predict(train_kernel, cross_kernel, y_train, regularization):
    """Fit all context coefficients using training means and a fixed lambda."""
    y = np.asarray(y_train, dtype=float)
    kernel = np.asarray(train_kernel, dtype=float)
    cross = np.asarray(cross_kernel, dtype=float)
    if y.ndim != 2 or kernel.shape != (len(y), len(y)) or cross.ndim != 2:
        raise ValueError("incompatible training target or kernel dimensions")
    if cross.shape[1] != len(y) or not len(y):
        raise ValueError("incompatible cross-kernel dimensions")
    if not all(np.isfinite(a).all() for a in (y, kernel, cross)) or np.any(y < 0):
        raise ValueError("nonfinite kernel or invalid fitness")
    if not np.isfinite(regularization) or regularization <= 0:
        raise ValueError("regularization must be positive")
    means = y.mean(axis=0)
    if np.any(means <= 0) or not np.isfinite(means).all():
        raise ValueError("nonpositive or nonfinite training-context mean")
    coefficients = np.linalg.solve(
        kernel + len(y) * regularization * np.eye(len(y)), y / means - 1.
    )
    predictions = np.maximum(0., 1. + cross @ coefficients)
    if not np.isfinite(predictions).all():
        raise ValueError("nonfinite predictions")
    return predictions, means


def check_psd(kernel):
    """Reject substantial negative eigenvalues; do not repair the kernel."""
    eigenvalues = np.linalg.eigvalsh(kernel)
    smallest, largest = float(eigenvalues[0]), float(eigenvalues[-1])
    tolerance = 1e-8 * max(1., largest)
    if smallest < -tolerance:
        raise ValueError(f"genetic kernel is not PSD: minimum eigenvalue {smallest}")
    return {"minimum_eigenvalue": smallest, "largest_eigenvalue": largest,
            "negative_eigenvalue_tolerance": tolerance}


def make_kernels(coords, distance, train, test):
    """Build both kernels using only the declared training sample statistics."""
    coords = np.asarray(coords, dtype=float)
    train, test = np.asarray(train, dtype=int), np.asarray(test, dtype=int)
    mean = coords[train].mean(axis=0)
    sd = coords[train].std(axis=0)
    variable = sd > 1e-14
    z = (coords - mean) / np.where(variable, sd, 1.)
    z[:, ~variable] = 0.
    lat, lon = z[:, 0], z[:, 1]
    basis = np.column_stack((lat, lon, lat * lat, lat * lon, lon * lon))
    basis_mean = basis[train].mean(axis=0)
    basis_sd = basis[train].std(axis=0)
    basis_variable = basis_sd > 1e-14
    features = (basis - basis_mean) / np.where(basis_variable, basis_sd, 1.)
    features[:, ~basis_variable] = 0.
    geo_train, geo_cross, geo_scale = center_scale(
        features[train] @ features[train].T,
        features[test] @ features[train].T,
    )

    train_distance = distance[np.ix_(train, train)]
    positive = train_distance[np.triu_indices(len(train), k=1)]
    positive = positive[positive > 0]
    if not len(positive):
        raise ValueError("no positive training genetic distance for bandwidth")
    tau = float(np.median(positive))
    gen_train, gen_cross, gen_scale = center_scale(
        np.exp(-train_distance / tau),
        np.exp(-distance[np.ix_(test, train)] / tau),
    )
    psd = check_psd(gen_train)
    combined_train, combined_cross, combined_scale = center_scale(
        geo_train + gen_train, geo_cross + gen_cross,
    )
    return {"M0": (geo_train, geo_cross), "M1": (combined_train, combined_cross)}, {
        "tau": tau, "geographic_component_scale": geo_scale,
        "genetic_component_scale": gen_scale, "combined_component_scale": combined_scale,
        "genetic_kernel_psd": psd,
        "M0_mean_training_diagonal": float(np.diag(geo_train).mean()),
        "M1_mean_training_diagonal": float(np.diag(combined_train).mean()),
    }


def validate_arrays(data):
    """Validate and jointly reorder labelled source arrays by numeric ID."""
    required = {"ids", "coords", "distance", "fitness", "contexts"}
    if not required <= set(data):
        raise ValueError("prepared input lacks required arrays")
    ids = np.asarray(data["ids"]).astype(str)
    if ids.ndim != 1 or len(ids) < 5 or len(set(ids)) != len(ids):
        raise ValueError("need at least five unique accession IDs")
    if any(not re.fullmatch(r"[1-9][0-9]*", x) for x in ids):
        raise ValueError("accession IDs must be canonical positive integer strings")
    contexts = np.asarray(data["contexts"]).astype(str)
    if contexts.ndim != 1 or tuple(contexts) != CONTEXTS:
        raise ValueError("unexpected context identities or order")
    n = len(ids)
    coords = np.asarray(data["coords"], dtype=float)
    distance = np.asarray(data["distance"], dtype=float)
    fitness = np.asarray(data["fitness"], dtype=float)
    if coords.shape != (n, 2) or distance.shape != (n, n) or fitness.shape != (n, 8):
        raise ValueError("prepared source dimensions do not align")
    if not all(np.isfinite(a).all() for a in (coords, distance, fitness)):
        raise ValueError("prepared source contains missing or nonfinite values")
    if np.any(np.abs(coords[:, 0]) > 90) or np.any(np.abs(coords[:, 1]) > 180):
        raise ValueError("coordinates outside latitude/longitude ranges")
    if np.any(fitness < 0) or np.any(distance < 0):
        raise ValueError("negative fitness or genetic distance")
    if not np.allclose(distance, distance.T, rtol=0., atol=1e-12):
        raise ValueError("genetic distance matrix is not symmetric")
    if np.any(np.abs(np.diag(distance)) > 1e-12):
        raise ValueError("genetic distance diagonal must be zero")
    if np.any(distance[np.triu_indices(n, k=1)] == 0):
        raise ValueError("identical measured genotypes require a separately frozen split")
    order = np.array(sorted(range(n), key=lambda k: int(ids[k])), dtype=int)
    return {"ids": ids[order], "coords": coords[order], "fitness": fitness[order],
            "distance": distance[np.ix_(order, order)], "contexts": contexts}


def accession_folds(n, n_splits, seed):
    if not 2 <= n_splits <= n:
        raise ValueError("insufficient accessions for requested folds")
    permutation = np.random.default_rng(seed).permutation(n)
    result = []
    for held in np.array_split(permutation, n_splits):
        mask = np.ones(n, dtype=bool)
        mask[held] = False
        result.append((np.flatnonzero(mask), held))
    return result


def spatial_folds(cells, n_splits):
    groups = defaultdict(list)
    for i, cell in enumerate(cells):
        groups[tuple(map(int, cell))].append(i)
    if not 2 <= n_splits <= len(groups):
        raise ValueError("insufficient geographic cells for requested folds")
    held_sets = [[] for _ in range(n_splits)]
    for group in sorted(groups, key=lambda key: (-len(groups[key]), key)):
        fold = min(range(n_splits), key=lambda k: (len(held_sets[k]), k))
        held_sets[fold].extend(groups[group])
    result = []
    for indices in held_sets:
        held = np.array(sorted(indices), dtype=int)
        mask = np.ones(len(cells), dtype=bool)
        mask[held] = False
        result.append((np.flatnonzero(mask), held))
    return result


def geographic_cells(coords):
    return np.floor((np.asarray(coords) + np.array([90., 180.])) / 5).astype(int)


def _fingerprint_ids(ids):
    text = "\n".join(sorted(map(str, ids), key=int)) + "\n"
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def fit_outer_fold(data, train, held, mode, fold_index):
    """Return fitted predictions; held-out fitness is never accessed here."""
    train, held = np.asarray(train, dtype=int), np.asarray(held, dtype=int)
    if set(train) & set(held) or len(set(train)) != len(train) or len(set(held)) != len(held):
        raise ValueError("invalid overlapping or duplicate fold indices")
    if mode == "accession":
        inner = accession_folds(len(train), 3, SPLIT_SEED + fold_index)
    elif mode == "geographic":
        inner = spatial_folds(geographic_cells(data["coords"][train]), 3)
    else:
        raise ValueError("unknown validation mode")
    loss_sums = {name: np.zeros(len(LAMBDAS)) for name in ("M0", "M1")}
    validation_cells, inner_reports = 0, []
    for inner_train, inner_held in inner:
        training, validation = train[inner_train], train[inner_held]
        kernels, diagnostics = make_kernels(data["coords"], data["distance"], training, validation)
        for name in ("M0", "M1"):
            for j, regularization in enumerate(LAMBDAS):
                prediction, scale = fit_predict(*kernels[name], data["fitness"][training], regularization)
                error = prediction - data["fitness"][validation] / scale
                loss_sums[name][j] += float(np.sum(error * error))
        validation_cells += len(validation) * len(CONTEXTS)
        train_cells = set(map(tuple, geographic_cells(data["coords"][training])))
        held_cells = set(map(tuple, geographic_cells(data["coords"][validation])))
        inner_reports.append({
            "train_accessions": len(training), "heldout_accessions": len(validation),
            "train_ids_sha256": _fingerprint_ids(data["ids"][training]),
            "heldout_ids_sha256": _fingerprint_ids(data["ids"][validation]),
            "group_overlap": len(train_cells & held_cells),
            "kernel_diagnostics": diagnostics,
        })
    scores = {name: values / validation_cells for name, values in loss_sums.items()}
    selected = {
        name: float(max(value for value, loss in zip(LAMBDAS, values)
                        if loss <= float(np.min(values)) + 1e-12))
        for name, values in scores.items()
    }
    kernels, diagnostics = make_kernels(data["coords"], data["distance"], train, held)
    predictions = {"Mean": np.ones((len(held), len(CONTEXTS)))}
    training_means = None
    for name in ("M0", "M1"):
        predictions[name], training_means = fit_predict(
            *kernels[name], data["fitness"][train], selected[name]
        )
    return {
        "predictions": predictions, "training_means": training_means,
        "selected_lambdas": selected,
        "inner_mse": {name: {str(lam): float(score) for lam, score in zip(LAMBDAS, values)}
                      for name, values in scores.items()},
        "inner_folds": inner_reports, "kernel_diagnostics": diagnostics,
    }


def evaluate(data, mode):
    """Evaluate the frozen split mode and return aggregates, never source rows."""
    data = validate_arrays(data)
    n = len(data["ids"])
    cells = geographic_cells(data["coords"])
    if mode == "accession":
        outer = accession_folds(n, 5, SPLIT_SEED)
    elif mode == "geographic":
        outer = spatial_folds(cells, 5)
    else:
        raise ValueError("unknown validation mode")
    losses = {name: np.full((n, len(CONTEXTS)), np.nan) for name in MODELS}
    assignment = np.full(n, -1, dtype=int)
    fold_reports = []
    for k, (train, held) in enumerate(outer, 1):
        fitted = fit_outer_fold(data, train, held, mode, k)
        target = data["fitness"][held] / fitted["training_means"]
        for name in MODELS:
            losses[name][held] = (fitted["predictions"][name] - target) ** 2
        assignment[held] = k
        train_groups, held_groups = set(map(tuple, cells[train])), set(map(tuple, cells[held]))
        fold_reports.append({
            "fold": k, "train_accessions": len(train), "heldout_accessions": len(held),
            "train_geographic_cells": len(train_groups), "heldout_geographic_cells": len(held_groups),
            "geographic_cell_overlap": len(train_groups & held_groups),
            "train_ids_sha256": _fingerprint_ids(data["ids"][train]),
            "heldout_ids_sha256": _fingerprint_ids(data["ids"][held]),
            "training_context_means": {c: float(v) for c, v in zip(CONTEXTS, fitted["training_means"])},
            "selected_lambdas": fitted["selected_lambdas"],
            "inner_mse": fitted["inner_mse"], "inner_folds": fitted["inner_folds"],
            "kernel_diagnostics": fitted["kernel_diagnostics"],
            "model_mse": {name: float(losses[name][held].mean()) for name in MODELS},
            "M1_gain_over_M0": float((losses["M0"][held] - losses["M1"][held]).mean()),
        })
    if np.any(assignment < 0) or not all(np.isfinite(v).all() for v in losses.values()):
        raise ValueError("validation did not score every accession/context")
    models = {
        name: {"mse": float(values.mean()),
               "context_mse": {c: float(values[:, j].mean()) for j, c in enumerate(CONTEXTS)},
               "site_mse": {"Madrid": float(values[:, :4].mean()),
                            "Tuebingen": float(values[:, 4:].mean())}}
        for name, values in losses.items()
    }
    gain = losses["M0"] - losses["M1"]
    interval = conditional_interval(gain.mean(axis=1), cells if mode == "geographic" else None)
    context_gain = {c: float(gain[:, j].mean()) for j, c in enumerate(CONTEXTS)}
    site_gain = {"Madrid": float(gain[:, :4].mean()), "Tuebingen": float(gain[:, 4:].mean())}
    conditions = {
        "mean_gain_positive": bool(gain.mean() > 0),
        "conditional_interval_lower_positive": bool(interval["ci95"][0] > 0),
        "all_five_outer_folds_positive": all(x["M1_gain_over_M0"] > 0 for x in fold_reports),
        "both_sites_positive": all(v > 0 for v in site_gain.values()),
        "M1_beats_mean_predictor": models["M1"]["mse"] < models["Mean"]["mse"],
    }
    assignment_text = "\n".join(f"{identity}:{fold}" for identity, fold in zip(data["ids"], assignment)) + "\n"
    return {
        "split": mode, "accessions": n, "response_cells": n * len(CONTEXTS),
        "geographic_cells": len(set(map(tuple, cells))),
        "cohort_ids_sha256": _fingerprint_ids(data["ids"]),
        "fold_assignment_sha256": hashlib.sha256(assignment_text.encode()).hexdigest(),
        "models": models, "folds": fold_reports,
        "contrast": {"definition": "M0 MSE minus M1 MSE; positive favors M1",
                     "mean_gain": float(gain.mean()), "context_gains": context_gain,
                     "site_gains": site_gain, "conditional_ci95": interval["ci95"],
                     "conditional_bootstrap": interval,
                     "M1_gain_over_mean_predictor": models["Mean"]["mse"] - models["M1"]["mse"]},
        "numerical_gate": {"role": "primary" if mode == "accession" else "sensitivity_only",
                           "conditions": conditions, "passed": all(conditions.values())},
    }


def conditional_interval(gain, groups=None):
    """Paired resampling holds predictions fixed; clusters retain all members."""
    gain = np.asarray(gain, dtype=float)
    if gain.ndim != 1 or not len(gain) or not np.isfinite(gain).all():
        raise ValueError("invalid per-accession gain for resampling")
    rng = np.random.default_rng(BOOTSTRAP_SEED)
    if groups is None:
        indices = rng.integers(0, len(gain), size=(BOOTSTRAP_DRAWS, len(gain)))
        draws = gain[indices].mean(axis=1)
        units, unit_name = len(gain), "accessions"
    else:
        groups = np.asarray(groups)
        if len(groups) != len(gain):
            raise ValueError("bootstrap groups do not align with gains")
        _, inverse = np.unique(groups, axis=0, return_inverse=True)
        sizes = np.bincount(inverse)
        sums = np.bincount(inverse, weights=gain)
        indices = rng.integers(0, len(sizes), size=(BOOTSTRAP_DRAWS, len(sizes)))
        draws = sums[indices].sum(axis=1) / sizes[indices].sum(axis=1)
        units, unit_name = len(sizes), "five_degree_geographic_cells"
    return {"point_estimate": float(gain.mean()),
            "ci95": np.quantile(draws, [.025, .975], method="linear").tolist(),
            "draws": BOOTSTRAP_DRAWS, "seed": BOOTSTRAP_SEED,
            "resampling_units": units, "unit": unit_name,
            "conditioning": "fixed predictions, tuning, source summaries and preprocessing"}


def verify_source_binding(path, audit):
    expected = audit.get("prepared_npz_sha256")
    if not isinstance(expected, str) or not re.fullmatch(r"[a-f0-9]{64}", expected):
        raise ValueError("source audit lacks the prepared NPZ SHA256 binding")
    actual = hashlib.sha256(Path(path).read_bytes()).hexdigest()
    if actual != expected:
        raise ValueError("prepared NPZ differs from the source-audited bytes")
    return actual


def analyse(prepared, source_audit, protocol):
    """Run a prepared, byte-bound cohort without loading any unlabelled inputs."""
    prepared, source_audit, protocol = map(Path, (prepared, source_audit, protocol))
    audit_bytes = source_audit.read_bytes()
    audit = json.loads(audit_bytes)
    prepared_digest = verify_source_binding(prepared, audit)
    with np.load(prepared, allow_pickle=False) as archive:
        data = validate_arrays({name: archive[name] for name in archive.files})
    expected_counts = {"n_accessions": len(data["ids"]), "n_contexts": len(CONTEXTS),
                       "n_response_cells": len(data["ids"]) * len(CONTEXTS)}
    if any(audit.get(key) != value for key, value in expected_counts.items()):
        raise ValueError("prepared cohort counts disagree with source audit")
    if not isinstance(audit.get("source_files"), list) or not audit["source_files"]:
        raise ValueError("source audit lacks original source-file hashes")
    return {
        "study_doi": "10.1038/s41586-019-1520-9",
        "estimand": "conditional prediction of published accession-context fitness summaries",
        "target": "final D4 Fitness divided by each fit's training-context arithmetic mean",
        "provenance": {
            "prepared_npz_sha256": prepared_digest,
            "source_audit_sha256": hashlib.sha256(audit_bytes).hexdigest(),
            "protocol_sha256": hashlib.sha256(protocol.read_bytes()).hexdigest(),
            "analysis_script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "source_files": audit["source_files"],
        },
        "runtime": {"python": platform.python_version(), "numpy": np.__version__},
        "settings": {"outer_folds": 5, "inner_folds": 3, "lambdas": list(LAMBDAS),
                     "primary_split_seed": SPLIT_SEED, "bootstrap_seed": BOOTSTRAP_SEED,
                     "bootstrap_draws": BOOTSTRAP_DRAWS, "contexts": list(CONTEXTS),
                     "inner_loss_weighting": "equal validation accession by context, pooled across folds",
                     "bootstrap_quantile_method": "linear"},
        "primary": evaluate(data, "accession"),
        "geographic_sensitivity": evaluate(data, "geographic"),
        "interpretation_limits": [
            "Conditional on upstream measurement, calibration and published aggregation.",
            "Accession holdout does not establish transfer to new biological populations or environments.",
            "Genetic gain is relative to the specified quadratic-coordinate predictor.",
            "Bootstrap intervals hold fits and targets fixed and do not include refitting uncertainty.",
            "No treatment-policy value, causal-variant inference or exact MLTR theorem validation.",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prepared", required=True, type=Path)
    parser.add_argument("--source-audit", required=True, type=Path)
    parser.add_argument("--protocol", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    try:
        report = analyse(args.prepared, args.source_audit, args.protocol)
        encoded = json.dumps(report, indent=2, allow_nan=False) + "\n"
    except (ValueError, OSError, KeyError, np.linalg.LinAlgError) as error:
        parser.error(str(error))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(encoded, encoding="utf-8")
    print(json.dumps({"output": str(args.output),
                      "primary_gate_passed": report["primary"]["numerical_gate"]["passed"],
                      "primary_mean_gain": report["primary"]["contrast"]["mean_gain"]}))


if __name__ == "__main__":
    main()
