# Paper A novelty and journal strategy

## Revised fixed claim

**Do Ecological Macro-Laws Survive Structural Replacement?** is not presented as a new generic bisimulation, lumpability, partition-refinement method, constrained-coarsest-partition theorem, path-dependence principle, or open-composition lower-bound theorem.

The paper's safest contribution is an **ecological model-reuse audit**:

> Given an already accepted ecological state classification, a declared structural change, and the outputs and management actions that matter after that change, determine whether the inherited classification is still decision-sufficient; if it is not, identify the missing distinctions, determine whether the inherited meaning composes consistently across replacement stages, and retain historical context only when genuinely different declared routes assign incompatible terminal meanings.

The mathematical contribution is therefore layered rather than located in generic refinement:

1. **Carried-semantics contract.** A many-to-many source--target relation carries one inherited label map exactly when every target state receives one source-label value; label conflict is an explicit finite witness.
2. **Compositional carried semantics.** For total declared relations `R` and `S`, direct transport through `R;S` is defined iff sequential transport through `R` and then `S` is defined, and when defined
   \[
   (\pi_0)_{R;S}=(\pi_R)_S.
   \]
   Thus decomposition of one fixed route does not itself create semantic path dependence.
3. **Route coherence and minimum history completion.** Different declared routes support one route-independent inherited terminal law exactly when their complete carried terminal maps agree. When they disagree, histories share a mode exactly by equality of those complete maps.
4. **Decision-sufficiency audit.** On each carried target slice, outputs, legal actions, and action-conditioned successors determine whether the inherited state variable is sufficient for the target management problem.
5. **Standard exact repair.** Once a carried partition is fixed, coarsest exact refinement is established partition-refinement / abstraction machinery. MLTR uses it; it does not claim it as a new generic theorem.
6. **Transport defect.** The increase in repaired state count or description length is a diagnostic quantity tied to the source-relative repair, not a standalone mathematical novelty claim.

## Why the revision is necessary

The previous wording still risked placing novelty on

> “the unique coarsest exact target refinement constrained by carried source labels.”

That is too strong. The nearest prior theory already includes this mathematical pattern.

- The relational coarsest-partition problem starts from an initial partition and asks for the coarsest compatible refinement; Fernandez (1990) explicitly relates bisimulation minimization to this problem.
- Abstract-interpretation work on strong preservation proves existence of minimal strongly preserving refinements and fixed-point characterizations; Ranzato and Tapparo (2007) subsume several behavioral equivalences and refinement algorithms in this framework.
- Biological-network reduction also uses arbitrary user-specified initial partitions and computes their unique coarsest admissible refinement. Argyris et al. (2023), for example, use this to preserve model-specific variables in Boolean-network reduction.

Therefore Paper A must never imply that “start from an inherited partition and compute its unique coarsest exact refinement” is itself the new theorem.

## Hard boundary against CCOC

MLTR fixes one inherited source partition. Its admissible target solution must remain a refinement of the carried source labels:

\[
\min_{q_T\text{ exact},\;q_T\succeq \operatorname{carry}(q_S)} |q_T|.
\]

CCOC asks a different quantified question: each closed grammar may have its own independently optimized exact interface, and the theorem compares those minima with the minimum exact interface under a jointly open grammar.

A target in MLTR may expose new legal actions or future words, but that is only an application instance of source-relative model reuse. **MLTR does not claim CCOC's independently optimized closed-vs-open interface separation.** Conversely, CCOC does not ask whether one accepted source classification retains its inherited operational meaning under declared replacement routes.

See `docs/ccoc_mltr_claim_firewall_2026-08-16.md`.

## Nearest prior literatures and the corrected boundary

### 1. Relational coarsest partition, bisimulation, and abstract interpretation

The initial-partition / coarsest-refinement problem is established. This includes Paige--Tarjan-style partition refinement, Fernandez's relational coarsest-partition framing, and abstract-interpretation formulations of minimal strongly preserving refinements.

**Overlap:** initial partitions, finite witnesses, iterative splitting, fixed-point termination, unique coarsest stable refinement.

**Correct MLTR boundary:** these are infrastructure after a carried target labeling has been fixed. The source-relative work that precedes refinement is to define inherited meaning through non-nested replacement relations, expose semantic conflicts in many-to-many carriage, prove direct/sequential carriage consistency, and compare genuinely different replacement routes.

### 2. Model-specific biological reduction

