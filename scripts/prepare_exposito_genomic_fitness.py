#!/usr/bin/env python3
"""Authenticate and join the frozen Exposito-Alonso 2019 prediction sources.

The output contains published accession summaries, not reconstructed independent
plant observations. No response transformation, imputation, pot deduplication,
feature selection, or model fitting is performed here. Source readers require
openpyxl and rdata; the record-level admission function requires only NumPy.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import math
import platform
from importlib.metadata import version
from pathlib import Path

import numpy as np


CONTEXTS = ("mhi", "mhp", "mli", "mlp", "thi", "thp", "tli", "tlp")
ARRAY_KEYS = ("ids", "coords", "distance", "fitness", "contexts")
D2_HEADERS = ("id", "name", "country", "latitude", "longitude")
D4_HEADERS = (
    "id", "site", "water", "indpop", "Germination_time", "Green", "Red",
    "Survival_flowering", "Flowering_time", "Inflorescence_size",
    "Survival_num", "Survival_fruit", "Fruits", "Seeds", "Infloresncence_byind",
    "Fruits_byind", "Seeds_byind", "Fitness",
)
SOURCE_FILES = (
    {
        "name": "S_DATASETS.xlsx",
        "bytes": 3725000,
        "sha256": "032045433e3ace035977c11ff5d0ae8731335e8210c6cee14d64575ae0bebd05",
        "url": "https://ndownloader.figshare.com/files/17131214",
    },
    {
        "name": "ibs1001g.rda",
        "bytes": 8947948,
        "sha256": "906724ce620a30a8c199ade07c5ffaa27aa7b1a91e8229f63b27e882547a70ad",
        "url": "https://raw.githubusercontent.com/MoisesExpositoAlonso/dryAR/"
               "ddf703c91a01a990b8041f0aea9c94de119cd60b/data-cleaning/ibs1001g.rda",
    },
)


def verify_source_bytes(raw, *, expected_sha256, expected_size, label):
    """Reject altered input bytes before any source parser sees them."""
    if len(raw) != expected_size:
        raise ValueError(f"{label}: source size mismatch")
    if hashlib.sha256(raw).hexdigest() != expected_sha256:
        raise ValueError(f"{label}: source hash mismatch")


def _identifier(value):
    if isinstance(value, (bool, np.bool_)) or value is None:
        raise ValueError("invalid accession ID")
    try:
        number = int(value)
        if number <= 0 or float(value) != number:
            raise ValueError
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(f"invalid accession ID: {value!r}") from exc
    return str(number)


def _axis_ids(values, label):
    result = [_identifier(value) for value in values]
    if not result or len(result) != len(set(result)):
        raise ValueError(f"empty or duplicate genetic {label} accession IDs")
    return result


def _context(record):
    try:
        site = {"madrid": "m", "tuebingen": "t"}[record["site"]]
        context = site + record["water"] + record["indpop"]
    except (KeyError, TypeError) as exc:
        raise ValueError("invalid source context key") from exc
    if context not in CONTEXTS:
        raise ValueError(f"invalid source context key: {context!r}")
    return context


def prepare_from_records(accessions, summaries, row_ids, column_ids, distance_matrix):
    """Join explicit source labels and return the five arrays and an audit.

    Missing response contexts exclude the accession; measured zeros survive.
    Duplicate records and malformed measurements are errors, even if resolving
    or dropping them would leave a complete cohort. Genetic axes may arrive in
    different orders, but their unique label sets must match exactly.
    """
    metadata = {}
    for record in accessions:
        identifier = _identifier(record["id"])
        if identifier in metadata:
            raise ValueError(f"duplicate accession metadata: {identifier}")
        try:
            latitude = float(record["latitude"])
            longitude = float(record["longitude"])
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError(f"invalid coordinate for accession {identifier}") from exc
        if not (math.isfinite(latitude) and math.isfinite(longitude)
                and -90 <= latitude <= 90 and -180 <= longitude <= 180):
            raise ValueError(f"invalid coordinate for accession {identifier}")
        metadata[identifier] = {
            "name": str(record.get("name", "")),
            "coords": (latitude, longitude),
        }

    fitness_by_key = {}
    observed_keys = set()
    summary_count = 0
    for record in summaries:
        summary_count += 1
        identifier = _identifier(record["id"])
        if identifier not in metadata:
            raise ValueError(f"summary accession absent from D2 metadata: {identifier}")
        context = _context(record)
        key = (identifier, context)
        if key in observed_keys:
            raise ValueError(f"duplicate accession-context summary: {key}")
        observed_keys.add(key)
        raw = record["Fitness"]
        if raw is None:
            continue
        try:
            value = float(raw)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"invalid Fitness for {key}") from exc
        if math.isnan(value):
            continue
        if not math.isfinite(value) or value < 0:
            raise ValueError(f"invalid Fitness for {key}")
        fitness_by_key[key] = value

    rows = _axis_ids(row_ids, "row")
    columns = _axis_ids(column_ids, "column")
    if set(rows) != set(columns):
        raise ValueError("genetic row and column accession sets differ")
    distance = np.asarray(distance_matrix, dtype=np.float64)
    if distance.shape != (len(rows), len(columns)):
        raise ValueError("genetic distance shape does not match labelled axes")
    column_index = {identifier: index for index, identifier in enumerate(columns)}
    distance = distance[:, [column_index[identifier] for identifier in rows]]
    if not np.isfinite(distance).all() or np.any(distance < 0):
        raise ValueError("genetic distance must be finite and nonnegative")
    if not np.array_equal(distance, distance.T):
        raise ValueError("genetic distance is not exactly symmetric after labelled alignment")
    if np.any(np.diag(distance) != 0):
        raise ValueError("genetic distance diagonal is not zero")

    row_index = {identifier: index for index, identifier in enumerate(rows)}
    eligible = []
    excluded = []
    complete_count = 0
    for identifier in sorted(metadata, key=int):
        missing = [context for context in CONTEXTS
                   if (identifier, context) not in fitness_by_key]
        complete_count += not missing
        reasons = []
        if identifier not in row_index:
            reasons.append("missing_genetic_distance")
        if missing:
            reasons.append("incomplete_contexts")
        if reasons:
            excluded.append({"id": identifier, "name": metadata[identifier]["name"],
                             "reasons": reasons, "missing_contexts": missing})
        else:
            eligible.append(identifier)
    if not eligible:
        raise ValueError("no accession satisfies the complete source contract")
    indices = [row_index[identifier] for identifier in eligible]
    admitted_distance = distance[np.ix_(indices, indices)]
    if np.any(np.triu(admitted_distance == 0, k=1)):
        raise ValueError("off-diagonal zero distance in admitted cohort")

    arrays = {
        "ids": np.array(eligible, dtype=str),
        "coords": np.array([metadata[identifier]["coords"] for identifier in eligible],
                           dtype=np.float64),
        "distance": admitted_distance,
        "fitness": np.array([[fitness_by_key[(identifier, context)] for context in CONTEXTS]
                             for identifier in eligible], dtype=np.float64),
        "contexts": np.array(CONTEXTS, dtype=str),
    }
    audit = {
        "schema_version": 1,
        "n_accessions": len(eligible),
        "n_contexts": len(CONTEXTS),
        "n_response_cells": int(arrays["fitness"].size),
        "contexts": list(CONTEXTS),
        "cohort_ids_sha256": hashlib.sha256(("\n".join(eligible) + "\n").encode()).hexdigest(),
        "source_record_counts": {"D2_accessions": len(metadata),
                                 "D4_summaries": summary_count,
                                 "genetic_distance_accessions": len(rows),
                                 "D2_with_genetic_distance": len(set(metadata) & set(rows)),
                                 "D2_with_complete_fitness_contexts": complete_count},
        "excluded_accessions": excluded,
        "zero_response_cells_preserved": int(np.count_nonzero(arrays["fitness"] == 0)),
        "distance_qc": {"source_shape": list(distance.shape),
                        "row_column_source_order_identical": rows == columns,
                        "aligned_by_explicit_ids": True, "finite_nonnegative": True,
                        "exactly_symmetric": True, "diagonal_zero": True,
                        "admitted_offdiagonal_zero_pairs": 0},
        "array_contract": {"keys": list(ARRAY_KEYS), "id_order": "numeric ascending",
                           "coordinate_order": ["latitude", "longitude"],
                           "coordinate_source": "final D2_accessions",
                           "fitness_source": "untransformed final D4_datsummary Fitness",
                           "distance_source": "author R object kkk, explicit ID axes"},
        "processing": {"response_transformation": False, "imputation": False,
                       "D3_deduplication": False, "model_fitting": False},
    }
    return arrays, audit


def _sheet_records(workbook, sheet_name, expected_headers):
    rows = workbook[sheet_name].iter_rows(min_row=4, values_only=True)
    headers = tuple(next(rows))
    if headers != expected_headers:
        raise ValueError(f"unexpected headers in {sheet_name}: {headers!r}")
    records = []
    for row in rows:
        if all(value is None for value in row):
            continue
        if len(row) != len(headers) or row[0] is None:
            raise ValueError(f"malformed source row in {sheet_name}")
        records.append(dict(zip(headers, row)))
    return records


def load_sources(workbook_path, ibs_path):
    """Parse only authenticated original bytes; no unpinned source mode exists."""
    raw_sources = []
    for path, record in zip((workbook_path, ibs_path), SOURCE_FILES):
        raw = Path(path).read_bytes()
        verify_source_bytes(raw, expected_sha256=record["sha256"],
                            expected_size=record["bytes"], label=record["name"])
        raw_sources.append(raw)

    import openpyxl
    import rdata

    workbook = openpyxl.load_workbook(io.BytesIO(raw_sources[0]), read_only=True, data_only=True)
    try:
        accessions = _sheet_records(workbook, "D2_accessions", D2_HEADERS)
        summaries = _sheet_records(workbook, "D4_datsummary", D4_HEADERS)
    finally:
        workbook.close()
    objects = rdata.conversion.convert(rdata.parser.parse_data(raw_sources[1]),
                                       default_encoding="utf-8")
    genetic = objects.get("kkk")
    if genetic is None or not all(hasattr(genetic, attr) for attr in ("index", "columns", "to_numpy")):
        raise ValueError("R object kkk must have explicit row and column accession labels")
    arrays, audit = prepare_from_records(accessions, summaries, genetic.index, genetic.columns,
                                        genetic.to_numpy(dtype=float))
    expected = {"D2_accessions": 517, "D4_summaries": 4135,
                "genetic_distance_accessions": 1135, "D2_with_genetic_distance": 515,
                "D2_with_complete_fitness_contexts": 516}
    if audit["source_record_counts"] != expected or audit["n_accessions"] != 514:
        raise ValueError("authenticated source parsing disagrees with the frozen cohort counts")
    audit["source_files"] = [dict(record) for record in SOURCE_FILES]
    audit["software_versions"] = {"python": platform.python_version(), "numpy": np.__version__,
                                  "openpyxl": version("openpyxl"), "rdata": version("rdata")}
    audit["target_scope"] = (
        "Published estimated seed output per planted seed, aggregated by accession and context. "
        "Shared calibration and upstream summary uncertainty are not validated here. "
        "The individual-pot table contains 360 repeated physical-pot keys with conflicting "
        "outcomes (375 extra rows); this loader uses the final published D4 summaries without "
        "deduplicating D3 or claiming independent plant-level reconstruction."
    )
    return arrays, audit


def write_outputs(arrays, audit, npz_path, audit_path):
    """Bind a compact audit to the exact written prepared-array file."""
    if set(arrays) != set(ARRAY_KEYS):
        raise ValueError("prepared array keys differ from the source contract")
    npz_path, audit_path = Path(npz_path), Path(audit_path)
    if npz_path.resolve() == audit_path.resolve():
        raise ValueError("NPZ and audit paths must differ")
    npz_path.parent.mkdir(parents=True, exist_ok=True)
    audit_path.parent.mkdir(parents=True, exist_ok=True)
    with npz_path.open("wb") as handle:
        np.savez_compressed(handle, **{key: arrays[key] for key in ARRAY_KEYS})
    written = dict(audit, prepared_npz_sha256=hashlib.sha256(npz_path.read_bytes()).hexdigest())
    audit_path.write_text(json.dumps(written, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    return written


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workbook", required=True, type=Path)
    parser.add_argument("--ibs", required=True, type=Path)
    parser.add_argument("--out-npz", required=True, type=Path)
    parser.add_argument("--out-audit", required=True, type=Path)
    args = parser.parse_args(argv)
    arrays, audit = load_sources(args.workbook, args.ibs)
    audit = write_outputs(arrays, audit, args.out_npz, args.out_audit)
    print(json.dumps({"n_accessions": audit["n_accessions"],
                      "n_response_cells": audit["n_response_cells"],
                      "prepared_npz_sha256": audit["prepared_npz_sha256"],
                      "npz": str(args.out_npz), "audit": str(args.out_audit)}, indent=2))


if __name__ == "__main__":
    main()
