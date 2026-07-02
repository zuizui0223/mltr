"""Exact transport of finite macro-laws across non-nested ecological replacement.

The public API contains only the replacement/rewiring theorem program. It does
not re-export RACH's open-composition lower bound, identifiability companions,
or experimental-design shelves.
"""

from .conservative import ConservativeTransportedSchemaCertificate, certify_conservative_transported_schema
from .defect_witnesses import accumulating_transport_defect_witness, local_fiber_split_defect_witness
from .finite import FiniteControlledOutputSystem, FinitePrefixGrammar, GrammarAwareControlledSystem
from .macro import ConservativeMacroSchema, PortableMacroDynamics, StageMacroProjection
from .obstruction import ReplacementFiberSplitObstructionCertificate
from .refinement import (
    RelativeExactRefinement,
    TransportDefectCertificate,
    certify_transport_defect,
    is_refinement,
    relative_exact_refinement,
)
from .relation_transport import (
    ReplacementTransport,
    TransportCoherentMacroLawCertificate,
    TransportedTargetProjectionCertificate,
    certify_transport_coherent_macro_law,
    certify_transported_target_projection,
)
from .witnesses import (
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
    "RelativeExactRefinement",
    "TransportDefectCertificate",
    "certify_transported_target_projection",
    "certify_transport_coherent_macro_law",
    "certify_conservative_transported_schema",
    "relative_exact_refinement",
    "is_refinement",
    "certify_transport_defect",
    "many_to_one_replacement_witness",
    "derived_target_projection_witness",
    "conservative_transport_witness",
    "new_action_fiber_split_witness",
    "local_fiber_split_defect_witness",
    "accumulating_transport_defect_witness",
]