"""Exact macro-law transport through finite non-nested replacement relations."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from .finite import GrammarAwareControlledSystem
from .macro import PortableMacroDynamics, StageMacroProjection

Pair = tuple[int, int]


def normalize_relation(relation: Iterable[Pair]) -> tuple[Pair, ...]:
    try:
        pairs = tuple(relation)
    except TypeError as error:
        raise ValueError("transport relation must be iterable") from error
    if not pairs or any(
        not isinstance(pair, tuple)
        or len(pair) != 2
        or any(not isinstance(index, int) or isinstance(index, bool) for index in pair)
        for pair in pairs
    ):
        raise ValueError("transport relation must contain integer index pairs")
    if tuple(sorted(set(pairs))) != pairs:
        raise ValueError("transport relation must be sorted and unique")
    return pairs


def _output(system: GrammarAwareControlledSystem, index: int):
    state, _ = system.product_pair(index)
    return system.system.output(state)


def _legal(system: GrammarAwareControlledSystem, index: int) -> tuple[str, ...]:
    _, grammar_state = system.product_pair(index)
    return system.grammar.legal_actions(grammar_state)


def validate_coverage(source: GrammarAwareControlledSystem, target: GrammarAwareControlledSystem, relation: tuple[Pair, ...]) -> None:
    if source.system.actions != target.system.actions:
        raise ValueError("source and target action alphabets must agree")
    if any(not 0 <= left < source.product_state_count or not 0 <= right < target.product_state_count for left, right in relation):
        raise ValueError("relation contains an out-of-range product index")
    if {left for left, _ in relation} != set(range(source.product_state_count)):
        raise ValueError("relation must cover each source product state")
    if {right for _, right in relation} != set(range(target.product_state_count)):
        raise ValueError("relation must cover each target product state")


@dataclass(frozen=True)
class ReplacementTransport:
    """A total output/legal/successor-preserving relation between exact stages."""

    source: StageMacroProjection
    target: StageMacroProjection
    relation: tuple[Pair, ...]

    @property
    def is_source_to_target_injection(self) -> bool:
        return (
            len(self.relation) == self.source.constrained_system.product_state_count
            and len({target for _, target in self.relation}) == len(self.relation)
        )

    def verify(self) -> bool:
        try:
            if not self.source.verify() or not self.target.verify() or self.source.induced_macro() != self.target.induced_macro():
                return False
            relation = normalize_relation(self.relation)
            if relation != self.relation:
                return False
            source_system = self.source.constrained_system
            target_system = self.target.constrained_system
            validate_coverage(source_system, target_system, relation)
            relation_set = set(relation)
            for source_index, target_index in relation:
                if self.source.summary_labels[source_index] != self.target.summary_labels[target_index]:
                    return False
                if _output(source_system, source_index) != _output(target_system, target_index):
                    return False
                legal = _legal(source_system, source_index)
                if legal != _legal(target_system, target_index):
                    return False
                for action in legal:
                    if (source_system.successor_index(source_index, action), target_system.successor_index(target_index, action)) not in relation_set:
                        return False
            return True
        except (TypeError, ValueError):
            return False


def derive_target_labels(source: StageMacroProjection, target: GrammarAwareControlledSystem, relation: Iterable[Pair]) -> tuple[int, ...]:
    """Derive target macro labels under equal-legal-row transport assumptions."""
    if not source.verify():
        raise ValueError("source must be exact")
    pairs = normalize_relation(relation)
    source_system = source.constrained_system
    validate_coverage(source_system, target, pairs)
    relation_set = set(pairs)
    labels: list[int | None] = [None] * target.product_state_count
    for source_index, target_index in pairs:
        source_label = source.summary_labels[source_index]
        old = labels[target_index]
        if old is None:
            labels[target_index] = source_label
        elif old != source_label:
            raise ValueError("target fiber is not source-label consistent")
        if _output(source_system, source_index) != _output(target, target_index):
            raise ValueError("relation does not preserve output")
        legal = _legal(source_system, source_index)
        if legal != _legal(target, target_index):
            raise ValueError("relation does not preserve equal legal rows")
        for action in legal:
            if (source_system.successor_index(source_index, action), target.successor_index(target_index, action)) not in relation_set:
                raise ValueError("relation is not successor-closed")
    if any(label is None for label in labels):
        raise AssertionError("coverage must derive every target label")
    result = tuple(int(label) for label in labels)
    if tuple(sorted(set(result))) != tuple(range(max(result) + 1)):
        raise ValueError("derived labels are not canonical")
    return result


@dataclass(frozen=True)
class TransportedTargetProjectionCertificate:
    """A relation constructs an exact target projection from a source projection."""

    source: StageMacroProjection
    target_system: GrammarAwareControlledSystem
    relation: tuple[Pair, ...]

    @property
    def target_labels(self) -> tuple[int, ...]:
        return derive_target_labels(self.source, self.target_system, self.relation)

    @property
    def target_projection(self) -> StageMacroProjection:
        projection = StageMacroProjection(self.target_system, self.target_labels)
        if not projection.verify():
            raise AssertionError("derived labels are not an exact target projection")
        return projection

    def verify(self) -> bool:
        try:
            return self.source.verify() and self.target_projection.induced_macro() == self.source.induced_macro()
        except (AssertionError, TypeError, ValueError):
            return False


def certify_transported_target_projection(source: StageMacroProjection, target_system: GrammarAwareControlledSystem, relation: Iterable[Pair]) -> TransportedTargetProjectionCertificate:
    certificate = TransportedTargetProjectionCertificate(source, target_system, tuple(relation))
    if not certificate.verify():
        raise ValueError("relation does not construct an exact target projection")
    return certificate


@dataclass(frozen=True)
class TransportCoherentMacroLawCertificate:
    """One macro-law over a connected finite graph of replacement relations."""

    macro: PortableMacroDynamics
    stages: tuple[StageMacroProjection, ...]
    transports: tuple[ReplacementTransport, ...]

    def verify(self) -> bool:
        try:
            if not self.macro.verify() or len(self.stages) < 2 or not self.transports:
                return False
            if any(not stage.verify() or stage.induced_macro() != self.macro for stage in self.stages):
                return False
            adjacency = {index: set() for index in range(len(self.stages))}
            for transport in self.transports:
                if not transport.verify():
                    return False
                left = self.stages.index(transport.source)
                right = self.stages.index(transport.target)
                if left == right:
                    return False
                adjacency[left].add(right)
                adjacency[right].add(left)
            reached, frontier = {0}, [0]
            while frontier:
                current = frontier.pop()
                for next_index in adjacency[current]:
                    if next_index not in reached:
                        reached.add(next_index)
                        frontier.append(next_index)
            return reached == set(range(len(self.stages)))
        except (TypeError, ValueError):
            return False


def certify_transport_coherent_macro_law(macro: PortableMacroDynamics, stages: Iterable[StageMacroProjection], transports: Iterable[ReplacementTransport]) -> TransportCoherentMacroLawCertificate:
    certificate = TransportCoherentMacroLawCertificate(macro, tuple(stages), tuple(transports))
    if not certificate.verify():
        raise ValueError("replacement graph does not realize one coherent macro-law")
    return certificate
