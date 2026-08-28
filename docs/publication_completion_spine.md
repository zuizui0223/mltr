# Paper A publication-completion spine

## Fixed identity

**Working title:** Do Ecological Macro-Laws Survive Structural Replacement? Route Coherence and Minimal Historical Completion

**Repository scope:** MLTR is the active manuscript and reproducibility repository for **source-relative transport of one inherited macro-law**. CCOC is an adjacent theorem repository for a different cross-grammar lower-bound problem and is not an MLTR result source except for clearly attributed shared substrate or motivation.

**Central question:** Given one accepted ecological macro-law and several declared structural-replacement histories, when do they preserve one terminal meaning, and what is the necessary-and-sufficient historical context when their complete carried maps disagree?

No new theorem family should be added during submission preparation.

## Claim firewall against CCOC

MLTR fixes \(q_S\) and solves

\[
\min_{q_T\text{ exact},\;q_T\succeq \operatorname{carry}(q_S)} |q_T|.
\]

CCOC instead compares independently optimized closed-grammar minima with the minimum exact interface under a jointly open grammar. Its cross-grammar lower bound and bounded-local sharpness family are **not** part of MLTR's four-result hierarchy.

A target-only action or newly legal word may be used in MLTR because it can expose a split inside one inherited fiber. That is a transport/repair instance, not a claim that open composition itself is subsumed by MLTR.

See `docs/ccoc_mltr_claim_firewall_2026-08-16.md`.

## Publication abstract

An ecological macro-law accepted at one stage need not retain one route-independent meaning after structural replacement. We formulate finite operational models in which declared replacement histories carry a source law to a terminal system. A single carried terminal law exists exactly when the complete carried terminal label maps agree across histories. When they disagree, histories can share an immutable mode exactly when their complete carried maps are equal; consequently, one mode per distinct map is necessary and sufficient to preserve all declared inherited meanings. Relative exact refinement on these history slices then yields the unique coarsest exact history-aware interface. Exact portability, local failure witnesses, and source-relative fixed-point repair supply the supporting audit for each route. Standard exactness and partition refinement are therefore infrastructure, while the central result locates the precise boundary between route-free reuse and mandatory historical context.

## Introduction spine

### Problem

Ecological macrostates are routinely transported across altered communities and management regimes. A guild label, occupancy class, resilience category, or functional state may be exact for the original system but cease to be exact after species turnover, interaction rewiring, or expansion of the intervention repertoire.

### Gap

Coarse graining, lumpability, abstraction, and bisimulation provide mature languages for state aggregation. Transportability addresses whether conclusions transfer across environments. These literatures do not by themselves answer MLTR's constrained question: given an already accepted ecological macro-law and a declared structural change, when does that exact law remain valid, and if it does not, what is the unique coarsest exact repair constrained to preserve its source semantics?

Do not broaden this gap statement into CCOC's different question about whether all closed futures can be individually easy to compress while the jointly open future requires a large minimum interface.

### Contribution hierarchy

1. **Route Coherence and Minimum History Completion (headline).** Complete carried terminal maps determine whether one inherited terminal law exists. Histories share a mode exactly when those maps agree; one mode per equality class is necessary and sufficient when they do not.
2. **Operational Portability Criterion (infrastructure).** The carried target partition is exact if and only if current outputs, legal-action rows, and action successors factor through the inherited labels.
3. **Local Obstruction and Unique Coarsest Source-relative Repair (infrastructure).** A target-legal action or future word can witness failure inside one carried fiber; iterative operational refinement returns the unique coarsest exact partition refining the inherited labels.
4. **Transport Defect (quantitative witness).** The source-relative repair burden is quantified by the increase in repaired state count or description length relative to the inherited law.

### Ecological conclusion

The framework distinguishes scientifically different outcomes of model transfer: the inherited variable may remain valid, or structural change may expose an ecologically consequential distinction that must be added. The repair theorem identifies the least such addition under the declared operational model.

