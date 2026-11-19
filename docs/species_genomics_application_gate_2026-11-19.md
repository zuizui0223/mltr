# Species-genomics application gate for CCOC / MLTR — 2026-11-19

**Status:** cross-repository evidence audit and prospective test protocol; **not** a theorem, genomic confirmation of MLTR, or a modification to the canonical Paper A manuscript.

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
2. **Eligible population-genomics pilot:** [2022 Dryad Cirsium maritimum MIG-seq Genepop](https://doi.org/10.5061/dryad.tb2rbp03j). One focal species has past-wild/current-wild/ex-situ samples. Download, hash and audit sample labels, per-locus missingness, within-species allelic variation and separation by time/management; do not call this an action-response MLTR validation without sample-matched fitness/trait outcomes.
3. **Eligible full-state pilot only after source audit:** obtain sample-linked genomic states and intervention outcomes in Campanula, Camellia or a comparably well-sampled species/radiation. Genomic sequences without matched phenotypes and responses open only the observational-resolution gate.
4. **Out of scope:** altering Paper A theorem or canonical manuscript, promoting existing coarsest-refinement machinery as new, inferring hybridization from one discordant organelle/nrDNA pair, or using genomewide structure as a surrogate for causal intervention response.

## Decision

**Current status: observational bridge supported; species-genomic decision-sufficiency validation NOT YET TESTED.** Prefer the sample-linked genomic-response experiment over collecting further unpaired taxon-level correlations. This preserves the source-relative finite theorem and offers a falsifiable empirical target.
