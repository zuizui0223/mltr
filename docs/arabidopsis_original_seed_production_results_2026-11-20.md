# Original Arabidopsis drought study: estimated lifetime seeds and treatment choice

**Analysis date:** 2026-11-20. **Result: predictive improvement is scale- and fold-dependent; operational treatment-choice value NOT SUPPORTED.** The exact sources were supplied by the user as two independent CSV files from the same Fitzpatrick et al. (2019) drought experiment. This is a post-result phenotypic extension, **not a new ecological field experiment, a genomic-sequence analysis, or an empirical MLTR finite-theorem proof**.

## Source and biological units

Fitzpatrick, Mustafa & Viliunas, 2019, *Journal of Evolutionary Biology*, DOI 10.1111/jeb.13426; source Dryad DOI 10.5061/dryad.334765v. The original article explicitly estimates individual lifetime seed output in drought Experiment 2 as:

**estimated lifetime seeds = individual fruit count × accession-and-watering mean seeds per fruit**.

The latter is an estimate from a limited sample of fruits for each genotype×watering treatment, and was not individually counted for every plant. No extra soil-microbe-specific calibration is warranted from this seed table. Plant-level seed output is **reconstructed, not directly measured**.

| Uploaded source | Bytes | SHA-256 |
| --- | ---: | --- |
| full_data_drought.csv | 21,391 | 13ca229e6c97ee1a6d0333e4d32a66dabbf30a99e824a14c6f32bacad23067e3 |
| seed.count.drought.csv | 519 | e85b41b6da29d8d505e01d0d3213d7a38f7a2e62fdb78071c70bbf6a8d31351d |

All **38 source accession IDs join one-to-one** with exactly one seed-calibration row. Both wet and dry seeds-per-fruit means are present for only **33 accessions** (33 wet, 35 dry, 33 both). Missing wet means: genotypes 19, 50, 61, 62, 65; dry missing: 50, 62, 65. The primary analysis, frozen in the [protocol](arabidopsis_original_seed_production_protocol_2026-11-20.md) before evaluating fitted seed outcomes, restricts to those 33 with both watering levels to ensure a comparable four-action support. The 33 accessions provide 660 design rows; **one fruit count is missing**, leaving **659 observed estimated-seed outputs**. The 5 excluded accessions contribute 100 otherwise observed fruit counts.

**Selection warning:** 64/100 (64%) fruit observations in the excluded accession groups are zero, versus just 52/660 (7.9%) among the 33 fully calibrated groups. Thus the seed calibration is conspicuously incomplete among low-reproduction genotypes. These 33-accession results do **not** apply without qualification to the complete 38-accession drought experiment.

## Primary 659-record raw estimated-seed prediction

Reused the earlier frozen model class, using each of five whole rack blocks as holdout, train-only accession/treatment means and fixed pseudocounts k_accession=k_action=10. All models predict **raw estimated seeds per plant**, and mean squared errors are in **estimated seeds squared**.

- P0: training mean estimated seed output for each water×microbe treatment.
- P1: P0 plus shrunken accession-wide mean residual.
- **P2c (primary): P1 plus accession×treatment residuals centered to zero mean within an accession using the training cell frequencies.** This isolates relative treatment response from mere repair of an over-shrunken P1 baseline.
- P2u (legacy comparison): same P2 action deviations but without centering; it can partially adjust the accession intercept, so do not attribute all its improvement to differential treatment responses.

| Fitted model | Out-of-rack mean squared error in estimated seeds squared |
| --- | ---: |
| P0 | 386,885.260 |
| P1 | 269,953.732 |
| **P2c** | **258,481.432** |
| P2u (legacy, not pure treatment response) | 249,754.660 |

**Primary P2c over P1 MSE reduction: +11,472.300.** Conditional 33-accession bootstrap interval (2,000 resamples of already held-out predictions) approximately **[+3,369,+20,154]**, and the accession-equal mean gain is +11,473.47. Fold-specific reductions are +24,431.08, +5,102.93, +17,113.35, +10,743.31 and **−116.97** (rack 5). Action-specific gains: dry-live **−1,219.10**; dry-sterile +1,884.41; wet-live +33,732.93; wet-sterile +11,491.07.

**Predefined strict predictive gate: NOT SUPPORTED**, because 1/5 rack folds is negative even though the overall mean and conditional bootstrap lower bound are positive. The negative dry-live action is an additional sensitivity warning, but the frozen gate permits one of the four actions to be negative. Treat the fitted-model mean improvement as an observation, not a uniform response law.

The uncentered P2u gain (+20,199.07) would pass the numerical gate (5/5 positive), but it is not a pure accession×action response estimand: P2u can adjust accession-wide means. Do not promote this easier model as a stronger mechanistic result.

## Prespecified scale/support sensitivity (not independent data)