Boolean-network reduction already allows an arbitrary initial partition so users can prevent specified variables from being merged, and then computes the unique coarsest refinement satisfying the reduction criterion.

**Overlap:** user-prescribed distinctions, exact dynamics, coarsest refinement preserving those distinctions.

**Correct MLTR boundary:** “source semantics must be preserved” cannot be sold merely as “we use an initial partition.” The added problem is that the initial target labeling itself is inherited through a declared source--target relation and may fail to be well-defined, may compose across multiple replacements, or may disagree across alternative histories.

### 3. Lumpability and state aggregation

Classical lumpability asks whether a partition yields an exact reduced process within one fixed stochastic or dynamical system.

**Overlap:** exact aggregation and transition preservation.

**Correct MLTR boundary:** the ecological object being audited is an already accepted state classification that is being reused after structural change. The target state representation is judged relative to the outputs and interventions required by the new management problem.

### 4. State-and-transition models, resilience, and adaptive management

Ecological state-and-transition models organize ecosystem states, transitions, management actions, and monitoring information. Their value lies in linking ecological understanding to management decisions, but practical use is limited by insufficient context, heterogeneity, uncertainty, and weak connections between monitored variables and the decisions they are meant to support.

**Overlap:** state classifications, structural change, intervention response, monitoring redesign, historical context.

**MLTR ecological contribution:** turn “is this state variable still adequate?” into a formal decision-sufficiency audit. Two configurations should remain in one inherited management state only when they agree on the target outputs, feasible interventions, and action-conditioned successor meanings relevant to the declared decision problem.

### 5. Transportability and domain adaptation

Causal transportability and statistical domain adaptation address whether effects or predictors transfer across populations or environments.

**Overlap:** model reuse after environmental change.

**Correct MLTR boundary:** MLTR assumes the source and target systems and replacement relations have been declared. It asks a prior structural question: whether the inherited state interface can possibly factor the target management behavior. It neither estimates the relation nor guarantees empirical external validity.

### 6. Generic path dependence and historical contingency

Historical contingency, path dependence, legacy effects, and alternative recovery trajectories are established ideas in ecology and other fields.

**Overlap:** current state meaning may depend on past events.

**Correct MLTR boundary:** do not claim generic path dependence as new. The exact result is narrower: for declared replacement paths and a fixed inherited source law, retain history only to the extent that complete carried terminal maps differ. Stepwise decomposition of a *single* route is not history dependence because compositional carriage guarantees direct = sequential transport on that route.

## Defensible contribution statement

Use this wording in the abstract, introduction, cover letter, and reviewer responses:

> Existing coarsest-partition, bisimulation, and abstract-refinement theories already provide machinery for computing stable refinements from an initial classification. We use that machinery after a different source-relative problem has been solved: carrying an accepted ecological state meaning through declared structural replacement. In MLTR, many-to-many carriage is valid only when inherited labels are unambiguous, direct and sequential carriage agree along every fixed route, and genuinely different routes can share a history-free terminal law exactly when their complete carried terminal maps agree. The ecological role of the subsequent refinement is to identify the additional distinctions required for the inherited state variable to remain sufficient for target management decisions.

This statement is deliberately a positioning claim, not evidence of historical firstness.

## The revised contribution hierarchy for Paper A

### Headline ecological contribution

**Audit of decision sufficiency for inherited ecological state variables after structural change.**

The paper should lead with the fact that ecological state classifications are interfaces to management decisions, not permanent natural kinds. A classification may be sufficient under one action repertoire and become insufficient after invasion, species loss, rewiring, climate change, restoration, or the introduction of a new intervention.

### Headline formal contribution

**Source-carried semantics across replacement paths.**

The strongest formal sequence is now:

\[
\text{carriage consistency}
\rightarrow
\text{composition}
\rightarrow
\text{route coherence}
\rightarrow
\text{minimum history completion}.
\]

This is preferable to leading with the refinement theorem.

### Supporting infrastructure

- exact target decision-sufficiency criterion;
- local output/action/successor obstruction;
- standard source-relative partition refinement;
- transport defect as a diagnostic burden;
- finite executable witnesses.

## The most vulnerable claims after revision

