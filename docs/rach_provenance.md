# Provenance: extraction from RACH legacy transport branch

## Source archive

The initial EXT theorem program was extracted from the frozen non-nested
replacement branch of:

```text
zuizui0223/rach-causal-invariants
commit b52ee777ac63a332e60a59d5e64721d98745be3f
```

That RACH commit follows the paper-core mathematical audit and is the source
reference for this migration.

## RACH assets migrated conceptually

| RACH registry ID | RACH source | EXT standalone module | Role retained |
|---|---|---|---|
| `EXT-1` | `causal_model/non_nested_portability.py` | `relation_transport.py` | relation-preserving common macro-law |
| `EXT-2` | `causal_model/non_nested_portability.py` | `relation_transport.py` | derived target exact projection |
| `EXT-3` | `causal_model/non_nested_conservative_transport.py` | `conservative.py` | target-only action conservative schema |
| `EXT-4` | `causal_model/non_nested_portability.py` | `obstruction.py` | newly legal word / carried-fiber split |

The RACH controlled-system, grammar, and exact-interface primitives were reduced
to `finite.py`, `exact.py`, and `macro.py`. Their role is only to make the
replacement theorems executable without importing RACH's open-composition or
identifiability branches.

## Deliberately excluded

EXT does **not** import or claim:

- the RACH extension--compression lower bound and relay sharpness witness;
- delayed exposure, adaptive finite-evidence no-go, or candidate-mechanism laws;
- reset-panel, coverage, cell-loss, common-mode failure, or experimental-design
  results;
- finite closure classification; or
- non-transport historical examples and benchmarks.

Those remain in RACH as archived provenance and can be cited only when a future
EXT theorem changes its assumptions or conclusion.

## Divergence policy

RACH is frozen as the source archive for its open-composition paper. EXT is the
canonical workspace for new replacement/rewiring mathematics. New theorems,
examples, and workflows about non-nested transport must be added here rather
than backported into RACH.

A later cross-reference should name both the RACH source commit and the EXT
commit/release containing the derived result.
