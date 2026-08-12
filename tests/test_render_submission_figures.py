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
        "figure4_decision_reversal.svg",
    ]
    for path in outputs:
        text = path.read_text(encoding="utf-8")
        assert text.startswith("<svg")
        assert "</svg>" in text
    local_split = outputs[0].read_text(encoding="utf-8")
    assert "Least exact distinction" in local_split
    assert "structural defect = 1 macrostate" in local_split
    assert "Monitoring implication" in local_split
    assert "least state distinction" in local_split
    defect = outputs[1].read_text(encoding="utf-8")
    assert "2^m + 1" in defect
    assert "not monitoring cost or regret" in defect
    assert "requires 2 carried-map contexts" in outputs[2].read_text(encoding="utf-8")
    reversal = outputs[3].read_text(encoding="utf-8")
    assert "0.15" in reversal
    assert "illustrative case" in reversal
    assert "reverses the cheap-site rule" in reversal
