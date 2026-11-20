# Arabidopsis experimental action-choice value: prediction improvement without confirmed decision improvement

**Analysed 2026-11-20.** Source-locked retrospective teaching-mirror analysis. **Result: DECISION VALUE NOT SUPPORTED** under the frozen action and value criterion.

## Evidence boundary and source provenance

The source was the University of Toronto R-course's 33,492-byte 'Fitzpatrick_2018.csv', SHA-256 5872c228388bd6422458fa6f65a15e59e0ea283973ead376f5d3f7cd47ee485c, Git blob 8a79d0a5aa9e21854a556cd63c4afc5af6199b1c. The course source contains 879 observations, 44 nominal Arabidopsis accession labels, 5 rack/replicate blocks, and a factorial water × microbial treatment. The original published Fitzpatrick et al. (2019) 38-accession/760-plant Dryad 10.5061/dryad.334765v matrix has **not been opened or byte-matched**. All conclusions in this note concern the course CSV only; 'accession' is not a measured SNP or causal genome variant.

This was an extension *after* a positive square-root-fruit predictive result had been identified, **not a new experiment or preregistered independent validation**. The action alternatives, panel restrictions, utility and acceptance criterion were fixed in the separate [protocol](arabidopsis_action_decision_protocol_2026-11-20.md) before examining the held-out action-choice values.

## Decision test

- Hold one complete rack out in each of 5 folds; fit the previous P0/P1/P2 predictors on the other 4.
- P0 = species-wide mean response per water×microbe treatment; P1 adds a shared accession intercept (thus picks the *same action* as P0); P2 adds accession-specific response residuals by action.
- Choose the predicted highest-utility action for that accession, treating all four laboratory treatments as **equal cost solely in the simulation**. No irrigation/sterilization cost data are available.
- Outcome utility = sqrt(number of recorded fruits), not seed output or population growth.
- For each accession × held-out rack, compare two observed treatments **in separate plants**. Admit only complete panels with exactly one observed plant in each action; ignore any cell with missing or repeated treatments independent of outcome values.

**Raw design balance:** 44 accessions × 5 racks = 220 nominal panels. **218 complete, 2 excluded** in rack 5 (one 3-cell panel; one 4-row panel with a duplicated action and another missing action), omitting 7 observations. Therefore 218 × 4 = 872 source observations were in complete panels.

## Measured decision outcome

| Quantity | Observed |
| --- | ---: |
| Previously verified held-out genotype×action P2 over P1 squared-error reduction | **+0.20429876** per plant |
| Complete matched accession×held-out-rack decision panels | **218** |
| P2 decisions different from P0/P1 | **16 / 218 (7.34%)** |
| P0/P1 chosen action | **W|S in all 218 panels** |
| P2 chosen action | W|S in 202; W|L in 16 |
| Mean held-out decision utility difference, P2 choice − P0 choice | **−0.05560812 sqrt-fruit units per panel** |
| Equal-accession-average gain | **−0.05510260** |
| Conditional 95% accession-cluster bootstrap interval | **[−0.13353002, +0.02219335]** |
| Accession-level gains | 2 positive; 6 negative; 36 zero |

The 2,000-resample accession bootstrap resampled entire available rack panels within each accession together (seed 20261120). It conditions on the five prefit policies and observed treatments and cannot be interpreted as a true across-experiment confidence interval. **The interval includes zero.** Thus the result does not establish that genotype-specific choices cause lower fitness; it establishes that **additional predictive detail has not improved this defined held-out decision metric**.

By fully held-out rack, P2−P0 realized utility was +0.01167260 (rack 1, 44 panels), −0.01878826 (rack 2, 44), −0.04575282 (rack 3, 44), −0.01817027 (rack 4, 44), and −0.21421110 (rack 5, 42). **Only 1/5 racks is positive**, failing the frozen 3/5 requirement, as well as the positive-gain and bootstrap-lower-bound requirements.

## Scientific interpretation

This is a particularly useful example for ecological **state reuse audits**: finer labels can improve response *prediction*, yet yield no reliable improvement in a specific *decision*. Even within a common sample frame, the operational objective determines which distinctions matter. The species-wide choice was W|S in every held-out panel. P2's more detailed learned response altered only 7.3% of choices, and those changes did not yield a positive average realized utility.

However, the MLTR framework's formal notion of carried-label decision sufficiency includes exact output, permitted-action and successor-state properties for a specified finite model. This experimental observation checks **only one equal-cost four-action choice objective** in a teaching data mirror. It does **not** identify a total nonnested source–target relation, prove a coarsest exact refinement, measure route-label coherence, establish minimum history modes, infer genotype-specific causation, or validate a theoretical theorem.

The four treatment outcomes in an accession/rack are measured from **different plants**, not four potential outcomes for the same individual. Environmental intervention costs, accession novelty, and independent source validation remain open.

## Reproducible code and validation

- [Protocol frozen before action choice](arabidopsis_action_decision_protocol_2026-11-20.md)
- [Source-locked decision script](../scripts/audit_arabidopsis_action_decision_value.py)
- [Six additional synthetic source/choice tests](../tests/test_arabidopsis_action_decision_value.py)
- [Machine-readable aggregate](results/arabidopsis_action_decision_value_2026-11-20.json)

GitHub Actions run **44678800488** passed the source-locked teaching-data audit and 14 combined Arabidopsis unit tests, reporting 218 complete panels, 16 changes, mean gain −0.05560812, and accession-bootstrap range [−0.13353002,+0.02219335]. An independent source extraction and JavaScript implementation gave the same 218 panels, 16 action reversals and mean utility difference. The bootstrap simulations use different random-number generators, so their endpoint values are not expected to be identical.

No raw specimen records, lineage response vectors or source CSV are committed to GitHub. Paper A and all mathematical theorems remain unchanged.

## Original-data admission still blocked

The actual related 2019 Dryad dataset [10.5061/dryad.334765v](https://doi.org/10.5061/dryad.334765v) publicly lists full_data_drought.csv (21.39 KB), seed.count.drought.csv (519 B) and analysis code. These **file bytes** have not been successfully accessed in this execution environment. A DOI landing page is not equivalent to opening original records. A publication-grade replication would first check original sample IDs, excluded genotypes, treatments, and fruit-to-seed conversion rather than silently relabel this education-source analysis as original-paper reanalysis.
