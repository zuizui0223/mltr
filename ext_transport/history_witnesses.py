"""Finite witnesses for history augmentation."""

from __future__ import annotations

from .history_augmentation import HistoryAugmentationCertificate, certify_history_augmentation
from .path_witnesses import coherent_defect_diamond_witness, incoherent_label_diamond_witness


def coherent_history_augmentation_witness() -> HistoryAugmentationCertificate:
    route_certificate = coherent_defect_diamond_witness()
    certificate = certify_history_augmentation(route_certificate.graph, "terminal")
    if certificate.minimum_history_mode_count != 1:
        raise AssertionError("coherent witness needs one history mode")
    if certificate.augmented_carried_labels != (0, 0, 1):
        raise AssertionError("unexpected coherent carried labels")
    if certificate.refinement.refined_labels != (0, 1, 2):
        raise AssertionError("unexpected coherent repair")
    return certificate


def incoherent_history_augmentation_witness() -> HistoryAugmentationCertificate:
    path_witness = incoherent_label_diamond_witness()
    certificate = certify_history_augmentation(path_witness.graph, path_witness.terminal)
    if certificate.history_label_maps != ((0, 1), (1, 0)):
        raise AssertionError("unexpected history label maps")
    if certificate.path_history_modes != (0, 1):
        raise AssertionError("unexpected path-mode assignment")
    if certificate.augmented_carried_labels != (0, 1, 1, 0):
        raise AssertionError("unexpected augmented carried labels")
    if certificate.refinement.refined_labels != (0, 1, 2, 3):
        raise AssertionError("unexpected history repair")
    return certificate
