# White clover: endpoint concordance and genomic-prediction failure-mode audit

**Date:** 2026-11-19  
**Status:** source-derived data-quality facts and exploratory sensitivity complete; **pre-frozen primary negative result unchanged**.

This note extends the [470-plant out-of-origin-population haploblock fitness analysis](clover_haploblock_fitness_holdout_result_2026-11-19.md). It does not open a new confirmatory phenotype, redefine the primary outcome, or claim an MLTR carried-label obstruction.

## Exact source and independent numerical replay

The original user-supplied [Dryad v20250829](https://doi.org/10.5061/dryad.dfn2z3593) ZIP has SHA-256 dc8fa8378176a063db4367e2fc4dd75914758a7246010e67b7ff7957e5632eb8c. As in the earlier analysis, both records sharing one conflicting specimen/BAM identifier are excluded before fitting, retaining **470 of 472 rows**, **93 source populations** and four gardens.

An independent Pandas/scikit-learn implementation reproduced the source-locked population GroupKFold predictions:

| Frozen model | Held-out log loss |
| --- | ---: |
| M0: garden + origin latitude / longitude | **0.628916** |
| M1: M0 + five haploblocks | **0.637734** |
| M2: M1 + garden × haploblock interactions | **0.647986** |

Primary M1−M0 predictive logscore gain is **−0.008818 nats/plant**, population-equal mean **−0.010128**. The earlier negative result is preserved, not changed or reconfirmed by a new biological sample.

## Source endpoints have different observable patterns

The source README defines FloweredFull as survival to flowering, FlowerHeadNumberFull as counted inflorescences and SeedSetMassFull as produced seed mass. The source fields can refer to different events or time intervals; these labels do not authorize assuming equivalence.

| Archived source comparison | Observed n | Lafayette | Montpellier | Toronto | Uppsala |
| --- | ---: | ---: | ---: | ---: | ---: |
| FloweredFull=1 but FlowerHeadNumberFull=0 | **43** | 0 | 0 | 36 | 7 |
| FloweredFull=0 but head count positive | **1** | 0 | 0 | 1 | 0 |
| FloweredFull=1 but SeedSetMassFull=0 | **59** | 3 | 0 | 39 | 17 |
| FloweredFull=0 but seed mass positive | **17** | 0 | 0 | 1 | 16 |
| FloweredFull=1 but Survived1st=0 | **20** | 6 | 2 | 9 | 3 |

These are **recorded disagreements**, not proof of entry errors. The first-year survival and full-experiment outcomes may refer to different events. Do not silently relabel the frozen FloweredFull outcome from the other columns.

## Haploblock genotype support is sparse

| Marker | Dosage 0 | Dosage 0.5 | Dosage 1 |
| --- | ---: | ---: | ---: |
| hb7a1 | 400 | 65 | **5** |
| hb7a2 | 391 | 71 | **8** |
| hb7b | 397 | 71 | **2** |
| hb9 | 321 | 118 | 31 |
| hb13 | 260 | 159 | 51 |

Only 2–8 alternative homozygotes occur in the first three haploblocks across all four gardens. This makes finely conditioned genotype × environment response estimation sparse. It does **not** show that any genotype has no biological effect.

## Exploratory sensitivity: selection for binary/count concordance

As a *nonconfirmatory* audit, discard 44 individuals whose FloweredFull binary state disagrees with whether FlowerHeadNumberFull is zero or positive. Retain the same M0/M1/M2 features, source-population GroupKFold=5, train-only geographical standardization and logistic C=1, but re-fit on **426 individuals** and **93 populations**.

| Model | 426-subset held-out log loss |
| --- | ---: |
| M0 | **0.620195** |
| M1 | **0.628936** |
| M2 | **0.633173** |

The M1−M0 mean score difference is **−0.008742 nats/plant**, with population-equal mean **−0.008777**. The garden-level differences are Lafayette −0.011737, Montpellier +0.002035, Toronto −0.016218 and Uppsala −0.000956.

**Interpretation boundary:** this subset is selected using an outcome-adjacent measure and changes the sample and fold membership. Its direction is consistent with the primary analysis, but it **cannot replace the original 470-plant frozen result**, cannot serve as independent replication, and does not diagnose a particular record as incorrect.

## Negative predictive gain is not negative genetic information

At a common target distribution and with optimal conditional forecasts, conditional mutual information satisfies

\[
I(Y;G\mid B)=H(Y\mid B)-H(Y\mid B,G)\geq 0.
\]

Here B is the coarse predictor, G is additional genotype. The reported result instead estimates the **finite fitted, out-of-origin-population predictive score difference**

\[
\widehat{\Delta}
=\frac{1}{n}\sum_i\left[
\log\widehat p_{\mathrm{M1},-p(i)}(Y_i)
-\log\widehat p_{\mathrm{M0},-p(i)}(Y_i)
\right],
\]

where the origin population of held-out individual i is excluded from training. This can be negative through limited data, sparse genotype classes, regularization, misspecification or shift across populations. The source does **not** identify which explanation dominates. Therefore the negative result neither refutes prior published genotype–fitness associations nor proves zero causal or conditional genomic information.

**What is supported:** in these four common gardens, five haploblocks did not improve the specified fitted model's prediction of flowering for unseen source populations. **What is not identified:** a general evolutionary law, genotype-driven fitness causality, new-garden generalization or an exact MLTR source–target/historical state law.

## Reproduce

The exact user-supplied original ZIP must be available to run this audit; raw individual genotypes and BAM IDs are not committed to GitHub. Install the existing clover empirical dependencies and run:

    python scripts/audit_clover_endpoint_integrity.py --zip /path/to/doi_10_5061_dryad_dfn2z3593__v20250829.zip --out artifacts/clover_endpoint_integrity.json

[Audit code](../scripts/audit_clover_endpoint_integrity.py) · [Synthetic-only checks](../tests/test_clover_endpoint_integrity.py) · [Aggregated evidence JSON](results/clover_endpoint_integrity_2026-11-19.json).

Next evidence beyond this same source requires **independent data with paired genotype × intervention/environment × fitness**, rather than post hoc optimization of alternate outcomes. The canonical MLTR Paper A manuscript and theorem set remain unchanged.
