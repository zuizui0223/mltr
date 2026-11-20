#!/usr/bin/env python3
"""Out-of-rack retrospective action-choice value for known Arabidopsis accessions.

Source-locked University of Toronto teaching copy, NOT original verified Dryad,
NOT molecular-genomic evidence, NOT MLTR source-target transport validation.
All intervention outcomes are from DIFFERENT randomized plants per accession
× rack; they are not four counterfactual outcomes for any one individual.

Protocol: docs/arabidopsis_action_decision_protocol_2026-11-20.md
"""
from __future__ import annotations

import argparse
import json
import random
from collections import Counter, defaultdict
from pathlib import Path

from audit_arabidopsis_factorial_response import (
    get_public_csv, parse_source, train_models, predict_one, checksum
)

ACTION_ORDER = ("D|L", "D|S", "W|L", "W|S")
RACKS = ("1", "2", "3", "4", "5")


def choose_action(predictions: dict[str, float]) -> str:
    if set(predictions) != set(ACTION_ORDER):
        raise ValueError("action choice requires exactly four alternatives")
    # stable tie breaking in frozen order
    return max(ACTION_ORDER, key=lambda action: predictions[action])


def complete_panel(rows: list[dict]) -> bool:
    counts = Counter(row["action"] for row in rows)
    return len(rows) == 4 and all(counts[action] == 1 for action in ACTION_ORDER)


def bootstrap_accession_gain(by_accession: dict[str, list[float]],
                             draws=2000, seed=20261120):
    if draws < 1 or len(by_accession) < 3:
        raise ValueError("not enough clusters/draws")
    means = [sum(vals)/len(vals) for vals in by_accession.values()]
    n = len(means)
    rng = random.Random(seed)
    replicate = []
    for _ in range(draws):
        replicate.append(
            sum(means[rng.randrange(n)] for _ in range(n)) / n
        )
    replicate.sort()
    def q(frac):
        x = (len(replicate) - 1) * frac
        i = int(x)
        t = x - i
        j = min(i + 1, len(replicate)-1)
        return replicate[i]*(1-t) + replicate[j]*t
    return {
        "n_accession_clusters":n,
        "draws":draws,
        "seed":seed,
        "mean_equal_accession":round(sum(means)/n,8),
        "conditional_95ci":[round(q(0.025),8),round(q(0.975),8)],
        "n_positive_accessions":sum(value>0 for value in means),
        "n_negative_accessions":sum(value<0 for value in means),
        "n_zero_accessions":sum(value==0 for value in means),
    }


