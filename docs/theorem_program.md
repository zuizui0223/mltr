# EXT theorem program: macro-law transport across ecological replacement

## Central question

Let a source controlled system and a target controlled system represent two
finite ecological stages connected by turnover, extinction, recolonization, or
rewiring. The raw state spaces need not be nested. When can one exact macro-law
be transported from source to target?

The paper target is not “all ecology after turnover.” It is the following finite
structural problem:

\[
\text{source exact macro-law}
+ \text{declared replacement relation}
\Longrightarrow ?
\text{target exact macro-law}.
\]

## Formal setup

A stage is a finite deterministic output system together with a finite
prefix-closed action grammar. An exact stage projection is a label map on
`system state × grammar state` preserving:

1. current output;
2. the legal-action row; and
3. the successor label under every legal action.

A replacement relation is a total relation

\[
R\subseteq S\times T
\]

between source and target product states. It may be many-to-one or one-to-many.
It is therefore not assumed to be an embedding.

## Theorem A — transport of a supplied common macro-law

Suppose source and target already have exact projections into one finite macro
dynamics. If every related pair has the same macro label, output, legal-action
row, and related successor under every legal action, then one macro-law is shared
across that replacement edge. If such edges connect a finite replacement graph,
the macro-law is shared across the declared graph.

This is a sufficient finite-domain theorem. It does not infer relations or
classify every possible rewiring.

## Theorem B — derived target exact projection

Let \(q_S:S\to Q\) be an exact source projection. Suppose the relation:

1. covers all source and target product states;
2. is label-consistent on every target fiber;
3. preserves output;
4. preserves equal legal-action rows; and
5. is successor-closed.

Then

\[
q_T(t)=q_S(s) \qquad ((s,t)\in R)
\]

is well-defined and exact on the target. It induces the same macro dynamics as
\(q_S\).

The key discovery is constructive: **target labels are derived rather than
assumed**. This is the main result around which a theorem-first paper can be
built.

## Theorem C — conservative transport with target-only actions

Equal legal-action rows are stronger than necessary. Keep a common finite action
alphabet, preserve all source-legal actions and their successors, then permit a
target-only action only if, within each derived target macro fiber, it has:

- one availability status; and
- one target macro successor.

Then source and target realize one conservative macro schema: source rows are
restrictions, target rows are the expanded schema rows.

This theorem is sufficient. A successful certificate does not show uniqueness,
and its failure does not prove that no alternative target macro-law exists.

## Proposition D — newly legal word splits a carried merge

When a future word is illegal in the source grammar but legal after replacement,
and it gives distinct target traces from two carried states inside one proposed
macro fiber, that proposed merge is not exact at target.

This is a local obstruction. It identifies a repair requirement, not global
memory growth or universal impossibility.

## Ecological interpretation

| Mathematical object | Synthetic ecological reading |
|---|---|
| source stage | community before species loss, colonization, or rewiring |
| target stage | replacement community with potentially different raw microstates |
| replacement relation | declared correspondence between pre- and post-turnover configurations |
| action | permitted intervention, connection, perturbation, or future event |
| macro-law | coarse ecological description exact under the declared action grammar |

Possible application contracts include pollinator guild turnover, island
colonization/extinction, host replacement after pathogen invasion, restoration
rewiring, and succession. None is validated by the theorem without a separately
declared finite model and relation.

## Paper-shaped gap still open

The extracted theorems are sufficient and executable. A full next paper should
answer one further quantitative question:

> When transport fails, what is the minimum target refinement needed to repair
> the carried macro-law?

This motivates three possible next results:

1. **transport defect:** the minimum number of target-fiber splits needed for an
   exact target projection;
2. **path independence:** conditions under which transport around a replacement
   graph gives the same target labels regardless of route;
3. **stochastic/approximate transport:** controlled relaxations for ecological
   turnover with noisy transitions.

The first is the best immediate theorem target: it follows directly from the
existing fiber-split obstruction without mixing in a new empirical domain.

## Explicit non-claims

- No theorem infers replacement relations from field observations.
- No failed transport certificate proves all macro-laws fail.
- No result yet covers stochastic, approximate, continuous, or unbounded systems.
- No result validates a macro-law for a real ecosystem.
