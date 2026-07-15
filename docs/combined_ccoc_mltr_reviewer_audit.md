# Reviewer audit — combined CCOC/RACH + MLTR paper

## Proposed paper

**Exact Ecological Macro-Laws under Structural Change: Portability, Minimal Repair, and Historical Context**

## Editorial verdict

**Potentially strong as one paper, provided the manuscript is rebuilt around one
question and does not read as two repositories stapled together.**

The combined paper is stronger than separate CCOC and MLTR submissions because
CCOC supplies the obstruction and MLTR supplies the constructive response. The
paper should not present open composition and non-nested replacement as two equal
application domains. They are two ways in which the set of operationally relevant
future distinctions changes.

The central question should be:

> When ecological change exposes distinctions hidden by an inherited macro-law,
> can the law remain exact, and if not, what is the uniquely minimal repair that
> preserves its inherited meaning?

## Likely reviewer first impression

### Positive

- The paper addresses a real conceptual gap between coarse ecological description
  and changing community composition.
- It goes beyond transferability diagnostics by constructing a coarsest exact
  source-relative repair.
- The transport defect gives a quantitative object rather than a binary
  portable/nonportable label.
- Replacement histories provide a natural ecological interpretation of path
  dependence.
- Finite exact statements and executable witnesses make assumptions inspectable.

### Immediate concerns

1. **Is this ecology or automata theory with ecological labels?**
2. **Why is exactness the right standard?**
3. **Is the result merely partition refinement or bisimulation minimization?**
4. **Does transport defect measure ecological complexity, or only complexity under
   a chosen source partition and action grammar?**
5. **Are open composition and non-nested replacement genuinely unified, or just
   adjacent sections?**
6. **Where is the ecological example that makes the distinctions operational?**

The manuscript must answer all six before the reviewers ask them.

## Core novelty that is defensible

The novelty is not coarse graining, state aggregation, model transfer, or path
dependence in general. Those are established subjects.

The defensible contribution is the combination of four exact structural claims:

1. an inherited macro-law remains exact only while all newly operational future
   distinctions are uniform inside its fibers;
2. structural change can expose a local fiber split that certifies failure of the
   inherited law;
3. after non-nested replacement, there is a coarsest exact refinement preserving
   every inherited merge still compatible with the target system;
4. the additional macrostates or bits define a source-relative transport defect,
   with route-independent repair under path-label coherence and minimum history
   augmentation otherwise.

The phrase **source-relative** must remain visible. A positive defect does not prove
that no unrelated smaller target abstraction exists.

## Main rejection risks

### Risk 1 — two papers stapled together

CCOC currently asks about widening future composition in a fixed system. MLTR asks
about transporting a law across a non-nested replacement. If the manuscript has one
CCOC half and one MLTR half, the editor may ask for separation.

**Required fix:** introduce one abstract operation: a change from an inherited
operational model to a target operational model. Open composition is a nested
special case; non-nested replacement is the general case. State one master
portability criterion before presenting either witness family.

### Risk 2 — known minimization machinery

A reviewer may say that the coarsest exact refinement is standard partition
refinement.

**Required fix:** do not claim novelty for the algorithm alone. Claim novelty for:

- source-relative repair under a declared replacement relation;
- preservation of inherited ecological semantics;
- the transport-defect quantity;
- path-label coherence and minimum history context;
- the sharp ecological-change witness families.

State explicitly which proof ingredients are classical and which theorem statement
is new.

### Risk 3 — weak ecological grounding

Abstract species turnover language is not enough.

**Required fix:** use one worked ecological model throughout. Recommended example:
a plant–pollinator community before and after loss and replacement of a pollinator
guild. Define finite states, outputs, management actions, the replacement relation,
and one target-only action that splits an inherited macro fiber.

### Risk 4 — exactness appears brittle

Reviewers may prefer approximate or stochastic transfer.

**Required fix:** present exactness as a benchmark and audit standard, not as a
claim that ecosystems are deterministic. Exact results identify the distinctions
that any approximate extension would have to control. Put stochastic and
approximate repair in Discussion, not in the current theorem package.

### Risk 5 — too many results

Open-interface lower bounds, relay sharpness, target repair, defect accumulation,
path coherence, and history augmentation can feel like unrelated theorem inventory.

**Required fix:** four-result hierarchy only.

## Recommended four-result hierarchy

### Result 1 — Operational portability criterion

An inherited macro partition remains exact after structural change iff output,
legal-action rows, and target successors remain uniform inside every carried fiber.

This absorbs the conceptual role of CCOC's exact grammar-aware interface and
MLTR's exact relation transport.

### Result 2 — Local obstruction and minimal repair

A newly legal future word or target-only action that distinguishes two states in a
carried fiber certifies nonportability. Repeated refinement gives the coarsest exact
target partition preserving all surviving inherited merges.

This is the headline theorem.

### Result 3 — Transport defect and sharp accumulation

Define state-count and bit defects relative to the inherited partition. Show a
finite family where independently exposed distinctions accumulate sharply.

This is the quantitative importance result.

### Result 4 — Route coherence and minimum historical completion

If all replacement paths carry the same labels to terminal states, repair is route
independent. Otherwise one immutable history mode per distinct carried label map is
necessary and sufficient.

This closes the theory; it is not a second headline.

## Recommended story

```text
Ecologists reuse coarse state variables after communities change.
        ↓
A coarse law is portable only if change does not expose distinctions it had merged.
        ↓
Open composition and replacement both create such newly operational distinctions.
        ↓
One local split refutes portability.
        ↓
The coarsest source-relative refinement is the unique minimal repair.
        ↓
Transport defect quantifies the repair burden.
        ↓
Multiple histories either agree, or require a minimum retained history context.
```

## Main-text content

- unified structural-change setup;
- one master portability theorem;
- one local split proposition;
- coarsest source-relative repair theorem;
- transport defect and one sharp family;
- path-label coherence theorem;
- short history-completion proposition;
- one worked ecological example;
- three figures.

## Supplement content

- CCOC relay compilation details;
- all legacy theorem registry material;
- full partition-refinement algorithm and implementation proofs;
- additional binary witness families;
- extended history examples;
- all deterministic replay schemas.

## Suggested figures

1. **Inherited law under structural change** — one diagram showing nested open
   composition and non-nested replacement as two target-model changes.
2. **Local split and minimal repair** — an inherited fiber split by a new action,
   followed by the repaired partition and defect.
3. **Coherent and incoherent histories** — replacement diamond with one repair
   versus minimum history slices.

## Acceptance conditions

The paper is likely publishable as a strong theory contribution if it satisfies all
of the following:

- one unified definition of structural change;
- one master portability theorem;
- clear attribution of standard refinement machinery;
- source-relative minimality stated without overclaim;
- one nontrivial ecological worked example;
- a related-work section covering lumpability/bisimulation, ecological model
  transferability, community turnover, and path dependence;
- no more than four named main results.

## Recommendation

**Proceed as a combined flagship manuscript.** Keep the CCOC repository frozen and
use it as proof provenance. Develop the unified manuscript and any bridge notation
in MLTR or a dedicated manuscript repository. Do not reopen CCOC theorem
development.