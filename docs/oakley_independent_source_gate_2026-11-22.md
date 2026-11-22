# Oakley 2023 independent source gate — 2026-11-22

**Current state:** candidate located; original files unavailable in this session. No joined dataset, model fit or empirical verdict exists. The executable study selected for the current increment is [Exposito-Alonso 2019](exposito_genomic_prediction_protocol_2026-11-22.md).

## Evidence and access

[Oakley et al. (2023)](https://doi.org/10.1111/mec.17045) describe 400 Arabidopsis recombinant inbred lines (398 genotyped), 348 SNP markers, two sites in Italy and Sweden, and eight experimental years. The reproductive target is fruit output per planted seedling. The published annual fitness estimates adjust for experimental spatial effects; they are not individual seed counts. These are publication descriptions, not verified dimensions of the original files.

The [Dryad deposit](https://datadryad.org/dataset/doi:10.5061/dryad.g1jwstqw6) has dataset ID 109134 and version 238395. Its public API lists six originals totaling 782,553 bytes. The saved [retrieval manifest](results/oakley_source_retrieval_2026-11-22.json) distinguishes expected source digests from actual downloads. No originals were downloaded. Tested API downloads returned HTTP401, and the tested HTML file stream returned HTTP403. [Dryad's official API documentation](https://github.com/datadryad/dryad-app/blob/main/documentation/apis/api_accounts.md) requires authentication for file downloads. No access workaround was attempted. Searches of the shared files did not locate this dataset.

## Required next work if originals become available

1. Verify all six original payloads against the deposit's SHA256 digests and sizes. Record archive provenance separately.
2. Inspect the README and R/qtl import arguments before reading CSV axes. Distinguish markers, map metadata, traits and line IDs. Do not infer unseen column names or force the published counts.
3. Establish allele codes, missingness and exact genotype–phenotype matches. Inspect actual site/year labels and distinguish annual summaries, adjusted means, normalized scores and across-year averages.
4. Determine which outcome-dependent spatial adjustments or transformations were shared across lines. A whole-line split in a later predictor does not undo upstream fitting of the target summaries.
5. Freeze a prediction protocol before scoring. Use outcome-independent measured markers rather than the paper's fitness-selected QTL.

A conditional benchmark could predict the authors' published summaries for held-out lines in this two-parent cross. Without raw observations and adequate adjustment details, it cannot certify isolated individual-plant validation. An unseen recombinant line from two parents also does not establish transfer to a new source population. The full-data construction of the summaries and the exact season labels remain unresolved. This gate supplies no new evidence for the formal MLTR theorems.
