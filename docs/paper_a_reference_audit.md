# Paper A reference audit

This audit maps the manuscript's boundary claims to verified prior work. It is deliberately adversarial: when a close formal or ecological precedent exists, the manuscript must credit it and move novelty elsewhere.

## Established formal machinery

- Kemeny and Snell (1960): finite-chain lumpability.
- Feret et al. (2012): lumpability abstractions for rule-based systems.
- Milner (1989) and Larsen and Skou (1991): behavioral and probabilistic bisimulation baselines.
- Paige and Tarjan (1987): relational coarsest partition from an arbitrary initial partition.
- Givan, Dean and Greig (2003): coarsest homogeneous refinement of any MDP partition in a stochastic setting that contains the deterministic case used here.
- Li, Walsh and Littman (2006): taxonomy of MDP state abstractions by what they preserve.

**Consequence.** The coarsest exact refinement of a carried partition is established prior art. Paper A must not present the refinement algorithm, its finite termination, or its coarseness/uniqueness as a new general result.

## Transfer of abstractions across decision processes

- Ravindran and Barto (2003): homomorphisms between distinct semi-Markov decision processes.
- Walsh, Li and Littman (2006), *Transferring State Abstractions Between MDPs*: explicit treatment and an algorithm for transferring state abstractions from source MDPs to target MDPs.

**Correction to PR #30's initial novelty boundary.** It is not enough to say that the present framework is new because a source abstraction is moved to a target system. Abstraction transfer itself is prior art. The defensible distinction is narrower: an already accepted ecological state classification is carried through a declared ecological correspondence and then **audited for target decision sufficiency**; failure is treated as the scientific object rather than assumed away or resolved solely for computational speed.

## Ecological state models and targeted monitoring

- Jones et al. (2023), *Ecological Applications*: uses a pre-existing state-and-transition model, validates state classifications with field data, and identifies a reduced set of variables and thresholds for targeted monitoring of transitions.
- Holling (1978) and Walters (1986): adaptive-management foundations.
- Holling (1973) and Scheffer et al. (2001): resilience/regime-state background.

**Boundary.** Paper A does not claim that selecting a small set of monitoring indicators is new. Its proposed ecological role is upstream: first test whether an inherited state classification remains sufficient for the changed action set; only when it fails, use the separating pairs to define what distinctions a monitoring design must be able to resolve.

## Decision analysis and value of information

- Canessa et al. (2015): value-of-information analysis for deciding whether additional ecological information is worth collecting given objectives, actions, uncertainty, and consequences.

**Boundary.** Paper A does not replace VoI. Its exact audit is a structural precondition: it identifies distinctions that the inherited state representation suppresses. VoI can then evaluate whether measuring those distinctions is worth the cost under uncertainty.

## Ecological model transferability

- Yates et al. (2018): expert assessment establishing transferability as a major ecological prediction problem.

Use Yates et al. to establish importance, not to claim that Paper A solves the twelve challenges in that review. Those challenges are largely statistical; the present failure can occur even with perfect knowledge of the declared source and target systems.

## History-sensitive and path-consistency formal theories

- Montanari and Pistore (1997): minimal transition systems for history-preserving bisimulation, representing a broad formal literature in which past causal structure can be retained in behavioral equivalence.
- Additional adversarial searches found broad literatures on history-sensitive equivalence, commutativity conditions, refinement, and path-based semantics. None of the sources reviewed gave the exact ecological object used here -- externally declared replacement routes carrying source label maps to a common terminal system -- but lack of a direct match is not a basis for a strong mathematical-novelty claim.

**Boundary.** The words "history," "path," "coherence," and "minimum context" are not novel. The route criterion in Paper A is a scoped formal closure statement: one route-independent carried interface exists when the complete terminal carried maps agree, and incompatible maps require distinct immutable contexts before exact refinement.

## What Paper A may claim

The safest contribution statement is:

1. formulate reuse of an inherited ecological state classification as a **decision-sufficiency audit** under declared structural change and a target action repertoire;
2. use established refinement machinery to return the least state distinction required once the inherited interface fails;
3. translate separating witnesses into requirements for candidate monitoring variables;
4. separate structural repair complexity from distribution-sensitive information, monitoring cost, and decision regret; and
5. integrate route consistency into the same audit so that historical context is retained only when alternative declared replacement routes assign incompatible operational meanings.

**Do not sell any one of these as a standalone new generic mathematical theorem.** The defensible novelty is the ecological problem formulation and the integration of established formal ingredients into a management-state audit with explicit monitoring and decision consequences. Item 5 remains a useful scoped formal result, but its proof is elementary enough that the paper should not depend on a claim of mathematical priority for publication value.

## Source-verification notes added 2026-08-12

- Walsh--Li--Littman (2006) was verified from the author's publication page and the workshop paper itself; its abstract explicitly states that it provides a general treatment and algorithm for transferring state abstractions in MDPs.
- Jones et al. (2023) was verified from the publisher page; it explicitly develops targeted monitoring from a pre-existing state-and-transition model by selecting variables that distinguish states and thresholds.
- Canessa et al. (2015) was verified from the publisher page; it defines value of information as the expected improvement in management outcomes from additional information and emphasizes dependence on actions, objectives, and information quality.
- The history/path search found a substantial history-preserving and path-sensitive formal literature, including Montanari--Pistore (1997), as well as work on commutativity/refinement. This is why the manuscript scopes the route result narrowly and does not advertise it as the primary novelty.

## Guardrails

- Never call the coarsest-refinement construction a new theorem without immediately crediting Paige--Tarjan and Givan--Dean--Greig.
- Never claim novelty merely from source-to-target abstraction transfer; cite Walsh--Li--Littman (2006).
- Treat the transport-defect state count as a **structural diagnostic**, not an ecological effect size, monetary cost, information measure, or proxy for decision regret.
- If a target-state distribution is supplied, conditional repair information may be reported separately as H(Q* | C).
- Candidate monitoring variables and their costs define a separate minimum realization problem; decision values define a separate regret/VoI problem.
- The plant--pollinator case is an illustrative finite management example. Any probabilities or costs introduced for sensitivity analysis must be labeled illustrative, not empirical.
- History-preserving bisimulation and related causal-history formalisms exist; Paper A's scoped route result is about externally declared replacement routes and carried terminal label maps, not the invention of history-sensitive equivalence.
- The cover letter and abstract should lead with the ecological management-state problem, not with claims of a new formal algorithm or new general mathematics.
