# Original Arabidopsis drought experiment — seed-production extension protocol

**Frozen 2026-11-20 before examining estimated-seed model or action-value scores.** This is a post-result extension to the already analysed original 38-accession fruit dataset, not an independent experiment or exact MLTR theorem test.

## Sources and definitions
- Original user-supplied full_data_drought.csv: 760 records (38 accessions × four water/microbe actions × five racks), one missing fruit count; SHA-256 **13ca229e6c97ee1a6d0333e4d32a66dabbf30a99e824a14c6f32bacad23067e3**.
- New user-supplied seed.count.drought.csv: 519 bytes, 38 genotype rows, columns genotype / Seed wet / Seed dry; SHA-256 **e85b41b6da29d8d505e01d0d3213d7a38f7a2e62fdb78071c70bbf6a8d31351d**.
- The paper Fitzpatrick et al. (2019) doi:10.1111/jeb.13426 and Dryad doi:10.5061/dryad.334765v specifies the Experiment 2 estimate of lifetime seed production as **individual fruit count times genotype×watering-treatment mean seeds per fruit**. The genotype-water means came from approximately five fruits drawn from five individuals; they are **not** plant-specific seed counts. The soil microbe treatment does not get its own seed-per-fruit multiplier. Thus the product is *estimated* lifetime seed output; use these words, not directly measured seeds.
- Accessions are named lineages, not measured SNP or whole-genome genotypes. No ecological source–target replacement relation was measured.

## Source QC, primary denominator and selection
- All 38 original accessions appear exactly once in the seed calibration source. Wet values available for 33/38, drought for 35/38, both for **33/38**. Missing wet: 19, 50, 61, 62, 65. Missing drought: 50, 62, 65.
- The **primary cohort** is exactly the 33 accessions with both watering calibrations, chosen *without looking at model outcomes*, not imputed, to keep the same genetic support for all four candidate actions. They contribute 660 designed source records; one fruit observation is missing, giving **659** usable fruit-and-seed observations. All zero-fruit plants are retained as zero estimated seeds.
- The five incompletely calibrated accessions contribute 100 source records, **64 with zero fruits**, whereas the 33 fully calibrated accessions have 52 zero-fruit records among their 660 design cells. The complete-pair cohort can thus omit poorly reproducing genotypes. No claim of generality to all original 38 or worldwide Arabidopsis is permissible.
- The four-action **decision comparison** admits only accession×rack panels with exactly one observed fruit measurement in each D|L, D|S, W|L, W|S. One fruit-missing record leaves **164 complete four-treatment panels** from 33 × 5 = 165 possible.

## Frozen primary model and outcome
1. **Primary quantitative response = estimated raw lifetime seeds**, individually calculated as fruit count × source genotype-water mean seeds/fruit. Prediction units raw estimated seeds per plant. Train the previous *fixed* training-only model on each four-rack subset and predict the held-out rack:
   - P0 = training mean of estimated seeds in each of four water×microbe treatments.
   - P1 = P0 plus shrunken accession-wide residual (pseudocount k_accession=10).
   - **P2c = P1 plus shrunken accession×action residual with the training-cell-size-weighted mean offset forcibly zero within each accession** (k_action=10). This is the primary *relative action response* model; it cannot simply repair P1's accession intercept shrinkage.
   - For continuity, also report historical **uncentered** P2u, but do not use its effect as the main response-specific evidence.
   - **Primary prediction estimand:** held-out MSE(P1) minus MSE(P2c) in raw estimated-seeds-squared units. Positive means lower prediction error with accession-specific relative responses.
2. **Primary decision utility = raw estimated seeds**, equal treatment costs **assumed only for this retrospective laboratory check**. On the training racks P0/P1 select the same predicted-best global action (P1 adds a constant across actions), and P2c selects the action with the best accession-specific predicted raw seed total. Ties break D|L, D|S, W|L, W|S. In each complete held-out accession×rack panel, subtract the observed estimated seeds of the P0-choice plant from those of the P2c-choice plant (different individuals). Report the mean across 164 panels, the number of action changes, each rack, equal-accession mean, 2,000 fixed-policy accession-cluster bootstrap replicates (seed 20261120).
3. **Predefined scale and mechanism checks:** repeat P0/P1/P2c prediction on *sqrt(estimated seeds)*; evaluate prior fruit-only model P0/P1/P2c on the **identical 33-accession/659-record cohort** using sqrt fruit, so changes cannot be attributed only to selection. Do not search for a new best regularization/shrinkage value after results. All variants are descriptive and must not be substituted for the raw-seed primary.

## Positive claim gates and leakage caveat
- **Primary predictive gain supported only if** MSE(P1)−MSE(P2c)>0 overall, each of 5 rack-fold gains is nonnegative, the lower 95% fixed-prediction accession-cluster bootstrap limit>0, and at least 3 of 4 treatment cells gain. Otherwise **NOT SUPPORTED**.
- **Primary action-value gain supported only if** mean realized raw estimated seeds of P2c-vs-P0 choice is positive, the lower conditional accession-bootstrap limit>0, and at least 3/5 rack gains positive. Otherwise **NOT SUPPORTED**.
- Seed-per-fruit factors were estimated from the **same biological experiment** using only averages for accession×water; individual seed-calibration observations are not separated by rack in this file. They are **fixed across all cross-validation folds** and might contain information from plants in held-out racks. Therefore this is a within-experiment *conditional-on-calibration* prediction audit, not fully independent out-of-rack seed-fitness measurement or a new causal experiment.
- A favorable result cannot establish genotype genome causation, source-relative carried-label semantics, nonnested source–target replacement histories, exact MLTR decision sufficiency, or a reproducible cost-aware conservation policy. Original paper's G×E findings remain prior art.

## Execution contract
Implement offline source-SHA-locked script accepting both user-supplied originals, strict accession join and missingness, running primary and declared sensitivity models, reporting **aggregate-only** JSON. Add synthetic-only GitHub Actions tests. Do not redistribute original raw fruit/seed tables, individual outcomes or seed calibration rows. Passing CI tests without the user-uploaded originals does not prove real seed data have been processed by GitHub Actions.
