"""Minimal exact repair of carried macro partitions after replacement.

A replacement relation may preserve all source-legal actions while target-only
interactions split a carried target macro fiber.  This module computes the
coarsest exact target interface that refines that carried partition.  It does
not claim that every failed replacement relation has this form: the source
projection, relation, and old-action preservation are declared finite-model
assumptions.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from math import log2
from typing import Hashable

from .conservative import derive_conservative_target_labels
from .exact import canonical_labels, is_exact_interface
from .finite import GrammarAwareControlledSystem
from .macro import StageMacroProjection
from .relation_transport import Pair


def _first_occurrence_labels(labels: Iterable[int], count: int) -> tuple[int, ...]:
    """Return an equivalent partition with labels ordered by first occurrence."""
    values = canonical_labels(labels, count)
    translation: dict[int, int] = {}
    normalized: list[int] = []
    for value in values:
        if value not in translation:
            translation[value] = len(translation)
        normalized.append(translation[value])
    return tuple(normalized)


def is_refinement(fine_labels: Iterable[int], coarse_labels: Iterable[int], count: int) -> bool:
    """Whether ``fine`` only splits, and never merges, blocks of ``coarse``."""
    fine = canonical_labels(fine_labels, count)
    coarse = canonical_labels(coarse_labels, count)
    return all(
        fine[left] != fine[right] or coarse[left] == coarse[right]
        for left in range(count)
        for right in range(count)
    )


def _refine_once(system: GrammarAwareControlledSystem, labels: tuple[int, ...]) -> tuple[int, ...]:
    """Split each current block by output, legal row, and successor blocks."""
    signature_to_label: dict[tuple[Hashable | int | tuple[object, ...], ...], int] = {}
    refined: list[int] = []
    for index in range(system.product_state_count):
        state, grammar_state = system.product_pair(index)
        legal = system.grammar.legal_actions(grammar_state)
        successor_labels = tuple(labels[system.successor_index(index, action)] for action in legal)
        signature = (labels[index], system.system.output(state), legal, successor_labels)
        if signature not in signature_to_label:
            signature_to_label[signature] = len(signature_to_label)
        refined.append(signature_to_label[signature])
    return tuple(refined)


@dataclass(frozen=True)
class RelativeExactRefinement:
    """The coarsest exact target partition refining a carried partition.

    ``carried_labels`` are derived from a source macro-law through a declared
    replacement relation.  ``refined_labels`` are obtained by monotone
    partition refinement on the target controlled system.  The construction
    never merges carried blocks, so every increase in label count is a required
    repair of the transported macro description.
    """

    target_system: GrammarAwareControlledSystem
    carried_labels: tuple[int, ...]
    refined_labels: tuple[int, ...]
    refinement_rounds: int

    @property
    def carried_label_count(self) -> int:
        return max(self.carried_labels) + 1

    @property
    def refined_label_count(self) -> int:
        return max(self.refined_labels) + 1

    @property
    def additional_macrostates(self) -> int:
        return self.refined_label_count - self.carried_label_count

    @property
    def additional_memory_bits(self) -> float:
        return log2(self.refined_label_count) - log2(self.carried_label_count)

    @property
    def fiber_split_profile(self) -> tuple[int, ...]:
        """Number of repaired target blocks inside each carried macro fiber."""
        return tuple(
            len({self.refined_labels[index] for index, label in enumerate(self.carried_labels) if label == carried})
            for carried in range(self.carried_label_count)
        )

    def verify(self) -> bool:
        try:
            count = self.target_system.product_state_count
            carried = _first_occurrence_labels(self.carried_labels, count)
            refined = _first_occurrence_labels(self.refined_labels, count)
            if carried != self.carried_labels or refined != self.refined_labels:
                return False
            if not isinstance(self.refinement_rounds, int) or self.refinement_rounds < 0:
                return False
            recomputed = relative_exact_refinement(self.target_system, carried)
            return (
                recomputed.refined_labels == refined
                and recomputed.refinement_rounds == self.refinement_rounds
                and is_refinement(refined, carried, count)
                and is_exact_interface(self.target_system, refined)
            )
        except (TypeError, ValueError):
            return False

    @property
    def target_projection(self) -> StageMacroProjection:
        projection = StageMacroProjection(self.target_system, self.refined_labels)
        if not projection.verify():
            raise AssertionError("relative refinement did not produce an exact target projection")
        return projection


def relative_exact_refinement(
    target_system: GrammarAwareControlledSystem,
    carried_labels: Iterable[int],
) -> RelativeExactRefinement:
    """Compute the coarsest exact interface refining ``carried_labels``.

    The finite iteration is the standard output/legal-row/successor partition
    refinement, constrained never to merge the supplied carried partition.  At
    its fixed point, blocks satisfy the exact-interface condition.  Any exact
    target interface refining the carried partition must refine every iteration
    and hence the returned fixed point.
    """
    current = _first_occurrence_labels(carried_labels, target_system.product_state_count)
    rounds = 0
    while True:
        next_labels = _refine_once(target_system, current)
        if next_labels == current:
            result = RelativeExactRefinement(target_system, current if rounds == 0 else _first_occurrence_labels(carried_labels, target_system.product_state_count), current, rounds)
            # ``carried_labels`` must remain the initial partition, rather than
            # the last refinement, in the returned certificate.
            result = RelativeExactRefinement(
                target_system,
                _first_occurrence_labels(carried_labels, target_system.product_state_count),
                current,
                rounds,
            )
            if not result.verify():
                raise AssertionError("relative refinement fixed point failed exactness verification")
            return result
        current = next_labels
        rounds += 1
        if rounds >= target_system.product_state_count:
            raise AssertionError("finite partition refinement did not stabilize")


@dataclass(frozen=True)
class TransportDefectCertificate:
    """Quantify minimal exact target repair after conservative replacement.

    The source projection and relation first induce a carried target partition
    that preserves all source-legal actions.  The relative exact refinement then
    gives the coarsest exact target projection refining that partition.  The
    defect is therefore a repair cost for this carried macro-law, not a claim
    that every target macro-law or every replacement relation is impossible.
    """

    source: StageMacroProjection
    target_system: GrammarAwareControlledSystem
    relation: tuple[Pair, ...]

    @property
    def carried_labels(self) -> tuple[int, ...]:
        return _first_occurrence_labels(
            derive_conservative_target_labels(self.source, self.target_system, self.relation),
            self.target_system.product_state_count,
        )

    @property
    def refinement(self) -> RelativeExactRefinement:
        return relative_exact_refinement(self.target_system, self.carried_labels)

    @property
    def repaired_target_projection(self) -> StageMacroProjection:
        return self.refinement.target_projection

    @property
    def source_macrostate_count(self) -> int:
        return self.source.label_count

    @property
    def target_macrostate_count(self) -> int:
        return self.refinement.refined_label_count

    @property
    def transport_defect_states(self) -> int:
        return self.target_macrostate_count - self.source_macrostate_count

    @property
    def transport_defect_bits(self) -> float:
        return log2(self.target_macrostate_count) - log2(self.source_macrostate_count)

    def verify(self) -> bool:
        try:
            if not self.source.verify():
                return False
            carried = self.carried_labels
            if max(carried) + 1 != self.source.label_count:
                return False
            refinement = self.refinement
            return (
                refinement.verify()
                and self.repaired_target_projection.verify()
                and self.transport_defect_states == refinement.additional_macrostates
                and abs(self.transport_defect_bits - refinement.additional_memory_bits) < 1e-12
            )
        except (AssertionError, TypeError, ValueError):
            return False


def certify_transport_defect(
    source: StageMacroProjection,
    target_system: GrammarAwareControlledSystem,
    relation: Iterable[Pair],
) -> TransportDefectCertificate:
    """Certify the minimum exact target repair of a carried macro partition."""
    certificate = TransportDefectCertificate(source, target_system, tuple(relation))
    if not certificate.verify():
        raise ValueError("relation does not support a finite conservative transport-defect certificate")
    return certificate
