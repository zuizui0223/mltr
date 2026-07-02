"""Conservative macro-schema transport with target-only actions."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from .finite import GrammarAwareControlledSystem
from .macro import ConservativeMacroSchema, StageMacroProjection
from .relation_transport import Pair, _legal, _output, normalize_relation, validate_coverage


def derive_conservative_target_labels(source: StageMacroProjection, target: GrammarAwareControlledSystem, relation: Iterable[Pair]) -> tuple[int, ...]:
    """Derive target labels while allowing target-only legal actions."""
    if not source.verify():
        raise ValueError("source must be exact")
    pairs = normalize_relation(relation)
    source_system = source.constrained_system
    validate_coverage(source_system, target, pairs)
    relation_set = set(pairs)
    labels: list[int | None] = [None] * target.product_state_count
    for source_index, target_index in pairs:
        label = source.summary_labels[source_index]
        previous = labels[target_index]
        if previous is None:
            labels[target_index] = label
        elif previous != label:
            raise ValueError("target fiber is not source-label consistent")
        if _output(source_system, source_index) != _output(target, target_index):
            raise ValueError("relation does not preserve output")
        source_legal = _legal(source_system, source_index)
        target_legal = _legal(target, target_index)
        if not set(source_legal).issubset(target_legal):
            raise ValueError("target does not preserve source-legal actions")
        for action in source_legal:
            if (source_system.successor_index(source_index, action), target.successor_index(target_index, action)) not in relation_set:
                raise ValueError("relation is not successor-closed for an old action")
    if any(label is None for label in labels):
        raise AssertionError("coverage must derive every target label")
    result = tuple(int(label) for label in labels)
    if tuple(sorted(set(result))) != tuple(range(max(result) + 1)):
        raise ValueError("derived labels are not canonical")
    return result


@dataclass(frozen=True)
class ConservativeTransportedSchemaCertificate:
    """One source macro-law and target-only actions define a common schema.

    An action newly legal at the target must have the same availability and one
    macro successor at every target state in a derived macro fiber. This is a
    sufficient criterion, not a characterization of every possible transport.
    """

    source: StageMacroProjection
    target_system: GrammarAwareControlledSystem
    relation: tuple[Pair, ...]

    @property
    def target_labels(self) -> tuple[int, ...]:
        return derive_conservative_target_labels(self.source, self.target_system, self.relation)

    @property
    def schema(self) -> ConservativeMacroSchema:
        labels = self.target_labels
        source_macro = self.source.induced_macro()
        actions = self.source.constrained_system.system.actions
        rows: list[tuple[int | None, ...]] = []
        for label in range(source_macro.state_count):
            members = [index for index, value in enumerate(labels) if value == label]
            if not members:
                raise AssertionError("every source macro label must occur at target")
            old_legal = source_macro.legal_action_rows[label]
            reference_legal = _legal(self.target_system, members[0])
            if not set(old_legal).issubset(reference_legal):
                raise AssertionError("old action preservation should already have been checked")
            successor_by_action: dict[str, int] = {}
            for target_index in members:
                legal = _legal(self.target_system, target_index)
                if legal != reference_legal:
                    raise ValueError("target-only action availability is not uniform within a macro fiber")
                for action in legal:
                    successor = labels[self.target_system.successor_index(target_index, action)]
                    previous = successor_by_action.get(action)
                    if previous is None:
                        successor_by_action[action] = successor
                    elif previous != successor:
                        raise ValueError("target action is not macro-successor deterministic within a fiber")
            row: list[int | None] = []
            for action_index, action in enumerate(actions):
                old_successor = source_macro.transition_rows[label][action_index]
                if old_successor is not None:
                    if successor_by_action.get(action) != old_successor:
                        raise ValueError("old macro action changed meaning at target")
                    row.append(old_successor)
                else:
                    row.append(successor_by_action.get(action))
            rows.append(tuple(row))
        schema = ConservativeMacroSchema(actions, source_macro.outputs, tuple(rows))
        if not schema.verify():
            raise AssertionError("constructed conservative macro schema did not verify")
        return schema

    @property
    def target_projection(self) -> StageMacroProjection:
        projection = StageMacroProjection(self.target_system, self.target_labels)
        if not projection.verify():
            raise AssertionError("derived target labels did not define an exact target projection")
        return projection

    def verify(self) -> bool:
        try:
            schema = self.schema
            target = self.target_projection
            if target.stage_rows() != schema.transition_rows:
                return False
            return all(
                old is None or old == new
                for source_row, schema_row in zip(self.source.stage_rows(), schema.transition_rows)
                for old, new in zip(source_row, schema_row)
            )
        except (AssertionError, TypeError, ValueError):
            return False


def certify_conservative_transported_schema(source: StageMacroProjection, target_system: GrammarAwareControlledSystem, relation: Iterable[Pair]) -> ConservativeTransportedSchemaCertificate:
    certificate = ConservativeTransportedSchemaCertificate(source, target_system, tuple(relation))
    if not certificate.verify():
        raise ValueError("relation does not construct a conservative target macro schema")
    return certificate
