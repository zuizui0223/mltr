"""Exact transport of finite macro-laws across non-nested ecological replacement.

The public API contains only the replacement/rewiring theorem program. It does
not re-export RACH's open-composition lower bound, identifiability companions,
or experimental-design shelves.
"""

from .conservative import ConservativeTransportedSchemaCertificate, certify_conservative_transported_schema
from .defect_witnesses import accumulating_transport_defect_witness, local_fiber_split_defect_witness
from .finite import FiniteControlledOutputSystem, FinitePrefixGrammar, GrammarAwareControlledSystem
from .history_augmentation import (
    HistoryAugmentationCertificate,
    certify_history_augmentation,
    history_assignment_is_compatible,
    history_augmented_carried_labels,
    history_augmented_product_index,
    history_augmented_terminal_system,
    minimum_history_mode_assignment,
)
from .history_witnesses import coherent_history_augmentation_witness, incoherent_history_augmentation_witness
from .macro import ConservativeMacroSchema, PortableMacroDynamics, StageMacroProjection
from .obstruction import ReplacementFiberSplitObstructionCertificate
from .path_transport import (
    PathCoherentTransportCertificate,
    ReplacementPathEdge,
    ReplacementPathStage,
    RootedReplacementGraph,
    certify_path_coherent_transport,
    compose_relations,
    derive_root_carried_labels,
    path_carried_labels,
    path_label_coherent,
)
from .path_witnesses import coherent_defect_diamond_witness, incoherent_label_diamond_witness
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
    "ReplacementPathStage",
    "ReplacementPathEdge",
    "RootedReplacementGraph",
    "PathCoherentTransportCertificate",
    "HistoryAugmentationCertificate",
    "certify_transported_target_projection",
    "certify_transport_coherent_macro_law",
    "certify_conservative_transported_schema",
    "relative_exact_refinement",
    "is_refinement",
    "certify_transport_defect",
    "compose_relations",
    "derive_root_carried_labels",
    "path_carried_labels",
    "path_label_coherent",
    "certify_path_coherent_transport",
    "history_assignment_is_compatible",
    "minimum_history_mode_assignment",
    "history_augmented_terminal_system",
    "history_augmented_product_index",
    "history_augmented_carried_labels",
    "certify_history_augmentation",
    "many_to_one_replacement_witness",
    "derived_target_projection_witness",
    "conservative_transport_witness",
    "new_action_fiber_split_witness",
    "local_fiber_split_defect_witness",
    "accumulating_transport_defect_witness",
    "coherent_defect_diamond_witness",
    "incoherent_label_diamond_witness",
    "coherent_history_augmentation_witness",
    "incoherent_history_augmentation_witness",
]