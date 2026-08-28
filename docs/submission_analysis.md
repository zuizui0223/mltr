# Submission analysis — structural-change flagship paper

## Paper decision

Proceed with one combined CCOC/RACH–MLTR manuscript. The manuscript must be written
as one structural-change theory, not as an open-composition paper followed by a
replacement paper.

## Central question

> When declared ecological replacement histories carry an accepted macro-law to
> one terminal system, when do they preserve one route-independent meaning, and
> what minimum immutable context is forced when their complete carried maps
> disagree?

## Submission-facing result hierarchy

### Headline result — route coherence and history completion

One route-independent inherited terminal law exists exactly when all declared
histories induce the same complete carried terminal map. If their maps differ,
two histories may share one immutable mode exactly when their maps agree. The
minimum mode count is therefore the number of equality classes of complete
carried maps before unique coarsest exact history-aware refinement.

### Supporting result 1 — operational portability

A carried macro partition remains exact exactly while current outputs, legal-action
rows, and target successors remain uniform inside every carried fiber. Nested open
composition and non-nested replacement are two ways the target operational model
can differ from the source.

### Supporting result 2 — local obstruction and unique coarsest exact repair

A newly legal word or target-only action that distinguishes states inside one
carried fiber is a finite obstruction to portability. Monotone
output/legal-row/successor refinement gives the coarsest exact target partition that
preserves every inherited merge still compatible with the target model.

This is the core supporting theorem. Standard refinement supplies the machinery;
source-relative initialization makes it the canonical repair used by the
headline route/history result.

### Supporting result 3 — transport defect

The state-count and bit increases from the inherited source law to the repaired
target law quantify the source-relative transport burden. The accumulating binary
family gives

```text
source macrostates = 2
repaired target macrostates = 2^m + 1
transport defect states = 2^m - 1.
```

This is a sharp witness for the declared growing probe repertoire, not an empirical
growth law.

## Added analysis

`scripts/verify_submission_story.py` consolidates the main finite evidence used in
the manuscript:

- the one-fiber local obstruction;
- the accumulating defect curve for `m = 1, ..., 6`;
- the coherent replacement diamond;
- the incoherent boundary diamond; and
- minimum history augmentation.

The resulting JSON is designed to drive the three main figures and keep manuscript
numbers synchronized with the verified theorem witnesses.

## Figure analyses

### Figure 1 — portability and local repair

Use the local witness:

```text
carried labels:   (0, 0, 1)
repaired labels:  (0, 1, 2)
fiber split:      (2, 1)
transport defect: 1 state
```

The figure should show one target-only action splitting the inherited low-state
fiber.

### Figure 2 — accumulating repair burden

Plot `m` against:

- repaired target states `2^m + 1`;
- defect states `2^m - 1`; and
- defect bits `log2(2^m + 1) - 1`.

The caption must state that the target probe repertoire grows with `m`.

### Figure 3 — coherent and incoherent histories

Show:

- two coherent paths carrying `(0,0,1)` and yielding repair `(0,1,2)`;
- two incoherent paths carrying `(0,1)` and `(1,0)`;
- two required history modes and four history-aware exact states.

## Ecological worked example requirements

Use one plant–pollinator turnover model throughout.

1. Source states describe a functional pollination regime, not species identities.
2. A pollinator guild is lost and another guild colonizes.
3. The declared relation maps source configurations to target configurations.
4. A target-only floral manipulation or exclusion action distinguishes two target
   states that inherited the same source macro label.
5. Relative refinement splits only the affected inherited fiber.
6. Alternative loss–colonization histories either carry the same labels or require
   a finite history context.

The example must instantiate every formal object but must not be presented as an
empirically fitted case study.

## Reviewer-facing novelty boundary

Do not claim novelty for partition refinement, bisimulation, coarse graining, model
transfer, or path dependence in general. Claim the combination of:

- exact portability under declared structural change;
- local operational obstruction;
- unique coarsest source-relative repair;
- transport-defect quantification; and
- route coherence/minimum history completion.

Always retain the phrase **source-relative**. A positive defect does not rule out a
smaller unrelated target abstraction after abandoning inherited semantics.

## Required related-work comparison

The manuscript must explicitly compare its contribution with:

- lumpability and bisimulation/minimization;
- ecological state aggregation and coarse graining;
- transferability and domain adaptation of ecological models;
- ecological novelty and community turnover;
- hysteresis and path dependence.

For every area, identify the closest known object and state precisely which
source-relative minimality or history result is not supplied by that literature.

## Submission gate

The paper is ready for drafting only when:

- one notation covers nested and non-nested structural change;
- the master portability statement is written and proved in that notation;
- the verified submission replay drives all figure values;
- one worked ecological example uses every main definition;
- classical refinement machinery is credited explicitly; and
- no more than four named main results appear in the main text.
