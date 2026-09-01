# MLTR paper architecture: route-coherent macro-laws under ecological replacement

## Recommended working title

**Do Ecological Macro-Laws Survive Structural Replacement? Route Coherence and Minimal Historical Completion**

A shorter alternative is **Portable Macro-Laws after Ecological Replacement**.

The question title is preferable because it leads with the ecological conclusion
and names the two distinctive outputs rather than the standard refinement
machinery used to obtain them.

## One-sentence thesis

> An accepted ecological macro-law need not survive structural replacement as one route-free law: declared histories share a terminal meaning exactly when their complete carried maps agree, and disagreement requires one immutable history mode per equality class of those maps before unique coarsest exact repair.

## What the paper should and should not claim

### Core claim

The manuscript gives a finite structural theory for deciding whether an
**already exact** macro-law retains one terminal meaning across non-nested
replacement histories and for deriving the necessary-and-sufficient historical
context when it does not.

### Do claim

- Source and target state spaces need not be nested for exact transport.
- A source macro projection can induce target labels through a declared relation.
- Target-only actions can force a canonical, coarsest exact refinement of the
  carried partition.
- The resulting repair cost is quantifiable in macrostate count and bits.
- Path-label coherence is sufficient for route-independent repair on a declared
  finite replacement DAG.
- When carried label maps differ across paths, the number of distinct maps is the
  minimum history-context cardinality needed to represent them all.

### Do not claim

- That an observed ecological system has been shown to obey one of these finite
  certificates.
- That the declared relation or replacement history can be inferred from field
  data by the present theory.
- That a positive defect proves no alternative target abstraction exists after
  abandoning source provenance.
- That a failed coherence certificate proves history must be stored in every
  ecological model.
- That the deterministic finite theory already covers stochastic, approximate,
  continuous, recurrent, or partially observed systems.

## Contribution hierarchy

The formal theorem labels remain in dependency order, but the reader-facing
hierarchy begins with the historical result.

### Headline package — route coherence and minimum historical completion

Every declared root-to-terminal path induces a complete carried terminal map
\(c_p\). One route-independent inherited law exists exactly when these maps
agree. When they do not, two paths can share one immutable history mode if and
only if their maps agree, hence

\[
|H_{\min}|=|\{c_p\}|,
\qquad
\Delta_H^K=\log_2|H_{\min}|.
\]

History-sliced relative refinement then constructs the unique coarsest exact
history-aware interface. This is the manuscript headline. Its importance is
the necessary-and-sufficient minimum, not a generic claim that ecology is path
dependent or a claim of literature-firstness.

### Supporting infrastructure — route-specific portability and repair

A total relation carries a common exact macro-law when output, legal-action
rows, labels, and successors are preserved. When the carried partition fails,
a finite local witness identifies the split and standard refinement initialized
at the carried labels returns the unique coarsest exact target interface that
preserves inherited semantics.

This infrastructure defines the source-relative transport defect

\[
\Delta_{\#}=|Q_T^{\min}|-|Q_S|,
\qquad
\Delta_K=\log_2|Q_T^{\min}|-\log_2|Q_S|,
\]

and supports the accumulating binary witness. It is essential to the proof
architecture but is not presented as a new generic exactness, lumpability, or
partition-refinement result.

## Recommended manuscript structure

1. **Introduction** — accepted laws may lose one terminal meaning across
   replacement histories; state the route-coherence/history-minimum conclusion.
2. **Finite replacement setting** — controlled systems, action grammars, exact
   macro projections, and total non-nested replacement relations.
3. **Headline Results: replacement histories** — Result IV, coherent diamond,
   incoherent boundary diamond, Result V, and minimum history augmentation.
4. **Supporting Results: transport and derived target labels** — Result I and
   the conservative target-only-action boundary.
5. **Supporting Results: unique coarsest repair and transport defect** — Result
   II, local split obstruction, and Result III binary family.
6. **Worked ecological example** — connect the route decision and target repair
   to one restoration-priority reversal.
7. **Discussion** — lead with equality classes of complete carried maps, then
   interpret the portability and repair infrastructure and empirical limits.

The paper should not be divided by implementation modules. The reader should see
one progression:

```text
declared replacement histories
    → compare complete carried terminal maps
    → one route-independent law if maps agree
    → one immutable mode per map class if they do not
    → unique coarsest exact repair within the resulting context
```

## Results section posture

This is a theorem paper. Use the heading **Results** only if each subsection
states a formal finite result and follows it immediately with its interpretation
and witness. Do not write as though the repository's finite witnesses were field
experiments.

Useful opening sentence:

> An accepted source macro-law has one route-independent terminal meaning
> exactly when all declared histories induce the same complete carried map;
> otherwise, equality classes of those maps are the necessary-and-sufficient
> immutable history modes before unique coarsest exact repair.

## Figure and table plan

### Figure 1 — The transport-to-history decision structure

A left-to-right diagram:

```text
exact source macro-law + declared replacement relation
                │
                ├── target labels exact → unchanged transport
                │
                └── target labels not exact → coarsest relative refinement
                                                    │
                                                    ├── one replacement path → transport defect
                                                    │
                                                    └── multiple histories
                                                           │
                                                           ├── path-label coherent → one route-independent repair
                                                           └── incoherent → minimum history augmentation
```

This should be the conceptual figure in the main text.

### Figure 2 — Local split and accumulating transport defect

Panel A: a carried target fiber split by one target-only action.

Panel B: binary probe family showing

\[
2\longrightarrow 2^m+1
\]

exact macrostates. The caption must state that the global probe alphabet grows
with \(m\).

### Figure 3 — Coherent versus incoherent replacement diamonds

Panel A: two paths with identical carried labels and identical repair.

Panel B: two paths with distinct carried maps, followed by two immutable history
slices and the history-aware exact interface.

### Table 1 — Finite outcomes after replacement

| Declared condition | Exact object retained | Required response |
|---|---|---|
| Edge relation preserves exact interface conditions | Common macro-law | Transport unchanged |
| Carried partition is not exact at target | Source provenance | Coarsest relative refinement |
| Multiple paths carry identical terminal labels | One target repair | Route-independent transport defect |
| Multiple paths carry distinct terminal labels | All path-specific carried maps | Minimum history augmentation |

## Proposed Results-to-Discussion transition

> The results show that replacement-induced nonportability has two distinct
> sources. One is local to the terminal system: newly relevant outputs, actions,
> or successors split an inherited macro fiber. The other is historical: distinct
> replacement routes assign incompatible inherited labels to the same terminal
> configuration. The discussion asks how these two sources should be interpreted
> in ecological theory and how they could be operationalized in empirical work.

## Relationship to RACH

Keep this manuscript independent from the frozen RACH paper.

- **RACH:** under a fixed finite system, widening the declared future connection
  grammar can increase the exact memory needed for an open interface.
- **EXT:** after non-nested replacement, a previously exact macro-law may be
  transportable, require target repair, or require retained replacement history.

A brief sentence in the Discussion can call them complementary problems, but the
EXT manuscript should not rely on RACH's open-composition lower bound or reuse
its headline claim.
