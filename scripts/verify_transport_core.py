"""Write a deterministic replay report for the EXT theorem core."""

from __future__ import annotations

import argparse
import json
import os
import platform
from pathlib import Path

from ext_transport.defect_witnesses import (
    accumulating_transport_defect_witness,
    local_fiber_split_defect_witness,
)
from ext_transport.path_witnesses import coherent_defect_diamond_witness, incoherent_label_diamond_witness
from ext_transport.witnesses import (
    conservative_transport_witness,
    derived_target_projection_witness,
    many_to_one_replacement_witness,
    new_action_fiber_split_witness,
)

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "artifacts" / "transport_core_report.json"


def build_report() -> dict[str, object]:
    replacement = many_to_one_replacement_witness()
    target_projection = derived_target_projection_witness()
    conservative = conservative_transport_witness()
    obstruction = new_action_fiber_split_witness()
    local_defect = local_fiber_split_defect_witness()
    accumulating_defect = accumulating_transport_defect_witness(4)
    coherent_path = coherent_defect_diamond_witness()
    incoherent_path = incoherent_label_diamond_witness()
    certificates = (
        replacement,
        target_projection,
        conservative,
        obstruction,
        local_defect,
        accumulating_defect,
        coherent_path,
        incoherent_path,
    )
    if not all(item.verify() for item in certificates):
        raise AssertionError("one EXT finite witness failed verification")
    transport = replacement.transports[0]
    return {
        "schema_version": 3,
        "source": {
            "git_sha": os.environ.get("GITHUB_SHA", "local-unpinned"),
            "python": platform.python_version(),
        },
        "scope": {
            "model_class": "declared finite deterministic controlled systems, finite prefix-closed grammars, finite replacement relations, and rooted finite replacement DAGs",
            "non_claim": "the replay does not infer ecological replacement histories, establish field turnover mechanisms, or prove transport, repair, or route coherence for arbitrary stochastic systems",
        },
        "exact_replacement_transport": {
            "source_product_states": transport.source.constrained_system.product_state_count,
            "target_product_states": transport.target.constrained_system.product_state_count,
            "macro_states": replacement.macro.state_count,
            "relation": [list(pair) for pair in transport.relation],
            "source_to_target_injection": transport.is_source_to_target_injection,
        },
        "derived_target_projection": {
            "target_labels": list(target_projection.target_labels),
            "macro_state_count": target_projection.target_projection.label_count,
        },
        "conservative_target_only_action": {
            "target_labels": list(conservative.target_labels),
            "schema_rows": [list(row) for row in conservative.schema.transition_rows],
        },
        "fiber_split_obstruction": {
            "future_word": list(obstruction.future_word),
            "left_source_index": obstruction.left_source_index,
            "right_source_index": obstruction.right_source_index,
            "status": "the proposed carried merge is refuted",
        },
        "relative_exact_refinement": {
            "carried_labels": list(local_defect.carried_labels),
            "refined_labels": list(local_defect.refinement.refined_labels),
            "refinement_rounds": local_defect.refinement.refinement_rounds,
            "fiber_split_profile": list(local_defect.refinement.fiber_split_profile),
            "source_macrostate_count": local_defect.source_macrostate_count,
            "target_macrostate_count": local_defect.target_macrostate_count,
            "defect_states": local_defect.transport_defect_states,
            "defect_bits": local_defect.transport_defect_bits,
        },
        "accumulating_transport_defect": {
            "module_count": 4,
            "source_macrostate_count": accumulating_defect.source_macrostate_count,
            "target_macrostate_count": accumulating_defect.target_macrostate_count,
            "defect_states": accumulating_defect.transport_defect_states,
            "defect_bits": accumulating_defect.transport_defect_bits,
            "fiber_split_profile": list(accumulating_defect.refinement.fiber_split_profile),
        },
        "path_coherent_transport": {
            "path_count": len(coherent_path.paths),
            "paths": [list(path) for path in coherent_path.paths],
            "labels_by_path": [list(labels) for labels in coherent_path.labels_by_path],
            "carried_labels": list(coherent_path.carried_labels),
            "refined_labels": list(coherent_path.refinement.refined_labels),
            "defect_states": coherent_path.transport_defect_states,
            "defect_bits": coherent_path.transport_defect_bits,
            "status": "one carried partition and one minimal repair across all declared routes",
        },
        "path_incoherence_boundary": {
            "labels_by_path": [list(labels) for labels in incoherent_path.labels_by_path],
            "status": "different declared routes assign different root macro labels; coherence certificate is rejected",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-report", action="store_true")
    args = parser.parse_args()
    report = build_report()
    if args.write_report:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
