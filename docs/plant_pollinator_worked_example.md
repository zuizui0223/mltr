# Worked ecological example — pollinator turnover and functional-state repair

## Purpose

This example instantiates the structural-change theorem without claiming empirical fitting. It is designed to support all three main figures and every formal object used in the manuscript.

## Source system

A plant population is summarized by two functional pollination regimes:

```text
Q0 = {low service, high service}.
```

The source community contains a resident pollinator guild. Under the source action grammar, only a baseline management action is available. Two distinct low-service microconfigurations are therefore merged because they have the same observed service class and the same future response under every source-legal action.

The exact source macro-law is

```text
microstates:  x0, x1, x2
source labels: low, low, high.
```

## Structural change

The resident guild is lost and a replacement guild colonizes. The target community admits an additional floral manipulation or exclusion treatment that was not meaningful in the source community.

A declared replacement relation carries source meaning to target configurations:

```text
source low  -> target x0 and x1
source high -> target x2.
```

Thus the carried target labels are

```text
(low, low, high).
```

## Portability failure

Under the newly available treatment:

```text
x0 -> low-service successor
x1 -> high-service successor.
```

The two target states inherited the same source label but no longer have the same action successor. The old functional classification is therefore not exact for the target operational model.

The key ecological interpretation is not that species identities must always be retained. It is that the replacement guild makes one previously irrelevant floral or interaction distinction predictive under a declared future intervention.

## Minimal repair

The coarsest source-relative exact repair is

```text
x0 -> low-A
x1 -> low-B
x2 -> high.
```

Only the affected inherited low-service fiber is split. The high-service fiber remains unchanged. The transport defect is one additional macrostate.

This distinguishes the framework from constructing an entirely new target classification: the repair preserves every inherited merge that remains exact.

## Accumulating target distinctions

To illustrate the sharp family, suppose the replacement community introduces `m` independently manipulable floral or interaction channels. Each low-service target configuration carries a binary vector

```text
(b1,...,bm).
```

Treatment `probe_i` exposes coordinate `bi`. The inherited low-service class therefore splits into all `2^m` response profiles, while the high-service state remains one class.

The repaired target law has

```text
2^m + 1 states,
```

and transport defect

```text
2^m - 1 states.
```

The manuscript must state that the intervention repertoire grows with `m`; this is a sharp construction, not a field-estimated scaling relationship.

## Alternative replacement histories

Consider two loss–colonization routes:

```text
route A: resident loss -> guild L colonization -> terminal community
route B: resident loss -> guild R colonization -> terminal community.
```

If both routes assign the same inherited functional labels to every terminal configuration, the minimal repair is route independent.

If route A carries terminal labels `(low, high)` while route B carries `(high, low)`, the same terminal configurations inherit incompatible source meanings. No route-free carried partition exists. Two history modes are then necessary and sufficient before computing the history-aware repair.

## Figure mapping

### Figure 1

Show source macro fibers, replacement relation, target-only intervention, and the one-fiber split.

### Figure 2

Show the verified transport-defect curve across `m`, with repaired states and defect states.

### Figure 3

Show coherent and incoherent replacement diamonds, followed by the two-mode history augmentation.

## Scope statement

The relation, action grammar, guild turnover, and response table are declared theoretical inputs. The example demonstrates the theorem's ecological interpretation but does not infer a real pollination network, estimate treatment responses, or claim that all community turnover requires history-dependent states.
