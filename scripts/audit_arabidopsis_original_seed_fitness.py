#!/usr/bin/env python3
"""Original Dryad drought experiment: estimated lifetime seeds, not directly counted seeds.

Two exact user-uploaded files; no raw genotype/fruit/seed-calibration rows
emitted or committed. The seed-per-fruit multiplier is GENOTYPE x WATER, not
a microbial action effect, and was estimated in the same biological experiment.
All conditional held-out scores consequently share in-study calibration.
This is not a genomics or an exact finite MLTR theorem validation.

Frozen before seed-output response testing:
docs/arabidopsis_original_seed_production_protocol_2026-11-20.md
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
from collections import Counter
from pathlib import Path

from audit_arabidopsis_original_dryad_38 import read_original, SOURCE_SHA256
from audit_arabidopsis_factorial_response import score_folds
from audit_arabidopsis_action_decision_value import evaluate_policy

SEED_SOURCE_SHA256 = "e85b41b6da29d8d505e01d0d3213d7a38f7a2e62fdb78071c70bbf6a8d31351d"
SEED_SOURCE_BYTES = 519
SEED_COLUMNS = ("genotype", "Seed wet", "Seed dry")


def parse_seed_calibration(raw: bytes, strict: bool = True):
    digest = hashlib.sha256(raw).hexdigest()
    if strict and (len(raw) != SEED_SOURCE_BYTES or digest != SEED_SOURCE_SHA256):
        raise ValueError("original Dryad seed.count.drought.csv hash/size mismatch")
    with io.StringIO(raw.decode("utf-8-sig"), newline="") as stream:
        reader = csv.DictReader(stream)
        if tuple(reader.fieldnames or ()) != SEED_COLUMNS:
            raise ValueError("unexpected seed calibration source columns")
        original = list(reader)
    calib = {}
    for row in original:
        identifier = row["genotype"].strip()
        if not identifier or identifier in calib:
            raise ValueError("missing or duplicated genotype in seed calibration")
        pair = {}
        for water, column in (("W", "Seed wet"), ("D", "Seed dry")):
            value = row[column].strip()
            if value in ("", "NA"):
                pair[water] = None
                continue
            try:
                numeric = float(value)
            except ValueError as exc:
                raise ValueError("non-numeric seed/fruit mean") from exc
            if not math.isfinite(numeric) or numeric <= 0:
                raise ValueError("invalid seed-per-fruit mean")
            pair[water] = numeric
        calib[identifier] = pair
    if strict and (len(calib) != 38
                   or sum(v["W"] is not None for v in calib.values()) != 33
                   or sum(v["D"] is not None for v in calib.values()) != 35
                   or sum(all(value is not None for value in v.values())
                          for v in calib.values()) != 33):
        raise ValueError("seed source completeness contract changed")
    return calib, {
        "filename": "seed.count.drought.csv",
        "sha256": digest, "bytes": len(raw), "n_genotypes": len(calib),
        "wet_observed": sum(v["W"] is not None for v in calib.values()),
        "drought_observed": sum(v["D"] is not None for v in calib.values()),
        "both_observed": sum(all(x is not None for x in v.values())
                             for v in calib.values()),
        "both_missing": sum(all(x is None for x in v.values())
                            for v in calib.values()),
        "seed_units": "genotype x watering mean seeds per fruit (not plant-specific)",
    }


def eligible_joint_rows(original_rows: list[dict], calibrations: dict,
                        strict: bool = True):
    original_ids = {row["accession"].strip() for row in original_rows}
    if original_ids != set(calibrations):
        raise ValueError("original fruit and seed genotype ID sets disagree")
    complete_ids = {
        name for name, values in calibrations.items()
        if values["W"] is not None and values["D"] is not None
    }
    retained, excluded = [], []
    selected_fruit_missing = 0
    total_zero = Counter()
    for row in original_rows:
        genotype = row["accession"].strip()
        water = row["water"].strip()
        action = water + "|" + row["microbe"].strip()
        rack = row["rack"].strip()
        if water not in ("W", "D") or action not in ("W|L","W|S","D|L","D|S"):
            raise ValueError("unexpected original experimental action")
        token = row["fruit"].strip()
        if genotype not in complete_ids:
            excluded.append(row)
            if token == "0":
                total_zero["excluded_incomplete_seed_genotype"] += 1
            continue
        if token in ("","NA"):
            selected_fruit_missing += 1
            continue
        fruit = float(token)
        if not math.isfinite(fruit) or fruit < 0 or fruit != int(fruit):
            raise ValueError("invalid original fruit count")
        if fruit == 0:
            total_zero["retained_both_seed_water_conditions"] += 1
        multiplier = calibrations[genotype][water]
        if multiplier is None:
            raise ValueError("unavailable seed multiplier in complete cohort")
        seed_output = fruit * multiplier
        retained.append({
            "accession": genotype, "replicate": rack, "action": action,
            "fruit": int(fruit),
            "estimated_seed_count": seed_output,
            "value": seed_output,
        })
    if strict and (len(complete_ids)!=33 or len(retained)!=659
                   or len(excluded)!=100 or selected_fruit_missing!=1
                   or total_zero["excluded_incomplete_seed_genotype"]!=64
                   or total_zero["retained_both_seed_water_conditions"]!=52):
        raise ValueError("complete-case cohort / zero-outcome composition changed")
    counts = Counter((r["accession"],r["action"],r["replicate"]) for r in retained)
    if any(value != 1 for value in counts.values()):
        raise ValueError("duplicate genotype×treatment×rack cell")
    if set(row["accession"] for row in retained) != complete_ids:
        raise ValueError("complete genotype source missing after joint filtering")
    return retained, {
        "n_accessions_original": len(original_ids),
        "n_complete_seed_accessions": len(complete_ids),
        "n_dropped_seed_incomplete_accessions":len(original_ids-complete_ids),
        "n_design_rows_complete_accessions":len(retained)+selected_fruit_missing,
        "n_joint_observed":len(retained),
        "n_original_fruit_missing_in_complete_cohort":selected_fruit_missing,
        "n_dropped_design_rows_from_incomplete_seed_accessions":len(excluded),
        "zero_fruit_in_complete_accessions":total_zero["retained_both_seed_water_conditions"],
        "zero_fruit_in_excluded_accessions":total_zero["excluded_incomplete_seed_genotype"],
        "selection_caveat":"incomplete seed-factor groups have high zero-fruit prevalence",
        "n_potential_four_action_panels":len(complete_ids)*5,
        "n_missing_joint_action_records":selected_fruit_missing,
    }


def score_on_outcome(rows: list[dict], field: str, transform: str,
                     centered: bool, bootstrap: int):
    vals = []
    for r in rows:
        v = float(r[field])
        vals.append({
            "accession":r["accession"], "action":r["action"],
            "replicate":r["replicate"], "fruit":r["fruit"],
            "value": math.sqrt(v) if transform=="sqrt" else v,
        })
    result = score_folds(vals,10.0,10.0,bootstrap=bootstrap,
                         center_action=centered)
    result["model_specification"]["outcome"] = (
        ("sqrt_" if transform=="sqrt" else "raw_") + field
    )
    result["scientific_scope"] = (
        "fixed seed calibration derived within source experiment"
        if field=="estimated_seed_count" else
        "fruit-only same accessions and same observed original records"
    )
    return result


def analyse(fruit_bytes:bytes, seed_bytes:bytes, bootstrap:int=2000):
    original, _fruits, fruit_qc=read_original(fruit_bytes,strict=True)
    calibrated, seed_qc=parse_seed_calibration(seed_bytes,strict=True)
    records, joint_qc=eligible_joint_rows(original,calibrated,strict=True)
    policy=evaluate_policy(records,bootstrap_draws=bootstrap)
    if policy["n_panels"]!=164 or policy["n_design_excluded_panels"]!=1:
        raise ValueError("policy panel count changed, cannot claim matched action value")
    policy["fixed_protocol"]["value"] = (
        "estimated raw seeds = fruit * genotype-and-watering mean seeds per fruit"
    )
    policy["fixed_protocol"]["fine_model"] = (
        "P2 with zero-centered accession x action residual; ranking identical "
        "to uncentered P2 for any given accession"
    )
    policy["interpretive_limits"] = [
        "Average seed-per-fruit calibration was estimated within the same biological experiment, not separately by held-out rack",
        "These are estimated seeds, not direct plant-specific seed counts",
        "Four action outcomes are from different plants within each accession x rack",
        "Calibration availability selects 33/38 accessions and omits many zero-fruit plants",
        "Real irrigation or soil sterilization costs were not measured",
        "Genetic accession identity is nominal, not a measured SNP or molecular variant",
        "Exact MLTR source-target replacement and history theorems not evaluated",
    ]
    prediction=score_on_outcome(records,"estimated_seed_count","raw",True,bootstrap)
    legacy=score_on_outcome(records,"estimated_seed_count","raw",False,bootstrap)
    root=score_on_outcome(records,"estimated_seed_count","sqrt",True,bootstrap)
    fruit_matched=score_on_outcome(records,"fruit","sqrt",True,bootstrap)
    return {
        "source": {
            "paper_doi":"10.1111/jeb.13426",
            "dataset_doi":"10.5061/dryad.334765v",
            "fruit_csv_sha256":SOURCE_SHA256,
            "seed_csv_sha256":SEED_SOURCE_SHA256,
            "fruit": {"source_status":"user-supplied original file, hash-pinned",
                      "n_design":fruit_qc["records_design"]},
            "seed":seed_qc,
        },
        "cohort":joint_qc,
        "primary_seed_output_model":prediction,
        "legacy_uncentered_seed_output_model":legacy,
        "sqrt_seed_output_scale_sensitivity":root,
        "same_33_accessions_sqrt_fruit_sensitivity":fruit_matched,
        "raw_estimated_seed_action_decision":policy,
        "status":"ESTIMATED_SEED_FITNESS_RESPONSE_AND_DECISION_AUDIT_CONDITIONAL_SOURCE_CALIBRATION",
        "inferential_limits":[
            "Predefined exploratory source analysis, original published paper already described genotype-by-treatment fitness response",
            "All seed-output measurements are estimated as fruits x genotype-and-watering mean seed/fruit",
            "Seed-per-fruit lookup was estimated in same experiment, and per-rack calibration samples are unavailable; complete independence across held-out racks is not established",
            "The 33-accession complete water-pair cohort is not representative of all 38, as missing factors track many zero-fruit groups",
            "Within-accession action centering isolates relative treatment variation from accession mean repair",
            "No plant-level directly observed seeds, new experiment, molecular genome, causal genotype perturbation, cost-aware field policy, or exact MLTR formal theorem test",
        ],
    }


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--fruit",type=Path,required=True)
    ap.add_argument("--seed",type=Path,required=True)
    ap.add_argument("--out",type=Path,required=True)
    args=ap.parse_args()
    report=analyse(args.fruit.read_bytes(),args.seed.read_bytes())
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({
        "n_eligible":report["cohort"]["n_joint_observed"],
        "n_accessions":report["cohort"]["n_complete_seed_accessions"],
        "raw_seeds_model_gain":report["primary_seed_output_model"]["mean_gain_P2_minus_P1"],
        "raw_seeds_model_gate":report["primary_seed_output_model"]["positive_gate"],
        "decision_gain_estimated_seeds":report["raw_estimated_seed_action_decision"]["mean_gain_sqrt_fruit_per_panel"],
        "decision_gate":report["raw_estimated_seed_action_decision"]["status"],
        "n_complete_action_panels":report["raw_estimated_seed_action_decision"]["n_panels"],
    },sort_keys=True))


if __name__=="__main__":
    main()
