# Exposito genomic prediction implementation plan

> For agentic workers: use executing-plans for execution and verification-before-completion before completion claims. The user has authorized autonomous continuation and the established branch/PR/CI/merge workflow.

**Goal:** execute one source-pinned independent genomic prediction benchmark and preserve its actual result.

**Architecture:** a source-preparation script authenticates and joins the published workbook and labelled genetic-distance object. A separate NumPy-only prediction module performs frozen nested validation. Aggregate reports remain separate from source records and theorem code.

**Tech Stack:** Python, NumPy, openpyxl for source extraction, rdata for the published R object, unittest, existing GitHub CI.

**Spec:** [frozen protocol](../../exposito_genomic_prediction_protocol_2026-11-22.md).

## Global constraints

- Keep Paper A, theorem code, previous analyses and previous verdicts unchanged.
- No predictive scores until the protocol is committed. Source QC may inspect consistency, completeness and measurement definitions.
- No raw sample records or source binary files in git. No model/metric selection after scoring.
- Preserve conflicts in the individual-pot source as a limitation of the conditional published-summary target.

## Review focus

ID/axis alignment, distance versus similarity, fold isolation, training-only kernel/target transforms, nested tuning, an explicit intercept, matched kernel scale, conditional uncertainty, and claim boundaries.

## 1. Source contract and preparation

- Create `scripts/prepare_exposito_genomic_fitness.py` and `tests/test_exposito_genomic_source.py`.
- Accept the exact published workbook and RDA; fail on changed hashes, ambiguous IDs, invalid distances or malformed context keys.
- Extract final D2 coordinates and D4 Fitness; join by ID, preserve zeros, require eight contexts, and report exclusions and individual-pot key conflicts.
- Emit a local NPZ with `ids`, `coords`, `distance`, `fitness`, `contexts`, and a compact JSON source audit. Never infer the order of an unlabelled matrix.
- Verify synthetic misalignment/duplicate/missingness cases first; then verify the 514-accession real source join and the 512-accession AraPheno crosswalk.

## 2. Frozen prediction implementation

- Create `scripts/analyze_exposito_genomic_fitness.py` and `tests/test_exposito_genomic_prediction.py`.
- Implement deterministic accession/spatial splits, train-only kernels, nested tuning, all three model scores and conditional paired resampling.
- Test intercept-only prediction, invariance to held-out target changes, ID/fold coverage, whole-cell grouping, scaling invariance and rejection of invalid inputs. Use hand-checkable fixtures rather than mirroring implementation.
- Add `.github/workflows/exposito-genomic-prediction.yml` to run the empirical tests with isolated optional dependencies.

## 3. Run and interpret

- Execute the admitted source through both frozen split modes once; diagnose implementation failures without changing the estimand.
- Write `docs/results/exposito_genomic_prediction_2026-11-22.json`, compact source audit JSON, and `docs/exposito_genomic_prediction_result_2026-11-22.md`.
- Append the actual result and limitations to the species-genomics application gate. Retain the authenticated-download-blocked Oakley candidate as later work, not a completed replication.

## 4. Verify and integrate

- Run `python -m unittest discover -s tests -p 'test_exposito_*.py' -v` and the full existing `python -m pytest` suite in an isolated project environment.
- Obtain independent code/scientific review of the exact files and aggregate outputs. Address material issues and rerun the affected verification.
- Create the PR, inspect required checks on its actual head, merge after passing, and verify the resulting main commit. Report numbers, scope and remaining limitations in Japanese.
