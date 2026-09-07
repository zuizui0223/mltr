import pytest

from ext_transport.compositional_transport import (
    carried_label_conflicts,
    certify_carried_label_composition,
    derive_carried_labels,
)
from ext_transport.path_witnesses import (
    coherent_defect_diamond_witness,
    incoherent_label_diamond_witness,
)


def _identity(size: int) -> tuple[tuple[int, int], ...]:
    return tuple((index, index) for index in range(size))


def test_direct_and_sequential_transport_commute_on_coherent_route():
    witness = coherent_defect_diamond_witness()
    graph = witness.graph
    certificate = certify_carried_label_composition(
        source_projection=graph.root_projection,
        intermediate_system=graph.stage_map["left"],
        terminal_system=graph.stage_map["terminal"],
        first_relation=graph.edges[0].relation,
        second_relation=graph.edges[1].relation,
    )

    assert certificate.verify()
    assert certificate.direct_defined
    assert certificate.sequential_defined
    assert certificate.commutes
    assert certificate.intermediate_labels == (0, 0, 1)
    assert certificate.direct_terminal_labels == (0, 0, 1)
    assert certificate.sequential_terminal_labels == (0, 0, 1)


def test_composition_preserves_inherited_label_identity_under_state_swap():
    witness = incoherent_label_diamond_witness()
    graph = witness.graph
    certificate = certify_carried_label_composition(
        source_projection=graph.root_projection,
        intermediate_system=graph.stage_map["right"],
        terminal_system=graph.stage_map["terminal"],
        first_relation=graph.edges[2].relation,
        second_relation=graph.edges[3].relation,
    )

    assert certificate.verify()
    assert certificate.commutes
    assert certificate.intermediate_labels == (0, 1)
    assert certificate.direct_terminal_labels == (1, 0)
    assert certificate.sequential_terminal_labels == (1, 0)

    # The inherited source labels themselves are not silently renumbered by the
    # target state order.
    assert derive_carried_labels(
        graph.root_projection.summary_labels,
        graph.root_projection.constrained_system,
        graph.stage_map["terminal"],
        ((0, 1), (1, 0)),
    ) == (1, 0)


def test_first_edge_label_conflict_forces_direct_composite_conflict():
    witness = coherent_defect_diamond_witness()
    graph = witness.graph
    intermediate = graph.stage_map["left"]
    terminal = graph.stage_map["terminal"]

    # Source labels are (0, 1). Target state 0 receives both source states, so
    # the inherited carried meaning is undefined already on the first edge.
    conflicting_first = ((0, 0), (0, 1), (1, 0), (1, 2))
    certificate = certify_carried_label_composition(
        source_projection=graph.root_projection,
        intermediate_system=intermediate,
        terminal_system=terminal,
        first_relation=conflicting_first,
        second_relation=_identity(terminal.product_state_count),
    )

    assert certificate.verify()
    assert not certificate.sequential_defined
    assert not certificate.direct_defined
    assert certificate.first_conflicts[0].target_index == 0
    assert certificate.first_conflicts[0].source_labels == (0, 1)
    assert certificate.direct_conflicts[0].source_labels == (0, 1)
    with pytest.raises(ValueError):
        _ = certificate.intermediate_labels


def test_second_edge_label_conflict_is_exactly_visible_in_direct_composite():
    witness = coherent_defect_diamond_witness()
    graph = witness.graph
    intermediate = graph.stage_map["left"]
    terminal = graph.stage_map["terminal"]

    # The valid first carry gives intermediate labels (0, 0, 1). The second
    # relation sends intermediate states 0 and 2 into terminal state 0, creating
    # a 0/1 inherited-label conflict there.
    conflicting_second = ((0, 0), (1, 1), (2, 0), (2, 2))
    certificate = certify_carried_label_composition(
        source_projection=graph.root_projection,
        intermediate_system=intermediate,
        terminal_system=terminal,
        first_relation=graph.edges[0].relation,
        second_relation=conflicting_second,
    )

    assert certificate.verify()
    assert certificate.first_conflicts == ()
    assert certificate.intermediate_labels == (0, 0, 1)
    assert certificate.second_conflicts is not None
    assert certificate.second_conflicts[0].target_index == 0
    assert certificate.second_conflicts[0].source_labels == (0, 1)
    assert not certificate.sequential_defined
    assert not certificate.direct_defined
    assert certificate.direct_conflicts[0].target_index == 0


def test_conflict_api_reports_all_inherited_labels_at_target_state():
    witness = coherent_defect_diamond_witness()
    graph = witness.graph
    conflicts = carried_label_conflicts(
        graph.root_projection.summary_labels,
        graph.root_projection.constrained_system,
        graph.stage_map["left"],
        ((0, 0), (0, 1), (1, 0), (1, 2)),
    )
    assert len(conflicts) == 1
    assert conflicts[0].target_index == 0
    assert conflicts[0].source_indices == (0, 1)
    assert conflicts[0].source_labels == (0, 1)
