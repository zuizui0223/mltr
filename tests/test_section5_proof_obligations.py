import itertools

from ext_transport.history_augmentation import (
    history_assignment_is_compatible,
    minimum_history_mode_assignment,
)
from ext_transport.path_transport import path_label_coherent
from ext_transport.path_witnesses import coherent_defect_diamond_witness


def _canonical(labels):
    mapping = {}
    out = []
    for value in labels:
        if value not in mapping:
            mapping[value] = len(mapping)
        out.append(mapping[value])
    return tuple(out)


def test_minimum_history_modes_equal_number_of_distinct_canonical_maps_for_small_families():
    maps = (
        (0, 0, 1),
        (4, 4, 9),  # same canonical carried map as (0,0,1)
        (0, 1, 0),
        (0, 1, 2),
    )
    for size in range(1, 5):
        for family in itertools.product(maps, repeat=size):
            modes, assignment = minimum_history_mode_assignment(family, 3)
            canonical_family = tuple(_canonical(labels) for labels in family)
            assert len(modes) == len(set(canonical_family))
            assert history_assignment_is_compatible(family, assignment, 3)
            for left in range(size):
                for right in range(size):
                    assert (assignment[left] == assignment[right]) == (
                        canonical_family[left] == canonical_family[right]
                    )


def test_any_assignment_using_fewer_modes_than_distinct_maps_is_incompatible():
    family = ((0, 0, 1), (0, 1, 0), (0, 1, 2))
    modes, assignment = minimum_history_mode_assignment(family, 3)
    assert len(modes) == 3
    assert assignment == (0, 1, 2)

    for candidate in itertools.product(range(2), repeat=len(family)):
        if set(candidate) != {0, 1}:
            continue
        assert not history_assignment_is_compatible(family, candidate, 3)


def test_minimum_assignment_is_invariant_to_path_order_up_to_mode_renaming():
    family = ((0, 1, 2), (0, 0, 1), (0, 1, 2), (0, 1, 0))
    base_modes, base_assignment = minimum_history_mode_assignment(family, 3)
    base_partition = {
        frozenset(i for i, mode in enumerate(base_assignment) if mode == m)
        for m in set(base_assignment)
    }

    for permutation in itertools.permutations(range(len(family))):
        permuted = tuple(family[i] for i in permutation)
        _modes, assignment = minimum_history_mode_assignment(permuted, 3)
        pulled_back = {
            frozenset(permutation[i] for i, mode in enumerate(assignment) if mode == m)
            for m in set(assignment)
        }
        assert pulled_back == base_partition
        assert len(_modes) == len(base_modes)


def test_canonical_relabeling_does_not_create_spurious_history_modes():
    family = (
        (10, 10, 20, 20),
        (0, 0, 1, 1),
        (7, 8, 7, 8),
        (2, 3, 2, 3),
    )
    modes, assignment = minimum_history_mode_assignment(family, 4)
    assert len(modes) == 2
    assert assignment[0] == assignment[1]
    assert assignment[2] == assignment[3]
    assert assignment[0] != assignment[2]


def test_path_coherence_is_exactly_single_history_mode_on_known_coherent_witness():
    certificate = coherent_defect_diamond_witness()
    assert path_label_coherent(certificate.graph, certificate.terminal)
    modes, assignment = minimum_history_mode_assignment(
        certificate.labels_by_path,
        certificate.graph.stage_map[certificate.terminal].product_state_count,
    )
    assert len(modes) == 1
    assert set(assignment) == {0}
