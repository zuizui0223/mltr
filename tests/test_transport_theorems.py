import pytest

from ext_transport.conservative import certify_conservative_transported_schema
from ext_transport.finite import FiniteControlledOutputSystem, FinitePrefixGrammar, GrammarAwareControlledSystem
from ext_transport.macro import StageMacroProjection
from ext_transport.relation_transport import certify_transported_target_projection
from ext_transport.witnesses import (
    conservative_transport_witness,
    derived_target_projection_witness,
    many_to_one_replacement_witness,
    new_action_fiber_split_witness,
)


def _grammar(actions, rows):
    return FinitePrefixGrammar(actions, rows)


def test_many_to_one_replacement_preserves_one_exact_macro_law_without_embedding():
    certificate = many_to_one_replacement_witness()
    transport = certificate.transports[0]
    assert certificate.verify()
    assert transport.verify()
    assert not transport.is_source_to_target_injection
    assert transport.source.constrained_system.product_state_count == 3
    assert transport.target.constrained_system.product_state_count == 2
    assert certificate.macro.state_count == 2


def test_target_projection_is_constructed_from_relation_not_supplied_as_input():
    certificate = derived_target_projection_witness()
    assert certificate.verify()
    assert certificate.target_labels == (0, 1)
    assert certificate.target_projection.induced_macro() == certificate.source.induced_macro()


def test_label_inconsistent_target_fiber_cannot_receive_a_derived_projection():
    base = many_to_one_replacement_witness()
    transport = base.transports[0]
    with pytest.raises(ValueError):
        certify_transported_target_projection(
            transport.source,
            transport.target.constrained_system,
            ((0, 0), (1, 1), (2, 0)),
        )


def test_target_only_action_can_be_transported_when_uniform_inside_each_fiber():
    certificate = conservative_transport_witness()
    assert certificate.verify()
    assert certificate.target_labels == (0, 1)
    assert certificate.schema.transition_rows == ((1, 1), (0, 1))


def test_nonuniform_target_only_action_availability_rejects_the_proposed_transport():
    actions = ("flip", "reveal")
    source = StageMacroProjection(
        GrammarAwareControlledSystem(
            FiniteControlledOutputSystem(actions, ((2, 0), (2, 1), (0, 2)), ("low", "low", "high")),
            _grammar(actions, ((0, None),)),
        ),
        (0, 0, 1),
    )
    target = GrammarAwareControlledSystem(
        FiniteControlledOutputSystem(actions, ((1, 0), (0, 1)), ("low", "high")),
        _grammar(actions, ((0, 0), (1, None))),
    )
    relation = ((0, 0), (0, 1), (1, 0), (2, 2), (2, 3))
    with pytest.raises(ValueError):
        certify_conservative_transported_schema(source, target, relation)


def test_nonuniform_target_only_successor_rejects_the_proposed_transport():
    actions = ("flip", "reveal")
    source = StageMacroProjection(
        GrammarAwareControlledSystem(
            FiniteControlledOutputSystem(actions, ((2, 0), (2, 1), (0, 2)), ("low", "low", "high")),
            _grammar(actions, ((0, None),)),
        ),
        (0, 0, 1),
    )
    target = GrammarAwareControlledSystem(
        FiniteControlledOutputSystem(actions, ((2, 0), (2, 2), (0, 2)), ("low", "low", "high")),
        _grammar(actions, ((0, 0),)),
    )
    with pytest.raises(ValueError):
        certify_conservative_transported_schema(source, target, ((0, 0), (1, 1), (2, 2)))


def test_newly_legal_word_refutes_only_the_carried_merge():
    certificate = new_action_fiber_split_witness()
    assert certificate.verify()
    assert certificate.future_word == ("reveal",)
    assert certificate.proposed_target_labels[0] == certificate.proposed_target_labels[1]


def test_exact_stage_rejects_a_merge_with_different_current_outputs():
    actions = ("stay",)
    stage = StageMacroProjection(
        GrammarAwareControlledSystem(
            FiniteControlledOutputSystem(actions, ((0,), (1,)), (0, 1)),
            _grammar(actions, ((0,),)),
        ),
        (0, 0),
    )
    assert not stage.verify()
