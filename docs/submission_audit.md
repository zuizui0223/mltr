# MLTR / Paper A submission audit

## Current publication claim

Paper A is no longer positioned as a new generic refinement theorem. The current claim is an ecological **decision-sufficiency audit of an inherited state classification after declared structural change, with exact monitoring repair as the main applied output**.

The publication-facing workflow is:

1. carry an accepted source classification to a target through a declared relation;
2. audit whether target outputs, legal actions, and action-conditioned successors are uniform within inherited target classes;
3. return a local obstruction when the inherited interface fails;
4. apply established coarsest-partition refinement to obtain the least exact additional distinction;
5. define the obstruction-pair set that any repaired monitoring system must separate;
6. test whether a supplied candidate measurement library can exactly reconstruct the repaired state;
7. return either an explicit uncovered-pair impossibility certificate or, when feasible, a minimum-cost exact measurement-selection problem;
8. keep structural defect, conditional information, monitoring cost, and decision regret distinct; and
9. retain immutable replacement-route context only when different declared routes carry incompatible terminal label maps.

## Novelty boundary

Established prior art explicitly credited:

- arbitrary-initial-partition coarsest refinement: Paige & Tarjan (1987);
- coarsest homogeneous MDP refinement: Givan, Dean & Greig (2003);
- state-abstraction taxonomy: Li, Walsh & Littman (2006);
- source-to-target state-abstraction transfer: Walsh, Li & Littman (2006);
- mappings between distinct decision processes: Ravindran & Barto (2003);
- targeted monitoring from state-and-transition models: Jones et al. (2023);
- ecological value of information: Canessa et al. (2015);
- history-sensitive formal equivalence and path-sensitive formalisms: Montanari & Pistore (1997) and adjacent literatures;
- generic weighted set cover / test cover.

The manuscript must not claim these individual constructions as new.

The defensible Paper A novelty is **ecological and integrative rather than algorithmic**: it makes failure of an inherited management-state definition the scientific object, produces the exact state pairs that monitoring must distinguish, certifies whether a supplied measurement library is sufficient or insufficient, and separates representation complexity from management consequence.

## Proof closure

The four previously under-justified results are now formally closed in the supplement.

### Minimum conditional repair information

Every exact target refinement of the inherited state refines the coarsest exact repair, so the repaired label is a deterministic function of any exact finer label. The conditional-entropy chain rule gives the minimum-information inequality and the classwise support bound.

### Monitoring realization

A measurement set `S` realizes the repaired state exactly when a decoder exists:

`Q*(x) = d_S(C(x), z_S(x))`.

This is proved equivalent to separation of every obstruction pair. It yields:

- a necessary-and-sufficient feasibility test for a supplied candidate library;
- an uncovered obstruction pair as an impossibility certificate;
- weighted set cover as the minimum-cost exact realization when costs are additive.

### No universal defect-regret ordering

For every integer `d >= 1` and every `r >= 0`, a finite exact-repair decision problem can be constructed with state-count defect `d` and regret `r`. State-count defect therefore cannot provide a universal upper bound, positive lower bound, or monotone ranking of management loss.

### Source-relative exact repair

The supplement gives a self-contained finite specialization proof: monotone splitting, finite termination, exactness of the fixed point, and induction establishing unique coarseness. Paige--Tarjan and Givan--Dean--Greig are citations of prior-art status and general context rather than hidden proof dependencies.

## Reproducible results — schema 3

The submission replay now includes:

- inherited labels `(0, 0, 1)` and least exact repair `(0, 1, 2)`;
- the local obstruction pair `(0, 1)`;
- an illustrative candidate measurement library in which `substitute_response_capacity` separates the obstruction whereas the abundance and soil-condition proxies do not;
- full-library monitoring feasibility;
- minimum exact acquisition cost `1.0` for the separating illustrative measurement;
- an explicitly insufficient two-variable sublibrary whose uncovered pair `(0, 1)` certifies exact monitoring infeasibility;
- structural defect of one macrostate in the local witness;
- uniform-distribution conditional repair information of `2/3` bit;
- sharp structural family `|Q*| = 2^m + 1`;
- illustrative plant--pollinator decision layer with `B=1`, `c_A=0.20`, `c_B=0.35`, `p_A=0.25`, `p_B=0.80`;
- pooled inherited choice `A`, repaired choice `B`, and one-step regret `0.40`;
- decision-reversal boundary `p_B - p_A > 0.15` for that cost/benefit setting;
- route-coherent and route-incoherent witnesses, with two carried-map contexts in the incoherent case.

