from DSL4Pipelines.src.metamodel.artefacts.ml_artefacts import Data
from DSL4Pipelines.src.metamodel.catalogs.artefact_catalog import ArtefactCatalog
from DSL4Pipelines.src.metamodel.catalogs.DatasetCatalog import DatasetCatalog


def test_DataSet_validation():
    # Test with valid data artifact
    data = Data(
        name="TestDataset",
        data_types=["images"],
        dataset_kinds=["dataset"],
        data_formats=[".jpg"],
        dataset_size=1000000,
        dataset_availability="public",
        dataset_has_sensitive_personal_information="no",
        dataset_intended_use="For training image classification models.",
        dataset_known_bias=["may contain more images of certain categories"],
    )
    errors = []
    isValid = data.validate(errors)
    assert isValid is True, f"Validation failed with errors: {errors}"
    assert data.type == "Data"

    # Test with invalid data artifact (invalid availability)
    invalid_data = Data(name="InvalidDataset", dataset_availability="unknown_status")
    errors = []
    isvalid = invalid_data.validate(errors)
    assert isvalid is False, (
        f"Validation should have failed but passed. Errors: {errors}"
    )
    print(f"Validation correctly failed with errors: {errors}")
    assert "datasetAvailability 'unknown_status' is not recognized." in errors[0]


def test_Corpus_validation():
    openWebText = Data(
        name="openWebText",
        description="a reconstructed 'open' version of the GPT2 training corpus \n based on the data published in the GPT2 technical report, \n This corpus was constructed from the code located on code_ref",
        data_types=["text"],
        dataset_kinds=["corpus"],
        data_formats=[".txt"],
        software_download_location="https://huggingface.co/datasets/Skylion007/openwebtext",
        access=ArtefactCatalog.ACCESS.PRIVATE,
        license="none",
        properties=[{"code_ref": "https://github.com/jcpeterson/openwebtext"}],
    )
    assert openWebText.validate() is True


def test_Vocabulary_validation():
    vocabulary = Data(
        name="vocabulary",
        type="Vocabulary",
        description="The generated ...",
        dataset_kinds=[DatasetCatalog.DATASET_KINDS.DATASET],
        data_formats=["text"],
        software_file_kind="bpe",
        content_type="?",
        software_download_location="https://openaipublic.blob.core.windows.net/gpt-2/encodings/main/vocab.bpe",
        access=ArtefactCatalog.ACCESS.PRIVATE,
        license="none",
        properties=[
            {"code_ref": "https://github.com/jcpeterson/openwebtext"},
            {"n_vocab": 50257},
        ],
    )
    assert vocabulary.validate() is False
    vocabulary.content_type = "text/plain"
    assert vocabulary.validate() is True
