#!/usr/bin/env python3
"""Endpoint concordance and exploratory source-quality sensitivity in white clover.

Requires the exact original user-supplied Dryad v20250829 ZIP. This script
reuses the already frozen source/QC and M0/M1/M2 model functions, and reports
only aggregate values; it never writes raw genotype or specimen identifiers.

Excluding cases by a second outcome-like field is *post-outcome selection* and
therefore cannot replace the original preregistered 470-plant analysis.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
from collections import Counter
from pathlib import Path

from analyze_clover_haploblock_fitness import source_data, read_source, evaluate, HAPS


def _num(record: dict, field: str) -> float | None:
    value = str(record.get(field, "")).strip()
    return None if value in {"", "NA", "NaN", "nan", "999", "999.0"} else float(value)


def indicator_flags(record: dict) -> dict[str, bool]:
    """Source-field mismatches, not automatically proven measurement errors."""
    flower = _num(record, "FloweredFull")
    heads = _num(record, "FlowerHeadNumberFull")
    seeds = _num(record, "SeedSetMassFull")
    survived = _num(record, "Survived1st")
    if flower not in (0, 1) or heads is None or seeds is None:
        raise ValueError("source indicator not interpretable")
    return {
        "flowered_one_head_zero": flower == 1 and heads == 0,
        "flowered_zero_head_positive": flower == 0 and heads > 0,
        "flowered_one_seed_zero": flower == 1 and seeds == 0,
        "flowered_zero_seed_positive": flower == 0 and seeds > 0,
        "flowered_one_firstyear_survival_zero": flower == 1 and survived == 0,
    }


def audit(original_zip: Path, evaluate_exploratory: bool = True) -> dict:
    raw_csv, provenance = source_data(original_zip, is_zip=True)
    rows = list(csv.DictReader(io.StringIO(raw_csv.decode("utf-8-sig"))))
    records, source_qc = read_source(raw_csv)
    counts = Counter(row["File"].strip() for row in rows)
    reused = {name for name, n in counts.items() if name and n > 1}
    retained_rows = [row for row in rows if row["File"].strip() not in reused]
    if len(retained_rows) != len(records):
        raise ValueError("original source processing excludes more than the duplicated-ID rows")
    for item, processed in zip(retained_rows, records):
        if (
            item["Garden"] != processed["garden"]
            or str(item["Population"]) != processed["population"]
            or int(float(item["FloweredFull"])) != processed["y"]
        ):
            raise ValueError("row-level source-to-model crosswalk drift")

    garden_names = sorted(set(item["Garden"] for item in retained_rows))
    flags = [indicator_flags(row) for row in retained_rows]
    flag_names = list(flags[0])
    by_flag = {
        name: {
            "n": sum(item[name] for item in flags),
            "by_garden": {
                g: sum(item[name] for item, row in zip(flags, retained_rows) if row["Garden"] == g)
                for g in garden_names
            },
        }
        for name in flag_names
    }
    discordant_head = [
        bool(f["flowered_one_head_zero"] or f["flowered_zero_head_positive"])
        for f in flags
    ]
    rare = {
        h: {
            dosage: sum(float(row[h]) == float(dosage) for row in retained_rows)
            for dosage in ("0", "0.5", "1")
        }
        for h in HAPS
    }
    baseline_scores, baseline_contrasts, baseline_folds = evaluate(records)
    m1 = baseline_contrasts["M1_minus_M0"]
    report = {
        "status": "SOURCE_ENDPOINT_CONCORDANCE_EXPLORATORY_NOT_MLTR_VALIDATION",
        "source": provenance,
        "population_disjoint_original_model": {
            "n": len(records),
            "origin_populations": source_qc["complete_origin_populations"],
            "model_log_loss": {
                k: v["out_of_origin_population_log_loss"] for k, v in baseline_scores.items()
            },
            "M1_minus_M0_individual_mean_nats": m1["individual_mean_gain_nats"],
            "M1_minus_M0_population_equal_mean_nats": m1["population_equal_weight_gain_nats"],
        },
        "n_original_raw_rows": len(rows),
        "n_excluded_ambiguous_ID_rows": len(rows) - len(records),
        "n_analysed": len(records),
        "garden_counts": source_qc["gardens"],
        "indicator_discordance": by_flag,
        "n_flowered_head_count_discordant": sum(discordant_head),
        "haploblock_dosage_counts": rare,
        "interpretation": [
            "FloweredFull, FlowerHeadNumberFull, SeedSetMassFull and Survived1st are distinct source variables and may differ in measurement timing/definition.",
            "Discordance alone does not demonstrate a source coding error.",
            "Five scored haploblocks are not a full genomic ancestry panel; rarer dosage categories are sparse.",
            "The preregistered original 470-plant prediction test is the primary scientific result.",
        ],
    }
    if evaluate_exploratory:
        selected = [record for record, mismatch in zip(records, discordant_head) if not mismatch]
        scores, contrasts, folds = evaluate(selected)
        report["head_concordant_subset"] = {
            "status": "POST_OUTCOME_SELECTED_DIAGNOSTIC_NOT_PRIMARY",
            "n": len(selected),
            "excluded_from_original": len(records) - len(selected),
            "origin_populations": len(set(x["population"] for x in selected)),
            "model_log_loss": {k: v["out_of_origin_population_log_loss"] for k, v in scores.items()},
            "M1_minus_M0_individual_mean_nats": contrasts["M1_minus_M0"]["individual_mean_gain_nats"],
            "M1_minus_M0_population_equal_mean_nats": contrasts["M1_minus_M0"]["population_equal_weight_gain_nats"],
            "M1_minus_M0_garden_mean_nats": contrasts["M1_minus_M0"]["garden_mean_gains"],
            "warning": "case selection by outcome-adjacent variable and changed folds; not a confirmatory causal correction",
        }
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--zip", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.zip)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("source QC discordant records:", result["n_flowered_head_count_discordant"])
    print("source-verified report:", args.out)


if __name__ == "__main__":
    main()
