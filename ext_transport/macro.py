"""Finite macro dynamics and exact stage projections for EXT."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Hashable, Iterable

from .exact import canonical_labels, is_exact_interface
from .finite import GrammarAwareControlledSystem


@dataclass(frozen=True)
class PortableMacroDynamics:
    """One finite deterministic macro output/legal-action/transition system."""

    actions: tuple[str, ...]
    outputs: tuple[Hashable, ...]
    legal_action_rows: tuple[tuple[str, ...], ...]
    transition_rows: tuple[tuple[int | None, ...], ...]

    @property
    def state_count(self) -> int:
        return len(self.outputs)

    def verify(self) -> bool:
        try:
            if not self.actions or len(set(self.actions)) != len(self.actions):
                return False
            if not self.outputs or len(self.legal_action_rows) != self.state_count or len(self.transition_rows) != self.state_count:
                return False
            for output in self.outputs:
                hash(output)
            for legal, row in zip(self.legal_action_rows, self.transition_rows):
                if len(row) != len(self.actions):
                    return False
                if tuple(action for action, successor in zip(self.actions, row) if successor is not None) != legal:
                    return False
                if len(set(legal)) != len(legal) or any(action not in self.actions for action in legal):
                    return False
                if any(successor is not None and (not isinstance(successor, int) or not 0 <= successor < self.state_count) for successor in row):
                    return False
            return True
        except TypeError:
            return False


@dataclass(frozen=True)
class ConservativeMacroSchema:
    """One macro schema whose rows may add legal actions across replacement."""

    actions: tuple[str, ...]
    outputs: tuple[Hashable, ...]
    transition_rows: tuple[tuple[int | None, ...], ...]

    @property
    def state_count(self) -> int:
        return len(self.outputs)

    @property
    def legal_action_rows(self) -> tuple[tuple[str, ...], ...]:
        return tuple(
            tuple(action for action, successor in zip(self.actions, row) if successor is not None)
            for row in self.transition_rows
        )

    def verify(self) -> bool:
        return PortableMacroDynamics(self.actions, self.outputs, self.legal_action_rows, self.transition_rows).verify()


@dataclass(frozen=True)
class StageMacroProjection:
    """A declared exact projection of one controlled stage into macro labels."""

    constrained_system: GrammarAwareControlledSystem
    summary_labels: tuple[int, ...]

    @property
    def label_count(self) -> int:
        return max(self.summary_labels) + 1

    def induced_macro(self) -> PortableMacroDynamics:
        if not self.verify():
            raise ValueError("stage labels must be an exact grammar-aware interface")
        actions = self.constrained_system.system.actions
        outputs: list[Hashable] = []
        legal_rows: list[tuple[str, ...]] = []
        rows: list[tuple[int | None, ...]] = []
        for label in range(self.label_count):
            members = [index for index, value in enumerate(self.summary_labels) if value == label]
            if not members:
                raise AssertionError("canonical labels must realize every macro label")
            representative = members[0]
            state, grammar_state = self.constrained_system.product_pair(representative)
            legal = self.constrained_system.grammar.legal_actions(grammar_state)
            outputs.append(self.constrained_system.system.output(state))
            legal_rows.append(legal)
            rows.append(
                tuple(
                    self.summary_labels[self.constrained_system.successor_index(representative, action)]
                    if action in legal
                    else None
                    for action in actions
                )
            )
        macro = PortableMacroDynamics(actions, tuple(outputs), tuple(legal_rows), tuple(rows))
        if not macro.verify():
            raise AssertionError("induced macro dynamics did not verify")
        return macro

    def stage_rows(self) -> tuple[tuple[int | None, ...], ...]:
        return self.induced_macro().transition_rows

    def verify(self) -> bool:
        try:
            labels = canonical_labels(self.summary_labels, self.constrained_system.product_state_count)
            return labels == self.summary_labels and is_exact_interface(self.constrained_system, labels)
        except (TypeError, ValueError):
            return False


def ensure_exact_stage(system: GrammarAwareControlledSystem, labels: Iterable[int]) -> StageMacroProjection:
    stage = StageMacroProjection(system, tuple(labels))
    if not stage.verify():
        raise ValueError("labels do not define an exact macro projection")
    return stage
