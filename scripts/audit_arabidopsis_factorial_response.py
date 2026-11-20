#!/usr/bin/env python3
"""Explore accession×action fruit prediction in a public Arabidopsis teaching CSV.

This is a SOURCE-UNVERIFIED TEACHING MIRROR, not the authenticated 2019
publication's 38-accession/760-plant Dryad drought experiment.
Only accession ID (not genome variants), water, microbial inoculum and fruit
counts are available. Predictions use five replicate/rack-held-out blocks.
No specimen-level records or response vectors are emitted to results.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import random
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path

SOURCE_URL = "https://raw.githubusercontent.com/UofTCoders/rcourse/master/data/Fitzpatrick_2018.csv"
GIT_BLOB_SHA1 = "8a79d0a5aa9e21854a556cd63c4afc5af6199b1c"
ALLOWED_ACTIONS = {"D|L", "D|S", "W|L", "W|S"}
COLUMNS = ("accession", "water", "microbe", "replicate", "tray",
           "shelf", "rack", "fruit", "flowering", "counter")
EXPECTED_ROWS = 879
EXPECTED_ACCESSIONS = 44


def checksum(raw: bytes) -> dict:
    blob_header = b"blob " + str(len(raw)).encode("ascii") + b"\0"
    git_sha1 = hashlib.sha1(blob_header + raw).hexdigest()
    if git_sha1 != GIT_BLOB_SHA1:
        raise ValueError("unverified course CSV version: Git blob SHA-1 mismatch")
    return {"git_blob_sha1": git_sha1, "sha256": hashlib.sha256(raw).hexdigest(),
            "bytes": len(raw), "source_url": SOURCE_URL}


def get_public_csv() -> bytes:
    request = urllib.request.Request(SOURCE_URL, headers={
        "User-Agent": "MLTR-accession-response-audit/0.1",
        "Accept": "text/csv, text/plain",
    })
    with urllib.request.urlopen(request, timeout=30) as response:
        raw = response.read(70000)
    if len(raw) >= 70000:
        raise ValueError("CSV exceeds source-size guard")
    checksum(raw)
    return raw


def parse_source(raw: bytes, exact_source: bool = True):
    if exact_source:
        checksum(raw)
    with io.StringIO(raw.decode("utf-8-sig")) as handle:
        reader = csv.DictReader(handle)
        if tuple(reader.fieldnames or ()) != COLUMNS:
            raise ValueError("unexpected source CSV schema")
        rows = list(reader)
    records = []
    bad = Counter()
    seen = Counter()
    raw_actions, accession_counts, replicate_counts = Counter(), Counter(), Counter()
    for i, row in enumerate(rows, 2):
        genotype, water, microbe = (row[k].strip() for k in ("accession","water","microbe"))
        replicate, rack = row["replicate"].strip(), row["rack"].strip()
        if not genotype or water not in ("D","W") or microbe not in ("L","S"):
            raise ValueError(f"invalid lineage/action at source row {i}")
        if replicate not in ("1","2","3","4","5") or rack != replicate:
            raise ValueError(f"rack/replicate disagreement at source row {i}")
        try:
            fruit = float(row["fruit"])
        except (TypeError, ValueError) as exc:
            raise ValueError(f"invalid fruit at row {i}") from exc
        if not math.isfinite(fruit) or fruit < 0 or fruit != int(fruit):
            raise ValueError(f"noncount/negative fruit at row {i}")
        action = water + "|" + microbe
        key = (genotype,action,replicate)
        seen[key] += 1
        accession_counts[genotype] += 1
        replicate_counts[replicate] += 1
        raw_actions[action] += 1
        records.append({
            "accession": genotype,
            "action": action,
            "replicate": replicate,
            "value": math.sqrt(fruit),
            "fruit": int(fruit),
        })
        if row["flowering"].strip() in ("NA",""):
            bad["flowering_unobserved"] += 1
        bad["fruit_zero"] += fruit == 0
    if exact_source and (len(rows) != EXPECTED_ROWS
                         or len(accession_counts) != EXPECTED_ACCESSIONS
                         or set(raw_actions) != ALLOWED_ACTIONS
                         or set(replicate_counts) != {"1","2","3","4","5"}):
        raise ValueError("source counts do not match pinned education CSV")
    return records, {
        "n_rows":len(records), "n_accessions":len(accession_counts),
        "n_replicate_racks":len(replicate_counts),
        "action_counts":dict(sorted(raw_actions.items())),
        "replicate_counts":dict(sorted(replicate_counts.items())),
        "accession_observation_histogram":dict(sorted(Counter(accession_counts.values()).items())),
        "repeated_accession_action_replicate_assignments":sum(
            v-1 for v in seen.values() if v > 1
        ),
        "zero_fruit_records":int(bad["fruit_zero"]),
        "flowering_missing_but_fruit_retained":int(bad["flowering_unobserved"]),
        "interpretation": "teaching mirror accession label, not actual SNP genotype or authenticated publication data",
    }


def train_models(train, k_accession=10.0, k_action=10.0, center_action=False):
    if k_accession <= 0 or k_action <= 0:
        raise ValueError("shrinkage pseudocounts must be positive")
    action_y = defaultdict(list)
    for row in train:
        action_y[row["action"]].append(row["value"])
    if set(action_y) != ALLOWED_ACTIONS:
        raise ValueError("training lacks one of four action contexts")
    mu = {a: sum(values)/len(values) for a,values in action_y.items()}
    residuals = defaultdict(list)
    for row in train:
        residuals[row["accession"]].append(row["value"]-mu[row["action"]])
    acc = {g: sum(values)/(len(values)+k_accession)
           for g,values in residuals.items()}
    cells = defaultdict(list)
    for row in train:
        key = (row["accession"],row["action"])
        cells[key].append(row["value"]-mu[row["action"]]-acc[row["accession"]])
    cell = {key: sum(values)/(len(values)+k_action)
            for key,values in cells.items()}
    if center_action:
        # Post-result sensitivity: remove the part of P2 that can merely
        # compensate for over-shrinkage of P1's accession main effect.
        # Training-count weighted action offsets then sum to zero per genotype.
        for genotype in acc:
            matches=[(key, len(vals)) for key,vals in cells.items()
                     if key[0] == genotype]
            n=sum(nrows for _key,nrows in matches)
            if n <= 0:
                raise ValueError("no within-genotype actions to center")
            average=sum(cell[key]*nrows for key,nrows in matches)/n
            for key,_nrows in matches:
                cell[key]-=average
    return mu,acc,cell


def predict_one(row, fit):
    mu,acc,cell=fit
    if row["action"] not in mu or row["accession"] not in acc:
        raise ValueError("out-of-support accession/action cell in held-out block")
    base=mu[row["action"]]
    lineage=base+acc[row["accession"]]
    actionwise=lineage+cell.get((row["accession"],row["action"]),0.0)
    return {"P0":base, "P1":lineage,"P2":actionwise}


def quantile(values, q):
    v=sorted(values)
    p=(len(v)-1)*q
    low=int(p)
    high=min(low+1,len(v)-1)
    return v[low]*(1-(p-low))+v[high]*(p-low)


def score_folds(records, k_accession=10.0, k_action=10.0,
                bootstrap=2000, center_action=False):
    predictions=[]
    folds=[]
    for rack in ("1","2","3","4","5"):
        training=[row for row in records if row["replicate"] != rack]
        holdout=[row for row in records if row["replicate"] == rack]
        if not holdout or not training:
            raise ValueError("empty source holdout")
        model=train_models(training,k_accession,k_action,
                           center_action=center_action)
        fold_sums=Counter()
        for row in holdout:
            p=predict_one(row,model)
            se={k:(row["value"]-p[k])**2 for k in p}
            delta1=se["P0"]-se["P1"]
            delta2=se["P1"]-se["P2"]
            predictions.append((row["accession"],row["action"],rack,se,delta1,delta2))
            fold_sums["P0"]+=se["P0"];fold_sums["P1"]+=se["P1"];fold_sums["P2"]+=se["P2"]
            fold_sums["gain_P1_P0"]+=delta1;fold_sums["gain_P2_P1"]+=delta2
        folds.append({
            "rack_held_out":rack,
            "n":len(holdout),
            "MSE_P0":round(fold_sums["P0"]/len(holdout),8),
            "MSE_P1":round(fold_sums["P1"]/len(holdout),8),
            "MSE_P2":round(fold_sums["P2"]/len(holdout),8),
            "P1_minus_P0_gain":round(fold_sums["gain_P1_P0"]/len(holdout),8),
            "P2_minus_P1_gain":round(fold_sums["gain_P2_P1"]/len(holdout),8),
        })
    acc_deltas=defaultdict(list)
    act_deltas=defaultdict(list)
    sums=Counter()
    for accession,action,rack,se,delta1,delta2 in predictions:
        acc_deltas[accession].append(delta2)
        act_deltas[action].append(delta2)
        for m in ("P0","P1","P2"):
            sums[m]+=se[m]
        sums["gain_P1_P0"]+=delta1;sums["gain_P2_P1"]+=delta2
    accession_means=[sum(vals)/len(vals) for vals in acc_deltas.values()]
    rng=random.Random(20261119)
    resampled=[]
    for _ in range(bootstrap):
        sample=[accession_means[rng.randrange(len(accession_means))]
                for _ in accession_means]
        resampled.append(sum(sample)/len(sample))
    condition_gains={
        a:round(sum(v)/len(v),8) for a,v in sorted(act_deltas.items())
    }
    locus_gain=sums["gain_P2_P1"]/len(predictions)
    pop_mean=sum(accession_means)/len(accession_means)
    ci=[quantile(resampled,0.025),quantile(resampled,0.975)]
    positive_folds=sum(row["P2_minus_P1_gain"] >= 0 for row in folds)
    positive_contexts=sum(value > 0 for value in condition_gains.values())
    gate=(
        positive_folds==5 and pop_mean>0 and ci[0]>0
        and positive_contexts>=3
    )
    return {
        "model_specification": {
            "outcome":"square_root_fruit_count",
            "P0":"water×microbe pooled action mean",
            "P1":"P0+shrunken accession residual",
            "P2":"P1+shrunken accession×full-action-cell residual",
            "k_accession":k_accession,"k_action":k_action,
            "center_action_effects":center_action,
            "test":"leave-one-rack-out, five folds",
        },
        "n_tested":len(predictions),"n_accessions":len(acc_deltas),
        "folds":folds,
        "heldout_mse":{m:round(sums[m]/len(predictions),8)
                       for m in ("P0","P1","P2")},
        "mean_gain_P1_minus_P0":round(sums["gain_P1_P0"]/len(predictions),8),
        "mean_gain_P2_minus_P1":round(locus_gain,8),
        "accession_equal_gain_P2_minus_P1":round(pop_mean,8),
        "accession_resampled_conditional_95_interval":[round(v,8) for v in ci],
        "action_specific_gain_P2_minus_P1":condition_gains,
        "n_positive_folds":positive_folds,
        "n_positive_contexts":positive_contexts,
        "n_positive_accessions":sum(v>0 for v in accession_means),
        "positive_gate": (
            "EXPLORATORY_ACCESSION_ACTION_GAIN_SUPPORTED" if gate
            else "ACCESSION_ACTION_GAIN_NOT_SUPPORTED_UNDER_FROZEN_GATE"
        ),
        "caveat": "Conditional bootstrap of accession means after fixed heldout predictions; "
                  "not external validation or a theorem proof",
    }


def analyse(raw:bytes):
    provenance=checksum(raw)
    records,qc=parse_source(raw)
    action_means=defaultdict(list)
    for row in records:
        action_means[row["action"]].append(row["fruit"])
    return {
        "source":provenance,"qc":qc,
        "primary":score_folds(records,10,10),
        "post_result_centered_action_only_sensitivity": score_folds(
            records,10,10,center_action=True
        ),
        "sensitivity_fixed_before_outcome":{
            "k_5":score_folds(records,5,5,bootstrap=250),
            "k_20":score_folds(records,20,20,bootstrap=250),
        },
        "source_action_fruit_means":{
            action:round(sum(v)/len(v),6) for action,v in sorted(action_means.items())
        },
        "status":"EDUCATIONAL_MIRROR_ONLY_NOT_AUTHENTICATED_2019_DRYAD_GENOMIC_STATE",
        "limits":[
            "The centered-action-only diagnostic was added after seeing the original P2 prediction. "
            "It is a post-result parametric sensitivity, not a new confirmatory gate.",
            "The 2019 paper states 38 accessions and 760 individuals for the drought experiment, "
            "but this teaching mirror has 44 accession codes and 879 source records.",
            "Only accession identifiers, not genotypes/SNPs or origin ancestry, were observed.",
            "Fitness measurement is fruit count, not verified lifetime seeds.",
            "Replicate/rack holdouts use the same accession set and five experimental blocks.",
            "These predictive contrasts cannot test MLTR total source-target relations or history coherence.",
            "Original publication already reported genotype-specific drought/microbial effects.",
        ],
    }


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    source=parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--input",type=Path)
    source.add_argument("--from-public-github",action="store_true")
    parser.add_argument("--out",type=Path,required=True)
    args=parser.parse_args()
    raw=get_public_csv() if args.from_public_github else args.input.read_bytes()
    result=analyse(raw)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({
        "sha256":result["source"]["sha256"],
        "n":result["qc"]["n_rows"],
        "n_accessions":result["qc"]["n_accessions"],
        "source_status":result["status"],
        "primary_gain":result["primary"]["mean_gain_P2_minus_P1"],
        "primary_gate":result["primary"]["positive_gate"],
        "centered_action_only_gain":result["post_result_centered_action_only_sensitivity"]["mean_gain_P2_minus_P1"],
        "centered_action_only_conditional_interval":result["post_result_centered_action_only_sensitivity"]["accession_resampled_conditional_95_interval"],
        "centered_action_only_gate":result["post_result_centered_action_only_sensitivity"]["positive_gate"],
        "centered_action_only_positive_accessions":result["post_result_centered_action_only_sensitivity"]["n_positive_accessions"],
        "P0_P1_P2_mse":result["primary"]["heldout_mse"],
        "five_folds":result["primary"]["folds"],
        "conditional_interval":result["primary"]["accession_resampled_conditional_95_interval"],
    },sort_keys=True))


if __name__=="__main__":
    main()
