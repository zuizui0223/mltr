#!/usr/bin/env python3
"""Source-locked descriptive QC for the public Cirsium maritimum MIG-seq Genepop.

Never infers history/fitness/MLTR decision sufficiency from population genotypes.
Only uses Python's standard library; it can run offline on an independently
downloaded Genepop file or download the whole published Dryad ZIP (opt-in).
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import sys
import urllib.request
import zipfile
from collections import Counter
from pathlib import Path
from typing import Any

DOI = "10.5061/dryad.tb2rbp03j"
API_ZIP = "https://datadryad.org/api/v2/datasets/doi%3A10.5061%2Fdryad.tb2rbp03j/download"
TARGET = "Genepop_Cmaritimum.txt"
MAX_ZIP_BYTES = 5_000_000
ALLOWED_GROUPS = {"past_wild", "current_wild", "ex_situ"}


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def fetch_dryad() -> tuple[bytes, bytes | None, dict[str, Any]]:
    """Public dataset ZIP, no auth or unknown mirror. Fail closed on errors."""
    req = urllib.request.Request(
        API_ZIP, headers={"User-Agent": "MLTR-Genepop-audit/0.1 (research)"}
    )
    with urllib.request.urlopen(req, timeout=45) as response:
        raw = response.read(MAX_ZIP_BYTES + 1)
    if len(raw) > MAX_ZIP_BYTES:
        raise ValueError("Dryad ZIP exceeds bounded maximum size")
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        matches = [n for n in archive.namelist() if Path(n).name == TARGET]
        readmes = [n for n in archive.namelist() if Path(n).name == "README.txt"]
        if len(matches) != 1 or len(readmes) > 1:
            raise ValueError("expected exactly one Genepop file and at most one README")
        genotype = archive.read(matches[0])
        readme = archive.read(readmes[0]) if readmes else None
    return genotype, readme, {
        "mode": "dryad_api_zip",
        "doi": DOI,
        "api_url": API_ZIP,
        "zip_sha256": sha256(raw),
        "zip_bytes": len(raw),
    }


def allele_pair(token: str) -> tuple[str, str] | None:
    """GENEPOP diploid 2- or 3-digit allele encoding; all-zero is missing."""
    token = token.strip()
    if not re.fullmatch(r"[0-9]+", token) or len(token) not in (4, 6):
        raise ValueError(f"unsupported diploid genotype token: {token!r}")
    half = len(token) // 2
    a, b = token[:half], token[half:]
    if int(a) == int(b) == 0:
        return None
    if int(a) == 0 or int(b) == 0:
        raise ValueError("partial-zero genotype requires manual decoding audit")
    return (a, b)


def parse_genepop(raw: bytes) -> tuple[list[str], list[list[tuple[str, list[tuple[str, str] | None]]]]]:
    """Strict parser: never silently skip lines, drop loci or impute missing calls."""
    text = raw.decode("utf-8-sig")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if len(lines) < 4:
        raise ValueError("too few Genepop lines")
    loci: list[str] = []
    populations: list[list[tuple[str, list[tuple[str, str] | None]]]] = []
    entered_pop = False
    for lineno, line in enumerate(lines[1:], 2):
        if line.casefold() == "pop":
            if entered_pop and not populations[-1]:
                raise ValueError(f"empty POP block at nonblank line {lineno}")
            entered_pop = True
            populations.append([])
            continue
        if not entered_pop:
            loci.extend(item.strip() for item in line.split(","))
            continue
        if "," not in line:
            raise ValueError(f"sample line lacks sample-ID comma at {lineno}")
        name, genotypes = line.split(",", 1)
        name = name.strip()
        tokens = genotypes.split()
        if not name or len(tokens) != len(loci):
            raise ValueError(f"sample/locus mismatch at {lineno}: {name!r}, {len(tokens)} != {len(loci)}")
        if any(name == existing[0] for existing in populations[-1]):
            raise ValueError(f"duplicate sample ID within POP block: {name!r}")
        populations[-1].append((name, [allele_pair(token) for token in tokens]))
    if not loci or len(set(loci)) != len(loci) or not populations or not populations[-1]:
        raise ValueError("no loci, duplicate locus names, or empty populations")
    return loci, populations


def profile(loci: list[str], pop: list[tuple[str, list[tuple[str, str] | None]]]) -> dict:
    called = 0
    hetero = 0
    alleles: dict[str, set[str]] = {locus: set() for locus in loci}
    per_locus_called = {locus: 0 for locus in loci}
    for _, genotype in pop:
        for locus, pair in zip(loci, genotype):
            if pair is None:
                continue
            called += 1
            per_locus_called[locus] += 1
            hetero += int(pair[0] != pair[1])
            alleles[locus].update(pair)
    n = len(pop)
    return {
        "n_individuals": n,
        "n_loci": len(loci),
        "called_genotypes": called,
        "possible_genotypes": n * len(loci),
        "call_fraction": round(called / (n * len(loci)), 8),
        "observed_heterozygosity": round(hetero / called, 8) if called else None,
        "loci_with_any_call": sum(bool(x) for x in alleles.values()),
        "polymorphic_loci": sum(len(x) > 1 for x in alleles.values()),
        "locus_allele_count_total": sum(map(len, alleles.values())),
        "sample_id_examples": [sample_id for sample_id, _ in pop[:3]],
        "locus_call_counts": per_locus_called,
        "_alleles": alleles,
    }


def read_map(path: Path, n_pop: int) -> dict[int, str]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    result: dict[int, str] = {}
    for row in rows:
        index = int(row["pop_index"])
        group = row["group"].strip()
        if index in result or index < 1 or index > n_pop or group not in ALLOWED_GROUPS:
            raise ValueError("invalid, repeated or out-of-range population map entry")
        result[index] = group
    if set(result) != set(range(1, n_pop + 1)):
        raise ValueError("population map must explicitly assign every POP block")
    if set(result.values()) != ALLOWED_GROUPS:
        raise ValueError("population map requires past_wild/current_wild/ex_situ")
    return result


def analyse(
    raw: bytes, provenance: dict[str, Any], group_map: dict[int, str] | None = None
) -> dict[str, Any]:
    loci, populations = parse_genepop(raw)
    profs = [profile(loci, pop) for pop in populations]
    seen: dict[str, list[int]] = {}
    for i, pop in enumerate(populations, 1):
        for sample_id, _ in pop:
            seen.setdefault(sample_id, []).append(i)
    duplicates = sorted(sample_id for sample_id, blocks in seen.items() if len(blocks) > 1)
    outputs = []
    for i, prof in enumerate(profs, 1):
        row = {key: value for key, value in prof.items() if not key.startswith("_")}
        row["pop_index"] = i
        row["group"] = group_map[i] if group_map else None
        outputs.append(row)
    result = {
        "status": "POPULATION_QC_ONLY_NO_DECISION_RESPONSE",
        "source": {**provenance, "genepop_sha256": sha256(raw), "genepop_bytes": len(raw)},
        "n_loci": len(loci),
        "n_populations": len(populations),
        "n_individuals": sum(map(len, populations)),
        "duplicated_sample_ids_across_pop_blocks": duplicates,
        "populations": outputs,
        "historical_observed_allele_comparison": None,
        "limitations": [
            "No source-linked fitness, intervention or environmental response: not an empirical MLTR decision-sufficiency test.",
            "POP block meanings must be independently crosswalked to README; no labels inferred from order.",
            "An allele not observed in one sample is not proven extinct; unequal coverage/sampling can induce differences.",
            "Population/locus summaries do not establish hybridization, adaptation or causal histories.",
        ],
    }
    if group_map:
        by_group = {group: set() for group in ALLOWED_GROUPS}
        for i, prof in enumerate(profs, 1):
            by_group[group_map[i]].update(
                (locus, allele)
                for locus, alleles in prof["_alleles"].items()
                for allele in alleles
            )
        past, current, exsitu = (by_group[g] for g in ("past_wild", "current_wild", "ex_situ"))
        not_observed_current = past - current
        result["historical_observed_allele_comparison"] = {
            "past_observed_not_current_observed": len(not_observed_current),
            "past_not_current_but_ex_situ_observed": len(not_observed_current & exsitu),
            "past_not_current_and_not_ex_situ_observed": len(not_observed_current - exsitu),
            "past_observed_total": len(past),
            "current_observed_total": len(current),
            "ex_situ_observed_total": len(exsitu),
            "status": "DESCRIPTIVE_SAMPLE_DETECTION_ONLY_NOT_ALLELE_EXTINCTION",
        }
    return result


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    source = p.add_mutually_exclusive_group(required=True)
    source.add_argument("--input", type=Path, help="local original Genepop file")
    source.add_argument("--from-dryad", action="store_true", help="fetch public published ZIP")
    p.add_argument("--population-map", type=Path, help="reviewed CSV: pop_index,group")
    p.add_argument("--out", type=Path, required=True, help="output JSON; no raw genotypes emitted")
    args = p.parse_args()
    if args.from_dryad:
        raw, readme, provenance = fetch_dryad()
        if readme is not None:
            provenance["readme_sha256"] = sha256(readme)
            provenance["readme_bytes"] = len(readme)
    else:
        raw = args.input.read_bytes()
        provenance = {"mode": "local_file", "doi": DOI, "input_name": args.input.name}
    loci, populations = parse_genepop(raw)
    crosswalk = read_map(args.population_map, len(populations)) if args.population_map else None
    report = analyse(raw, provenance, crosswalk)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    print(f"{report['status']} | n={report['n_individuals']} | loci={len(loci)} | pop={len(populations)}")
    print(f"report={args.out}")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, UnicodeError, urllib.error.URLError, zipfile.BadZipFile) as exc:
        print(f"DATA_NOT_ANALYZED: {exc}", file=sys.stderr)
        sys.exit(2)