| Same 33 accessions/659 plants | P1 MSE | Centered P2 MSE | P2−P1 improvement | Interpretation |
| --- | ---: | ---: | ---: | --- |
| Raw estimated seeds | 269,953.732 | 258,481.432 | **+11,472.300** | 4/5 racks positive; strict gate fails |
| Sqrt(estimated seeds) | 90.679 | 88.379 | **+2.2995** | 5/5 racks positive; conditional 95% interval about [+0.446,+4.388] |
| Sqrt(fruit counts) | 2.2530 | 2.2118 | **+0.04126** | 3/5 racks positive; conditional interval about [−0.0067,+0.0962] |

The sqrt-seed comparison meets the *exploratory* numerical prediction gate on its own score scale. However, the outcome was **constructed using accession×watering mean-seed factors** from the same experiment, and thus contains genetic-identity/treatment structure by construction. The more modest same-individual fruit result weakens the case that this improvement is an independent *fruit-response* signal. No molecular genotype effects or new causal ecological mechanism are identified.

## Primary decision value: choose watering × microbial treatment

Before outcome-value comparison, choices were specified as exactly four laboratory treatments, all assumed **equally costly**. P0/P1 chooses the same predicted-best population-average raw seed-output action; P2c changes the choice only via relative accession×action estimates. Choices are learned on four racks and scored on the fifth, using **different plants in each treatment** for each accession×rack; there are no within-individual four-action counterfactuals.

- From 33×5 = **165** nominal accession×rack four-action panels, one panel was incomplete due to the original single missing fruit outcome. Thus **164 complete panels / 656 source fruit outcomes** were used in the choice comparison; the three observed rows in that incomplete panel are not evaluated as four-action options.
- P0/P1 chooses **well-watered + sterile microbes (W|S)** for all 164 complete panels.
- P2c instead chooses **well-watered + live microbes (W|L)** in **23/164 (14.0%)** panels; W|S is retained in 141.
- **Mean realized P2c choice − P0 choice: +5.6416 estimated seeds per panel.** Accession-equal mean +5.6074. Conditional 2,000-resample accession-cluster bootstrap 95% interval **[−77.82,+102.65]**.
- Mean choice gains by held-out rack: **+54.01, −79.96, +100.48, +22.02, −70.66** estimated seeds; only 3/5 racks positive. Across 33 accessions, 3 are positive, 6 negative, 24 ties.

**The predefined decision-value positive gate FAILS** because the conditional interval includes zero, despite a slightly positive point estimate. The data do not support claims that genotype-specific treatment selection either reliably improves or reliably harms seed production. Experimental irrigation and sterilization costs have not been measured, so these are not deployable conservation/management recommendations.

## Causal, measurement and source qualifications

1. The original publication already explains genotype×water-specific seed calibration and reports drought/microbial genotype fitness effects; no novelty claim for that phenomenon.
2. The seed table supplies genotype×water **averages estimated using other measured fruits within the same experiment** and does not identify calibration source racks. The held-out seed-output target is therefore *conditional on same-experiment calibration*; if the calibration includes the held-out rack's fruit samples, it is not a fully independent leave-one-rack-out seed measurement. This cannot be repaired with the provided aggregated seed table.
3. The missing seed factors are enriched in poorly performing accessions; excluding five entire accessions is a selection problem. Do not extrapolate to 38 source genotypes without additional data.
4. Neither the fruit measurements nor the seed multipliers contain SNP, structural genome markers or reconstructed phylogenetic ancestry. The accession label is a **categorical experimental genotype ID**, not a measured genomic locus.
5. Prediction accuracy, relative accession×action effect and cost-aware decision value are **distinct endpoints**. The estimated positive prediction gain and unconfirmed policy value do not prove any universal law or exact MLTR state-sufficiency obstruction.
6. User-uploaded raw files are kept outside GitHub. Their source hashes, documented measurement grain and aggregate results permit offline reanalysis. GitHub Actions synthetic tests cannot independently reprocess the two noncommitted originals.

## Reproduce

The exact source-hash-locked offline entrypoint is [scripts/audit_arabidopsis_original_seed_fitness.py](../scripts/audit_arabidopsis_original_seed_fitness.py). It reuses previously merged cohort parsing, score fitting, centered response effects and four-action choice functions and writes only aggregate JSON.

    python scripts/audit_arabidopsis_original_seed_fitness.py --fruit /path/to/full_data_drought.csv --seed /path/to/seed.count.drought.csv --out artifacts/arabidopsis_original_seed_estimates.json

See [structured source-backed results](results/arabidopsis_original_seed_production_2026-11-20.json) and [six synthetic-only data-quality/model tests](../tests/test_arabidopsis_original_seed_fitness.py). No changes to Paper A's canonical manuscript or finite mathematical theorems.
