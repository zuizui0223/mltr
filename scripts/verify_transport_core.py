"""Write a deterministic replay report for the EXT theorem core."""

from __future__ import annotations

import argparse
import json
import os
import platform
from pathlib import Path

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
    if not all(item.verify() for item in (replacement, target_projection, conservative, obstruction)):
        raise AssertionError("one EXT finite witness failed verification")
    transport = replacement.transports[0]
    return {
        "schema_version": 1,
        "source": {
            "git_sha": os.environ.get("GITHUB_SHA", "local-unpinned"),
            "python": platform.python_version(),
        },
        "scope": {
            "model_class": "declared finite deterministic controlled systems and finite replacement relations",
            "non_claim": "the replay does not infer an ecological replacement relation, establish a field turnover mechanism, or prove transport for arbitrary stochastic systems",
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
