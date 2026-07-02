"""Local obstructions to carrying a macro merge through replacement."""

from __future__ import annotations

from dataclasses import dataclass

from .exact import canonical_labels
from .finite import GrammarAwareControlledSystem
from .macro import StageMacroProjection
from .relation_transport import Pair, _legal, _output, normalize_relation


@dataclass(frozen=True)
class ReplacementFiberSplitObstructionCertificate:
    """A newly legal target word separates one carried source macro fiber.

    This refutes the supplied carried merge only. It does not imply unbounded
    memory, nor that every alternative target macro-law fails.
    """

    source: StageMacroProjection
    target_system: GrammarAwareControlledSystem
    proposed_target_labels: tuple[int, ...]
    relation: tuple[Pair, ...]
    left_source_index: int
    right_source_index: int
    future_word: tuple[str, ...]

    def verify(self) -> bool:
        try:
            if not self.source.verify():
                return False
            source_system = self.source.constrained_system
            if source_system.system.actions != self.target_system.system.actions:
                return False
            labels = canonical_labels(self.proposed_target_labels, self.target_system.product_state_count)
            if labels != self.proposed_target_labels:
                return False
            relation = normalize_relation(self.relation)
            if relation != self.relation:
                return False
            if {source_index for source_index, _ in relation} != set(range(source_system.product_state_count)):
                return False
            relation_map = dict(relation)
            if len(relation_map) != len(relation):
                return False
            for source_index, target_index in relation:
                if not 0 <= target_index < self.target_system.product_state_count:
                    return False
                if self.source.summary_labels[source_index] != labels[target_index]:
                    return False
                if _output(source_system, source_index) != _output(self.target_system, target_index):
                    return False
                old_actions = _legal(source_system, source_index)
                if not set(old_actions).issubset(_legal(self.target_system, target_index)):
                    return False
                for action in old_actions:
                    if relation_map.get(source_system.successor_index(source_index, action)) != self.target_system.successor_index(target_index, action):
                        return False
            if self.left_source_index == self.right_source_index:
                return False
            if self.left_source_index not in relation_map or self.right_source_index not in relation_map:
                return False
            if self.source.summary_labels[self.left_source_index] != self.source.summary_labels[self.right_source_index]:
                return False
            left_target = relation_map[self.left_source_index]
            right_target = relation_map[self.right_source_index]
            if labels[left_target] != labels[right_target]:
                return False
            source_left_grammar = source_system.product_pair(self.left_source_index)[1]
            source_right_grammar = source_system.product_pair(self.right_source_index)[1]
            try:
                source_system.grammar.normalize_legal_word(self.future_word, source_left_grammar)
                source_system.grammar.normalize_legal_word(self.future_word, source_right_grammar)
                return False
            except ValueError:
                pass
            target_left_grammar = self.target_system.product_pair(left_target)[1]
            target_right_grammar = self.target_system.product_pair(right_target)[1]
            self.target_system.grammar.normalize_legal_word(self.future_word, target_left_grammar)
            self.target_system.grammar.normalize_legal_word(self.future_word, target_right_grammar)
            return self.target_system.trace(left_target, self.future_word) != self.target_system.trace(right_target, self.future_word)
        except (AssertionError, TypeError, ValueError):
            return False
