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
    """Show the ecological sequence from pollinator loss to decision reversal."""
    local = report["local_split"]
    carried = tuple(local["carried_labels"])
    repaired = tuple(local["repaired_labels"])
    body = [_text(500, 30, "From pollinator turnover to repaired restoration priority", 20)]

    steps = [
        ("1. Pollinator loss", "Original dominant guild disappears", "community structure changes"),
        ("2. Inherited monitoring class", "Sites A and B remain grouped", f"carried labels: {carried}"),
        ("3. New management action", "Competitor removal becomes legal", "substitute access is tested"),
        ("4. Local obstruction", "Same inherited label, different successor", "A fails; B retains response"),
        ("5. Minimal source-relative repair", f"labels: {carried} → {repaired}", f"defect = {local['transport_defect_states']} macrostate"),
        ("6. Revised restoration decision", "Prioritize Site B", "B retains substitute response"),
    ]

    x_positions = [95, 255, 415, 575, 735, 895]
    widths = [140, 140, 140, 140, 150, 150]
    for index, ((title, line1, line2), x, width) in enumerate(zip(steps, x_positions, widths)):
        left = x - width / 2
        css_class = "decision" if index in {1, 5} else "box"
        body.append(f'<rect class="{css_class}" x="{left}" y="85" width="{width}" height="165" rx="10"/>')
        body.append(_text(x, 112, title, 14))
        body.append(_text(x, 151, line1, 12))
        body.append(_text(x, 174, line2, 12))
        if index == 1:
            body.append(_text(x, 212, "old rule: choose cheaper A", 12))
        if index == 4:
            body.append(_text(x, 212, "retain all valid old merges", 12))
        if index < len(steps) - 1:
            next_left = x_positions[index + 1] - widths[index + 1] / 2
            body.append(f'<path class="arrow" d="M{left + width} 167 L{next_left - 10} 167"/>')

    body.append('<rect class="fiber" x="245" y="300" width="510" height="95" rx="10"/>')
    body.append(_text(500, 328, "Management consequence", 16))
    body.append(_text(500, 354, "Inherited law: A > B because outcomes appear tied and A is cheaper", 13))
    body.append(_text(500, 378, "Repaired law: B > A because only B can recover pollination service", 13))

    return _svg(1000, 430, "\n".join(body))


def render_defect_curve(report: dict[str, object]) -> str:
    rows = list(report["accumulating_defect"])
    width, height = 820, 480
    left, right, top, bottom = 90, 760, 55, 405
    max_x = max(row["module_count"] for row in rows)
    max_y = max(row["repaired_target_macrostates"] for row in rows)
    points = []
    body = [_text(410, 30, "Minimal repair burden under independently exposed distinctions", 20)]
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
    body.append(_text((left+right)/2, 456, "independently exposed target distinctions (m)", 15))
    body.append(_text(18, (top+bottom)/2, "repaired states", 15, "start"))
    body.append(_text(585, 75, "verified family: |Q*| = 2^m + 1", 14))
    return _svg(width, height, "\n".join(body))


def render_history(report: dict[str, object]) -> str:
    history = report["history"]
    body = [_text(450, 32, "Route coherence and minimum history completion", 20)]
    for offset, label in ((0, "coherent"), (450, "incoherent")):
        body.append(f'<circle class="fiber" cx="{100+offset}" cy="120" r="30"/>')
        body.append(f'<circle class="fiber" cx="{240+offset}" cy="75" r="30"/>')
        body.append(f'<circle class="fiber" cx="{240+offset}" cy="165" r="30"/>')
        body.append(f'<circle class="fiber" cx="{380+offset}" cy="120" r="30"/>')
        body.extend([
            f'<line class="thin" x1="130" y1="110" x2="210" y2="82" transform="translate({offset},0)"/>',
            f'<line class="thin" x1="130" y1="130" x2="210" y2="158" transform="translate({offset},0)"/>',
            f'<line class="thin" x1="270" y1="82" x2="350" y2="110" transform="translate({offset},0)"/>',
            f'<line class="thin" x1="270" y1="158" x2="350" y2="130" transform="translate({offset},0)"/>',
        ])
        body.append(_text(240+offset, 225, label, 16))
    body.append(_text(225, 270, "one route-independent repair", 14))
    body.append(_text(675, 270, f"requires {history['minimum_history_modes']} history modes", 14))
    body.append(_text(675, 305, f"history-aware states = {history['history_aware_label_count']}", 14))
    return _svg(900, 350, "\n".join(body))


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
