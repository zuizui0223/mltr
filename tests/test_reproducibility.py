import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "verify_transport_core.py"
REPORT = ROOT / "artifacts" / "transport_core_report.json"


def test_transport_core_replay_writes_the_expected_finite_report():
    completed = subprocess.run(
        [sys.executable, str(SCRIPT), "--write-report"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    report = json.loads(completed.stdout)
    assert REPORT.is_file()
    assert report["schema_version"] == 3
    assert report["exact_replacement_transport"]["source_product_states"] == 3
    assert report["exact_replacement_transport"]["target_product_states"] == 2
    assert not report["exact_replacement_transport"]["source_to_target_injection"]
    assert report["derived_target_projection"]["target_labels"] == [0, 1]
    assert report["conservative_target_only_action"]["schema_rows"] == [[1, 1], [0, 1]]
    assert report["fiber_split_obstruction"]["future_word"] == ["reveal"]
    assert report["relative_exact_refinement"]["carried_labels"] == [0, 0, 1]
    assert report["relative_exact_refinement"]["refined_labels"] == [0, 1, 2]
    assert report["relative_exact_refinement"]["defect_states"] == 1
    assert report["accumulating_transport_defect"]["module_count"] == 4
    assert report["accumulating_transport_defect"]["target_macrostate_count"] == 17
    assert report["accumulating_transport_defect"]["defect_states"] == 15
    assert report["path_coherent_transport"]["path_count"] == 2
    assert report["path_coherent_transport"]["labels_by_path"] == [[0, 0, 1], [0, 0, 1]]
    assert report["path_coherent_transport"]["refined_labels"] == [0, 1, 2]
    assert report["path_coherent_transport"]["defect_states"] == 1
    assert report["path_incoherence_boundary"]["labels_by_path"] == [[0, 1], [1, 0]]
