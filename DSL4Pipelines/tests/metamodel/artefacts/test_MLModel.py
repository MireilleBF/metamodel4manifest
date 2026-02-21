from DSL4Pipelines.src.metamodel.artefacts.ml_artefacts import MLModel


def test_MLModel_validate():
    model = MLModel(name="TestModel", ml_model_type="Transformer")
    assert model.type == "MLModel"
    errors = []
    isvalid = model.validate(errors)
    print(f"Validation errors: {errors}")
    assert isvalid is True

    # assert .category == "PERFORMANCE"
    # assert m.kind == "accuracy"


def test_MLModel_validate_with_invalid_type():
    model = MLModel(name="TestModel", ml_model_type="UnknownType")
    errors = []
    isvalid = model.validate(errors)
    print(f"Validation errors: {errors}")
    assert isvalid is False
    assert "ml_modelType 'UnknownType' is not recognized." in errors[0]
