# Exposito-Alonso 2019 genomic prediction protocol — 2026-11-22

**Status at freeze:** source structure, joins, missingness and target provenance inspected; no predictive model scores computed. This is a new, retrospective analysis of a published independent experiment. It is not a registered replication of the authors' hypothesis tests or the earlier MLTR application proposal.

## Question and scope

Does an author-published genome-derived genetic-distance representation improve prediction of published accession-level fitness summaries beyond a fixed quadratic-coordinate predictor for held-out accessions in the existing experiment?

The primary task is prediction within the sampled panel and its eight observed environments. Geographic-cell holdout is a prespecified sensitivity. Neither split establishes transfer to an independently sampled biological population, a new experiment, or a new environment. This analysis does not evaluate a treatment-selection policy or exact MLTR source–target transport. Paper A and all earlier empirical verdicts remain unchanged.

## Sources and admission

- Study: [Exposito-Alonso et al. (2019), Nature](https://doi.org/10.1038/s41586-019-1520-9).
- Canonical phenotypes and coordinates: final [Figshare supplementary datasets v3](https://doi.org/10.6084/m9.figshare.6480599.v3), file `S_DATASETS.xlsx`, SHA256 `032045433e3ace035977c11ff5d0ae8731335e8210c6cee14d64575ae0bebd05`.
- Genetic distances: [`dryAR` published commit](https://github.com/MoisesExpositoAlonso/dryAR/tree/ddf703c91a01a990b8041f0aea9c94de119cd60b), `data-cleaning/ibs1001g.rda`, SHA256 `906724ce620a30a8c199ade07c5ffaa27aa7b1a91e8229f63b27e882547a70ad`.
- [AraPheno study 34](https://arapheno.1001genomes.org/study/34/) is an independent representation of the same study for crosschecking, not an independent biological replicate or the cohort definition. Its 512 × 8 relative-fitness cells agree with the final workbook up to one positive context-specific multiplier within absolute tolerance 1e-8. Final-workbook coordinates take precedence over live portal metadata.

Use the exact intersection of final D2 accession metadata, labelled genetic-distance rows/columns, and complete D4 `Fitness` across all eight site × rainfall × density contexts. Preserve reproductive zeros. Do not select subjects or features using prediction performance or fitness associations. The source audit identifies **514 eligible accessions × eight contexts = 4,112 summaries**, including the two laboratory controls present in the final study. Of 517 field accessions, two lack genetic-distance records and one lacks a phenotype context. Report those exclusions without imputing the absent outcomes.

The source distance object is 1,135 × 1,135 with explicit matching row/column IDs, finite nonnegative entries, exact symmetry, and zero diagonal. It is a **distance**, not a covariance matrix. No off-diagonal zero distance occurs in the admitted 514-accession cohort. Stop if this condition changes; do not claim unseen measured genotypes from a split that separates identical profiles.

The target is the authors' published estimated seed output per planted seed, aggregated by accession and context. Its measurement and summary construction are fixed upstream. The individual-pot table has 360 repeated keys with conflicting outcomes (375 extra rows); this analysis does not silently deduplicate them or claim to reconstruct independent plant-level targets. Shared image calibration, aggregation and measurement uncertainty are outside the new predictor's validation.

## Frozen models and loss

Order accessions by numeric source ID and contexts lexicographically as `mhi`, `mhp`, `mli`, `mlp`, `thi`, `thp`, `tli`, `tlp`. Here m/t denote Madrid/Tuebingen, h/l rainfall, and i/p single-plant/high-density pots.

For every fit, divide each context's target by its **training-accession arithmetic mean**. Stop if a training mean is nonpositive or nonfinite. This defines train-relative fitness; a common positive source multiplier cancels exactly. It does not undo nonlinear image calibration, shifts, or aggregation. Keep all eight outputs separate, with separate fitted response coefficients but one shared tuning parameter per model per outer fold.

1. **Mean:** predict one in each train-relative context. It has no fitted tuning parameter.
2. **M0, coordinates:** standardize latitude and longitude using training means and population standard deviations. Form `[lat, lon, lat², lat×lon, lon²]`, then center and standardize each basis column using training data. A constant column becomes zero. Its dot-product kernel is centered on training samples and scaled to unit mean training diagonal when nonzero.
3. **M1, coordinates plus genetics:** add a genetic kernel `exp(-D/tau)`, where `tau` is the median strictly positive off-diagonal distance among training accessions. Center it using training row/column/grand means and scale it to unit mean training diagonal when nonzero. Normalize the sum of geographic and genetic components again to unit mean training diagonal. With both nondegenerate components this is `(Kgeo + Kgen)/2`, so M0 and M1 have the same total kernel scale.

For either fitted model, with n training accessions, solve

`alpha = (K_train + n*lambda*I)^(-1) (Y_train_relative - 1)`

and predict `1 + K_test,train @ alpha`. Clip predictions below zero to zero in both models. The explicit intercept is one because each training-context target has mean one. Newly fitted preprocessing uses only the corresponding training fold, including inner folds.

Check each training genetic kernel for numerical positive semidefiniteness. Reject a minimum eigenvalue below `-1e-8 * max(1, largest_eigenvalue)`. Do not silently repair a materially indefinite kernel using the full cohort. Numerical eigensolver noise within that tolerance is recorded, not outcome-selected.

Select lambda independently for M0 and M1 from `[0.01, 0.1, 1.0, 10.0]` by three-fold inner validation. Minimize equal-accession × equal-context mean squared error in each inner fit's train-relative units, pooling all validation accessions rather than averaging unequal-sized fold means. Use the larger lambda for a tie within absolute 1e-12. There is one lambda across all eight contexts; do not tune separate context models, genomic weights or bandwidth grids.

## Splits, uncertainty and decision rule

- **Primary:** five accession-disjoint outer folds. Sort IDs numerically, permute indices with NumPy PCG64/default_rng seed 20261122, and partition with `array_split` into five held-out sets. Within outer fold k (one-based), construct three inner folds the same way with seed `20261122 + k`. All eight contexts of an accession stay together.
- **Geographic sensitivity:** assign the final coordinates to fixed cells `(floor((latitude+90)/5), floor((longitude+180)/5))`. Keep whole cells together. Sort groups by decreasing sample count, break ties lexicographically by the integer cell pair, and assign each group to the lowest-count fold (lowest fold index breaks ties). Use five outer and three inner grouped folds. The inner grouping matches this spatial prediction task.
- **Loss:** MSE on the corresponding training-relative fitness. The primary gain is `loss(M0) - loss(M1)`; positive means M1 is better. Give each accession and each context equal weight. Relative scaling does not equalize context variance; report all eight context results, both sites, five folds, and comparison with the mean predictor.
- **Intervals:** 2,000 paired bootstrap draws, resetting seed 20261123 for each split mode. Report percentile 95% endpoints with `np.quantile(draws, [0.025, 0.975], method='linear')`. For the primary, resample accession-level means with all eight contexts intact. For the spatial sensitivity, resample geographic cells and compute the accession-weighted mean from each resampled set of cells. Predictions, fitted preprocessing, tuning and upstream summaries remain fixed. These are conditional descriptive intervals, not uncertainty over new experiments, refits or source populations. Related accessions and shared field effects can remain dependent.
- **Primary numerical gate:** positive mean M1 gain over M0, positive lower endpoint of its conditional 95% interval, positive gain in all five outer folds and both sites, and lower pooled MSE for M1 than the mean predictor. All conditions are required. This gate is a stability criterion for this benchmark, not a significance test or the earlier empirical sufficiency criterion. The geographic sensitivity cannot replace a failed primary.

Only M1 versus M0 is the primary contrast. Do not infer a new causal genotype–fitness effect or genomic sufficiency from this comparison. A gain can reflect fine geographic structure not represented by the quadratic baseline. Preserve a null/negative result; do not revise models, cohorts, scales or splits after scoring to obtain a positive gate.

## Reproducibility and stopping rule

Keep original source records outside the repository. Commit the source contract, preparation and prediction scripts, meaningful synthetic tests, aggregate results and interpretation. Record exact source hashes, cohort/fold fingerprints, software versions, selected lambdas, model losses and the protocol file hash. Source admission failures stop scoring and are reported explicitly. Finish with an independent methodological/code review, targeted empirical tests, the existing project suite, and CI before merging.
