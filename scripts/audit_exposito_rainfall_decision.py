#!/usr/bin/env python3
"""Frozen, exploratory out-of-accession rainfall-allocation decision value.

Source: Exposito-Alonso et al. (2019) published 514-accession × 8-condition
estimated-fitness summaries, measured under high/low rainfall in two sites and
two planting densities. Genomics enters only through the already frozen M1
kernel. Site/density fixed; high-rainfall resource quota 25% per outer fold.

NEVER compare training-relative predictions across rainfall contexts. Every
relative forecast is multiplied by its own *training-only* context mean prior
to allocation. All heldout targets are masked before invoking the existing
nested fit. Only aggregate output, no accession-level policies, is written.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np

from analyze_exposito_genomic_fitness import (
    CONTEXTS, SPLIT_SEED, validate_arrays, accession_folds, spatial_folds,
    geographic_cells, fit_outer_fold, verify_source_binding,
)

PROTOCOL_GIT_BLOB_SHA1 = "9d315bc5b0317d7d2ec0b950bd9697f33c3eb774"
COHORT_IDS_SHA256 = "781bdddcae7dd562802f76c1dea824e74a8ae2d62148bb015ceff441b017fb19"
SOURCE_SHA256 = {
    "S_DATASETS.xlsx": "032045433e3ace035977c11ff5d0ae8731335e8210c6cee14d64575ae0bebd05",
    "ibs1001g.rda": "906724ce620a30a8c199ade07c5ffaa27aa7b1a91e8229f63b27e882547a70ad",
}
STRATA = (("mi", "mhi", "mli"), ("mp", "mhp", "mlp"),
          ("ti", "thi", "tli"), ("tp", "thp", "tlp"))
QUOTA_FRACTION = 0.25
BOOTSTRAP_SEED = 20261124
BOOTSTRAP_DRAWS = 2000


def git_blob_sha1(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()


def choose_high_rainfall(ids, predicted_high, predicted_low):
    """Exactly ceil(25% of heldout accessions), rank by raw projected gain.

    Stable ties are resolved by numeric accession identifier. Outcomes never
    enter this function. No switch to a more favorable budget is permitted.
    """
    ids = list(map(str, ids))
    high = np.asarray(predicted_high, dtype=float)
    low = np.asarray(predicted_low, dtype=float)
    n = len(ids)
    if not n or len(high) != n or len(low) != n or len(set(ids)) != n:
        raise ValueError("invalid rainfall allocation candidate set")
    if (not np.isfinite(high).all() or not np.isfinite(low).all()
            or np.any(high < 0) or np.any(low < 0)):
        raise ValueError("invalid raw predicted fitness for rainfall choice")
    if any(not z.isdigit() or int(z) <= 0 for z in ids):
        raise ValueError("rainfall allocation IDs must be positive integers")
    k = math.ceil(QUOTA_FRACTION * n)
    gains = high - low
    order = sorted(range(n), key=lambda i: (-gains[i], int(ids[i])))
    selected = np.zeros(n, dtype=bool)
    selected[order[:k]] = True
    if int(selected.sum()) != k:
        raise ValueError("high rainfall fixed quota violated")
    return selected


def evaluate_heldout_policy(ids, outcomes, model_raw):
    """Compare policies on separately measured high/low treatment summaries."""
    ids = np.asarray(ids).astype(str)
    outcomes = np.asarray(outcomes, dtype=float)
    if outcomes.shape != (len(ids), len(CONTEXTS)):
        raise ValueError("heldout experimental outcome matrix mismatch")
    if not np.isfinite(outcomes).all() or np.any(outcomes < 0):
        raise ValueError("invalid heldout fitness summary")
    if set(model_raw) != {"M0", "M1"}:
        raise ValueError("only frozen geographic and genomic models allowed")
    for name, predicted in model_raw.items():
        v = np.asarray(predicted, dtype=float)
        if v.shape != outcomes.shape or not np.isfinite(v).all() or np.any(v < 0):
            raise ValueError("invalid raw model predictions: " + name)

    per_accession_by_stratum = np.zeros((len(ids), len(STRATA)))
    stratified = []
    changes = 0
    baseline_assignments = []
    for j, (key, high, low) in enumerate(STRATA):
        hi, lo = CONTEXTS.index(high), CONTEXTS.index(low)
        m0 = choose_high_rainfall(ids, model_raw["M0"][:, hi], model_raw["M0"][:, lo])
        m1 = choose_high_rainfall(ids, model_raw["M1"][:, hi], model_raw["M1"][:, lo])
        quota = math.ceil(len(ids) * QUOTA_FRACTION)
        if int(m0.sum()) != quota or int(m1.sum()) != quota:
            raise ValueError("M0 and M1 did not receive identical rainfall budget")
        raw_high, raw_low = outcomes[:, hi], outcomes[:, lo]
        value_m0 = np.where(m0, raw_high, raw_low)
        value_m1 = np.where(m1, raw_high, raw_low)
        changed = int(np.count_nonzero(m0 != m1))
        changes += changed
        per_accession_by_stratum[:, j] = value_m1 - value_m0
        # Descriptive constant-allocation reference, not outcome-selected:
        # exactly same high rainfall quota, smallest numeric IDs first.
        baseline = np.zeros(len(ids), dtype=bool)
        baseline[sorted(range(len(ids)), key=lambda i: int(ids[i]))[:quota]] = True
        baseline_value = np.where(baseline, raw_high, raw_low)
        baseline_assignments.append(baseline_value)
        stratified.append({
            "stratum": key, "site": "Madrid" if key[0] == "m" else "Tuebingen",
            "density": "single" if key[1] == "i" else "high",
            "n_heldout_accessions": len(ids), "high_rainfall_quota": quota,
            "n_changed_accession_rainfall_decisions": changed,
            "mean_realized_M0_estimated_fitness": float(value_m0.mean()),
            "mean_realized_M1_estimated_fitness": float(value_m1.mean()),
            "mean_realized_ID_baseline_fitness": float(baseline_value.mean()),
            "mean_M1_minus_M0_fitness": float((value_m1 - value_m0).mean()),
        })
    return per_accession_by_stratum, stratified, changes


def conditional_interval(gain_per_accession, groups=None):
    """Conditional bootstrap of fixed policies, no model/policy refitting."""
    gain = np.asarray(gain_per_accession, dtype=float)
    if gain.ndim != 1 or not len(gain) or not np.isfinite(gain).all():
        raise ValueError("invalid per-accession value gain")
    rng = np.random.default_rng(BOOTSTRAP_SEED)
    if groups is None:
        index = rng.integers(0, len(gain), size=(BOOTSTRAP_DRAWS, len(gain)))
        values = gain[index].mean(axis=1)
        count,unit = len(gain),"accession"
    else:
        groups = np.asarray(groups)
        if len(groups) != len(gain):
            raise ValueError("bootstrap geographic groups not aligned")
        _, inverse = np.unique(groups, axis=0, return_inverse=True)
        sizes = np.bincount(inverse)
        sums = np.bincount(inverse, weights=gain)
        sampled = rng.integers(0, len(sizes), size=(BOOTSTRAP_DRAWS, len(sizes)))
        values = sums[sampled].sum(axis=1)/sizes[sampled].sum(axis=1)
        count,unit = len(sizes),"five_degree_origin_cell"
    return {
        "mean": float(gain.mean()),
        "ci95": np.quantile(values, [.025,.975], method="linear").tolist(),
        "resampling_clusters": count, "unit": unit, "draws": BOOTSTRAP_DRAWS,
        "seed": BOOTSTRAP_SEED,
        "conditioning": "fixed source observations, nested model fits and allocations",
    }


def evaluate_policy(data, mode, fit_function=fit_outer_fold):
    """Fit the original frozen genomic model and only then reveal heldout Y."""
    data = validate_arrays(data)
    n = len(data["ids"])
    if n != 514:
        raise ValueError("the source cohort is not the published 514-accession benchmark")
    ids_hash = hashlib.sha256(
        ("\n".join(data["ids"].tolist()) + "\n").encode("utf-8")).hexdigest()
    if ids_hash != COHORT_IDS_SHA256:
        raise ValueError("accession source ID set/order changed")
    cells = geographic_cells(data["coords"])
    if mode == "accession":
        folds = accession_folds(n, 5, SPLIT_SEED)
    elif mode == "geographic":
        folds = spatial_folds(cells, 5)
    else:
        raise ValueError("unknown genomic prediction split")
    deltas = np.full((n,len(STRATA)), np.nan)
    raw_losses = {name: np.full((n,len(CONTEXTS)), np.nan) for name in ("M0","M1")}
    fold_summary = []
    for fold_index,(train,held) in enumerate(folds,1):
        # Guard: heldout target is NOT AVAILABLE during fit/inner tuning.
        fit_data = dict(data)
        fit_data["fitness"] = data["fitness"].copy()
        fit_data["fitness"][held] = np.nan
        fitted = fit_function(fit_data, train, held, mode, fold_index)
        means = np.asarray(fitted["training_means"],dtype=float)
        if means.shape != (len(CONTEXTS),) or not np.isfinite(means).all() or np.any(means <= 0):
            raise ValueError("model train context means invalid")
        actual = data["fitness"][held]
        preds = {}
        for name in ("M0","M1"):
            relative = np.asarray(fitted["predictions"][name],dtype=float)
            if relative.shape != actual.shape or not np.isfinite(relative).all():
                raise ValueError("frozen model produced wrong forecast dimensions")
            preds[name] = relative * means[None,:]
            raw_losses[name][held] = (preds[name]-actual)**2
        panel, strata, changes = evaluate_heldout_policy(
            data["ids"][held], actual, preds)
        deltas[held] = panel
        fold_summary.append({
            "fold": fold_index, "heldout_accessions":len(held),
            "train_accessions":len(train),
            "M1_minus_M0_mean_policy_value":float(panel.mean()),
            "n_changed_accession_stratum_decisions":changes,
            "strata":strata,
            "train_ids_sha256":hashlib.sha256(
                ("\n".join(sorted(data["ids"][train].tolist(),key=int))+"\n").encode()
            ).hexdigest(),
            "heldout_ids_sha256":hashlib.sha256(
                ("\n".join(sorted(data["ids"][held].tolist(),key=int))+"\n").encode()
            ).hexdigest(),
            "selected_lambdas": fitted.get("selected_lambdas"),
        })
    if not np.isfinite(deltas).all() or any(not np.isfinite(x).all() for x in raw_losses.values()):
        raise ValueError("some policies or forecasts are missing")
    policy_gain = deltas.mean(axis=1)
    interval = conditional_interval(policy_gain,cells if mode=="geographic" else None)
    per_context = {k:float(deltas[:,j].mean()) for j,(k,_,_) in enumerate(STRATA)}
    fold_gains = [x["M1_minus_M0_mean_policy_value"] for x in fold_summary]
    changed=sum(f["n_changed_accession_stratum_decisions"] for f in fold_summary)
    conditions={
        "overall_gain_positive":bool(interval["mean"]>0),
        "conditional_interval_lower_positive":bool(interval["ci95"][0]>0),
        "at_least_four_of_five_outer_folds_positive":sum(v>0 for v in fold_gains)>=4,
        "at_least_three_of_four_fixed_strata_positive":sum(v>0 for v in per_context.values())>=3,
        "at_least_one_changed_action":changed>0,
    }
    return {
        "split":mode, "n_accessions":n,
        "n_site_density_decisions":int(deltas.size),
        "n_strata":len(STRATA),
        "n_changed_accession_stratum_decisions":changed,
        "fraction_changed_decisions":changed/deltas.size,
        "M1_minus_M0_mean_realized_estimated_fitness":interval["mean"],
        "conditional_interval":interval,
        "site_density_gains":per_context,
        "n_positive_strata":sum(v>0 for v in per_context.values()),
        "n_positive_outer_folds":sum(v>0 for v in fold_gains),
        "folds":fold_summary,
        "raw_fitness_prediction_mse_diagnostic": {
            name:float(values.mean()) for name,values in raw_losses.items()
        },
        "numerical_gate":{
            "role":"primary" if mode=="accession" else "sensitivity_only",
            "conditions":conditions, "passed":all(conditions.values())
        },
        "meaning":"retrospective equal-quota treatment choice using four site/density "
                  "strata and published aggregated fitness per planted seed",
    }


def analyse(prepared, source_audit, protocol):
    prepared = Path(prepared); source_audit=Path(source_audit); protocol=Path(protocol)
    raw_protocol=protocol.read_bytes()
    if git_blob_sha1(raw_protocol) != PROTOCOL_GIT_BLOB_SHA1:
        raise ValueError("rainfall decision protocol changed after freeze")
    audit=json.loads(source_audit.read_bytes())
    verify_source_binding(prepared,audit)
    files=audit.get("source_files")
    if not isinstance(files,list) or {r.get("name"):r.get("sha256") for r in files} != SOURCE_SHA256:
        raise ValueError("wrong source file fingerprints")
    with np.load(prepared,allow_pickle=False) as archive:
        data=validate_arrays({name:archive[name] for name in archive.files})
    if (audit.get("n_accessions")!=514 or audit.get("n_contexts")!=8
            or audit.get("n_response_cells")!=4112
            or audit.get("cohort_ids_sha256")!=COHORT_IDS_SHA256):
        raise ValueError("original source admission mismatch")
    return {
        "study_doi":"10.1038/s41586-019-1520-9",
        "status":"POST_RESULT_EXPLORATORY_RAINFALL_POLICY_VALUE",
        "provenance":{
            "prepared_npz_sha256":audit["prepared_npz_sha256"],
            "source_audit_sha256":hashlib.sha256(source_audit.read_bytes()).hexdigest(),
            "protocol_git_blob_sha1":PROTOCOL_GIT_BLOB_SHA1,
            "analysis_script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "source_files":files,
            "cohort_ids_sha256":COHORT_IDS_SHA256
        },
        "settings":{
            "budget_fraction":QUOTA_FRACTION,
            "budget_per_outer_fold_and_site_density":"ceil(0.25 * heldout accessions)",
            "heldout_unit":"entire accession, all eight experimental contexts",
            "decision":"high vs low rainfall in fixed site × planting density",
            "units":"published estimated fitness per planted seed, unstandardized",
            "train_relative_predictions_denormalized":True,
            "bootstrap_seed":BOOTSTRAP_SEED,"bootstrap_draws":BOOTSTRAP_DRAWS,
            "source_experiment_replicated":False,
            "post_result_followup":True
        },
        "primary":evaluate_policy(data,"accession"),
        "geographic_sensitivity":evaluate_policy(data,"geographic"),
        "interpretation_limits":[
            "Prediction results from the original frozen M0/M1 model without outcome-dependent alterations.",
            "Experimental high/low precipitation is simulated as a hypothetical scarce water-budget intervention.",
            "No observed water-treatment cost or feasible field conservation policy.",
            "Published accession×context summaries of estimated fitness; not independently observed potential outcomes for single plants.",
            "Source genotype-distance object may capture ancestry and finer geographic structure.",
            "Bootstrap conditions on original measurements, preprocessing, selected fits and fixed allocations.",
            "No new experimental replication, causal genome effect or exact MLTR carried-history theorem test.",
            "Original genome-kernel prediction increment remained unsupported by its frozen gate."
        ]
    }


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prepared",required=True,type=Path)
    parser.add_argument("--source-audit",required=True,type=Path)
    parser.add_argument("--protocol",required=True,type=Path)
    parser.add_argument("--out",required=True,type=Path)
    args=parser.parse_args()
    result=analyse(args.prepared,args.source_audit,args.protocol)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+"\n",encoding="utf-8")
    print(json.dumps({
        "n_accessions":result["primary"]["n_accessions"],
        "n_decisions":result["primary"]["n_site_density_decisions"],
        "M1_over_M0_policy_gain":result["primary"]["M1_minus_M0_mean_realized_estimated_fitness"],
        "primary_interval":result["primary"]["conditional_interval"]["ci95"],
        "primary_positive_gate":result["primary"]["numerical_gate"]["passed"],
        "primary_changed_decisions":result["primary"]["n_changed_accession_stratum_decisions"],
        "geographic_gain":result["geographic_sensitivity"]["M1_minus_M0_mean_realized_estimated_fitness"],
        "geographic_positive_gate":result["geographic_sensitivity"]["numerical_gate"]["passed"],
    },sort_keys=True))


if __name__=="__main__":
    main()