1. **“Unique coarsest exact repair” is established machinery.** Cite the relevant partition-refinement / abstract-interpretation prior art and explicitly demote this result to infrastructure.
2. **“Preserving source semantics” is not enough by itself.** User-chosen initial partitions are already used in model reduction. The manuscript must explain that the target inherited partition is itself produced through a source--target relation and can be inconsistent or route dependent.
3. **“History completion” can look like copying the system by path.** State the quotient: raw path identity is discarded; only equality classes of complete carried terminal maps are retained.
4. **Generic path dependence is not new.** The manuscript may claim an exact source-relative criterion, not generic firstness.
5. **Transport defect is a diagnostic definition.** Do not present block-count increase alone as a new fundamental mathematical quantity.
6. **The ecological contribution must be visible without formal-methods vocabulary.** The plant--pollinator example must show a real decision reversal or monitoring consequence, not just a partition split.
7. **The relation is declared, not inferred.** This limitation must remain explicit; empirical relation inference belongs to a later application layer.

## Required changes to the manuscript background

The introduction should follow this logic:

1. Ecological management relies on compressed state descriptions.
2. State-and-transition and adaptive-management frameworks connect states to expected intervention responses.
3. Structural change or a changed intervention repertoire can invalidate the information content of an inherited state variable.
4. Lumpability, bisimulation, relational coarsest partition, and abstract interpretation already provide exact aggregation and coarsest-refinement machinery.
5. Therefore Paper A does not claim a new generic refinement algorithm or new existence/uniqueness result.
6. The source-relative problem begins one layer earlier: how an accepted classification is carried across a non-nested source--target relation, whether that carriage is label-consistent, whether it composes, and whether different histories induce one terminal meaning.
7. When the inherited meaning is fixed, standard refinement is interpreted ecologically as the additional information required for target decision sufficiency.
8. Historical context is retained only when it changes the carried operational meaning of the present state.

## Required literature anchors

### Formal refinement / aggregation

- Kemeny & Snell — finite-chain lumpability;
- Paige & Tarjan — partition refinement;
- Fernandez (1990) — relational coarsest partition and bisimulation minimization;
- Milner; Larsen & Skou — behavioral equivalence / probabilistic bisimulation;
- Ranzato & Tapparo (2007) — generalized strong preservation and minimal refinement by abstract interpretation;
- Feret et al. — lumpability abstractions;
- Argyris et al. (2023) — biological-network reduction from user-specified initial partitions.

### Ecology / management

- Holling; Walters — adaptive management;
- state-and-transition model literature linking discrete ecological states, management actions, and monitoring;
- resilience / regime-shift literature;
- monitoring and restoration literature in which indicator choice is explicitly tied to intervention outcomes and decision objectives.

## Journal ranking

### First choice: Theoretical Ecology

**Fit:** strongest if the paper is framed as an ecological theory of state-variable reuse and decision sufficiency, not as a new partition algorithm.

**Submission condition:** foreground ecological state meaning, management actions, monitoring repair, and history; explicitly acknowledge formal prior art.

### Second choice: Ecological Modelling

**Fit:** very good and lower-risk. The model-audit / model-transfer framing and executable finite workflow fit naturally.

### Ambitious alternative: Journal of the Royal Society Interface

Only realistic if the ecological/biological application becomes broader than one finite illustration.

### Mathematical fallback: Bulletin of Mathematical Biology

Appropriate if the formal relation/route theorem package becomes the main product while the ecological interpretation remains substantive.

### Not first choice now: Methods in Ecology and Evolution

The manuscript still lacks the multi-system empirical benchmarking and uptake-oriented software workflow expected for a strong methods paper.

## Revision gate before submission

- [x] prove and implement direct = sequential carried semantics under total replacement relations;
- [x] expose many-to-many inherited-label conflict witnesses;
- [x] add formal prior-art references for initial-partition coarsest refinement;
- [ ] rewrite the main Introduction so constrained refinement is explicitly established machinery;
- [ ] add the carried-semantics composition proposition to the main text;
- [ ] make state-and-transition / management-decision motivation visible in the first two paragraphs;
- [ ] revise the contribution table so “coarsest repair” is not the main difference from bisimulation;
- [ ] develop the plant--pollinator example into a complete decision workflow;
- [ ] keep CCOC's independently optimized cross-grammar bound outside the MLTR theorem hierarchy;
- [ ] run the manuscript/reproducibility suite and freeze a submission SHA only after the revised novelty wording passes audit.

## Final recommendation

Continue targeting **Theoretical Ecology**, but only with the revised novelty placement above. The paper is strongest when read as:

> **a formal audit of whether an inherited ecological state still carries enough information for management after structural change, with exact rules for source-label carriage, route composition, route coherence, and the minimum historical context required when inherited meanings diverge.**

That is substantially safer than presenting Paper A as a new coarsest-refinement theorem.
