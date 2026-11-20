#!/usr/bin/env python3
"""Source-locked reanalysis of user-provided original 2019 Arabidopsis drought CSV.

Important: source is original Dryad file as SUPPLIED BY USER; file hash is
locally pinned, not independently authenticated by a Dryad byte download.
Related course CSV is a superset of 759 measured original rows + 120 from six
extra accessions (the one missing original fruit row is not in that mirror).

No SNP/whole-genome genotypes; 'accession' is a categorical genetic lineage.
No raw individual observations are ever written to the aggregate report.
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

from audit_arabidopsis_factorial_response import (
    score_folds, get_public_csv, checksum as verify_course
)
from audit_arabidopsis_action_decision_value import evaluate_policy

DOI = "10.5061/dryad.334765v"
SOURCE_FILE = "full_data_drought.csv"
SOURCE_SHA256 = "13ca229e6c97ee1a6d0333e4d32a66dabbf30a99e824a14c6f32bacad23067e3"
SOURCE_BYTES = 21391
SOURCE_FIELDS = ("accession","water","microbe","replicate","tray",
                 "shelf","rack","fruit","flowering","counter","source")
COMMON = SOURCE_FIELDS[:-1]
ACTIONS = ("D|L","D|S","W|L","W|S")
RACKS = ("1","2","3","4","5")
COURSE_SHA256 = "5872c228388bd6422458fa6f65a15e59e0ea283973ead376f5d3f7cd47ee485c"
EXPECTED_ORIGINAL_CALLED_CANON_SHA256 = (
    "d84f3b4a78c1d65860c9d9f5b14afbd09b05a16f734bae6237f34d6e3767fe8f"
)


def read_original(raw:bytes, strict:bool=True):
    raw_hash = hashlib.sha256(raw).hexdigest()
    if strict and (len(raw) != SOURCE_BYTES or raw_hash != SOURCE_SHA256):
        raise ValueError("original 2019 Dryad CSV does not match pinned uploaded bytes")
    with io.StringIO(raw.decode("utf-8-sig"), newline="") as handle:
        reader=csv.DictReader(handle)
        if tuple(reader.fieldnames or ()) != SOURCE_FIELDS:
            raise ValueError("unexpected original Dryad column order/schema")
        source_rows=list(reader)
    if not source_rows:
        raise ValueError("no rows in original source")
    seen=Counter()
    source_counts=Counter()
    accession_counts=Counter()
    missing=0
    records=[]
    for i,row in enumerate(source_rows,2):
        accession=row["accession"].strip()
        water=row["water"].strip()
        microbe=row["microbe"].strip()
        rack=row["rack"].strip()
        rep=row["replicate"].strip()
        if not accession or water not in ("D","W") or microbe not in ("L","S"):
            raise ValueError(f"invalid accession/treatment on row {i}")
        if rack not in RACKS or rack != rep:
            raise ValueError(f"rack differs from replicate at row {i}")
        if row["source"] not in ("ut","abrc"):
            raise ValueError("unexpected seed-stock source")
        key=(accession,water,microbe,rack)
        seen[key]+=1
        accession_counts[accession]+=1
        source_counts[row["source"]]+=1
        text=row["fruit"].strip()
        if not text or text=="NA":
            missing+=1
            continue
        try:
            fruit=float(text)
        except ValueError as exc:
            raise ValueError(f"invalid fruit count at row {i}") from exc
        if not math.isfinite(fruit) or fruit < 0 or fruit != int(fruit):
            raise ValueError(f"invalid noninteger/negative fruit count at row {i}")
        records.append({
            "accession":accession,"action":water+"|"+microbe,
            "replicate":rack,"value":math.sqrt(fruit),"fruit":int(fruit)
        })
    if any(v!=1 for v in seen.values()):
        raise ValueError("source contains duplicate accession/treatment/rack assignment")
    if strict:
        if (len(source_rows)!=760 or len(accession_counts)!=38
                or any(v!=20 for v in accession_counts.values())
                or len(seen)!=760 or missing!=1 or len(records)!=759):
            raise ValueError("original published 38×4×5 source contract has changed")
        if {x[1]+"|"+x[2] for x in seen} != set(ACTIONS):
            raise ValueError("source missing one treatment condition")
    profile={
        "uploaded_source_sha256":raw_hash,
        "uploaded_source_bytes":len(raw),
        "records_design":len(source_rows),
        "records_observed_fruit":len(records),
        "records_fruit_missing":missing,
        "n_accessions":len(accession_counts),
        "per_accession_design_sizes":dict(sorted(Counter(accession_counts.values()).items())),
        "n_unique_accession_action_rack_cells":len(seen),
        "stock_source_counts":dict(sorted(source_counts.items())),
        "rack_design_sizes":dict(sorted(Counter(k[3] for k in seen).items())),
        "action_design_sizes":dict(sorted(Counter(k[1]+"|"+k[2] for k in seen).items())),
        "action_usable_sizes":dict(sorted(Counter(r["action"] for r in records).items())),
        "zero_fruit_observations":sum(r["fruit"]==0 for r in records),
        "status":"USER_UPLOADED_ORIGINAL_CSV_HASH_PINNED; NOT_INDEPENDENT_DRYAD_BYTE_VERIFIED",
    }
    return source_rows, records, profile


def canonical_calls(rows, columns=COMMON):
    """Non-identifying canonical check against the course mirror at same rows."""
    def canon(row):
        return "\t".join(
            (row[c].strip() if row[c].strip()!="NA" else "")
            for c in columns
        )
    return sorted(
        canon(row) for row in rows
        if row["fruit"].strip() not in ("","NA")
    )


def compare_course(original_rows, teaching_raw:bytes):
    course_profile=verify_course(teaching_raw)
    if course_profile["sha256"] != COURSE_SHA256:
        raise ValueError("teaching mirror changed unexpectedly")
    with io.StringIO(teaching_raw.decode("utf-8-sig"), newline="") as handle:
        reader=csv.DictReader(handle)
        if tuple(reader.fieldnames or ()) != COMMON:
            raise ValueError("teaching-mirror field mismatch")
        course=list(reader)
    source_ids={r["accession"] for r in original_rows}
    matched=[r for r in course if r["accession"] in source_ids]
    extra=[r for r in course if r["accession"] not in source_ids]
    original_norm=canonical_calls(original_rows)
    mirror_norm=canonical_calls(matched)
    if original_norm!=mirror_norm:
        raise ValueError("original and education mirror record content differ")
    if len(matched)!=759 or len(extra)!=120 or len({x["accession"] for x in extra})!=6:
        raise ValueError("education-source extra accession census failed")
    canonical_text="\n".join(original_norm)+"\n"
    canon_hash=hashlib.sha256(canonical_text.encode("utf-8")).hexdigest()
    if canon_hash != EXPECTED_ORIGINAL_CALLED_CANON_SHA256:
        raise ValueError("original subset canonical source hash mismatch")
    return {
        "status":"ALL_759_CALLED_ORIGINAL_ROWS_MATCH_COURSE_MIRROR",
        "course_sha256":course_profile["sha256"],
        "original_usable_records":len(original_norm),
        "original_missing_fruit_records_absent_course":len(original_rows)-len(original_norm),
        "additional_course_records":len(extra),
        "additional_course_accession_count":len({r["accession"] for r in extra}),
        "canonical_common_10_column_sha256":canon_hash,
        "source_interpretation":"teaching mirror contains observed original subset plus six extra accessions; not independent replication",
    }


def analyse(original_bytes:bytes, course_bytes:bytes|None=None):
    original_rows, records, qc = read_original(original_bytes)
    model=score_folds(records,10.0,10.0,bootstrap=2000)
    centered=score_folds(
        records,10.0,10.0,bootstrap=2000,center_action=True
    )
    small=score_folds(records,5.0,5.0,bootstrap=250)
    large=score_folds(records,20.0,20.0,bootstrap=250)
    decision=evaluate_policy(records,pseudo=10.0,bootstrap_draws=2000)
    crosswalk=(compare_course(original_rows,course_bytes)
               if course_bytes is not None else {
                   "status":"COURSE_MIRROR_NOT_REOPENED_IN_THIS_EXECUTION",
                   "matching_759_record_subset_previously_checked_independently":True
               })
    return {
        "source":{
            "doi":DOI,"filename":SOURCE_FILE,
            "file_sha256":qc["uploaded_source_sha256"],
            "bytes":qc["uploaded_source_bytes"],
            "original_dryad_download_byte_hash_independently_verified":False
        },
        "qc":qc,
        "course_subset_crosswalk":crosswalk,
        "heldout_rack_prediction":{
            "primary_original_specification":model,
            "post_result_centered_action_only_sensitivity":centered,
            "shrinkage_sensitivity_fixed_in_previous_course_audit":{
                "k5":small,
                "k20":large
            },
        },
        "heldout_action_decision":decision,
        "status":"ORIGINAL_38_ACCESSIONS_PREDICTION_SUPPORTED_DECISION_VALUE_NOT_SUPPORTED",
        "scope_limits":[
            "Original 38 accessions and 759 observed fruit records are a subset of the earlier educational 44-accession/879-record source, not independent biological replication.",
            "The original 760th record has missing fruit; not imputed and its incomplete four-action panel excluded from decision-value calculation.",
            "Accession identifiers are not SNP genotypes or molecular markers.",
            "Original published genotype-by-environment associations are prior art.",
            "Prediction uses already known accession IDs in held-out racks, not unseen accession transfer.",
            "The centered P2 treatment-only analysis is post-result and its interval can include zero.",
            "Actions are laboratory treatment assignments with equal utility cost assumed, not validated field management.",
            "No source-target replacement relation, carried-label history, or exact MLTR decision-sufficiency theorem tested.",
        ],
    }


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input",required=True,type=Path,
                        help="uploaded source full_data_drought.csv (not committed)")
    parser.add_argument("--course",type=Path,
                        help="optional exact University of Toronto teaching CSV")
    parser.add_argument("--compare-course-public",action="store_true",
                        help="download/verify exact public teaching mirror for row crosswalk")
    parser.add_argument("--out",required=True,type=Path)
    args=parser.parse_args()
    if args.course and args.compare_course_public:
        parser.error("choose only one course-source pathway")
    course=(args.course.read_bytes() if args.course else
            get_public_csv() if args.compare_course_public else None)
    report=analyse(args.input.read_bytes(),course)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({
        "source_sha256":report["source"]["file_sha256"],
        "n_fruit":report["qc"]["records_observed_fruit"],
        "n_accessions":report["qc"]["n_accessions"],
        "course_crosswalk":report["course_subset_crosswalk"]["status"],
        "heldout_mse":report["heldout_rack_prediction"]["primary_original_specification"]["heldout_mse"],
        "P2_P1_predictive_gain":report["heldout_rack_prediction"]["primary_original_specification"]["mean_gain_P2_minus_P1"],
        "P2_P1_centered_gain":report["heldout_rack_prediction"]["post_result_centered_action_only_sensitivity"]["mean_gain_P2_minus_P1"],
        "decision_value":report["heldout_action_decision"]["mean_gain_sqrt_fruit_per_panel"],
        "decision_gate":report["heldout_action_decision"]["status"],
    },sort_keys=True))


if __name__=="__main__":
    main()
