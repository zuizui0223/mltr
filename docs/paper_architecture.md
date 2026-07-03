# EXT paper architecture: portable macro-laws under ecological replacement

## Recommended working title

**Exact Macro-Law Transport through Ecological Replacement: Minimal Repair and Historical Context**

A shorter alternative is **Portable Macro-Laws after Ecological Replacement**.

The first title is preferable while the paper remains theorem-first because it
names the formal object (exact macro-law transport), the domain reading
(ecological replacement), and the two nontrivial extensions (repair and history).

## One-sentence thesis

> In declared finite ecological replacement models, an exact macro-law is not simply portable or nonportable: it can be transported unchanged, repaired by a uniquely minimal target refinement, made route independent by path-label coherence, or completed by a minimum finite history context when replacement histories carry incompatible terminal labels.

## What the paper should and should not claim

### Core claim

The manuscript gives a finite structural theory for carrying an **already exact**
macro-law across non-nested replacement relations and for diagnosing the minimum
additional state distinction required when unchanged transport fails.

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

The paper will be stronger if its results are not presented as seven equal
"theorems." They form one escalating decision structure.

### Result I — Exact transport across non-nested replacement

**Role:** foundational transport result.

A total relation preserves a common exact macro-law when it preserves output,
legal-action rows, macro labels, and successors. Under target-fiber label
consistency, target labels can be derived from the root/source projection rather
than supplied in advance.

**Paper status:** theorem-level result; needed to make all later repair claims
about transported source semantics rather than an arbitrary target partition.

### Result II — Canonical repair after target change

**Role:** main mathematical contribution.

Starting from carried target labels, output/legal-row/successor partition
refinement returns the coarsest exact target interface that preserves every
carried merge still possible. This defines the relative transport defect.

\[
\Delta_{\#}=|Q_T^{\min}|-|Q_S|,
\qquad
\Delta_K=\log_2|Q_T^{\min}|-\log_2|Q_S|.
\]

**Paper status:** headline theorem. It turns failed portability into a unique
minimal repair problem, rather than an all-or-nothing failure statement.

### Result III — Repair can accumulate sharply

**Role:** quantitative witness.

The binary target-only-probe family shows that independently newly addressable
target distinctions can make the relative repair grow as

\[
|Q_T^{\min}|=2^m+1,
\qquad
\Delta_{\#}=2^m-1.
\]

**Paper status:** sharp finite family, not a claim that real ecological systems
use a constant-size global action alphabet or have this exact growth rate.

### Result IV — Coherent histories make repair route independent

**Role:** graph-level extension.

When every root-to-terminal path carries the same root macro labels to every
terminal product state, the carried partition and its coarsest exact repair are
independent of replacement route.

**Paper status:** theorem-level result. It separates terminal-state dependence
from replacement-history dependence.

### Result V — Incoherent histories have a canonical finite completion

**Role:** completion proposition, not the paper headline.

If paths carry different terminal label tuples, the smallest immutable history
context has one mode per distinct tuple. History-sliced relative refinement then
constructs the coarsest exact history-aware interface.

\[
|H_{\min}|=|\{c_p\}|,
\qquad
\Delta_H^K=\log_2|H_{\min}|.
\]

**Paper status:** call this a proposition or canonical construction in the
manuscript. Its importance is conceptual closure: it says precisely what must be
added when route independence fails. Its proof should be short.

## Recommended manuscript structure

1. **Introduction** — ecological replacement changes state spaces and future
   intervention repertoires; existing coarse laws need a transfer criterion.
2. **Finite replacement setting** — controlled systems, action grammars, exact
   macro projections, and total non-nested replacement relations.
3. **Transport and derived target labels** — Results I and the conservative
   target-only-action boundary.
4. **Minimal repair and transport defect** — Result II, local split obstruction,
   and Result III binary family.
5. **Replacement histories** — Result IV, coherent diamond, and incoherent
   boundary diamond.
6. **Minimum history augmentation** — Result V and history-sliced exact repair.
7. **Discussion** — what replacement changes in ecological macro-laws, what
   history dependence means, and what an empirical extension would require.

The paper should not be divided by implementation modules. The reader should see
one progression:

```text
transport unchanged
    → repair if target distinctions split carried fibers
    → route-independent repair if path labels cohere
    → minimum history context if they do not
```

## Results section posture

This is a theorem paper. Use the heading **Results** only if each subsection
states a formal finite result and follows it immediately with its interpretation
and witness. Do not write as though the repository's finite witnesses were field
experiments.

Useful opening sentence:

> We obtained a finite decision structure for the fate of an exact source
> macro-law after non-nested replacement: unchanged transport, canonical target
> repair, route-independent repair, or minimum history-aware completion.

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
