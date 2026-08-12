# MLTR / Paper A submission audit

## Current publication claim

Paper A is no longer positioned as a new generic refinement theorem. The current claim is an ecological **decision-sufficiency audit of an inherited state classification after declared structural change**.

The publication-facing workflow is:

1. carry an accepted source classification to a target through a declared relation;
2. audit whether target outputs, legal actions, and action-conditioned successors are uniform within inherited target classes;
3. return a local obstruction when the inherited interface fails;
4. apply established coarsest-partition refinement to obtain the least exact additional distinction;
5. translate obstruction pairs into requirements for candidate monitoring variables;
6. distinguish structural defect from conditional information, monitoring cost, and decision regret; and
7. retain immutable replacement-route context only when different declared routes carry incompatible terminal label maps.

## Novelty boundary

Established prior art now explicitly credited:

- arbitrary-initial-partition coarsest refinement: Paige & Tarjan (1987);
- coarsest homogeneous MDP refinement: Givan, Dean & Greig (2003);
- state-abstraction taxonomy: Li, Walsh & Littman (2006);
- source-to-target state-abstraction transfer: Walsh, Li & Littman (2006);
- mappings between distinct decision processes: Ravindran & Barto (2003);
- targeted monitoring from state-and-transition models: Jones et al. (2023);
- ecological value of information: Canessa et al. (2015);
- history-sensitive formal equivalence: Montanari & Pistore (1997) and the wider history-preserving bisimulation literature.

The manuscript must not claim these individual constructions as new.

The defensible Paper A contribution is the ecological organization of the audit, repair, monitoring implication, and route-context logic. The route-coherence/minimum-carried-map-context result remains the only component with a plausible scoped mathematical-novelty claim after the current review.

## Reproducible results

The submission replay now includes:

- inherited labels `(0, 0, 1)` and least exact repair `(0, 1, 2)`;
- structural defect of one macrostate in the local witness;
- uniform-distribution conditional repair information of `2/3` bit in that witness;
- sharp structural family `|Q*| = 2^m + 1`;
- illustrative plant–pollinator decision layer with `B=1`, `c_A=0.20`, `c_B=0.35`, `p_A=0.25`, `p_B=0.80`;
- pooled inherited choice `A`, repaired choice `B`, and one-step regret `0.40`;
- decision-reversal boundary `p_B - p_A > 0.15` for that cost/benefit setting;
- route-coherent and route-incoherent witnesses, with two carried-map contexts in the incoherent case.

The probabilities and costs are illustrative sensitivity values, not empirical estimates.

## Figure map

1. ecological audit workflow: structural change -> inherited class -> target intervention -> local failure -> least exact distinction -> monitoring implication;
2. structural repair-complexity witness family;
3. route coherence and minimum carried-map context;
4. probabilistic decision-reversal region for the illustrative plant–pollinator example.

## Current stop rule for theorem expansion

Do not add more general mathematics by default. Add a theorem only if it:

- closes a specific logical gap in the decision-sufficiency story;
- is required to make the monitoring interpretation correct;
- survives a direct prior-art challenge; or
- changes the ecological conclusion.

Otherwise prioritize manuscript readability, figure inspection, bibliography verification, and submission metadata.

## Remaining submission blockers

Scientific/technical:

- verify the current reframed HEAD with CI, transport reproducibility, and manuscript build;
- visually inspect the rebuilt four-figure PDF;
- check that the abstract remains within the journal word limit and that all citation keys resolve;
- decide whether the conditional-information and monitoring-realization propositions remain in the main text or move to the supplement.

Author-supplied:

- author names and order;
- affiliations and corresponding-author email;
- ORCID identifiers if used;
- funding, acknowledgments, competing interests, and author contributions;
- final archive/DOI for code and replay artifacts;
- final Springer template/caption decision;
- suggested reviewers if requested by the submission system.

## Current verdict

The repository is in manuscript-completion mode, not theorem-expansion mode. If the current Actions run is green and the rebuilt PDF is visually clean, the next scientific decision is supervisor review of the ecological framing rather than further formal development.
