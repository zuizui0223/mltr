"""Exact transport of finite macro-laws across non-nested ecological replacement.

The public API deliberately contains only the replacement/rewiring theorem
program.  It does not re-export the RACH open-composition lower bound,
identifiability companions, or experimental-design shelves.
"""

from .finite import FiniteControlledOutputSystem, FinitePrefixGrammar, GrammarAwareControlledSystem
from .macro import ConservativeMacroSchema, PortableMacroDynamics, StageMacroProjection
from .transport import (
    ConservativeTransportedSchemaCertificate,
    ReplacementFiberSplitObstructionCertificate,
    ReplacementTransport,
    TransportCoherentMacroLawCertificate,
    TransportedTargetProjectionCertificate,
    certify_conservative_transported_schema,
    certify_transport_coherent_macro_law,
    certify_transported_target_projection,
    conservative_transport_witness,
    derived_target_projection_witness,
    many_to_one_replacement_witness,
    new_action_fiber_split_witness,
)

__all__ = [
    "FiniteControlledOutputSystem",
    "FinitePrefixGrammar",
    "GrammarAwareControlledSystem",
    "PortableMacroDynamics",
    "ConservativeMacroSchema",
    "StageMacroProjection",
    "ReplacementTransport",
    "TransportedTargetProjectionCertificate",
    "TransportCoherentMacroLawCertificate",
    "ConservativeTransportedSchemaCertificate",
    "ReplacementFiberSplitObstructionCertificate",
    "certify_transported_target_projection",
    "certify_transport_coherent_macro_law",
    "certify_conservative_transported_schema",
    "many_to_one_replacement_witness",
    "derived_target_projection_witness",
    "conservative_transport_witness",
    "new_action_fiber_split_witness",
]
