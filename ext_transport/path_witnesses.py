"""Finite diamonds for path-label coherence and history dependence."""

from __future__ import annotations

from dataclasses import dataclass

from .defect_witnesses import local_fiber_split_defect_witness
from .finite import FiniteControlledOutputSystem, FinitePrefixGrammar, GrammarAwareControlledSystem
from .macro import StageMacroProjection
from .path_transport import (
    PathCoherentTransportCertificate,
    ReplacementPathEdge,
    ReplacementPathStage,
    RootedReplacementGraph,
    certify_path_coherent_transport,
    path_carried_labels,
    path_label_coherent,
)


def _identity(size: int) -> tuple[tuple[int, int], ...]:
    return tuple((index, index) for index in range(size))


def coherent_defect_diamond_witness() -> PathCoherentTransportCertificate:
    """Two replacement histories yield one carried partition and one repair.

    Both branches carry the existing local conservative defect relation from a
    two-state source to a three-state target.  Thus each route yields
    ``(0, 0, 1)`` and its coarsest exact repair ``(0, 1, 2)``.
    """
    defect = local_fiber_split_defect_witness()
    root = defect.source
    target = defect.target_system
    relation = defect.relation
    graph = RootedReplacementGraph(
        root="root",
        root_projection=root,
        stages=(
            ReplacementPathStage("root", root.constrained_system),
            ReplacementPathStage("left", target),
            ReplacementPathStage("right", target),
            ReplacementPathStage("terminal", target),
        ),
        edges=(
            ReplacementPathEdge("root", "left", relation),
            ReplacementPathEdge("left", "terminal", _identity(target.product_state_count)),
            ReplacementPathEdge("root", "right", relation),
            ReplacementPathEdge("right", "terminal", _identity(target.product_state_count)),
        ),
    )
    certificate = certify_path_coherent_transport(graph, "terminal")
    if certificate.carried_labels != (0, 0, 1):
        raise AssertionError("coherent diamond carried unexpected labels")
    if certificate.refinement.refined_labels != (0, 1, 2):
        raise AssertionError("coherent diamond repair is not the local split repair")
    return certificate


@dataclass(frozen=True)
class PathIncoherenceWitness:
    """A finite diamond whose declared paths assign different root labels."""

    graph: RootedReplacementGraph
    terminal: str

    @property
    def labels_by_path(self) -> tuple[tuple[int, ...], ...]:
        return path_carried_labels(self.graph, self.terminal)

    def verify(self) -> bool:
        try:
            return (
                self.graph.verify()
                and len(self.labels_by_path) == 2
                and self.labels_by_path[0] != self.labels_by_path[1]
                and not path_label_coherent(self.graph, self.terminal)
            )
        except (AssertionError, TypeError, ValueError):
            return False


def incoherent_label_diamond_witness() -> PathIncoherenceWitness:
    """A boundary witness: relation coverage alone does not ensure coherence.

    The right-hand edge swaps two terminal product states, so the same terminal
    raw states inherit ``(0, 1)`` along one route and ``(1, 0)`` along another.
    This witness intentionally checks only the graph-level declared-relation
    assumptions; the swapped edge is not an edge-level exact transport
    certificate. It shows why path-label coherence is an additional condition.
    """
    actions = ("stay",)
    grammar = FinitePrefixGrammar(actions, ((0,),))
    system = GrammarAwareControlledSystem(
        FiniteControlledOutputSystem(actions, ((0,), (1,)), ("low", "high")),
        grammar,
    )
    root = StageMacroProjection(system, (0, 1))
    graph = RootedReplacementGraph(
        root="root",
        root_projection=root,
        stages=(
            ReplacementPathStage("root", system),
            ReplacementPathStage("left", system),
            ReplacementPathStage("right", system),
            ReplacementPathStage("terminal", system),
        ),
        edges=(
            ReplacementPathEdge("root", "left", _identity(2)),
            ReplacementPathEdge("left", "terminal", _identity(2)),
            ReplacementPathEdge("root", "right", _identity(2)),
            ReplacementPathEdge("right", "terminal", ((0, 1), (1, 0))),
        ),
    )
    witness = PathIncoherenceWitness(graph, "terminal")
    if not witness.verify():
        raise AssertionError("incoherent diamond did not expose route-dependent labels")
    return witness
