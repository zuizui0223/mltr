"""Route-independent carried macro labels on finite replacement graphs.

This module adds a graph-level layer above EXT's edge-level transport results.
Each edge is a declared total relation between finite product-state spaces.  The
module does not infer or re-prove ecological validity of those relations; an
edge can separately be certified by the exact or conservative transport modules.

For a root exact projection, every root-to-terminal path composes edge relations
and induces a carried terminal partition.  Path-label coherence means all such
paths induce the same root-label map.  Since relative exact refinement is
deterministic from the terminal system and carried partition, coherence makes
the resulting repair and transport defect route-independent.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from math import log2

from .exact import canonical_labels
from .finite import GrammarAwareControlledSystem
from .macro import StageMacroProjection
from .refinement import RelativeExactRefinement, relative_exact_refinement
from .relation_transport import Pair, normalize_relation, validate_coverage

Path = tuple[int, ...]


@dataclass(frozen=True)
class ReplacementPathStage:
    """A named finite stage in a declared rooted replacement graph."""

    name: str
    system: GrammarAwareControlledSystem


@dataclass(frozen=True)
class ReplacementPathEdge:
    """One declared total relation from ``source`` to ``target`` stage."""

    source: str
    target: str
    relation: tuple[Pair, ...]


def compose_relations(left: Iterable[Pair], right: Iterable[Pair]) -> tuple[Pair, ...]:
    """Relational composition ``left ; right`` for finite sorted index pairs."""
    first = normalize_relation(left)
    second = normalize_relation(right)
    successors: dict[int, set[int]] = {}
    for middle, target in second:
        successors.setdefault(middle, set()).add(target)
    composed = tuple(sorted({(source, target) for source, middle in first for target in successors.get(middle, set())}))
    if not composed:
        raise ValueError("consecutive replacement relations have empty composition")
    return normalize_relation(composed)


def _identity_relation(system: GrammarAwareControlledSystem) -> tuple[Pair, ...]:
    return tuple((index, index) for index in range(system.product_state_count))


@dataclass(frozen=True)
class RootedReplacementGraph:
    """A finite directed acyclic graph of declared replacement relations.

    ``root_projection`` supplies the one exact source macro-law.  Edges are
    validated for action-alphabet agreement and total product-state coverage;
    output/action/successor preservation remains an edge-level assumption to be
    certified through the existing EXT transport APIs when that stronger claim is
    needed.
    """

    root: str
    root_projection: StageMacroProjection
    stages: tuple[ReplacementPathStage, ...]
    edges: tuple[ReplacementPathEdge, ...]

    @property
    def stage_map(self) -> dict[str, GrammarAwareControlledSystem]:
        return {stage.name: stage.system for stage in self.stages}

    def paths_to(self, terminal: str) -> tuple[Path, ...]:
        """Enumerate all root-to-terminal edge-index paths in the finite DAG."""
        if not self.verify():
            raise ValueError("replacement graph is not valid")
        if terminal not in self.stage_map:
            raise ValueError("terminal stage is absent from graph")
        paths: list[Path] = []

        def visit(node: str, prefix: Path) -> None:
            if node == terminal:
                paths.append(prefix)
                return
            for index, edge in enumerate(self.edges):
                if edge.source == node:
                    visit(edge.target, prefix + (index,))

        visit(self.root, ())
        if not paths:
            raise ValueError("terminal is not reachable from graph root")
        return tuple(paths)

    def compose_path(self, path: Path) -> tuple[Pair, ...]:
        """Compose one root-starting path into a relation to its terminal stage."""
        if not self.verify():
            raise ValueError("replacement graph is not valid")
        if not path:
            return _identity_relation(self.root_projection.constrained_system)
        current_node = self.root
        relation: tuple[Pair, ...] | None = None
        for edge_index in path:
            if not isinstance(edge_index, int) or isinstance(edge_index, bool) or not 0 <= edge_index < len(self.edges):
                raise ValueError("path contains an invalid edge index")
            edge = self.edges[edge_index]
            if edge.source != current_node:
                raise ValueError("path edges are not consecutive from the root")
            relation = edge.relation if relation is None else compose_relations(relation, edge.relation)
            current_node = edge.target
        if relation is None:
            raise AssertionError("nonempty path must yield a relation")
        validate_coverage(self.root_projection.constrained_system, self.stage_map[current_node], relation)
        return relation

    def path_terminal(self, path: Path) -> str:
        """Return the terminal stage name for a valid root-starting path."""
        if not path:
            return self.root
        current_node = self.root
        for edge_index in path:
            if not isinstance(edge_index, int) or isinstance(edge_index, bool) or not 0 <= edge_index < len(self.edges):
                raise ValueError("path contains an invalid edge index")
            edge = self.edges[edge_index]
            if edge.source != current_node:
                raise ValueError("path edges are not consecutive from the root")
            current_node = edge.target
        return current_node

    def verify(self) -> bool:
        try:
            if not self.root_projection.verify() or not isinstance(self.root, str) or not self.root:
                return False
            if not self.stages or not isinstance(self.edges, tuple):
                return False
            names = tuple(stage.name for stage in self.stages)
            if (
                any(not isinstance(stage.name, str) or not stage.name for stage in self.stages)
                or len(set(names)) != len(names)
                or self.root not in names
            ):
                return False
            systems = self.stage_map
            if systems[self.root] != self.root_projection.constrained_system:
                return False
            if len({(edge.source, edge.target) for edge in self.edges}) != len(self.edges):
                return False
            for edge in self.edges:
                if (
                    not isinstance(edge.source, str)
                    or not isinstance(edge.target, str)
                    or edge.source not in systems
                    or edge.target not in systems
                    or edge.source == edge.target
                ):
                    return False
                relation = normalize_relation(edge.relation)
                if relation != edge.relation:
                    return False
                validate_coverage(systems[edge.source], systems[edge.target], relation)

            outgoing: dict[str, tuple[str, ...]] = {
                name: tuple(edge.target for edge in self.edges if edge.source == name) for name in names
            }
            visiting: set[str] = set()
            visited: set[str] = set()

            def acyclic(node: str) -> bool:
                if node in visiting:
                    return False
                if node in visited:
                    return True
                visiting.add(node)
                for target in outgoing[node]:
                    if not acyclic(target):
                        return False
                visiting.remove(node)
                visited.add(node)
                return True

            if not acyclic(self.root):
                return False
            reached, frontier = {self.root}, [self.root]
            while frontier:
                current = frontier.pop()
                for target in outgoing[current]:
                    if target not in reached:
                        reached.add(target)
                        frontier.append(target)
            return reached == set(names)
        except (AssertionError, TypeError, ValueError):
            return False


def derive_root_carried_labels(
    root_projection: StageMacroProjection,
    terminal_system: GrammarAwareControlledSystem,
    relation: Iterable[Pair],
) -> tuple[int, ...]:
    """Carry root macro labels to one terminal through a composed relation."""
    if not root_projection.verify():
        raise ValueError("root projection must be exact")
    pairs = normalize_relation(relation)
    validate_coverage(root_projection.constrained_system, terminal_system, pairs)
    labels: list[int | None] = [None] * terminal_system.product_state_count
    for root_index, terminal_index in pairs:
        root_label = root_projection.summary_labels[root_index]
        old = labels[terminal_index]
        if old is None:
            labels[terminal_index] = root_label
        elif old != root_label:
            raise ValueError("one path maps distinct root macro labels into one terminal state")
    if any(label is None for label in labels):
        raise AssertionError("totality must assign every terminal state")
    return canonical_labels(tuple(int(label) for label in labels), terminal_system.product_state_count)


def path_carried_labels(graph: RootedReplacementGraph, terminal: str) -> tuple[tuple[int, ...], ...]:
    """Return root-carried terminal labels for every root-to-terminal path."""
    if not graph.verify():
        raise ValueError("replacement graph is not valid")
    terminal_system = graph.stage_map[terminal]
    return tuple(
        derive_root_carried_labels(graph.root_projection, terminal_system, graph.compose_path(path))
        for path in graph.paths_to(terminal)
    )


def path_label_coherent(graph: RootedReplacementGraph, terminal: str) -> bool:
    """Whether all declared root-to-terminal paths induce one carried partition."""
    try:
        labels = path_carried_labels(graph, terminal)
        return bool(labels) and all(current == labels[0] for current in labels[1:])
    except (AssertionError, TypeError, ValueError):
        return False


@dataclass(frozen=True)
class PathCoherentTransportCertificate:
    """A route-independent carried partition and minimal target repair.

    The certificate is deliberately relative to a chosen root exact projection
    and declared DAG of relations.  It proves neither that the relations were
    inferred from ecological data nor that every replacement path has equivalent
    biological meaning.
    """

    graph: RootedReplacementGraph
    terminal: str

    @property
    def paths(self) -> tuple[Path, ...]:
        return self.graph.paths_to(self.terminal)

    @property
    def path_relations(self) -> tuple[tuple[Pair, ...], ...]:
        return tuple(self.graph.compose_path(path) for path in self.paths)

    @property
    def labels_by_path(self) -> tuple[tuple[int, ...], ...]:
        return path_carried_labels(self.graph, self.terminal)

    @property
    def carried_labels(self) -> tuple[int, ...]:
        labels = self.labels_by_path
        if not labels or any(current != labels[0] for current in labels[1:]):
            raise ValueError("replacement histories are not path-label coherent")
        return labels[0]

    @property
    def refinement(self) -> RelativeExactRefinement:
        return relative_exact_refinement(self.graph.stage_map[self.terminal], self.carried_labels)

    @property
    def transport_defect_states(self) -> int:
        return self.refinement.refined_label_count - self.graph.root_projection.label_count

    @property
    def transport_defect_bits(self) -> float:
        return log2(self.refinement.refined_label_count) - log2(self.graph.root_projection.label_count)

    def verify(self) -> bool:
        try:
            if not self.graph.verify() or self.terminal not in self.graph.stage_map:
                return False
            labels = self.labels_by_path
            if len(labels) < 1 or any(current != labels[0] for current in labels[1:]):
                return False
            refinement = self.refinement
            return (
                refinement.verify()
                and max(labels[0]) + 1 == self.graph.root_projection.label_count
                and self.transport_defect_states == refinement.additional_macrostates
                and abs(self.transport_defect_bits - refinement.additional_memory_bits) < 1e-12
            )
        except (AssertionError, TypeError, ValueError):
            return False


def certify_path_coherent_transport(
    graph: RootedReplacementGraph,
    terminal: str,
) -> PathCoherentTransportCertificate:
    """Certify route-independent carried labels and relative exact repair."""
    certificate = PathCoherentTransportCertificate(graph, terminal)
    if not certificate.verify():
        raise ValueError("replacement graph does not yield a route-independent carried target partition")
    return certificate
