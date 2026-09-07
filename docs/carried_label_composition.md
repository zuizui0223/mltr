# Compositional carried semantics under declared replacement relations

> **Status:** exact supporting proposition for Paper A. This result strengthens the source--target relation layer requested by the novelty audit. It is not a claim that relational composition, quotient refinement, or bisimulation machinery is historically new.

## 1. Problem

Let a source exact macro-law have label map

\[
\pi_0:X_0\to Q.
\]

Let

\[
R\subseteq X_0\times X_1,
\qquad
S\subseteq X_1\times X_2
\]

be declared finite replacement relations. In the executable model the `X_i` are grammar-aware product-state spaces. Every relation is **total on both sides** in the MLTR sense: every source state occurs in at least one pair and every target state occurs in at least one pair.

The basic source-relative question is not whether a target-only quotient exists. It is whether the inherited source label can be assigned unambiguously after replacement.

For one relation `R`, define the carried label at `x_1` only when all source states related to `x_1` have the same source label:

\[
\pi_R(x_1)=q
\quad\Longleftrightarrow\quad
\{\pi_0(x_0):(x_0,x_1)\in R\}=\{q\}.
\]

Thus a many-to-many relation is allowed. What is forbidden is a **source-semantic conflict**: one target state receiving two distinct inherited source labels.

## 2. Proposition — exact local criterion for a carried label map

A carried label map through `R` exists if and only if every target state receives exactly one source-label value:

\[
\forall x_1\in X_1,
\qquad
\left|
\{\pi_0(x_0):(x_0,x_1)\in R\}
\right|=1.
\]

Because target coverage is assumed, the set is never empty. Therefore failure has a finite local witness

\[
(x_1,q,q'),\qquad q\ne q',
\]

with source states of labels `q` and `q'` both related to the same target state `x_1`.

This is a label-transport obstruction, not the later target-dynamics refinement obstruction. The two should remain conceptually separate in Paper A.

## 3. Proposition — direct and sequential transport commute

Assume `R` and `S` are total on both sides. Then the following are equivalent:

1. direct carried transport through the relational composite
   \[
   R;S=\{(x_0,x_2):\exists x_1,\ x_0Rx_1\land x_1Sx_2\}
   \]
   is well defined;
2. the carried map through `R` is well defined and, using that map as the inherited labels on `X_1`, the carried map through `S` is well defined.

Whenever these equivalent conditions hold,

\[
\boxed{
(\pi_0)_{R;S}=(\pi_R)_S.
}
\]

### Proof

#### Sequential implies direct

Suppose both sequential carries are well defined. Take any terminal state `x_2` and any two source states `x_0,x'_0` related to it through the composite. Choose witnesses `x_1,x'_1` with

\[
x_0Rx_1Sx_2,
\qquad
x'_0Rx'_1Sx_2.
\]

Because the first carry is well defined,

\[
\pi_0(x_0)=\pi_R(x_1),
\qquad
\pi_0(x'_0)=\pi_R(x'_1).
\]

Because the second carry is well defined and both `x_1,x'_1` relate to `x_2`,

\[
\pi_R(x_1)=\pi_R(x'_1).
\]

Hence every source state reaching `x_2` through `R;S` has the same inherited label, so direct transport is well defined. The common value is exactly the sequential terminal label, proving pointwise equality.

#### Direct implies the first carry

Suppose direct transport through `R;S` is well defined but the carry through `R` is not. Then some `x_1` receives source states `x_0,x'_0` with different source labels. Source coverage of `S` guarantees at least one `x_2` with `x_1Sx_2`. Both `(x_0,x_2)` and `(x'_0,x_2)` then lie in `R;S`, contradicting direct well-definedness.

#### Direct implies the second carry

The first carry is therefore well defined. Suppose the second carry is not. Then some terminal `x_2` receives intermediate states `x_1,x'_1` with different carried labels. Target coverage of `R` guarantees source states `x_0Rx_1` and `x'_0Rx'_1`. By definition of the first carry,

\[
\pi_0(x_0)=\pi_R(x_1)
\ne
\pi_R(x'_1)=\pi_0(x'_0).
\]

Both source states reach `x_2` through `R;S`, again contradicting direct well-definedness. Therefore the second carry is well defined. `\square`

## 4. Corollary — fixed-route parenthesization is irrelevant

By induction, for any finite chain of declared total relations

\[
R_1,R_2,\ldots,R_k,
\]

carried source semantics is either undefined for both direct and stepwise transport, or else every parenthesization gives the same terminal carried label map:

\[
\boxed{
\pi_{R_1;\cdots;R_k}
=(((\pi_{R_1})_{R_2})\cdots)_{R_k}.
}
\]

Thus there are two distinct questions:

1. **within one route:** direct and sequential transport cannot disagree merely because the route was decomposed into more stages;
2. **between different routes:** distinct composite relations can still induce different terminal carried maps, which is exactly the route-coherence problem treated by the history theorem.

This separation sharpens the role of history. Historical context is not required because a fixed route is represented stepwise rather than directly. It is required only when genuinely different declared routes induce incompatible terminal inherited meanings.

## 5. Relation to established refinement theory

This proposition does **not** make the coarsest-refinement result novel. Once one carried partition is fixed on a target system, computing its coarsest exact refinement is established partition-refinement / abstraction machinery. The present proposition belongs one layer earlier: it states when the inherited source labels themselves are well-defined under many-to-many non-nested replacement and proves that this label transport composes consistently.

This is the safe Paper A hierarchy:

1. source-label carriage through a relation: local semantic-consistency condition;
2. relation composition: direct = sequential carried semantics;
3. route coherence: different replacement routes agree or disagree at the terminal system;
4. minimum history completion: retain exactly the carried-map distinctions required by route disagreement;
5. exact target refinement: standard machinery used after the carried semantics is fixed.

## 6. Executable surface

`ext_transport.compositional_transport` provides:

- `carried_label_conflicts(...)` — returns every target state receiving incompatible inherited labels;
- `derive_carried_labels(...)` — derives the inherited target map without renumbering source labels;
- `CarriedLabelCompositionCertificate` — audits direct versus sequential transport, including conflict cases;
- `certify_carried_label_composition(...)` — finite replay entry point.

The tests include:

- a coherent two-edge route;
- a state-swapping route showing that inherited label identity is preserved;
- a first-edge many-to-one label conflict;
- a second-edge conflict that is also visible in the direct composite.

These finite certificates are regression evidence. The quantified proof is the argument above.
