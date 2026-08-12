# MLTR — Ecological State-Interface Transport and Repair

MLTR is a finite mathematical-ecology repository centered on one management question:

> When an ecological state classification was accepted for a source system, does it remain decision-sufficient after structural change, and what is the least additional distinction required when it does not?

The project treats turnover, extinction, recolonization, habitat reconfiguration, interaction rewiring, and changes in the available intervention repertoire as **non-nested** system changes. The source state space need not embed into the target state space.

## Publication-facing workflow

1. **Carry an inherited state interface.** A declared relation maps a source classification to the target system.
2. **Audit decision sufficiency.** States sharing an inherited target label must agree in current output, legal actions, and action-conditioned successor labels.
3. **Return a local obstruction.** When the audit fails, a finite state pair and action/future witness the missing distinction.
4. **Recover the least exact distinction.** Established coarsest-partition refinement is applied to the carried partition. MLTR does not claim this generic refinement construction as new.
5. **Translate repair into monitoring requirements.** Candidate measurements must separate pairs merged by the inherited interface but split by the exact repair.
6. **Separate consequences.** Structural repair complexity is kept distinct from distribution-sensitive information, measurement cost, and decision regret.
7. **Retain history only when necessary.** Alternative declared replacement routes share one interface when they carry the same terminal label map; incompatible carried maps require immutable route context.

## Novelty boundary

The repository explicitly does **not** claim invention of:

- partition refinement or coarsest stable refinement;
- MDP bisimulation or model minimization;
- the general idea of transferring state abstractions from source to target decision processes;
- targeted ecological monitoring; or
- value-of-information analysis.

Those are established literatures and are credited in `manuscript/references.bib` and `docs/paper_a_reference_audit.md`.

The contribution is instead the organization of those ingredients around an inherited ecological management interface: audit the old state variable after declared structural change, identify the exact distinction that the target action set exposes, translate the obstruction into a monitoring requirement, and determine when replacement history changes the operational meaning of the present state.

## Submission-facing results

The current Paper A replay verifies:

- exact pass/fail auditing of an inherited finite state interface;
- a local target-action obstruction and its least exact repair;
- a sharp family showing growth of **structural** repair complexity;
- conditional repair information for the finite local witness;
- an illustrative probabilistic plant–pollinator priority reversal and one-step decision regret;
- route coherence and minimum carried-map context.

The plant–pollinator probabilities and costs are illustrative sensitivity values, not empirical estimates.

## Reproducibility

```bash
python -m pip install -e '.[dev]'
pytest
python scripts/verify_transport_core.py --write-report
python scripts/verify_submission_story.py
python scripts/render_submission_figures.py
```

Generated JSON reports, SVG figures, and LaTeX build products are ignored on working branches and rebuilt in GitHub Actions. Submission/release commits should archive the generated artifacts separately.

## Start here

- [Paper A manuscript](manuscript/paper_a_main.tex) — current publication-facing draft.
- [Paper A reference audit](docs/paper_a_reference_audit.md) — adversarial novelty boundary and citation guardrails.
- [Submission audit](docs/submission_audit.md) — claim hierarchy and pre-submission work.
- [Paper architecture](docs/paper_architecture.md) — theorem hierarchy and figure plan.
- [Transport defect](docs/transport_defect.md) — finite structural repair witnesses.
- [Path coherence](docs/path_coherence.md) — route-independent carried labels and repair.
- [History augmentation](docs/history_augmentation.md) — minimum carried-map context after route incoherence.
- [Reproducibility](docs/reproducibility.md) — deterministic replay and Actions artifacts.

## Scope

The current formal domain is declared finite deterministic controlled systems, finite prefix-closed action grammars, finite replacement relations, and finite replacement DAGs. MLTR does not infer replacement relations, histories, actions, ecological probabilities, or field mechanisms from observations. Exactness is used as a structural benchmark; stochastic, approximate, and empirically estimated variants remain extensions.
