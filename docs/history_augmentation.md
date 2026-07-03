# Minimal history augmentation after path incoherence

## Question

Path-label coherence makes a transported terminal macro-law independent of
replacement route. When coherence fails, different declared histories assign
different root macro labels to the same terminal product state. Rather than
abandoning the transported law, ask:

> What is the minimum finite history context needed to represent every declared
> carried terminal label map simultaneously, and what exact macro-law remains
> after that context is retained?

## Carried maps and history modes

Fix a root exact projection \(q_r\), terminal controlled system \(T\), and a
finite set of root-to-terminal paths \(p\). Every path whose composed relation is
root-fiber-label-consistent gives a carried map

\[
c_p:T\to Q_r.
\]

A finite history assignment maps every path to a mode

\[
\eta:p\mapsto h\in H
\]

and represents all carried maps only when one mode never has to encode two
different full label tuples:

\[
\eta(p)=\eta(p')
\quad\Longrightarrow\quad
c_p=c_{p'}.
\]

Thus the canonical minimum history modes are the distinct carried maps:

\[
H_{\min}=\{c_p: p\text{ is a declared root-to-terminal path}\}.
\]

## Minimum history augmentation theorem

\[
\boxed{
|H_{\min}|=
\bigl|\{c_p\}\bigr|
}
\]

is the smallest number of immutable history modes capable of preserving every
declared path-specific carried map.

### Proof

If two paths have different carried tuples, a single mode would require one
function \(c^H(-,h)\) to assign two different labels to at least one terminal
state. Hence they must occupy distinct modes, giving the lower bound by the
number of distinct tuples. Assign one mode to each distinct tuple. This
construction represents every path and reaches the lower bound.

The resulting raw history-context cost is

\[
\Delta_H^{\#}=|H_{\min}|-1,
\qquad
\Delta_H^K=\log_2|H_{\min}|.
\]

It is measured relative to one route-independent terminal context. It is not a
claim that all historical details must be stored.

## History-sliced terminal system

For every history mode \(h\), make one immutable copy \(T_h\) of the terminal
controlled system. The action grammar and within-slice dynamics are unchanged:

\[
(t,h)\xrightarrow{a}(t',h).
\]

Give slice \(h\) the carried labels represented by that mode. Apply EXT's
relative exact refinement to this augmented finite system.

### Theorem: coarsest history-aware exact repair

The relative exact refinement of the history-sliced terminal system is the
coarsest exact interface that refines all path-specific carried labels while
retaining only the minimum number of history modes. It may merge slices again
when their carried labels and all legal futures are indistinguishable. Therefore
history is retained only to the extent the declared model requires.

Define the final exact-interface cost relative to the root law by

\[
\Delta_{\mathrm{HA}}^{\#}=|Q_{T\times H}^{\min}|-|Q_r|,
\qquad
\Delta_{\mathrm{HA}}^K=
\log_2|Q_{T\times H}^{\min}|-\log_2|Q_r|.
\]

This is distinct from \(\Delta_H\): the former counts final exact macrostate
repair, while the latter counts the minimum raw history context necessary to
represent the incompatible carried maps at all.

## Two-route boundary witness

The repository's path-incoherent diamond has terminal carried maps

\[
c_{p_1}=(0,1),
\qquad
c_{p_2}=(1,0).
\]

They are distinct, so

\[
|H_{\min}|=2,
\qquad
\Delta_H^{\#}=1,
qquad
\Delta_H^K=1.
\]

The two history slices receive carried labels

\[
(0,1,1,0).
\]

Since equal carried labels now occur at states with distinct output, exact
refinement separates all four augmented witness states:

\[
|Q_r|=2,
\qquad
|Q_{T\times H}^{\min}|=4,
\qquad
\Delta_{\mathrm{HA}}^{\#}=2,
\qquad
\Delta_{\mathrm{HA}}^K=1.
\]

## Ecological reading

A terminal community can be structurally similar after different sequences of
extinction, recolonization, restoration, or rewiring. When those histories carry
different macro labels under a declared model, the terminal configuration alone
cannot support one transported law. A minimal history mode records only which
class of path-specific carried assignment occurred; the subsequent exact
refinement determines whether that context changes any future output or
intervention response.

The theorem does not infer historical pathways from field data, identify the
correct ecological memory variable, or claim that observed communities are
finite deterministic systems. Histories, relations, states, and action grammars
are declared components of a separate finite model contract.
