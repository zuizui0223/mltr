# Three coastal species: within-species genomic information beyond a species label

**Analysis date:** 2026-11-19. **Scientific role:** exploratory real-data cross-taxon extension of the species-genomics application gate, **not** a new CCOC/MLTR theorem or an empirical causal decision-sufficiency test.

## Exact source and contrast

Original supplied Dryad v20220815 ZIP, [DOI:10.5061/dryad.tb2rbp03j](https://doi.org/10.5061/dryad.tb2rbp03j), SHA-256: e81efee9bfe1f1176609bbcd3a1f23f9be63c698e614db09884676684ceb9b8c. Three independent species *within one published study* and a shared MIG-seq/St acks ascertainment pipeline. The README source-group labels, not POP-block order, define collection year, geographic region and ex-situ status. Repeated group identifiers are not individual IDs; retain every specimen row. Diploid biallelic SNP calls are 0101/0102/0202, with 0000 missing.

| Species | Individuals (all samples) | SNP loci | Regional group comparison | No. geographic pairs |
| --- | ---: | ---: | --- | ---: |
| *Cirsium maritimum* | 50 | 281 | Awaji 2019, Shizuoka 2019, Mie 2019, Wakayama 2019 | 6 |
| *Linaria japonica* | 56 | 379 | Awaji 2020, Miyagi 2019, Fukui 2020, Kyoto 2019, Shin-onsen 2020, Tottori 2019 | 15 |
| *Suaeda glauca* | 45 | 138 | Awaji 2019, Mie 2019, Okayama 2020 | 3 |

The *L. japonica* historic L6 group (Kami, Hyogo, 1995–2011) was excluded from the 2019–2020 regional comparison. It has only four individuals, call fraction 26.58%, and just 21–33 qualifying SNPs in pairwise Fst when included. Comparisons use the same specimen and accession-level source, not three independent laboratory replications.

## Result A — regional nuclear-SNP differentiation within each named species

Hudson-type pooled ratio-of-sums Fst computed only on SNPs with at least four called individuals in **each** compared population; no imputation. Both numerator and denominator are pooled across loci, not averaged per-SNP Fst.

| Species | Regional Fst range | Eligible SNPs across pairwise comparisons | Positive geographic pairs |
| --- | ---: | ---: | ---: |
| *Cirsium maritimum* | **0.599–0.779** | 197–224 | 6/6 |
| *Linaria japonica* (excluding historic L6) | **0.323–0.737** | 220–345 | 15/15 |
| *Suaeda glauca* | **0.473–0.742** | 115–123 | 3/3 |

A positive Fst is **not** a test that the taxon is polyphyletic, a cryptic species, locally adapted, genomically incompatible, or necessarily subject to a different future intervention response. Allele frequencies may also be influenced by sample provenance, historical divergence, kinship and marker ascertainment.

## Result B — previously unseen individuals' alleles are better predicted when region is retained

This is a *strictly observational genomic prediction* contrast. Every test genotype is removed from training. For each SNP, compare the frequency of its alternative allele among all other sampled individuals of that species (M0) versus other individuals in the focal regional population (M1). Calculate the held-out allele-copy log predictive score with Beta(alpha, alpha) smoothing, requiring at least three called **other individuals in the focal group**, and 10 others across all regional groups. All comparisons are on exactly the same called SNPs. Score difference is average log probability M1 − M0 in **nats per allele copy** (not the CCOC exact-state memory bound).

| Species | Evaluated regional specimens | LOO predictive gain at alpha=0.5 | Positive individuals | More conservative alpha=2 gain |
| --- | ---: | ---: | ---: | ---: |
| *C. maritimum* | 32 | **+0.2183 nats / allele** | 32/32 | +0.1524 |
| *L. japonica* (L6 excluded) | 42 | **+0.1047 nats / allele** | 42/42 | +0.0337 (32/42 positive) |
| *S. glauca* | 24 | **+0.2094 nats / allele** | 24/24 | +0.1551 |

The positive direction at alpha=0.5 holds at each of the 13 included regional population group means. The L. japonica prediction is **partially smoothing-sensitive**: at alpha=2 the L7 regional mean changes sign slightly (−0.0057), although the overall mean remains positive. This limitation is essential.

A secondary conditional association check randomized the **individual-level regional labels** 999 times, preserving group sizes and the individuals' genotypes/missingness. For each species, zero randomized labelings exceeded the observed alpha=0.5 held-out score, giving the minimum attainable one-sided randomization P=0.001. This is **post-outcome exploratory** and rests on conditional label exchangeability, which cannot rule out sequencing batch, population relatedness or regional sampling confounding. The SNP predictions are not fitness predictions.

## Result C — distinct historical and conservation collections contain partly different sampled alleles

Within the focal Awaji-origin comparison (past wild versus the later wild sample), current-genotype callable loci only:

| Species | Past n | Current n | Historically detected allele not observed current | Observed in >=1 ex-situ sample | Historical singleton specimens |
| --- | ---: | ---: | ---: | ---: | ---: |
| *C. maritimum*: 2007 / 2019 | 2 | 8 | 20 | 6 | 19/20 |
| *L. japonica*: 1988–2006 / 2020 | 4 | 4 | 80 | 31 | 60/80 |
| *S. glauca*: 1998–2007 / 2019 | 5 | 8 | 18 | 3 | 17/18 |

*L. japonica* has **16 further historic alleles** at SNPs with **no callable current genotype**, which are excluded from the 80. For *S. glauca*, only **3 SNPs** were fully genotyped in all five historical and all eight current individuals, preventing a reliable fully complete temporal comparison. *C. maritimum* has just **10** loci fully callable across both past individuals and all eight current specimens. These are not allele extinctions: old sample sizes, specimen quality, per-locus dropout and ascertainment affect detection. There is no support here for a generalized or statistically significant temporal reduction in genetic diversity.

**Source ascertainment caution:** the original Dryad README explicitly states that loci found *only in historical specimens* were removed manually to exclude possible contamination. It also specifies a Stacks minimum minor-allele frequency of 0.01, per-locus coverage threshold r=0.3, and TASSEL sample/site filters. Therefore the reported historic/current non-detections are **conditional on a pre-filtered marker panel**, and neither allele-loss incidence nor temporal population-genetic erosion can be estimated as if all potentially historical loci had been retained. This source-driven bias is separate from the low historical n and unequal missingness discussed above.

## Main inference and strict boundary

**Supported:** the nominal species label alone discards substantial geographical allele-frequency information within three coastal plant species. Regional identity improves prediction of genotypes of held-out individuals from those already represented populations, beyond a species-wide allele frequency. This is an *observable-genotype* rather than an *evolutionary-fitness* prediction claim.

**Not supported:** the current evidence cannot determine whether source–target genetic relationships preserve any specified biological management action or demographic response. No reproductive success, measured action, candidate mechanisms, migration/reticulation paths or total replacement relation are available. Therefore neither the MLTR decision-sufficiency obstruction nor the minimum-history-mode theorem has undergone empirical validation. This exercise is not a whole-genome analysis: SNP genotypes come from a reduced-representation MIG-seq panel.

## Reproduce

A no-raw-redistribution, standard-library source-locked script is provided at [scripts/audit_three_species_snp_states.py](../scripts/audit_three_species_snp_states.py):

    python scripts/audit_three_species_snp_states.py --zip /path/to/doi_10_5061_dryad_tb2rbp03j__v20220815.zip --out three_species_snp_summary.json

Optionally run 999 conditional label permutations:

    python scripts/audit_three_species_snp_states.py --zip /path/to/original.zip --out permuted.json --permutations 999

The original ZIP must match its exact frozen SHA-256 and each of the three Genepop files and README must pass their own SHA-256 checks. No raw genotype file is committed to this repository. Synthetic-only unit tests cover parsing, multiple identical genotype rows, missingness, Fst, held-out prediction, historical non-detection and hash refusal.

The main C. maritimum published-source analysis remains [here](cmaritimum_real_genomic_results_2026-11-19.md). A separate, outside-GitHub NumPy implementation independently recounted its 50×281 calls, 20/6 historic/ex-situ allele sets and all six original regional Fst estimates to published report rounding, before the present extension was admitted.

## Publication decision

This is an **informative biological application example**, not a new mathematical discovery or sufficient standalone cross-species genomics paper. Main-paper claims should remain the source-relative MLTR finite theory; genomic evidence may support a future application/method demonstration, *after* genotype × intervention-response matching is obtained.
