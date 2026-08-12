# Paper A format audit against Theoretical Ecology submission guidelines

Audit date: 2026-08-12

Official source checked: Theoretical Ecology, Springer Nature, submission and journal guidance.

## Scientific-positioning update

The manuscript has been reframed from a theorem-first claim about source-relative coarsest repair to an ecological **decision-sufficiency audit of inherited state classifications**.

This change was required by closer prior-art review:

- arbitrary-initial-partition coarsest refinement is established (Paige--Tarjan; Givan--Dean--Greig);
- state abstractions have been explicitly transferred from source MDPs to target MDPs (Walsh--Li--Littman 2006);
- targeted ecological monitoring from state-and-transition models is established (Jones et al. 2023);
- value-of-information analysis already links information acquisition to management consequences and cost (Canessa et al. 2015);
- history-preserving and path-sensitive formalisms are established topics.

The current manuscript therefore does not depend on claiming any one generic mathematical ingredient as newly invented. Its publication-facing novelty is ecological and integrative: audit an inherited management state after declared structural/intervention change, identify the hidden distinction when it fails, translate that distinction into a monitoring requirement, separate representation complexity from decision consequence, and retain route context only when it changes present operational meaning.

## Final verified technical state

Final manuscript/supplement head: `bc40b4d28cb997da34c5239b0ce8d207d27e85a3`.

- CI: pass.
- Transport-core reproducibility: pass.
- Manuscript build: pass.
- Main manuscript and supplement are editable LaTeX.
- Main manuscript: 12 A4 pages.
- Supplement: 9 A4 pages.
- Abstract: 226 words, within the journal's 150--250-word range.
- Six keywords are supplied.
- Author--year citations compile with no undefined citations.
- Four reproducible figures compile and render correctly.
- Internal hyperlinks use `hidelinks`.
- Figure titles are outside the generated illustrations; explanatory wording is in manuscript captions.
- Main and supplement were rendered and inspected page by page: no clipping, overlap, broken glyphs, or missing figures.
- Supplement title, proofs, algorithms, reproducibility notes, and examples now use the same decision-sufficiency and prior-art boundary as the main paper.
- Generated outputs are reproducible Actions artifacts rather than tracked working-tree products.

## Submission-facing additions completed

- Added the closest source-to-target abstraction-transfer precedent.
- Added targeted-monitoring and value-of-information ecological precedents.
- Reframed transport defect as structural representation complexity only.
- Added conditional repair information as a distinct distribution-sensitive quantity.
- Added a minimum monitoring-realization formulation over obstruction pairs.
- Added an illustrative probabilistic plant--pollinator decision reversal with explicit regret.
- Added a fourth reproducible SVG figure for the reversal region.
- Scoped route/history language against existing history-sensitive formal theories.
- Updated the manuscript-build workflow so the SVG conversion list is derived from figure references in the manuscript rather than hard-coded.

## Remaining typesetting polish

The generic `article` class is still used. Remaining TeX warnings are visually harmless:

- underfull boxes in the compact related-work table;
- one approximately 6.9-pt overfull main-text heading;
- one approximately 0.21-pt overfull supplementary line.

These are best removed during the final Springer Nature template/caption pass rather than by destabilizing the supervisor-review draft.

## Formal submission gaps still requiring author-supplied information

1. complete author names and order;
2. affiliations;
3. corresponding-author email;
4. ORCID identifiers, if used;
5. acknowledgments and funding statement;
6. competing-interest statement;
7. author-contribution statement;
8. final public archive/DOI for code and verification materials;
9. Data Availability wording tied to that archive;
10. final decision on Springer Nature LaTeX template migration and caption styling;
11. suggested reviewers if required by the submission workflow.

## Current scientific verdict

The formal core, ecological reframe, decision example, monitoring bridge, supplement, and reproducibility pipeline are now sufficient for a supervisor-facing manuscript. The next scientific gate is supervisor evaluation of the ecological framing, not further theorem expansion. Formal journal submission should wait for author metadata, declarations, archive/Data Availability, and final template decisions.