## Results spine

### Headline Result — History coherence and minimum completion

Present path coherence as the graph-level characterization and minimum history completion as its canonical failure repair. The minimum number of modes is the number of distinct carried terminal maps.

**Reviewer-facing interpretation:** This does not infer historical pathways or ecological memory from data. It characterizes the exact context needed when several declared histories induce different target semantics.

**Ecological payoff:** It determines when one management model is valid regardless of replacement route and when path identity must remain part of the predictive state.

### Supporting Result 1 — Operational portability

State one source-relative theorem only. Exact interface conditions are standard/foundational ingredients; the MLTR claim begins once source semantics are carried through a declared relation and tested in the target.

**Reviewer-facing interpretation:** This is not merely a homomorphism restatement because the transported labels are inherited through a possibly non-nested state relation and are tested against the target's legal operational grammar.

**Ecological payoff:** It gives an exact diagnostic for whether a macro-variable learned before structural change can still support every declared target prediction and intervention.

### Supporting Result 2 — Local obstruction and unique coarsest exact repair

Treat the local witness and fixed-point refinement as one theorem package. The theorem must visibly contain existence, exactness, coarseness, and uniqueness relative to the carried labels.

**Reviewer-facing interpretation:** Standard partition refinement is credited as machinery. Novelty lies in the source-relative transport problem and the unique repair interpretation, not in a new generic refinement algorithm or a CCOC-style open-interface lower bound.

**Ecological payoff:** When transfer fails, the result identifies the minimum additional ecological distinction required rather than merely rejecting the old classification.

### Supporting Result 3 — Transport defect

Define

- `Delta_count = |Q_target_repaired| - |Q_source|`,
- `Delta_bits = log2 |Q_target_repaired| - log2 |Q_source|`.

Present any accumulating finite family only as a source-relative repair witness. Do not use CCOC's independently optimized closed/open interface gap as the definition or proof of MLTR transport defect.

**Ecological payoff:** Defect separates mild structural change, which needs one extra state, from change that destroys most of the inherited compression.

## Worked ecological example

Use one finite plant–pollinator guild example throughout.

1. The source system has an exact functional macro-law that merges two microstates with the same output and source-legal future.
2. Structural turnover carries those labels to a target community.
3. A target-only intervention, such as pollinator exclusion or competitor removal, gives different successors within one inherited fiber.
4. The local obstruction rejects unchanged portability.
5. Relative refinement splits exactly that fiber and no other.
6. Transport defect reports the added state and bit burden.
7. Two replacement paths are compared: one coherent pair sharing the repair and one incoherent pair requiring two history modes.

Every main definition and result must appear in this single example. Avoid a second unrelated example in the main text.

## Discussion spine

### What is new

The paper supplies an exact source-relative route boundary for one inherited ecological macro-law under structural replacement: equality of complete carried terminal maps gives one route-independent law, while their equality classes give the necessary-and-sufficient immutable history modes when route independence fails. Portability, unique coarsest exact repair, and defect are the supporting audit.

### What is not claimed

- no inference of the source–target relation from field data;
- no empirical claim that a chosen ecological variable is exact;
- no stochastic or approximate theorem beyond the declared finite deterministic setting;
- no claim that partition refinement, bisimulation, or lumpability are new;
- no claim that historical paths are identifiable from terminal observations;
- no claim that MLTR proves CCOC's closed-vs-open minimum-interface lower bound.

### Relation to adjacent literatures and CCOC

- **Coarse graining and lumpability:** provide exact aggregation criteria within a fixed system; this paper studies inherited aggregation across declared structural change.
- **Abstraction and bisimulation:** provide behavioral equivalence machinery; this paper adds source-relative transport, unique constrained repair, and repair burden.
- **Transportability:** studies transfer of causal or statistical conclusions; this paper gives an operational state-space criterion and exact repair for transported macro-laws.
- **Ecological resilience and regime shifts:** motivate structural change but do not generally provide a unique minimal refinement of an inherited predictive variable.
- **CCOC:** asks whether separately optimized closed-grammar interfaces can all be small while the jointly open grammar forces a large minimum exact interface. That quantifier structure and lower bound remain a separate theorem story.

