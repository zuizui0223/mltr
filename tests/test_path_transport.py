import math

import pytest

from ext_transport.path_transport import (
    ReplacementPathEdge,
    ReplacementPathStage,
    RootedReplacementGraph,
    certify_path_coherent_transport,
    compose_relations,
    path_carried_labels,
    path_label_coherent,
)
from ext_transport.path_witnesses import coherent_defect_diamond_witness, incoherent_label_diamond_witness


def test_relation_composition_is_sorted_and_deduplicated():
    assert compose_relations(((0, 0), (0, 1), (1, 1)), ((0, 2), (1, 2), (1, 3))) == (
        (0, 2),
        (0, 3),
        (1, 2),
        (1, 3),
    )


def test_coherent_diamond_has_one_carried_partition_and_one_minimal_repair():
    certificate = coherent_defect_diamond_witness()
    assert certificate.verify()
    assert certificate.paths == ((0, 1), (2, 3))
    assert certificate.labels_by_path == ((0, 0, 1), (0, 0, 1))
    assert certificate.carried_labels == (0, 0, 1)
    assert certificate.refinement.refined_labels == (0, 1, 2)
    assert certificate.transport_defect_states == 1
    assert math.isclose(certificate.transport_defect_bits, math.log2(3) - 1)


def test_coherent_diamond_composes_the_same_root_to_terminal_relation_by_both_routes():
    certificate = coherent_defect_diamond_witness()
    assert certificate.path_relations == (
        ((0, 0), (0, 1), (1, 2)),
        ((0, 0), (0, 1), (1, 2)),
    )


def test_incoherent_diamond_exposes_history_dependent_carried_labels():
    witness = incoherent_label_diamond_witness()
    assert witness.verify()
    assert path_carried_labels(witness.graph, witness.terminal) == ((0, 1), (1, 0))
    assert not path_label_coherent(witness.graph, witness.terminal)
    with pytest.raises(ValueError):
        certify_path_coherent_transport(witness.graph, witness.terminal)


def test_graph_rejects_cycles_and_unreachable_stages():
    witness = incoherent_label_diamond_witness()
    graph = witness.graph
    cyclic = RootedReplacementGraph(
        root=graph.root,
        root_projection=graph.root_projection,
        stages=graph.stages,
        edges=graph.edges + (ReplacementPathEdge("terminal", "root", ((0, 0), (1, 1))),),
    )
    assert not cyclic.verify()

    unreachable = RootedReplacementGraph(
        root=graph.root,
        root_projection=graph.root_projection,
        stages=graph.stages + (ReplacementPathStage("orphan", graph.stage_map["terminal"]),),
        edges=graph.edges,
    )
    assert not unreachable.verify()
