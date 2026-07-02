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
    assert report["schema_version"] == 1
    assert report["exact_replacement_transport"]["source_product_states"] == 3
    assert report["exact_replacement_transport"]["target_product_states"] == 2
    assert not report["exact_replacement_transport"]["source_to_target_injection"]
    assert report["derived_target_projection"]["target_labels"] == [0, 1]
    assert report["conservative_target_only_action"]["schema_rows"] == [[1, 1], [0, 1]]
    assert report["fiber_split_obstruction"]["future_word"] == ["reveal"]
