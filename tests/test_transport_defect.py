import math

import pytest

from ext_transport.conservative import certify_conservative_transported_schema
from ext_transport.defect_witnesses import (
    accumulating_transport_defect_witness,
    local_fiber_split_defect_witness,
)
from ext_transport.exact import is_exact_interface
from ext_transport.refinement import certify_transport_defect, is_refinement
from ext_transport.witnesses import conservative_transport_witness


def _canonical_partitions(count: int):
    """Enumerate partitions in first-occurrence canonical label form."""
    def extend(prefix, maximum):
        if len(prefix) == count:
            yield tuple(prefix)
            return
        for label in range(maximum + 2):
            yield from extend(prefix + [label], max(maximum, label))

    yield from extend([0], 0)


def test_zero_defect_when_conservative_transport_is_already_exact():
    base = conservative_transport_witness()
    certificate = certify_transport_defect(base.source, base.target_system, base.relation)
    assert certificate.verify()
    assert certificate.transport_defect_states == 0
    assert certificate.transport_defect_bits == 0.0
    assert certificate.refinement.refinement_rounds == 0
    assert certificate.repaired_target_projection.summary_labels == certificate.carried_labels


def test_local_new_action_split_has_one_required_target_refinement():
    certificate = local_fiber_split_defect_witness()
    refinement = certificate.refinement
    assert certificate.verify()
    assert certificate.carried_labels == (0, 0, 1)
    assert refinement.refined_labels == (0, 1, 2)
    assert refinement.fiber_split_profile == (2, 1)
    assert certificate.transport_defect_states == 1
    assert math.isclose(certificate.transport_defect_bits, math.log2(3) - 1)
    assert certificate.repaired_target_projection.verify()


def test_local_repair_is_minimal_among_all_exact_refinements_of_carried_partition():
    certificate = local_fiber_split_defect_witness()
    target = certificate.target_system
    carried = certificate.carried_labels
    exact_refining_counts = []
    for labels in _canonical_partitions(target.product_state_count):
        if is_refinement(labels, carried, target.product_state_count) and is_exact_interface(target, labels):
            exact_refining_counts.append(max(labels) + 1)
    assert exact_refining_counts
    assert min(exact_refining_counts) == certificate.target_macrostate_count == 3


@pytest.mark.parametrize("module_count", [1, 2, 3, 4])
def test_accumulating_family_has_sharp_exponential_state_defect(module_count):
    certificate = accumulating_transport_defect_witness(module_count)
    low_state_count = 1 << module_count
    assert certificate.verify()
    assert certificate.source_macrostate_count == 2
    assert certificate.target_macrostate_count == low_state_count + 1
    assert certificate.transport_defect_states == low_state_count - 1
    assert math.isclose(certificate.transport_defect_bits, math.log2(low_state_count + 1) - 1)
    assert certificate.refinement.fiber_split_profile == (low_state_count, 1)
    assert certificate.refinement.refinement_rounds == 1


def test_transport_defect_rejects_relation_that_does_not_preserve_old_actions():
    base = local_fiber_split_defect_witness()
    with pytest.raises(ValueError):
        certify_transport_defect(base.source, base.target_system, ((0, 0), (1, 2)))
