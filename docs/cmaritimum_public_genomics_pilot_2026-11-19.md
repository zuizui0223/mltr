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

For a locally downloaded source:

    python scripts/audit_genepop_cmaritimum.py --input /path/to/Genepop_Cmaritimum.txt --out artifacts/genepop_cmaritimum_local_qc.json

The report records raw-input SHA-256, per-POP sample counts, locus count, called-genotype fraction, observed diploid heterozygosity, polymorphic loci, allele inventories and duplicate-ID alerts. The script does not output or commit raw genotypes.

## The group-label and historical-detection gate

GENEPOP POP-block numbers are *not* automatically biologically meaningful. Inspect the original Dryad README, original study methods and specimen labels before making a CSV with exactly the headers:

    pop_index,group

Assign each actual POP block exactly once, using past_wild, current_wild, ex_situ only. Do not guess from file order. Use the reviewed file with the script's --population-map option. Detected-allele counts are descriptive and must not be called losses without sampling/missingness controls.

## Access boundary already observed

Initial GitHub Actions run **44475698404**:
- Eight synthetic parser/QC tests passed.
- Dryad /api/v2/datasets/{doi}/download returned **HTTP 401 Unauthorized**.
- Thus no real genetic rows or alleles were measured in this run, and no real-data artifact was produced.

A single bounded alternative via the published Dryad metadata, the exact pinned version/file IDs, and public file-stream URLs has been added. The fallback checks DOI, size and provided digest before parsing. If access still requires authentication, the original 73.09 KB Genepop source must be obtained via a lawful user-facing download; do not treat a file listing as genotype access.

## No claim inflation: promotion criteria

| Gate | Status | What is required |
| --- | --- | --- |
| S0: published DOI/file identity | PASS | Exact cited source |
| S1: real file bytes and parsing | PENDING | Original SHA-256 and validated individual/locus totals |
| S2: population-group crosswalk | PENDING | README-backed labels and missingness by group |
| S3: group genotype contrast | NOT RUN | Comparable coverage, uncertainty and detected-allele caveats |
| S4: MLTR genomic response sufficiency | NOT IDENTIFIABLE | Linked fitness/action outcomes and held-out genotype-response predictions |
| S5: MLTR history coherence | NOT DEFINED | Explicit alternative histories and declared total state correspondence |

When S1–S3 pass, same-named species with different sampled allele inventories supports within-species genetic heterogeneity, not an action-conditioned decision difference. The latter requires independent response data and S4.

## Sources

- [Dryad DOI](https://doi.org/10.5061/dryad.tb2rbp03j)
- [EAzami nuclear evidence audit](https://github.com/zuizui0223/EAzami/blob/main/docs/chapter2/EAST_ASIA_INDEPENDENT_NUCLEAR_EVIDENCE_AUDIT_V1.md)
- [MLTR species genomics bridge](species_genomics_application_gate_2026-11-19.md)
- [Bounded public source check](../.github/workflows/public-genepop-source-audit.yml)
