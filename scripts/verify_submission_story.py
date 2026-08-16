"""Submission-facing structural-change analysis for Paper A."""

from __future__ import annotations

import json
import math
from itertools import combinations
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


def _entropy(probabilities: tuple[float, ...]) -> float:
    return -sum(p * math.log2(p) for p in probabilities if p > 0.0)


def _uniform_conditional_repair_information(
    carried_labels: tuple[int, ...],
    repaired_labels: tuple[int, ...],
) -> float:
    """Return H(repaired | carried) under a uniform microstate distribution."""
    count = len(carried_labels)
    if count == 0 or len(repaired_labels) != count:
        raise ValueError("carried and repaired labels must have the same positive length")
    total = 0.0
    for carried in sorted(set(carried_labels)):
        members = [i for i, label in enumerate(carried_labels) if label == carried]
        repaired_counts: dict[int, int] = {}
        for index in members:
            repaired = repaired_labels[index]
            repaired_counts[repaired] = repaired_counts.get(repaired, 0) + 1
        conditional = tuple(value / len(members) for value in repaired_counts.values())
        total += (len(members) / count) * _entropy(conditional)
    return total


def _monitoring_realization_example(
    carried_labels: tuple[int, ...],
    repaired_labels: tuple[int, ...],
) -> dict[str, object]:
    """Verify feasible, infeasible, and least-cost monitoring for the local split."""
    if len(carried_labels) != len(repaired_labels):
        raise ValueError("carried and repaired labels must have the same length")

    obstruction_pairs = tuple(
        (i, j)
        for i in range(len(carried_labels))
        for j in range(i + 1, len(carried_labels))
        if carried_labels[i] == carried_labels[j] and repaired_labels[i] != repaired_labels[j]
    )

    library = {
        "flower_abundance": {"values": (1, 1, 0), "cost": 0.25},
        "soil_condition": {"values": (0, 0, 1), "cost": 0.50},
        "substitute_response_capacity": {"values": (0, 1, 0), "cost": 1.00},
    }

    coverage: dict[str, tuple[tuple[int, int], ...]] = {}
    for name, spec in library.items():
        values = tuple(spec["values"])
        coverage[name] = tuple(
            pair for pair in obstruction_pairs if values[pair[0]] != values[pair[1]]
        )

    required = set(obstruction_pairs)
    full_coverage = set().union(*(set(pairs) for pairs in coverage.values())) if coverage else set()
    full_library_feasible = full_coverage == required

    feasible_subsets: list[tuple[float, tuple[str, ...]]] = []
    names = tuple(library)
    for subset_size in range(len(names) + 1):
        for subset in combinations(names, subset_size):
            covered = set().union(*(set(coverage[name]) for name in subset)) if subset else set()
            if covered == required:
                total_cost = sum(float(library[name]["cost"]) for name in subset)
                feasible_subsets.append((total_cost, subset))
    if not feasible_subsets:
        minimum_cost = None
        minimum_cost_measurements: tuple[str, ...] = ()
    else:
        minimum_cost, minimum_cost_measurements = min(
            feasible_subsets,
            key=lambda item: (item[0], len(item[1]), item[1]),
        )

    insufficient_library = ("flower_abundance", "soil_condition")
    insufficient_coverage = set().union(
        *(set(coverage[name]) for name in insufficient_library)
    )
    uncovered_pairs = tuple(pair for pair in obstruction_pairs if pair not in insufficient_coverage)

    return {
        "obstruction_pairs": obstruction_pairs,
        "candidate_library": library,
        "coverage_by_measurement": coverage,
        "full_library_feasible": full_library_feasible,
        "minimum_cost_measurements": minimum_cost_measurements,
        "minimum_cost": minimum_cost,
        "insufficient_library": insufficient_library,
        "uncovered_pairs": uncovered_pairs,
        "interpretation": (
            "illustrative exact monitoring library; measurement values and costs are not empirical estimates"
        ),
    }


def _decision_reversal_example() -> dict[str, object]:
    benefit = 1.0
    cost_a = 0.20
    cost_b = 0.35
    success_a = 0.25
    success_b = 0.80
    pooled_success = (success_a + success_b) / 2.0
    inherited_a = benefit * pooled_success - cost_a
    inherited_b = benefit * pooled_success - cost_b
    repaired_a = benefit * success_a - cost_a
    repaired_b = benefit * success_b - cost_b
    inherited_choice = "A" if inherited_a >= inherited_b else "B"
    repaired_choice = "A" if repaired_a >= repaired_b else "B"
    true_value_of_inherited_choice = repaired_a if inherited_choice == "A" else repaired_b
    true_value_of_repaired_choice = repaired_a if repaired_choice == "A" else repaired_b
    return {
        "benefit": benefit,
        "cost_a": cost_a,
        "cost_b": cost_b,
        "success_a": success_a,
        "success_b": success_b,
        "pooled_success": pooled_success,
        "inherited_expected_net_a": inherited_a,
        "inherited_expected_net_b": inherited_b,
        "repaired_expected_net_a": repaired_a,
        "repaired_expected_net_b": repaired_b,
        "inherited_choice": inherited_choice,
        "repaired_choice": repaired_choice,
        "decision_regret": true_value_of_repaired_choice - true_value_of_inherited_choice,
        "reversal_threshold_delta_p": (cost_b - cost_a) / benefit,
        "observed_delta_p": success_b - success_a,
        "interpretation": "illustrative decision analysis; probabilities and costs are not empirical estimates",
    }


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
    carried = tuple(local.carried_labels)
    repaired = tuple(local.refinement.refined_labels)

    return {
        "schema_version": 3,
        "paper_claim": (
            "audit whether an inherited ecological state classification remains decision-sufficient "
            "after declared structural change and convert failure into an exact monitoring-repair requirement"
        ),
        "local_split": {
            "carried_labels": carried,
            "repaired_labels": repaired,
            "source_macrostates": local.source_macrostate_count,
            "target_macrostates": local.target_macrostate_count,
            "transport_defect_states": local.transport_defect_states,
            "fiber_split_profile": local.refinement.fiber_split_profile,
            "uniform_conditional_repair_information_bits": round(
                _uniform_conditional_repair_information(carried, repaired), 12
            ),
        },
        "monitoring_realization": _monitoring_realization_example(carried, repaired),
        "decision_reversal": _decision_reversal_example(),
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
            "headline_result": (
                "ecological decision-sufficiency audit with exact monitoring feasibility, "
                "impossibility certificates, and minimum-cost realization"
            ),
            "repair_result": (
                "established coarsest-refinement machinery returns the least exact distinction "
                "once the carried interface fails"
            ),
            "measurement_result": (
                "candidate monitoring variables are sufficient exactly when they separate every "
                "obstruction pair; uncovered pairs certify an inadequate measurement library"
            ),
            "decision_result": (
                "structural repair complexity is distinct from decision regret; an illustrative "
                "pollinator example produces a priority reversal"
            ),
            "closing_result": (
                "path coherence yields one route-independent interface; incoherence requires "
                "minimum immutable carried-map context"
            ),
        },
    }


def main() -> None:
    report = build_report()
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
