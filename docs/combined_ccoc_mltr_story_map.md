# Combined CCOC/RACH + MLTR manuscript story map

## Manuscript identity

**Exact Ecological Macro-Laws under Structural Change: Portability, Minimal Repair, and Historical Context**

## Core claim

Ecological macro-laws are portable across structural change exactly while newly
operational outputs, actions, and successors remain uniform inside their inherited
macro fibers. When this fails, the inherited law has a unique coarsest exact
source-relative repair; its additional states or bits define a transport defect,
and multiple replacement histories either share one repair or require a minimum
finite history context.

## Unified setup

Use one source operational model and one target operational model.

- The source carries an exact macro projection.
- A declared relation carries source semantics to target configurations.
- The target may have a larger, smaller, or non-nested raw state space.
- The target may expose new legal actions or future words.
- Portability asks whether inherited target fibers remain exact under the target
  operational grammar.

Nested open composition becomes one special case in which the target extends the
source's legal future grammar. Non-nested ecological replacement is the general
case in which the raw state space and state correspondence may also change.

## Four main results

### Result 1 — Exact portability under structural change

State one master criterion: the carried partition is exact iff current outputs,
legal-action rows, and target successors factor through it.

Use CCOC's grammar-aware exact interface and MLTR's relation transport as theorem
components, not as separate opening results.

### Result 2 — Local split and coarsest source-relative repair

A future word or target-only action that distinguishes two target states carrying
the same source macro label is a local obstruction. Iterated output/action/successor
refinement constructs the coarsest exact partition refining the carried labels.

This is the headline theorem.

### Result 3 — Transport defect

Define

```text
Delta_count = |Q_target_repaired| - |Q_source|
Delta_bits  = log2 |Q_target_repaired| - log2 |Q_source|.
```

Present one sharp finite family where newly exposed distinctions accumulate. State
all scope conditions in the caption.

### Result 4 — Historical coherence

On a replacement DAG, path-label coherence yields one route-independent carried
partition and one repair. When paths carry distinct terminal label maps, one
immutable history mode per distinct map is necessary and sufficient before relative
repair.

## Section plan

1. **Introduction**
   - ecological state variables are often reused after community change;
   - change can expose distinctions that the old variables suppressed;
   - existing language of transferability rarely gives a unique minimal repair.
2. **Operational models and inherited macro-laws**
   - finite states, outputs, actions, legal words, exact projections;
   - structural-change relation;
   - carried target labels.
3. **Portability criterion**
   - master theorem;
   - nested open-composition and non-nested replacement examples.
4. **Obstruction and minimal repair**
   - local split;
   - coarsest relative refinement;
   - uniqueness and source-relative minimality.
5. **Transport defect**
   - count and bit measures;
   - sharp family;
   - ecological interpretation.
6. **Replacement histories**
   - coherent paths;
   - minimum history augmentation.
7. **Worked ecological example**
   - plant–pollinator guild replacement;
   - inherited functional-state labels;
   - new management action splits one fiber;
   - repaired states and route dependence.
8. **Discussion**
   - exactness as benchmark;
   - relation to transferability, lumpability, bisimulation, resilience, and path
     dependence;
   - empirical requirements and approximate extensions.

## Abstract logic

1. Ecologists use coarse state variables to transfer understanding across change.
2. Structural change may alter the state space and future intervention repertoire.
3. We give an exact portability criterion for inherited macro-laws.
4. Failure has a local witness and a unique coarsest source-relative repair.
5. The repair burden is quantified by transport defect.
6. Historical coherence determines whether one repair applies across routes.
7. A finite ecological example illustrates turnover and rewiring.

## Result deletion and demotion

### Main text

- master portability criterion;
- local obstruction;
- coarsest repair;
- transport defect;
- path coherence;
- short history-completion proposition.

### Supplement

- relay construction details;
- complete CCOC theorem registry;
- all alternative witness families;
- implementation-level refinement lemmas;
- extended replacement graphs;
- deterministic replay details.

### Exclude from this manuscript

- finite evidence and detection theory;
- candidate mechanism uncertainty;
- empirical fitting claims;
- approximate/stochastic repair without a developed theorem.

## Work order

1. create unified notation translating CCOC and MLTR symbols;
2. write the master portability theorem and proof from existing ingredients;
3. choose one source–target ecological example;
4. generate the local-split/minimal-repair figure;
5. rewrite current MLTR Results around the four-result hierarchy;
6. import only the necessary CCOC proof statements by citation/provenance;
7. complete related-work review;
8. prepare release and archive artifacts.

## Submission gate

Do not submit until:

- the combined manuscript reads without requiring the reader to know repository
  history;
- open composition appears as a special case of structural change, not a separate
  first paper inside the manuscript;
- the minimal-repair theorem is visibly the main contribution;
- the worked ecological example uses every main definition;
- standard partition-refinement ingredients are credited explicitly.