All measurement values/costs and decision probabilities/costs in these small replay examples are illustrative constants, not empirical estimates.

## Figure and table map

1. Figure 1: structural change -> inherited state -> target intervention -> local obstruction -> least exact distinction -> candidate measurement library -> feasible or infeasible exact monitoring repair;
2. main-text audit table: inherited state passes / repair measurable / repair not measurable with the current library;
3. Figure 4: probabilistic restoration-priority reversal;
4. Figure 2: structural repair-complexity witness family, explicitly secondary;
5. Figure 3: route coherence and minimum carried-map context, explicitly secondary.

## Current manuscript architecture

Working title:

**Auditing Ecological State Classifications after Structural Change: Decision Sufficiency and Monitoring Repair**

Main story:

`inherited management state -> structural audit -> obstruction -> monitoring feasibility/impossibility -> minimum monitoring cost -> decision consequence`

Secondary results on conditional information, structural defect, defect-regret separation, and historical route context remain in the paper but no longer compete with monitoring realization for the headline.

## Verification status

Monitoring-centered scientific/replay revision `278ba502a5e39e6e522dbc867eaaf2bbdcb5566a`:

- CI: pass;
- Transport-core reproducibility: pass;
- Manuscript build: pass;
- main manuscript: 13 pages;
- supplementary manuscript: 13 pages;
- four SVG figures generated and converted;
- Figure 1 visually inspected with readable feasible/infeasible monitoring branches;
- main and supplement rendered page by page: no clipping, overlap, broken glyphs, or missing figures/proof content;
- main abstract: 221 words, within the journal's 150--250-word range.

A subsequent formatting-only edit shortens one supplementary prose line that had produced a 9.2-pt overfull box; it does not change scientific content.

## Current stop rule for theorem expansion

Do not add more general mathematics by default. Add formal development only if it:

- closes a specific logical gap in the audit-to-monitoring story;
- is required to make the monitoring interpretation correct;
- survives a direct prior-art challenge; or
- changes the ecological conclusion.

Otherwise prioritize supervisor review, empirical interpretability, bibliography discipline, and submission metadata.

## Remaining scientific risk

The unresolved risk is no longer proof closure. It is whether the ecological community recognizes the following as sufficiently general and important for Theoretical Ecology:

> an inherited ecological state can remain interpretable while becoming insufficient for a changed management intervention; when it fails, the obstruction defines an exact, falsifiable requirement for monitoring redesign rather than merely a request for more data.

The relationship to adjacent ecology is deliberately sequential:

- Jones et al. (2023): downstream selection and validation of practical variables/thresholds once the state distinctions to detect are specified;
- Canessa et al. (2015): downstream value-of-information analysis once uncertainty, acquisition costs, and management consequences are specified.

## Remaining submission blockers

Scientific/editorial:

- supervisor judgment of ecological generality/significance;
- decision whether the theoretical example is sufficient or one empirical application should be added before submission;
- final Springer template/caption styling.

Author-supplied:

- author names and order;
- affiliations and corresponding-author email;
- ORCID identifiers if used;
- funding, acknowledgments, competing interests, and author contributions;
- final archive/DOI for code and replay artifacts;
- Data Availability wording tied to that archive;
- suggested reviewers if requested by the submission system.

## Current verdict

The repository is in manuscript-completion mode, not theorem-expansion mode. The mathematical gaps identified in review have been closed, and the manuscript has been reorganized around the strongest ecological output: **audit failure -> exact monitoring feasibility/impossibility -> minimum-cost monitoring repair -> management consequence**.
