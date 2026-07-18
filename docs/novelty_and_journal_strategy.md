# Paper A novelty and journal strategy

## Fixed claim

**Exact Ecological Macro-Laws under Structural Change** is not presented as a new generic bisimulation, lumpability, or partition-refinement method. Its contribution is a source-relative transport problem:

> Given an already accepted exact ecological macro-law and a declared structural change between possibly non-nested systems, determine whether the inherited law remains exact; if not, return the unique coarsest exact target law constrained to preserve every inherited merge that remains valid.

The paper then quantifies the minimum repair burden and characterizes when several declared replacement histories admit one route-independent repair.

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

**Difference:** Paper A gives an explicit finite ecological decision structure for an inherited macro-law: unchanged portability, a local operational obstruction, unique least source-relative repair, repair defect, and minimum history completion. Open composition is only a special case of the more general source-target relation.

### 4. Transportability and domain adaptation

Causal transportability and statistical domain adaptation ask whether effects or predictors transfer between populations or environments.

**Overlap:** transfer across changed environments.

**Difference:** Paper A is not an estimation theorem and does not infer a transport relation. It studies exact operational closure of a declared macrostate interface under outputs, legal interventions, and successors, and returns a canonical structural repair when transfer fails.

### 5. Ecological coarse variables, resilience classes, and model transfer

Ecology routinely uses functional groups, occupancy states, resilience categories, regime states, and reduced ecosystem models. Existing ecological modeling literature discusses structural uncertainty, transfer failure, and prediction under interventions.

**Overlap:** ecological variables can fail after turnover or intervention.

**Difference:** the present paper supplies a finite necessary-and-sufficient portability criterion and a unique minimal repair, rather than only showing that models may fail or refitting an unrelated target model.

## Defensible novelty statement

Use this wording in the abstract, introduction, cover letter, and reviewer responses:

> Existing lumpability, bisimulation, and partition-refinement theories characterize exact aggregation within a specified system. We address a different constrained problem: an accepted macro-law is transported through a declared structural change, and any repair must preserve its inherited semantics. We characterize unchanged portability, prove that failure has a finite operational witness, and obtain the unique coarsest exact target refinement of the carried labels. This source-relative minimality supports a transport-defect measure and a sharp characterization of when multiple replacement histories require explicit context.

Avoid claims that partition refinement, bisimulation, quotient construction, or exact aggregation are new.

## The most vulnerable claims

1. **“Unique coarsest repair” may look like ordinary coarsest bisimulation.** The theorem statement and proof must make the constraint `refines the carried source labels` visible in every clause.
2. **“Transport defect” is a definition, not a standalone theorem.** Its value comes from being tied to the unique minimal repair and verified witness families.
3. **“History completion” can look like copying the system by path.** The main result must emphasize the necessary-and-sufficient minimum: histories share a mode exactly when their complete carried terminal maps agree.
4. **The ecological contribution is currently conceptual.** The plant-pollinator example must show a management conclusion that changes after a target-only intervention; otherwise editors may see computer-science formalism with ecological nouns.

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

- add a related-work section using the five boundaries above;
- state the carried-label constraint in the main repair theorem;
- add one table contrasting fixed-system aggregation, statistical transport, and source-relative repair;
- develop the plant-pollinator example into a complete decision workflow;
- ensure every headline claim can be read without CCOC/MLTR terminology;
- prepare a cover letter centered on the constrained transport problem, not on a new refinement algorithm.
