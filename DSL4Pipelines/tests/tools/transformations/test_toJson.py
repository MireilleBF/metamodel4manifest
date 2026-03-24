from DSL4Pipelines.src.metamodel.manifests.manifests import Manifest
from DSL4Pipelines.src.tools.transformations.toJson import yaml_to_json

def test_to_json():
    #read yaml file and transform it to json
    file = "/Users/mireillefornarino/GIT/RECHERCHES/metamodele4manifest/DSL4Pipelines/tests/examples/sources/nanoGPT_manifest3.yaml"
    output_dir = "/Users/mireillefornarino/GIT/RECHERCHES/metamodele4manifest/DSL4Pipelines/tests/examples/outputs/"
    outputPath = yaml_to_json(file,output_dir)
    print(f"Json file generated in : {outputPath}")

