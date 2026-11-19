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
import io
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold

HAPS = ("hb7a1", "hb7a2", "hb7b", "hb9", "hb13")
ORIGINAL_ZIP_SHA256 = "dc8fa8378176a063db4367e2fc4dd75914758a7246010e67b7ff7957e5632eb8"
ORIGINAL_CSV_SHA256 = "cbd9691e4b07a48e97619385bedc9f9a45fb02164d4ce08c1a99c9af7df054d4"
ORIGINAL_README_SHA256 = "72b966bbd7326a36cac14294c91dc15f3e4878e6ff7ae4c4289a3da531a83131"
ORIGINAL_CSV = "DatasetA_commongarden.csv"
REQUIRED = ("Garden", "File", "Population", "Latitude", "Longitude", "FloweredFull") + HAPS
MISSING = {"", "NA", "NaN", "nan", "N/A", "999", "999.0"}
DOI = "10.5061/dryad.dfn2z3593"


def source_data(path: Path, is_zip: bool = False) -> tuple[bytes, dict]:
    """Read exact original user-supplied Dryad ZIP, or a local CSV test input."""
    if not is_zip:
        raw = path.read_bytes()
        return raw, {
            "mode": "local_csv", "csv_sha256": hashlib.sha256(raw).hexdigest(),
            "exact_v20250829_csv": hashlib.sha256(raw).hexdigest() == ORIGINAL_CSV_SHA256,
        }
    zip_bytes = path.read_bytes()
    if len(zip_bytes) > 2_000_000 or hashlib.sha256(zip_bytes).hexdigest() != ORIGINAL_ZIP_SHA256:
        raise ValueError("original Dryad v20250829 ZIP hash mismatch")
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as archive:
        if sorted(archive.namelist()) != [ORIGINAL_CSV, "README.md"]:
            raise ValueError("original Dryad ZIP manifest mismatch")
        raw = archive.read(ORIGINAL_CSV)
        readme = archive.read("README.md")
    if hashlib.sha256(raw).hexdigest() != ORIGINAL_CSV_SHA256:
        raise ValueError("original common garden CSV hash mismatch")
    if hashlib.sha256(readme).hexdigest() != ORIGINAL_README_SHA256:
        raise ValueError("original common garden README hash mismatch")
    return raw, {
        "mode": "verified_original_zip", "zip_sha256": ORIGINAL_ZIP_SHA256,
        "csv_sha256": ORIGINAL_CSV_SHA256, "readme_sha256": ORIGINAL_README_SHA256,
        "version": "v20250829", "exact_v20250829_csv": True,
    }


def read_source(path_or_bytes: Path | bytes):
    raw = path_or_bytes.read_bytes() if isinstance(path_or_bytes, Path) else path_or_bytes
    with io.StringIO(raw.decode("utf-8-sig")) as handle:
        reader = csv.DictReader(handle)
        fields = set(reader.fieldnames or [])
        if not set(REQUIRED) <= fields:
            raise ValueError(f"missing columns: {sorted(set(REQUIRED)-fields)}")
        raw_rows = list(reader)
    if not raw_rows:
        raise ValueError("no source rows")
    # A real source .bam ID occurs twice with DIFFERENT hb9/hb13 genotypes
    # but identical metadata and fitness fields. Neither row is selectable
    # without a corrected specimen crosswalk; exclude BOTH before outcome fit.
    ids = Counter(str(row.get("File", "")).strip() for row in raw_rows)
    duplicated = {key for key, count in ids.items() if key and count > 1}
    conflict_fields = set()
    for key in duplicated:
        matches = [row for row in raw_rows if row.get("File", "").strip() == key]
        conflict_fields.update(
            field for field in (REQUIRED + ("Continent", "Rep", "Survived1st", "SeedSetMassFull"))
            if any(row.get(field) != matches[0].get(field) for row in matches)
        )
    selected, reasons, all_pops = [], {}, set()
    for line_no, row in enumerate(raw_rows, 2):
        sample_id = (row["File"] or "").strip()
        population = (row["Population"] or "").strip()
        garden = (row["Garden"] or "").strip()
        if not sample_id or not population or not garden:
            reasons["missing_identifier"] = reasons.get("missing_identifier", 0) + 1
            continue
        all_pops.add(population)
        if sample_id in duplicated:
            reasons["conflicting_or_reused_bam_id_rows"] = reasons.get(
                "conflicting_or_reused_bam_id_rows", 0
            ) + 1
            continue

        def number(name):
            val = str(row[name] or "").strip()
            return None if val in MISSING else float(val)

        try:
            numbers = [number(k) for k in ("Latitude", "Longitude") + HAPS + ("FloweredFull",)]
        except ValueError as error:
            raise ValueError(f"non-numeric source field at line {line_no}") from error
        if any(x is None for x in numbers):
            reasons["missing_complete_case_field"] = reasons.get(
                "missing_complete_case_field", 0
            ) + 1
            continue
        lat, lon, *other = numbers
        five, outcome = other[:-1], other[-1]
        if not (-90 <= lat <= 90 and -180 <= lon <= 180):
            raise ValueError("invalid coordinates")
        if any(h not in (0.0, 0.5, 1.0) for h in five):
            raise ValueError("haploblock dosage must be 0/0.5/1")
        if outcome not in (0.0, 1.0):
            raise ValueError("FloweredFull must be coded 0/1")
        selected.append({
            "garden":garden, "population":population,
            "lat":lat, "lon":lon, "haps":five, "y":int(outcome)
        })
    populations = {row["population"] for row in selected}
    gardens = sorted({row["garden"] for row in selected})
    if len(selected) < 100 or len(populations) < 10 or len(gardens) != 4:
        raise ValueError("source admission: >=100 complete, >=10 origin populations, exactly four gardens")
    return selected, {
        "raw_rows":len(raw_rows),
        "complete_case_rows":len(selected),
        "raw_origin_populations":len(all_pops),
        "complete_origin_populations":len(populations),
        "gardens":{g:sum(row["garden"] == g for row in selected) for g in gardens},
        "exclusion_counts":reasons,
        "reused_bam_identifiers":len(duplicated),
        "reused_identifier_conflict_columns":sorted(conflict_fields),
        "source_field_case":list(HAPS),
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


def analyse(path:Path, is_zip: bool = False):
    source_bytes, provenance = source_data(path, is_zip=is_zip)
    records,quality = read_source(source_bytes)
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
        "source":{"doi":DOI, "file":ORIGINAL_CSV, **provenance},
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
            "Two conflicting rows with one .bam ID are both excluded, never arbitrarily chosen",
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
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--input",type=Path,help="original CSV or synthetic test input")
    source.add_argument("--zip",type=Path,help="exact original Dryad v20250829 ZIP")
    parser.add_argument("--out",type=Path,required=True)
    args=parser.parse_args()
    result=analyse(args.zip if args.zip else args.input, is_zip=bool(args.zip))
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print("PREDICTION_ONLY", result["source_quality"])
    print("Saved",args.out)


if __name__=="__main__":
    main()
