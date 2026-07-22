import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "render_submission_figures.py"


def test_submission_figures_render_from_verified_report(tmp_path, monkeypatch):
    module = runpy.run_path(str(SCRIPT))
    monkeypatch.setitem(module["render_all"].__globals__, "ARTIFACTS", tmp_path)
    outputs = module["render_all"]()
    assert [path.name for path in outputs] == [
        "figure1_local_split.svg",
        "figure2_transport_defect.svg",
        "figure3_history_completion.svg",
    ]
    for path in outputs:
        text = path.read_text(encoding="utf-8")
        assert text.startswith("<svg")
        assert "</svg>" in text
    local_split = outputs[0].read_text(encoding="utf-8")
    assert "Minimal source-relative repair" in local_split
    assert "transport defect = 1 macrostate" in local_split
    assert "Decision reversal" in local_split
    assert "The inherited law treats A and B as tied" in local_split
    assert "2^m + 1" in outputs[1].read_text(encoding="utf-8")
    assert "requires 2 history modes" in outputs[2].read_text(encoding="utf-8")
