"""Exact interfaces for declared finite controlled systems.

The local output/legal-action/successor condition is sufficient for equality of
all legal future traces by induction on word length. EXT uses it as a finite
certificate predicate; it is not a procedure for inferring a grammar from data.
"""

from __future__ import annotations

from collections.abc import Iterable

from .finite import GrammarAwareControlledSystem


def canonical_labels(labels: Iterable[int], count: int) -> tuple[int, ...]:
    """Validate one contiguous nonnegative macro label per product state."""
    try:
        values = tuple(labels)
    except TypeError as error:
        raise ValueError("summary labels must be iterable") from error
    if len(values) != count or not values:
        raise ValueError("summary labels must provide one entry per product state")
    if any(not isinstance(value, int) or isinstance(value, bool) or value < 0 for value in values):
        raise ValueError("summary labels must be nonnegative integers")
    if tuple(sorted(set(values))) != tuple(range(max(values) + 1)):
        raise ValueError("summary labels must be canonical and contiguous")
    return values


def is_exact_interface(system: GrammarAwareControlledSystem, labels: Iterable[int]) -> bool:
    """Check exact output, legal-row, and successor factorization.

    For any two product states in the same macro fiber, this checks equal current
    output, equal legal action rows, and equal macro successors for each legal
    action. Induction then gives equal traces for every legal future word.
    """
    try:
        normalized = canonical_labels(labels, system.product_state_count)
        for left in range(system.product_state_count):
            left_state, left_grammar = system.product_pair(left)
            left_output = system.system.output(left_state)
            left_legal = system.grammar.legal_actions(left_grammar)
            for right in range(system.product_state_count):
                if normalized[left] != normalized[right]:
                    continue
                right_state, right_grammar = system.product_pair(right)
                if left_output != system.system.output(right_state):
                    return False
                if left_legal != system.grammar.legal_actions(right_grammar):
                    return False
                for action in left_legal:
                    if normalized[system.successor_index(left, action)] != normalized[system.successor_index(right, action)]:
                        return False
        return True
    except (TypeError, ValueError):
        return False
