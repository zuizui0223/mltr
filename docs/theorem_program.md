# EXT theorem program: macro-law transport across ecological replacement

## Central question

Let a source controlled system and a target controlled system represent two
finite ecological stages connected by turnover, extinction, recolonization, or
rewiring. The raw state spaces need not be nested. When can one exact macro-law
be transported from source to target, and when it cannot, what is the minimum
exact target repair of the carried macro partition?

The paper target is not “all ecology after turnover.” It is the finite structural
problem

\[
\text{source exact macro-law}
+\text{ declared replacement relation}
\Longrightarrow ?
\text{ target exact macro-law}.
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
q_T(t)=q_S(s)\qquad ((s,t)\in R)
\]

is well-defined and exact on the target. It induces the same macro dynamics as
\(q_S\).

The key discovery is constructive: **target labels are derived rather than
assumed**.

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

## Theorem E — relative exact refinement and transport defect

Assume the conservative old-action conditions of Theorem C, but do not assume
that target-only actions are uniform in carried fibers. The replacement relation
still induces a carried target partition \(c_R\). Repeatedly split its blocks by
current output, legal-action row, and successor block under each legal target
action.

The finite fixed point is the **coarsest exact target projection refining**
\(c_R\). Hence it is the unique minimal repair of this carried macro-law.

If \(Q_S\) is the source macrostate set and \(Q_T^{\min}\) is that repaired
target projection, define

\[
\Delta_{\#}=|Q_T^{\min}|-|Q_S|,
\qquad
\Delta_K=\log_2|Q_T^{\min}|-\log_2|Q_S|.
\]

These are the relative transport defect in macrostate count and exact interface
memory. For the accumulating binary witness with \(m\) newly legal probes,

\[
|Q_S|=2,
\qquad
|Q_T^{\min}|=2^m+1,
\qquad
\Delta_{\#}=2^m-1.
\]

See [transport defect](transport_defect.md) for the proof and boundary.

## Ecological interpretation

| Mathematical object | Synthetic ecological reading |
|---|---|
| source stage | community before species loss, colonization, or rewiring |
| target stage | replacement community with potentially different raw microstates |
| replacement relation | declared correspondence between pre- and post-turnover configurations |
| action | permitted intervention, connection, perturbation, or future event |
| macro-law | coarse ecological description exact under the declared action grammar |
| transport defect | additional coarse ecological states required because new target interactions distinguish configurations formerly merged |

Possible application contracts include pollinator guild turnover, island
colonization/extinction, host replacement after pathogen invasion, restoration
rewiring, and succession. None is validated by the theorem without a separately
declared finite model and relation.

## Explicit non-claims

- No theorem infers replacement relations from field observations.
- No failed transport certificate proves all macro-laws fail.
- The transport defect is relative to a declared carried partition; it does not
  prove a globally minimal target abstraction after abandoning source provenance.
- No result yet covers stochastic, approximate, continuous, or unbounded systems.
- No result validates a macro-law for a real ecosystem.