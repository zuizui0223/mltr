# Path-label coherence: route-independent repair on replacement graphs

## Question

The transport-defect theorem quantifies the minimum exact repair of a carried
macro-law along one declared replacement relation. A replacement history is often
not unique: two sequences of turnover, recolonization, restoration, or rewiring
may reach the same declared terminal stage.

> When do all declared histories carry the same root macro labels to that
> terminal stage, and therefore require the same minimal exact repair?

## Rooted finite replacement graph

Let a finite directed acyclic graph have root stage \(r\), terminal stage \(v\),
and one declared total relation \(R_e\) on every directed edge. The root carries
an exact projection

\[
q_r:S_r\to Q_r.
\]

For a root-to-terminal path

\[
p=(e_1,\ldots,e_k),
\]

write its composed relation as

\[
R_p=R_{e_1};\cdots;R_{e_k}\subseteq S_r\times S_v.
\]

The path induces a carried terminal label map when every terminal state related
by \(R_p\) receives one root macro label:

\[
c_p(t)=q_r(s)\qquad ((s,t)\in R_p).
\]

The implementation checks total relation coverage and this path-level
root-fiber-label consistency. Stronger output/legal-row/successor conditions for
an individual edge remain assumptions to be certified by EXT's existing exact or
conservative edge-level transport modules.

## Path-label coherence

The graph is **path-label coherent at \(v\)** when every root-to-\(v\) path has
a well-defined carried map and all paths agree pointwise:

\[
\boxed{
 c_p(t)=c_{p'}(t)
 \quad\text{for every terminal state }t
 \text{ and every two root-to-}v\text{ paths }p,p'.
}
\]

Equivalently, for any shared terminal state,

\[
(s,t)\in R_p,\quad (s',t)\in R_{p'}
\quad\Longrightarrow\quad
q_r(s)=q_r(s').
\]

## Theorem: route-independent carried partition and repair

If a rooted finite replacement DAG is path-label coherent at terminal \(v\),
then there is one carried terminal partition

\[
c_v=c_p
\]

independent of the root-to-\(v\) path \(p\). Let

\[
\operatorname{Ref}_v(c_v)
\]

be EXT's relative exact refinement of that partition under the terminal action
grammar. Then

\[
\boxed{
\operatorname{Ref}_v(c_p)=\operatorname{Ref}_v(c_{p'})
}
\]

for all root-to-terminal paths. In particular, the relative transport defect

\[
\Delta_{\#}=|Q_v^{\min}|-|Q_r|,
\qquad
\Delta_K=\log_2|Q_v^{\min}|-\log_2|Q_r|
\]

is route independent.

### Proof

Path-label coherence gives equality of the carried label tuple at every terminal
product state. Relative exact refinement is a deterministic finite fixed-point
function of only that tuple and the terminal controlled system. Equal inputs
therefore yield equal fixed points, and the two defect quantities depend only on
that fixed point and the fixed root projection.

## Positive diamond witness

The repository contains a two-route diamond in which both branches carry the
same local transport-defect relation:

\[
(0,0,1)\longrightarrow(0,1,2).
\]

Each route gives the carried target labels \((0,0,1)\), the same three-state
exact repair, and

\[
\Delta_{\#}=1.
\]

## Boundary witness

A second diamond preserves only the graph-level total-relation assumptions. One
path carries \((0,1)\), while the other carries \((1,0)\). The path-coherence
certificate rejects this graph.

This is intentionally **not** an edge-level exact transport certificate. It
shows that total relations alone do not make a transported macro-law independent
of replacement history. The extra coherence condition is doing real work.

## Ecological reading

Different sequences of extinction, recolonization, restoration, or interaction
rewiring can lead to a similarly described terminal community. Path-label
coherence asks whether the coarse law carried from a declared pre-turnover stage
has the same meaning regardless of which declared history occurred. A failure
means that the final community description alone is insufficient to identify the
carried macro-law; the replacement history matters under the chosen model
contract.

The theorem does not infer ecological history, relations, or action grammars
from field observations. It applies only after those finite objects are declared.
