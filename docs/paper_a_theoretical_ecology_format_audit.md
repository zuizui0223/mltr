# Paper A — Theoretical Ecology submission audit

Audit refreshed: 2026-08-12.

This file supersedes the 2026-07-23 snapshot. The live scientific/format audit is also maintained in `docs/paper_a_format_audit.md`.

## Current verified state

- Paper A is framed as an ecological decision-sufficiency audit rather than a new generic refinement theorem.
- Main manuscript: 12 A4 pages.
- Supplement: 9 A4 pages.
- Abstract length: 226 words, within the journal's 150--250-word requirement.
- Six keywords are supplied.
- Author--year citations compile with no undefined citations.
- Four reproducible figures compile and render correctly.
- Main manuscript and supplement build successfully in GitHub Actions.
- CI and transport-core reproducibility pass on final manuscript/supplement head `bc40b4d28cb997da34c5239b0ce8d207d27e85a3`.
- Both PDFs were rendered and inspected page by page on 2026-08-12; no clipping, overlaps, missing figures, or broken glyphs were found.
- The supplement now uses the same article title, novelty boundary, monitoring interpretation, probabilistic decision layer, and route-context language as the main paper.
- `hidelinks` is enabled in the main manuscript and supplement.
- Internal figure titles are outside the artwork; descriptive wording is carried by manuscript captions.

## Remaining typesetting polish

The generic `article` class is still used. Before final submission, decide whether to migrate to the current Springer Nature `sn-jnl` template or reproduce the journal caption conventions explicitly.

The final generic build contains only minor box warnings:

- underfull boxes in the compact related-work table;
- one approximately 6.9-pt overfull main-text heading;
- one approximately 0.21-pt overfull supplementary line.

No warning caused visible clipping in the rendered PDFs. These are best removed during the final journal-template pass rather than by changing the scientific layout now.

## Author-supplied submission blockers

The repository cannot safely infer:

- complete author names and order;
- affiliations;
- corresponding-author email;
- ORCID identifiers if used;
- acknowledgments;
- funding statement / grant numbers or explicit no-funding statement;
- competing-interest statement;
- author-contribution statement;
- final archive/DOI for code and verification materials;
- final Data Availability wording tied to that archive;
- suggested reviewers if required by the submission interface.

## Current verdict

The main manuscript and supplement are **scientifically and technically ready for supervisor review**, but not yet formally submission-ready because author metadata, declarations, archival DOI/Data Availability, and final journal-template decisions are unresolved.
