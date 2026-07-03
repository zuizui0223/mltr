# EXT theorem program: macro-law transport across ecological replacement

## Central question

Let a source controlled system and a target controlled system represent two
finite ecological stages connected by turnover, extinction, recolonization, or
rewiring. The raw state spaces need not be nested. When can one exact macro-law
be transported from source to target, when it cannot, what is the minimum exact
target repair of the carried macro partition, when is that repair independent of
replacement history, and what is the minimum history context when it is not?

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

## Theorem F — path-label coherence and route-independent repair

Let a rooted finite directed acyclic replacement graph have root exact projection
\(q_r\). Compose declared total edge relations along every root-to-terminal path
\(p\), yielding \(R_p\). When each path defines a carried terminal map

\[
c_p(t)=q_r(s)\qquad ((s,t)\in R_p),
\]

assume the maps agree pointwise across all root-to-terminal paths:

\[
c_p(t)=c_{p'}(t).
\]

Then one carried terminal partition is route independent. Because relative exact
refinement is a deterministic function of the terminal system and that carried
partition, its repaired target projection and the defects \(\Delta_{\#}\) and
\(\Delta_K\) are also route independent.

This graph-level theorem composes **declared** relations. It does not re-prove
that each edge preserves output, legal rows, and successors; those stronger
edge-level claims remain available through Theorems A–C. See [path-label
coherence](path_coherence.md) for proof, positive diamond, and negative boundary
witness.

## Theorem G — minimum history augmentation after route incoherence

Let \(c_p\) range over all well-defined carried terminal maps induced by declared
root-to-terminal paths. A finite history assignment can place two paths in one
history mode only when their entire carried label tuples coincide. Therefore the
minimum number of modes is

\[
|H_{\min}|=\bigl|\{c_p\}\bigr|.
\]

Retain one immutable terminal-system copy per distinct tuple and lift that tuple
to its copy. Relative exact refinement of this history-context system is the
coarsest exact interface compatible with every declared path-specific carried
map.

Define raw context and final exact-interface costs by

\[
\Delta_H^{\#}=|H_{\min}|-1,
\qquad
\Delta_H^K=\log_2|H_{\min}|,
\]

and

\[
\Delta_{\mathrm{HA}}^{\#}=|Q_{T\times H}^{\min}|-|Q_r|,
\qquad
\Delta_{\mathrm{HA}}^K=
\log_2|Q_{T\times H}^{\min}|-\log_2|Q_r|.
\]

The first cost is the minimum history context needed to retain all incompatible
carried maps; the second is the resulting exact macrostate repair. They need not
be equal. See [minimal history augmentation](history_augmentation.md) for proof
and the two-route boundary witness.

## Ecological interpretation

| Mathematical object | Synthetic ecological reading |
|---|---|
| source stage | community before species loss, colonization, or rewiring |
| target stage | replacement community with potentially different raw microstates |
| replacement relation | declared correspondence between pre- and post-turnover configurations |
| action | permitted intervention, connection, perturbation, or future event |
| macro-law | coarse ecological description exact under the declared action grammar |
| transport defect | additional coarse ecological states required because new target interactions distinguish configurations formerly merged |
| path-label coherence | different declared turnover histories preserve one carried terminal macro-law and repair |
| history augmentation | minimal retained path context when terminal labels are history dependent |

Possible application contracts include pollinator guild turnover, island
colonization/extinction, host replacement after pathogen invasion, restoration
rewiring, and succession. None is validated by the theorem without a separately
declared finite model and relation.

## Explicit non-claims

- No theorem infers replacement relations or replacement histories from field observations.
- No failed transport certificate proves all macro-laws fail.
- The transport defect is relative to a declared carried partition; it does not
  prove a globally minimal target abstraction after abandoning source provenance.
- Path coherence is sufficient for route-independent carried labels, not a
  characterization of every history-independent ecological representation.
- History augmentation is relative to declared carried maps; it does not infer a
  unique ecological memory variable or prove that observed history must be stored.
- No result yet covers stochastic, approximate, continuous, or unbounded systems.
- No result validates a macro-law for a real ecosystem.
