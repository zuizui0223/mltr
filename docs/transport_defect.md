# Transport defect: minimal exact repair after ecological replacement

## Question

The existing EXT transport theorems ask whether a source macro-law can be carried
unchanged to a target system. This document studies the next finite question:

> When the carried target partition is not exact, what is the smallest target
> refinement that repairs it?

The setting is deliberately restricted. A source exact projection and a declared
replacement relation must already preserve current output and every source-legal
action. Target-only actions may then split a carried target macro fiber.

## Carried target partition

Let

\[
q_S:S\to Q_S
\]

be an exact source projection, let `T` be a target controlled system, and let

\[
R\subseteq S\times T
\]

be a total relation satisfying the conservative old-action conditions of
`derive_conservative_target_labels`. Target-fiber label consistency defines the
carried partition

\[
c_R(t)=q_S(s)\qquad ((s,t)\in R).
\]

The relation therefore transports the old macro labels even when it does not yet
produce an exact target interface.

## Relative exact refinement theorem

Start from the carried partition \(P_0=c_R\). Given a partition \(P_n\), split
two target product states that are in the same \(P_n\)-block whenever they differ
in at least one of:

1. current output;
2. legal-action row; or
3. the \(P_n\)-block of a successor under a common legal action.

Call the resulting partition \(P_{n+1}\). The finite sequence

\[
P_0\preceq P_1\preceq P_2\preceq\cdots
\]

never merges carried blocks and stabilizes after finitely many strict splits.
Let \(P_\infty\) be the fixed point.

### Theorem

\[
\boxed{
P_\infty\text{ is the coarsest exact target interface that refines }c_R.
}
\]

Equivalently, if \(Q\) is any exact target interface whose blocks refine the
carried partition, then \(Q\) also refines \(P_\infty\).

### Proof

At a fixed point, states in one block have equal output, equal legal-action row,
and equal successor blocks for every legal action. The fixed point is therefore
an exact interface.

For minimality, let \(Q\) be any exact target interface refining \(P_0\). By
induction, suppose \(Q\) refines \(P_n\). If two states share a \(Q\)-label,
exactness gives equal output, equal legal row, and equal successor \(Q\)-labels.
By the induction hypothesis their successors also share \(P_n\)-labels, so the
two states cannot be split by the construction of \(P_{n+1}\). Hence \(Q\)
refines \(P_{n+1}\). The claim follows at the finite fixed point.

## Transport defect

Let \(Q_T^{\min}=P_\infty\) and let \(Q_S\) be the source macrostate set. The
minimal repair cost for this carried macro-law is

\[
\Delta_{\#}=|Q_T^{\min}|-|Q_S|
\]

additional macrostates, or

\[
\Delta_K=\log_2|Q_T^{\min}|-\log_2|Q_S|
\]

additional bits of exact interface memory.

- \(\Delta_{\#}=0\): the carried macro partition is already exact at target.
- \(\Delta_{\#}>0\): target replacement forces at least that many additional
  macrostate blocks for this transported description.

This is a **relative** defect. It does not claim that no smaller target
abstraction exists after abandoning the carried source partition, and it does
not infer a replacement relation from data.

## Accumulating binary defect family

For \(m\) target-only probes, source has two macro labels: `low` and `high`.
Only `reset` is source-legal. The target contains one low state for every binary
vector

\[
(b_1,\ldots,b_m)\in\{0,1\}^m
\]

and one high state. Newly legal `probe_i` moves a low vector to the high state
exactly when \(b_i=1\). The entire low vector family inherits one carried source
label, but the probes distinguish every pair of binary vectors. Therefore

\[
|Q_S|=2,
\qquad
|Q_T^{\min}|=2^m+1,
\]

and

\[
\boxed{\Delta_{\#}=2^m-1,\qquad
\Delta_K=\log_2(2^m+1)-1.}
\]

The witness uses a growing global probe alphabet. It does not claim a
constant-size global action alphabet, stochastic robustness, or direct empirical
realism.

## Ecological reading

A source stage can be read as a community before turnover; target-only probes
represent newly possible interaction opportunities after colonization,
extinction, restoration, or rewiring. A positive defect means that states once
safe to summarize together must be separated to preserve every declared target
intervention. The theorem does not infer which interactions are possible in a
real community; states, relation, and action grammar are supplied by a separate
finite model contract.
