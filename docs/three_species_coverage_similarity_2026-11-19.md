# Source-locked robustness audit: common SNP coverage and near-identical genotype leakage

**Source:** Nakahama et al. (2022), Dryad DOI [10.5061/dryad.tb2rbp03j](https://doi.org/10.5061/dryad.tb2rbp03j), supplied v20220815 ZIP SHA-256 `e81efee9bfe1f1176609bbcd3a1f23f9be63c698e614db09884676684ceb9b8c`.

**Scientific scope:** SNP genotype prediction in previously sampled regions (not unseen-region fitness/management responses). This is a follow-up to the already-merged [three-species observational audit](three_species_genomic_state_audit_2026-11-19.md); no new MLTR/CCOC theorem, and no intervention response.

## 1. Shared coverage: retain the same callable-marker panel across regions

To test whether a highly population-specific missingness filter drives the earlier prediction, retain only SNPs with genotypes in at least 75% of specimens in **each** included modern regional group; then rerun per-individual leave-one-out (LOO) SNP allele-copy logscore using region-specific frequencies versus species-wide frequencies. Both models use the same locus panel and the same held-out individual's called genotypes; held-out genotypes never enter training allele frequency estimates.

| Species | Complete-region panel (SNPs) | Region-minus-species gain, nats / called allele copy | Positive individuals |
| --- | ---: | ---: | ---: |
| *Cirsium maritimum* | 71 | **+0.2175963** | 32/32 |
| *Linaria japonica* | 98 | **+0.0946244** | 40/42 |
| *Suaeda glauca* | 80 | **+0.2642634** | 24/24 |

All retained estimates remain positive. Restricting to **100%** called loci in each region leaves only 9/17/22 SNPs, respectively, but the mean signal is still positive: +0.26437/+0.07728/+0.36313 nats/allele. These 100%-complete panels are very small and cannot establish genomewide universality.

## 2. Highly similar genotypes: source-relative observation, not inferred clonality

Across **at least 60 jointly called SNPs**, exact diploid genotype identity was measured within and between regional populations. At >=95% identity the observed within-region high-similarity pair counts were:

| Species | Within-region pairs >=95% genotype identity | Mean within-region identity | Mean between-region identity |
| --- | ---: | ---: | ---: |
| *C. maritimum* | **18** | 0.884 | 0.633 |
| *L. japonica* | **58** | 0.894 | 0.744 |
| *S. glauca* | **19** | 0.883 | 0.594 |

Such pairs are **not identified clones, sibships or technical replicate records**; the SNP panel is ascertained and incomplete. The source population codes are not unique specimen identifiers. It would be invalid to deduplicate individuals solely on genotype similarity.

To guard against a near-genotype training shortcut, each held-out individual was scored after excluding from **both** the local and species-wide training sets any other specimen from the same regional group with >=95% exact genotype identity on >=60 jointly called SNPs. Models still required >=3 called remaining local training individuals and >=10 called remaining species-wide training individuals per evaluated SNP.

| Species | Full SNP panel: gain | Evaluated individuals | 75%-common panel: gain | Evaluated individuals |
| --- | ---: | ---: | ---: | ---: |
| *C. maritimum* | **+0.2151427** | 28/32 | +0.2184786 | 28/32 |
| *L. japonica* | **+0.0656346** | 24/42 | +0.0631359 | 24/42 |
| *S. glauca* | **+0.2154878** | 21/24 | +0.2702425 | 21/24 |

The region-specific information remains positively predictive in the **evaluable subset**, but particularly for *L. japonica* the removal produces **18 unevaluable samples**. This is informative sample-selection and no same-rate generalization to all 42 individuals is warranted. At 98% instead of 95% the usable subsets become 32/32, 35/42 and 24/24; gains remain positive (full SNP panels +0.21948, +0.07938, +0.21369).

## 3. Missingness is itself geographically structured

With only the **binary called/missing indicator** as the held-out outcome (instead of SNP alleles), regional identity also improves the mean call-status logscore for:

- *C. maritimum*: +0.02288 nats per binary SNP status, 22/32 positive specimens;
- *L. japonica*: +0.02931, 31/42 positive;
- *S. glauca*: +0.00180, 9/24 positive.

This warns that extraction, sample provenance, genotyping batch or quality may be aligned with geographic groups. It does **not**, by itself, explain away genotype frequency differences because the allele-prediction effect survives the common-coverage panel and similarity exclusions. No batch metadata capable of attributing that difference are available in the original genotype files.

## 4. Boundaries and inference

**Positive, within-sample-frame statement:** regional SNP allele frequency carries predictive information beyond the named species identity for new individuals from these **already sampled** regions. This statement is robust to simple coverage restrictions; it is *directionally positive* after high-identity exclusions in a substantially smaller evaluable subset.

**Unresolved:** degree of genetic independence among specimens; conservation-management or reproductive response differences; generalization to novel regions; evolutionary origin of the variation; and whether ancestry is causal rather than an indicator of sample provenance. A region-label permutation test is not a kinship-adjusted, cross-site intervention experiment.

This is an exploratory post-result robustness analysis, **not** a separately preregistered prospective validation. Original README specifies that loci detected only in historical specimens were removed manually as potential contamination. Neither this study nor the prior SNP archive estimates the absolute loss of historical alleles.

## Run

The source-locked standard-library script and synthetic-only tests are:

```bash
python -m pytest -q tests/test_three_species_coverage_similarity.py
python scripts/audit_three_species_coverage_similarity.py \
  --zip /path/to/doi_10_5061_dryad_tb2rbp03j__v20220815.zip \
  --out artifacts/three_species_coverage_similarity.json
```

The ZIP and each source file are checked against the exact hashes used in the earlier main-branch analysis. The script emits summaries, not genotypes. The source cannot be silently substituted. This audit remains an empirical application layer; **MLTR Paper A and all mathematical theorems are unchanged.**
