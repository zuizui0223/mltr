# MLTR — Macro-Law Transport and Repair

MLTR is a theorem-first finite mathematical-ecology repository for one question:

> When species turnover, extinction, recolonization, or interaction rewiring replaces one ecological system by another rather than merely adding modules, when can an exact macro-law be transported across the replacement—and, when it cannot, what is the minimal exact repair?

The project develops finite theorems for **non-nested** system changes. It does not assume that the source state space embeds into the target state space.

## Central results

1. **Replacement transport.** A total relation between two exact projected stages preserves one common macro-law when it preserves macro labels, current output, legal-action rows, and successors.
2. **Derived target projection.** A source projection plus a total, target-fiber-label-consistent relation constructs the target projection; target labels need not be supplied in advance.
3. **Conservative target-only actions.** A target may add an action only when its availability and macro successor are uniform inside each derived target macro fiber.
4. **Fiber-split obstruction.** A word newly legal after replacement refutes one proposed carried merge if it yields different target traces from two states in that fiber.
5. **Relative exact refinement and transport defect.** Starting from the carried target partition, finite output/legal-row/successor refinement constructs the coarsest exact target interface that preserves every carried merge possible. The extra target macrostates and bits quantify the minimum repair cost for that carried macro-law.
6. **Path-label coherence.** In a declared rooted replacement DAG, if every root-to-terminal history carries the same root macro labels to each terminal state, then the carried partition, its coarsest exact repair, and its transport defect are independent of replacement route.
7. **Minimal history augmentation.** If declared histories carry different terminal label tuples, exactly one immutable history mode per distinct tuple is necessary and sufficient to preserve them all. Relative exact refinement on the history-sliced terminal system then gives the coarsest exact history-aware macro-law.

## Ecological reading

- **Source stage:** an ecological community before turnover, extinction, colonization, habitat reconfiguration, or interaction rewiring.
- **Target stage:** the altered community, potentially with a different raw state space.
- **Relation:** a declared correspondence between source and target finite configurations; it may be many-to-one or one-to-many.
- **Macro-law:** a coarse ecological state description preserving all outputs and actions declared by the finite model contract.
- **Transport defect:** the number of additional coarse ecological states required after replacement because newly possible interactions distinguish configurations that the old macro-law merged.
- **Path-label coherence:** a condition ensuring that different declared replacement histories give one carried terminal macro-law rather than history-dependent labels.
- **History augmentation:** the minimum finite context retaining only the path classes that carry genuinely different terminal macro labels.

MLTR does not infer a replacement relation, replacement history, or action grammar from field data. These are assumptions of a finite mathematical model.

## Start here

- [Submission audit](docs/submission_audit.md) — claim hierarchy, theorem-to-figure map, and remaining pre-submission work.
- [Paper architecture](docs/paper_architecture.md) — recommended central claim, theorem hierarchy, Results order, and figure plan.
- [Working Results and Discussion](docs/paper_results_discussion.md) — manuscript-facing English draft for the theorem results and interpretation.
- [Theorem program](docs/theorem_program.md) — definitions, theorem statements, non-claims, and paper direction.
- [Transport defect theorem](docs/transport_defect.md) — the coarsest relative exact refinement and the accumulating binary family.
- [Path-label coherence theorem](docs/path_coherence.md) — route-independent carried labels and repair on replacement graphs.
- [Minimal history augmentation theorem](docs/history_augmentation.md) — minimum path context and exact history-aware repair after route incoherence.
- [CCOC provenance](docs/rach_provenance.md) — exact source assets copied from the legacy branch and what was deliberately excluded.
- [Reproducibility](docs/reproducibility.md) — tests, deterministic JSON replay, and GitHub Actions artifact.

## Run

```bash
python -m pip install -e '.[dev]'
pytest
python scripts/verify_transport_core.py --write-report
```

The last command writes `artifacts/transport_core_report.json`.

## Provenance and status

This repository was initialized from the non-nested replacement branch (`EXT-1`–`EXT-4`) of the CCOC/RACH archive. `EXT` was the development name; **MLTR** is the publication-facing repository identity. The current Python package remains `ext_transport` for compatibility with the finite replay surface.

CCOC remains the frozen provenance archive. MLTR is the active workspace for the separate replacement/rewiring theorem program.

## Scope

The current domain is declared finite deterministic controlled systems and finite prefix-closed action grammars. No empirical ecological data, field inference, parameter fitting, or claim that a finite certificate validates an observed ecosystem is included.
