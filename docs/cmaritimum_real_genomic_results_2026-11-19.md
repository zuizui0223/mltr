# Cirsium maritimum real-source genomic audit (2026-11-19)

Source: Nakahama et al. (2022), Dryad doi:10.5061/dryad.tb2rbp03j, original v20220815 archive supplied by user. **Descriptive population-genomic evidence only; NOT an MLTR/CCOC empirical theorem validation.** No raw genetic matrix is redistributed here.

## Source fingerprint

- ZIP 222,683 bytes, SHA-256 e81efee9bfe1f1176609bbcd3a1f23f9be63c698e614db09884676684ceb9b8c.
- Genepop_Cmaritimum.txt: 73,087 bytes, SHA-256 ecf44241752d8844e35d9cbdc4fa2d57d8aadbc3f2e1f0f17f77c4a4283fcd9e.
- README.txt: 6,406 bytes, SHA-256 51e373dd9df6c20d8efc370ebb3beca2f55739c179c96dee5885a5e28c917627.
- 281 uniquely named SNP loci × 50 individual rows in seven POP blocks; 14,050 possible genotype calls, 10,001 observed (71.18%), 4,049 missing (28.82%).
- Observed genotype codes: 0101, 0102, 0202, 0000 (missing).
- Original POP order: C2, C3, C4, C1-2, C1-3, C1-4, C1-1, **not chronology**.
- Repeated code C1-1, C1-2 etc. denotes a population, **not a duplicated individual**. Different rows within each block were distinct genotypes.

## Exact README matched populations

| Code | Origin | n | Call rate | Ho among called genotypes | Polymorphic SNP loci |
|---|---|---:|---:|---:|---:|
| C1-1 | Awaji wild, 2007 | 2 | 63.52% | 0.1036 | 38 |
| C1-2 | Awaji wild, 2019 | 8 | 70.24% | 0.1134 | 83 |
| C1-3 | Awaji origin 2000, ex situ at Sanda | 8 | 85.05% | 0.0669 | 48 |
| C1-4 | Awaji origin 2014, ex situ at Himeji | 8 | 55.12% | 0.1162 | 89 |
| C2 | Shizuoka 2019 | 8 | 69.44% | 0.0474 | 33 |
| C3 | Mie 2019 | 8 | 75.98% | 0.1282 | 98 |
| C4 | Wakayama 2019 | 8 | 73.18% | 0.0930 | 77 |

Ho is the fraction of heterozygous *called* diploid SNP genotypes among these ascertained loci, not genomewide nucleotide diversity. Polymorphic SNP counts cannot be directly compared between historical n=2 and modern n=8 or where call rates differ. A significant temporal decline in genetic diversity **is not established**.

## Historical allele observation / ex situ retention

C1-1 (2007, n=2) vs C1-2 (2019, n=8): **20 locus-specific alleles** observed historically but not detected among current samples at callable loci. **19/20** occur in *only one* of the two historical individual rows. Additional sample coverage gates reduce the 20 count to 19 (at least 2 contemporary calls), 14 (at least 4), 10 (at least 6) and 2 (all 8), respectively. The historic two individuals have 80 loci callable in both; both historical and all eight current individuals have only 10 fully jointly callable loci.

Of those 20 alleles, **5** are observed in ex situ C1-3, **4** in C1-4; **6** in their union, **3** in both, and **14** in neither sampled ex situ group. At loci with at least one historical call, 63 current alleles were not sampled in 2007; 6 further contemporary alleles occur at loci with no historic genotype calls and must not be counted as historic absence.

Descriptive 2-versus-2 sensitivity: all 28 possible current pairs against the 2 historic samples, requiring the locus to be callable in all four individuals. 19–60 SNPs per pair; mean (current minus historical) observed alleles per matched locus −0.0705; 22/28 negative, 2/28 positive, 4 tied. These 28 pairs are highly overlapping/nonindependent and use different callable loci: **not a hypothesis test**, not proof of loss or selection.

