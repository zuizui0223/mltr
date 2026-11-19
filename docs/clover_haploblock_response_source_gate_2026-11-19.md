# Next experimental-source gate: haploblock state vs fitness across clover common gardens

**Status 2026-11-19 (source received after protocol freeze):** the original v20250829 Dryad ZIP was supplied and verified. The fixed model comparison was executed on 470 individuals (472 raw minus two conflicting duplicated `.bam` rows), 93 origin populations and four gardens. The **primary M1−M0 out-of-population predictive increment is negative and NOT SUPPORTED**. [Full real-data audit and sensitivities](clover_haploblock_fitness_holdout_result_2026-11-19.md) · [frozen aggregate metrics JSON](results/clover_haploblock_fitness_holdout_2026-11-19.json). No new causal conclusion or exact MLTR finite theorem claim is made.

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

## Source/implementation gates (historical freeze and current result)

The following model and response contracts were fixed **before the uploaded row-level file was opened**. Their substantive contents (primary `FloweredFull`, M0/M1/M2, origin-population GroupKFold, C=1, conditional bootstrap and positive threshold) remain unchanged.

1. **S0 source identity: PASS.** Original ZIP SHA-256 `dc8fa8378176a063db4367e2fc4dd75914758a7246010e67b7ff7957e5632eb8`; original CSV SHA-256 `cbd9691e4b07a48e97619385bedc9f9a45fb02164d4ce08c1a99c9af7df054d4`; README SHA-256 `72b966bbd7326a36cac14294c91dc15f3e4878e6ff7ae4c4289a3da531a83131`.
2. **S1 schema + source QC: PASS WITH EXCLUSION.** Original CSV labels use lowercase `hb7a1` etc. rather than display-name capitals. A `.bam` ID occurs twice with contradictory `hb9`/`hb13`; both rows are excluded from the primary fit. Complete case: 470 of 472 plants, all 93 source populations and four gardens.
3. **S2 reproducibility: synthetic-only CI tests plus an independent original-source local fit.** The source parser and five-fold group holdout were repaired only for observed capitalization/duplicate-ID source contract, never for outcome direction.
4. **S3 original-source primary outcome: NOT SUPPORTED.** M0 heldout log loss 0.628916, M1 0.637734, M2 0.647986. Mean M1−M0 predictive logscore −0.008818 nats/individual; equal-population mean −0.010128, conditional bootstrap interval [−0.018486, −0.002030]; only one of four gardens positive. Duplicate alternatives do not reverse the direction.
5. **S4 MLTR formal decision-sufficiency: NOT ESTIMATED.** Genomic prediction failure does not establish or refute any exact source-carriage, history-completion or future-interface theorem, nor imply a causal null effect of structural variation.

The exact source-derived results and limitations are in [the auditable results document](clover_haploblock_fitness_holdout_result_2026-11-19.md). The uploaded individual genotype/fitness CSV is intentionally not copied into GitHub.

## Execution

For an authorized original Dryad file downloaded locally (do **not** commit sample IDs or raw genotypes):

```bash
python -m pip install numpy scikit-learn
python scripts/analyze_clover_haploblock_fitness.py \
  --zip /path/to/doi_10_5061_dryad_dfn2z3593__v20250829.zip \
  --out artifacts/clover_haploblock_out_of_population.json
```

A separate GitHub workflow validates only synthetic data. The real experiment is deliberately not run in CI because the raw Dryad CSV is not in the repository. This remains an application study, not a change to Paper A.
