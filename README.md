# EXT — Exact macro-law transport through ecological replacement

EXT studies one question in finite deterministic mathematical ecology:

> When species turnover, extinction, recolonization, or interaction rewiring replaces one ecological system by another rather than merely adding modules, when can one exact macro-law be transported across the replacement?

The project develops finite theorems for **non-nested** system changes. It does not assume that the source state space embeds into the target state space.

## Central program

1. Start from an exact source macro-projection.
2. Give a declared relation between source and target product states.
3. Derive target macro labels from the relation whenever each target fiber carries one source macro label.
4. Check output preservation, old-action preservation, and successor closure.
5. Decide whether the target realizes the same macro-law, a conservative extension of it, or a concrete fiber-split obstruction.

## Current status

This repository was initialized from the non-nested replacement branch (`EXT-1`–`EXT-4`) of `zuizui0223/rach-causal-invariants`, pinned after its RACH paper-core audit merge commit `b52ee777ac63a332e60a59d5e64721d98745be3f`.

RACH remains the frozen provenance archive. EXT is the active workspace for the separate replacement/rewiring theorem program.

## Scope

The current domain is declared finite deterministic controlled systems and finite prefix-closed action grammars. No empirical ecological data, field inference, parameter fitting, or claim that a finite certificate validates an observed ecosystem is included.
