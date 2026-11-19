#!/usr/bin/env python3
"""Source-locked three-species SNP audit; outputs aggregated genomic observations only.

Genotypes are from Nakahama et al., Dryad 10.5061/dryad.tb2rbp03j,
v20220815. This is not an MLTR action-response or adaptation test.
Uses Python standard library only. Raw genotypes must not be committed.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import random
import zipfile
from pathlib import Path

ZIP_SHA = "e81efee9bfe1f1176609bbcd3a1f23f9be63c698e614db09884676684ceb9b8c"
READ_SHA = "51e373dd9df6c20d8efc370ebb3beca2f55739c179c96dee5885a5e28c917627"
FILES = {
    "Cmaritimum": ("ecf44241752d8844e35d9cbdc4fa2d57d8aadbc3f2e1f0f17f77c4a4283fcd9e",
                   ["C1-2", "C2", "C3", "C4"], "C1-1", "C1-2", ["C1-3", "C1-4"]),
    "Ljaponica": ("5717cb242507a483ce6787aae694674e4267d9d131e158634614b6049872b711",
                  ["L1-2", "L2", "L3", "L4", "L5", "L7"], "L1-1", "L1-2", ["L1-3"]),
    "Sglauca": ("4325d8e89f715544e2a30d98b9525b235b175c0b1f3fcc07ed1ab02f4435d3de",
                ["S1-2", "S2", "S3"], "S1-1", "S1-2", ["S1-3", "S1-4"]),
}
# Values encode number of copies of the alternative allele + 1.
# 0 is entirely missing, 1=0101, 2=0102, 3=0202.
TOKENS = {"0000": 0, "0101": 1, "0102": 2, "0201": 2, "0202": 3}


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def parse(raw: bytes):
    lines = [x.strip() for x in raw.decode("utf-8-sig").splitlines() if x.strip()]
    if not lines or not lines[0].startswith("Title line:"):
        raise ValueError("invalid Genepop header")
    loci, order, data = [], [], {}
    current = None
    for line in lines[1:]:
        if line.casefold() == "pop":
            current = []
            continue
        if current is None:
            loci.extend(x.strip() for x in line.split(",") if x.strip())
            continue
        if "," not in line:
            raise ValueError("invalid Genepop genotype record")
        label, genotypes = line.split(",", 1)
        label = label.strip()
        fields = genotypes.split()
        if not label or len(fields) != len(loci):
            raise ValueError("wrong genotype row length")
        if any(t not in TOKENS for t in fields):
            raise ValueError("unsupported or partially missing allele encoding")
        if not current:
            if label in data:
                raise ValueError("duplicate POP block label")
            order.append(label)
            data[label] = current
        elif label != order[-1]:
            raise ValueError("mixed population codes inside POP block")
        current.append([TOKENS[t] for t in fields])
    if len(set(loci)) != len(loci) or not order:
        raise ValueError("duplicate or empty loci/populations")
    return loci, order, data


def observed_alleles(pop):
    answer = set()
    for i in range(len(pop[0])):
        calls = [row[i] for row in pop]
        if any(x in (1, 2) for x in calls):
            answer.add((i, 1))
        if any(x in (2, 3) for x in calls):
            answer.add((i, 2))
    return answer


def qc(pop):
    called = sum(g != 0 for row in pop for g in row)
    het = sum(g == 2 for row in pop for g in row)
    loci = len(pop[0])
    return {
        "n": len(pop), "loci": loci, "called": called,
        "call_fraction": round(called / (len(pop) * loci), 6),
        "heterozygosity_among_called": round(het / called, 6) if called else None,
    }


def historic(past, current, ex_situ):
    old = observed_alleles(past)
    modern = observed_alleles(current)
    old_missing = {x for x in old - modern if any(row[x[0]] != 0 for row in current)}
    absent_uninformative = {x for x in old - modern if not any(row[x[0]] != 0 for row in current)}
    ex_union = set().union(*(observed_alleles(group) for group in ex_situ.values()))
    singletons = 0
    for locus, allele in old_missing:
        copies = sum((row[locus] in ((1, 2) if allele == 1 else (2, 3)))
                     for row in past)
        if copies == 1:
            singletons += 1
    current_counts = [sum(row[j] != 0 for row in current) for j in range(len(current[0]))]
    thresholds = {str(k): sum(current_counts[locus] >= k for locus, _ in old_missing)
                  for k in (1, 2, 4, 6, 8) if k <= len(current)}
    return {
        "past_n": len(past), "current_n": len(current),
        "past_alleles_not_detected_current_at_callable_loci": len(old_missing),
        "past_alleles_at_entirely_uncalled_current_loci": len(absent_uninformative),
        "past_only_one_individual": singletons,
        "past_not_current_found_in_any_ex_situ": len(old_missing & ex_union),
        "by_ex_situ": {k: len(old_missing & observed_alleles(v))
                       for k, v in ex_situ.items()},
        "current_min_callable_individuals": thresholds,
        "claim": "sample detection only: not allele extinction or adaptive value",
    }


def fst(pop1, pop2, minimum=4):
    numer, denom, kept = 0.0, 0.0, 0
    for j in range(len(pop1[0])):
        a = [row[j] - 1 for row in pop1 if row[j] != 0]
        b = [row[j] - 1 for row in pop2 if row[j] != 0]
        na, nb = len(a), len(b)
        if min(na, nb) < minimum:
            continue
        pa, pb = sum(a) / (2 * na), sum(b) / (2 * nb)
        numer += (pa - pb)**2 - pa * (1 - pa) / (2 * na - 1) - pb * (1 - pb) / (2 * nb - 1)
        denom += pa * (1 - pb) + pb * (1 - pa)
        kept += 1
    return {"fst": round(numer / denom, 6) if denom > 0 else None, "loci": kept}


def loo_score(populations, labels, alpha=0.5, min_other=3):
    """Region-informed versus pooled-species allele log score for held-out individuals.

    Predicts observed SNP copies, NOT fitness. Held individual is removed from
    both population and species allele-frequency estimates at every locus.
    """
    individuals = [(g, row) for g in labels for row in populations[g]]
    loci = len(individuals[0][1])
    total_calls = [0] * loci
    total_alt = [0] * loci
    group_counts = {g: [0] * loci for g in labels}
    group_alt = {g: [0] * loci for g in labels}
    for group, row in individuals:
        for j, v in enumerate(row):
            if v == 0:
                continue
            total_calls[j] += 1
            total_alt[j] += v - 1
            group_counts[group][j] += 1
            group_alt[group][j] += v - 1
    total_diff = 0.0
    eligible_genotypes = 0
    sample_deltas = []
    for group, row in individuals:
        delta, used = 0.0, 0
        for j, v in enumerate(row):
            if not v:
                continue
            gc = group_counts[group][j] - 1
            sc = total_calls[j] - 1
            if gc < min_other or sc < 10:
                continue
            a1 = group_alt[group][j] - (v - 1)
            a0 = total_alt[j] - (v - 1)
            p1 = (a1 + alpha) / (2 * gc + 2 * alpha)
            p0 = (a0 + alpha) / (2 * sc + 2 * alpha)
            alt = v - 1
            delta += alt * math.log(p1 / p0) + (2 - alt) * math.log((1 - p1) / (1 - p0))
            used += 1
        if used:
            sample_deltas.append(delta / (2 * used))
            total_diff += delta
            eligible_genotypes += used
    if not eligible_genotypes:
        raise ValueError("no comparable held-out called genotypes")
    return {
        "mean_gain_nats_per_allele": round(total_diff / (2 * eligible_genotypes), 7),
        "mean_gain_bits_per_allele": round(total_diff / (2 * eligible_genotypes * math.log(2)), 7),
        "held_out_individuals": len(sample_deltas),
        "positive_individuals": sum(x > 0 for x in sample_deltas),
        "evaluated_genotypes": eligible_genotypes,
        "status": "PREDICTIVE_OBSERVED_SNP_ONLY",
    }



def permutation_check(populations, groups, n=999, seed=20424117):
    """Conditional label permutation, NOT exchangeability-proof or causal evidence.

    Shuffles whole individual group labels preserving group size and exact SNP
    missingness patterns. The available-locus subset may vary by permutation.
    """
    if n < 1:
        raise ValueError("permutation count must be positive")
    pooled = [row for group in groups for row in populations[group]]
    labels = [group for group in groups for _ in populations[group]]
    observed = loo_score(populations, groups)["mean_gain_nats_per_allele"]
    rng = random.Random(seed)
    null = []
    for _ in range(n):
        shuffle = list(labels)
        rng.shuffle(shuffle)
        shuffled = {label: [] for label in groups}
        for row, label in zip(pooled, shuffle):
            shuffled[label].append(row)
        stat = loo_score(shuffled, groups)["mean_gain_nats_per_allele"]
        null.append(stat)
    exceeds = sum(x >= observed for x in null)
    return {
        "observed_nats_per_allele": observed,
        "null_mean": round(sum(null) / n, 7),
        "null_q025": round(sorted(null)[int(0.025 * (n - 1))], 7), 
        "null_q975": round(sorted(null)[int(0.975 * (n - 1))], 7),
        "n_permutations": n, "random_seed": seed,
        "n_randomized_labels_ge_observed": exceeds,
        "one_sided_conditional_randomization_p": round((exceeds + 1) / (n + 1), 6),
        "claim": "geographic label association with observed SNP calls, not independent ecological or adaptive replication",
    }


def analyse_zip(path: Path, n_permutations: int = 0):
    raw = path.read_bytes()
    if len(raw) > 5_000_000 or digest(raw) != ZIP_SHA:
        raise ValueError("Dryad source archive is not the pinned v20220815 ZIP")
    output = {
        "source": {"doi": "10.5061/dryad.tb2rbp03j", "zip_sha256": digest(raw)},
        "status": "PREDICTIVE_GENOTYPE_ONLY_NOT_MLTR_ACTION_SUFFICIENCY", "species": {},
    }
    with zipfile.ZipFile(path) as archive:
        if digest(archive.read("README.txt")) != READ_SHA:
            raise ValueError("README hash conflict")
        readme = archive.read("README.txt").decode("utf-8-sig")
        for species, (expected, regions, past, current, ex_codes) in FILES.items():
            file_name = f"Genepop_{species}.txt"
            genotype = archive.read(file_name)
            if digest(genotype) != expected:
                raise ValueError(f"source file digest mismatch: {file_name}")
            loci, order, pop = parse(genotype)
            expected_codes = set(regions) | {past} | set(ex_codes)
            # The readme and file-code crosswalk is frozen before response testing;
            # never take POP order as time, conservation or geography.
            if set(order) != expected_codes or any(
                f"{label}:" not in readme for label in expected_codes
            ):
                raise ValueError(f"{species}: unexpected population codes/source labels")
            reference = {k: qc(v) for k, v in pop.items()}
            contrasts = [
                {"group_a": a, "group_b": b, **fst(pop[a], pop[b])}
                for a, b in itertools.combinations(regions, 2)
            ]
            result = {
                "source_sha256": digest(genotype), "n_loci": len(loci),
                "n_individuals": sum(len(v) for v in pop.values()),
                "n_populations": len(order), "population_order": order,
                "qc": reference,
                "historic_sampling": historic(pop[past], pop[current],
                                            {g: pop[g] for g in ex_codes}),
                "contemporary_region_pairs": contrasts,
                "out_of_individual_genotype_prediction": {
                    f"alpha_{a}": loo_score(pop, regions, alpha=a) for a in (0.5, 1.0, 2.0)
                },
                "interpretation_limit": (
                    "All taxa share one study/ascertainment pipeline. L. japonica L6 "
                    "is excluded from contemporary contrasts because it is historic "
                    "and has poor genotype calls. Predictor is SNP identity, not "
                    "reproductive performance, adaptation or MLTR action response."
                ),
            }
            if n_permutations:
                result["conditional_population_label_permutations"] = permutation_check(
                    pop, regions, n=n_permutations
                )
            output["species"][species] = result
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--zip", required=True, type=Path, help="original Dryad v20220815 zip")
    parser.add_argument("--out", type=Path, required=True, help="aggregated JSON output")
    parser.add_argument("--permutations", type=int, default=0,
                        help="optional conditional label shuffle, e.g. 999; no ecological causality inference")
    args = parser.parse_args()
    if args.permutations < 0 or args.permutations > 9999:
        raise ValueError("permutations outside bounded interval 0..9999")
    report = analyse_zip(args.zip, n_permutations=args.permutations)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    for name, result in report["species"].items():
        print(name, result["n_individuals"], result["n_loci"], "SNP loci")
    print(args.out)


if __name__ == "__main__":
    main()
