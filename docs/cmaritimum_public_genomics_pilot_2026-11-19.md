# Cirsium maritimum public genomics pilot — 2026-11-19

Status: **descriptive source/analysis gate**. Not a new MLTR theorem or an empirical validation of decision sufficiency.

## Published source

Nakahama et al. 2022, Dryad DOI **10.5061/dryad.tb2rbp03j**; published 2022-08-15. The deposited focal source is **Genepop_Cmaritimum.txt** (73.09 KB). The other species' Genepop matrices in the Dryad archive are excluded.

The published study uses MIG-seq with museum-derived past wild, current wild, and ex-situ samples from Awaji Island. Its cross-species decline in wild genetic diversity was not statistically significant. It reports alleles observed in past or ex-situ samples but not in the sampled current wild plants. Unobserved does not mean proven extinct.

## Reproduction (Python standard library)

Run the synthetic-only tests:

    python -m unittest discover -s tests -p test_genepop_cmaritimum_audit.py -v

Attempt the official public Dryad source:

    python scripts/audit_genepop_cmaritimum.py --from-dryad --out artifacts/genepop_cmaritimum_source_qc.json

For the now-received original 2022-08-15 Dryad ZIP (source README crosswalk required):

    python scripts/audit_genepop_cmaritimum.py --input-zip /path/to/doi_10_5061_dryad_tb2rbp03j__v20220815.zip --out artifacts/genepop_cmaritimum_local_qc.json

For a separately extracted genotype file, include the reviewed README:

    python scripts/audit_genepop_cmaritimum.py --input /path/to/Genepop_Cmaritimum.txt --readme /path/to/README.txt --out artifacts/genepop_cmaritimum_local_qc.json

The report records raw-input SHA-256, per-POP sample counts, locus count, called-genotype fraction, observed diploid heterozygosity, polymorphic loci, allele inventories and duplicate-ID alerts. The script does not output or commit raw genotypes.

## The source-verified historical group-label gate

The supplied original README has been opened and checked. The seven POP blocks are **C2 / C3 / C4 / C1-2 / C1-3 / C1-4 / C1-1**. These are original group codes, **not unique sample IDs nor chronological order**. C1-1 is Awaji wild 2007 (n=2), C1-2 Awaji wild 2019 (n=8), C1-3 origin 2000 ex situ at Sanda (n=8), C1-4 origin 2014 ex situ at Himeji (n=8); C2–C4 are Shizuoka, Mie and Wakayama 2019 comparators (n=8 each). The reader verifies all seven code/site/year/ex-situ statements from the README before enabling history-specific output. A generic group-map CSV is not needed and must not be mixed with this verified README.

## Access history versus current source status

Earlier GitHub Actions runs **44475698404** and **44476940036** confirmed that direct package download returns **HTTP 401** and file-stream download **HTTP 403**. The problem was limited to public API retrieval; automatic PR downloads are now disabled. This is retained as reproducibility provenance, **not a current raw-data blocker**.

The user supplied the original **222,683-byte ZIP**, SHA-256 **e81efee9bfe1f1176609bbcd3a1f23f9be63c698e614db09884676684ceb9b8c**, with the exact **73,087-byte Genepop_Cmaritimum.txt**, SHA-256 **ecf44241752d8844e35d9cbdc4fa2d57d8aadbc3f2e1f0f17f77c4a4283fcd9e**. The independent local source audit recovered **50 genotype rows, 281 SNPs, 7 population blocks, 10,001 / 14,050 called genotypes (71.18%)**. Full quantitative evidence, reanalysis, and sampling limitations are in [real-source genomic results](cmaritimum_real_genomic_results_2026-11-19.md).

## No claim inflation: updated promotion gates

| Gate | Status | Verified observation / still required |
| --- | --- | --- |
| S0: exact published DOI/file identity | **PASS** | Original ZIP and README SHA-256 |
| S1: real file bytes and parsing | **PASS** | 50 rows / 281 SNPs / 7 POP blocks |
| S2: population-group crosswalk | **PASS** | Year, site, source-group and ex-situ labels checked against README |
| S3: group genotype contrast | **DESCRIPTIVE COMPLETE** | 20 historic SNP alleles not detected in current sample; 6 observed in at least one ex-situ group; strong regional SNP Fst structure, with n/coverage controls |
| S4: MLTR genomic response sufficiency | **NOT IDENTIFIABLE** | Requires same-sample genotype, intervention/abiotic exposure and fitness/reproductive outcomes with held-out population validation |
| S5: MLTR route coherence | **NOT DEFINED** | Requires declared alternative replacement histories and total source–target relations |

Group genotype differences are empirical evidence that one named species can contain strongly distinct nuclear-SNP states. **They do not themselves prove action-conditioned ecological response or validate the finite MLTR/CCOC theorem.**

## Sources

- [Dryad DOI](https://doi.org/10.5061/dryad.tb2rbp03j)
- [EAzami nuclear evidence audit](https://github.com/zuizui0223/EAzami/blob/main/docs/chapter2/EAST_ASIA_INDEPENDENT_NUCLEAR_EVIDENCE_AUDIT_V1.md)
- [MLTR species genomics bridge](species_genomics_application_gate_2026-11-19.md)
- [Bounded public source check](../.github/workflows/public-genepop-source-audit.yml)
