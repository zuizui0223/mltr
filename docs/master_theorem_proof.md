# Master theorem proof package

This document gives the formal proof structure for the structural-change manuscript.

## Theorem

Let a finite source controlled ecological system carry an exact source macro-law. Let a finite target system be connected to the source by a total label-consistent relation, inducing a carried target partition.

1. The carried partition is exact if and only if output, legal-action rows, and successor carried labels are constant inside each carried fiber.
2. Failure has a finite within-fiber witness.
3. Iterative refinement by output, legal row, and successor block terminates at the unique coarsest exact target partition refining the carried partition.
4. Its state and bit increases are minimal among source-relative exact target descriptions.
5. Across a rooted finite replacement graph, if all root-to-terminal paths induce the same carried terminal label map, then the carried semantics, relative repair, and defect are route independent. If declared paths induce different carried maps, no single route-free carried label map can preserve all of those inherited source semantics; one history mode per distinct carried map is necessary and sufficient to represent them simultaneously before relative exact refinement.

The last clause is a statement about preservation of inherited **label semantics**. It does not claim that two different carried maps must produce different unlabeled final repair partitions: distinct inherited assignments can in principle refine to the same final partition after all necessary splits are made.

## Proof 1: portability

Necessity follows directly from exactness: quotient output, action legality, and quotient successors must not depend on the chosen representative. Conversely, if all three quantities are uniform inside each carried fiber, they define representative-independent quotient functions, so the target dynamics descend to the carried quotient.

## Proof 2: local obstruction

If exactness fails, at least one quotient function is not representative-independent. Hence two target configurations in one carried fiber differ in output, legal actions, or successor carried block under a declared action. That finite pair is a certificate. Any such pair prevents exactness.

## Proof 3: coarsest repair

Start from the carried partition. Repeatedly split blocks by output, legal-action row, and successor block under every declared legal action. Each step refines the previous partition. Finiteness guarantees stabilization.

The fixed point is exact by construction. Let `E` be any exact partition refining the carried partition. Inductively, `E` must refine every iteration because exactness forces every split introduced by the refinement operator. Therefore `E` refines the fixed point. The fixed point is consequently the unique coarsest exact refinement.

## Proof 4: minimal defect

Every source-relative exact target partition refines the coarsest repair and therefore has at least as many blocks. Thus the increases in block count and log2 block count are minimal. The accumulating witness attains repaired-state count `2^m + 1` and defect `2^m - 1`.

## Proof 5: route coherence and history

If all root-to-terminal paths induce the same carried terminal map, one route-free inherited label assignment exists. Relative exact refinement is a deterministic function of that carried assignment and the terminal controlled system, so the repaired partition and defect are route independent.

If two paths induce different carried maps, some terminal configuration receives different inherited source labels under those paths. Therefore no single route-free **carried label map** can preserve both inherited assignments. This is the obstruction that history augmentation repairs; it is not a proof that the two unlabeled repaired partitions must differ.

Index the distinct carried maps by an immutable history variable. Each history slice now has a well-defined carried map and can be repaired. Fewer history modes would merge two distinct carried maps and require one mode to encode incompatible inherited labels somewhere on the terminal system. Thus one mode per distinct carried map is necessary and sufficient to preserve all declared path-specific semantics. Relative exact refinement of the history-sliced system then gives the coarsest exact interface compatible with those semantics.

## Contribution boundary

The fixed-point machinery is classical and functions as infrastructure. The manuscript's central contribution is the source-relative route boundary: complete carried terminal maps determine whether one inherited law is route independent, and their equality classes give the necessary-and-sufficient immutable history modes when it is not. The finite operational obstruction, unique coarsest exact repair, and transport defect make that boundary executable without claiming a new generic refinement algorithm or literature-firstness for path dependence.
