# Submission figure specification

## Figure 1 — portability failure and minimal repair

Four aligned panels:

1. source microstates grouped as `(low, low, high)`;
2. source-to-target relation carrying the same labels;
3. one target-only action separating the two carried-low configurations;
4. repaired target labels `(low-A, low-B, high)`.

The caption must state that only the affected inherited fiber is split and that the transport defect is one state.

## Figure 2 — accumulating transport defect

Use `artifacts/submission_transport_defect_curve.csv`.

Horizontal axis: independently exposed target distinctions `m`.

Vertical series:

- repaired target state count `2^m + 1`;
- transport-defect state count `2^m - 1`.

Place bit defect in an inset or secondary panel:

```text
log2(2^m + 1) - 1.
```

The caption must say that the action repertoire grows with `m`; the curve is a sharp finite witness, not an empirical scaling law.

## Figure 3 — history coherence boundary

Left: two replacement routes inducing the same carried terminal map and one shared repair.

Right: routes inducing `(0,1)` and `(1,0)`, followed by two immutable history modes and four history-aware exact states.

The visual claim is necessity and sufficiency of one mode per distinct carried map, not generic ecological path dependence.

## Figure 4 — ecological interpretation

Use the pollinator-turnover example:

```text
resident guild loss
replacement guild colonization
new floral manipulation
old low-service class split
```

Map every formal object to an ecological object in a side legend:

- microstate: plant–pollinator configuration;
- macro label: functional pollination regime;
- action: management manipulation or exclusion;
- replacement relation: declared source-to-target correspondence;
- repair: restored functional distinction;
- history mode: loss–colonization route class.

## Main-text table

One compact table should compare:

| Question | Certificate | Output |
|---|---|---|
| Does the inherited law transport? | within-fiber uniformity | yes/no |
| Why does it fail? | local state/action pair | obstruction |
| What is the least repair? | fixed-point refinement | coarsest exact partition |
| How costly is repair? | state/bit defect | source-relative burden |
| Is repair route independent? | equality of carried maps | one repair or history modes |

## Production rule

All numerical labels in Figures 1–3 must be read from the verified replay or generated CSV files. No hand-entered numerical values should remain in the final plotting code.
