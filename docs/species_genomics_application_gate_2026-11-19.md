# Species-genomics application gate for CCOC / MLTR — 2026-11-19

**Status:** cross-repository evidence audit and prospective test protocol; **not** a theorem, genomic confirmation of MLTR, or a modification to the canonical Paper A manuscript.

**Current empirical synthesis updated 2026-11-22:** the original Arabidopsis estimated-seed extension, unchanged-code replay, and independent Exposito-Alonso genomic prediction benchmark are included below. Known-accession rack holdouts and within-panel accession/geographic-cell holdouts are distinct from the full out-of-lineage genomic-response proposal.

## Question

Under what conditions does a species name, current phenotype or genomic cluster cease to be a sufficient interface for the evolutionary / intervention response that the analysis asks it to predict? This is an empirical *application question* for the existing formal contracts; taxonomy disagreement or phylogenetic structure alone does not certify an MLTR obstruction.

## Confirmed results, by evidence tier

| Source | Checked result | Evidence type | Strict inference boundary |
| --- | --- | --- | --- |
| [CCOC main](https://github.com/zuizui0223/ccoc) | Closed/open future family: `|P_C|=2`, `|P_O|=2^(m+1)`, memory increment `m` bits | Exact finite construction | No genomic/biological replication |
| [MLTR main](https://github.com/zuizui0223/mltr) | Many-to-many carried-label criterion, fixed-route direct=sequential carriage, route coherence and minimum history modes | Declared finite-model propositions/tests | Requires *declared total* source-target relations and a target response/action model; not inferred from genetic data |
| [CREST main](https://github.com/zuizui0223/crest) | Sparse access witness has `N=4`, `k=1`, `m=10`, `|Q|=1027`, 10.00422 bits | Finite semantic witness | Do not interpret 1027 as empirically observed genomic classes |
| [chun hidden-memory clade CSV](https://github.com/zuizui0223/chun/blob/main/data/flowerclades51_hidden_fine_memory_clades_v0_1.csv) | Recount: 18/21 positive centered within-coarse AUC effects; median +0.0270078; 6/21 nominal one-sided P≤0.05, 4/21 BH discoveries at 0.05 | Retrospective phylogenetic phenotype analysis | Not 18 individually significant systems; not genome-sequence-level evidence; clades are not necessarily independent biological replicates |
| [chun prospective Schistanthe](https://github.com/zuizui0223/chun/blob/main/docs/SCHISTANTHE_HIDDEN_MEMORY_RESULT_V0_1.md) | 129 exactly matched tips; centered AUC +0.064158; 9,999 permutations; one-sided P=0.0033 | Independent prospective visible-phenotype/phylogeny validation | Supports hierarchical visible-color memory, not a molecular mechanism |
| [chun prospective Gesnerioideae](https://github.com/zuizui0223/chun/blob/main/docs/GESNERIOIDEAE_BIOCHEMICAL_HIDDEN_MEMORY_RESULT_V0_1.md) | 30 retained tips; biochemical centered AUC −0.0077868; P=0.5005 | Prospective null/negative control | Blocks universal biochemical/visible cross-representation generalization |
| [EAzami nuclear scaffold](https://github.com/zuizui0223/EAzami/blob/main/docs/chapter2/MANUSCRIPT_JEB_V4.md) | 236 QC loci, 176 outgroup-rootable loci, 161,654 bp; JPN20's two samples non-monophyletic in ML and all 1,000 bootstrap trees | Nuclear sequence/topology evidence | Species-tip mismatch, not proof of hybridization or a management-response split |
| [EAzami V10](https://github.com/zuizui0223/EAzami/blob/main/README.md) | Orientation minimum 4–6, phyllary 3, stickiness 5 steps; zero of three pairs pass robust common transition-localization rule | Topology-conditioned trait-history lower bounds | Minimum steps ≠ independent evolutionary origins or detected adaptive causes |
| [Daphne 2025 taxon/marker comparison](https://doi.org/10.11110/kjpt.2025.55.3.157) | `D. pseudomezereum var. koreana` is placed with `D. kamtschatica` by plastome, with nominate `D. pseudomezereum` by ITS | Published cytonuclear discordance | One marker contrast is not a nuclear species tree or unique evidence for ancient introgression; accession ON244034 refers to var. koreana |
| [Daphne 2026 plastome study](https://doi.org/10.1002/2211-5463.70143) | Revised 17-species Daphne sampling is plastome-monophyletic; plastome sister clade Thymelaea | Published organelle phylogeny | Revised versus broad genus are different taxon sets; plastome cannot be silently substituted for nuclear species history |
| [Fan et al. 2026 Camellia genomics](https://doi.org/10.1111/pbi.70442) | 237 accessions, 11 de novo/reference assemblies, widespread TE-associated SVs, experimentally supported MYB60 regulatory variant | Published genome-scale genotype-to-expression/colour mechanism | Prior art, not this programme's new genomic inference; raw underlying genomic data are not openly downloadable according to publication data statement |

## Explicit separation of three observational insufficiencies

1. **Species-tip compression:** a nominal taxon can merge sequence-divergent samples; EAzami JPN20 is a topology-level warning, pending voucher/identity/ILS/reticulation checks.
2. **Phenotypic compression:** genetically informed phylogenies can retain fine-state structure within a coarse phenotype. The independent Schistanthe test supports this at the *visible-colour* level; it does not test a genome-to-function map.
3. **Marker/concept discordance:** plastome and ITS (or historical vs revised taxonomy) can disagree. A disagreement is not by itself an MLTR history-mode count. Distinct marker gene trees are **not** automatically alternative replacement routes.

## Frozen prospective test proposal (no outcome yet)

**Primary estimand:** out-of-lineage predictive improvement for a declared response under an intervention or environment change. For accession `i`, record taxon-concept-version `T_i`, coarse phenotype `C_i`, sample-linked nuclear ancestry `A_i`, structural/regulatory alleles `G_i`, historical/reticulation status `H_i`, environment `E_i`, action `a`, and observed response `Y_i(a)`.

- Baseline: `M0: Y(a) ~ C + T + E + a`.
- Added genomic state: `M1: Y(a) ~ C + T + E + a + A + G + (a × A/G)`.
- Optional history mode: `M2: M1 + H + a×H`, tested *only* where immutable alternative histories and valid correspondence maps are independently supported.
- Predefine matched-sample accession/voucher crosswalks, ploidy, orthology/locus-QC and population/species disjoint folds. Compare out-of-sample log predictive density (primary) and whether the added information changes the sign/rank of a declared decision (secondary). Group by lineage or population to prevent leakage.
- **Positive empirical sufficiency failure:** same coarse label and controlled covariates, but replicated, independently measured response difference under the declared action; M1/M2 improves out-of-lineage prediction and exceeds pre-frozen null and multiplicity controls. This is finite/noisy evidence, not an exact deterministic quotient theorem.
- **Negative result:** after independent ancestry and genotype quality controls, adding `A/G/H` fails to improve held-out response or no comparable action outcome exists. Preserve the negative status; do not relabel topology discordance as response insufficiency.

## First executable steps and blockers

1. **Completed now:** audit source-facing counts above; recompute 21-clade signs, median and nominal/BH discovery count from committed `chun` CSV (no new hypothesis testing or additional prospective replication).
2. **Real population-genomics pilot COMPLETED:** [2022 Dryad Cirsium maritimum MIG-seq Genepop](https://doi.org/10.5061/dryad.tb2rbp03j), original v20220815 ZIP supplied by user. [Source-locked analysis](cmaritimum_real_genomic_results_2026-11-19.md) and [aggregate result JSON](results/cmaritimum_real_genomic_summary_2026-11-19.json) establish 50 rows/281 SNPs/7 verified sample groups, 20 historically observed alleles not detected in the sampled contemporary wild group (6 also observed in an ex-situ group), and large pairwise geographic Fst (0.60–0.78 among four 2019 geographic populations). Source age, n=2 historical sampling, genotype missingness, and nonindependent SNP-locus bootstraps limit causal inference. **No matched action/fitness outcomes; no MLTR decision-sufficiency validation.**
3. **Eligible full-state pilot only after source audit:** obtain sample-linked genomic states and intervention outcomes in Campanula, Camellia or a comparably well-sampled species/radiation. Genomic sequences without matched phenotypes and responses open only the observational-resolution gate.
4. **Out of scope:** altering Paper A theorem or canonical manuscript, promoting existing coarsest-refinement machinery as new, inferring hybridization from one discordant organelle/nrDNA pair, or using genomewide structure as a surrogate for causal intervention response.

## Added 2026-11-19: independent fitness-response pilot and negative prediction result

After this framework was drafted, the user supplied the exact published [white-clover common-garden Dryad ZIP](https://doi.org/10.5061/dryad.dfn2z3593) containing five haploblock dosages and a matched observed outcome, `FloweredFull`. The original common-garden study already published haploblock × fitness associations; this is **not a de novo genotype-fitness discovery**. The test was defined *before* opening the source's outcome rows: origin-population-disjoint 5-fold prediction of `FloweredFull`, with fixed M0 (garden+origin lat/lon), M1 (M0+five haploblocks), and exploratory M2 (M1+garden×haploblock).

The exact original CSV has 472 records, with one reused .bam ID appearing on two lines with different `hb9`/`hb13` dosages. Both ambiguous lines were excluded, yielding **470 individuals / 93 origin populations / four gardens**. Under the frozen test M0 out-of-origin-population log loss was **0.628916**, M1 **0.637734**, and M2 **0.647986**. Primary M1−M0 average held-out logscore **−0.008818 nats/individual**, equal-population average **−0.010128** and conditional population-bootstrap interval **[−0.018486, −0.002030]**. Only Montpellier had a positive garden-level M1 gain, so the fixed positive gate **failed**. Retaining either of the conflicting .bam lines individually did not make the primary result positive.

**Interpretation:** population geography can predict genotypes (the three coastal-species pilot), while these five clover genomic features **do not improve the specified held-out fitness prediction** under these four gardens and this frozen model. This does **not** mean structural variants have no biological fitness effect, nor does it establish exact MLTR decision sufficiency. Details: [source-audited real result](clover_haploblock_fitness_holdout_result_2026-11-19.md) and [machine-readable estimate contract](results/clover_haploblock_fitness_holdout_2026-11-19.json).

## 2026-11-20 original Dryad Arabidopsis restriction and operational choice

- The uploaded original [Fitzpatrick et al. Dryad 10.5061/dryad.334765v](https://doi.org/10.5061/dryad.334765v) 'full_data_drought.csv' contains 760 rows, 38 accessions and one missing fruit. The teaching mirror consists of **the same 759 fruit-observed original rows plus 120 observations of six additional accession codes**, not a second independent study.
- Under the earlier frozen P0/P1/P2 source-relative five-rack prediction comparison, P2 over P1 retains a **+0.188126** MSE reduction (all five rack folds positive) on original 38 accession fruit observations. After eliminating an accession-wide P2 intercept adjustment, the post-result action-only increment is weaker (+0.046842; conditional 38-accession interval crosses zero). No sequence-level genome features were measured.
- For the experimental four-choice action policy evaluated on 189 complete accession×rack panels, P2 changes the pooled action in 14 panels but has **no supported positive policy value**: mean −0.057559 sqrt-fruit units, conditional interval [−0.146246,+0.037777], only 1/5 racks positive.
- This reinforces the strict logical separation of **state heterogeneity, fitted-response predictive accuracy, and realized decision value**. It does **not** prove the exact MLTR decision-sufficiency or source–target replacement-history theorem. [Full original-source analysis](arabidopsis_original_dryad_38_reanalysis_2026-11-20.md) · [source-hash-locked aggregate results](results/arabidopsis_original_dryad_38_2026-11-20.json).


## Estimated lifetime-seed extension of the same Arabidopsis experiment

The separately supplied seed-per-fruit table permits reconstructed seed output for **33 accessions with both watering calibrations: 659 observed outputs and 164 complete four-action panels**. The same accession IDs occur in training and held-out racks. These are known-accession block predictions within the original study, not independent biological replication, an unseen-lineage test or a genomic assay.

Centered P2 reduces pooled raw estimated-seed MSE by **+11,472.300**, but the frozen primary predictive gate **fails** because one rack has negative gain. The equal-accession mean is +11,473.47, with conditional bootstrap interval [+3,369.26,+20,154.49]; that interval does not override the fold criterion. The sqrt-seed sensitivity passes its exploratory numerical gate, while the matched33 sqrt-fruit sensitivity does not. The sensitivity result cannot replace the raw-seed primary.

The mean realized action-choice difference is **+5.6416 estimated seeds per complete panel**. The equal-accession mean is +5.6074, with conditional interval **[−77.82,+102.65]**; treatment-choice benefit and harm remain unsupported. These intervals hold predictions or policies and calibration factors fixed. Seed factors are averages from the same experiment; rack-separated calibration observations and calibration uncertainty are unavailable. The five excluded accessions are enriched in zero-fruit observations, so the retained cohort cannot stand for all 38 accessions. [Full results](arabidopsis_original_seed_production_results_2026-11-20.md).

The 2026-11-21 [production replay](arabidopsis_seed_replay_and_claim_audit_2026-11-21.md) reproduces the archived estimates to reported numerical precision using the unchanged merged code and exact source hashes. This adds computational verification, not independent evidence about biological effects or treatment value.

## Independent Exposito-Alonso genomic prediction benchmark — 2026-11-22

The [new source-pinned benchmark](exposito_genomic_prediction_result_2026-11-22.md) links author-published genetic distances to final published fitness summaries for **514 accessions × eight site/rainfall/density contexts (4,112 summaries)**. The protocol was committed before predictive scoring. It holds each accession's full response vector out together, with training-only preprocessing and nested tuning; a prespecified sensitivity holds out whole five-degree geographic cells. This is an independent experiment relative to the earlier Arabidopsis/clover datasets, but a reanalysis of published data, not a new genomic-selection discovery.

Primary MSE is **0.716511** for the training-mean predictor, **0.699939** for quadratic collection coordinates (M0), and **0.694101** after adding genetic distance (M1). The M1 increment is **+0.005837** train-relative squared-error units (0.834% of M0 loss), conditional 95% interval **[−0.003921,+0.016383]**, with only **3/5 folds positive**. The frozen primary stability gate **fails**. Geographic-cell sensitivity also fails: gain **+0.003639**, conditional interval **[−0.003442,+0.011120]**, **3/5 folds positive**. Neither result establishes a stable genomic increment under this benchmark; neither shows an absence of biological genetic effects.

The targets are image/calibration-derived published summaries. Repeated physical-pot keys have differing harvest-image records; no silent deduplication or independent plant-level reconstruction was performed. Resampling holds published targets and fitted predictors fixed. The primary is within-panel accession prediction, not an unseen biological population or new-environment test. No action policy or exact MLTR source–target relation was evaluated. [Frozen protocol](exposito_genomic_prediction_protocol_2026-11-22.md) · [aggregate results](results/exposito_genomic_prediction_2026-11-22.json).

## Current decision — 2026-11-22

| Evidence question | Current permitted conclusion |
| --- | --- |
| Does the coastal genomic sample retain geographic/state structure? | The earlier source audits support sample-level genomic structure; comparable treatment/fitness outcomes are absent. |
| Do the five clover haploblocks improve the frozen out-of-origin-population fitness prediction? | **Not supported** under the specified garden/geography baseline. Preserve this result without tuning further variants to obtain a positive outcome. |
| Does finer Arabidopsis accession×action response improve prediction? | Pooled fitted errors can improve, but the **primary centered raw estimated-seed gate fails**; the exploratory sensitivity is scale-dependent and conditional on in-study calibration. |
| Does accession-specific Arabidopsis treatment selection improve realized output? | **Not supported** for the evaluated fruit or estimated-seed policies. The seed analysis also does not establish harm. |
| Does the independent Exposito genetic-distance representation improve held-out fitness prediction over quadratic coordinates? | A small positive pooled gain is observed, but **stable improvement is not established**: the primary and geographic sensitivity both have intervals crossing zero and only 3/5 positive folds. This conclusion is conditional on the published summaries and specified predictors. |
| Has exact MLTR decision sufficiency or historical transport been tested? | **Not tested**: declared finite source–target relations and the required action-conditioned law are absent. The Arabidopsis extension does not satisfy the proposed out-of-lineage genomic-response test. |

The empirical distinction is between evidence for biological state structure, performance of a specified predictor and value of a specified action rule. They require separate observations and comparisons; a positive result for one does not authorize the other claims. This synthesis preserves the frozen models, thresholds and biological conclusions.
