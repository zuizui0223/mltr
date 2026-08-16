# Paper A architecture — ecological decision-sufficiency audit and monitoring repair

## One-sentence paper

An ecological state classification can remain interpretable after structural change while becoming insufficient for a new management action; Paper A audits that failure and converts the resulting obstruction into an exact monitoring-feasibility, impossibility, and minimum-cost measurement problem.

## Primary story arc

1. **Ecological practice starts from coarse states.** Managers use state-and-transition models, habitat classes, functional states, and other compressed interfaces because full ecological detail is not operationally manageable.
2. **Structural change can invalidate the interface.** Turnover, rewiring, habitat change, or a new intervention can expose differences that the inherited class suppresses.
3. **Audit before refitting or collecting more data.** Check outputs, legal actions, and action-conditioned successors within each inherited target class.
4. **Diagnose locally.** A pair of states and an action/future witness why the old state is no longer decision-sufficient.
5. **Recover the least exact distinction.** Use established coarsest refinement to define the state distinction that the changed management problem requires.
6. **Ask whether monitoring can actually recover it.** A measurement library is sufficient iff it separates every obstruction pair. An uncovered pair is an impossibility certificate.
7. **If recovery is possible, minimize monitoring cost.** Candidate measurements induce a weighted set-cover problem over obstruction pairs.
8. **Show why it matters for management.** The plant--pollinator example demonstrates a restoration-priority reversal after the hidden distinction is restored.
9. **Treat other consequences as secondary.** Structural defect, conditional information, decision regret, and route context support the main audit-to-monitoring story but do not compete with it for the headline.

## Main-text result hierarchy

### Result 1 — decision-sufficiency audit

Necessary and sufficient target-fiber conditions for unchanged reuse of the inherited state classification.

### Result 2 — local obstruction

A finite state pair and action/future identify the ecological distinction hidden by the inherited class.

### Result 3 — exact monitoring realization — applied centerpiece

For candidate measurements `z_j`, a selected set `S` recovers the repaired state exactly iff a decoder

`Q*(x) = d_S(C(x), z_S(x))`

exists, equivalently iff every pair merged by `C` but separated by `Q*` is separated by at least one selected measurement.

Consequences:

- **feasibility:** the full candidate library covers every obstruction pair;
- **impossibility:** any uncovered obstruction pair certifies that the supplied library cannot exactly recover the decision-sufficient state;
- **minimum cost:** when feasible, least-cost exact monitoring is weighted set cover over obstruction pairs.

This is the main bridge to ecological monitoring. It does not claim a new generic set-cover algorithm.

### Result 4 — least exact distinction — supporting formal machinery

Established Paige--Tarjan / Givan--Dean--Greig refinement machinery is instantiated at the carried classification. The construction is prior art. The supplement supplies a self-contained finite specialization proof so the paper has no hidden proof dependency.

### Result 5 — management consequence

The illustrative plant--pollinator layer shows that a single hidden state distinction can reverse restoration priority. This is a theoretical sensitivity example, not empirical evidence.

### Result 6 — secondary diagnostics

- structural state-count defect measures loss of compression only;
- conditional repair information weights the extra labels by a target-state distribution;
- decision regret is utility-dependent and is not ordered by state-count defect;
- for every `d >= 1` and `r >= 0`, a finite exact-repair problem can have defect `d` and regret `r`.

### Result 7 — route coherence / minimum context

Equality of complete terminal carried maps is the criterion for a route-independent inherited interface; otherwise one immutable context per distinct carried terminal map is necessary before exact refinement. This is a secondary closure result, not the paper's novelty anchor.

## Main ecological worked example

Plant--pollinator turnover:

- inherited class merges Sites A and B;
- a target competitor-removal action exposes different substitute-pollinator responses;
- the local witness identifies substitute-response capacity as the missing ecological distinction;
- least exact repair splits A and B;
- a monitoring library must contain variables that separate the A--B obstruction;
- illustrative probabilities/costs show that the repaired classification can reverse restoration priority;
- the probability/cost values are sensitivity values, not empirical data.

## Figure and table plan

1. Figure 1: audit-to-monitoring workflow;
2. Table: three audit outcomes — inherited state passes; repair measurable; repair not measurable with current library;
3. Figure 4: decision-reversal region for the illustrative pollinator management layer;
4. Figure 2: structural repair-complexity witness family, explicitly secondary;
5. Figure 3: route coherence and carried-map context, explicitly secondary.

## What stays out of the headline

- generic partition-refinement novelty;
- generic source-to-target abstraction-transfer novelty;
- a claim that transport defect is an ecological effect size;
- a claim that targeted monitoring or value of information is new;
- a claim that history-sensitive equivalence is new;
- stochastic or approximate transport theorems not proved in the repository.

## Recommended manuscript order

1. Introduction: inherited ecological states can become insufficient after structural or intervention change; the missing gap is between state failure and monitoring redesign.
2. Relation to existing theory and practice: exact aggregation, abstraction transfer, ecological transferability, targeted monitoring, VoI, history-sensitive formalisms.
3. Operational framework.
4. Results I: decision-sufficiency audit and local obstruction.
5. Results II: exact monitoring realization, candidate-library feasibility/impossibility, minimum cost.
6. Results III: plant--pollinator restoration-priority consequence.
7. Results IV: structural/information/regret diagnostics.
8. Results V: route context.
9. Discussion: audit is upstream of Jones-style indicator selection and Canessa-style VoI.
10. Scope / methods / supplement references.

## Discussion message

The key ecological message is not that managers should use a new aggregation algorithm. It is that **state validity is action-dependent, and a failure of state validity creates a precise monitoring requirement**. A classification built for one structural and management regime can become insufficient under another. When it does, the framework identifies the specific hidden distinctions that change target action consequences, tests whether the available measurement library can recover those distinctions, and, if it can, returns the least-cost exact measurement problem. This is stronger and more actionable than either retaining the old state blindly or responding with undirected additional monitoring.

## Publication-risk statement

The remaining publication risk is ecological significance and generality, not proof closure. The paper should be judged on whether the sequence

`inherited state -> structural audit -> obstruction -> monitoring feasibility/cost -> decision consequence`

is recognized as a useful theoretical problem for ecological management. Mathematical priority for generic refinement, transfer, set cover, entropy, or history is not required for the paper's claim and should not be implied.

## Stop rule

This paper is in manuscript-completion mode. Do not expand the theorem inventory by default. New mathematics belongs in the paper only if it closes a visible logical gap, is required for the ecological interpretation, survives direct prior-art comparison, or changes the management conclusion.
