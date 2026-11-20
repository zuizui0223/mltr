# Predefined exploratory action-decision-value test (2026-11-20)

**Protocol frozen before action-value calculation.** This is a post-result follow-up to prior *prediction* analysis. It is not an independent biological experiment, a genomic-SNP demonstration, or an exact MLTR theorem test.

## Data and provenance
- Source: University of Toronto rcourses teaching CSV, public Fitzpatrick_2018.csv, source Git blob SHA-1 8a79d0a5aa9e21854a556cd63c4afc5af6199b1c, CSV SHA-256 5872c228388bd6422458fa6f65a15e59e0ea283973ead376f5d3f7cd47ee485c.
- The educational copy has 879 plant records, 44 nominal accession labels, 5 complete experimental rack replicates, 4 actions.
- The Fitzpatrick et al. (2019) published drought study reports 38 accessions/760 individuals, while its original Dryad DOI 10.5061/dryad.334765v lists full_data_drought.csv and seed.count.drought.csv. **The original Dryad CSV has not been obtained or crosswalked; do not equate it to the teaching copy.**
- Accession is a lineage label, not SNP or whole-genome evidence. The original paper already identifies genotype-dependent drought/microbe fitness differences: prior art.

## Fixed action/policy problem
- Four experimental options D|L, D|S, W|L, W|S (dry or watered; live or sterilized microbe condition).
- Assume **equal action costs solely for this retrospective test**. Treatment costs are not equal in actual ecological management. Do not call the output a deployable conservation policy.
- Utility is **square root of observed fruit count**. It is not lifetime seeds.
- For each of the five replicate racks, hold out the entire rack, fit the prior P0, P1, P2 estimators on the other four racks with unchanged pseudocounts k_accession=10 and k_action=10.
- P0 chooses the action with greatest training mean sqrt fruit. P1 adds an accession-specific intercept common to every action and hence chooses **the same** action as P0.
- P2 chooses the largest predicted value after adding shrunken accession×action residual; subtracting a genotype-wide mean from all four P2 adjustments would NOT change this action ranking.
- Break action ties in deterministic order D|L, D|S, W|L, W|S.

## Held-out evaluation (before inspecting outcomes)
- A test unit is an accession×held-out-rack panel with **exactly one observed individual in each of all four actions**. Omit incomplete panels and panels with duplicate action records based on DESIGN only, never on fruit count.
- Within each full panel, measure the fruit utility of P2's chosen action and P0's chosen action from different randomized treatment plants of the **same accession and rack**.
- Primary contrast: average sqrt-fruit utility gain of P2 choice minus P0 choice across complete held-out panels. If P2 and P0 choose the same action, difference is zero.
- Report number of admissible panels, total observations excluded by panel completeness, changed-action panel count, choice mix, gain by held-out rack, equal-accession mean and fixed-prediction accession-cluster bootstrap 95% interval with 2,000 draws, seed 20261120.
- Positive exploratory gate: observed gain >0, lower conditional accession-bootstrap interval >0, and strictly positive gain in at least 3 of 5 held-out racks. Otherwise declare NOT SUPPORTED even if the P2 genotype prediction MSE was lower.
- No post-outcome switching to other outcome scales, action-cost weights, action restrictions, or other shrinkage.

## Interpretation
This tests whether retaining the existing *accession×action response* estimate actually changes a **choice** and improves an out-of-rack experimental utility. It is not a within-individual counterfactual effect; four outcomes belong to separate plants per accession/rack. It cannot establish genotype causation, ecological source-to-target total relations, MLTR route coherence, history modes, or exact decision sufficiency. A positive decision gain would be an exploratory ecological application *analogue* under the teaching copy only.
