# MLTR — Ecological State-Interface Audit and Monitoring Repair

MLTR is a finite mathematical-ecology repository centered on one management question:

> When an ecological state classification was accepted for a source system, does it remain decision-sufficient after structural change, and, if not, can the available monitoring variables recover the distinction required by the changed management problem?

The project treats turnover, extinction, recolonization, habitat reconfiguration, interaction rewiring, and changes in the available intervention repertoire as **non-nested** system changes. The source state space need not embed into the target state space.

## Publication-facing workflow

1. **Carry an inherited state interface.** A declared relation maps a source classification to the target system.
2. **Audit decision sufficiency.** States sharing an inherited target label must agree in current output, legal actions, and action-conditioned successor labels.
3. **Return a local obstruction.** When the audit fails, a finite state pair and action/future witness the missing distinction.
4. **Recover the least exact distinction.** Established coarsest-partition refinement is applied to the carried partition. MLTR does not claim this generic refinement construction as new.
5. **Test exact monitoring realization.** Candidate measurements recover the repaired state iff they separate every obstruction pair. An uncovered pair certifies that the current measurement library is structurally insufficient.
6. **Minimize acquisition cost when recovery is feasible.** With additive measurement costs, least-cost exact monitoring is a weighted set-cover problem over the audit-generated obstruction pairs.
7. **Separate secondary consequences.** Structural repair complexity is kept distinct from conditional information, measurement cost, and decision regret.
8. **Retain history only when necessary.** Alternative declared replacement routes share one interface when they carry the same terminal label map; incompatible carried maps require immutable route context.

## Novelty boundary

The repository explicitly does **not** claim invention of:

- partition refinement or coarsest stable refinement;
- MDP bisimulation or model minimization;
- the general idea of transferring state abstractions from source to target decision processes;
- generic state/sensor selection or weighted set cover;
- targeted ecological monitoring; or
- value-of-information analysis.

Those are established literatures and are credited in `manuscript/references.bib` and `docs/paper_a_reference_audit.md`.

The contribution is instead the ecological organization of these ingredients around an inherited management interface: audit the old state variable after declared structural change, generate the exact distinctions that the target intervention exposes, determine whether a supplied measurement library can recover them, return an impossibility certificate when it cannot, and connect successful repair to management consequences.

## Submission-facing results

The current Paper A replay (schema 3) verifies:

- exact pass/fail auditing of an inherited finite state interface;
- a local target-action obstruction and its least exact repair;
- the local obstruction pair `(0,1)` for inherited labels `(0,0,1)` and repaired labels `(0,1,2)`;
- an illustrative candidate monitoring library in which `substitute_response_capacity` separates the obstruction while abundance and soil-condition proxies do not;
- exact feasibility of the full illustrative library and minimum exact acquisition cost `1.0`;
- an explicitly insufficient two-proxy sublibrary with uncovered obstruction pair `(0,1)`;
- a sharp family showing growth of **structural** repair complexity;
- conditional repair information for the finite local witness;
- an illustrative probabilistic plant–pollinator priority reversal and one-step decision regret;
- route coherence and minimum carried-map context.

The monitoring values/costs and plant–pollinator probabilities/costs are illustrative finite replay values, not empirical estimates.

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
- [Paper architecture](docs/paper_architecture.md) — monitoring-centered result hierarchy and figure plan.
- [Supervisor brief](docs/paper_a_supervisor_brief_ja.md) — Japanese handoff of the current scientific story.
- [Transport defect](docs/transport_defect.md) — finite structural repair witnesses.
- [Path coherence](docs/path_coherence.md) — route-independent carried labels and repair.
- [History augmentation](docs/history_augmentation.md) — minimum carried-map context after route incoherence.
- [Reproducibility](docs/reproducibility.md) — deterministic replay and Actions artifacts.

## Scope

The current formal domain is declared finite deterministic controlled systems, finite prefix-closed action grammars, finite replacement relations, finite candidate measurement libraries, and finite replacement DAGs. MLTR does not infer replacement relations, histories, actions, ecological probabilities, field mechanisms, or measurement-error models from observations. Exactness is used as a structural benchmark; stochastic, approximate, imperfect-detection, and empirically estimated variants remain extensions.
