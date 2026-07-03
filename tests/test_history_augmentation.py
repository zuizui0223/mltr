import math

from ext_transport.history_augmentation import (
    certify_history_augmentation,
    history_assignment_is_compatible,
    history_augmented_terminal_system,
    minimum_history_mode_assignment,
)
from ext_transport.history_witnesses import (
    coherent_history_augmentation_witness,
    incoherent_history_augmentation_witness,
)
from ext_transport.path_witnesses import incoherent_label_diamond_witness


def test_minimum_history_assignment_groups_only_equal_carried_maps():
    maps, assignment = minimum_history_mode_assignment(((0, 1), (1, 0), (0, 1)), 2)
    assert maps == ((0, 1), (1, 0))
    assert assignment == (0, 1, 0)
    assert history_assignment_is_compatible(((0, 1), (1, 0), (0, 1)), assignment, 2)
    assert not history_assignment_is_compatible(((0, 1), (1, 0), (0, 1)), (0, 0, 0), 2)


def test_coherent_histories_need_no_extra_context_and_keep_known_repair():
    certificate = coherent_history_augmentation_witness()
    assert certificate.verify()
    assert certificate.minimum_history_mode_count == 1
    assert certificate.additional_history_modes == 0
    assert certificate.history_augmentation_bits == 0.0
    assert certificate.augmented_system == certificate.terminal_system
    assert certificate.history_aware_macrostate_count == 3
    assert certificate.history_aware_defect_states == 1
    assert math.isclose(certificate.history_aware_defect_bits, math.log2(3) - 1)


def test_incoherent_histories_require_two_minimum_modes_and_exact_repair():
    certificate = incoherent_history_augmentation_witness()
    assert certificate.verify()
    assert certificate.minimum_history_mode_count == 2
    assert certificate.additional_history_modes == 1
    assert certificate.path_history_modes == (0, 1)
    assert certificate.augmented_system.product_state_count == 4
    assert certificate.augmented_carried_labels == (0, 1, 1, 0)
    assert certificate.refinement.refined_labels == (0, 1, 2, 3)
    assert certificate.history_aware_macrostate_count == 4
    assert certificate.history_aware_defect_states == 2
    assert math.isclose(certificate.history_augmentation_bits, 1.0)
    assert math.isclose(certificate.history_aware_defect_bits, 1.0)


def test_history_slice_copies_terminal_dynamics_without_changing_grammar():
    witness = incoherent_label_diamond_witness()
    terminal = witness.graph.stage_map[witness.terminal]
    augmented = history_augmented_terminal_system(terminal, 2)
    assert augmented.system.actions == terminal.system.actions
    assert augmented.grammar == terminal.grammar
    assert augmented.system.outputs == ("low", "high", "low", "high")
    assert augmented.system.transition_table == ((0,), (1,), (2,), (3,))


def test_generic_certificate_accepts_path_incoherence_by_augmenting_history():
    witness = incoherent_label_diamond_witness()
    certificate = certify_history_augmentation(witness.graph, witness.terminal)
    assert certificate.verify()
    assert certificate.labels_by_path == ((0, 1), (1, 0))
