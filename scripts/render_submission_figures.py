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
        '.shade{fill:#efefef;stroke:none} .dash{stroke:#777;stroke-width:1.2;stroke-dasharray:5,5;fill:none} '
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
    """Show audit failure, exact monitoring feasibility, and the next action."""
    local = report["local_split"]
    carried = tuple(local["carried_labels"])
    repaired = tuple(local["repaired_labels"])
    body: list[str] = []

    boxes = [
        (70, 25, "1. Structural change", "Dominant pollinator is lost", "interaction structure changes", "box"),
        (550, 25, "2. Inherited state", "Sites A and B remain grouped", f"carried labels: {carried}", "decision"),
        (550, 175, "3. Target intervention", "Competitor removal becomes legal", "tests substitute-pollinator access", "box"),
        (70, 175, "4. Local obstruction", "Same inherited label", "but A and B have different successors", "box"),
        (70, 325, "5. Least exact distinction", f"standard refinement: {carried} → {repaired}", f"structural defect = {local['transport_defect_states']} macrostate", "box"),
        (550, 325, "6. Candidate measurements", "Can the library separate every", "obstruction pair in the repaired state?", "decision"),
    ]

    for x, y, title, line1, line2, css_class in boxes:
        body.append(f'<rect class="{css_class}" x="{x}" y="{y}" width="400" height="115" rx="12"/>')
        body.append(_text(x + 200, y + 28, title, 16))
        body.append(_text(x + 200, y + 62, line1, 14))
        body.append(_text(x + 200, y + 87, line2, 13))

    body.extend([
        '<path class="arrow" d="M470 82 L540 82"/>',
        '<path class="arrow" d="M750 140 L750 165"/>',
        '<path class="arrow" d="M550 232 L480 232"/>',
        '<path class="arrow" d="M270 290 L270 315"/>',
        '<path class="arrow" d="M470 382 L540 382"/>',
        '<path class="arrow" d="M750 440 L750 474"/>',
    ])

    body.append('<path class="arrow" d="M750 474 C750 490 510 490 360 515"/>')
    body.append('<path class="arrow" d="M750 474 C750 490 865 490 865 515"/>')

    body.append('<rect class="decision" x="90" y="520" width="440" height="115" rx="12"/>')
    body.append(_text(310, 548, "Library covers every obstruction pair", 15))
    body.append(_text(310, 577, "Exact recovery is feasible", 14))
    body.append(_text(310, 603, "choose a feasible / minimum-cost subset", 13))
    body.append(_text(310, 625, "then estimate thresholds, errors, and decision value", 12))

    body.append('<rect class="box" x="570" y="520" width="400" height="115" rx="12"/>')
    body.append(_text(770, 548, "At least one pair is uncovered", 15))
    body.append(_text(770, 577, "Exact recovery is impossible", 14))
    body.append(_text(770, 603, "with the current measurement library", 13))
    body.append(_text(770, 625, "expand measurements before reusing the state", 12))

    body.append('<rect class="fiber" x="220" y="670" width="660" height="64" rx="12"/>')
    body.append(_text(550, 695, "Ecological output: a falsifiable monitoring-repair requirement", 15))
    body.append(_text(550, 718, "not an undirected request for more variables", 13))

    return _svg(1040, 760, "\n".join(body))


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
    body.append(_text(585, 68, "structural complexity only: not monitoring cost or regret", 12))
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
    body.append(_text(225, 240, "one route-independent carried interface", 14))
    body.append(_text(675, 240, f"requires {history['minimum_history_modes']} carried-map contexts", 14))
    body.append(_text(675, 275, f"history-aware states = {history['history_aware_label_count']}", 14))
    return _svg(900, 310, "\n".join(body))


def render_decision_reversal(report: dict[str, object]) -> str:
    """Show where the repaired two-site decision prefers Site B."""
    decision = report["decision_reversal"]
    width, height = 760, 520
    left, right, top, bottom = 95, 700, 45, 430
    threshold = float(decision["reversal_threshold_delta_p"])

    def px(value: float) -> float:
        return left + (right - left) * value

    def py(value: float) -> float:
        return bottom - (bottom - top) * value

    body: list[str] = [
        f'<line class="axis" x1="{left}" y1="{bottom}" x2="{right}" y2="{bottom}"/>',
        f'<line class="axis" x1="{left}" y1="{bottom}" x2="{left}" y2="{top}"/>',
    ]

    boundary_start_x = 0.0
    boundary_start_y = threshold
    boundary_end_x = 1.0 - threshold
    boundary_end_y = 1.0
    body.append(
        f'<polygon class="shade" points="{px(boundary_start_x):.1f},{py(boundary_start_y):.1f} '
        f'{px(boundary_end_x):.1f},{py(boundary_end_y):.1f} {px(0.0):.1f},{py(1.0):.1f}"/>'
    )
    body.append(
        f'<line class="thin" x1="{px(boundary_start_x):.1f}" y1="{py(boundary_start_y):.1f}" '
        f'x2="{px(boundary_end_x):.1f}" y2="{py(boundary_end_y):.1f}"/>'
    )

    for tick in (0.0, 0.25, 0.5, 0.75, 1.0):
        body.append(f'<line class="thin" x1="{px(tick):.1f}" y1="{bottom}" x2="{px(tick):.1f}" y2="{bottom+6}"/>')
        body.append(_text(px(tick), bottom + 24, f"{tick:.2g}", 11))
        body.append(f'<line class="thin" x1="{left-6}" y1="{py(tick):.1f}" x2="{left}" y2="{py(tick):.1f}"/>')
        body.append(_text(left - 12, py(tick) + 4, f"{tick:.2g}", 11, "end"))

    point_x = px(float(decision["success_a"]))
    point_y = py(float(decision["success_b"]))
    body.append(f'<circle cx="{point_x:.1f}" cy="{point_y:.1f}" r="6" fill="#111"/>')
    body.append(_text(point_x + 12, point_y - 10, "illustrative case", 12, "start"))
    body.append(_text(450, 92, f"Site B preferred when p_B - p_A > {threshold:.2f}", 14))
    body.append(_text(450, 116, "shaded region: repaired classification reverses the cheap-site rule", 12))
    body.append(_text((left + right) / 2, 492, "Site A intervention success probability (p_A)", 14))
    body.append(_text(22, (top + bottom) / 2, "p_B", 14, "start"))
    return _svg(width, height, "\n".join(body))


def render_all() -> tuple[Path, Path, Path, Path]:
    report = _report()
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    outputs = (
        (ARTIFACTS / "figure1_local_split.svg", render_local_split(report)),
        (ARTIFACTS / "figure2_transport_defect.svg", render_defect_curve(report)),
        (ARTIFACTS / "figure3_history_completion.svg", render_history(report)),
        (ARTIFACTS / "figure4_decision_reversal.svg", render_decision_reversal(report)),
    )
    for path, content in outputs:
        path.write_text(content, encoding="utf-8")
    return tuple(path for path, _ in outputs)


if __name__ == "__main__":
    for output in render_all():
        print(output)
