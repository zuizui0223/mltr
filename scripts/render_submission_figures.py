"""Render manuscript-ready SVG figures from verified submission analyses.

The renderer uses only the Python standard library. All numerical labels come from
``verify_submission_story.build_report`` so figures cannot silently drift from the
reproducibility witness.
"""

from __future__ import annotations

import html
import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "artifacts"
VERIFY_SCRIPT = Path(__file__).with_name("verify_submission_story.py")


def _report(max_module_count: int = 6) -> dict[str, object]:
    return runpy.run_path(str(VERIFY_SCRIPT))["build_report"](max_module_count)


def _svg(width: int, height: int, body: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img">\n'
        '<style>text{font-family:Arial,sans-serif;fill:#111} .axis{stroke:#111;stroke-width:1.5} '
        '.thin{stroke:#555;stroke-width:1.2;fill:none} .box{fill:#fff;stroke:#111;stroke-width:1.5} '
        '.fiber{fill:#ececec;stroke:#111;stroke-width:1.2} .decision{fill:#f7f7f7;stroke:#111;stroke-width:1.5} '
        '.arrow{stroke:#111;stroke-width:1.5;fill:none;marker-end:url(#arrowhead)}</style>\n'
        '<defs><marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">'
        '<polygon points="0 0, 10 3.5, 0 7" fill="#111"/></marker></defs>\n'
        f"{body}\n</svg>\n"
    )


def _text(x: float, y: float, value: object, size: int = 15, anchor: str = "middle") -> str:
    return (
        f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}">'
        f"{html.escape(str(value))}</text>"
    )


def render_local_split(report: dict[str, object]) -> str:
    """Show a readable ecological pathway from turnover to decision reversal."""
    local = report["local_split"]
    carried = tuple(local["carried_labels"])
    repaired = tuple(local["repaired_labels"])
    body: list[str] = []

    boxes = [
        (80, 30, "1. Structural change", "Dominant pollinator is lost", "community interaction structure changes", "box"),
        (540, 30, "2. Inherited classification", "Sites A and B remain grouped", f"carried labels: {carried}", "decision"),
        (540, 200, "3. New intervention", "Competitor removal becomes legal", "the action tests substitute-pollinator access", "box"),
        (80, 200, "4. Local obstruction", "Same inherited label", "but A fails and B retains pollination response", "box"),
        (80, 370, "5. Minimal source-relative repair", f"split only the exposed class: {carried} → {repaired}", f"transport defect = {local['transport_defect_states']} macrostate", "box"),
        (540, 370, "6. Decision reversal", "Old rule: prioritize cheaper Site A", "Repaired rule: prioritize responsive Site B", "decision"),
    ]

    for x, y, title, line1, line2, css_class in boxes:
        body.append(f'<rect class="{css_class}" x="{x}" y="{y}" width="380" height="120" rx="12"/>')
        body.append(_text(x + 190, y + 30, title, 16))
        body.append(_text(x + 190, y + 65, line1, 14))
        body.append(_text(x + 190, y + 90, line2, 13))

    body.extend([
        '<path class="arrow" d="M460 90 L530 90"/>',
        '<path class="arrow" d="M730 150 L730 190"/>',
        '<path class="arrow" d="M540 260 L470 260"/>',
        '<path class="arrow" d="M270 320 L270 360"/>',
        '<path class="arrow" d="M460 430 L530 430"/>',
    ])

    body.append('<rect class="fiber" x="180" y="540" width="640" height="88" rx="12"/>')
    body.append(_text(500, 569, "Management consequence", 16))
    body.append(_text(500, 597, "The inherited law treats A and B as tied; the repaired law recognizes only B as recoverable.", 14))
    body.append(_text(500, 619, "The theorem changes the decision by identifying exactly one missing ecological distinction.", 13))

    return _svg(1000, 660, "\n".join(body))


def render_defect_curve(report: dict[str, object]) -> str:
    rows = list(report["accumulating_defect"])
    width, height = 820, 440
    left, right, top, bottom = 90, 760, 25, 365
    max_x = max(row["module_count"] for row in rows)
    max_y = max(row["repaired_target_macrostates"] for row in rows)
    points = []
    body: list[str] = []
    body.extend([
        f'<line class="axis" x1="{left}" y1="{bottom}" x2="{right}" y2="{bottom}"/>',
        f'<line class="axis" x1="{left}" y1="{bottom}" x2="{left}" y2="{top}"/>',
    ])
    for row in rows:
        x = left + (right-left) * row["module_count"] / max_x
        y = bottom - (bottom-top) * row["repaired_target_macrostates"] / max_y
        points.append(f"{x:.1f},{y:.1f}")
        body.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.5" fill="#111"/>')
        body.append(_text(x, y-10, row["repaired_target_macrostates"], 12))
        body.append(_text(x, bottom+24, row["module_count"], 12))
    body.append(f'<polyline class="thin" points="{" ".join(points)}"/>')
    body.append(_text((left+right)/2, 416, "independently exposed target distinctions (m)", 15))
    body.append(_text(18, (top+bottom)/2, "repaired states", 15, "start"))
    body.append(_text(585, 45, "verified family: |Q*| = 2^m + 1", 14))
    return _svg(width, height, "\n".join(body))


def render_history(report: dict[str, object]) -> str:
    history = report["history"]
    body: list[str] = []
    for offset, label in ((0, "coherent"), (450, "incoherent")):
        body.append(f'<circle class="fiber" cx="{100+offset}" cy="90" r="30"/>')
        body.append(f'<circle class="fiber" cx="{240+offset}" cy="45" r="30"/>')
        body.append(f'<circle class="fiber" cx="{240+offset}" cy="135" r="30"/>')
        body.append(f'<circle class="fiber" cx="{380+offset}" cy="90" r="30"/>')
        body.extend([
            f'<line class="thin" x1="130" y1="80" x2="210" y2="52" transform="translate({offset},0)"/>',
            f'<line class="thin" x1="130" y1="100" x2="210" y2="128" transform="translate({offset},0)"/>',
            f'<line class="thin" x1="270" y1="52" x2="350" y2="80" transform="translate({offset},0)"/>',
            f'<line class="thin" x1="270" y1="128" x2="350" y2="100" transform="translate({offset},0)"/>',
        ])
        body.append(_text(240+offset, 195, label, 16))
    body.append(_text(225, 240, "one route-independent repair", 14))
    body.append(_text(675, 240, f"requires {history['minimum_history_modes']} history modes", 14))
    body.append(_text(675, 275, f"history-aware states = {history['history_aware_label_count']}", 14))
    return _svg(900, 310, "\n".join(body))


def render_all() -> tuple[Path, Path, Path]:
    report = _report()
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    outputs = (
        (ARTIFACTS / "figure1_local_split.svg", render_local_split(report)),
        (ARTIFACTS / "figure2_transport_defect.svg", render_defect_curve(report)),
        (ARTIFACTS / "figure3_history_completion.svg", render_history(report)),
    )
    for path, content in outputs:
        path.write_text(content, encoding="utf-8")
    return tuple(path for path, _ in outputs)


if __name__ == "__main__":
    for output in render_all():
        print(output)
