from enum import Enum
# https://github.com/spdx/tools-python/blob/main/src/spdx_tools/spdx/model/relationship.py
# 1. On définit les types autorisés par le standard

""""
Type de Relation,Usage dans votre SBOM
contains,Un package contient un fichier ou un répertoire.
generates,Un script (ex: train.py) génère un artefact (ex: model.bin).
trainedOn,Un modèle a été entraîné en utilisant un dataset spécifique.
testedOn,Un modèle a été évalué sur un dataset de test.
hasDocumentation,Lie un package à son fichier README.md ou ses techdocs.
dependsOn,Un script a besoin d'une bibliothèque ou d'un autre fichier.
hasDataFile,"Un script de prédiction utilise un fichier de poids (.bin, .pt)."
"""


# Some relationship types are not included in the SPDX standard but can be useful for our use case, so we can add them as needed.
class RelationshipType(str, Enum):
    CONTAINS = "contains"
    TRAINED_ON = "trainedOn"
    TESTED_ON = "testedOn"
    HAS_DECLARED_LICENSE = "hasDeclaredLicense"
    HAS_DATA_FILE = "hasDataFile"
    HAS_DOCUMENTATION = "hasDocumentation"
    DEPENDS_ON = "dependsOn"
    EVALUATES = "evaluates"
    EVALUATED_BY = "evaluated_by"
    GENERATED_FROM = "generatedFrom"
    GENERATED_BY = "generatedBy"
    GENERATES = "generates"
    USED_BY = "usedBy"
    # Mi
    SOURCE = "fromSource"
    NEXT = "next"  # MI added for pipeline steps
    #    HAS_PREREQUISITE = auto()
    #    METAFILE_OF = auto()
    #    OPTIONAL_COMPONENT_OF = auto()
    #    OPTIONAL_DEPENDENCY_OF = auto()
    OTHER = "other"


#    PACKAGE_OF = auto()
#    PATCH_APPLIED = auto()
#    PATCH_FOR = auto()
#   PREREQUISITE_FOR = auto()
#    PROVIDED_DEPENDENCY_OF = auto()
#    REQUIREMENT_DESCRIPTION_FOR = auto()
#    RUNTIME_DEPENDENCY_OF = auto()
#    SPECIFICATION_FOR = auto()
#    STATIC_LINK = auto()
#    TEST_CASE_OF = auto()
#   TEST_DEPENDENCY_OF = auto()
#   TEST_OF = auto()
#   TEST_TOOL_OF = auto()
#   VARIANT_OF = auto()


class FileKind(str, Enum):
    FILE = "file"
    DIRECTORY = "directory"
