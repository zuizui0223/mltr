# Paper A novelty and journal strategy

## Fixed claim

**Do Ecological Macro-Laws Survive Structural Replacement?** is not presented as a new generic bisimulation, lumpability, partition-refinement method, path-dependence principle, or open-composition lower-bound theorem. Its contribution is a source-relative route-coherence problem:

> Given an accepted exact ecological macro-law and several declared structural-replacement histories, determine whether they induce one terminal carried meaning; if not, characterize exactly which histories can share an immutable mode and then construct the unique coarsest exact history-aware interface.

The necessary-and-sufficient headline is that histories share a mode exactly when their complete carried terminal maps agree. Exact portability, local obstruction, fixed-point repair, and transport defect are supporting infrastructure that makes the route-level statement operational.

## Hard boundary against CCOC

MLTR fixes one inherited source partition. Its admissible target solution must refine the carried source labels:

\[
\min_{q_T\text{ exact},\;q_T\succeq \operatorname{carry}(q_S)} |q_T|.
\]

CCOC asks a different quantified question: each closed grammar may have its own independently optimized exact interface, and the theorem compares those minima with the minimum exact interface under a jointly open grammar. Its headline is a cross-grammar lower bound such as

\[
\max_i K_i^*=O(1),\qquad K_O^*=\Omega(m).
\]

A target in MLTR may expose new legal actions or future words, but that is only an application instance of source-relative transport. **MLTR does not claim CCOC's independently optimized closed-vs-open interface separation, and CCOC does not own MLTR's unique inherited-law repair, transport defect, or history completion.**

See `docs/ccoc_mltr_claim_firewall_2026-08-16.md`.

## Nearest prior literatures and the boundary

### 1. Lumpability and state aggregation

Classical lumpability asks whether a partition yields an exact reduced process within one fixed Markov or dynamical system. The relevant baseline includes Kemeny and Snell's finite-chain theory, subsequent exact and approximate lumpability, and state-aggregation work for controlled and probabilistic systems.

**Overlap:** exact aggregation, quotient states, preservation of transition behavior.

**Difference:** Paper A starts with an inherited source partition, carries it through a declared source-target relation, and seeks the coarsest exact *refinement of that inherited partition*. It does not optimize an unconstrained target-only aggregation.

### 2. Bisimulation and partition refinement

Bisimulation, quotient transition systems, and Paige-Tarjan-style refinement already provide coarsest behavior-preserving partitions. Modern work includes probabilistic and continuous-state bisimulation metrics, constrained bisimulations, and incremental abstraction.

**Overlap:** output/action/successor stability and fixed-point refinement.

**Difference:** algorithmic refinement is credited as standard machinery. The novelty claim is the transport test and constrained repair relative to source semantics under structural change, including non-nested replacement relations and changes in legal operational grammar.

### 3. Abstraction and model reduction under composition

Compositional verification, supervisory control, open systems, and modular abstraction study whether guarantees and reductions survive composition or extension.

**Overlap:** environmental interaction can invalidate an abstraction; context matters.

**Difference:** Paper A fixes an inherited macro-law and asks whether that law survives a declared target change and, if not, how to repair it with minimum source-relative refinement. It does **not** ask how the globally minimum exact interface changes when one optimizes separately under several closed grammars and then opens the grammar; that is the CCOC problem.

### 4. Transportability and domain adaptation

Causal transportability and statistical domain adaptation ask whether effects or predictors transfer between populations or environments.

**Overlap:** transfer across changed environments.

**Difference:** Paper A is not an estimation theorem and does not infer a transport relation. It studies exact operational closure of a declared inherited macrostate interface under outputs, legal interventions, and successors, and returns a canonical structural repair when transfer fails.

### 5. Ecological coarse variables, resilience classes, and model transfer

Ecology routinely uses functional groups, occupancy states, resilience categories, regime states, and reduced ecosystem models. Existing ecological modeling literature discusses structural uncertainty, transfer failure, and prediction under interventions.

**Overlap:** ecological variables can fail after turnover or intervention.

**Difference:** the present paper supplies a finite necessary-and-sufficient portability criterion and a unique coarsest exact repair constrained by carried labels, rather than only showing that models may fail or refitting an unrelated target model.

## Defensible contribution statement

Use this wording in the abstract, introduction, cover letter, and reviewer responses:

> Existing lumpability, bisimulation, and partition-refinement theories supply exactness and refinement machinery within specified systems. We use that machinery for a source-relative structural-replacement problem whose central output is historical: one route-independent carried law exists exactly when complete carried terminal maps agree, whereas disagreement requires one immutable mode per equality class of those maps. Route-specific portability tests and the unique coarsest exact repair of carried labels support this characterization.

