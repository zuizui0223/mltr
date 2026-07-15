import runpy
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "verify_submission_story.py"


def test_submission_story_replay_tracks_main_claims():
    report = runpy.run_path(str(SCRIPT))["build_report"](4)
    assert report["schema_version"] == 1
    assert report["local_split"] == {
        "carried_labels": (0, 0, 1),
        "repaired_labels": (0, 1, 2),
        "source_macrostates": 2,
        "target_macrostates": 3,
        "transport_defect_states": 1,
        "fiber_split_profile": (2, 1),
    }
    assert [row["repaired_target_macrostates"] for row in report["accumulating_defect"]] == [3, 5, 9, 17]
    assert [row["transport_defect_states"] for row in report["accumulating_defect"]] == [1, 3, 7, 15]
    assert report["history"]["coherent_path_count"] == 2
    assert report["history"]["incoherent_carried_maps"] == ((0, 1), (1, 0))
    assert report["history"]["minimum_history_modes"] == 2
    assert report["history"]["history_context_bits"] == pytest.approx(1.0)
    assert report["history"]["history_aware_label_count"] == 4


def test_submission_story_rejects_invalid_analysis_range():
    build_report = runpy.run_path(str(SCRIPT))["build_report"]
    with pytest.raises(ValueError):
        build_report(0)
