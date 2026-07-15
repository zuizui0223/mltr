"""Submission-facing structural-change analysis for the combined CCOC–MLTR paper."""

from __future__ import annotations

import json
from pathlib import Path

from ext_transport.defect_witnesses import (
    accumulating_transport_defect_witness,
    local_fiber_split_defect_witness,
)
from ext_transport.history_witnesses import incoherent_history_augmentation_witness
from ext_transport.path_witnesses import (
    coherent_defect_diamond_witness,
    incoherent_label_diamond_witness,
)

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "artifacts" / "submission_story_report.json"


def build_report(max_module_count: int = 6) -> dict[str, object]:
    if not isinstance(max_module_count, int) or isinstance(max_module_count, bool) or max_module_count < 1:
        raise ValueError("max_module_count must be a positive integer")

    local = local_fiber_split_defect_witness()
    accumulation = []
    for module_count in range(1, max_module_count + 1):
        certificate = accumulating_transport_defect_witness(module_count)
        accumulation.append(
            {
                "module_count": module_count,
                "source_macrostates": certificate.source_macrostate_count,
                "repaired_target_macrostates": certificate.target_macrostate_count,
                "transport_defect_states": certificate.transport_defect_states,
                "transport_defect_bits": round(certificate.transport_defect_bits, 12),
            }
        )

    coherent = coherent_defect_diamond_witness()
    incoherent = incoherent_label_diamond_witness()
    augmented = incoherent_history_augmentation_witness()

    return {
        "schema_version": 1,
        "paper_claim": "structural change preserves an inherited macro-law exactly, forces a unique source-relative repair, or requires minimum history context",
        "local_split": {
            "carried_labels": local.carried_labels,
            "repaired_labels": local.refinement.refined_labels,
            "source_macrostates": local.source_macrostate_count,
            "target_macrostates": local.target_macrostate_count,
            "transport_defect_states": local.transport_defect_states,
            "fiber_split_profile": local.refinement.fiber_split_profile,
        },
        "accumulating_defect": accumulation,
        "history": {
            "coherent_path_count": len(coherent.paths),
            "coherent_carried_labels": coherent.carried_labels,
            "coherent_repaired_labels": coherent.refinement.refined_labels,
            "incoherent_path_count": len(incoherent.graph.paths_to(incoherent.terminal)),
            "incoherent_carried_maps": incoherent.labels_by_path,
            "minimum_history_modes": augmented.minimum_history_mode_count,
            "history_context_bits": round(augmented.history_augmentation_bits, 12),
            "history_aware_label_count": augmented.history_aware_macrostate_count,
        },
        "submission_interpretation": {
            "headline_result": "coarsest source-relative exact repair",
            "quantitative_result": "transport defect grows with independently exposed target distinctions",
            "closing_result": "path coherence yields one repair; incoherence has a minimum finite history completion",
        },
    }


def main() -> None:
    report = build_report()
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
