"""Finite witnesses for relative exact refinement and transport defect."""

from __future__ import annotations

from .finite import FiniteControlledOutputSystem, FinitePrefixGrammar, GrammarAwareControlledSystem
from .macro import StageMacroProjection
from .refinement import TransportDefectCertificate, certify_transport_defect


def _single_state_grammar(actions: tuple[str, ...], legal: tuple[bool, ...]) -> FinitePrefixGrammar:
    return FinitePrefixGrammar(actions, (tuple(0 if enabled else None for enabled in legal),))


def local_fiber_split_defect_witness() -> TransportDefectCertificate:
    """One target-only action forces one carried target fiber to split in two."""
    actions = ("stay", "reveal")
    source = StageMacroProjection(
        GrammarAwareControlledSystem(
            FiniteControlledOutputSystem(actions, ((0, 0), (1, 1)), (0, 1)),
            _single_state_grammar(actions, (True, False)),
        ),
        (0, 1),
    )
    target = GrammarAwareControlledSystem(
        FiniteControlledOutputSystem(actions, ((0, 0), (1, 2), (2, 2)), (0, 0, 1)),
        _single_state_grammar(actions, (True, True)),
    )
    certificate = certify_transport_defect(source, target, ((0, 0), (0, 1), (1, 2)))
    if certificate.carried_labels != (0, 0, 1):
        raise AssertionError("unexpected carried partition")
    if certificate.refinement.refined_label_count != 3:
        raise AssertionError("local split witness did not require three target labels")
    return certificate


def accumulating_transport_defect_witness(module_count: int) -> TransportDefectCertificate:
    """A binary family with an exponentially growing target repair count.

    The source has two macrostates, ``low`` and ``high``, and only ``reset`` is
    legal. The target has one low state for every binary vector
    ``(b_1,...,b_m)`` and one high state. Every newly legal ``probe_i`` exposes
    bit ``b_i`` by moving to the high state iff that bit is one. The carried low
    macrostate therefore refines into all ``2**m`` binary target states.
    """
    if not isinstance(module_count, int) or isinstance(module_count, bool) or module_count < 1:
        raise ValueError("module_count must be a positive integer")
    actions = ("reset",) + tuple(f"probe_{index}" for index in range(module_count))
    source = StageMacroProjection(
        GrammarAwareControlledSystem(
            FiniteControlledOutputSystem(
                actions,
                (
                    (0,) + (0,) * module_count,
                    (0,) + (1,) * module_count,
                ),
                (0, 1),
            ),
            _single_state_grammar(actions, (True,) + (False,) * module_count),
        ),
        (0, 1),
    )

    low_state_count = 1 << module_count
    high_state = low_state_count
    target_rows = []
    for mask in range(low_state_count):
        target_rows.append(
            (0,) + tuple(high_state if mask & (1 << bit) else 0 for bit in range(module_count))
        )
    target_rows.append((0,) + (high_state,) * module_count)
    target = GrammarAwareControlledSystem(
        FiniteControlledOutputSystem(actions, tuple(target_rows), (0,) * low_state_count + (1,)),
        _single_state_grammar(actions, (True,) * len(actions)),
    )
    relation = tuple((0, target_index) for target_index in range(low_state_count)) + ((1, high_state),)
    certificate = certify_transport_defect(source, target, relation)
    expected_target_count = low_state_count + 1
    if certificate.target_macrostate_count != expected_target_count:
        raise AssertionError("binary target repair count is not sharp")
    if certificate.transport_defect_states != low_state_count - 1:
        raise AssertionError("unexpected transport defect state count")
    return certificate
