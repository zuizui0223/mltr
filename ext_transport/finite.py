"""Finite controlled systems and declared prefix grammars used by EXT.

These are intentionally small primitives.  A grammar state represents a declared
intervention/action contract, not an inferred biological hidden state.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Hashable, Iterable

Action = str
State = int
GrammarState = int
ProductState = tuple[int, int]


def _as_tuple(value: Iterable[object], name: str) -> tuple[object, ...]:
    try:
        return tuple(value)
    except TypeError as error:
        raise ValueError(f"{name} must be iterable") from error


@dataclass(frozen=True)
class FiniteControlledOutputSystem:
    """A finite deterministic output system with a fixed action alphabet."""

    actions: tuple[Action, ...]
    transition_table: tuple[tuple[State, ...], ...]
    outputs: tuple[Hashable, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.actions, tuple) or not self.actions:
            raise ValueError("actions must be a nonempty tuple")
        if any(not isinstance(action, str) or not action for action in self.actions):
            raise ValueError("actions must be nonempty strings")
        if len(set(self.actions)) != len(self.actions):
            raise ValueError("actions must be unique")
        if not isinstance(self.outputs, tuple) or not self.outputs:
            raise ValueError("outputs must be a nonempty tuple")
        state_count = len(self.outputs)
        if not isinstance(self.transition_table, tuple) or len(self.transition_table) != state_count:
            raise ValueError("transition_table must have one row per state")
        for row in self.transition_table:
            if not isinstance(row, tuple) or len(row) != len(self.actions):
                raise ValueError("every transition row must match actions")
            for target in row:
                if not isinstance(target, int) or isinstance(target, bool) or not 0 <= target < state_count:
                    raise ValueError("transition targets must be valid state indices")
        try:
            for output in self.outputs:
                hash(output)
        except TypeError as error:
            raise ValueError("outputs must be hashable") from error

    @property
    def state_count(self) -> int:
        return len(self.outputs)

    @property
    def states(self) -> tuple[State, ...]:
        return tuple(range(self.state_count))

    def validate_state(self, state: State) -> None:
        if not isinstance(state, int) or isinstance(state, bool) or not 0 <= state < self.state_count:
            raise ValueError("state is outside the finite state space")

    def action_index(self, action: Action) -> int:
        try:
            return self.actions.index(action)
        except ValueError as error:
            raise ValueError(f"unknown action: {action!r}") from error

    def output(self, state: State) -> Hashable:
        self.validate_state(state)
        return self.outputs[state]

    def transition(self, state: State, action: Action) -> State:
        self.validate_state(state)
        return self.transition_table[state][self.action_index(action)]


@dataclass(frozen=True)
class FinitePrefixGrammar:
    """Deterministic finite prefix-closed legal-action grammar."""

    actions: tuple[Action, ...]
    transition_table: tuple[tuple[GrammarState | None, ...], ...]
    initial_state: GrammarState = 0

    def __post_init__(self) -> None:
        if not isinstance(self.actions, tuple) or not self.actions:
            raise ValueError("actions must be a nonempty tuple")
        if any(not isinstance(action, str) or not action for action in self.actions):
            raise ValueError("actions must be nonempty strings")
        if len(set(self.actions)) != len(self.actions):
            raise ValueError("actions must be unique")
        if not isinstance(self.transition_table, tuple) or not self.transition_table:
            raise ValueError("transition_table must be nonempty")
        state_count = len(self.transition_table)
        if not isinstance(self.initial_state, int) or isinstance(self.initial_state, bool) or not 0 <= self.initial_state < state_count:
            raise ValueError("initial_state is outside the grammar")
        for row in self.transition_table:
            if not isinstance(row, tuple) or len(row) != len(self.actions):
                raise ValueError("every grammar row must match actions")
            for target in row:
                if target is not None and (
                    not isinstance(target, int) or isinstance(target, bool) or not 0 <= target < state_count
                ):
                    raise ValueError("grammar targets must be valid states or None")

    @property
    def state_count(self) -> int:
        return len(self.transition_table)

    @property
    def states(self) -> tuple[GrammarState, ...]:
        return tuple(range(self.state_count))

    def validate_state(self, state: GrammarState) -> None:
        if not isinstance(state, int) or isinstance(state, bool) or not 0 <= state < self.state_count:
            raise ValueError("grammar state is outside the finite grammar")

    def action_index(self, action: Action) -> int:
        try:
            return self.actions.index(action)
        except ValueError as error:
            raise ValueError(f"unknown grammar action: {action!r}") from error

    def legal_actions(self, state: GrammarState) -> tuple[Action, ...]:
        self.validate_state(state)
        return tuple(action for action, target in zip(self.actions, self.transition_table[state]) if target is not None)

    def transition(self, state: GrammarState, action: Action) -> GrammarState:
        self.validate_state(state)
        target = self.transition_table[state][self.action_index(action)]
        if target is None:
            raise ValueError(f"action {action!r} is illegal at grammar state {state}")
        return target

    def normalize_legal_word(self, word: Iterable[Action], start_state: GrammarState | None = None) -> tuple[Action, ...]:
        actions = _as_tuple(word, "word")
        current = self.initial_state if start_state is None else start_state
        self.validate_state(current)
        for action in actions:
            if not isinstance(action, str):
                raise ValueError("actions in a word must be strings")
            current = self.transition(current, action)
        return tuple(actions)  # type: ignore[return-value]


@dataclass(frozen=True)
class GrammarAwareControlledSystem:
    """Product of a finite controlled system and its declared legal grammar."""

    system: FiniteControlledOutputSystem
    grammar: FinitePrefixGrammar

    def __post_init__(self) -> None:
        if self.system.actions != self.grammar.actions:
            raise ValueError("system and grammar must use the same ordered actions")

    @property
    def product_state_count(self) -> int:
        return self.system.state_count * self.grammar.state_count

    @property
    def product_states(self) -> tuple[ProductState, ...]:
        return tuple(
            (system_state, grammar_state)
            for system_state in self.system.states
            for grammar_state in self.grammar.states
        )

    def product_index(self, pair: ProductState) -> int:
        system_state, grammar_state = pair
        self.system.validate_state(system_state)
        self.grammar.validate_state(grammar_state)
        return system_state * self.grammar.state_count + grammar_state

    def product_pair(self, index: int) -> ProductState:
        if not isinstance(index, int) or isinstance(index, bool) or not 0 <= index < self.product_state_count:
            raise ValueError("product index is outside the constrained system")
        return index // self.grammar.state_count, index % self.grammar.state_count

    def successor_index(self, index: int, action: Action) -> int:
        state, grammar_state = self.product_pair(index)
        return self.product_index((self.system.transition(state, action), self.grammar.transition(grammar_state, action)))

    def trace(self, index: int, word: Iterable[Action]) -> tuple[Hashable, ...]:
        state, grammar_state = self.product_pair(index)
        normalized = self.grammar.normalize_legal_word(word, grammar_state)
        trace: list[Hashable] = [self.system.output(state)]
        for action in normalized:
            state = self.system.transition(state, action)
            grammar_state = self.grammar.transition(grammar_state, action)
            trace.append(self.system.output(state))
        return tuple(trace)
