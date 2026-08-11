# Paper A reference audit

This audit maps each boundary claim in the main manuscript to a verified reference before citation commands are inserted. It is intentionally conservative: references are included only where bibliographic metadata and the claimed scope match.

## Fixed-system aggregation and lumpability

- Kemeny and Snell (1960), *Finite Markov Chains*: classical finite-chain lumpability baseline.
- Feret et al. (2012), “Lumpability Abstractions of Rule-based Systems”: biological rule-based systems, weak lumpability, and Markov bisimulation.

Use these for claims that lumpability concerns exact aggregation of a specified stochastic or dynamical system. Do not cite them as solving source-relative transport under structural replacement.

## Bisimulation and partition refinement

- Milner (1989), *Communication and Concurrency*: standard process-theoretic treatment of bisimulation.
- Larsen and Skou (1991), “Bisimulation through Probabilistic Testing”: probabilistic bisimulation baseline.
- Paige and Tarjan (1987), “Three Partition Refinement Algorithms”: the relational coarsest partition problem, **posed for an arbitrary initial partition**.
- Givan, Dean and Greig (2003), “Equivalence Notions and Model Minimization in Markov Decision Processes”: **the coarsest homogeneous refinement of any partition of the state space**, in a stochastic setting strictly containing Paper A's deterministic one.
- Li, Walsh and Littman (2006), “Towards a Unified Theory of State Abstraction for MDPs”: taxonomy of abstractions by what each preserves.
- Ravindran and Barto (2003), “SMDP Homomorphisms”: maps between distinct decision processes.

**Correction to an earlier version of this audit.** This document previously instructed that the Paper A claim be “restricted to initialization by carried source labels and source-relative minimality.” That restriction does not establish novelty, because refinement from an arbitrary initial partition is exactly what Paige–Tarjan and Givan–Dean–Greig solve. The unique coarsest refinement of a given partition is **established prior art and must be cited as such**, not credited as machinery while the theorem is presented as new.

The defensible contribution is therefore relocated to three places:

1. the construction of the initial partition by transporting an accepted source law across a declared relation between non-coinciding state spaces (contrast with homomorphisms, where dynamics preservation is assumed rather than tested);
2. the reading of the inherited-to-repaired difference as an ecological quantity; and
3. path-label coherence and minimum history completion, for which no direct counterpart in the abstraction literature has been identified.

Item 3 is the only headline result with a plausible claim to mathematical novelty and should carry corresponding weight in the manuscript.

## Ecological model transferability

- Yates et al. (2018), “Outstanding Challenges in the Transferability of Ecological Models”, *TREE* 33(10):790–802: expert assessment establishing transferability as a recognized open problem in ecology.

Use this to establish **importance**, not gap. The twelve listed challenges are predominantly statistical (predictive accuracy under novel conditions, data quality, model complexity, uncertainty quantification). Paper A addresses a structural failure that is not among them, and the manuscript must say so explicitly rather than implying that it answers the listed challenges.

## Transportability

- Pearl and Bareinboim (2014), “External Validity: From Do-Calculus to Transportability Across Populations”: causal transportability between populations.

Use this for the contrast between causal-effect transport and exact operational closure. Do not imply that Paper A estimates causal effects or identifies source–target relations.

## Resilience and regime shifts

- Holling (1973), “Resilience and Stability of Ecological Systems”: ecological resilience baseline.
- Scheffer et al. (2001), “Catastrophic Shifts in Ecosystems”: abrupt ecosystem shifts and alternative regimes.

Use these for the ecological role of resilience classes, thresholds, and regime labels. Paper A audits whether such labels remain operationally sufficient; it does not redefine resilience or derive tipping thresholds.

## Adaptive management

- Holling (ed., 1978), *Adaptive Environmental Assessment and Management*.
- Walters (1986), *Adaptive Management of Renewable Resources*.

Use these for iterative decision-making, learning through management, and changing policies under uncertainty. Paper A audits the state representation supplied to those procedures; it does not optimize policies or perform Bayesian learning.

## Citation insertion targets

1. Introduction paragraph naming neighboring literatures.
2. “Coarse graining and lumpability” subsection.
3. “Bisimulation, abstraction, and partition refinement” subsection.
4. “Transportability and model transfer” subsection.
5. “Resilience, regime shifts, and ecological state classifications” subsection.
6. “Adaptive management” subsection.
7. Discussion statements about regime history and monitoring design only where the reference directly supports the ecological background claim.

## Guardrails

- The coarsest refinement of a carried partition **is** established prior art and must be cited to Paige–Tarjan and Givan–Dean–Greig at every point where the repair theorem is stated. Do not present it as a new theorem, and do not defend it by describing refinement as "machinery" while claiming the constrained object is new.
- Novelty claims are confined to the transport construction, the ecological reading of the defect, and path coherence / minimum history completion.
- Yates et al. supports importance only. Do not cite it as evidence that the structural question is unsolved.
- “Transport defect” remains a definition tied to the unique repair, not a literature-backed universal ecological effect size.
- The plant–pollinator management reversal remains a finite worked example, not an empirical claim about a particular species or restoration programme.
