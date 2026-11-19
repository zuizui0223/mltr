# Next experimental-source gate: haploblock state vs fitness across clover common gardens

**Status 2026-11-19:** analysis protocol and *synthetic-only* implementation complete; original row-level **DatasetA_commongarden.csv is not yet in the analysis environment**. Thus no new fit, coefficient, prediction gain, significance test or species-genomics generalization is claimed.

## Published empirical source and novelty firewall

- Battlay et al. (2025), *Nature Ecology & Evolution*, [doi:10.1038/s41559-025-02751-2](https://doi.org/10.1038/s41559-025-02751-2), title: **Haploblocks contribute to parallel climate adaptation following global invasion of a cosmopolitan plant**.
- Original fitness × haploblock source: [Dryad 10.5061/dryad.dfn2z3593](https://doi.org/10.5061/dryad.dfn2z3593), file **DatasetA_commongarden.csv** (41.15 KB) plus **README.md**.
- Source metadata describes **472 individual plants** in **four field common gardens** (Lafayette, Toronto/Mississauga, Montpellier, Uppsala/Uppsula), from **46 North American and 47 European source populations**. Whether all expected rows are usable must be checked against the exact file rather than assumed from metadata.
- Exact joined columns named in the source README: `Garden`, `File` (.bam identifier), `Population`, `Latitude`, `Longitude`, `Hb7a1`, `Hb7a2`, `Hb7b`, `Hb9`, `Hb13`, `Survived1st`, `GrowthRate`, `FloweredFull`, `FlowerHeadNumberFull`, `SeedSetMassFull`. Haploblock states 0/0.5/1, missing coded 999.
- The original research **already reported** haploblock genotype × garden associations for survival-to-flowering and seed mass. Repeating that result is not a novel biological discovery, a new genomic mechanism, or independent external confirmation.

## New, falsifiable question

> In a **source population not used for training**, does retaining five structural-variant haploblock genotypes improve prediction of survival to flowering across the four observed garden environments, beyond an inherited coarse descriptor using garden and collection-site latitude/longitude?

This is a **predictive sufficiency** question concerning matched genotype × environment × fitness; it is distinct from the prior three-species allele-prediction exercise, which had *no fitness measurement*.

### Frozen modeling contract before row-level source opening

| Model | Pre-outcome inputs | Role |
| --- | --- | --- |
| M0: coarse state | Garden (categorical) + origin latitude + origin longitude | Primary comparator |
| M1: genomic state | M0 + five observed haploblock dosages | Primary genomic prediction test |
| M2: garden-sensitive genotype | M1 + garden × haploblock interactions | Exploratory environment-conditional test only |

**Primary outcome** `FloweredFull` = survived to flowering (0/1). The outcome is independent of the predictors; do **not** condition this model on post-exposure growth or flowering. `SeedSetMassFull` is a potential separate fecundity follow-up, not combined with survival or used to tune the primary test.

**Cross-validation:** five origin-population-disjoint folds: all descendants/individuals from the same `Population` are assigned entirely to train or held-out evaluation, regardless of garden. All models evaluate the **same complete-case individuals**, same folds and same observed outcomes. Source latitude/longitude standardization is fitted on training records only. Models: fixed L2-penalized logistic regression (C=1.0). Missing marker/coordinate/outcome records coded 999 are excluded from all models, not imputed in M0 alone.

**Primary estimand:** paired M1−M0 held-out log predictive score, in nats per plant. Report individual-weighted score and equal-origin-population-weighted score, with a **conditional** 2,000-resample origin-population bootstrap interval. Diagnose missingness by garden and the fraction of origin populations with positive effects. For the primary claim to pass a conservative *exploratory* gate, require at least 10 complete-case individuals in **each garden**, a positive equal-origin-population average increment, the lower population-bootstrap bound >0, and positive score improvement in at least three of four gardens. The script emits a terminal status for this frozen criterion, never promoting the exploratory interaction M2 on a primary M1 failure. A failed/unevaluable gate remains a negative or unresolved result, not a reason to change the metric. M2 is **not** promoted post hoc if M1 fails.

**Independence and causal limitations:** an origin-population holdout tests transfer to *previously unsampled populations within these four existing garden settings*; it does **not** test entirely new gardens, manipulate haploblocks genetically, control all population ancestry or exclude batch effects. The original authors have already investigated selection; this additional test is predictive rather than a new causal demonstration.

## Source/implementation gates

1. **S0 — source identity confirmed:** DOI and README column names/four gardens/fitness variables checked from publisher and original paper. The exact source file hash is **pending** until `DatasetA_commongarden.csv` is available.
2. **S1 — source QC not run:** confirm SHA-256, number of rows, unique `.bam` IDs, exact genotype coding, complete-case numbers, missingness by garden, population disjointness, positivity of both survival outcome classes in train folds.
3. **S2 — synthetic-only code checked:** [source-locked analysis template](../scripts/analyze_clover_haploblock_fitness.py) and [tests](../tests/test_clover_haploblock_fitness.py). This does not imply any real-data prediction.
4. **S3 — real held-out prediction pending:** apply frozen M0/M1/M2 comparisons only after S1. Preserve all negative/sensitive and unevaluable outcomes.
5. **S4 — MLTR interpretation pending:** even a positive M1−M0 outcome is not automatically an exact `carried-label` conflict, replacement history mode, or MLTR finite-model theorem validation. Those require explicit total source–target relations, declared actions and the relevant outputs.

## Execution

For an authorized original Dryad file downloaded locally (do **not** commit sample IDs or raw genotypes):

```bash
python -m pip install numpy scikit-learn
python scripts/analyze_clover_haploblock_fitness.py \
  --input /path/to/DatasetA_commongarden.csv \
  --out artifacts/clover_haploblock_out_of_population.json
```

A separate GitHub workflow validates only synthetic data. The real experiment is deliberately not run in CI because the raw Dryad CSV is not in the repository. This remains an application study, not a change to Paper A.
