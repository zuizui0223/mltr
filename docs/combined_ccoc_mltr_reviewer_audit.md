# Superseded reviewer audit — former combined CCOC/RACH + MLTR paper

**Status: superseded on 2026-08-16.**

The previous audit recommended one combined flagship manuscript in which CCOC supplied an open-composition obstruction and MLTR supplied repair. That recommendation is no longer controlling because it hides a material difference in the theorem quantifiers.

## Current reviewer-facing distinction

### CCOC

For each closed grammar, choose its own minimum exact interface. Compare those closed minima with the minimum exact interface under the jointly open grammar. The headline is a quantitative separation:

\[
\max_i K_i^*=O(1),\qquad K_O^*=\Omega(m),
\]

with bounded-local sharpness witnesses.

No inherited source partition is fixed in the headline theorem.

### MLTR

Fix an already accepted source macro-law, carry its labels to a declared target, and test whether the inherited partition remains exact. If it fails, return the unique coarsest exact target refinement constrained to preserve inherited semantics. Transport defect and history completion are defined relative to that fixed inherited law.

## Reviewer test

A reviewer should be able to distinguish the papers by one question:

- **CCOC:** can every closed future be individually compressible while no comparably small exact interface exists for the open future?
- **MLTR:** given this particular inherited ecological law, can it be reused after structural change, and what is its least exact repair if not?

If either manuscript can be summarized using the other question without changing the quantifiers, the firewall has failed.

## Current MLTR result hierarchy

1. source-relative operational portability;
2. local failure witness plus unique coarsest source-relative repair;
3. transport defect induced by that repair;
4. route coherence and minimum history context.

CCOC's cross-grammar lower bound and relay sharpness family are adjacent results, not MLTR main-text results.

Use `docs/ccoc_mltr_claim_firewall_2026-08-16.md`, `docs/publication_completion_spine.md`, and `docs/novelty_and_journal_strategy.md` as the controlling documents.

The full former combined audit remains recoverable in Git history at commit `f7aa2b87398e4e034a9b4a444a6daac48e02169d`.