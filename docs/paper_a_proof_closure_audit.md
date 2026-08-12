# Paper A proof-closure audit

Audit date: 2026-08-12

This note responds to four proof gaps identified after the ecological reframing of Paper A and separates logical closure from publication novelty.

## 1. Minimum conditional repair information — CLOSED

The supplement now defines a target-state distribution `mu` and treats the inherited label `C`, coarsest exact repair `Q*`, and any admissible exact refinement `P` as finite random variables.

Because `Q*` is the coarsest exact refinement of `C`, every admissible exact `P` refines `Q*`. Hence `Q*` is a deterministic function of `P`. The supplement gives the explicit entropy chain-rule proof

`H(P | C) = H(Q*,P | C) = H(Q* | C) + H(P | Q*,C) >= H(Q* | C)`.

It also proves

`0 <= H(Q* | C) <= sum_c Pr(C=c) log2(k_c) <= log2(max_c k_c)`,

where `k_c` is the number of repaired blocks inside inherited class `c`.

Status: mathematically closed. This is presented as an information-theoretic corollary of coarsest repair, not as a new general entropy theorem.

## 2. Monitoring realization — CLOSED AND PROMOTED TO THE APPLIED BRIDGE

The earlier wording used “recover the repaired classification” without defining recovery. The supplement now makes this exact.

For candidate measurements `z_j : X -> Z_j` and selected set `S`, `S` realizes the repaired classification relative to `C` iff there exists a decoder `d_S` such that

`Q*(x) = d_S(C(x), z_S(x))`

for every target state.

Let

`E = {(x,x'): C(x)=C(x'), Q*(x) != Q*(x')}`

be the obstruction pairs.

The supplement proves the necessary-and-sufficient criterion:

`S realizes Q* relative to C`

iff

`every pair in E is separated by at least one selected measurement`.

The sufficiency proof explicitly constructs the decoder and proves it is well defined.

For each candidate measurement `j`, let `A_j` be the obstruction pairs it separates. The least-cost exact realization is therefore

`min sum_{j in S} c_j` subject to `union_{j in S} A_j = E`.

A realization exists iff the full candidate library covers `E`. Any uncovered obstruction pair is an explicit impossibility certificate: no monitoring design built from the supplied variables can reconstruct the decision-sufficient repaired state exactly.

Status: mathematically closed. This is the strongest ecological bridge in the paper. It does not claim a new set-cover algorithm; its contribution is to derive the monitoring target from failure of an inherited management state.

## 3. No universal defect–regret ordering — CLOSED WITH A STRONGER CONSTRUCTION

The main text previously stated a negative relation without defining regret formally. The supplement now defines, for a target distribution `mu`, management actions `U`, payoff `u`, and classification `P`,

`V_mu(P;u) = max_alpha E_mu[u(X, alpha(P(X)))]`,

where `alpha` is restricted to depend only on the classification. The one-step regret of using the inherited state rather than the repaired state is

`R_mu(C,Q*;u) = V_mu(Q*;u) - V_mu(C;u)`.

The supplement proves the stronger statement:

> For every integer `d >= 1` and every real `r >= 0`, there exists a finite target operational system for which the coarsest exact repair satisfies `|Q*|-|C| = d` and the decision regret is exactly `r`.

The construction uses `d+1` target states with distinct declared outputs, which forces the singleton partition to be the coarsest exact repair, while downstream payoffs are chosen so that the repaired state supports state-specific actions and the inherited one-class state cannot.

Status: mathematically closed. Therefore state-count defect is provably a representation-complexity diagnostic, not a universal proxy for management loss.

## 4. Source-relative exact repair — LOGICAL DEPENDENCY MADE EXPLICIT

The paper no longer relies on Paige–Tarjan or Givan–Dean–Greig as black-box proof steps.

The supplement defines the exact refinement operator directly. For current classification `P`, the state signature contains:

- current `P` label;
- current output;
- legality of every declared action; and
- current `P` label of every legal successor.

Starting from `P_0=C`, equality of signatures defines `P_{k+1}`.

The supplement proves self-containedly that:

1. every nontrivial iteration strictly refines, so finite termination follows;
2. a fixed point is exactly an exact operational interface;
3. every exact refinement `E` of `C` refines every `P_k` by induction;
4. therefore the fixed point is the unique coarsest exact refinement of `C`.

Paige–Tarjan (1987) and Givan–Dean–Greig (2003) are now invoked only to establish prior-art status and general algorithmic context: coarsest refinement from a supplied initial partition is not a Paper A invention.

Status: logically closed and novelty boundary explicit.

## Structural publication issue

The reference audit is correct that Paper A should not live or die on a claim of generic mathematical priority. After the additional history/path search, the manuscript now goes further: it does not depend on claiming that any one generic formal ingredient is newly invented.

This leaves a real editorial risk. The paper must convince an ecology audience that the following ecological question is itself worth formalizing:

> When a state classification already embedded in monitoring and management is carried into a structurally changed system, is that state still sufficient for the target intervention, and if not, what must a feasible monitoring design distinguish before the decision interface can be trusted again?

The current best defense is not rhetoric alone. The monitoring-realization theorem supplies an operational output:

- a pass/fail audit of the inherited state;
- explicit obstruction pairs when it fails;
- a necessary-and-sufficient criterion for whether a candidate measurement library can recover the repaired state;
- an impossibility certificate when it cannot; and
- a minimum acquisition-cost formulation when it can.

Jones et al. (2023) begin with ecological states and identify variables that discriminate them. Paper A now formalizes the upstream failure mode in which the inherited states themselves cease to be sufficient for a changed intervention. Canessa et al. (2015) then remains downstream: once a feasible measurement design and uncertain consequences exist, value-of-information analysis can assess whether collecting that information is worth its cost.

## Publication recommendation after proof closure

1. Keep Theoretical Ecology as first target only if the manuscript leads with the ecological state-management problem and monitoring-realization consequence.
2. Do not lead with `coarsest refinement`, `transport defect`, or a mathematical-priority claim.
3. Treat Monitoring realization as the central applied result; conditional information and defect–regret separation support it.
4. Keep the plant–pollinator reversal as a transparent theoretical sensitivity example unless a real system can be added without delaying the paper substantially.
5. Use Ecological Modelling as the immediate fallback if editors judge the contribution too methods/formal-systems oriented for Theoretical Ecology.

The remaining scientific risk is therefore **ecological significance and generality**, not an unresolved proof gap in the four items audited here.
