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


def _fetch_bounded(url: str, maximum: int) -> bytes:
    req = urllib.request.Request(
        url, headers={"User-Agent": "MLTR-Genepop-audit/0.2 (research)"}
    )
    with urllib.request.urlopen(req, timeout=45) as response:
        raw = response.read(maximum + 1)
    if len(raw) > maximum:
        raise ValueError("download exceeds bounded maximum size")
    return raw


def _fetch_public_file_streams() -> tuple[bytes, bytes | None, dict[str, Any]]:
    """Fallback for a published dataset when the ZIP endpoint requires auth.

    The file list is discovered through Dryad's public metadata API, never from
    guessed IDs or a search-index snippet. A source checksum is honored if present.
    """
    root = "https://datadryad.org"
    dataset_api = root + "/api/v2/datasets/doi%3A10.5061%2Fdryad.tb2rbp03j"
    dataset = json.loads(_fetch_bounded(dataset_api, 200_000))
    if dataset.get("identifier") != "doi:" + DOI:
        raise ValueError("Dryad dataset metadata DOI mismatch")
    versions_href = dataset.get("_links", {}).get("stash:version", {}).get("href")
    if not isinstance(versions_href, str):
        raise ValueError("no pinned latest published version URL in metadata")
    version_path = re.fullmatch(r"/api/v2/versions/([0-9]+)", versions_href)
    if version_path is None:
        raise ValueError("unsafe/unexpected Dryad latest version URL")
    version_id = int(version_path.group(1))
    listing_url = f"{root}/api/v2/versions/{version_id}/files?per_page=100"
    listing = json.loads(_fetch_bounded(listing_url, 200_000))
    files = listing.get("_embedded", {}).get("stash:files", [])
    if not isinstance(files, list) or len(files) >= 100:
        raise ValueError("file listing empty/ambiguous or truncated")
    def find_exact(basename: str) -> dict[str, Any] | None:
        hits = [f for f in files if Path(str(f.get("path", ""))).name == basename]
        if len(hits) > 1:
            raise ValueError("multiple source files with identical basename")
        return hits[0] if hits else None
    focal = find_exact(TARGET)
    if focal is None:
        raise ValueError("source Genepop absent in pinned version file list")
    readme_record = find_exact("README.txt")
    def file_id(record: dict[str, Any]) -> int:
        """File listings may expose the ID through their HAL self link, not id."""
        if "id" in record:
            fid = int(record["id"])
            if fid > 0:
                return fid
        links = record.get("_links", {})
        for key in ("self", "stash:download"):
            href = links.get(key, {}).get("href", "")
            match = re.fullmatch(
                r"(?:https://datadryad\.org)?/api/v2/files/([0-9]+)(?:/download)?",
                href,
            )
            if match and int(match.group(1)) > 0:
                return int(match.group(1))
        raise ValueError("Dryad file lacks valid ID/self link; cannot fetch")

    def download(record: dict[str, Any], max_size: int) -> bytes:
        fid = file_id(record)
        raw = _fetch_bounded(f"{root}/downloads/file_stream/{fid}", max_size)
        size = record.get("size")
        if size is not None and int(size) != len(raw):
            raise ValueError("Dryad file size did not match metadata")
        digest = record.get("digest")
        digest_type = str(record.get("digestType", "")).lower().replace("-", "")
        if digest and digest_type in ("md5", "sha256"):
            if hashlib.new(digest_type, raw).hexdigest().lower() != str(digest).lower():
                raise ValueError("Dryad file digest mismatch")
        return raw
    genotype = download(focal, 3_000_000)
    readme = download(readme_record, 300_000) if readme_record else None
    return genotype, readme, {
        "mode": "dryad_public_file_stream",
        "doi": DOI,
        "dataset_api": dataset_api,
        "version_id": version_id,
        "genepop_file_id": file_id(focal),
        "readme_file_id": file_id(readme_record) if readme_record else None,
    }


