# Independent accession × intervention-response gate — exploratory teaching-source audit (frozen 2026-11-19)

**Study identity and source status.** A University of Toronto R-course data file [`Fitzpatrick_2018.csv`](https://github.com/UofTCoders/rcourse/blob/master/data/Fitzpatrick_2018.csv), source Git blob **8a79d0a5aa9e21854a556cd63c4afc5af6199b1c**, was fetched and inspected directly, containing 879 plant-level fruit counts, 44 nominal accession IDs, 2 watering conditions D/W, 2 microbial inoculum conditions L/S, and five complete growth-chamber rack/replicate labels. The [course lesson](https://uoftcoders.github.io/rcourse/lec08-linear-mixed-effects-models.html) describes this public file explicitly. The related [Fitzpatrick, Mustafa & Viliunas (2019) paper](https://doi.org/10.1111/jeb.13426) reports a **38-accession/760-plant drought experiment** and the original [Dryad](https://doi.org/10.5061/dryad.334765v) file is named `full_data_drought.csv`. Thus **the teaching mirror cannot currently be authenticated as a byte-exact reproduction of the published experiment**. Do not claim that its 879 observations reproduce the original 760-plant analysis. This is a new source-provenance *blocker*, not a discrepancy to smooth over.

**Genetic-information boundary.** `accession` is a nominal genetic-lineage label. The teaching source has **no SNP or whole-genome genotype matrix**. Any result is at most accession-conditioned *phenotypic response prediction*, **not species genomics** and **not an MLTR carried-label-history proof**.

## Frozen contrast, set before looking at genotype-specific response statistics

Endpoint is `sqrt(fruit)`: number of recorded fruit per plant, square-root transformed. This is **not** lifetime seed production, which additionally needs accession- and treatment-specific seeds-per-fruit data. Retain zero-fruit records as zero (do not delete mortality). Compare three *fixed* hierarchical-shrinkage predictors using the same training/testing observations in all models:

- **P0 (species-coarse action interface):** training mean transformed fruit for each of 4 watering × microbial treatment actions.
- **P1 (accession identity):** P0 plus shrunken accession-specific mean residual across all actions. Shrinkage pseudo-count `k_accession=10`.
- **P2 (accession × action response):** P1 plus shrunken accession × full action-cell residual, `k_action=10`.

All predicted values are estimated from training rows only. No effect of flowering time, counter, tray, rack, or collection year is used to select features or tune the prediction after observing outcomes. No extrapolation to unseen accessions is claimed.

**Held-out unit:** growth-chamber rack / replicate **1 through 5**, each wholly withheld in one fold, so all five observation blocks are disjoint in test. Validate that the original `replicate` field agrees with `rack` per record. Every genotype × water × microbe cell must have training support before a fold is considered valid.

**Primary estimand:** `P2 minus P1` gain in held-out *squared error*, `MSE(P1)-MSE(P2)`, averaged across all 879 plants. Positive means accession × action information improves observed fruit prediction beyond accession baseline. Secondary `P1 minus P0` tests only whether lineage intercepts carry information. Report each fold and each action separately; 2,000 conditional bootstrap resamples of the **44 accession identities** for a descriptive interval; note folds share training data and accession resamples are not an external validation experiment.

**Exploratory positive gate:** all five fold directions must be nonnegative, the accession-equal-weight average `P2-P1` must be strictly positive, the conditional accession-bootstrap 2.5% quantile must be above zero, and the score gain must be positive in at least three of four action contexts. If any gate fails, **no supported accession×action predictive gain** is claimed. Report negative and ambiguous outcomes unchanged. Fixing shrinkage `k=10` before evaluation prevents cherry-picking. A prespecified descriptive sensitivity at `k=5` and `k=20` is permitted without optimizing the primary result.

## Raw-data QC admission

1. The source file must match the exact Git blob **8a79d0a5aa9e21854a556cd63c4afc5af6199b1c** (Git-compatible SHA-1 over full file), with recorded byte size, SHA-256 and source URL.
2. Expect exactly 879 rows, 44 unique `accession` codes, 5 replicated racks and the 4 designated actions. Every fruit value must be nonnegative and numeric; all observations (including zero fruit and missing flowering-time readings) remain in the primary analysis.
3. **One repeated accession×water×microbe×replicate assignment** was observed in the teaching source; **do not deduplicate**, as these are plant rows without unique specimen IDs. Record the incomplete cell and repeated assignment separately.
4. `counter` varies with rack, and tray nests within rack. This prevents identifying any unique mechanistic role for microbe or accessions in a simple predictive model. Randomized treatment design in the original publication does not by itself authenticate this course-file mirror.
5. The source may be downloaded only from its publicly linked GitHub course location. No raw sample-level file, accession vectors or simulated biological findings are committed.

## Scientific interpretation

A positive P2 increment would demonstrate a **predictively useful accession×action distinction within this educational excerpt** under the five observed blocks. A negative result would not negate the prior peer-reviewed paper's genotype-specific environment-response analysis. Neither case alone establishes a declared total **source→target replacement relation**, source-label inheritance, route coherence, or exact minimum-history-mode theorem. Proper MLTR operational-sufficiency validation needs declared ecological source and target, repeated action outcomes, and a defensible observation model.

**Strong independent follow-up (not accessed yet):** Luo et al. (2025), [published Arabidopsis knockout × drought fitness screen](https://doi.org/10.1111/mec.70129) with [Dryad archive DOI 10.5061/dryad.qrfj6q5s4](https://doi.org/10.5061/dryad.qrfj6q5s4), provides genotypes defined by molecular knockout identities and independently tested drought actions, plus replicate follow-up. Its **raw archive has not been inspected or acquired**, so this is a source candidate, not a claimed result.
