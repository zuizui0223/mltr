# Master theorem proof package

This document gives the formal proof structure for the combined structural-change manuscript.

## Theorem

Let a finite source controlled ecological system carry an exact source macro-law. Let a finite target system be connected to the source by a total label-consistent relation, inducing a carried target partition.

1. The carried partition is exact if and only if output, legal-action rows, and successor carried labels are constant inside each carried fiber.
2. Failure has a finite within-fiber witness.
3. Iterative refinement by output, legal row, and successor block terminates at the unique coarsest exact target partition refining the carried partition.
4. Its state and bit increases are minimal among source-relative exact target descriptions.
5. Across a rooted finite replacement graph, route-independent repair exists if and only if all root-to-terminal paths induce the same terminal carried map. Otherwise one history mode per distinct carried map is necessary and sufficient.

## Proof 1: portability

Necessity follows directly from exactness: quotient output, action legality, and quotient successors must not depend on the chosen representative. Conversely, if all three quantities are uniform inside each carried fiber, they define representative-independent quotient functions, so the target dynamics descend to the carried quotient.

## Proof 2: local obstruction

If exactness fails, at least one quotient function is not representative-independent. Hence two target configurations in one carried fiber differ in output, legal actions, or successor carried block under a declared action. That finite pair is a certificate. Any such pair prevents exactness.

## Proof 3: coarsest repair

Start from the carried partition. Repeatedly split blocks by output, legal-action row, and successor block under every shared legal action. Each step refines the previous partition. Finiteness guarantees stabilization.

The fixed point is exact by construction. Let `E` be any exact partition refining the carried partition. Inductively, `E` must refine every iteration because exactness forces every split introduced by the refinement operator. Therefore `E` refines the fixed point. The fixed point is consequently the unique coarsest exact refinement.

## Proof 4: minimal defect

Every source-relative exact target partition refines the coarsest repair and therefore has at least as many blocks. Thus the increases in block count and log2 block count are minimal. The accumulating witness attains repaired-state count `2^m + 1` and defect `2^m - 1`.

## Proof 5: route coherence and history

If all root-to-terminal paths induce the same carried terminal map, one route-free carried partition exists and the coarsest repair applies. If two paths induce different maps, some terminal configuration receives incompatible inherited labels, so no route-free source-relative assignment can preserve both.

Index the distinct carried maps by an immutable history variable. Each history slice now has a well-defined carried map and can be repaired. Fewer history modes would merge two distinct maps and recreate the incompatibility, so one mode per distinct map is necessary and sufficient.

## Novelty boundary

The fixed-point machinery is classical. The manuscript contribution is the source-relative ecological portability problem, its finite operational obstruction, minimal repair burden, and minimum history completion.
