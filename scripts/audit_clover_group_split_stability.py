#!/usr/bin/env python3
"""Exploratory group-split stability of the frozen white-clover M0/M1 models.

Original source: Battlay et al. Dryad 10.5061/dryad.dfn2z3593 v20250829.
Only original ZIP, hash/QC validated by the already merged reader. No raw
specimen genotypes or IDs are saved. Split quantiles are NOT confidence intervals.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold, GroupShuffleSplit

from analyze_clover_haploblock_fitness import source_data, read_source, features


def heldout_contrast(records, train, held):
    gardens = sorted({r["garden"] for r in records})
    origin = np.array([r["population"] for r in records])
    y = np.array([r["y"] for r in records], dtype=int)
    if set(origin[train]) & set(origin[held]):
        raise ValueError("same origin population in training and test")
    if len(set(y[train])) != 2:
        raise ValueError("only one response class in train")
    if {records[i]["garden"] for i in held} - {records[i]["garden"] for i in train}:
        raise ValueError("held-out garden was absent in training")
    ll = []
    for model in ("M0", "M1"):
        x = features(records, gardens, train, model)
        fit = LogisticRegression(
            C=1.0, solver="lbfgs", max_iter=2000, random_state=20261119
        ).fit(x[train], y[train])
        probability = np.clip(fit.predict_proba(x[held])[:, 1], 1e-12, 1-1e-12)
        ll.append(y[held]*np.log(probability) +
                  (1-y[held])*np.log1p(-probability))
    difference = ll[1] - ll[0]
    groups = origin[held]
    pop_scores = [difference[groups == g].mean() for g in set(groups)]
    pos_gardens = sum(
        difference[np.array([records[i]["garden"] == g for i in held])].mean() > 0
        for g in {records[i]["garden"] for i in held}
    )
    return {
        "heldout_n": len(held),
        "heldout_origin_populations": len(set(groups)),
        "mean_gain_nats": float(difference.mean()),
        "origin_equal_gain_nats": float(np.mean(pop_scores)),
        "n_positive_gardens": int(pos_gardens),
    }


def summary(values):
    v = np.array(values, dtype=float)
    return {key: round(float(val), 8) for key, val in {
        "mean": v.mean(), "median": np.median(v),
        "q025": np.quantile(v, .025), "q975": np.quantile(v, .975),
        "min": v.min(), "max": v.max(),
    }.items()}


def evaluate_split_stability(records, n_repeats=100, seed=20261119):
    if not 1 <= n_repeats <= 500:
        raise ValueError("split repetitions outside bounded range 1..500")
    origin = np.array([r["population"] for r in records])
    y = np.array([r["y"] for r in records], dtype=int)
    a = np.zeros(len(records))
    fixed = [
        heldout_contrast(records, train, test)
        for train, test in GroupKFold(n_splits=5).split(a, y, origin)
    ]
    fixed_mean = sum(row["mean_gain_nats"]*row["heldout_n"] for row in fixed)/len(records)
    random_splits = [
        heldout_contrast(records, train, test)
        for train, test in GroupShuffleSplit(
            n_splits=n_repeats, test_size=.2, random_state=seed
        ).split(a, y, origin)
    ]
    gains = [row["mean_gain_nats"] for row in random_splits]
    pop_gains = [row["origin_equal_gain_nats"] for row in random_splits]
    return {
        "reference_fixed_5fold": {
            "weighted_M1_minus_M0_nats_per_plant": round(fixed_mean, 8),
            "per_fold_gain_nats": [round(row["mean_gain_nats"], 8) for row in fixed],
        },
        "repeated_group_shuffle_80_20": {
            "repeats": n_repeats, "random_seed": seed,
            "mean_heldout_individuals": round(float(np.mean([
                row["heldout_n"] for row in random_splits
            ])), 2),
            "mean_heldout_origin_populations": round(float(np.mean([
                row["heldout_origin_populations"] for row in random_splits
            ])), 2),
            "individual_mean_gain_distribution": summary(gains),
            "origin_equal_gain_distribution": summary(pop_gains),
            "negative_repeats": sum(v < 0 for v in gains),
            "positive_repeats": sum(v > 0 for v in gains),
            "repeats_with_at_least_three_positive_gardens": sum(
                row["n_positive_gardens"] >= 3 for row in random_splits
            ),
        },
    }


def analyse(archive: Path, repeats=100):
    raw, provenance = source_data(archive, is_zip=True)
    records, quality = read_source(raw)
    if len(records) != 470 or quality["complete_origin_populations"] != 93:
        raise ValueError("source QC 470 records/93 origin populations changed")
    return {
        "source": {"doi": "10.5061/dryad.dfn2z3593", **provenance},
        "source_qc": {
            "raw_rows": quality["raw_rows"],
            "primary_n": len(records),
            "origin_populations": quality["complete_origin_populations"],
            "gardens": quality["gardens"],
            "excluded_conflicting_BAM_rows": quality["exclusion_counts"].get(
                "conflicting_or_reused_bam_id_rows", 0
            ),
        },
        "status": "EXPLORATORY_SPLIT_SENSITIVITY_NOT_A_NEW_MLTR_OR_FITNESS_HYPOTHESIS",
        "model_specification": "Frozen M0/M1, 5 haploblocks, L2 logistic C=1, train-only geographic scaling",
        **evaluate_split_stability(records, repeats),
        "limitations": [
            "Overlapping held-out splits are not independent biological experiments.",
            "Split quantiles are NOT confidence intervals and negative fraction is not a P value.",
            "The original fixed 5-fold negative test remains primary; repeated splits are post-result sensitivity.",
            "Fitness-genotype causation, new-garden transfer and exact MLTR semantics remain untested.",
        ],
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--zip", required=True, type=Path)
    p.add_argument("--out", required=True, type=Path)
    p.add_argument("--repeats", type=int, default=100)
    args = p.parse_args()
    report = analyse(args.zip, repeats=args.repeats)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n",
                        encoding="utf-8")
    print(report["reference_fixed_5fold"])
    print(report["repeated_group_shuffle_80_20"])


if __name__ == "__main__":
    main()