def fetch_dryad() -> tuple[bytes, bytes | None, dict[str, Any]]:
    """Try official ZIP once, then the published file metadata/stream path on 401."""
    try:
        raw = _fetch_bounded(API_ZIP, MAX_ZIP_BYTES)
    except urllib.error.HTTPError as error:
        if error.code not in (401, 403):
            raise
        return _fetch_public_file_streams()
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
        parsed = [allele_pair(token) for token in tokens]
        # Dryad C. maritimum uses a repeated *population* code for every
        # individual row, not a unique individual identifier.
        if any(name == other_name and parsed == other_g
               for other_name, other_g in populations[-1]):
            raise ValueError(f"identical sample-label/genotype row within POP: {name!r}")
        populations[-1].append((name, parsed))
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
    duplicates = sorted(sample_id for sample_id, blocks in seen.items() if len(set(blocks)) > 1)
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



SOURCE_LABELS = {
    "C1-1": ("Awaji Island", "2007", False, "past_wild"),
    "C1-2": ("Awaji Island", "2019", False, "current_wild"),
    "C1-3": ("Awaji Island", "2000", True, "ex_situ"),
    "C1-4": ("Awaji Island", "2014", True, "ex_situ"),
    "C2": ("Shizuoka Prefecture", "2019", False, "geographic_comparator"),
    "C3": ("Mie Prefecture", "2019", False, "geographic_comparator"),
    "C4": ("Wakayama Prefecture", "2019", False, "geographic_comparator"),
}


def verify_source_labels(
    readme: bytes, populations: list[list[tuple[str, list[tuple[str, str] | None]]]]
) -> list[str]:
    """Independent README crosswalk: POP position never defines sample history."""
    txt = readme.decode("utf-8-sig")
    if "4. Sample information" not in txt or "Cirsium maritimum" not in txt:
        raise ValueError("missing README sample information/source species")
    section = txt.split("4. Sample information", 1)[1].split("Linaria japonica", 1)[0]
    code_lines = {}
    for line in section.splitlines():
        match = re.match(r"^\s*(C1-[1-4]|C[234]):\s*(.+)$", line)
        if match:
            if match.group(1) in code_lines:
                raise ValueError("duplicated source code in README")
            code_lines[match.group(1)] = match.group(2)
    if set(code_lines) != set(SOURCE_LABELS):
        raise ValueError("README sample codes differ from the frozen Cirsium contract")
    for label, (site, year, ex_situ, _) in SOURCE_LABELS.items():
        description = code_lines[label]
        if site not in description or year not in description:
            raise ValueError(f"README site/year conflict for {label}")
        if ("ex situ conserved" in description) != ex_situ:
            raise ValueError(f"README ex-situ status conflict for {label}")
    labels = []
    for index, pop in enumerate(populations, 1):
        observed = {sample_label for sample_label, _ in pop}
        if len(observed) != 1:
            raise ValueError(f"source POP block {index} mixes different group labels")
        labels.append(next(iter(observed)))
    if len(labels) != len(SOURCE_LABELS) or set(labels) != set(SOURCE_LABELS):
        raise ValueError("source population codes missing, duplicated or outside README")
    return labels


