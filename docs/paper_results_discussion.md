# Working Results and Discussion Draft — monitoring-repair framing

This note mirrors the current Paper A manuscript. It replaces both the older theorem-first story and the intermediate version in which monitoring realization was only one of several parallel consequences of repair.

## Results story

### 1. Audit an inherited ecological state classification

The source classification is carried to a target system through a declared relation. The target interface remains exact only when current outputs, legal-action rows, and action-conditioned successor labels are uniform within every inherited target class.

The ecological interpretation is **decision sufficiency**: an old state variable is valid for a target management problem only if the distinctions that the new system and action repertoire can expose are still represented.

### 2. Return the local obstruction

Failure is witnessed by a pair of target states merged by the inherited classification but distinguished by output, action availability, or action-conditioned future. The witness is scientifically useful because it identifies a contrast that the inherited state suppresses.

Established coarsest refinement then supplies the least exact state distinction required by the target interface. This construction is prior art and functions only as the canonical repair target.

### 3. Monitoring realization is the applied centerpiece

Let

`E = {(x,x'): C(x)=C(x'), Q*(x) != Q*(x')}`

be the obstruction pairs. A selected candidate-measurement set `S` exactly realizes the repaired state when a decoder exists:

`Q*(x) = d_S(C(x), z_S(x))`.

The main monitoring theorem proves that this holds **if and only if** every pair in `E` is separated by at least one selected measurement.

This produces three ecological outcomes:

1. **Inherited state passes:** no structural monitoring repair is required for the declared target interface.
2. **Inherited state fails, but the candidate library covers all obstruction pairs:** exact recovery is possible; if measurement costs are supplied, least-cost monitoring is weighted set cover over the obstruction pairs.
3. **Inherited state fails and at least one obstruction pair is uncovered by the full candidate library:** the current monitoring library is structurally incapable of recovering the decision-sufficient state. The uncovered pair is an explicit impossibility certificate.

This is the strongest bridge to ecological monitoring. Paper A does not claim a new generic set-cover algorithm; it specifies the scientifically required universe of distinctions that the monitoring design must cover.

### 4. Plant--pollinator example links monitoring failure to restoration choice

The verified finite witness merges Sites A and B under an inherited functional state. Pollinator turnover plus a target intervention exposes different substitute-pollinator responses, forcing a split. In biological terms, the missing state coordinate is substitute-response capacity.

The additional probability/cost layer is explicitly illustrative rather than empirical:

- `B = 1`;
- `c_A = 0.20`, `c_B = 0.35`;
- `p_A = 0.25`, `p_B = 0.80`;
- inherited pooled classification chooses A;
- repaired state information chooses B;
- one-step regret of the inherited choice is `0.40`;
- priority reverses when `p_B - p_A > (c_B - c_A)/B`.

The point is not the chosen numbers. It shows why recovering the obstruction can matter operationally and identifies the field quantities needed to connect monitoring repair to management consequences.

### 5. Structural defect, information, and regret are secondary and distinct

The current manuscript separates:

- **structural state-count defect:** loss of compression;
- **conditional repair information:** `H(Q* | C)` under a specified target-state distribution;
- **monitoring realization cost:** acquisition cost of measurements sufficient to reconstruct `Q*`;
- **decision regret:** utility-dependent loss from acting through the inherited interface.

The supplement proves the strong non-ordering result: for every `d >= 1` and every `r >= 0`, there is a finite exact-repair problem with defect `d` and regret `r`. State-count defect therefore cannot be used as a universal proxy for ecological importance or management loss.

### 6. Route coherence determines when history can be forgotten

For several declared replacement routes to the same terminal system, one route-independent carried interface exists exactly when the routes induce the same complete terminal carried label map. If the maps differ, at least one immutable context per distinct carried map is required before exact refinement.

History-sensitive equivalence is not new in general. This is a secondary closure result for meanings carried by externally declared ecological replacement routes.

## Discussion story

The paper should be read as a theory of ecological state representation and monitoring repair under structural change, not as a new generic abstraction algorithm.

The main ecological chain is now deliberately one-dimensional:

```text
existing management state
        -> structural / intervention change
        -> decision-sufficiency audit
        -> local obstruction
        -> exact monitoring feasibility / impossibility
        -> minimum-cost monitoring realization
        -> management consequence
```

This places Paper A upstream of two established ecological tasks:

1. Jones-style targeted monitoring can identify practical field indicators, thresholds, and error properties once the audit has determined which distinctions must be recovered;
2. Canessa-style value-of-information analysis can decide whether measuring those distinctions is worth the cost once uncertainty and decision consequences are specified.

The central message is therefore stronger than ``the old classification may fail.'' It is:

> when an inherited ecological state fails under a changed intervention, the failure defines a falsifiable requirement for monitoring redesign. A candidate monitoring library can be certified sufficient, certified insufficient by an uncovered obstruction, or optimized for least exact acquisition cost.

## Scope guardrails

Paper A does not:

- infer replacement relations or histories from field data;
- estimate stochastic transition probabilities;
- optimize management policies;
- introduce generic coarsest partition refinement;
- introduce source-to-target state-abstraction transfer;
- invent targeted monitoring, set cover, or value of information;
- claim structural state-count defect is an ecological effect size;
- claim history-sensitive equivalence is generally new;
- present the illustrative plant--pollinator probabilities as empirical estimates.

Detailed notation, propositions, figures, and citations should be taken from `manuscript/paper_a_main.tex`; the novelty boundary is maintained in `docs/paper_a_reference_audit.md`.
