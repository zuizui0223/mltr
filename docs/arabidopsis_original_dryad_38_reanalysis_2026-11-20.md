# Original Dryad 2019 Arabidopsis drought study: 38-accession predictive and action-value reanalysis

**Analysis date:** 2026-11-20. **Source:** user-supplied original file full_data_drought.csv (21,391 bytes, SHA-256 **13ca229e6c97ee1a6d0333e4d32a66dabbf30a99e824a14c6f32bacad23067e3**), corresponding in size, schema and design to [Fitzpatrick, Mustafa & Viliunas (2019), Dryad 10.5061/dryad.334765v](https://doi.org/10.5061/dryad.334765v). This file has **not** been independently downloaded from Dryad for a second byte-level checksum; reproducibility is by the *exact supplied SHA*.

**Primary conclusion:** in original 38-accession data, additional accession×action response residuals improve the specified held-out-rack fruit prediction, but the experimentally observed **action-choice utility improvement remains unsupported**. The stricter pure treatment-response sensitivity is also uncertain. These original observations are a **subset of**, not an independent replication of, the earlier 44-accession teaching mirror.

## 1. Exact original-source audit and teaching mirror crosswalk

Original CSV: **760 rows**, **38 accession codes**, 4 treatments (water D/W × microbe live L/sterile S), **5 racks** of 152 rows each. The original design is exactly 38×4×5 and all accession×treatment×rack assignments occur exactly once. **One fruit count is missing**, leaving **759 available fruit observations**; no missing fruit value is imputed. The original column source (seed-stock origin) has categories ut (620 rows) and abrc (140 rows); it is **not** a sequenced SNP marker or an invented genetic-ancestry estimate.

The [University of Toronto course file](https://github.com/UofTCoders/rcourse/blob/master/data/Fitzpatrick_2018.csv) has 879 rows / 44 accession codes. Directly comparing *all ten shared non-source fields* in canonical order establishes that **759/759 measured original rows are present in the education mirror with identical source fields**, with one original missing-fruit row omitted and **120 rows from 6 additional accession codes** added to the mirror. The source-mirror Git blob is 8a79d0a5aa9e21854a556cd63c4afc5af6199b1c. Canonical original and mirror 759-row content was independently hashed in two execution environments: FNV64 e1d4fedfdfdb3a4f, and **SHA-256 d84f3b4a78c1d65860c9d9f5b14afbd09b05a16f734bae6237f34d6e3767fe8f on BOTH sources** (canonical 17,969-byte UTF-8 representation). This is a cryptographically matched full-record-content crosswalk, not a match inferred from only sample counts.

**Therefore the 44/879 prior results and this 38/759 restriction are two analyses of nested biological observations, NOT independent datasets, and must never be counted as replication across studies.**

## 2. Original 38-accession held-out fruit prediction

Retain the previous fixed model definition and regularization: square-root *fruit count* response, leave exactly one rack out per fold, pseudo-count k_accession=k_action=10, train-only treatment and accession means. The measured accession codes are only identity labels; no molecular genotypes appear in this dataset.

- P0: mean of the four watering×microbial treatments.
- P1: P0 plus shrunken accession baseline across the four actions.
- P2: P1 plus shrunken accession×action residuals.

| Model | Original 759 valid-fruit, held-out-rack mean squared error |
| --- | ---: |
| P0 | 4.16846716 |
| P1 | 2.36159502 |
| **P2** | **2.17346946** |

P1 over P0 improvement is **+1.80687214**, and P2 over P1 improvement is **+0.18812556** MSE units (lower MSE is better). Each held-out rack has a positive P2−P1 improvement: **+0.26063949, +0.13095965, +0.24101439, +0.13887652, +0.16901203** (n=152/152/152/152/151). The accession-equal conditional mean is +0.18799502; 27/38 accessional means are positive. The 2,000-resample **fixed-prediction accession-cluster** bootstrap interval is approximately **[+0.10873305,+0.27793677]**. This is conditional on the original 38 accessions and fixed model fits, not a new independent experiment.

The original Fitzpatrick et al. article already reported genetic-lineage×drought/microbial responses. Our new output is an explicitly source-locked held-out *predictive* comparison, not discovery of new biological G×E.

### Post-result source-independent mechanism check: action-only centering

The uncentered P2 layer may also repair a P1 accession-average intercept over-shrunk by the k=10 pseudo-count. The additional treatment-only diagnostic subtracts each accession's training-count-weighted mean P2 action residual, leaving **no net accession-wide intercept change**. This check was introduced only **after** the prior teaching-source positive result; it is NOT a preregistered independent outcome test.

At k=10 the centered P2 held-out MSE is **2.31475287** and improvement vs P1 **+0.04684215**, substantially smaller than +0.18812556. Fold gains are **+0.10417172, −0.00090776, +0.07643077, +0.04770316, +0.00654776**; 4/5 positive. Accession-equal conditional mean is +0.04693515; its conditional bootstrap interval is **[−0.00154727,+0.09465540]**, crossing zero. Only 21/38 accession means improve.

**Therefore robust pure action-response information beyond the accession baseline is not confirmed by this stricter post-result check.** An uncentered P2 improvement is a supported *finite fitted-prediction* result, not a free-standing proof of strict genotype×treatment interaction.

## 3. Original 38-accession matched experimental action-choice utility

Reuse the prior independently declared equal-cost four-action choice policy and P0/P2 prediction methods without tuning. The original design permits **190** accession×rack four-action panels. One panel is incomplete in *observed fruit* because a W|S fruit count is missing: exclude its three otherwise observed fruit records from the matched four-action policy assessment. **189 complete panels** and **756** corresponding observed individual plants remain.

Each action is observed on a **different experimental plant** from the same accession×rack, rather than four counterfactual outcomes on one plant.

| Action-choice outcome (utility = sqrt fruit count) | Original Dryad result |
| --- | ---: |
| P0/P1 choose W|S (watered/sterile) | 189/189 panels |
| P2 changes choice to W|L (watered/live) | **14/189 panels (7.41%)** |
| P2 still chooses W|S | 175/189 |
| P2 choice − P0 choice, mean held-out utility | **−0.05755883** |
| Equal-accession average | −0.05725589 |
| Accession-cluster conditional 95% interval (2,000 resamples) | **[−0.14624606,+0.03777653]** |
| Accession-level positive / negative / tie | 1 / 6 / 31 |

Held-out rack mean utility differences were +0.00508507, −0.04220546, −0.05297695, −0.02103926, −0.17987643. **Only one of five racks improves.** The frozen exploratory positive-decision gate (positive mean, lower conditional bound >0, and at least 3/5 positive racks) **FAILS**. The interval includes zero; do not claim that detailed state information causes lower fitness or is necessarily harmful.

The original course-mirror result (218 panels, 16 action changes, −0.05560812 utility gain) points in the same direction because this original 38-genotype dataset is nested within it. This is a *sampling restriction robustness result*, not independent biological replication.

## 4. Scientific synthesis and exact MLTR claim firewall

Three distinct objects must be separated:

1. **Measured lineage and treatment heterogeneity:** documented in the original publication and visible in the original plant-by-action file. *Accession IDs are not nuclear variant measurements*.
2. **Fitted model predictive gain:** uncentered P2 improves held-out rack MSE (+0.1881), but a more targeted action-centered gain (+0.0468) is weaker and its accession bootstrap interval includes zero.
3. **Operational action choice:** finer P2 predictions alter 14/189 optimal equal-cost treatment choices, but do not yield a supported increase in realized fruit utility (−0.0576; conditional interval spans zero).

This demonstrates **for the specified fitted models and retrospective decision objective** that response prediction, strict treatment-response signal, and decision value are not interchangeable. It does **not** prove the true mutual information conditional on the coarse state is zero, a causal genetic mechanism, novel fitness adaptation, a complete ecological decision policy, or the exact finite MLTR carried-label/obstruction/history-mode theorem.

The *original 38-genotype data* and previous 44-genotype teaching data must NOT be counted as separate studies when reporting universality or meta-analysis.

## 5. Reproduction and source limits

Use the [source-hash-locked original-file script](../scripts/audit_arabidopsis_original_dryad_38.py) with the user-supplied original bytes. It reads and verifies original source contents, excludes only the single missing fruit value, reuses the already merged P0/P1/P2 model and action-choice functions, and outputs **only aggregate results**, no individual rows or accession×outcome keys.

Command:

    python scripts/audit_arabidopsis_original_dryad_38.py --input /path/to/full_data_drought.csv --out artifacts/arabidopsis_original38_summary.json

For the **optional exact course-mirror comparison**, if network access is available:

    python scripts/audit_arabidopsis_original_dryad_38.py --input /path/to/full_data_drought.csv --compare-course-public --out artifacts/arabidopsis_original38_with_course_crosswalk.json

[Six synthetic tests](../tests/test_arabidopsis_original_dryad_38.py) guard source hash, complete design, missing fruit, invalid cell duplicates, and accidental inference of verified mirror identity. **GitHub Actions does not have the original uploaded CSV; passing CI tests does NOT establish that CI reran the real 760-row source.** All original-source quantitative figures were recomputed within this conversation using the uploaded file, independent of the teaching data model code, and recorded as aggregate JSON in [results](results/arabidopsis_original_dryad_38_2026-11-20.json).

The user-uploaded original source has the expected published file size, exact schema and balanced design but has not been independently downloaded from Dryad and byte-compared to a second copy. This is a remaining provenance qualification, not a reason to relabel the row-level crosswalk or model result.
