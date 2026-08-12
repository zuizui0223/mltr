# Working Results and Discussion Draft — decision-sufficiency framing

This note mirrors the current Paper A manuscript. It replaces the older theorem-first draft in which coarsest source-relative refinement was treated as the headline mathematical contribution.

## Results story

### 1. Audit an inherited ecological state classification

The source classification is carried to a target system through a declared relation. The target interface remains exact only when current outputs, legal-action rows, and action-conditioned successor labels are uniform within every inherited target class.

The ecological interpretation is **decision sufficiency**: an old state variable is valid for a target management problem only if the distinctions that the new system and action repertoire can expose are still represented.

### 2. Use a local obstruction to diagnose what is missing

Failure is witnessed by a pair of target states merged by the inherited classification but distinguished by output, action availability, or action-conditioned future. The witness is scientifically useful because it identifies a contrast that a redesigned monitoring system must be able to resolve.

### 3. Recover the least exact distinction with established refinement machinery

The coarsest exact refinement of the carried partition is computed using established partition-refinement / MDP-minimization results (Paige--Tarjan; Givan--Dean--Greig). The algorithm, its termination, and the existence/uniqueness of the coarsest refinement are prior art.

Paper A uses the result as a canonical **repair target** for an inherited ecological interface: retain every old merge that remains compatible with the target decision, and split only those that the target operations force apart.

### 4. Do not collapse all repair consequences into transport defect

The current manuscript separates:

- **structural transport defect:** increase in operational state count / uniform code-length proxy;
- **conditional repair information:** `H(Q* | C)` under a specified target-state distribution;
- **monitoring realization:** which candidate variables of what cost separate all obstruction pairs;
- **decision regret:** utility-dependent loss from acting through the inherited interface.

A large state-count defect is therefore not automatically a large management burden or ecological effect. Reward rescaling can change regret without changing the partition, and many structural splits can have negligible consequences.

### 5. Plant--pollinator example links representation failure to restoration choice

The verified finite witness merges Sites A and B under an inherited functional state. Pollinator turnover plus a target intervention exposes different substitute-pollinator responses, forcing a split.

The additional probability/cost layer is explicitly illustrative rather than empirical:

- `B = 1`;
- `c_A = 0.20`, `c_B = 0.35`;
- `p_A = 0.25`, `p_B = 0.80`;
- inherited pooled classification chooses A;
- repaired state information chooses B;
- one-step regret of the inherited choice is `0.40`;
- priority reverses when `p_B - p_A > (c_B - c_A)/B`.

The point of the calculation is not the chosen numbers. It identifies the field quantities needed to translate a structural obstruction into a management consequence.

### 6. Route coherence determines when history can be forgotten

For several declared replacement routes to the same terminal system, one route-independent carried interface exists exactly when the routes induce the same complete terminal carried label map. If the maps differ, at least one immutable context per distinct carried map is required before exact refinement.

History-sensitive equivalence is not new in general. The scoped object here is the meaning carried by **externally declared ecological replacement routes**.

## Discussion story

The paper should be read as a theory of ecological state representation for management under structural change, not as a new generic abstraction algorithm.

The main ecological chain is:

```text
existing management state
        -> structural / intervention change
        -> decision-sufficiency audit
        -> local hidden distinction
        -> least exact state repair
        -> targeted monitoring requirement
        -> decision analysis / VoI if uncertainty and costs matter
```

This places Paper A upstream of two established ecological tasks:

1. targeted monitoring can identify practical variables and thresholds once the state distinction that matters is known;
2. value-of-information analysis can decide whether resolving uncertainty about that distinction is worth the sampling cost.

The central message is that ecological state validity is conditional on the current system, outputs, actions, and management objective. An inherited label can remain biologically intelligible while becoming operationally insufficient.

## Scope guardrails

Paper A does not:

- infer replacement relations or histories from field data;
- estimate stochastic transition probabilities;
- optimize management policies;
- introduce generic coarsest partition refinement;
- introduce source-to-target state-abstraction transfer;
- invent targeted monitoring or value of information;
- claim structural state-count defect is an ecological effect size;
- claim history-sensitive equivalence is generally new;
- present the illustrative plant--pollinator probabilities as empirical estimates.

Detailed notation, propositions, figures, and citations should be taken from `manuscript/paper_a_main.tex`; the novelty boundary is maintained in `docs/paper_a_reference_audit.md`.
