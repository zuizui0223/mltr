# MLTR history responsibility at a temporal cut — definition firewall

## Purpose

This note fixes the mathematical meaning of the **past/history** side used when MLTR is projected into CREST. It is a claim-control note, not a new theorem.

The critical distinction is between:

1. a raw declared replacement history, which exists before the terminal state quotient; and
2. the minimum history mode retained by MLTR, which is a quotient of those raw histories induced by carried semantics.

## Primitive objects

Fix a finite rooted directed acyclic replacement graph with root stage `r`, terminal stage `v`, and a declared total replacement relation `R_e` on each directed edge.

Fix an already accepted root macro-law

\[
q_r:S_r\to Q_r.
\]

The root law is part of the source-relative MLTR contract. It is not defined from the terminal CREST state.

A raw declared history is a root-to-terminal path

\[
p=(e_1,\ldots,e_k).
\]

Its composite replacement relation is

\[
R_p=R_{e_1};\cdots;R_{e_k}\subseteq S_r\times S_v.
\]

Thus the raw past object is the path `p` (or equivalently the declared composite relation together with its route identity), not a history mode and not a terminal macrostate.

## Carried semantic map

When root-fiber labels are consistent along `R_p`, the path induces the carried terminal map

\[
c_p:S_v\to Q_r,
\qquad
c_p(t)=q_r(s)\ \text{for }(s,t)\in R_p.
\]

This map is defined from the root law and the declared replacement relations before any history-aware terminal quotient is constructed.

## History equivalence

Two declared histories are equivalent for inherited semantics exactly when they induce the same complete carried terminal map:

\[
p\equiv_H p'
\iff
c_p=c_{p'}.
\]

The minimum raw history context is therefore

\[
H_{\min}=\{c_p:p\text{ declared root-to-terminal path}\},
\]

or equivalently the quotient of declared paths by `equiv_H`.

Only after this history quotient exists does MLTR construct the history-sliced terminal system and apply exact target refinement.

## Why this is non-circular

The dependency order is

\[
q_r,\ \text{rooted replacement DAG},\ \{R_e\}
\longrightarrow
p
\longrightarrow
R_p
\longrightarrow
c_p
\longrightarrow
\equiv_H
\longrightarrow
H_{\min}
\longrightarrow
\text{history-aware terminal refinement}.
\]

The terminal adequate state does not appear on the right-hand side of any definition used to construct `p`, `R_p`, or `c_p`.

The rooted DAG assumption also prevents semantic recursion through replacement cycles: every declared history begins at the fixed root law and terminates after finitely many forward replacement edges.

Therefore MLTR is **well founded but source relative**. It does not define ecological history from scratch; it answers the conditional question: given one accepted source semantic map and one declared replacement graph, which distinctions among histories must survive at the terminal cut?

## Bootstrap boundary

Because `q_r` is an accepted source macro-law, MLTR should not be used to claim that CREST derives the first ecological state in the universe without prior semantic commitments. For the temporal-cut flagship, the safe statement is:

> MLTR supplies a retrospective responsibility conditional on a declared root semantic map.

If a sequence of CREST analyses is applied recursively through time, each application must identify its root contract explicitly. No theorem in the current MLTR paper licenses a closed semantic loop in which the terminal state is used to define its own root law.

## Relation to CCOC

MLTR fixes `q_r` and varies declared replacement histories. CCOC independently optimizes exact response interfaces under declared future grammars. This is the existing quantifier firewall:

\[
\text{MLTR: fixed inherited law }q_r\ \to\ \text{transport/history};
\]

\[
\text{CCOC: fixed controlled system law }\mathcal M\ \to\ \text{future-grammar response equivalence}.
\]

A newly legal future action can make an MLTR-carried state decision-insufficient, but that does not redefine the past path itself.

## Relation to the temporal cut

For a CREST world `omega` observed at terminal cut `t`, let `p_t(omega)` be its declared replacement route from the fixed root contract. The retrospective responsibility map may be written

\[
H_t(\omega)=c_{p_t(\omega)}.
\]

Two same-cut worlds require distinct historical context exactly when these carried maps differ under the declared MLTR contract.

## Scope

This note does not infer historical pathways, replacement relations, or the root law from data. It fixes the finite non-circular dependency order already implicit in the MLTR route-coherence and minimum-history theorems.