def evaluate_policy(rows, pseudo=10.0, bootstrap_draws=2000):
    """Strictly preserve training/test rack segregation for every policy."""
    if pseudo != 10.0:
        # main policy assessment is locked; changing shrinkage later is not
        # a permissible optimization.
        raise ValueError("frozen decision policy requires pseudo=10")
    if set(row["replicate"] for row in rows) != set(RACKS):
        raise ValueError("missing rack/replicate")
    if len({row["accession"] for row in rows}) < 3:
        raise ValueError("not enough accessions for group uncertainty")
    records = []
    rack_summary = []
    excluded_design_panels = []
    action_mix = Counter()
    for hold in RACKS:
        training = [r for r in rows if r["replicate"] != hold]
        testing = [r for r in rows if r["replicate"] == hold]
        model = train_models(training, k_accession=10, k_action=10)
        baseline = choose_action({a: model[0][a] for a in ACTION_ORDER})
        panels = defaultdict(list)
        for r in testing:
            panels[r["accession"]].append(r)
        realized = []
        for genotype, panel in panels.items():
            if not complete_panel(panel):
                excluded_design_panels.append({
                    "heldout_rack": hold,
                    "n_rows":len(panel),
                    "reason":"panel_not_exactly_one_per_action",
                })
                continue
            source = {r["action"]:r["value"] for r in panel}
            predicted = {
                a:predict_one({"action":a,"accession":genotype},model)
                for a in ACTION_ORDER
            }
            p1 = choose_action({a:predicted[a]["P1"] for a in ACTION_ORDER})
            if p1 != baseline:
                raise ValueError("accession intercept altered action ranking")
            p2 = choose_action({a:predicted[a]["P2"] for a in ACTION_ORDER})
            if p2 != choose_action({
                a:predicted[a]["P2"]-sum(predicted[b]["P2"]-predicted[b]["P1"] for b in ACTION_ORDER)/4
                for a in ACTION_ORDER
            }):
                raise ValueError("subtracting accession intercept changed P2 action order")
            change = source[p2] - source[baseline]
            realized.append(change)
            action_mix["P0|"+baseline]+=1
            action_mix["P2|"+p2]+=1
            if p2 != baseline:
                action_mix["changed"]+=1
            records.append({
                "genotype": genotype,
                "rack":hold,
                "utility_gain":change,
                "changed_action":p2 != baseline,
                "oracle_regret_P0":max(source.values()) - source[baseline],
                "oracle_regret_P2":max(source.values()) - source[p2],
            })
        if not realized:
            raise ValueError("no complete panels in held-out rack")
        rack_summary.append({
            "heldout_rack":hold,
            "complete_panels":len(realized),
            "mean_gain_sqrt_fruit":round(sum(realized)/len(realized),8),
            "n_changed_actions":sum(r["changed_action"] for r in records if r["rack"] == hold),
        })
    if not records:
        raise ValueError("no admissible action panels")
    by_acc=defaultdict(list)
    for r in records:
        by_acc[r["genotype"]].append(r["utility_gain"])
    unc=bootstrap_accession_gain(by_acc,draws=bootstrap_draws)
    mean=sum(r["utility_gain"] for r in records)/len(records)
    pass_gate = (
        mean>0
        and unc["conditional_95ci"][0]>0
        and sum(z["mean_gain_sqrt_fruit"]>0 for z in rack_summary)>=3
    )
    return {
        "status":"EXPLORATORY_DECISION_VALUE_SUPPORTED" if pass_gate
                 else "DECISION_VALUE_NOT_SUPPORTED_UNDER_FROZEN_GATE",
        "n_panels":len(records),
        "n_source_rows_in_complete_panels":len(records)*4,
        "n_design_excluded_panels":len(excluded_design_panels),
        "n_source_rows_excluded_by_design":sum(x["n_rows"] for x in excluded_design_panels),
        "design_exclusions_by_rack":dict(sorted(Counter(x["heldout_rack"] for x in excluded_design_panels).items())),
        "mean_gain_sqrt_fruit_per_panel":round(mean,8),
        "mean_regret_baseline_P0":round(sum(r["oracle_regret_P0"] for r in records)/len(records),8),
        "mean_regret_P2":round(sum(r["oracle_regret_P2"] for r in records)/len(records),8),
        "fraction_action_changes":round(action_mix["changed"]/len(records),8),
        "n_action_changes":int(action_mix["changed"]),
        "action_mix":dict(sorted(action_mix.items())),
        "by_heldout_rack":rack_summary,
        "accession_cluster_uncertainty":unc,
        "fixed_protocol":{
            "alternatives":list(ACTION_ORDER),
            "experimental_costs":"assumed equal for retrospective check; not real management",
            "value":"sqrt(fruit) observed in one plant for selected action",
            "comparison":"P2 accession×action choice minus P0/P1 coarse choice",
            "holdout":"leave-one-rack-out; full four-action accession×rack panels only",
            "pseudocount":10,
            "gate":"mean gain positive; conditional accession bootstrap lower>0; >=3 of 5 racks positive",
        },
        "interpretive_limits":[
            "Teaching mirror is not byte-matched to the original Dryad 38-accession/760-plant drought dataset.",
            "Accession is a lineage label; no molecular SNP or genome markers in this file.",
            "All four actions had different plants, not within-individual counterfactual outcomes.",
            "No treatment cost or management risk: experimental equal-cost assumption only.",
            "Bootstrap resamples accession clusters conditional on fitted 5-fold policies and is not independent replication.",
            "Post-result exploratory policy test, although utility/gate frozen before action-score inspection.",
            "No declared source-target ecological replacement map or exact MLTR theorem was empirically tested.",
        ],
    }


def analyse(raw:bytes):
    provenance=checksum(raw)
    rows,qc=parse_source(raw)
    if qc["n_rows"]!=879 or qc["n_accessions"]!=44:
        raise ValueError("pinned mirror source population changed")
    return {
        "source":provenance,"qc":qc,
        "action_decision":evaluate_policy(rows),
        "scope":"OBSERVATIONAL_TEACHING_MIRROR_RETROSPECTIVE_ACTION_DECISION",
    }


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    source=ap.add_mutually_exclusive_group(required=True)
    source.add_argument("--input",type=Path)
    source.add_argument("--from-public-github",action="store_true")
    ap.add_argument("--out",type=Path,required=True)
    args=ap.parse_args()
    source_bytes=get_public_csv() if args.from_public_github else args.input.read_bytes()
    out=analyse(source_bytes)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    policy=out["action_decision"]
    print(json.dumps({
        "source_sha256":out["source"]["sha256"],
        "panels":policy["n_panels"],
        "decision_value_status":policy["status"],
        "n_action_changes":policy["n_action_changes"],
        "mean_gain":policy["mean_gain_sqrt_fruit_per_panel"],
        "bootstrap":policy["accession_cluster_uncertainty"],
        "folds":policy["by_heldout_rack"],
    },sort_keys=True))


if __name__=="__main__":
    main()
