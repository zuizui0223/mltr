# Post-result context-concentration audit of Exposito 2019 genomic prediction

**2026-11-22 — descriptive loss decomposition only.** This audit reads the **already archived** out-of-fold model losses from [the Exposito genomic prediction benchmark](exposito_genomic_prediction_result_2026-11-22.md), source Git blob \`68cef71c368a17ef63fac066f0260f289fe99bc0\`. It does **not** refit models, rescore individual observations, generate new confidence intervals, change the original frozen protocol or constitute independent biological replication. The context highlighted here was identified **after the original model results were inspected**.

## Main observation

The earlier mean squared error reduction from adding a published genetic-distance kernel was small and had a conditional interval crossing zero. Most of that *net* reduction comes from **one of eight factorial contexts: Madrid × low rainfall × population/high-density pots**, abbreviated \`mlp\`.

| Same fitted predictions, different validation split | Overall M0−M1 MSE gain | \`mlp\` contribution to pooled gain | \`mlp\` share of signed net gain | \`mlp\` share of M0 baseline loss | Mean gain over other seven contexts |
| --- | ---: | ---: | ---: | ---: | ---: |
| Unseen accession within the observed experimental panel | **+0.00583745** | +0.00524539 | **89.86%** | **59.25%** | +0.00067664 |
| Held-out five-degree geographic cells | **+0.00363911** | +0.00340350 | **93.53%** | **58.84%** | +0.00026927 |

The seven other contexts' M0 MSEs average 0.325996 and 0.330759 under accession and geographic validation, respectively. Consequently, their *pooled* relative MSE reductions are only **0.208%** and **0.081%**, compared with the original all-context reductions of **0.834%** and **0.518%**. These are **score-only exclusions from existing predictions, not re-trained leave-one-context-out experiments**.

### Exact accounting

With eight equally weighted context-specific losses, define

\`g_c = MSE(M0,c) - MSE(M1,c)\`, and \`G = (1/8) * sum_c g_c\`.

Then \`mlp\`'s arithmetic contribution to the pooled gain is \`g_mlp / 8\`, and its signed share of that net is \`g_mlp / (8*G)\`. The baseline-loss share is a different quantity, \`MSE(M0,mlp)/(8*MSE(M0))\`. The signed net share is **not** a fraction of explained biological variance or proof that the context causes selection; cancellation among positive and negative contributions can even make signed shares exceed 100% in other datasets.

For this source, the direct \`mlp\` MSE gains are **+0.04196316** (accession) and **+0.02722796** (geographic). The \`mlp\` M0 relative MSE reductions are **1.265%** and **0.823%**. The \`mlp\` baseline context accounts for **59.25%** and **58.84%** of total M0 MSE. Thus context heterogeneity in the original target/error scales is a plausible contributor to the pronounced *numerical* concentration.

Five of eight context-specific MSE increments are positive under each validation scheme. **Neither scheme passed the originally declared five-fold/interval-based positive gate**: the accession-fold conditional 95% interval is [−0.003921, +0.016383], and the geographic-cell conditional 95% interval is [−0.003442, +0.011120]; only 3/5 folds improve in each.

## Equalizing percentage rather than squared-error contributions — descriptive only

Context-specific relative reductions \`100 * g_c / MSE(M0,c)\` average **0.471%** (accession split) and **0.660%** (geographic split) when eight contexts are each weighted equally **after** dividing by their individual baseline MSEs. These new descriptive summaries differ from the original pooled-loss estimand and carry **no new interval or confirmatory acceptance gate**. They are reported to disclose scale sensitivity, not to select a more favorable response.

## Scientific boundary and candidate explanation

A hypothesis worth external testing is that genome-derived state similarity predicts reproductive output more usefully **under simultaneous water limitation and competition** than under benign conditions. The current audit does *not* test that interaction: only Madrid low-rain/high-density showed the large numerical contribution, and its baseline MSE is disproportionately large. Separating genuine conditional predictability from outcome-scale heteroscedasticity, shared image calibration and geographic-genetic confounding would require a **new predeclared independent experiment or validation**, not reweighting these same archived scores.

Neither the prior benchmark nor this decomposition evaluates **what experimental treatment a genotype should receive**. No decision-value claim or exact MLTR source–target/carried-label theorem validation is implied.

## Reproduce from committed aggregates, without original raw files

The [stdlib-only script](../scripts/audit_exposito_context_leverage.py) reads [the pinned production result](results/exposito_genomic_prediction_2026-11-22.json) and stops if its exact Git blob, cohort, context identities, model names, original numerical gate status, or pooled/context arithmetic is inconsistent. [Regression/synthetic tests](../tests/test_exposito_context_leverage.py) verify both synthetic identities and the archived original result. [Machine-readable audit](results/exposito_context_leverage_2026-11-22.json) retains every context, baseline-loss share, relative-gain accounting, and the eight score-only context omissions.

\`\`\`bash
python scripts/audit_exposito_context_leverage.py \
  --out artifacts/exposito_context_leverage.json
\`\`\`

The independent Exposito 2019 source experiment is a published prior study, not a new discovery of genotype-by-drought selection. The existing Oakley RIL dataset remains source-download-blocked. Canonical MLTR mathematical theorems, Paper A and original empirical gate criteria remain unchanged.
