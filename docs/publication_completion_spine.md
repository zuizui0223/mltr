# Paper A publication-completion spine

## Fixed identity

**Working title:** Exact Ecological Macro-Laws under Structural Change: Portability, Minimal Repair, and Historical Context

**Repository scope:** CCOC supplies the frozen open-composition theorem provenance; MLTR is the active manuscript and reproducibility repository. Open composition is presented only as a nested special case of structural change.

**Central question:** When does an ecological macro-law survive structural change, and, when it fails, what is the unique minimal exact repair?

No new theorem family should be added during submission preparation.

## Publication abstract

Ecological prediction often reuses coarse state variables after turnover, rewiring, habitat replacement, or changes in the available interventions. Such transfer is valid only if the structural change does not expose distinctions suppressed by the inherited macro-law. We formulate finite operational models in which a source macro-law is carried to a target system through a declared state relation and prove an exact portability criterion based on outputs, legal actions, and successors. When portability fails, the failure has a local operational witness and the inherited labels admit a unique coarsest source-relative exact refinement, which we interpret as the minimal repair required for valid prediction. The increase in repaired states, or equivalently in description length, defines a transport defect. For systems connected by several replacement histories, path coherence is necessary and sufficient for one route-independent carried repair; otherwise the minimum exact completion retains one immutable context for each distinct carried terminal map. A finite plant–pollinator turnover example shows how a previously adequate functional classification can become invalid after a new management action is introduced and how the theorem identifies the least additional ecological distinction needed to restore exact prediction.

## Introduction spine

### Problem

Ecological macrostates are routinely transported across altered communities and management regimes. A guild label, occupancy class, resilience category, or functional state may be exact for the original system but cease to be exact after species turnover, interaction rewiring, or expansion of the intervention repertoire.

### Gap

Coarse graining, lumpability, abstraction, and bisimulation provide mature languages for state aggregation. Transportability addresses whether conclusions transfer across environments. These literatures do not by themselves answer the paper's combined question: given an already accepted ecological macro-law and a declared structural change, when does that exact law remain valid, and if it does not, what is the unique coarsest exact repair constrained to preserve its source semantics?

### Contribution hierarchy

1. **Operational Portability Criterion.** The carried target partition is exact if and only if current outputs, legal-action rows, and action successors factor through the inherited labels.
2. **Local Obstruction and Unique Coarsest Source-relative Repair.** A newly legal action or future word can witness failure inside one carried fiber; iterative operational refinement returns the unique coarsest exact partition refining the inherited labels.
3. **Transport Defect.** The minimal repair burden is quantified by the increase in repaired state count or description length.
4. **History Coherence and Minimum History Completion.** Coherent replacement paths share one carried repair. Incoherent paths require exactly one immutable history mode per distinct carried terminal map before relative repair.

### Ecological conclusion

The framework distinguishes two scientifically different causes of failed transfer: the old variable may remain valid, or structural change may expose an ecologically consequential distinction that must be added. The repair theorem identifies the least such addition under the declared operational model.

## Results spine

### Result 1 — Operational portability

State one master theorem only. CCOC's grammar-aware interface conditions and MLTR's relation transport appear as ingredients or corollaries, not competing headline results.

**Reviewer-facing interpretation:** This is not merely a homomorphism restatement because the transported labels are inherited through a possibly non-nested state relation and are tested against the target's legal operational grammar.

**Ecological payoff:** It gives an exact diagnostic for whether a macro-variable learned before structural change can still support every declared target prediction and intervention.

### Result 2 — Local obstruction and minimal repair

Treat the local witness and the fixed-point refinement as one theorem package. The theorem must visibly contain existence, exactness, coarseness, and uniqueness relative to the carried labels.

**Reviewer-facing interpretation:** Standard partition refinement is credited as machinery. Novelty lies in the source-relative transport problem, the operational obstruction, and the unique repair interpretation, not in claiming a new generic refinement algorithm.

**Ecological payoff:** When transfer fails, the result identifies the minimum additional ecological distinction required rather than merely rejecting the old classification.

### Result 3 — Transport defect

Define

- `Delta_count = |Q_target_repaired| - |Q_source|`,
- `Delta_bits = log2 |Q_target_repaired| - log2 |Q_source|`.

Present the accumulating finite family as a sharp witness, with all scope assumptions in the proposition and figure caption. Do not promote the family to a separate theorem.

**Ecological payoff:** Defect separates mild structural change, which needs one extra state, from change that destroys most of the original compression.