def source_verified_analysis(raw: bytes, readme: bytes, provenance: dict[str, Any]) -> dict:
    """Descriptive genomic inventory; source history from verified README only."""
    loci, populations = parse_genepop(raw)
    labels = verify_source_labels(readme, populations)
    report = analyse(raw, {**provenance, "readme_sha256": sha256(readme)})
    profs = {label: profile(loci, pop) for label, pop in zip(labels, populations)}
    report["source_crosswalk"] = [
        {"pop_index": i, "sample_code": label,
         "sample_row_identity": "POP index + row index; original code repeats",
         "site": SOURCE_LABELS[label][0], "collection_year": int(SOURCE_LABELS[label][1]),
         "conservation_status": SOURCE_LABELS[label][3],
         "n_individuals": len(populations[i-1])}
        for i, label in enumerate(labels, 1)
    ]
    for row, label in zip(report["populations"], labels):
        row["source_code"] = label
        row["source_status"] = SOURCE_LABELS[label][3]

    def observed(label: str) -> set[tuple[str, str]]:
        return {(locus, allele)
                for locus, alleles in profs[label]["_alleles"].items()
                for allele in alleles}

    old = observed("C1-1")
    current = observed("C1-2")
    ex2000 = observed("C1-3")
    ex2014 = observed("C1-4")
    old_not_current = old - current
    only_at_current = current - old
    old_called = profs["C1-1"]["locus_call_counts"]
    current_called = profs["C1-2"]["locus_call_counts"]
    if any(current_called[locus] == 0 for locus, allele in old_not_current):
        # An allele cannot be called "not detected in contemporary sampling"
        # without at least one contemporary observation at its locus.
        raise ValueError("old/new allele contrast contains unobserved current loci")
    thresholds = {}
    for threshold in (1, 2, 4, 6, 8):
        thresholds[str(threshold)] = sum(
            current_called[locus] >= threshold and old_called[locus] >= 1
            for locus, _allele in old_not_current
        )
    all_old_both_called = {
        locus for locus in loci if old_called[locus] == len(populations[labels.index("C1-1")])
    }
    current_all_called = {
        locus for locus in loci if current_called[locus] == len(populations[labels.index("C1-2")])
    }
    report["observed_allele_contrasts"] = {
        "comparison": "C1-1 2007 Awaji wild vs C1-2 2019 Awaji wild",
        "past_sample_n": len(populations[labels.index("C1-1")]),
        "current_sample_n": len(populations[labels.index("C1-2")]),
        "past_alleles_not_observed_current": len(old_not_current),
        "current_alleles_not_observed_past": len(only_at_current),
        "past_not_current_observed_in_ex_situ_2000_C1-3": len(old_not_current & ex2000),
        "past_not_current_observed_in_ex_situ_2014_C1-4": len(old_not_current & ex2014),
        "past_not_current_observed_in_any_ex_situ": len(old_not_current & (ex2000 | ex2014)),
        "past_not_current_observed_in_both_ex_situ": len(old_not_current & ex2000 & ex2014),
        "past_not_current_not_observed_in_either_ex_situ": len(old_not_current - (ex2000 | ex2014)),
        "old_both_individuals_called_loci": len(all_old_both_called),
        "old_both_and_all_current_called_loci": len(all_old_both_called & current_all_called),
        "old_not_current_alleles_by_min_current_called_individuals": thresholds,
        "status": "OBSERVED_ALLELE_NONDETECTION_NOT_EXTINCTION",
    }

    # Exhaustive, exact sample-size sensitivity (2 historical vs each of
    # the 8-choose-2 = 28 contemporary pairs); each pair uses only loci called
    # in all four individuals. Pair combinations are dependent, not replicates.
    historic = populations[labels.index("C1-1")]
    contemporary = populations[labels.index("C1-2")]
    if len(historic) != 2 or len(contemporary) != 8:
        raise ValueError("source-specific sensitivity expects historic n=2/current n=8")
    from itertools import combinations
    pair_loci = []
    paired_deltas = []
    for ids in combinations(range(len(contemporary)), 2):
        current_pair = [contemporary[k][1] for k in ids]
        n_eligible = 0
        delta_alleles = 0
        for index in range(len(loci)):
            old_calls = [genos[index] for _id, genos in historic]
            new_calls = [genos[index] for genos in current_pair]
            if any(call is None for call in old_calls + new_calls):
                continue
            n_eligible += 1
            old_alleles = set(old_calls[0] + old_calls[1])
            new_alleles = set(new_calls[0] + new_calls[1])
            delta_alleles += len(new_alleles) - len(old_alleles)
        if n_eligible < 1:
            raise ValueError("no mutually complete loci for a 2-vs-2 comparison")
        pair_loci.append(n_eligible)
        paired_deltas.append(delta_alleles / n_eligible)
    report["sample_size_and_missingness_sensitivity"] = {
        "protocol": "all 28 current n=2 pairs vs original historical n=2; only mutually fully called loci",
        "n_comparisons_nonindependent": len(paired_deltas),
        "number_fully_called_loci_min": min(pair_loci),
        "number_fully_called_loci_max": max(pair_loci),
        "mean_current_minus_past_alleles_per_called_locus": round(sum(paired_deltas)/len(paired_deltas), 8),
        "n_current_pair_more_diverse": sum(delta > 0 for delta in paired_deltas),
        "n_current_pair_less_diverse": sum(delta < 0 for delta in paired_deltas),
        "n_equal": sum(delta == 0 for delta in paired_deltas),
        "status": "DESCRIPTIVE_SENSITIVITY_NOT_INDEPENDENT_STATISTICAL_REPLICATES",
    }
    report["status"] = "REAL_SOURCE_QC_COMPLETE_RESPONSE_LINK_MISSING"
    report["limitations"].extend([
        "Historical Awaji population has only two individuals; unequal sampling and locus dropout prevent a loss/extinction claim.",
        "Repeated C1 sample codes are group codes, not duplicate individual identifiers.",
        "Exact 28 paired subsets are highly dependent and cannot be treated as 28 independent replicates.",
        "An ex-situ group reflects a different sampled founder and propagation history; recovery of an allele does not establish its adaptive value.",
    ])
    return report


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    source = p.add_mutually_exclusive_group(required=True)
    source.add_argument("--input", type=Path, help="local original Genepop file")
    source.add_argument("--input-zip", type=Path, help="local original Dryad ZIP with Genepop and README")
    source.add_argument("--from-dryad", action="store_true", help="fetch public published ZIP")
    p.add_argument("--readme", type=Path, help="source README for local --input")
    p.add_argument("--population-map", type=Path, help="reviewed CSV: pop_index,group")
    p.add_argument("--out", type=Path, required=True, help="output JSON; no raw genotypes emitted")
    args = p.parse_args()
    if args.from_dryad:
        raw, readme, provenance = fetch_dryad()
    elif args.input_zip:
        zip_raw = args.input_zip.read_bytes()
        if len(zip_raw) > MAX_ZIP_BYTES:
            raise ValueError("uploaded ZIP exceeds bounded maximum size")
        with zipfile.ZipFile(io.BytesIO(zip_raw)) as archive:
            filenames = [Path(filename).name for filename in archive.namelist()]
            if filenames.count(TARGET) != 1 or filenames.count("README.txt") != 1:
                raise ValueError("source archive must contain one Cirsium Genepop and one README")
            file_name = archive.namelist()[filenames.index(TARGET)]
            readme_name = archive.namelist()[filenames.index("README.txt")]
            raw = archive.read(file_name)
            readme = archive.read(readme_name)
        provenance = {"mode": "uploaded_original_zip", "doi": DOI,
                      "zip_sha256": sha256(zip_raw), "zip_bytes": len(zip_raw)}
    else:
        raw = args.input.read_bytes()
        readme = args.readme.read_bytes() if args.readme else None
        provenance = {"mode": "local_file", "doi": DOI, "input_name": args.input.name}
    if readme is not None and args.population_map:
        raise ValueError("README-verified exact population map and generic map must not be mixed")
    if readme is not None:
        report = source_verified_analysis(raw, readme, provenance)
    else:
        loci, populations = parse_genepop(raw)
        crosswalk = read_map(args.population_map, len(populations)) if args.population_map else None
        report = analyse(raw, provenance, crosswalk)
    loci, populations = parse_genepop(raw)
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
