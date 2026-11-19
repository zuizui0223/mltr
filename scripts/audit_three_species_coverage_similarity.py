#!/usr/bin/env python3
"""Robustness audit: regional SNP prediction under even coverage and similarity purging.

Only observational genotypes. Does not identify genetic kinship, fitness,
selection, causal response, or an MLTR operational-state obstruction.
Requires original Nakahama et al. Dryad ZIP (not committed to the repository).
No third-party packages.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import zipfile
from pathlib import Path

from audit_three_species_snp_states import FILES, READ_SHA, ZIP_SHA, digest, parse


def common_locus_panel(groups: dict[str, list[list[int]]], fraction: float) -> list[bool]:
    if not 0 <= fraction <= 1:
        raise ValueError("fraction outside 0..1")
    n_loci = len(next(iter(groups.values()))[0])
    keep = []
    for j in range(n_loci):
        keep.append(all(
            sum(row[j] != 0 for row in rows) >= math.ceil(fraction * len(rows))
            for rows in groups.values()
        ))
    return keep


def shared_genotype_identity(a: list[int], b: list[int], min_shared: int = 60) -> float | None:
    shared = [(x, y) for x, y in zip(a, b) if x > 0 and y > 0]
    if len(shared) < min_shared:
        return None
    return sum(x == y for x, y in shared) / len(shared)


def similarity_inventory(
    grouped: dict[str, list[list[int]]], cut: float = 0.95, min_shared: int = 60
) -> dict:
    within, between = [], []
    high = 0
    items = [(g, row) for g, rows in grouped.items() for row in rows]
    for (g1, a), (g2, b) in itertools.combinations(items, 2):
        identity = shared_genotype_identity(a, b, min_shared)
        if identity is None:
            continue
        if g1 == g2:
            within.append(identity)
            high += identity >= cut
        else:
            between.append(identity)
    return {
        "within_pairs": len(within),
        "between_pairs": len(between),
        "within_mean_identity": round(sum(within) / len(within), 7) if within else None,
        "between_mean_identity": round(sum(between) / len(between), 7) if between else None,
        "within_max_identity": round(max(within), 7) if within else None,
        "between_max_identity": round(max(between), 7) if between else None,
        "within_pairs_above_cut": high,
        "similarity_cut": cut, "min_shared_called_loci": min_shared,
        "interpretation": "Genotype identity, not a validated relatedness or clone assignment",
    }


def score_held_out(
    grouped: dict[str, list[list[int]]],
    fraction: float = 0.75,
    remove_similar_at: float | None = None,
    min_shared: int = 60,
    alpha: float = 0.5,
) -> dict:
    if alpha <= 0:
        raise ValueError("smoothing alpha must be positive")
    panel = common_locus_panel(grouped, fraction)
    if not any(panel):
        return {"status": "NO_QUALIFYING_SNP_PANEL", "loci_panel": 0}
    rows = [(g, row) for g, entries in grouped.items() for row in entries]
    gain = 0.0
    n_valid = 0
    evaluated = 0
    positives = 0
    excluded_total = 0
    group_gain: dict[str, list[float]] = {}
    for hold, (region, target) in enumerate(rows):
        training = []
        for j, (r, row) in enumerate(rows):
            if j == hold:
                continue
            if remove_similar_at is not None and r == region:
                identity = shared_genotype_identity(target, row, min_shared)
                if identity is not None and identity >= remove_similar_at:
                    excluded_total += 1
                    continue
            training.append((r, row))
        local = [row for label, row in training if label == region]
        all_rows = [row for _, row in training]
        test_gain = 0.0
        test_n = 0
        for k, eligible in enumerate(panel):
            if not eligible or target[k] == 0:
                continue
            c_local = [row[k] for row in local if row[k] > 0]
            c_all = [row[k] for row in all_rows if row[k] > 0]
            if len(c_local) < 3 or len(c_all) < 10:
                continue
            p_local = (sum(v - 1 for v in c_local) + alpha) / (2 * len(c_local) + 2 * alpha)
            p_all = (sum(v - 1 for v in c_all) + alpha) / (2 * len(c_all) + 2 * alpha)
            n_alt = target[k] - 1
            test_gain += n_alt * math.log(p_local / p_all)
            test_gain += (2 - n_alt) * math.log((1 - p_local) / (1 - p_all))
            test_n += 1
        if test_n:
            gain += test_gain
            n_valid += 2 * test_n
            evaluated += 1
            positives += test_gain > 0
            group_gain.setdefault(region, []).append(test_gain / (2 * test_n))
    return {
        "status": "OBSERVED_GENOTYPE_PREDICTION_ONLY",
        "loci_panel": sum(panel),
        "min_coverage_each_population": fraction,
        "similarity_purge_cut": remove_similar_at,
        "min_shared_called_loci": min_shared,
        "smoothing_alpha": alpha,
        "mean_gain_nats_per_allele": round(gain / n_valid, 7) if n_valid else None,
        "evaluated_genotypes": n_valid // 2,
        "evaluated_individuals": evaluated,
        "positive_individuals": positives,
        "unevaluable_individuals": len(rows) - evaluated,
        "training_removals_total": excluded_total,
        "mean_gain_per_group": {
            k: round(sum(v) / len(v), 7) for k, v in group_gain.items()
        },
        "scope": "Leave-one-individual-out within known regions; not an unseen-region prediction",
    }


def missingness_score(grouped: dict[str, list[list[int]]], alpha: float = 1.0) -> dict:
    """Diagnostic: Does region label also predict binary SNP call/noncall status?"""
    rows = [(g, row) for g, entries in grouped.items() for row in entries]
    width = len(rows[0][1])
    global_n = [sum(row[k] != 0 for _, row in rows) for k in range(width)]
    gain = 0.0
    n_positive = 0
    for i, (group, target) in enumerate(rows):
        same = [row for label, row in rows if label == group]
        local_n = [sum(row[k] != 0 for row in same) for k in range(width)]
        local_t = len(same) - 1
        global_t = len(rows) - 1
        individual_gain = 0.0
        for k, v in enumerate(target):
            cv = int(v != 0)
            p_local = (local_n[k] - cv + alpha) / (local_t + 2 * alpha)
            p_all = (global_n[k] - cv + alpha) / (global_t + 2 * alpha)
            individual_gain += math.log(p_local / p_all) if cv else math.log((1-p_local)/(1-p_all))
        gain += individual_gain
        n_positive += individual_gain > 0
    return {
        "gain_nats_per_binary_SNP_call": round(gain / (len(rows) * width), 7),
        "positive_individuals": n_positive,
        "individuals": len(rows),
        "interpretation": "Technical call-status predictability can indicate batch/sample-quality confounding",
    }


def analyse(archive: Path) -> dict:
    if archive.stat().st_size > 5_000_000 or digest(archive.read_bytes()) != ZIP_SHA:
        raise ValueError("original Dryad ZIP hash mismatch")
    out = {
        "source": {"doi": "10.5061/dryad.tb2rbp03j", "zip_sha256": ZIP_SHA},
        "status": "SNP_GENOTYPE_ROBUSTNESS_ONLY_NOT_INTERVENTION_OR_MLTR_VALIDATION",
        "species": {},
        "limitations": [
            "All samples from one study; SNPs are not independent genomic loci",
            "Pairwise genotype identity is not a kinship coefficient",
            "Training exclusions can make held-out samples unevaluable",
            "Source processing had excluded loci found only in historical specimens",
            "Region-level scores cannot establish local adaptation or future action response",
        ],
    }
    with zipfile.ZipFile(archive) as z:
        if digest(z.read("README.txt")) != READ_SHA:
            raise ValueError("source README checksum conflict")
        for species, (file_sha, groups, past, current, exsitu) in FILES.items():
            filename = f"Genepop_{species}.txt"
            raw = z.read(filename)
            if digest(raw) != file_sha:
                raise ValueError(f"Genepop checksum conflict for {species}")
            _, _, all_groups = parse(raw)
            if species == "Ljaponica" and "L6" not in all_groups:
                raise ValueError("historical L6 must remain in QC")
            grouped = {g: all_groups[g] for g in groups}
            results = []
            for frac in (0.0, 0.5, 0.75, 1.0):
                for cut in (None, 0.95, 0.98):
                    results.append(score_held_out(grouped, fraction=frac, remove_similar_at=cut))
            out["species"][species] = {
                "regional_groups": groups, "n_individuals": sum(map(len, grouped.values())),
                "n_loci": len(next(iter(grouped.values()))[0]),
                "same_locus_coverage_and_similarity_sensitivities": results,
                "IBS": similarity_inventory(grouped),
                "technical_missingness_predictivity": missingness_score(grouped),
            }
    return out


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--zip", required=True, type=Path)
    p.add_argument("--out", required=True, type=Path)
    args = p.parse_args()
    result = analyse(args.zip)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n", encoding="utf-8")
    for taxon, findings in result["species"].items():
        print(taxon, "n", findings["n_individuals"], "SNPs", findings["n_loci"])
    print("Saved", args.out)


if __name__ == "__main__":
    main()
