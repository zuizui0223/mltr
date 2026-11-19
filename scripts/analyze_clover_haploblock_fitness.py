#!/usr/bin/env python3
"""Prediction-only transfer audit on published white-clover common-garden genotypes.

Original source: Battlay et al. (2025), Dryad 10.5061/dryad.dfn2z3593,
DatasetA_commongarden.csv. Genotype-haploblock associations with fitness are
already published prior art. This tests out-of-ORIGIN-population predictive
increment, not genotype causation, exact MLTR state transport or adaptation.
No raw individual records are written into the output.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold

HAPS = ("Hb7a1", "Hb7a2", "Hb7b", "Hb9", "Hb13")
REQUIRED = ("Garden", "File", "Population", "Latitude", "Longitude", "FloweredFull") + HAPS
MISSING = {"", "NA", "NaN", "nan", "N/A", "999", "999.0"}
DOI = "10.5061/dryad.dfn2z3593"


def read_source(path: Path):
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        fields = set(reader.fieldnames or [])
        if not set(REQUIRED) <= fields:
            raise ValueError(f"missing columns: {sorted(set(REQUIRED)-fields)}")
        raw_rows = list(reader)
    if not raw_rows:
        raise ValueError("no source rows")
    selected, reasons, seen, all_pops = [], {}, set(), set()
    for line_no, row in enumerate(raw_rows, 2):
        sample_id = row["File"].strip()
        population = row["Population"].strip()
        garden = row["Garden"].strip()
        if not sample_id or not population or not garden:
            reasons["missing_identifier"] = reasons.get("missing_identifier", 0) + 1
            continue
        if sample_id in seen:
            raise ValueError("duplicate .bam individual identifier")
        seen.add(sample_id)
        all_pops.add(population)

        def number(name):
            value = row[name].strip()
            return None if value in MISSING else float(value)

        try:
            numbers = [number(k) for k in ("Latitude", "Longitude") + HAPS + ("FloweredFull",)]
        except ValueError as error:
            raise ValueError(f"non-numeric field at row {line_no}") from error
        if any(x is None for x in numbers):
            reasons["missing_complete_case_field"] = reasons.get("missing_complete_case_field", 0) + 1
            continue
        lat, lon, *other = numbers
        five, outcome = other[:-1], other[-1]
        if not (-90 <= lat <= 90 and -180 <= lon <= 180):
            raise ValueError("invalid source coordinates")
        if any(h not in (0.0, 0.5, 1.0) for h in five):
            raise ValueError("haploblock dosage not coded 0/0.5/1")
        if outcome not in (0.0, 1.0):
            raise ValueError("survival-to-flowering must be binary 0/1")
        selected.append({
            "garden": garden,
            "population": population,
            "lat": lat, "lon": lon,
            "haps": five, "y": int(outcome)
        })
    populations = {row["population"] for row in selected}
    gardens = sorted({row["garden"] for row in selected})
    if len(selected) < 100 or len(populations) < 10 or len(gardens) != 4:
        raise ValueError("source eligibility failed: require >=100 complete, >=10 origin populations, four gardens")
    garden_counts = {g:sum(row["garden"] == g for row in selected) for g in gardens}
    return selected, {
        "raw_rows": len(raw_rows),
        "complete_case_rows": len(selected),
        "raw_origin_populations": len(all_pops),
        "complete_origin_populations": len(populations),
        "gardens": garden_counts,
        "exclusion_counts": reasons
    }


def features(records, garden_levels, training, model):
    coords = np.array([[r["lat"], r["lon"]] for r in records], dtype=float)
    mean = coords[training].mean(axis=0)
    sd = coords[training].std(axis=0)
    sd[sd < 1e-8] = 1.0
    geo = (coords - mean) / sd
    garden = np.array([[float(r["garden"] == name) for name in garden_levels]
                       for r in records])
    x = np.column_stack((garden, geo))
    markers = np.array([r["haps"] for r in records])
    if model in ("M1", "M2"):
        x = np.column_stack((x, markers))
    if model == "M2":
        x = np.column_stack((x, *(garden[:, j:j+1] * markers
                                    for j in range(len(garden_levels)))))
    return x


def evaluate(records):
    gardens = sorted({r["garden"] for r in records})
    origin = np.array([r["population"] for r in records])
    outcome = np.array([r["y"] for r in records], dtype=int)
    pred = {m: np.full(len(records), np.nan) for m in ("M0", "M1", "M2")}
    folds = []
    for k, (train, held) in enumerate(
        GroupKFold(n_splits=5).split(np.zeros(len(outcome)), outcome, origin), start=1
    ):
        if set(origin[train]) & set(origin[held]):
            raise ValueError("population leakage detected")
        if len(set(outcome[train])) != 2:
            raise ValueError("only one response class in training fold")
        if set(r["garden"] for i, r in enumerate(records) if i in held) - set(
            r["garden"] for i, r in enumerate(records) if i in train
        ):
            raise ValueError("unseen garden in heldout population fold")
        for model in pred:
            x = features(records, gardens, train, model)
            reg = LogisticRegression(C=1.0, solver="lbfgs", max_iter=2000,
                                     random_state=20261119)
            reg.fit(x[train], outcome[train])
            pred[model][held] = reg.predict_proba(x[held])[:, 1]
        folds.append({
            "fold":k, "train_individuals":len(train), "heldout_individuals":len(held),
            "train_origin_populations":len(set(origin[train])),
            "heldout_origin_populations":len(set(origin[held]))
        })
    if any(not np.isfinite(v).all() for v in pred.values()):
        raise ValueError("unscored held-out individuals")
    eps = 1e-12
    ll = {
        m:outcome * np.log(np.clip(probs, eps, 1-eps))
          + (1-outcome) * np.log1p(-np.clip(probs, eps, 1-eps))
        for m, probs in pred.items()
    }
    model_scores = {
        m: {
            "out_of_origin_population_log_loss":round(float(-ll[m].mean()), 7),
            "out_of_origin_population_brier":round(float(np.mean((pred[m]-outcome)**2)), 7)
        } for m in pred
    }
    rng = np.random.default_rng(20261119)
    contrasts = {}
    for model in ("M1", "M2"):
        gain = ll[model] - ll["M0"]
        pop_gain = np.array([gain[origin == p].mean() for p in np.unique(origin)])
        # Conditional population resampling of already held-out predictions.
        resampled = pop_gain[rng.integers(
            0, len(pop_gain), size=(2000,len(pop_gain))
        )].mean(axis=1)
        ci = np.quantile(resampled,[.025,.975])
        garden_deltas = {
            g:round(float(np.mean(gain[np.array([r["garden"] == g for r in records])])),7)
            for g in gardens
        }
        contrasts[f"{model}_minus_M0"] = {
            "individual_mean_gain_nats":round(float(gain.mean()),7),
            "population_equal_weight_gain_nats":round(float(pop_gain.mean()),7),
            "conditional_population_bootstrap_ci_95":list(map(
                lambda z:round(float(z),7),ci
            )),
            "origin_populations_with_positive_gain":int(sum(pop_gain>0)),
            "origin_populations_total":len(pop_gain),
            "garden_mean_gains":garden_deltas,
            "role":"PRIMARY" if model == "M1" else "EXPLORATORY_INTERACTION"
        }
    return model_scores, contrasts, folds


def analyse(path:Path):
    records,quality = read_source(path)
    scores,contrasts,folds = evaluate(records)
    primary = contrasts["M1_minus_M0"]
    eligible = all(n >= 10 for n in quality["gardens"].values())
    primary_pass = (
        eligible
        and primary["population_equal_weight_gain_nats"] > 0
        and primary["conditional_population_bootstrap_ci_95"][0] > 0
        and sum(value > 0 for value in primary["garden_mean_gains"].values()) >= 3
    )
    verdict = (
        "EXPLORATORY_PREDICTIVE_INCREMENT_SUPPORTED_IN_OBSERVED_GARDENS"
        if primary_pass else "PRIMARY_PREDICTIVE_INCREMENT_NOT_SUPPORTED_OR_UNEVALUABLE"
    )
    return {
        "source":{"doi":DOI, "file":path.name, "sha256":hashlib.sha256(path.read_bytes()).hexdigest()},
        "status":"OUT_OF_POPULATION_GENOTYPE_FITNESS_PREDICTION_NOT_CAUSAL_MLTR",
        "primary_evaluation_gate": {
            "status": verdict,
            "min_complete_case_each_garden": 10,
            "require_positive_equal_population_mean": True,
            "require_population_bootstrap_95ci_lower_above_zero": True,
            "require_positive_garden_mean_count_at_least": 3,
            "scope": "exploratory out-of-origin-population prediction in four existing gardens; not adaptation causality"
        },
        "primary_outcome":"FloweredFull (survival to flowering)",
        "M0":"garden + source latitude/longitude",
        "M1":"M0 + five haploblock genotypes",
        "M2":"M1 + haploblock by garden interaction (exploratory)",
        "crossvalidation":"5-fold GroupKFold by population; train-only standardization; L2 logistic C=1",
        "source_quality":quality,
        "folds":folds, "models":scores, "contrasts":contrasts,
        "scientific_limits":[
            "Original paper already established haploblock-by-garden associations",
            "Complete-case sample may be selection biased; compare excluded fractions by garden",
            "Source origin, ancestry and genotype are correlated; predictive increment is not causality",
            "Garden exposure is not genetic manipulation or a universally legal management action",
            "Not tested outside these four gardens and not a full-genome effect",
            "Population bootstrap is conditional on out-of-fold fitted predictions",
            "MLTR total replacement relation, path-label coherence and exact state law untested"
        ]
    }


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input",type=Path,required=True)
    parser.add_argument("--out",type=Path,required=True)
    args=parser.parse_args()
    result=analyse(args.input)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print("PREDICTION_ONLY", result["source_quality"])
    print("Saved",args.out)


if __name__=="__main__":
    main()
