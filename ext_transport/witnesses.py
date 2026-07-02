"""Small finite witnesses for the EXT theorem program."""

from __future__ import annotations

from .conservative import ConservativeTransportedSchemaCertificate, certify_conservative_transported_schema
from .finite import FiniteControlledOutputSystem, FinitePrefixGrammar, GrammarAwareControlledSystem
from .macro import PortableMacroDynamics, StageMacroProjection
from .obstruction import ReplacementFiberSplitObstructionCertificate
from .relation_transport import (
    ReplacementTransport,
    TransportCoherentMacroLawCertificate,
    TransportedTargetProjectionCertificate,
    certify_transport_coherent_macro_law,
    certify_transported_target_projection,
)


def _grammar(actions: tuple[str, ...], allowed: tuple[bool, ...]) -> FinitePrefixGrammar:
    return FinitePrefixGrammar(actions, (tuple(0 if value else None for value in allowed),))


def many_to_one_replacement_witness() -> TransportCoherentMacroLawCertificate:
    """Three source states contract to two target states without an embedding."""
    actions = ("flip",)
    macro = PortableMacroDynamics(actions, ("low", "high"), (actions, actions), ((1,), (0,)))
    grammar = _grammar(actions, (True,))
    source = StageMacroProjection(
        GrammarAwareControlledSystem(
            FiniteControlledOutputSystem(actions, ((2,), (2,), (0,)), ("low", "low", "high")),
            grammar,
        ),
        (0, 0, 1),
    )
    target = StageMacroProjection(
        GrammarAwareControlledSystem(
            FiniteControlledOutputSystem(actions, ((1,), (0,)), ("low", "high")),
            grammar,
        ),
        (0, 1),
    )
    relation = ReplacementTransport(source, target, ((0, 0), (1, 0), (2, 1)))
    certificate = certify_transport_coherent_macro_law(macro, (source, target), (relation,))
    if relation.is_source_to_target_injection:
        raise AssertionError("the witness must not be an embedding")
    return certificate


def derived_target_projection_witness() -> TransportedTargetProjectionCertificate:
    base = many_to_one_replacement_witness()
    relation = base.transports[0]
    certificate = certify_transported_target_projection(
        relation.source,
        relation.target.constrained_system,
        relation.relation,
    )
    if certificate.target_labels != relation.target.summary_labels:
        raise AssertionError("derived labels differ from explicit replacement witness")
    return certificate


def conservative_transport_witness() -> ConservativeTransportedSchemaCertificate:
    """A target-only reveal action is uniform in every transported fiber."""
    actions = ("flip", "reveal")
    source = StageMacroProjection(
        GrammarAwareControlledSystem(
            FiniteControlledOutputSystem(actions, ((2, 0), (2, 1), (0, 2)), ("low", "low", "high")),
            _grammar(actions, (True, False)),
        ),
        (0, 0, 1),
    )
    target = GrammarAwareControlledSystem(
        FiniteControlledOutputSystem(actions, ((1, 1), (0, 1)), ("low", "high")),
        _grammar(actions, (True, True)),
    )
    certificate = certify_conservative_transported_schema(source, target, ((0, 0), (1, 0), (2, 1)))
    if certificate.target_labels != (0, 1) or certificate.schema.transition_rows != ((1, 1), (0, 1)):
        raise AssertionError("unexpected conservative witness schema")
    return certificate


def new_action_fiber_split_witness() -> ReplacementFiberSplitObstructionCertificate:
    """Reveal is illegal before replacement but separates one carried target fiber."""
    actions = ("stay", "reveal")
    source = StageMacroProjection(
        GrammarAwareControlledSystem(
            FiniteControlledOutputSystem(actions, ((0, 0), (1, 1), (2, 2), (3, 3)), (0, 0, 0, 0)),
            _grammar(actions, (True, False)),
        ),
        (0, 0, 0, 0),
    )
    target = GrammarAwareControlledSystem(
        FiniteControlledOutputSystem(actions, ((0, 0), (1, 2), (2, 2)), (0, 0, 1)),
        _grammar(actions, (True, True)),
    )
    certificate = ReplacementFiberSplitObstructionCertificate(
        source=source,
        target_system=target,
        proposed_target_labels=(0, 0, 1),
        relation=((0, 0), (1, 1), (2, 0), (3, 1)),
        left_source_index=0,
        right_source_index=1,
        future_word=("reveal",),
    )
    if not certificate.verify():
        raise AssertionError("fiber split witness did not verify")
    return certificate
