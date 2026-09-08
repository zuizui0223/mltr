# MLTR — Macro-Law Transport and Repair

MLTR is a theorem-first finite mathematical-ecology repository for one source-relative model-reuse question:

> When structural replacement changes an ecological system, can an already accepted state classification be carried consistently and remain sufficient for the outputs and management actions that now matter—and, when different declared routes carry incompatible meanings, what is the minimum historical context required?

The project develops finite theorems for **non-nested** system changes. It does not assume that the source state space embeds into the target state space, and it does not infer the replacement relation from data.

## Headline result

1. **Carried semantics.** A declared many-to-many replacement relation carries one inherited source label map exactly when no target state receives incompatible source labels.
2. **Fixed-route composition.** For consecutive total relations `R` and `S`, direct carried semantics through `R;S` is defined iff sequential carriage through `R` and then `S` is defined; when defined, the two terminal maps are identical.
3. **Route coherence.** An accepted source macro-law has one route-independent carried meaning at a terminal system exactly when all declared root-to-terminal histories induce the same complete carried terminal label map.
4. **Minimum history completion.** When those maps disagree, histories can share an immutable mode exactly when their complete carried terminal maps agree. The necessary-and-sufficient mode count is therefore the number of equality classes of complete carried maps.

Thus stepwise representation of one fixed replacement route is not itself historical dependence. History is retained only when genuinely different declared routes change the inherited terminal meaning.

## Supporting decision-sufficiency and repair infrastructure

1. **Operational decision sufficiency.** Once a carried target labeling is defined, it remains exact only when current outputs, legal-action rows, and action-conditioned successor labels are constant inside every inherited fiber.
2. **Fiber-split obstruction.** A newly legal action or future word can expose two configurations that share an inherited state but imply different target outcomes or successor meanings.
3. **Established exact refinement.** Starting from the carried partition, standard finite partition-refinement machinery computes the unique coarsest exact target refinement compatible with those inherited labels. MLTR uses this result as infrastructure; it does not claim generic initial-partition coarsest refinement as new.
4. **Transport defect.** Extra target macrostates or description bits summarize source-relative repair burden. The defect is a diagnostic quantity tied to the repaired interface, not a standalone novelty claim.

The manuscript contribution is therefore the ecological model-reuse audit built around source-carried meaning, decision sufficiency, route composition, route coherence, and minimum historical context. Lumpability, bisimulation, coarsest-partition refinement, and fixed-point construction are credited as established substrate.

## Ecological reading

- **Source stage:** an ecological community before turnover, extinction, colonization, habitat reconfiguration, or interaction rewiring.
- **Target stage:** the altered community, potentially with a different raw state space and intervention repertoire.
- **Relation:** a declared correspondence between source and target finite configurations; it may be many-to-one, one-to-many, or many-to-many.
- **Carried-label conflict:** one target configuration is related to source configurations with different accepted ecological labels, so one inherited meaning is not defined there.
- **Decision sufficiency:** configurations sharing one inherited state agree on the target outputs, feasible interventions, and action-conditioned successor meanings relevant to the declared management problem.
- **Local obstruction:** a pair inside one inherited state that changes a target observation, action availability, or intervention response.
- **Monitoring repair:** the ecological distinction corresponding to that obstruction; standard exact refinement retains only the distinctions required by the declared operational model.
- **Path-label coherence:** different declared replacement histories give one carried terminal macro-law rather than history-dependent inherited labels.
- **History augmentation:** the minimum finite context retaining only path classes that carry genuinely different terminal maps.

MLTR does not infer a replacement relation, replacement history, action grammar, or ecological state variable from field data. These are assumptions of the finite mathematical model; empirical relation inference and approximate validation belong to later application layers.

## CREST role: historical / semantic insufficiency

The canonical synthesis lives in the dedicated [CREST repository](https://github.com/zuizui0223/crest), with the current hierarchy in the [trajectory-first program architecture](https://github.com/zuizui0223/crest/blob/main/docs/trajectory_first_program_architecture_2026-08-22.md).

CREST starts from temporally extended ecological worlds and asks whether a present snapshot is sufficient for a declared scientific state. Within that hierarchy, MLTR is the **historical / semantic obstruction theory**.

Two target configurations can share the same current descriptor while differing in the inherited meaning carried from a source system or replacement history. MLTR asks whether that inherited meaning is well defined, whether it composes consistently through replacement stages, whether the present state remains sufficient for target management, and whether alternative routes force historical context.

\[
\boxed{
\text{same present descriptor}
\not\Rightarrow
\text{same inherited operational state after replacement}.
}
\]

MLTR therefore owns the source-carriage, route-composition, route-coherence, and minimum-history questions. It uses established exact-refinement machinery after the inherited target semantics have been fixed.

Route other central objects as follows:

- independently optimized closed-vs-open future-interface lower bounds → **CCOC**;
- unresolved candidate-mechanism disagreement and candidate-safe state → **MRM**;
- finite/noisy evidence, monitoring feasibility, detection/failure architecture, calibration, or risk-limited reporting → **CED**.

A monitoring layer may consume MLTR obstruction pairs as an **application or cross-contract adapter**, but generic measurement selection, set cover, detection risk, or evidential certification is not an MLTR headline theorem. A genuinely new MLTR×CED result would have to prove a new coupling rather than merely apply standard monitoring machinery after a semantic audit.

Passing the MLTR audit does not imply that the repaired state is future-sufficient under every wider grammar, robust to retained mechanism uncertainty, or empirically resolved by available evidence.

## Start here

- [CREST trajectory-first architecture](https://github.com/zuizui0223/crest/blob/main/docs/trajectory_first_program_architecture_2026-08-22.md) — canonical program hierarchy and cross-repository routing.
- [CREST philosophical statement](https://github.com/zuizui0223/crest/blob/main/docs/contract_relative_ecological_state_theory.md) — world-level state definition and finite-theory boundary.
- [CCOC/MLTR claim firewall](docs/ccoc_mltr_claim_firewall_2026-08-16.md) — exact quantifier boundary between open-future lower bounds and source-relative repair.
- [Carried-label composition theorem](docs/carried_label_composition.md) — many-to-many inheritance conflicts and direct = sequential carried semantics.
- [Path-label coherence theorem](docs/path_coherence.md) — route-independent carried labels and target audit on replacement graphs.
- [Minimal history augmentation theorem](docs/history_augmentation.md) — minimum path context after route incoherence.
- [Novelty and journal strategy](docs/novelty_and_journal_strategy.md) — prior-art boundary and revised Paper A contribution hierarchy.
- [Submission audit](docs/submission_audit.md) — theorem-to-figure map and remaining pre-submission work.
- [Reproducibility](docs/reproducibility.md) — tests, deterministic JSON replay, and GitHub Actions artifacts.

## Run

```bash
python -m pip install -e '.[dev]'
pytest
python scripts/verify_transport_core.py --write-report
python scripts/verify_submission_story.py
```

The replay commands write deterministic reports under `artifacts/`.

## Provenance and status

This repository was initialized from the non-nested replacement branch (`EXT-1`–`EXT-4`) of the CCOC/RACH archive. `EXT` was the development name; **MLTR** is the publication-facing repository identity. The current Python package remains `ext_transport` for compatibility with the finite replay surface.

CCOC is both the historical provenance source for the migrated branch and the active independent CREST future-sufficiency layer. MLTR is the active workspace for the distinct source-relative replacement/rewiring theorem program.

## Scope

The current domain is declared finite deterministic controlled systems and finite prefix-closed action grammars. No empirical ecological data, field inference, parameter fitting, or claim that a finite certificate validates an observed ecosystem is included.
