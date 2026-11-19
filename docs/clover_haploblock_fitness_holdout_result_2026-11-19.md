# White clover: held-out population haploblock prediction fails to improve flowering survival

**Status (2026-11-19): completed empirical source audit and pre-frozen predictive comparison. Primary M1 increment: NOT SUPPORTED.** This is an *observational model-transfer* result inside four published common gardens, not a null causal effect of structural variation, a new result on the existence of haploblock-fitness associations, or proof of MLTR's mathematical theorems.

## Original source and admissions

Battlay et al. *Trifolium repens* common-garden data, [Dryad DOI 10.5061/dryad.dfn2z3593](https://doi.org/10.5061/dryad.dfn2z3593), user-supplied version **v20250829**. The original ZIP was directly inspected and contains `DatasetA_commongarden.csv` and `README.md`, no other files.

| Fingerprint | SHA-256 |
| --- | --- |
| original ZIP (45,396 bytes) | `dc8fa8378176a063db4367e2fc4dd75914758a7246010e67b7ff7957e5632eb8` |
| original CSV (41,152 bytes) | `cbd9691e4b07a48e97619385bedc9f9a45fb02164d4ce08c1a99c9af7df054d4` |
| README (3,970 bytes) | `72b966bbd7326a36cac14294c91dc15f3e4878e6ff7ae4c4289a3da531a83131` |

The archived CSV uses **lowercase** haploblock field names `hb7a1`, `hb7a2`, `hb7b`, `hb9`, `hb13` (the README capitalizes the displayed labels). All five are observed and code dosage `0/0.5/1`. The primary binary response `FloweredFull` has no missing values among the 472 source rows. Other study variables such as growth rate and first-year survival are not predictors or used to select outcomes.

**Source integrity failure and fixed resolution:** one `.bam` identifier appears on **two** CSV rows (source lines 431–432). The two rows share source population, garden and fitness outcomes but disagree in both `hb9` and `hb13`. Choosing one genotype would be arbitrary. **Both conflicting rows were excluded before fitting**, rather than deduplicating by phenotype or averaging dosage. Sensitivity analyses retaining exactly the first or second record are reported separately; neither alternative changes the negative primary result. No individual specimen identifiers or raw genotype vectors are committed to GitHub.

| Garden | Retained n | Reached flowering (`FloweredFull=1`) | Rate |
| --- | ---: | ---: | ---: |
| Lafayette | 80 | 22 | 27.5% |
| Montpellier | 98 | 79 | 80.6% |
| Toronto | 217 | 115 | 53.0% |
| Uppsala | 75 | 24 | 32.0% |
| **Total** | **470** | **240** | **51.1%** |

The complete-case primary analysis therefore has **470 individuals across 93 origin populations** and all four gardens. Each of five GroupKFold held-out folds has 94 individuals and 18–19 *entirely unseen* source populations. No origin population contributes to both training and test in a fold.

## Primary test frozen before raw outcome opening

- **Target:** whether five previously published genomic haploblocks add information for predicting `FloweredFull` in held-out origin populations, conditional on the garden and origin coordinates.
- **M0:** garden + origin latitude + origin longitude.
- **M1:** M0 + five haploblock dosages.
- **M2 (exploratory):** M1 + garden × haploblock dosages.
- **Estimator:** logistic regression with L2 penalty C=1.0; 5 folds grouped by origin population; geographic means/SD estimated from training rows alone.
- **Primary effect:** M1−M0 out-of-fold *log predictive score* difference in nats per plant. Population-equal-weight comparison and 2,000 origin-population bootstrap resamples of fixed out-of-fold prediction differences are secondary corroboration. PASS requires positive equal-population gain, conditional bootstrap lower bound >0, and positive gain in at least three gardens, with ≥10 complete-case plants in every garden.

This test is distinct from the pre-existing published within-study haploblock × garden genotype-fitness association. It tests prediction for **previously unsampled origin populations within the same four gardens**, not for unseen gardens, new climates, or manipulated haploblock genotypes.

## Result: genomic state does not improve this frozen prediction problem

| Model | Held-out log loss ↓ | Held-out Brier ↓ | Mean logscore gain vs M0, nats/plant |
| --- | ---: | ---: | ---: |
| **M0** garden + origin geography | **0.628916** | **0.219477** | baseline |
| M1 + haploblocks | 0.637734 | 0.223736 | **−0.008818** |
| M2 + garden interactions | 0.647986 | 0.228401 | **−0.019071** |

At the *origin-population equal-weighted* level the gains are **−0.010128** (M1) and **−0.018538** (M2), and their corresponding *conditional* population-bootstrap intervals are **[−0.018486, −0.002030]** and **[−0.030815, −0.006737]**. The latter interval is exploratory for M2. These intervals do **not** incorporate refitting or new-location uncertainty.

For M1, garden-specific average logscore differences were:

| Garden | M1 − M0, nats/individual |
| --- | ---: |
| Lafayette | −0.008011 |
| Montpellier | +0.003323 |
| Toronto | −0.016992 |
| Uppsala | −0.001893 |

Only **one of four gardens** improves. Thus the frozen primary predictive gate **FAILS** (no claim that the true causal genetic effect equals zero).

## Duplicate-ID sensitivity (predefined source-integrity alternatives)

| Duplicate treatment | n | M1−M0, mean nats/plant | Origin-pop. mean | Conditional population-bootstrap 95% interval | Primary PASS |
| --- | ---: | ---: | ---: | ---: | --- |
| **Exclude both (primary)** | **470** | **−0.008818** | −0.010128 | [−0.018486, −0.002030] | **NO** |
| Keep first only | 471 | −0.006872 | −0.006880 | [−0.014777, +0.001017] | NO |
| Keep second only | 471 | −0.006985 | −0.007018 | [−0.014748, +0.000668] | NO |

Both retained-duplicate alternatives are weaker negative estimates with intervals spanning zero, but **neither produces a positive primary estimate**. These are *data-quality sensitivities*, not different inferential specifications chosen to recover a desired result.

## How this relates to the previous three coastal-plant studies

The previously merged [three-species SNP-state study](three_species_genomic_state_audit_2026-11-19.md) found that geographic labels improved held-out **SNP genotype** prediction within known populations. That is not the same estimand as whether genomic haploblocks improve held-out **fitness-response** prediction across origin populations. The observed positive genotype information in the coastal plants is compatible with this clover fitness-prediction **negative** result.

The clover data contain only five scored structural-variation haploblocks rather than a whole-genome genotype matrix; the fields' dosage imbalance (e.g. alternative homozygotes rare at the first three haploblocks), strong garden differences in flowering, and population ancestry may limit transport. None establishes why the predictor fails. Original paper's published genomic and ecological claims remain prior art, not disproven by one out-of-population predictive comparison.

## What was achieved, and what remains outside reach

1. **Evidence delivered:** audited original ZIP provenance, complete-case 470-individual dataset, conflict-ID exclusion and sensitivity, population-disjoint M0/M1/M2 predictive comparison, primary negative verdict.
2. **Empirical boundary:** this source supports **failure to improve prediction in this fixed model**, not the formal exact MLTR source–target carried-label obstruction. No declared finite replacement relations or action-conditioned transition law are estimated, and no causal genetic intervention occurs.
3. **Next different-data requirement:** if the MLTR application is pursued, obtain replicated joint genotype–phenotype–action/fitness measurements with population/ancestry-disjoint samples and interventions. Additional post-outcome model variants of this same file should not be used to manufacture a positive outcome.

## Reproducibility

The original raw Dryad ZIP was not placed into GitHub. The branch includes a source-hash-locked offline entrypoint:

```bash
python -m pip install numpy scikit-learn
python scripts/analyze_clover_haploblock_fitness.py \
  --zip /path/to/doi_10_5061_dryad_dfn2z3593__v20250829.zip \
  --out artifacts/clover_haploblock_fitness_holdout.json
```

The exact old source-frozen model, group folds, L2 penalty and failure criteria have not been changed in response to the observed outcome. The only implementation changes reflect observed **source schema capitalization, exact ZIP checksums and conflicting duplicated file ID**; these are auditable source-repair rules. This note does not revise canonical Paper A, theorems, or infer an empirically measured MLTR history mode.