### Result 4 — History coherence and minimum completion

Present path coherence as the graph-level characterization and minimum history completion as its canonical failure repair. The minimum number of modes is the number of distinct carried terminal maps.

**Reviewer-facing interpretation:** This does not infer historical pathways or ecological memory from data. It characterizes the exact context needed when several declared histories induce different target semantics.

**Ecological payoff:** It determines when one management model is valid regardless of replacement route and when path identity must remain part of the predictive state.

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

The paper supplies a finite, exact decision structure for inherited ecological macro-laws under structural change: unchanged portability, unique minimal repair, quantified repair burden, route-independent repair, or minimum history-aware completion.

### What is not claimed

- no inference of the source–target relation from field data;
- no empirical claim that a chosen ecological variable is exact;
- no stochastic or approximate theorem beyond the declared finite deterministic setting;
- no claim that partition refinement, bisimulation, or lumpability are new;
- no claim that historical paths are identifiable from terminal observations.

### Relation to adjacent literatures

- **Coarse graining and lumpability:** provide exact aggregation criteria within a fixed system; this paper studies inherited aggregation across declared structural change.
- **Abstraction and bisimulation:** provide behavioral equivalence machinery; this paper adds source-relative transport, unique constrained repair, and repair burden.
- **Transportability:** studies transfer of causal or statistical conclusions; this paper gives an operational state-space criterion and exact repair for transported macro-laws.
- **Ecological resilience and regime shifts:** motivate structural change but do not generally provide a unique minimal refinement of an inherited predictive variable.

### Limitations and next step

Approximate, stochastic, and data-estimated variants are important but belong to future work unless supported by complete theorems. They should not be sketched as additional contribution families in the current manuscript.

## Figure plan

1. **Conceptual pipeline:** source exact macro-law → structural change → portability test → unchanged law or minimal repair.
2. **Local obstruction and repair:** one inherited fiber split by a target-only action, with the unique coarsest repaired partition.
3. **Transport defect:** verified accumulating witness, displaying repaired state count and defect against exposed distinctions.
4. **History coherence:** coherent routes sharing one repair versus incoherent routes requiring minimum history modes.

The ecological worked example should supply labels and interpretation for Figures 1, 2, and 4 rather than appearing as a disconnected fifth conceptual figure.

## Reviewer audit

### Criticism: “This is standard bisimulation or partition refinement.”

**Answer:** Credit the standard fixed-point machinery explicitly. The contribution is the characterization of an inherited source-relative partition under non-nested structural transport, the local operational failure witness, the unique constrained repair, and its transport/history consequences.

### Criticism: “The framework is too abstract to be ecological.”

**Answer:** The worked example must show a concrete conclusion unavailable before the theorem: whether an existing functional state remains usable after turnover and, if not, exactly which ecological distinction must be retained.

### Criticism: “The defect is a descriptive statistic rather than a theorem.”

**Answer:** Present defect as a definition supported by the minimal-repair theorem and sharp finite families. Do not inflate it into an independent theorem claim.

### Criticism: “History completion merely copies systems by path.”

**Answer:** The nontrivial statement is minimality: paths may share a mode exactly when their complete carried terminal maps agree, so the number of distinct maps is necessary and sufficient.

### Criticism: “Exact finite assumptions are unrealistic.”

**Answer:** Position exactness as a benchmark that isolates structural failure from statistical estimation error. State empirical and approximate extensions as limitations, not implied results.

## Demotion and deletion rules

### Main text

- master portability theorem;
- local obstruction plus unique coarsest repair;
- transport-defect definition with one sharp family;
- path coherence plus minimum history completion;
- one ecological example.

### Supplement

- relay construction details;
- implementation-level refinement lemmas;
- alternative witness families;
- extended replacement graphs;
- deterministic replay and software details;
- complete CCOC theorem registry and provenance.

### Exclude

- finite evidence and imperfect-detection theory;
- candidate-mechanism uncertainty;
- unsupported approximate or stochastic repair;
- new theorem families introduced only to increase result count.

## Submission gate

Paper A is ready for journal selection only when:

- the abstract and introduction name one central question;
- the main text contains no more than four result packages;
- existence, uniqueness, and source-relative minimality are visible in the repair theorem statement;
- the worked ecological example uses every main definition;
- open composition reads as a special case, not a paper nested inside the paper;
- related work explicitly credits coarse graining, abstraction, bisimulation, and transportability;
- all numerical figure labels come from the verified replay;
- the manuscript can be read without repository history or internal acronyms.
