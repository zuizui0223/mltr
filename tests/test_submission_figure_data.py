import csv
import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "write_submission_figure_data.py"


def test_submission_figure_tables(tmp_path, monkeypatch):
    namespace = runpy.run_path(str(SCRIPT))
    monkeypatch.setitem(namespace["write_tables"].__globals__, "ARTIFACTS", tmp_path)
    monkeypatch.setitem(namespace["write_tables"].__globals__, "DEFECT_CSV", tmp_path / "defect.csv")
    monkeypatch.setitem(namespace["write_tables"].__globals__, "SUMMARY_CSV", tmp_path / "summary.csv")
    defect_path, summary_path = namespace["write_tables"](4)
    with defect_path.open(encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert [int(row["repaired_target_macrostates"]) for row in rows] == [3, 5, 9, 17]
    assert [int(row["transport_defect_states"]) for row in rows] == [1, 3, 7, 15]
    with summary_path.open(encoding="utf-8") as handle:
        summary = list(csv.DictReader(handle))
    assert [row["analysis"] for row in summary] == [
        "local_split",
        "coherent_history",
        "incoherent_history",
    ]
