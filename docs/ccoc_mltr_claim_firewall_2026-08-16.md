# MLTR–CCOC claim firewall — 2026-08-16

## Decision

MLTR and CCOC may share exact finite operational notation and classical refinement machinery, but they answer different quantified questions and should be developed and submitted as distinct theorem stories unless a future manuscript explicitly proves a new bridge theorem.

## MLTR question: transport one inherited law

MLTR fixes an already accepted source macro-law \(q_S\), carries its semantics through a declared source–target relation, and asks whether those inherited labels remain exact in the target. If not, admissible repairs must refine the carried source labels.

The central optimization is therefore

\[
\min_{q_T\text{ exact},\;q_T\succeq \operatorname{carry}(q_S)} |q_T|.
\]

MLTR owns:

- unchanged portability of a fixed inherited macro-law;
- unique coarsest source-relative exact repair;
- transport defect relative to that inherited law;
- route coherence across replacement histories;
- minimum history context when carried terminal semantics disagree.

A target may expose new legal actions or future words. That does not turn MLTR into CCOC: the inherited source partition remains fixed and constrains the target repair.

## CCOC question: minimum interface under open futures

CCOC does not fix one inherited source partition. For each closed grammar \(\Gamma_i\), it may choose its own minimum exact interface,

\[
K_i^*=\min_{q\text{ exact under }\Gamma_i}\log_2|q|,
\]

and compares these with the minimum exact interface under a jointly open grammar,

\[
K_O^*=\min_{q\text{ exact under }\Gamma_O}\log_2|q|.
\]

Its headline separation has the form

\[
\max_i K_i^*=O(1),\qquad K_O^*=\Omega(m),
\]

with bounded-local sharpness witnesses.

CCOC owns the cross-grammar lower bound and its sharpness. MLTR must not import that separation as a transport-defect result or present open composition itself as one of MLTR's main theorem contributions.

## Writing rule for MLTR

Allowed wording:

> The target operational grammar may differ from the source grammar, so a newly legal action can invalidate an inherited macro-law. MLTR asks for unchanged transport or the least exact repair constrained by the inherited labels.

Avoid wording that says:

> Open composition is merely a special case of MLTR's theorem.

That sentence hides the quantifier difference. A grammar expansion can be an MLTR **application instance**, but CCOC's theorem optimizes over different closed interfaces before comparing them with one open minimum, which is a distinct problem.

## Manuscript consequence

MLTR Paper A should contain only the source-relative hierarchy:

1. operational portability of carried labels;
2. local failure witness plus unique coarsest source-relative repair;
3. transport defect induced by that repair;
4. route coherence and minimum history completion.

CCOC's open-interface lower bound and bounded-local relay family may be cited as adjacent motivation or external provenance, but they are not MLTR results and should not be counted in the MLTR result hierarchy.

## Development stop rule

A proposed MLTR result is out of scope if it independently optimizes the macro partition under each closed grammar and concludes that the minimum exact interface under their jointly open grammar must grow. Route that work to CCOC.

A proposed CCOC result is out of scope if it fixes one inherited source partition and returns its unique coarsest exact target repair, repair defect, or history augmentation. Route that work to MLTR.
