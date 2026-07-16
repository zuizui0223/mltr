"""Write CSV tables used by the combined structural-change manuscript figures."""

from __future__ import annotations

import csv
from pathlib import Path

from verify_submission_story import build_report

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "artifacts"
DEFECT_CSV = ARTIFACTS / "submission_transport_defect_curve.csv"
SUMMARY_CSV = ARTIFACTS / "submission_structural_change_summary.csv"


def write_tables(max_module_count: int = 8) -> tuple[Path, Path]:
    report = build_report(max_module_count)
    ARTIFACTS.mkdir(parents=True, exist_ok=True)

    with DEFECT_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=(
                "module_count",
                "source_macrostates",
                "repaired_target_macrostates",
                "transport_defect_states",
                "transport_defect_bits",
            ),
        )
        writer.writeheader()
        writer.writerows(report["accumulating_defect"])

    local = report["local_split"]
    history = report["history"]
    rows = (
        {
            "analysis": "local_split",
            "value_1": local["source_macrostates"],
            "value_2": local["target_macrostates"],
            "value_3": local["transport_defect_states"],
        },
        {
            "analysis": "coherent_history",
            "value_1": history["coherent_path_count"],
            "value_2": len(history["coherent_carried_labels"]),
            "value_3": len(history["coherent_repaired_labels"]),
        },
        {
            "analysis": "incoherent_history",
            "value_1": history["incoherent_path_count"],
            "value_2": history["minimum_history_modes"],
            "value_3": history["history_aware_label_count"],
        },
    )
    with SUMMARY_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=("analysis", "value_1", "value_2", "value_3")
        )
        writer.writeheader()
        writer.writerows(rows)

    return DEFECT_CSV, SUMMARY_CSV


def main() -> None:
    for path in write_tables():
        print(path)


if __name__ == "__main__":
    main()