### Limitations and next step

Approximate, stochastic, and data-estimated variants are important but belong to future work unless supported by complete theorems. They should not be sketched as additional contribution families in the current manuscript.

## Figure plan

1. **Conceptual pipeline:** declared replacement histories → compare complete carried terminal maps → one route-independent law or minimum history modes → unique coarsest exact repair.
2. **Local obstruction and repair:** one inherited fiber split by a target-only action, with the unique coarsest repaired partition.
3. **Transport defect:** source-relative repaired state count and defect against exposed inherited distinctions.
4. **History coherence:** coherent routes sharing one repair versus incoherent routes requiring minimum history modes.

The ecological worked example should supply labels and interpretation for Figures 1, 2, and 4 rather than appearing as a disconnected fifth conceptual figure.

## Reviewer audit

### Criticism: “This is standard bisimulation or partition refinement.”

**Answer:** Credit the standard fixed-point machinery explicitly. The contribution is the characterization of an inherited source-relative partition under non-nested structural transport, the local operational failure witness, the unique constrained repair, and its transport/history consequences.

### Criticism: “Isn't this just CCOC under different notation?”

**Answer:** No. CCOC has no fixed inherited source partition in its headline optimization; each closed grammar may choose a different optimal exact interface before comparison with the jointly open minimum. MLTR conditions all admissible target repairs on one carried source semantics. The two theorem statements have different quantifier order and different outputs.

### Criticism: “The framework is too abstract to be ecological.”

**Answer:** The worked example must show a concrete conclusion unavailable before the theorem: whether an existing functional state remains usable after turnover and, if not, exactly which ecological distinction must be retained.

### Criticism: “The defect is a descriptive statistic rather than a theorem.”

**Answer:** Present defect as a definition supported by the minimal-repair theorem and source-relative witness families. Do not inflate it into an independent theorem claim.

### Criticism: “History completion merely copies systems by path.”

**Answer:** The nontrivial statement is minimality: paths may share a mode exactly when their complete carried terminal maps agree, so the number of distinct maps is necessary and sufficient.

### Criticism: “Exact finite assumptions are unrealistic.”

**Answer:** Position exactness as a benchmark that isolates structural failure from statistical estimation error. State empirical and approximate extensions as limitations, not implied results.

## Demotion and deletion rules

### Main text

- source-relative portability theorem;
- local obstruction plus unique coarsest repair;
- transport-defect definition with one source-relative witness family;
- path coherence plus minimum history completion;
- one ecological example.

### Supplement

- implementation-level refinement lemmas;
- alternative source-relative witness families;
- extended replacement graphs;
- deterministic replay and software details.

### External/adjacent only

- CCOC cross-grammar open-interface lower bounds;
- CCOC relay sharpness constructions.

### Exclude

- finite evidence and imperfect-detection theory;
- candidate-mechanism uncertainty;
- unsupported approximate or stochastic repair;
- new theorem families introduced only to increase result count.

## Submission gate

Paper A is ready for journal selection only when:

- the abstract and introduction name one source-relative central question;
- the main text contains no more than four result packages;
- existence, uniqueness, and source-relative minimality are visible in the repair theorem statement;
- the worked ecological example uses every main definition;
- no sentence claims that CCOC's open-composition lower bound is an MLTR special case or MLTR result;
- related work explicitly credits coarse graining, abstraction, bisimulation, transportability, and CCOC as an adjacent distinct problem;
- all numerical figure labels come from verified MLTR replay;
- the manuscript can be read without repository history or internal acronyms.
