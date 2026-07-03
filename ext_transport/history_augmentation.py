"""Minimal finite history augmentation for path-incoherent replacement graphs.

Path-label coherence gives one carried terminal partition. When it fails, several
declared root-to-terminal histories can assign different root macro labels to the
same terminal product state. This module keeps exactly the minimum finite history
context needed to represent all such carried label maps simultaneously, then uses
EXT's relative exact refinement to construct the coarsest history-aware exact
interface.

The construction is relative to a declared finite rooted replacement graph. It
does not infer ecological histories or assert that every real historical process
should be treated as a persistent state variable.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from math import log2

from .exact import canonical_labels
from .finite import FiniteControlledOutputSystem, GrammarAwareControlledSystem
from .path_transport import RootedReplacementGraph, path_carried_labels
from .refinement import RelativeExactRefinement, relative_exact_refinement


def _normalized_path_maps(
    labels_by_path: Iterable[Iterable[int]],
    terminal_product_state_count: int,
) -> tuple[tuple[int, ...], ...]:
    """Validate one canonical root-label tuple for every declared history."""
    try:
        maps = tuple(canonical_labels(labels, terminal_product_state_count) for labels in labels_by_path)
    except TypeError as error:
        raise ValueError("labels_by_path must be iterable") from error
    if not maps:
        raise ValueError("at least one root-to-terminal path is required")
    return maps


def history_assignment_is_compatible(
    labels_by_path: Iterable[Iterable[int]],
    path_modes: Iterable[int],
    terminal_product_state_count: int,
) -> bool:
    """Whether one finite history-mode assignment represents all carried maps.

    A history mode may represent several paths only when their full carried
    terminal label tuples agree. This is the finite semantic constraint behind
    the history-augmentation minimum.
    """
    try:
        maps = _normalized_path_maps(labels_by_path, terminal_product_state_count)
        modes = tuple(path_modes)
        if len(modes) != len(maps) or not modes:
            return False
        if any(not isinstance(mode, int) or isinstance(mode, bool) or mode < 0 for mode in modes):
            return False
        if tuple(sorted(set(modes))) != tuple(range(max(modes) + 1)):
            return False
        return all(maps[left] == maps[right] for left in range(len(maps)) for right in range(len(maps)) if modes[left] == modes[right])
    except (TypeError, ValueError):
        return False


def minimum_history_mode_assignment(
    labels_by_path: Iterable[Iterable[int]],
    terminal_product_state_count: int,
) -> tuple[tuple[tuple[int, ...], ...], tuple[int, ...]]:
    """Return distinct carried label maps and the minimum path-to-mode assignment.

    Two paths share a mode exactly when their full terminal label tuples are the
    same. Therefore the number of distinct tuples is both achievable and a lower
    bound for every compatible finite history assignment.
    """
    maps = _normalized_path_maps(labels_by_path, terminal_product_state_count)
    modes: list[tuple[int, ...]] = []
    assignment: list[int] = []
    for labels in maps:
        if labels not in modes:
            modes.append(labels)
        assignment.append(modes.index(labels))
    result = tuple(modes), tuple(assignment)
    if not history_assignment_is_compatible(maps, result[1], terminal_product_state_count):
        raise AssertionError("minimum history assignment is not compatible")
    return result


def history_augmented_terminal_system(
    terminal_system: GrammarAwareControlledSystem,
    history_mode_count: int,
) -> GrammarAwareControlledSystem:
    """Copy a terminal controlled system once per immutable history mode."""
    if (
        not isinstance(history_mode_count, int)
        or isinstance(history_mode_count, bool)
        or history_mode_count < 1
    ):
        raise ValueError("history_mode_count must be a positive integer")
    raw = terminal_system.system
    raw_state_count = raw.state_count
    transitions = tuple(
        tuple(history_mode * raw_state_count + target for target in row)
        for history_mode in range(history_mode_count)
        for row in raw.transition_table
    )
    outputs = tuple(raw.outputs[state] for _history_mode in range(history_mode_count) for state in raw.states)
    return GrammarAwareControlledSystem(
        FiniteControlledOutputSystem(raw.actions, transitions, outputs),
        terminal_system.grammar,
    )


def history_augmented_product_index(
    terminal_system: GrammarAwareControlledSystem,
    history_mode: int,
    terminal_product_index: int,
) -> int:
    """Index the copy of a terminal product state in one history slice."""
    if not isinstance(history_mode, int) or isinstance(history_mode, bool) or history_mode < 0:
        raise ValueError("history_mode must be a nonnegative integer")
    raw_state, grammar_state = terminal_system.product_pair(terminal_product_index)
    augmented_raw_state = history_mode * terminal_system.system.state_count + raw_state
    grammar_count = terminal_system.grammar.state_count
    return augmented_raw_state * grammar_count + grammar_state


def history_augmented_carried_labels(
    terminal_system: GrammarAwareControlledSystem,
    history_label_maps: Iterable[Iterable[int]],
) -> tuple[int, ...]:
    """Lift one carried terminal label map to each history slice."""
    maps = _normalized_path_maps(history_label_maps, terminal_system.product_state_count)
    augmented_count = len(maps) * terminal_system.product_state_count
    labels: list[int | None] = [None] * augmented_count
    for history_mode, label_map in enumerate(maps):
        for terminal_index, label in enumerate(label_map):
            augmented_index = history_augmented_product_index(terminal_system, history_mode, terminal_index)
            labels[augmented_index] = label
    if any(label is None for label in labels):
        raise AssertionError("every augmented product state must receive a carried label")
    return canonical_labels(tuple(int(label) for label in labels), augmented_count)


@dataclass(frozen=True)
class HistoryAugmentationCertificate:
    """Minimum history contexts and coarsest exact history-aware repair.

    The certificate retains one immutable terminal slice for every distinct
    root-to-terminal carried label tuple. It is minimal among assignments that
    preserve all declared path-specific carried maps. Relative exact refinement
    then removes any history distinction that is not needed by the declared
    terminal output/action grammar.
    """

    graph: RootedReplacementGraph
    terminal: str

    @property
    def terminal_system(self) -> GrammarAwareControlledSystem:
        try:
            return self.graph.stage_map[self.terminal]
        except KeyError as error:
            raise ValueError("terminal stage is absent from graph") from error

    @property
    def labels_by_path(self) -> tuple[tuple[int, ...], ...]:
        return path_carried_labels(self.graph, self.terminal)

    @property
    def history_label_maps(self) -> tuple[tuple[int, ...], ...]:
        maps, _assignment = minimum_history_mode_assignment(
            self.labels_by_path,
            self.terminal_system.product_state_count,
        )
        return maps

    @property
    def path_history_modes(self) -> tuple[int, ...]:
        _maps, assignment = minimum_history_mode_assignment(
            self.labels_by_path,
            self.terminal_system.product_state_count,
        )
        return assignment

    @property
    def minimum_history_mode_count(self) -> int:
        return len(self.history_label_maps)

    @property
    def additional_history_modes(self) -> int:
        """Modes beyond a single route-independent terminal context."""
        return self.minimum_history_mode_count - 1

    @property
    def history_augmentation_bits(self) -> float:
        """Finite context bits needed to distinguish the minimum history modes."""
        return log2(self.minimum_history_mode_count)

    @property
    def augmented_system(self) -> GrammarAwareControlledSystem:
        return history_augmented_terminal_system(self.terminal_system, self.minimum_history_mode_count)

    @property
    def augmented_carried_labels(self) -> tuple[int, ...]:
        return history_augmented_carried_labels(self.terminal_system, self.history_label_maps)

    @property
    def refinement(self) -> RelativeExactRefinement:
        return relative_exact_refinement(self.augmented_system, self.augmented_carried_labels)

    @property
    def root_macrostate_count(self) -> int:
        return self.graph.root_projection.label_count

    @property
    def history_aware_macrostate_count(self) -> int:
        return self.refinement.refined_label_count

    @property
    def history_aware_defect_states(self) -> int:
        """Extra exact macrostates after retaining all required history modes."""
        return self.history_aware_macrostate_count - self.root_macrostate_count

    @property
    def history_aware_defect_bits(self) -> float:
        return log2(self.history_aware_macrostate_count) - log2(self.root_macrostate_count)

    def verify(self) -> bool:
        try:
            if not self.graph.verify() or self.terminal not in self.graph.stage_map:
                return False
            maps = self.labels_by_path
            modes = self.history_label_maps
            assignment = self.path_history_modes
            terminal_count = self.terminal_system.product_state_count
            if not history_assignment_is_compatible(maps, assignment, terminal_count):
                return False
            if len(modes) != len(set(maps)) or len(modes) != max(assignment) + 1:
                return False
            if any(modes[mode] != labels for mode, labels in zip(assignment, maps)):
                return False
            augmented = self.augmented_system
            if augmented.product_state_count != self.minimum_history_mode_count * terminal_count:
                return False
            carried = self.augmented_carried_labels
            for history_mode, label_map in enumerate(modes):
                for terminal_index, label in enumerate(label_map):
                    if carried[history_augmented_product_index(self.terminal_system, history_mode, terminal_index)] != label:
                        return False
            if max(carried) + 1 != self.root_macrostate_count:
                return False
            refinement = self.refinement
            return (
                refinement.verify()
                and self.history_aware_defect_states == refinement.additional_macrostates
                and abs(self.history_aware_defect_bits - refinement.additional_memory_bits) < 1e-12
            )
        except (AssertionError, TypeError, ValueError):
            return False


def certify_history_augmentation(
    graph: RootedReplacementGraph,
    terminal: str,
) -> HistoryAugmentationCertificate:
    """Certify minimal finite history augmentation and exact history-aware repair."""
    certificate = HistoryAugmentationCertificate(graph, terminal)
    if not certificate.verify():
        raise ValueError("replacement histories do not support a finite history-augmentation certificate")
    return certificate
