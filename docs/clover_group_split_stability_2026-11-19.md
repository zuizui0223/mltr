# White clover: population-split stability of a pre-frozen negative haploblock fitness test

**Source and date:** Battlay et al., user-supplied Dryad v20250829 ZIP, DOI 10.5061/dryad.dfn2z3593; analysis 2026-11-19. Original ZIP SHA-256 dc8fa8378176a063db4367e2fc4dd75914758a7246010e67b7ff7957e5632eb8c.

**Scientific status: post-result exploratory partition-sensitivity audit.** This is neither a new independent biological study nor a new test of the exact MLTR replacement-history or decision-sufficiency theorems. The previously merged source-verified negative M1-M0 fitness prediction is not replaced.

## Original frozen question and input cohort

Primary response is survival to flowering (FloweredFull). Pre-frozen M0 uses field garden plus geographic latitude/longitude of population origin; M1 adds five observed structural-variant haploblock genotypes (hb7a1, hb7a2, hb7b, hb9, hb13). Both are the same L2 logistic regression with C=1.0 and train-only coordinate standardization.

The same original 472 source rows are used, with both records for one contradictory repeated specimen/BAM identifier excluded before fitting. The analysis cohort therefore remains 470 plants from 93 origin populations and four existing gardens. No additional exclusions, imputation or feature tuning were introduced.

## Reference: independent reproduction of original GroupKFold=5 score

Using the source-hash-locked data reader and frozen feature/fit functions, the five origin-population-disjoint folds give:

| Fold | M1 minus M0 held-out logscore, nats / plant |
| --- | ---: |
| 1 | −0.01007398 |
| 2 | −0.00138181 |
| 3 | −0.00651450 |
| 4 | −0.00610494 |
| 5 | −0.02001440 |
| **470-plant weighted total** | **−0.00881793** |

All five folds are negative. This matches the previously recorded −0.008818 nats/plant to its quoted precision.

## New diagnostic: repeated origin-population-disjoint 80/20 splits

For each of 100 splits, randomly hold out 20% of the origin populations with GroupShuffleSplit, random seed 20261119. A held-out origin population is never present in model fitting. The average test set contains 19 origin populations / 94.8 individuals. M0/M1 response, predictors, regularization and logscore remain unchanged.

| Distribution across overlapping test splits | Individual-weighted gain (nats/plant) | Origin-population-equal gain |
| --- | ---: | ---: |
| Mean | **−0.00762423** | **−0.00760919** |
| Median | −0.00576346 | −0.00555959 |
| 2.5th percentile | −0.03147811 | −0.03113804 |
| 97.5th percentile | +0.00316532 | +0.00474356 |
| Minimum | −0.04004835 | −0.05198501 |
| Maximum | +0.00557424 | +0.00652236 |

**83/100** random splits yield a negative individual-weighted gain; **17/100** yield a positive gain. Only **12/100** splits have a positive gain in at least three of the four gardens. The latter is *not* the full pre-frozen positive-decision gate because it lacks the independent-population uncertainty criterion and many splits do not evaluate all gardens equivalently.

These splits overlap substantially. The quantiles are *descriptive variation across train/test assignments*, **not confidence bounds or a new P value**. The 100 is not an independent sample size, and the direction may differ under unseen gardens, independent studies or alternate source-ancestry distributions.

## Inference and uncertainty

The source supports the narrower claim that under the fixed, originally declared five-fold test, adding five haploblocks does not improve prediction of flowering for held-out origin populations. This negative result is *directionally frequent* under 100 post-result random holdouts but **not invariant across all possible training/test population assignments**. Reporting 83% negative is not a probability that a true genetic effect is absent.

The existing source-quality concerns remain: one conflicting specimen identifier; different source columns for flowering versus counted heads and seed mass; only 5, 8 and 2 alternative-homozygote plants at the first three haploblocks; and gardens differing strongly in survival-to-flowering rates. This sensitivity analysis does not establish which of these drives the negative gain. Original published haploblock-by-garden biological associations are prior art and are not overturned by an out-of-population prediction exercise.

## Reproducibility and decision boundary

1. Independently re-extracted the original ZIP and re-ran a simple independent reproduction of M0/M1 on the same 470 individuals, checking that the fixed five-fold weighted result exactly returns −0.00881793.
2. Independently cross-checked the separate script imported from main: same source/feature functions and random seed give identical repeated-group-split means, tails and negative counts.
3. A source-locked, offline, aggregated-only script is included at scripts/audit_clover_group_split_stability.py and synthetically tested in tests/test_clover_group_split_stability.py. It rejects a wrong original ZIP and does not write raw genotypes, outcomes for individuals, BAM names or population membership.

Reproduce with the original v20250829 Dryad archive (not committed):

    python scripts/audit_clover_group_split_stability.py --zip /path/to/doi_10_5061_dryad_dfn2z3593__v20250829.zip --out artifacts/clover_group_split_stability.json --repeats 100

Exact summary values are in results/clover_group_split_stability_2026-11-19.json.

**No Paper A change:** the exact finite source-relative MLTR interface, carried-label consistency and minimal-history-mode results are not tested by this population-genetics dataset. For an actual ecological decision-sufficiency test, the missing evidence is independently validated genotype-linked action-conditioned response under a declared source-to-target relation, not further tuning of these 470 records.
