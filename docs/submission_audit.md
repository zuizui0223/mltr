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

Established prior art explicitly credited:

- arbitrary-initial-partition coarsest refinement: Paige & Tarjan (1987);
- coarsest homogeneous MDP refinement: Givan, Dean & Greig (2003);
- state-abstraction taxonomy: Li, Walsh & Littman (2006);
- source-to-target state-abstraction transfer: Walsh, Li & Littman (2006);
- mappings between distinct decision processes: Ravindran & Barto (2003);
- targeted monitoring from state-and-transition models: Jones et al. (2023);
- ecological value of information: Canessa et al. (2015);
- history-sensitive formal equivalence and path-sensitive formalisms: Montanari & Pistore (1997) and adjacent literatures.

The manuscript must not claim these individual constructions as new.

The defensible Paper A novelty is **ecological rather than algorithmic or general-mathematical**: it organizes existing formal ingredients around a management-state audit, makes failure of an inherited classification the scientific object, translates exact separating pairs into monitoring requirements, and keeps representation complexity distinct from decision consequence. Route coherence/minimum carried-map context is retained as a scoped formal closure result, but the paper does not depend on a claim of mathematical priority for it.

## Reproducible results

The submission replay includes:

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

## Verification completed 2026-08-12

Scientific/build commit `38e0353e72743841412cd7465982d018e333bae0`:

- CI: pass;
- Transport-core reproducibility: pass;
- Manuscript build: pass;
- main and supplement compile;
- four SVG figures are generated and converted;
- no undefined citations in the successful build;
- abstract: 226 words, within the journal's 150--250-word range;
- 12-page main PDF rendered and inspected page by page: no clipping, overlap, broken glyphs, or missing figures.

The earlier manuscript failure was traced to a hard-coded three-figure conversion loop after Figure 4 was added. The workflow now derives the referenced SVG list from the manuscript, preventing recurrence of that failure mode.

Minor generic-LaTeX box warnings remain but are not visually damaging; they can be handled during final Springer-template migration.

## Current stop rule for theorem expansion

Do not add more general mathematics by default. Add formal development only if it:

- closes a specific logical gap in the decision-sufficiency story;
- is required to make the monitoring interpretation correct;
- survives a direct prior-art challenge; or
- changes the ecological conclusion.

Otherwise prioritize manuscript readability, supervisor review, bibliography discipline, and submission metadata.

## Remaining submission blockers

Scientific/editorial:

- supervisor review of the ecological framing;
- decide whether the conditional-information and monitoring-realization propositions remain in the main text or move to the supplement;
- final Springer template/caption styling and removal of minor box warnings.

Author-supplied:

- author names and order;
- affiliations and corresponding-author email;
- ORCID identifiers if used;
- funding, acknowledgments, competing interests, and author contributions;
- final archive/DOI for code and replay artifacts;
- Data Availability wording tied to that archive;
- suggested reviewers if requested by the submission system.

## Current verdict

The repository is in manuscript-completion mode, not theorem-expansion mode. The current manuscript is technically ready for supervisor scientific review. Formal journal submission should wait for author metadata, declarations, archival DOI/Data Availability, and final journal-template decisions.
