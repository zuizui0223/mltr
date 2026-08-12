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
- history-preserving equivalences are an established formal topic (e.g. Montanari--Pistore 1997).

The current manuscript therefore does not claim those ingredients individually as new. Its publication-facing contribution is their ecological organization around the question of whether an inherited management state remains sufficient after declared structural change, plus the scoped route-coherence/minimum-context result.

## Confirmed technical status before the current run

- Main manuscript and supplement are editable LaTeX.
- Abstract remains within the journal's 150--250 word range after reframing.
- Six keywords are supplied.
- Author--year citations and bibliography are integrated.
- Internal hyperlinks use `hidelinks`.
- Figure titles are outside the generated illustrations; explanatory titles/captions are in the manuscript.
- Generated outputs are reproducible Actions artifacts rather than tracked working-tree products.

## New submission-facing additions

- Added the closest source-to-target abstraction-transfer precedent.
- Added targeted-monitoring and value-of-information ecological precedents.
- Reframed transport defect as structural representation complexity only.
- Added conditional repair information as a distinct distribution-sensitive quantity.
- Added a minimum monitoring-realization formulation over obstruction pairs.
- Added an illustrative probabilistic plant--pollinator decision reversal with explicit regret.
- Added a fourth reproducible SVG figure for the reversal region.
- Scoped the history claim against existing history-preserving formal theories.

## Formal submission gaps still requiring author-supplied information

1. complete author names and order;
2. affiliations;
3. corresponding-author email;
4. ORCID identifiers, if used;
5. acknowledgments and funding statement;
6. competing-interest statement;
7. author-contribution statement;
8. final public archive/DOI for code and verification materials;
9. final decision on Springer Nature LaTeX template migration and caption styling;
10. suggested reviewers if required by the submission workflow.

## Current scientific verdict

The remaining bottleneck is no longer theorem expansion. The formal core and replay are sufficient for a supervisor-facing draft. The next gate is whether the reframed manuscript survives CI/manuscript build and whether the new ecological positioning is judged strong enough for Theoretical Ecology. Further mathematics should be added only if it closes a concrete reviewer-visible gap.
