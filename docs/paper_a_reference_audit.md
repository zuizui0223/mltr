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

## History-sensitive formal theories

- Montanari and Pistore (1997): minimal transition systems for history-preserving bisimulation, representing a broad formal literature in which past causal structure can be retained in behavioral equivalence.

**Boundary.** The words "history" and "path" are not novel. Paper A's history result concerns a different object: several externally declared replacement routes can carry different source label maps to the same terminal system. The manuscript should claim only the specific route-independence criterion and minimum number of immutable carried-map contexts. We found no direct counterpart for that exact construction in the sources reviewed, but this is a scoped literature finding, not proof of absence.

## What Paper A may claim

The safest contribution statement is:

1. formulate reuse of an inherited ecological state classification as a **decision-sufficiency audit** under declared structural change and a target action repertoire;
2. use established refinement machinery to return the least state distinction required once the inherited interface fails;
3. translate separating witnesses into requirements for candidate monitoring variables;
4. separate structural repair complexity from distribution-sensitive information, monitoring cost, and decision regret; and
5. characterize when multiple declared replacement routes admit one route-independent carried interface and when immutable history context is necessary.

Only item 5 currently has a plausible claim to mathematical novelty. Items 1--4 are best presented as a new ecological organization and interpretation of established formal and decision-theoretic ingredients.

## Guardrails

- Never call the coarsest-refinement construction a new theorem without immediately crediting Paige--Tarjan and Givan--Dean--Greig.
- Never claim novelty merely from source-to-target abstraction transfer; cite Walsh--Li--Littman (2006).
- Treat the transport-defect state count as a **structural diagnostic**, not an ecological effect size, monetary cost, information measure, or proxy for decision regret.
- If a target-state distribution is supplied, conditional repair information may be reported separately as H(Q* | C).
- Candidate monitoring variables and their costs define a separate minimum realization problem; decision values define a separate regret/VoI problem.
- The plant--pollinator case is an illustrative finite management example. Any probabilities or costs introduced for sensitivity analysis must be labeled illustrative, not empirical.
- History-preserving bisimulation and related causal-history formalisms exist; Paper A's scoped claim is about externally declared replacement routes and carried terminal label maps, not the invention of history-sensitive equivalence.
