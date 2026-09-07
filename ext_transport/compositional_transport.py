"""Compositionality of source-carried labels under total replacement relations.

This module isolates a source-relative algebraic contract that is distinct from
partition refinement.  A carried label map through a total many-to-many relation
is defined exactly when no target product state receives two distinct inherited
source labels.  For two consecutive total relations ``R`` and ``S``, direct
transport through ``R ; S`` is defined iff stepwise transport through ``R`` and
then ``S`` is defined.  When defined, the two terminal label maps are identical.

The result is deliberately scoped as supporting MLTR infrastructure.  Relational
composition itself is standard; the role here is to make the source-semantics
transport contract explicit and executable for the ecological model-reuse audit.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from .exact import canonical_labels
from .finite import GrammarAwareControlledSystem
from .macro import StageMacroProjection
from .path_transport import compose_relations
from .relation_transport import Pair, normalize_relation, validate_coverage


@dataclass(frozen=True)
class CarriedLabelConflict:
    """One target state that receives incompatible inherited source labels."""

    target_index: int
    source_indices: tuple[int, ...]
    source_labels: tuple[int, ...]

    def verify(self) -> bool:
        return (
            isinstance(self.target_index, int)
            and not isinstance(self.target_index, bool)
            and self.target_index >= 0
            and bool(self.source_indices)
            and tuple(sorted(set(self.source_indices))) == self.source_indices
            and len(set(self.source_labels)) >= 2
            and tuple(sorted(set(self.source_labels))) == self.source_labels
        )


def carried_label_conflicts(
    source_labels: Iterable[int],
    source_system: GrammarAwareControlledSystem,
    target_system: GrammarAwareControlledSystem,
    relation: Iterable[Pair],
) -> tuple[CarriedLabelConflict, ...]:
    """Return all target states receiving more than one inherited source label."""
    normalized_labels = canonical_labels(source_labels, source_system.product_state_count)
    pairs = normalize_relation(relation)
    validate_coverage(source_system, target_system, pairs)

    sources_by_target: dict[int, list[int]] = {}
    labels_by_target: dict[int, set[int]] = {}
    for source_index, target_index in pairs:
        sources_by_target.setdefault(target_index, []).append(source_index)
        labels_by_target.setdefault(target_index, set()).add(normalized_labels[source_index])

    conflicts: list[CarriedLabelConflict] = []
    for target_index in range(target_system.product_state_count):
        labels = tuple(sorted(labels_by_target[target_index]))
        if len(labels) < 2:
            continue
        conflict = CarriedLabelConflict(
            target_index=target_index,
            source_indices=tuple(sorted(set(sources_by_target[target_index]))),
            source_labels=labels,
        )
        if not conflict.verify():
            raise AssertionError("constructed carried-label conflict did not verify")
        conflicts.append(conflict)
    return tuple(conflicts)


def derive_carried_labels(
    source_labels: Iterable[int],
    source_system: GrammarAwareControlledSystem,
    target_system: GrammarAwareControlledSystem,
    relation: Iterable[Pair],
) -> tuple[int, ...]:
    """Carry inherited labels through one total relation without relabelling them."""
    normalized_labels = canonical_labels(source_labels, source_system.product_state_count)
    pairs = normalize_relation(relation)
    validate_coverage(source_system, target_system, pairs)
    conflicts = carried_label_conflicts(normalized_labels, source_system, target_system, pairs)
    if conflicts:
        first = conflicts[0]
        raise ValueError(
            "target state receives incompatible inherited source labels: "
            f"target={first.target_index}, labels={first.source_labels}"
        )

    target_labels: list[int | None] = [None] * target_system.product_state_count
    for source_index, target_index in pairs:
        label = normalized_labels[source_index]
        old = target_labels[target_index]
        if old is None:
            target_labels[target_index] = label
        elif old != label:
            raise AssertionError("conflict audit and carried assignment disagree")
    if any(label is None for label in target_labels):
        raise AssertionError("total relation must assign every target state")

    # Coverage of every source state ensures every source label is represented in
    # the target, so the inherited numeric label set remains canonical and no
    # source semantic identifier is silently renumbered.
    return canonical_labels(
        tuple(int(label) for label in target_labels),
        target_system.product_state_count,
    )


@dataclass(frozen=True)
class CarriedLabelCompositionCertificate:
    """Finite audit of direct versus sequential carried-label transport.

    A verified certificate checks the theorem on one supplied pair of consecutive
    total relations.  It may certify either the defined case (both routes yield
    one identical terminal map) or the conflict case (both direct and sequential
    transport are undefined because inherited source labels collide).
    """

    source_projection: StageMacroProjection
    intermediate_system: GrammarAwareControlledSystem
    terminal_system: GrammarAwareControlledSystem
    first_relation: tuple[Pair, ...]
    second_relation: tuple[Pair, ...]

    @property
    def source_system(self) -> GrammarAwareControlledSystem:
        return self.source_projection.constrained_system

    @property
    def direct_relation(self) -> tuple[Pair, ...]:
        return compose_relations(self.first_relation, self.second_relation)

    @property
    def first_conflicts(self) -> tuple[CarriedLabelConflict, ...]:
        return carried_label_conflicts(
            self.source_projection.summary_labels,
            self.source_system,
            self.intermediate_system,
            self.first_relation,
        )

    @property
    def intermediate_labels(self) -> tuple[int, ...]:
        return derive_carried_labels(
            self.source_projection.summary_labels,
            self.source_system,
            self.intermediate_system,
            self.first_relation,
        )

    @property
    def second_conflicts(self) -> tuple[CarriedLabelConflict, ...] | None:
        if self.first_conflicts:
            return None
        return carried_label_conflicts(
            self.intermediate_labels,
            self.intermediate_system,
            self.terminal_system,
            self.second_relation,
        )

    @property
    def direct_conflicts(self) -> tuple[CarriedLabelConflict, ...]:
        return carried_label_conflicts(
            self.source_projection.summary_labels,
            self.source_system,
            self.terminal_system,
            self.direct_relation,
        )

    @property
    def sequential_defined(self) -> bool:
        return not self.first_conflicts and self.second_conflicts == ()

    @property
    def direct_defined(self) -> bool:
        return not self.direct_conflicts

    @property
    def sequential_terminal_labels(self) -> tuple[int, ...]:
        if not self.sequential_defined:
            raise ValueError("sequential carried-label transport is not defined")
        return derive_carried_labels(
            self.intermediate_labels,
            self.intermediate_system,
            self.terminal_system,
            self.second_relation,
        )

    @property
    def direct_terminal_labels(self) -> tuple[int, ...]:
        if not self.direct_defined:
            raise ValueError("direct carried-label transport is not defined")
        return derive_carried_labels(
            self.source_projection.summary_labels,
            self.source_system,
            self.terminal_system,
            self.direct_relation,
        )

    @property
    def commutes(self) -> bool:
        return (
            self.direct_defined
            and self.sequential_defined
            and self.direct_terminal_labels == self.sequential_terminal_labels
        )

    def verify(self) -> bool:
        try:
            if not self.source_projection.verify():
                return False
            first = normalize_relation(self.first_relation)
            second = normalize_relation(self.second_relation)
            if first != self.first_relation or second != self.second_relation:
                return False
            validate_coverage(self.source_system, self.intermediate_system, first)
            validate_coverage(self.intermediate_system, self.terminal_system, second)
            validate_coverage(self.source_system, self.terminal_system, self.direct_relation)

            # The theorem has two parts: definedness is equivalent, and whenever
            # defined the terminal inherited map is exactly the same.
            if self.direct_defined != self.sequential_defined:
                return False
            if self.direct_defined:
                return self.commutes

            # In the undefined case the direct composite must expose at least one
            # inherited-label collision.  The sequential failure can occur either
            # on the first edge or on the second edge after a valid first carry.
            if not self.direct_conflicts:
                return False
            if self.first_conflicts:
                return True
            return bool(self.second_conflicts)
        except (AssertionError, TypeError, ValueError):
            return False


def certify_carried_label_composition(
    source_projection: StageMacroProjection,
    intermediate_system: GrammarAwareControlledSystem,
    terminal_system: GrammarAwareControlledSystem,
    first_relation: Iterable[Pair],
    second_relation: Iterable[Pair],
) -> CarriedLabelCompositionCertificate:
    """Certify direct/sequential equivalence for one pair of total relations."""
    certificate = CarriedLabelCompositionCertificate(
        source_projection=source_projection,
        intermediate_system=intermediate_system,
        terminal_system=terminal_system,
        first_relation=tuple(first_relation),
        second_relation=tuple(second_relation),
    )
    if not certificate.verify():
        raise ValueError("carried-label composition theorem did not verify")
    return certificate


__all__ = [
    "CarriedLabelConflict",
    "CarriedLabelCompositionCertificate",
    "carried_label_conflicts",
    "derive_carried_labels",
    "certify_carried_label_composition",
]
