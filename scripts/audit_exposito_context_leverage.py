#!/usr/bin/env python3
"""Post-result accounting of how context-wise losses make up a frozen genomic gain.

Reads ONLY the already-committed Exposito-Alonso 2019 aggregate report.
No original samples, genotype matrices, predictions or new model fits are used.
Deleting one context means deleting it from SCORE ACCOUNTING ONLY, not
retraining, reselecting lambda or obtaining an out-of-context validation.
This is a descriptive audit, never a separate confirmatory genomic test.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

SOURCE_GIT_BLOB = "68cef71c368a17ef63fac066f0260f289fe99bc0"
SOURCE_REL = "docs/results/exposito_genomic_prediction_2026-11-22.json"
CONTEXTS = ("mhi", "mhp", "mli", "mlp", "thi", "thp", "tli", "tlp")
FOCAL_CONTEXT = "mlp"
MODES = (("primary", "accession"), ("geographic_sensitivity", "geographic"))
TOL = 2e-11


def git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()


def read_pinned_report(path: Path):
    raw = path.read_bytes()
    actual = git_blob_sha1(raw)
    if actual != SOURCE_GIT_BLOB:
        raise ValueError("frozen Exposito result source Git blob mismatch")
    result = json.loads(raw)
    return result, {"path_in_repository": SOURCE_REL, "git_blob_sha1": actual,
                    "sha256": hashlib.sha256(raw).hexdigest()}


def _finite(value, context):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"nonfinite/non-numeric {context}")
    return float(value)


def _close(a, b, label):
    if not math.isclose(a, b, abs_tol=TOL, rel_tol=0):
        raise ValueError(f"frozen score algebra mismatch: {label} ({a} vs {b})")


def decompose_mode(mode_report: dict, declared_split: str):
    if mode_report.get("split") != declared_split or mode_report.get("accessions") != 514:
        raise ValueError("wrong cohort or split for frozen context decomposition")
    if mode_report.get("response_cells") != 514 * len(CONTEXTS):
        raise ValueError("source context count changed")
    models = mode_report["models"]
    if set(models) != {"Mean", "M0", "M1"}:
        raise ValueError("source prediction model names changed")

    context_mse = {}
    for name in ("Mean", "M0", "M1"):
        source_scores = models[name]["context_mse"]
        if set(source_scores) != set(CONTEXTS):
            raise ValueError("source context identities changed")
        values = [_finite(source_scores[c], name + "." + c) for c in CONTEXTS]
        if min(values) < 0:
            raise ValueError("MSE cannot be negative")
        context_mse[name] = dict(zip(CONTEXTS, values))
        _close(sum(values) / len(CONTEXTS),
               _finite(models[name]["mse"], name + ".pooled"), name + " pooled MSE")

    recorded = mode_report["contrast"]
    recorded_gains = recorded["context_gains"]
    if set(recorded_gains) != set(CONTEXTS):
        raise ValueError("source gain contexts changed")
    gains = {}
    relative_percent = {}
    for c in CONTEXTS:
        delta = context_mse["M0"][c] - context_mse["M1"][c]
        _close(delta, _finite(recorded_gains[c], c + ".gain"), c + " context MSE gain")
        gains[c] = delta
        denom = context_mse["M0"][c]
        relative_percent[c] = 100 * delta / denom if denom > 0 else None

    pooled_m0 = _finite(models["M0"]["mse"], "M0.pooled")
    pooled_m1 = _finite(models["M1"]["mse"], "M1.pooled")
    gain = pooled_m0 - pooled_m1
    _close(gain, _finite(recorded["mean_gain"], "pooled gain"), "pooled M0-M1")
    _close(gain, sum(gains.values()) / len(CONTEXTS), "sum of context contributions")
    if mode_report["numerical_gate"].get("passed") is not False:
        raise ValueError("frozen positive-gain gate status changed")

    k = len(CONTEXTS)
    focal_gain = gains[FOCAL_CONTEXT]
    focal_pooled_contribution = focal_gain / k
    others = [c for c in CONTEXTS if c != FOCAL_CONTEXT]
    others_m0 = sum(context_mse["M0"][c] for c in others) / len(others)
    others_m1 = sum(context_mse["M1"][c] for c in others) / len(others)
    others_gain = others_m0 - others_m1
    _close(others_gain, sum(gains[c] for c in others) / len(others), "non-focal 7")
    contributions = {
        c: {"gain": gains[c], "pooled_gain_contribution": gains[c] / k,
            "M0_mse": context_mse["M0"][c], "M1_mse": context_mse["M1"][c],
            "M0_relative_error_reduction_percent": relative_percent[c]}
        for c in CONTEXTS
    }
    leave_one_context_score_only = {
        c: sum(gains[z] for z in CONTEXTS if z != c) / (k - 1)
        for c in CONTEXTS
    }
    valid_relatives = [v for v in relative_percent.values() if v is not None]
    return {
        "split": declared_split,
        "n_accessions": 514,
        "n_contexts": len(CONTEXTS),
        "recorded_primary_stability_gate_passed": False,
        "focal_context": FOCAL_CONTEXT,
        "focal_description": "Madrid; low rainfall; high-density/population planting",
        "pooled_mse": {"M0": pooled_m0, "M1": pooled_m1},
        "pooled_gain_M0_minus_M1": gain,
        "focal_context_gain": focal_gain,
        "focal_context_pooled_gain_contribution": focal_pooled_contribution,
        "focal_share_of_signed_pooled_gain_percent": (
            100 * focal_pooled_contribution / gain if gain != 0 else None),
        "focal_share_of_M0_pooled_loss_percent": (
            100 * context_mse["M0"][FOCAL_CONTEXT] / (k * pooled_m0)
            if pooled_m0 > 0 else None),
        "other_seven_contexts": {
            "mean_M0_mse": others_m0,
            "mean_M1_mse": others_m1,
            "mean_gain": others_gain,
            "M0_relative_error_reduction_percent": (
                100 * others_gain / others_m0 if others_m0 > 0 else None),
        },
        "n_positive_contexts": sum(v > 0 for v in gains.values()),
        "equal_context_mean_of_percent_M0_reductions": (
            sum(valid_relatives) / len(valid_relatives) if valid_relatives else None),
        "contributions_by_context": contributions,
        "delete_one_context_from_existing_score_without_refitting": leave_one_context_score_only,
        "frozen_conditional_interval_for_original_pooled_gain": [
            _finite(v, "original pooled interval") for v in recorded["conditional_ci95"]],
        "scope": "Post-result arithmetic accounting ONLY, not new heldout predictions, "
                 "inference on context effects, or a new confidence interval.",
    }


def audit(report: dict):
    if report.get("study_doi") != "10.1038/s41586-019-1520-9":
        raise ValueError("wrong source study")
    result = {name: decompose_mode(report[name], split) for name, split in MODES}
    return {
        "status": "POST_HOC_CONTEXT_LEVERAGE_ACCOUNTING_NOT_CONFIRMATORY",
        "frozen_production_model_unchanged": True,
        "source_study": report["study_doi"],
        "main_context": FOCAL_CONTEXT,
        "context_labels": list(CONTEXTS),
        "modes": result,
        "interpretation_limits": [
            "Focal mlp was singled out after inspecting previously reported gains.",
            "Signed share of net gain is not fraction of explained biological variation.",
            "The mlp context also accounts for a large share of M0 prediction loss.",
            "Leave-one-context figures delete a context only from fixed prediction scores; "
            "nothing was refitted or tuned and they have no new uncertainty intervals.",
            "Mean context-specific percent reductions use different M0 denominators and "
            "are an exploratory alternative summary, not the frozen primary estimand.",
            "No positive MLTR state-sufficiency, causal genome, or treatment-choice inference."
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path,
                        default=Path(__file__).resolve().parents[1] / SOURCE_REL)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    source, fingerprint = read_pinned_report(args.source)
    result = audit(source)
    result["source"] = fingerprint
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, ensure_ascii=False,
                                   sort_keys=True, allow_nan=False) + "\n",
                        encoding="utf-8")
    print(json.dumps({
        "result": str(args.out),
        "primary_signed_gain_share_percent": result["modes"]["primary"][
            "focal_share_of_signed_pooled_gain_percent"],
        "geographic_signed_gain_share_percent": result["modes"][
            "geographic_sensitivity"]["focal_share_of_signed_pooled_gain_percent"],
        "new_empirical_test": False,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
