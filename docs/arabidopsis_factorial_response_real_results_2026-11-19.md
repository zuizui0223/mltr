# Arabidopsis accession-by-action predictive response audit — verified teaching mirror, 2026-11-19

**Result:** a *separate study source* from the preceding white-clover analyses shows positive **within-accession, held-out-rack prediction** for accession-specific fruit response to watering × microbial treatment. The accession×full-action signal is **exploratory**, not a genome/SNP effect and not exact MLTR state-transport validation.

## Provenance must not be misrepresented

- Exact data file: [UofTCoders/rcourse: data/Fitzpatrick_2018.csv](https://github.com/UofTCoders/rcourse/blob/master/data/Fitzpatrick_2018.csv), Git blob SHA-1 **8a79d0a5aa9e21854a556cd63c4afc5af6199b1c**, verified from GitHub's own content identity.
- Exact original *teaching-mirror CSV* SHA-256 **5872c228388bd6422458fa6f65a15e59e0ea283973ead376f5d3f7cd47ee485c**, **33,492 bytes**.
- Separate study: [Fitzpatrick, Mustafa & Viliunas, 2019](https://doi.org/10.1111/jeb.13426), with [original Dryad deposit](https://doi.org/10.5061/dryad.334765v). This paper reports **38 drought-experiment accessions, 760 plants**, and mentions excluding six accessions from the fitted drought analysis. The course mirror has **44 accession labels, 879 plants**, possibly representing an unfiltered precursor, **but byte-level equivalence to the published original Dryad full_data_drought.csv has NOT been established**.
- The course mirror contains **accession codes, not molecular genotypes**. Do not promote this pilot as species genomics. The source original already published microbial and drought effects on genetic-lineage fitness; this is a *prediction-sufficiency audit*, not a discovery of G×E.

## Direct source quality checks

| Source property | Observed |
| --- | ---: |
| Records, all fruit values nonnegative and observed | **879** |
| Nominal Arabidopsis lineage/accession codes | **44** |
| Watering treatments × microbial treatments | **4** |
| Independent rack/replicate labels | **5** (176, 176, 176, 176, 175 records) |
| Recorded zero fruit | **145** |
| Flowering-time readings unavailable (retained in fruit analysis) | **145** |
| Repeated accession × action × rack assignment | **1** |

No records were deleted to make the nominal accession × 4 treatments × 5 racks layout perfectly balanced. The original teaching CSV does not supply unique individual identifiers, so repeated experimental cell keys are **not proof of duplicate biological plants**.

Source treatment counts and fruit averages (*not* estimated lifetime seeds) are:

| Action | Plants | Mean fruit count |
| --- | ---: | ---: |
| D×L (dry, live inoculum) | 220 | 13.159 |
| D×S (dry, sterile inoculum) | 219 | 12.598 |
| W×L (watered, live) | 221 | 19.371 |
| W×S (watered, sterile) | 219 | 23.411 |

## Frozen five-rack prediction comparison

As committed to the source protocol **before testing genotype-specific response scores**, response is square-root fruit count and the score is held-out mean squared error (lower better). Each of five rack/replicate blocks is withheld entirely. The same genotype accessions, watering/microbe levels and experimental site occur in train and test: this is **not out-of-accession or out-of-study prediction**.

- P0: species-coarse mean response for each watering × microbial action.
- P1: P0 plus shrunken across-treatment accession baseline deviation (pseudo-count k_accession=10).
- P2: P1 plus shrunken accession × four-action residual (pseudo-count k_action=10).

| Model | Held-out transformed-fruit MSE |
| --- | ---: |
| P0 | 4.22075635 |
| P1 | 2.37533698 |
| **P2** | **2.17103823** |

Primary P2−P1 error reduction = **+0.20429876** transformed-fruit MSE units per test plant. P1−P0 error reduction = +1.84541936. P2−P1 conditional **accession-equal** average improvement = +0.20418825, with a fixed-prediction accession-bootstrap 95% interval **[+0.12048869,+0.29423497]** (2,000 accession resamples). **32/44 accession labels** have a positive within-label score change.

P2−P1 gain by held-out rack: **+0.282406, +0.164322, +0.223397, +0.161727, +0.189559**; all five positive. By treatment context: D×L +0.098108, D×S +0.114831, W×L +0.286099, W×S +0.317894; all four positive. Therefore this **course-mirror, original-specified exploratory P2 test** passes its frozen positive predictive gate.

These intervals are conditional on the observed 44 accessions and already-fitted five-fold predictions. They do not incorporate re-running a new experiment, new accessions, model uncertainty beyond this scheme, or the unknown original Dryad-vs-course crosswalk.

## Stricter post-result interpretation: do not confuse intercept repair with action response

The original P2's four action residuals have a small shared mean for an accession: P2 can partly correct **over-shrinkage of the P1 accession intercept**, not exclusively learn a treatment-response difference. This was noticed **after** inspecting the original positive result. An additional, explicitly *post-result sensitivity* subtracts the **training-cell-count-weighted within-accession mean of the four P2 offsets**. This forces the net accession shift to zero while preserving only action-to-action contrasts.

With unchanged k=10, the more conservative **action-centered** model has a P2−P1 held-out MSE reduction of **+0.05899715**, versus +0.20429876 uncentered. Five rack fold gains remain positive: **+0.114398, +0.024981, +0.064725, +0.064108, +0.026590**. **24/44 accessions** have positive individual-mean gains. Three of four treatment contexts are positive; dry-live is slightly negative (−0.006449). A separately coded 2,000-resample accession-mean bootstrap yielded an approximate conditional interval **[+0.0103,+0.1089]**; this is a post-result diagnostic interval and not a new confirmatory threshold.

Hence the defensible claim is **more modest than the original +0.204**: the observed course file retains some predictive value from accession-specific relative responses after correcting the accession-intercept aliasing, but the gain is small and not positive for every accession or action.

## Existing prior art and theory boundary

The original peer-reviewed study already reported genotype-dependent microbial and drought responses. This pilot's incremental output is an **inspectable held-out-rack predictive interface audit** with an explicit fine-label vs coarse-label comparison, not a new G×E discovery.

Likewise, this pilot does **not** prove MLTR's decision-sufficiency theorem, the existence of a non-nested source–target replacement relation, route-dependent carried labels, minimum history modes or a causal genomic locus effect. It uses only the source species label, nominal accession labels and action-conditioned observable fruit response. If the exact original Dryad matrix differs, the teaching-mirror results require a separate original-data rerun rather than silent reconciliation.

## Reproducibility

The [offline and GitHub source-locked analysis](../scripts/audit_arabidopsis_factorial_response.py) checks the original teaching Git blob identity and retains all 879 fruit observations. The [synthetic-only tests](../tests/test_arabidopsis_factorial_response.py) exercise source and prediction contracts. [GitHub Actions workflow](../.github/workflows/arabidopsis-factorial-response.yml) reads the public file, runs tests, and uploads **aggregate results only**.

Run without committing the original educational plant-level file:

    python scripts/audit_arabidopsis_factorial_response.py --from-public-github --out artifacts/arabidopsis_factorial_response_summary.json

## 2026-11-20 original published-source restriction audit

The source file 'full_data_drought.csv' was subsequently supplied by the user and directly read, with 760 rows from exactly 38 accessions in the complete four-action × five-rack design, plus one fruit missing value. All **759 valid original records** match the **759 shared 10-field records** in the 44-accession/879-record teaching mirror, which additionally contains six accessions (120 records). These are nested samples, not independent biological replications.

The original 38-accession, 759-valid-fruit restriction retains a P2−P1 **+0.18812556** reduction in five-rack-held-out MSE (five folds positive), down from +0.20429876 in the teaching mirror. However, a *post-result action-centered* P2 contrast yields only **+0.04684215**, with conditional 38-accession bootstrap interval **[−0.00154727,+0.09465540]** and one negative heldout rack. Original 38-accession treatment-choice gain is also **NOT SUPPORTED**: 14 changes across 189 complete panels, mean utility −0.05755883 (conditional interval crosses zero). See [complete original-source result](arabidopsis_original_dryad_38_reanalysis_2026-11-20.md).

The seed-per-fruit Dryad table still has not been directly read, so none of these quantities should be described as total lifetime seed fitness. The 38-accession original is **not** a new independent study for meta-analysis or a molecular-genomics test.