## Regional genetic structure: Hudson-type pooled SNP FST

For each comparison, only SNPs called in at least 4 individuals in each population were used. For called diploid allele frequency p, numerator is (p1−p2)^2 − p1(1−p1)/(2n1−1) − p2(1−p2)/(2n2−1); denominator p1(1−p2)+p2(1−p1); overall ratio is the ratio of locus sums, not the mean of per-locus ratios.

Below, intervals come from a local independent NumPy-based **1,500-SNP-locus bootstrap, RNG seed 20261119**. They are *conditional* on retained loci, do not represent sampling of independent regions, may underestimate linkage dependence, and may differ at the last decimal from a separate standard-library PRNG replay. Leave-one-out (LOO) removes one individual from *each* group per refit and reports the full range.

| Pair | Eligible SNPs | FST | Conditional locus-bootstrap 95% interval | LOO range |
|---|---:|---:|---:|---:|
| Awaji wild 2019 – Shizuoka | 197 | 0.7787 | 0.717–0.829 | 0.749–0.793 |
| Awaji wild 2019 – Mie | 214 | 0.6911 | 0.635–0.741 | 0.645–0.707 |
| Awaji wild 2019 – Wakayama | 218 | 0.6111 | 0.531–0.678 | 0.579–0.660 |
| Shizuoka – Mie | 212 | 0.5992 | 0.511–0.672 | 0.576–0.618 |
| Shizuoka – Wakayama | 203 | 0.7470 | 0.672–0.805 | 0.730–0.781 |
| Mie – Wakayama | 224 | 0.6245 | 0.556–0.687 | 0.594–0.653 |
| Awaji wild 2019 – ex situ C1-3 | 236 | 0.1527 | 0.091–0.227 | 0.092–0.180 |
| Awaji wild 2019 – ex situ C1-4 | 170 | 0.0662 | 0.024–0.111 | −0.007–0.106 |
| ex situ C1-3 – ex situ C1-4 | 176 | 0.2848 | 0.200–0.362 | 0.232–0.324 |

The six among-geographic-population contrasts are **large (FST 0.60–0.78) and leave-one-individual-out stable**, supporting population genomic structure *within one named species*. They are not evidence for specific selection, hybridization, cryptic species, or future management response. The C1-4 versus current result is coverage-sensitive: FST approximately +0.165 at ≥2 calls per group and −0.003 at ≥6; do not elevate this weaker effect to a firm conservation-history result.

**Additional source-level ascertainment constraint (original Dryad README, section 6):** loci present only in old samples were manually excluded as possible contamination during the published MIG-seq processing, alongside other minor-allele-frequency and coverage filters. Thus the 20 historically observed/not-current alleles are conditional on the retained SNP panel: they cannot estimate an unconditional historical allele-loss rate, even if missingness were completely resolved. This is a published preprocessing decision, not a new finding from the genotype calls.

## Interpretation boundary for CCOC / MLTR

**Confirmed empirical premise:** species name alone does not represent the sampled nuclear-SNP population state. Historical labels and ex situ provenance also encode necessary sampling information. **Not confirmed:** action-conditioned outputs, response sufficiency, route coherence, minimal historical repair, any selection mechanism, or the mathematical CCOC/MLTR finite theorems. To test those, acquire sample-linked genotype × phenotype × controlled environment/management-response data, and compare a preregistered species/phenotype model with a genomic-ancestry-augmented model under held-out populations.

### Reproduction notes

The PR source-locked parser handles repeated POP labels and README-verified group membership; it has a local uploaded-ZIP option. Its unit tests use synthetic genotypes only; this document was computed from the supplied original ZIP using independently checked allele extraction and NumPy SNP-frequency calculations. The original ZIP is intentionally excluded from GitHub.

No canonical Paper A claims or main-branch files were changed by this audit.