# Combined manuscript core — ecological macro-laws under structural change

## Working title

**When Ecological Macro-Laws Survive Structural Change: Exact Portability, Minimal Repair, and Historical Context**

## One-sentence claim

An inherited ecological macro-law remains exact precisely while structural change does not expose distinctions that the law merged; when it does, a unique coarsest source-relative exact refinement repairs the law, and path disagreement requires the minimum finite history context indexed by distinct carried terminal maps.

## Unified notation

A stage is a finite controlled ecological system

```text
S = (X, A, G, delta, y),
```

where `X` is the ecological state set, `A` the declared action set, `G` the finite action grammar, `delta` the controlled transition, and `y` the observable output. A macro-law is a surjection

```text
pi : X × G -> Q
```

that is exact when output, legal-action row, and successor macrostate are constant inside every macro fiber.

Structural change from source `S0` to target `S1` is represented by a declared total relation

```text
R subseteq (X0 × G0) × (X1 × G1).
```

Nested open composition is the special case in which source states embed into a target with additional legal actions or interaction channels. Non-nested ecological replacement is the general case in which source and target state sets differ and `R` carries source meaning to target configurations.

The source law induces a carried target partition `pi_R`. The question is whether `pi_R` is exact for the target operational model.

## Master theorem — portability, repair, and history

For a declared finite source exact law, target controlled system, and total label-consistent replacement relation:

1. **Portability.** The inherited macro-law transports unchanged if and only if output, legal-action rows, and target successor carried labels are constant inside every carried target fiber.
2. **Local obstruction.** Failure is witnessed by a finite pair of target states in one carried fiber that differ in output, legal actions, or successor carried fibers under a declared action.
3. **Minimal repair.** Iterative output/legal-row/successor refinement of the carried partition terminates at the unique coarsest exact target partition that refines the inherited partition.
4. **Defect.** The increase in macrostate count and memory bits is the minimum source-relative repair burden.
5. **History.** For a rooted replacement graph, one route-independent repair exists if and only if every root-to-terminal path carries the same terminal label map. Otherwise, one immutable history mode per distinct carried map is necessary and sufficient before relative exact refinement.

The theorem is source-relative: it preserves every inherited merge that remains operationally valid. It does not claim that the target lacks a smaller unrelated abstraction after source semantics are discarded.

## Results narrative

### Result 1 — structural change exposes hidden distinctions

The opening result should not begin with algorithms. Begin with the ecological fact that a macro-law is relative to a repertoire of possible future actions. Two configurations may be equivalent under the source repertoire but cease to be equivalent after a novel pollinator guild, disturbance response, management action, or interaction channel becomes available.

The local witness carries `(0,0,1)` from source to target. A target-only action gives different successors for the two target states carrying label `0`, so unchanged transport fails.

### Result 2 — failure has a unique minimal source-relative repair

The target-only distinction forces exactly one split:

```text
carried:  (0,0,1)
repaired: (0,1,2)
```

No exact target interface preserving the inherited labels can use fewer than three states. This is the headline theorem: the method does not merely detect transfer failure; it returns the unique least change required to restore exactness.

### Result 3 — repair burden can accumulate sharply

For `m` independently exposed binary target distinctions, the verified family gives

```text
source states = 2
repaired target states = 2^m + 1
defect states = 2^m - 1
defect bits = log2(2^m + 1) - 1.
```

This is not a universal ecological scaling law. It is a sharp finite family showing that a small inherited description can require rapidly increasing repair when the target action repertoire independently exposes previously merged coordinates.

### Result 4 — historical routes either agree or require memory

Two coherent loss–colonization routes carrying the same terminal map yield the same repaired law. When routes carry `(0,1)` and `(1,0)`, no route-free inherited label assignment exists. Two history modes are necessary and sufficient, and relative refinement on the augmented system gives four exact history-aware states.

## Discussion spine

1. Ecological macro-laws are operational objects, not timeless partitions.
2. Transferability is stronger than predictive fit on currently observed states: it requires closure under declared future actions.
3. Minimal repair distinguishes this framework from abandoning the old law and fitting a new unrelated abstraction.
4. Transport defect measures the price of preserving inherited ecological meaning.
5. History dependence is not invoked generically; finite history is retained only when declared routes carry incompatible meanings to the same terminal configuration.

## Main-text exclusions

Keep the following out of the headline Results:

- implementation details of partition refinement;
- every certificate field and validation helper;
- delayed-panel evidence results moved to CED;
- long history-augmentation construction details;
- claims about empirical inference of replacement relations or histories.

## Submission-ready abstract skeleton

Ecological models often compress many configurations into a small set of functional states, yet community turnover, novel interactions, and management interventions can make previously hidden distinctions operationally relevant. We develop an exact finite theory for deciding when an inherited ecological macro-law remains valid after structural change and for repairing it when it does not. A carried macro-law is portable exactly when target outputs, legal-action repertoires, and successor macro labels are uniform within every inherited fiber. Any failure has a finite local witness. Monotone refinement then yields the unique coarsest exact target law that preserves all inherited distinctions still compatible with the target, and the resulting increase in states or bits defines a transport defect. A sharp family shows that repair burden can grow as independently exposed distinctions accumulate. Across replacement histories, identical carried terminal maps produce one route-independent repair; incompatible maps require a minimum finite history context. A plant–pollinator turnover example illustrates how novel guilds and target-only manipulations can invalidate a functional classification and how the minimal repair identifies precisely which ecological distinctions must be restored.
