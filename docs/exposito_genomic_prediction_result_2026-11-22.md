# Independent genomic prediction benchmark — Exposito-Alonso 2019

**Decision, 2026-11-22:** adding the published genetic-distance representation yields a small positive average prediction gain, but **does not pass the frozen primary stability criterion**. The conditional interval crosses zero and two of five outer folds have negative gain. The geographic sensitivity gives the same qualitative verdict. Preserve this result without selecting new models, scales or cohorts to obtain a positive outcome.

This is an independent experiment relative to the earlier Fitzpatrick Arabidopsis and white-clover datasets. It is a new computational analysis of an already published study, not a new discovery that Arabidopsis genomes respond to selection. The [source study](https://doi.org/10.1038/s41586-019-1520-9) already investigated genomic selection. No claim of causal variants, policy benefit or exact MLTR theorem validation follows from this benchmark.

## What was executed

The [protocol](exposito_genomic_prediction_protocol_2026-11-22.md) was committed at [`8bd3a0e`](https://github.com/zuizui0223/mltr/commit/8bd3a0ef77a6800fe5493a15461e1064fc8c30fa) before predictive scoring. Its SHA256 is `9dec1cdbe003cd4d586ad1bc122e261b61761b5b25aa8366452601ddc3b0b1f6`. Source structure, joins, measurement definitions and missingness had already been inspected; this was not a blinded or externally registered analysis.

| Source admission | Verified count or decision |
|---|---|
| Final D2 field panel | 517 accessions, including laboratory controls |
| Author genetic-distance object | 1,135 explicitly labelled accessions; a distance matrix, not a covariance matrix |
| Field accessions with genetic distances | 515 |
| Field accessions with all eight D4 contexts | 516 |
| Final intersection | **514 accessions × 8 contexts = 4,112 summaries** |
| Exclusions | Two accessions lack distances; one lacks the Madrid/low-rain/high-density summary |
| Preserved zero summaries | 518 |
| Geographic sensitivity groups | 65 fixed five-degree cells |

The canonical inputs are the final [Figshare v3 workbook](https://doi.org/10.6084/m9.figshare.6480599.v3) and the [author's archived distance object](https://github.com/MoisesExpositoAlonso/dryAR/blob/ddf703c91a01a990b8041f0aea9c94de119cd60b/data-cleaning/ibs1001g.rda). Both pass fixed byte-size and SHA256 admission checks. Final-workbook coordinates are used: four live AraPheno coordinate records differ from the final publication data. The 512-accession portal cohort supplies a crosscheck, not the cohort selection rule. Its 4,096 relative-fitness cells agree with the final workbook after one positive context-specific multiplier, with maximum absolute discrepancy 4.01e-9. Details are in the [source audit](results/exposito_genomic_source_audit_2026-11-22.json) and [source crosschecks](results/exposito_source_crosschecks_2026-11-22.json).

Each accession is held out across all eight site × rainfall × density contexts together. All fitted target scaling, coordinate transformations, genetic-kernel bandwidths, centering and tuning use the relevant training set, including inner folds. The primary uses five accession folds; the sensitivity keeps entire geographic cells together in both outer and inner validation. The study's externally constructed genetic-distance representation and published target summaries remain fixed upstream.

## Predictive results

The response is published estimated seed output per planted seed, divided by each fit's training-context mean. Errors therefore have **squared train-relative-fitness units**, not squared seed counts. Mean predicts the training-context mean; M0 uses quadratic collection coordinates; M1 adds the genetic kernel. Both fitted models select one lambda across all eight outputs by three-fold inner validation.

| Evaluation | Mean MSE | M0 MSE | M1 MSE | M0−M1 gain | Conditional 95% interval | Positive folds |
|---|---:|---:|---:|---:|---|---:|
| Primary accession holdout | 0.716511 | 0.699939 | 0.694101 | **+0.005837** | **[−0.003921, +0.016383]** | **3/5** |
| Geographic-cell sensitivity | 0.708807 | 0.703149 | 0.699510 | **+0.003639** | **[−0.003442, +0.011120]** | **3/5** |

M1's MSE is 0.834% below M0 in the primary and 0.518% below M0 in the geographic sensitivity. These are point-estimate error reductions. The intervals and fold signs do not establish a stable positive increment. Each split has its own training-relative denominators, so differences between the two rows are not a direct estimate of a transfer penalty.

The primary frozen conditions require positive pooled gain, a positive interval lower endpoint, positive gain in all five folds and both sites, and M1 beating Mean. Pooled gain, site means and the Mean comparison pass. **The interval and all-fold conditions fail.** The geographic sensitivity also fails those two conditions and cannot replace the primary.

### Context-specific gains

Positive values favor M1. These were prespecified descriptive breakdowns, not separately selected discoveries.

| Site | Rainfall | Density | Primary gain | Geographic sensitivity gain |
|---|---|---|---:|---:|
| Madrid | High | Single plant | −0.000219 | +0.000331 |
| Madrid | High | High density | −0.000074 | +0.000529 |
| Madrid | Low | Single plant | +0.003796 | −0.000232 |
| Madrid | Low | High density | +0.041963 | +0.027228 |
| Tuebingen | High | Single plant | +0.000490 | +0.000693 |
| Tuebingen | High | High density | +0.001928 | +0.003074 |
| Tuebingen | Low | Single plant | +0.001175 | −0.000560 |
| Tuebingen | Low | High density | −0.002360 | −0.001950 |

Both site-average gains are positive, but most pooled improvement comes from the Madrid low-rain/high-density context. Equal context weighting does not equalize the variance of train-relative outcomes. The full [aggregate result](results/exposito_genomic_prediction_2026-11-22.json) retains all losses, training denominators, tuning scores, selected lambdas, fold fingerprints and kernel diagnostics.

## What remains conditional

The target uses image-derived fruit/seed estimates and the authors' curation. The archived summarization code floors nonmissing `Fitness < 1` to 1 and replaces missing values with 0. The new pipeline does not reinterpret those source zeros or repeat the calibration.

There are 23,154 records but 22,779 distinct physical-pot keys in D3: 360 repeated keys contain different harvest-image records, producing 375 extra rows. Their outcome values differ; they are not exact duplicate records to drop mechanically. Arithmetic means of the published D3 `Fitness` reproduce all 4,135 D4 summaries within 4.73e-11. Thus the final targets retain that record structure. This work neither resolves its biological weighting nor claims independent plant-level target reconstruction.

The 2,000-draw intervals hold predictions, tuning, preprocessing and source summaries fixed. Primary resampling keeps each accession's eight contexts together. Spatial resampling keeps each cell together and preserves the accession-weighted denominator. Shared field effects, calibration error, refitting variation and uncertainty over a new experiment are not included. Accessions can remain related; grid cells are not independently established biological populations.

The permitted conclusion is narrow: **a stable incremental benefit of this genetic-distance kernel over this quadratic-coordinate baseline was not established in this experiment under the frozen benchmark.** This does not show that genetic variation has no biological effect, that a species label is sufficient, or that every genomic predictor must fail. No treatment policy was evaluated. Paper A, the earlier clover null result, and the earlier known-accession fruit/seed results remain unchanged.

## Computational verification

An independent implementation was written from the committed protocol without importing or first inspecting production prediction code. It reproduces both split modes. Comparison covers **452 numerical fields and 170 exact checks**, including inner tuning scores, training denominators, selected lambdas and fold/cohort fingerprints. Maximum absolute numerical difference is **4.44e-16**, with no failed checks. All five input arrays are exactly equal across independent and production preparation, despite different NPZ serialization bytes. The portable replay changes only CLI paths and acceptance/recording of the two verified container hashes; its 13 non-main function ASTs match the original independent script.

The [comparison audit](results/exposito_genomic_replay_comparison_2026-11-22.json), [independent aggregates](results/exposito_genomic_independent_replay_2026-11-22.json), and [independent replay script](../scripts/replay_exposito_genomic_prediction.py) preserve that check. It is computational replication of one experiment, not additional biological evidence.

All **30 new synthetic tests** pass: ten source-admission tests and twenty prediction/CLI tests. The full local project suite passes **137 tests and 16 subtests**, with one deprecation warning from the installed anyio pytest plugin. The tests include ID-axis alignment, preserved zeros, failed hash admission, held-out-target isolation, nested geographic grouping, kernel scaling and a hand-derived intercept/ridge solution. A separate review found no material scientific or reporting error. The dedicated CI workflow runs these empirical tests without downloading original study records.

Initial core-only CI failed during source-test collection because NumPy is intentionally absent from the theorem package's minimal environment. The source test now follows the existing optional-dependency skip convention; the dedicated empirical job installs NumPy and executes all 30 new tests. Rechecking an isolated environment with no NumPy gives **93 passed, five optional modules skipped and two subtests passed**. The full numerical environment still gives **137 passed and 16 subtests passed**. This integration correction changes test collection only; source preparation, prediction code, frozen protocol and numerical results are unchanged.

## Reproduce

Use an isolated environment with Python 3.11 or 3.12, NumPy, openpyxl and rdata. The recorded execution used Python 3.12.14, NumPy 2.3.5, openpyxl 3.1.5 and rdata 1.1.0. Obtain the two originals using the source URLs in `SOURCE_FILES` in the preparation script. Keep them and the prepared array file outside the repository.

```bash
python scripts/prepare_exposito_genomic_fitness.py \
  --workbook /path/to/S_DATASETS.xlsx \
  --ibs /path/to/ibs1001g.rda \
  --out-npz /path/to/exposito_prepared.npz \
  --out-audit /path/to/source_audit.json

OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
python scripts/analyze_exposito_genomic_fitness.py \
  --prepared /path/to/exposito_prepared.npz \
  --source-audit /path/to/source_audit.json \
  --protocol docs/exposito_genomic_prediction_protocol_2026-11-22.md \
  --output /path/to/prediction_result.json
```

Source preparation enforces original-file hashes. Prediction then verifies the prepared bytes against that source audit and records the actual source/protocol/code hashes; it does not independently authenticate a user-authored audit. Verify the reported protocol hash against the frozen value above when replaying. The committed results came from the pinned production preparation and unchanged frozen protocol.

For the independently implemented check on the verified prepared bytes:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
python scripts/replay_exposito_genomic_prediction.py \
  --input /path/to/exposito_prepared.npz \
  --protocol docs/exposito_genomic_prediction_protocol_2026-11-22.md \
  --output /path/to/independent_replay.json
```

The alternative eight-year RIL study remains at its [source-access and preprocessing gate](oakley_independent_source_gate_2026-11-22.md); no results from it are implied here.
