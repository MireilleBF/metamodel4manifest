from pathlib import Path

from DSL4Pipelines.src.metamodel.manifests.manifests import Manifest
from DSL4Pipelines.src.tools.from_aibom.aibom_translator import AIBOMTranslator
from DSL4Pipelines.src.tools.queries.manifest_query import ManifestQuery
from DSL4Pipelines.src.tools.queries.rules.rules import check_dataset_and_model_presence
from tools.toFile import check_file_or_dict_exists, print_cwd, save_in_file
from tools.transformations.yamlSerializer import YAMLSerializer

import logging
logging.basicConfig(
    level=logging.INFO, # Niveau par défaut pour TOUT le monde
    format='%(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# An AIBOM Manager read a set of AIBOM files and transform them into a set of manifests
# Yhen we can apply our queries and rules on these manifests to evaluate the models described in the AIBOM files
class AIBOMManager:
    aibom_files: list[str]
    #un dictionnary that maps the name of the AIBOM file to the manifest generated from this file
    manifests : dict[str, Manifest]

    def __init__(self, path_to_aibom_files: str):
        self.aibom_files = self.get_aibom_files(path_to_aibom_files)
        self.manifests = {}
        for aibom_file in self.aibom_files:
            translator = AIBOMTranslator(aibom_file)
            manifest = translator.transform_aibom_to_manifest()
            filename = aibom_file.split('/')[-1]
            self.manifests[ filename] = manifest

    def get_aibom_files(self, path: str) -> list[str]:
        """This method takes a path to a directory and returns a list of all the AIBOM files in this directory (files with extension .json)"""
        p = Path(path)
        if check_file_or_dict_exists(p):
            aibom_files = [str(file) for file in p.glob("*.json")]
            logger.debug(f"AIBOM files found in {path} : {aibom_files}")
            return aibom_files
        return []

    #filter the manifests to keep only those that describe a model wich validates a given rule, for example a rule that says that the model must be based on a transformer architecture,
    # we will check if the manifest contains an MLModel artefact with a property "ml_model_type" with value "Transformer", and we will keep only the manifests that contain such an artefact.
    def filter_manifests_by_rule(self, rule) -> list[Manifest]:
        """This method takes a rule and returns a list of all the manifests that validate this rule"""
        valid_manifests = []
        for manifest in self.manifests.values():
            mq = ManifestQuery(manifest)
            if rule(mq):
                valid_manifests.append(manifest)
        logger.debug(f"Manifests that validate the rule {rule} : {valid_manifests}")
        return valid_manifests

    def save_manifests_in_yaml(self, output_path: str):
        """This method saves all the manifests in yaml format in the given output path"""
        for manifest_name, manifest in self.manifests.items():
            yaml_output = YAMLSerializer.to_yaml(manifest, True)
            file_name = manifest_name.replace('.json', '.yaml')
            save_in_file(output_path, file_name, yaml_output)
            logger.debug(f"Manifest {manifest_name} saved in yaml format in : {output_path + file_name}")

    def get_manifest(self, manifest_name: str) -> Manifest:
        """This method takes the name of a manifest and returns the manifest object"""
        return self.manifests.get(manifest_name)

    def get_file_name_from_manifest(self, manifest: Manifest) -> str:
        """This method takes a manifest and returns the name of the AIBOM file from which this manifest was generated"""
        for name, m in self.manifests.items():
            if m == manifest:
                return name
        return None