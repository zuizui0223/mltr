# Monitoring-repair companion layer

> **Status:** preserved companion results split out of Paper A. These statements were developed on PR #30 and are retained because they are mathematically useful, but they are not part of the standalone Paper A headline after the carried-semantics reframing in PR #38. Generic entropy identities, sensor discrimination, set cover, and value-of-information machinery are not claimed as new.

## 1. Setup

Let `C` be the inherited target classification and `Q*` the unique coarsest exact target repair refining `C`. Define the obstruction universe

\[
E=\{(x,x'): C(x)=C(x'),\; Q^*(x)\neq Q^*(x')\}.
\]

For a candidate measurement library indexed by `J`, let `z_j(x)` be measurement `j` on target state `x`. For `S\subseteq J`, write `z_S(x)=(z_j(x))_{j\in S}`.

A selected measurement set `S` **realizes the repaired state exactly relative to `C`** when there exists a decoder `d_S` such that

\[
Q^*(x)=d_S(C(x),z_S(x))
\]

for every target state.

## 2. Exact monitoring realization criterion

A selected measurement set `S` realizes `Q*` relative to `C` **if and only if** every obstruction pair is separated by at least one selected measurement:

\[
\forall (x,x')\in E\;\exists j\in S:\quad z_j(x)\neq z_j(x').
\]

### Proof

**Necessity.** Suppose `S` realizes `Q*` and take `(x,x')\in E`. If no selected measurement separated the pair, then `C(x)=C(x')` and `z_S(x)=z_S(x')`. The decoder would receive identical inputs and return the same repaired label, contradicting `Q^*(x)\neq Q^*(x')`.

**Sufficiency.** Assume every pair in `E` is separated by at least one selected measurement. If `C(x)=C(x')` and `z_S(x)=z_S(x')` but `Q^*(x)\neq Q^*(x')`, then `(x,x')\in E`, so some selected measurement would separate them, a contradiction. Therefore `Q*` is constant on every realized tuple `(C(x),z_S(x))`; defining `d_S` by that common value gives an exact decoder.

For each candidate measurement define

\[
A_j=\{(x,x')\in E:z_j(x)\neq z_j(x')\}.
\]

Therefore the least-cost exact realization with additive costs `c_j` is

\[
\min_{S\subseteq J}\sum_{j\in S} c_j
\quad\text{subject to}\quad
\bigcup_{j\in S}A_j=E.
\]

A realization exists exactly when

\[
\bigcup_{j\in J}A_j=E.
\]

Any obstruction pair outside this union is an explicit impossibility certificate for the supplied monitoring library.

## 3. Minimum conditional repair information

Let `X_\mu\sim\mu` be a target-state draw and write `C=C(X_\mu)`, `Q=Q^*(X_\mu)`, and `P=P(X_\mu)` for any exact target classification `P` refining `C`.

Because every exact refinement `P` of `C` also refines the coarsest exact repair `Q*`, there is a deterministic map `f` with `Q=f(P)`. Hence

\[
H_\mu(P\mid C)
=H_\mu(Q,P\mid C)
=H_\mu(Q\mid C)+H_\mu(P\mid Q,C)
\ge H_\mu(Q\mid C).
\]

Thus

\[
\boxed{H_\mu(Q^*\mid C)\le H_\mu(P\mid C)}.
\]

If carried class `c` contains `k_c` repaired `Q*` blocks, then

\[
0\le H_\mu(Q^*\mid C)
\le \sum_c \Pr_\mu(C=c)\log_2 k_c
\le \log_2\max_c k_c.
\]

This is an information-theoretic corollary of coarsest exact repair, not a new general entropy theorem.

## 4. Structural defect does not order decision regret

For every integer `d\ge1` and every real `r\ge0`, there exists a finite target operational system, inherited classification `C`, coarsest exact repair `Q*`, target-state distribution `\mu`, finite management action set, and payoff function such that

\[
|Q^*|-|C|=d
\qquad\text{and}\qquad
\mathcal R_\mu(C,Q^*;u)=r.
\]

A witness takes `d+1` target states in one inherited class, gives them distinct declared outputs so exactness forces the singleton repair, and places probability `1/2` on two states whose optimal management actions disagree. Scaling the two-state payoff contrast sets regret to any prescribed `r` while leaving the structural defect fixed at `d`.

Consequently state-count defect alone provides neither a nontrivial universal upper bound nor a positive universal lower bound on decision regret, and it cannot universally rank management consequence. Probabilities, utilities, and measurement costs must be analyzed directly.

## 5. Paper boundary

Paper A keeps source-carried semantics, decision sufficiency, fixed-route composition, route coherence, and minimum historical completion as the standalone manuscript contribution. The monitoring-repair results above remain an executable/theoretical companion layer for later monitoring-design or application work; they should not be allowed to make the Paper A novelty claim look like generic sensor selection or set cover.
