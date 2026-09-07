"""Submission-facing decision-sufficiency and route-coherence analysis for Paper A."""

from __future__ import annotations

import json
from pathlib import Path

from ext_transport.compositional_transport import certify_carried_label_composition
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

    graph = coherent.graph
    composition = certify_carried_label_composition(
        source_projection=graph.root_projection,
        intermediate_system=graph.stage_map["left"],
        terminal_system=graph.stage_map["terminal"],
        first_relation=graph.edges[0].relation,
        second_relation=graph.edges[1].relation,
    )

    return {
        "schema_version": 2,
        "paper_claim": (
            "an inherited ecological state is reusable only when its source meaning can be carried "
            "consistently and remains sufficient for target outputs and actions; fixed-route carriage "
            "composes, while genuinely different routes require history exactly when their complete "
            "carried terminal maps differ"
        ),
        "carried_semantics": {
            "direct_defined": composition.direct_defined,
            "sequential_defined": composition.sequential_defined,
            "commutes": composition.commutes,
            "intermediate_labels": composition.intermediate_labels,
            "direct_terminal_labels": composition.direct_terminal_labels,
            "sequential_terminal_labels": composition.sequential_terminal_labels,
        },
        "local_split": {
            "carried_labels": local.carried_labels,
            "repaired_labels": local.refinement.refined_labels,
            "source_macrostates": local.source_macrostate_count,
            "target_macrostates": local.target_macrostate_count,
            "transport_defect_states": local.transport_defect_states,
            "fiber_split_profile": local.refinement.fiber_split_profile,
            "ecological_interpretation": "one missing target decision distinction to add to monitoring",
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
            "headline_ecological_result": "decision-sufficiency audit for inherited ecological state variables after structural change",
            "headline_formal_result": "carried-semantics composition, route coherence, and necessary-and-sufficient minimum history completion",
            "established_infrastructure": "initial-partition exact refinement, finite split witnesses, and coarsest stable repair",
            "diagnostic_quantity": "transport defect summarizes source-relative repair burden and is not a standalone novelty claim",
            "closing_result": "history is retained only when it changes the carried operational meaning of the present terminal state",
        },
        "manuscript_result_order": (
            "carried_semantics_and_fixed_route_composition",
            "route_coherence_and_minimum_history_completion",
            "operational_decision_sufficiency",
            "established_source_relative_exact_refinement",
            "diagnostic_transport_defect",
        ),
    }


def main() -> None:
    report = build_report()
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
