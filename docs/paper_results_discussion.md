# Working Results and Discussion Draft

This document is a manuscript-facing draft for the EXT paper. It is written for
a theorem-first submission and intentionally contains no empirical claims. A
later literature pass should add citations in the Introduction and selected
Discussion paragraphs without changing the scope of the results.

## Results

### Overview

We obtained a finite decision structure for the fate of an exact source
macro-law after non-nested replacement. A source macro-law can be transported
unchanged when a declared replacement relation preserves the required
output/action/successor structure. If the transported labels remain meaningful
but are no longer exact at the target, the target admits a unique coarsest repair
that preserves the source provenance. When several replacement histories reach
the same terminal stage, this repair is route independent exactly under a
path-label coherence condition. If the condition fails, the distinct carried
label maps determine the minimum finite history context required to represent
all declared histories simultaneously.

All results concern declared finite deterministic controlled systems with finite
prefix-closed action grammars. In particular, a replacement relation, a set of
allowed actions, and the relevant outputs are supplied as part of the model
contract. The theorems do not infer these objects from observations.

### Exact macro-law transport does not require nested state spaces

We first considered a source stage and a target stage whose raw state spaces need
not be related by inclusion. Let a source exact projection map source product
states to a finite macrostate set. A replacement relation can be many-to-one or
one-to-many, so it does not function as an embedding of the source into the
target.

We showed that one macro-law is shared across the relation when related states
have the same macro label, current output, legal-action row, and related
successor under every legal action. Thus exact transport is a preservation
property of a declared relation, rather than a consequence of state-space
nesting. This matters for ecological replacement because extinction,
recolonization, and rewiring can change the available micro-configurations
without making the old configurations a literal subset of the new ones.

We next gave a constructive version of this result. When an exact source
projection and a total replacement relation satisfy target-fiber label
consistency together with output, legal-row, and successor preservation, the
target projection is derived by

\[
q_T(t)=q_S(s)\qquad ((s,t)\in R).
\]

The target macro labels therefore need not be chosen independently. The relation
carries the source semantics to the target, and exactness can then be checked on
the induced target projection.

A conservative extension result weakens the requirement that source and target
have identical legal-action rows. Source-legal actions must retain their
transported meaning, whereas an action that is legal only in the target is
portable when its availability and its target macro successor are uniform within
each carried target fiber. This identifies the first boundary of portability:
target novelty is compatible with transport only when it is macro-uniform.

### Replacement failure has a canonical minimum repair

We then considered the case in which old actions are preserved but target-only
actions, outputs, or successors distinguish states that inherit the same source
macro label. The source labels still define a carried target partition, but that
partition need not be an exact target interface.

Starting from the carried partition \(P_0\), we iteratively split a target block
whenever two of its states differ in current output, legal-action row, or the
current block of a successor under a common legal action. The finite iteration
stabilizes at a partition \(P_\infty\). We proved that

\[
P_\infty
\]

is the coarsest exact target interface refining the carried partition. In other
words, every exact target interface that preserves the transported source
semantics must make at least the splits made by \(P_\infty\). The result is
relative: it gives the minimum repair of the carried source macro-law, not the
smallest possible target abstraction after discarding source provenance.

This construction yields two measures of repair cost,