This is a defensible positioning statement, not evidence of literature-firstness. Avoid claims that partition refinement, bisimulation, quotient construction, exact aggregation, generic path dependence, history augmentation in general, or the closed-vs-open interface lower bound are MLTR novelties.

## The most vulnerable claims

1. **“History completion” can look like copying the system by path.** The headline must state the necessary-and-sufficient quotient: histories share a mode exactly when their complete carried terminal maps agree, so raw path identity is not retained unless it changes the carried map.
2. **Generic path dependence is established territory.** The manuscript may claim its exact source-relative characterization, but it must not claim literature-firstness without a dedicated source-verified audit.
3. **“Unique coarsest exact repair” may look like ordinary coarsest bisimulation.** Treat fixed-point refinement as infrastructure and keep the constraint `refines the carried source labels` visible in every clause.
4. **“Transport defect” is a definition, not a standalone theorem.** Its value comes from being tied to the unique coarsest exact repair and verified witness families.
5. **The ecological contribution is currently conceptual.** The plant-pollinator example must show both a management conclusion that changes after a target-only intervention and the route-coherence decision; otherwise editors may see computer-science formalism with ecological nouns.
6. **CCOC overlap may blur the claim.** Every open-grammar example must be written as transport of one fixed inherited law; do not import CCOC's separately optimized closed/open minima into the MLTR theorem hierarchy.

## Required literature groups for the manuscript

- exact and weak lumpability; approximate aggregation;
- strong, weak, probabilistic, and constrained bisimulation;
- Paige-Tarjan and later partition-refinement algorithms;
- compositional and incremental abstraction;
- causal/statistical transportability and domain shift;
- ecological model structural uncertainty and intervention prediction.

Representative anchors include Kemeny & Snell; Paige & Tarjan; Milner; Larsen & Skou; Ferns, Panangaden & Precup; Feret et al. on lumpability abstractions; modern incremental bisimulation work; and ecological literature on structural uncertainty and unreliable intervention forecasts.

## Journal ranking

### First choice: Theoretical Ecology

**Fit:** strongest thematic match if the paper is framed around an ecological question and the worked example is developed enough to increase ecological understanding. The journal explicitly welcomes mathematical, computational, statistical, and conceptual theory but rejects mathematics that does not advance ecology.

**Submission condition:** make the ecological result primary; move most formal-computer-science terminology to Methods or Supplement; add a clear paragraph explaining what field ecologists or ecological modelers can decide using the theorem.

### Second choice: Ecological Modelling

**Fit:** very good and lower-risk. It explicitly publishes new mathematical models, systems analysis, ecological theory, reproducibility, and environmental-management applications.

**Submission condition:** emphasize the framework as a model-audit and model-transfer method, retain executable examples, and show how transport defect or repair affects a management variable.

### Ambitious alternative: Journal of the Royal Society Interface

**Fit:** plausible only after strengthening the bridge between formal systems theory and ecology and demonstrating broader biological significance.

**Risk:** the current single finite example may be judged too abstract or too narrow.

### Mathematical fallback: Bulletin of Mathematical Biology

**Fit:** appropriate if the theorem package becomes the primary product and the ecological interpretation remains substantial.

**Risk:** the result may be viewed as more formal-methods/state-reduction than mathematical biology unless linked to a genuine biological modeling class.

### Not first choice now: Methods in Ecology and Evolution

MEE accepts conceptual and analytical methods and values reproducible uptake, but the present manuscript lacks a broad empirical workflow, benchmarking suite, and user-facing validation across real ecological problems. It becomes realistic only after adding several realistic case studies or a reusable diagnostic tool with clear adoption potential.

## Final recommendation

Submit first to **Theoretical Ecology** after one ecological-strengthening revision. Use **Ecological Modelling** as the immediate transfer target. Do not lead with MEE or PLOS Computational Biology in the current form.

## Revision gate before submission

- keep the source-relative carried-label constraint visible in the main repair theorem;
- add one table contrasting fixed-system aggregation, CCOC's cross-grammar lower-bound problem, statistical transport, and MLTR's source-relative repair;
- remove language that treats CCOC's open-composition theorem as an MLTR result;
- develop the plant-pollinator example into a complete decision workflow;
- ensure every headline claim can be read without CCOC/MLTR terminology;
- prepare a cover letter centered on route coherence and necessary-and-sufficient history completion, with transport and refinement identified as supporting infrastructure.
