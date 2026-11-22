# Exposito 2019 genomic-information decision test: rainfall-allocation value not supported

**Analysis date:** 2026-11-22. **Verdict:** M1's genomic-distance predictor did **not** pass the frozen positive *treatment-allocation* decision-value gate in either the accession-disjoint or geographic-cell-disjoint validation. This is a **post-result exploratory decision objective** on the same published experimental data, not an independent randomized policy trial or an exact MLTR theorem test.

## Pre-outcome source, models and action contract

The [protocol](exposito_rainfall_decision_protocol_2026-11-22.md) was committed to the PR branch at \`2dc667c\` **before** computing any decision/utility values. It defines a fixed 25%-budget simulated choice: within each held-out fold and each fixed **experimental site × pot density** stratum, select exactly \`ceil(0.25 * heldout accessions)\` genotypes for **high rainfall**, the others for **low rainfall**. Both policies spend the same hypothetical treatment budget. Ties are broken by numeric accession identifier; *site and density are not available actions*.

This uses the **identical 514 accessions × 8 settings** previously admitted by the Exposito genomic benchmark. Original experimental source data are the Figshare v3 \`S_DATASETS.xlsx\` (3,725,000 bytes, SHA-256 \`032045433e3ace035977c11ff5d0ae8731335e8210c6cee14d64575ae0bebd05\`) and the author's explicitly labelled genetic-distance \`ibs1001g.rda\` (8,947,948 bytes, SHA-256 \`906724ce620a30a8c199ade07c5ffaa27aa7b1a91e8229f63b27e882547a70ad\`). Public files were downloaded by GitHub Actions during this PR, checked *byte-for-byte* against the existing pinned source contracts, and parsed with the already-merged source pipeline. Raw phenotype/genetic matrices are **not** committed to GitHub.

- M0 uses collection coordinates and their fixed quadratic geographic kernel.
- M1 uses the same geographic kernel plus the published inter-genotype genetic-distance kernel.
- Each model's four-candidate ridge tuning, nested inner splits, five outer accession-disjoint splits, and five-degree geographic-cell sensitivity are **unchanged** from the previously frozen genomic MSE benchmark.
- **Crucial:** model predictions are normalized by the mean of each of the eight **training** treatment contexts. Comparing normalized high- versus low-rainfall predictions as action utilities would be invalid. The decision audit multiplies every prediction by its **own training-context raw \`Fitness\` mean** before comparing high and low outcomes.
- Before calling the existing outer-fold fitter, every held-out accession's entire eight-component target row was explicitly overwritten with NaNs in a copy of the input. Only after fit and action choice is the held-out published raw \`Fitness\` outcome used to score allocations.

The outcome is the **published accession×condition estimated lifetime seed output per planted seed**, not independently re-counted plant-level seeds. High/low rainfall was experimentally manipulated, but the choice objective is a retrospective hypothetical resource allocation. Real irrigation/rainfall manipulation costs and feasibility were not measured.

## Main result

| Evaluation method | M0 realized average fitness | M1 realized average fitness | Mean M1−M0 gain | Conditional 95% cluster interval | Changed assignments | Positive folds |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| **Held-out accession (primary)** | 2466.817 | 2481.430 | **+14.613** (+0.592%) | **[−105.055, +134.493]** | **182 / 2056** (8.85%) | **3 / 5** |
| Held-out five-degree geographic cells (sensitivity) | 2504.898 | 2493.412 | **−11.486** (−0.459%) | **[−555.604, +447.471]** | **214 / 2056** (10.41%) | **1 / 5** |

Units: original final D4 published *estimated fitness per planted seed* (raw, not relative to a per-context training mean). There are **514 accession × 4 fixed site-density decision opportunities = 2,056 policy comparisons**. For each held-out fold the two policies select exactly the same number of high-rainfall recipients in each site-density stratum. Changes are per accession×stratum assignments; each switch of one accession into high rain and one out registers two changed decisions.

The **frozen primary gate** required: positive pooled average, conditional lower 95% bound >0, strictly positive gain in at least **4/5 outer folds**, strictly positive in at least **3/4 site-density strata**, and at least one changed decision. It **fails the confidence-interval, fold, and stratum criteria** (two of four strata positive). The geographic sensitivity fails the pooled-gain, interval, fold and stratum requirements. The sign of the point estimate is also split-dependent.

## Which ecological conditions explain the observed policy differences?

| Fixed site × planting-density stratum | Primary M1−M0 raw fitness gain | Spatial-heldout gain | Primary changed assignments |
| --- | ---: | ---: | ---: |
| Madrid × single plant | **−0.733** | −58.558 | 36 |
| Madrid × high density | **−1.853** | −5.566 | 68 |
| Tübingen × single plant | **+58.873** | +17.877 | 44 |
| Tübingen × high density | **+2.166** | +0.303 | 34 |

**The largest primary realized action gain is Tübingen × single plant**, not Madrid low-rainfall/high-density. This is distinct from the previous **genomic MSE concentration** (Madrid low-rain/high-density contributed ~90% of the small normalized prediction-error improvement). The two quantities are not interchangeable: a reduction in conditional prediction MSE need not change the treatment ranking, and the ranking comparison must restore original fitness units.

Raw-fitness MSE across **all eight** contexts was 2,852,275 (M0) versus 2,853,138 (M1) in the primary. These are diagnostic raw-scale losses, different from the original benchmark's training-relative normalized MSE (0.699939 vs 0.694101). Even the *sign* of a model comparison may differ when the score units change. Geographic-cell raw MSE was 2,894,281 (M0) vs 2,874,934 (M1); that score difference did not imply a positive allocation value.

## Meaning and limitations

The strict reading is: **for this fixed 25% high-rainfall allocation policy, adding the author's genetic-distance state to the fixed coordinate-based predictor does not establish a reproducible improvement in retrospective experimental reproductive output**. The main policy's positive point estimate is small (~0.59%), its conditional uncertainty includes zero, the five outer folds disagree, and the spatial-heldout point estimate reverses sign.

This does **not** establish zero genomic information, zero genotype×rainfall interaction, a harmful genetic predictor, or a new causal mechanism. It does not show a universal claim that detailed ecological states are unnecessary in decision-making. It also does not prove the formal MLTR exact source→target history, carried-label obstruction, or coarsest action-sufficient quotient. The original 2019 paper's genomic adaptation findings remain prior art.

There is a **single source experiment** with summarized outcomes from different plants/pots under each treatment, not measured simultaneous potential outcomes for one individual. Original source image/seed calibration and 360 duplicated pot keys remain upstream measurement constraints. The high-rainfall quota was a **new hypothetical post-result policy objective**, not the experiment's actual resource allocation protocol, and real costs of water delivery are not included. The conditional bootstrap holds fits, source data and the full chosen assignment fixed; it does not quantify uncertainty in refitting, source measurement, genotype relatedness, new sites, or policy deployment.

A new independent validation would require a precommitted rainfall-allocation decision rule, experimental cost accounting and newly randomized policy assignments rather than another retrospective reweighting of the same 2016 field data.

## Reproducibility and GitHub validation

Run from this repository on a Python 3.12 environment with NumPy, openpyxl and rdata. The dedicated [workflow](../.github/workflows/exposito-rainfall-decision.yml) fetches exact public originals to the temporary GitHub runner, uses the old source admission code to verify both hashes and reconstruct 514×8, runs the existing M0/M1 nested KRR and the new [source-locked action evaluator](../scripts/audit_exposito_rainfall_decision.py), and retains **only the aggregate result**. GitHub Actions run [45012731642](https://github.com/zuizui0223/mltr/actions/runs/45012731642) completed both source-free synthetic unit tests (10/10) and real public-file prediction/decision evaluation.

The complete 2,056-decision [machine-readable results](results/exposito_rainfall_decision_2026-11-22.json) were parsed from the successful runner's aggregate-only output and re-checked independently as **weighted sums of all fold means and of all four stratum means**; both recover the original mean gains to floating-point precision. Every fold's high-rainfall quota and total changed decisions, both source input SHA-256s, source IDs hash, original 2019 study DOI and frozen protocol Git-blob fingerprint were checked before committing. Individual IDs and treatment rankings are not redistributed.

Example manual source-locking run (existing public originals retained outside Git):

\`\`\`bash
python scripts/prepare_exposito_genomic_fitness.py \
  --workbook /path/to/S_DATASETS.xlsx \
  --ibs /path/to/ibs1001g.rda \
  --out-npz /tmp/prepared.npz \
  --out-audit /tmp/exposito_source_audit.json

OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
python scripts/audit_exposito_rainfall_decision.py \
  --prepared /tmp/prepared.npz \
  --source-audit /tmp/exposito_source_audit.json \
  --protocol docs/exposito_rainfall_decision_protocol_2026-11-22.md \
  --out /tmp/exposito_rainfall_decision.json
\`\`\`

No modification to the canonical Paper A manuscript, theorem code, PR #52 frozen original genomic benchmark, or PR #53 loss concentration audit.