\[
\Delta_{\#}=|Q_T^{\min}|-|Q_S|
\]

and

\[
\Delta_K=\log_2|Q_T^{\min}|-\log_2|Q_S|,
\]

where \(Q_S\) is the source macrostate set and \(Q_T^{\min}\) is the repaired
target interface. The first counts additional macrostates, and the second
expresses the same change on a logarithmic exact-memory scale.

A local newly legal word provides a direct obstruction to unchanged transport. If
two target states inherit one source macro label but a target-only future word
produces different traces from them, they cannot remain merged in any exact
repair. The obstruction is local, but it becomes a mandatory split in the
coarsest refinement.

The binary probe family demonstrates that these splits can accumulate sharply. A
two-macrostate source has one `low` state and one `high` state. In the target,
there is one low state for every binary vector

\[
(b_1,\ldots,b_m)\in\{0,1\}^m,
\]

and a target-only `probe_i` exposes bit \(b_i\). Every low vector inherits one
source label, yet the probes distinguish every pair of vectors. Consequently,

\[
|Q_S|=2,
\qquad
|Q_T^{\min}|=2^m+1,
\qquad
\Delta_{\#}=2^m-1.
\]

This is a sharp finite witness for relative repair accumulation. It does not
assert that ecological systems have this exact architecture, and the family uses
a global probe alphabet that grows with \(m\).

### Coherent replacement histories yield route-independent repair

A target stage can be reached through several declared histories. We represented
such histories by root-to-terminal paths in a finite directed acyclic
replacement graph and composed the replacement relations along each path. Every
path that is root-fiber-label-consistent induces a carried terminal label map
\(c_p\).

We defined path-label coherence by pointwise equality of all such maps:

\[
c_p(t)=c_{p'}(t)
\]

for every terminal product state \(t\) and every pair of root-to-terminal paths
\(p,p'\). Under this condition, the carried terminal partition is independent of
replacement route. Since relative exact refinement is a deterministic function
of the terminal system and carried partition, the repaired target interface and
both defect measures are route independent as well.

A coherent diamond witness illustrates the result. Each branch carries the same
target labels

\[
(0,0,1)
\]

to the terminal system. Both paths therefore return the same exact repair

\[
(0,1,2)
\]

and the same transport defect \(\Delta_{\#}=1\). Thus a terminal community can
have a unique transported macro-law even when the route by which it was reached
is not unique.

The corresponding boundary witness shows that total replacement relations alone
are insufficient. Two paths can assign the label tuples

\[
(0,1)
\qquad\text{and}\qquad
(1,0)
\]

to the same terminal raw states. The coherence certificate rejects this case.
The boundary witness deliberately does not certify the swapped edge as an
edge-level exact transport relation; it isolates the additional graph-level
condition required for route-independent carried semantics.

### Path incoherence has a minimum finite history completion

Finally, we asked what should be retained when different paths assign
incompatible carried labels to the same terminal configuration. A history mode
can represent several paths only when their complete carried terminal label
tuples are identical. Therefore the minimum number of history modes is the
number of distinct carried maps,

\[
|H_{\min}|=|\{c_p\}|.
\]

This gives the raw history-context cost

\[
\Delta_H^{\#}=|H_{\min}|-1,
\qquad
\Delta_H^K=\log_2|H_{\min}|.
\]

The result is a canonical completion proposition. Its role is not to claim that
history is always ecologically important; it states exactly how much finite
context is required to preserve a specified collection of incompatible carried
maps.

We constructed one immutable copy of the terminal controlled system for every
distinct carried map. Within each slice, the terminal action grammar and
dynamics are unchanged. Applying relative exact refinement to this
history-sliced system yields the coarsest exact history-aware interface that is
compatible with all declared path-specific carried labels.

For the incoherent two-route diamond, the two maps \((0,1)\) and \((1,0)\)
require two history modes. The lifted carried labels are

\[
(0,1,1,0).
\]

Exact refinement separates the four augmented witness states, giving

\[
|Q_r|=2,
\qquad
|Q_{T\times H}^{\min}|=4,
\qquad
\Delta_{\mathrm{HA}}^{\#}=2.
\]

The final history-aware exact-interface cost differs conceptually from the raw
history-context cost. The former counts the exact macrostates after refinement;
the latter counts the minimum modes required before any such refinement can
represent all path-specific carried semantics.

## Discussion

### Replacement changes the question from prediction to portability

The central implication of these results is that a macro-law should not be
regarded as either universally valid or simply falsified by ecological
replacement. Once a source law is exact for a declared model, replacement raises
a more structured question: which parts of that law remain valid, which source
merges must be split, and whether the answer depends on the path through which
the new community was reached.

This distinguishes two sources of post-replacement nonportability. The first is
terminal and local. A new output distinction, target-only intervention, or
successor structure can split states that the source macro-law merged. Relative
exact refinement measures this effect without abandoning the source semantics.
The second is historical. Different replacement routes can assign different
source-derived labels to the same terminal configuration. In that case, no
single carried terminal map exists until an appropriate history context is
retained.

The distinction matters because these failures suggest different scientific
responses. A positive transport defect calls for refining the target state
summary. Path incoherence calls for asking whether a historical variable is
required by the stated transfer problem. Treating both situations simply as
"model failure" would conceal this difference.

### Ecological replacement can alter both states and allowable interventions

The finite framework is designed for situations in which the ecological object
of interest changes through turnover, extinction, recolonization, restoration,
or interaction rewiring. These processes can alter the set of available
micro-configurations, but they can also change which interventions or future
connections are scientifically relevant. For example, a source community may be
summarized adequately for pre-restoration management actions, while a restored
community makes additional colonization, connectivity, or interaction actions
relevant. Those target-only actions can expose distinctions that were safely
merged in the source law.

The formalism therefore treats action grammars as part of the ecological model
contract rather than as incidental implementation detail. A macrostate is exact
only relative to the declared outputs and legal futures. This does not imply that
all possible ecological events must be included. Instead, it requires that the
future events relevant to the transfer question be stated before claims of
portability are made.

### History is required conditionally, not by default

The history result should not be read as the familiar statement that ecological
communities are generally historical. The theorem is more precise and narrower.
History becomes necessary in this framework only when distinct declared
replacement paths carry incompatible root macro labels to the same terminal
product state. If all paths carry the same label map, the terminal macro-law and
its repair are route independent even though the system has multiple possible
histories.

Conversely, when path-label coherence fails, the minimum history context is not
the full sequence of past events. It is the quotient of declared histories by
identical carried terminal label maps. The theorem thus provides a finite notion
of the smallest historical distinction needed for a specified transported
semantics. Subsequent exact refinement can still merge history slices whenever
the carried labels and all legal futures are indistinguishable.

### Transport defects are relative measures of lost compression

The quantities \(\Delta_{\#}\) and \(\Delta_K\) should be interpreted as costs
of preserving a source macro-law under replacement, not as intrinsic complexity
measures of the target community. A target may admit a smaller abstraction if
the source labels are discarded and a different scientific question is asked.
The relative formulation is a feature rather than a weakness: it allows a clear
comparison between what a previous macro-law remembered and what must be added
to continue using that law after replacement.

The same distinction applies to history augmentation. \(\Delta_H\) measures the
minimum raw context required to represent incompatible carried maps; it is not
a direct measure of the number of final macrostates. The history-aware defect
\(\Delta_{\mathrm{HA}}\) is the corresponding exact-interface cost after the
terminal dynamics and action grammar have been taken into account. Keeping these
costs separate prevents a historical bookkeeping requirement from being confused
with an unavoidable increase in predictive state dimension.

### Relation to the companion open-composition problem

The present theory concerns non-nested replacement of the system itself. It is
therefore distinct from the frozen RACH result, which studies how widening a
declared future connection grammar can increase the exact memory required within
a fixed finite setting. The two problems are complementary. RACH asks what must
be retained before multiple external compositions are permitted. EXT asks whether
an already exact macro-law can survive, be repaired, or require historical
context after the constituent system has been replaced.

The EXT manuscript should remain self-contained. The relationship is useful for
a broader research program, but the transport and history theorems do not depend
on the open-composition lower bound.

### What an empirical extension would require

Applying the theory to an ecological system would require a separate modeling
and data program. First, one would define a finite state representation, a set
of output variables, and a legal action grammar tied to the management or
scientific question. Second, one would state candidate replacement relations
between pre- and post-turnover configurations. Third, one would test whether
those relations approximately preserve output, action availability, and
successor behavior. Finally, one could compare candidate histories by the
carried label maps they induce.

The current paper does not supply statistical estimators for these objects. In
particular, finite exactness is too strong for noisy observational data. A useful
next development would replace equality by a tolerance or risk criterion and
study approximate transport defects, confidence-aware path coherence, and
history augmentation under partial observation.

### Limits and next steps

Several boundaries are explicit. The current framework is finite and
deterministic, and replacement graphs are acyclic. It does not yet handle
recurrent replacement, stochastic transitions, continuous states, inferred
relations, unknown action grammars, or measurement error. Nor does it establish
necessary and sufficient conditions for all possible target abstractions.

These limitations identify a concrete next agenda rather than a conceptual gap
in the present paper. The deterministic finite theory supplies the baseline
against which approximate and stochastic versions can be defined. The next
technical extension should be an approximate history-aware transport theory in
which a carried partition is allowed a specified trace discrepancy and the cost
of repair trades off against that discrepancy.

### Concluding interpretation

Ecological replacement need not erase the usefulness of a coarse law. It can
leave the law unchanged, force a quantifiable refinement, preserve the same
repair across alternative histories, or require a minimum history context before
an exact law can be stated. The contribution of EXT is to make these outcomes
finite, explicit, and distinguishable under one declared model contract.
