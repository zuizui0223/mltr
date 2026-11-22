# Frozen follow-up: does genomic similarity improve rainfall allocation decisions?

**Protocol frozen 2026-11-22 before running any source-derived decision outcome.** This is a **post-result** policy-value study on the same Exposito-Alonso et al. (2019) experimental data used for the existing genomic MSE benchmark. It is not a preregistered independent experimental replication or an exact MLTR source–target/history theorem test.

## Source and measurement boundary

The authenticated originals are exactly the 3,725,000-byte Figshare \`S_DATASETS.xlsx\` (SHA-256 \`032045433e3ace035977c11ff5d0ae8731335e8210c6cee14d64575ae0bebd05\`) and 8,947,948-byte labelled author genetic-distance object \`ibs1001g.rda\` (SHA-256 \`906724ce620a30a8c199ade07c5ffaa27aa7b1a91e8229f63b27e882547a70ad\`). Fetch them from the exact \`SOURCE_FILES\` URLs in the already merged source parser and **reject mismatched bytes**. The source's final D2/D4 summaries and explicit distance labels admit **514 accessions × 8 experimental site × rainfall × density contexts**. Reuse the exact preparation and cohort without deleting extra pot records, selecting accession subsets or refitting upstream seed estimates.

The outcome in D4 (\`Fitness\`) is the published **estimated lifetime seed production per planted seed**, averaged by accession/context. Its genotype-specific upstream calibration and duplicate pot-key structure were not independently remeasured or repaired. It is **not** directly counted lifetime seeds for each pot.

The Nature 2019 original field experiment manipulated high/low rainfall in Madrid (Spain) and Tübingen (Germany), with both single-plant and dense/population pots. Rainfall is the **only action** considered; site and pot density are fixed strata and are **not** actions. We do not imply measured irrigation cost or feasible management deployment.

## Models and held-out unit are frozen by the previous benchmark

- Use the already merged \`validate_arrays\`, \`accession_folds\`, \`spatial_folds\`, \`geographic_cells\` and \`fit_outer_fold\` implementation unchanged from \`scripts/analyze_exposito_genomic_fitness.py\`. For each held-out fold, all eight outcomes of that accession remain entirely outside model training and inner hyperparameter selection.
- M0: site-of-origin polynomial coordinates, trained kernel predictor.
- M1: the same coordinates plus published labelled genomic distance kernel.
- Fixed primary split: five accession-disjoint outer folds, exactly as prior PR #52. Geographic sensitivity: whole fixed five-degree origin-coordinate cells excluded together, with identical nested inner grouping.
- Model outputs from the existing code are **train-context-mean-normalized** and must be multiplied by **their own training-only eight-context raw \`Fitness\` means** before any rainfall action comparison. No cross-context decision may use a normalized value directly.
- The benchmark fits one lambda per model across all eight contexts, from the prior fixed grid; no new model tuning, feature engineering, calibration, scaling, outcome transformation or optimal weighting is permitted.

## Frozen policy and target

For every held-out fold **separately** within each of four **site × density** strata \`mi\`, \`mp\`, \`ti\`, \`tp\`:

1. Every held-out accession has observed (published aggregated) fitness for both high (\`h\`) and low (\`l\`) rainfall treatments. A hypothetical *high-rainfall treatment budget* allows exactly \`ceil(0.25 × heldout_accession_count)\` accessions to receive high rainfall in that stratum; the rest receive low rainfall. The quota applies separately to each held-out fold × stratum; M0 and M1 use the **same budget**.
2. For model m in {M0, M1}, calculate the predicted **raw** incremental benefit \`delta_hat_m = raw_prediction(m, h) − raw_prediction(m, l)\`. Choose the accessions with the greatest delta_hat for high-rainfall assignment. Break any exact ranking tie by ascending numeric accession ID (never by outcome). Policy assignment is allowed to inspect only identities, model predictions, fixed site/density labels, and the externally fixed quota. It must not inspect held-out target values.
3. For each selected accession use its *observed published mean Fitness* in h; for each unselected accession use its observed mean Fitness in l. Aggregate a paired difference \`d_i = Y_i[action_M1] − Y_i[action_M0]\`. If policies agree the unit has exactly zero difference.
4. **Primary policy estimand:** the equal-accession × equal-site/density mean \`d_i\` across **514 × 4 = 2,056** accession/stratum decisions in original, *unstandardized* estimated fitness units per planted seed. This is a retrospective **in-sample experiment policy comparison on held-out accession groups**, not a prospective test of treating those accessions next year. The underlying h/l outcomes were measured on different plants/pots, not both treatments of one plant.
5. Record per-fold differences, per-stratum differences, M0 vs M1 agreement rate, high-rainfall assignments, and policy realized mean. No specimen or accession-specific decisions are committed, only aggregate summaries. Report the policy value of each model vs the *same* fixed non-data-dependent quota assignment (sort numeric IDs) as a descriptive benchmark, but **M1 versus M0 is the sole primary contrast**.
6. A **secondary, non-decision metric** is squared-error improvement of predictions in original raw fitness units. It is descriptive, not the previous benchmark's normalized MSE estimand; do not substitute it as positive policy evidence.

## Uncertainty and acceptance rule

- **Primary interval:** 2,000 paired nonparametric bootstrap draws with seed \`20261124\` over **accessions**, keeping all four site×density policy differences for any accession together. Conditional on observed source targets, trained fits, selected allocations and fixed quotas. Use the percentile 95% interval with NumPy \`method="linear"\`. This *does not* recompute chosen sets or refit the model on bootstrap resamples; it does not quantify calibration, genotype family structure, future crops or treatment-cost uncertainty.
- Geographic sensitivity: use the same frozen geographic-cell split. For its interval, resample **whole five-degree geographic cells** while preserving accession-weighted denominators; again keep all four strata of an accession together.
- **Positive decision-value gate:** M1−M0 gain strictly positive overall, lower conditional 95% bound >0, at least **4 of 5** outer folds with strictly positive gain, at least **3 of 4** site×density strata with strictly positive gain, and at least one changed decision. This is a deliberately conservative descriptive stability rule, **not** a hypothesis-testing p value. If any condition fails, report **NOT SUPPORTED**, including if M1's prior MSE decreases.
- Reuse the same two original split modes, source cohort and published outcome. No post-result changes to rainfall quotas, site strata, tie breaking, action costs, targets, split definitions or model settings. The original Exposito prediction "NOT SUPPORTED" result remains unchanged; the new action objective is a different estimand and cannot retroactively pass its prediction gate.

## Execution and citation boundary

Use source-hash-locked GitHub Actions that downloads the two public original files **only at runtime**, verifies their exact pinned checksums, reuses existing preparation and frozen prediction functions, and uploads **only aggregated JSON**. The Python tests with synthetic factorial cohorts must verify held-out target isolation and tie handling and must not embed the source genotype or phenotype rows. The GitHub main repository should **not** receive original uploaded files or per-accession response/policy predictions.

The original study already examined natural selection and genotype-by-rainfall responses. Any policy result is a *new retrospective estimand* of these existing published summaries, not an independent ecological mechanism discovery, no randomized policy trial, no causal SNP proof, no deployment with real watering costs, and no exact formal MLTR minimal-history-mode validation.
