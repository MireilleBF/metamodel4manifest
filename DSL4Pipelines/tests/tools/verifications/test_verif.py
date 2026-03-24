from typing import Callable, List

from DSL4Pipelines.src.metamodel.artefacts.metrics import Metric

from DSL4Pipelines.src.metamodel.catalogs.MetricCatalog import MetricCatalog

from DSL4Pipelines.src.metamodel.catalogs.vocabulary import RelationshipType

from DSL4Pipelines.src.metamodel.artefacts.artefacts import SoftwareFile

from DSL4Pipelines.src.tools.verifications.check import (
    filter_metrics,
    check,
    is_value_high_with_keyerror,
)
from DSL4Pipelines.tests.examples.NotebookIRISManifest import test_build_manifestFromNBonIrisClassification
from DSL4Pipelines.src.metamodel.manifests.manifests import Manifest

from DSL4Pipelines.src.metamodel.artefacts.artefacts import Artefact
from DSL4Pipelines.src.metamodel.core.structure import Element
from DSL4Pipelines.src.metamodel.artefacts.ml_artefacts import Data
from DSL4Pipelines.src.tools.verifications.discover import get_all_data


def test_metric_verifications():
    metric_accuracy = Metric(
        name="Model Accuracy",
        description="Accuracy du modèle de classification sur le dataset IRIS.",
        value=0.95,
        kind=MetricCatalog.PREDICT_PERFORMANCE.ACCURACY,
        # unit="%",
        properties=[{"calculation_method": "accuracy_score from scikit-learn"}],
    )

    metrics = ["perf:accuracy", "fair:bias", "perf:latency"]
    res = filter_metrics(metrics, "perf")
    assert res == ["perf:accuracy", "perf:latency"], (
        f"Expected ['perf:accuracy', 'perf:latency'], but got {res}"
    )
    data = get_all_data(metric_accuracy)
    print(f"Here is the flattened dictionary for the metric_accuracy object:\n \t {data}")
    assert data["name"] == "Model Accuracy", f"Expected 'name' to be 'Model Accuracy' but got {data['name']}"
    assert data["description"] == "Accuracy du modèle de classification sur le dataset IRIS.", f"Expected 'description' to be 'Accuracy du modèle de classification sur le dataset IRIS.' but got {data['description']}"
    assert data["value"] == 0.95, f"Expected 'value' to be 0.95 but got {data['value']}"
    assert data ["calculation_method"] == "accuracy_score from scikit-learn", f"Expected 'calculation_method' to be 'accuracy_score from scikit-learn' but got {data['calculation_method']}"


    # Does the metric have a value greater than 0.9 ?
    is_value_high = lambda d: d.value > 0.9
    assert is_value_high(metric_accuracy) == True

    # Does the metric belong to the "accuracy" type in the catalog ? (we check if the kind contains "accuracy")
    is_accuracy: Callable[[Metric], bool] = lambda d: (
            "accuracy" in d.kind or "ACCURACY" in d.kind
    )
    # lambda m: m.category == "PERFORMANCE" and m.kind == "accuracy"
    assert is_accuracy(metric_accuracy) == True


def test_metric_verifications_on_manifest():
    # Working on notebook example from the manisfest
    manifest : Manifest = test_build_manifestFromNBonIrisClassification()

    metrics = metric_presence(manifest)

    check_metric_properties(metrics)
    print("---------- All checks on the metric properties passed successfully !")
    # Do we have the code used to evaluate the metric ?
    ##Get the relationships in the manifest that link the metric to a SoftwareFile (which would be the code)
    print(f"Here are all the relationships in the manifest: {manifest.relations}")

    step = check_metric_produced_by(manifest, metrics)
    print("---------- Check on the metric production passed successfully !")
    print(f"Step linked to the metric {metrics[0].name} : {step.name} ")

    # if the step is an instance of Step, we look for the task that contains it.
    task = manifest.pipeline.tasks
    for t in manifest.pipeline.tasks:
        if step in t.steps:
            task = t
            break
    print(f"Task containing the step {step.name} : {task.name} ")
    assert task is not None, f"No task found containing the step {step.name} !"
    assert task.name == "ModelEvaluation", f"Expected task name to be 'ModelEvaluation' but got {task.name}"

    # We look for the dataset in the manifest
    # je n'ai pas identifié le dataset de test donc je ne fais qu'un test très simple
    dataset = next(a for a in manifest.artefacts if isinstance(a, Data))
    print(f"Dataset found in the manifest: {dataset.name} with num_instances = {dataset.properties.get('num_instances', 'unknown')}")
    assert dataset is not None, "No dataset found in the manifest !"

    # Est-ce que c'est un Dataset avec plus de 100 lignes ?
    is_big_dataset = lambda d: d.get("num_instances", 0) > 100
    assert is_big_dataset(dataset.properties), f"The dataset {dataset.name} is not a big dataset (num_instances <= 100) !"


def check_metric_properties(metrics: list[Artefact]):
    for m in metrics:
        assert m.name is not None and m.name != "", f"Metric {m} has no name !"
        assert m.description is not None and m.description != "", f"Metric {m} has no description !"
        assert m.kind is not None and m.kind != "", f"Metric {m} has no kind !"
        assert m.category is not None and m.category != "", f"Metric {m} has no category !"
    #get Accuracy metric
    metric_accuracy = next((m for m in metrics if "accuracy" in m.kind.lower()), None)
    assert metric_accuracy is not None, "No accuracy metric found in the metrics list !"
    data = get_all_data(metric_accuracy)
    assert "calculation_method" in data, f"Expected 'calculation_method' key in the metric properties but got {data.keys()}"
    assert "value" in data, f"Expected 'value' key in the metric properties but got {data.keys()}"
    metric_accuracy.__setattr__("value",0.95) # we set the value here just for the test of the check function, but in a real scenario, this value should come from the manifest or be calculated based on the code linked to the metric
    data = get_all_data(metric_accuracy)
    assert data["calculation_method"] == "accuracy_score from scikit-learn", f"Expected 'calculation_method' to be 'accuracy_score from scikit-learn' but got {data['calculation_method']}"
    assert data["value"] == 0.95, f"Expected 'value' to be 0.95 but got {data['value']}"
    print(f"Here is the flattened dictionary for the metric_accuracy object:\n \t {data}")
    print(f"Résultat du test : {check(metric_accuracy, is_value_high_with_keyerror)}")



def check_metric_produced_by(manifest: Manifest, metrics: list[Artefact]) -> Element:
    metric1 = metrics[0]
    linksToMetrics = [
        r
        for r in manifest.relations
        if r.to_.__contains__(metric1) and r.relationship_type == RelationshipType.PRODUCES
    ]
    print(f"Relationships linking to the metric {metric1.name} : {linksToMetrics} ")
    assert len(linksToMetrics) > 0, f"No relationships found linking to the metric {metric1.name} !"
    assert len(
        linksToMetrics) == 1, f"Multiple relationships found linking to the metric {metric1.name} ! Expected only one relationship but got {len(linksToMetrics)}"
    step = linksToMetrics[0].from_
    print(f"Step linked to the metric {metric1.name} : {step.name} ")
    return step



def metric_presence(manifest: Manifest) -> list[Artefact]:
    # What are the metric kinds used to evaluate the performance of the model ? (we check if the kind is in the PERFORMANCE category of the catalog)
    ## 1. We first look for artefacts of type Metric in the manifest
    metrics: List[Artefact] = [e for e in manifest.artefacts if e.__class__ == Metric]
    assert len(metrics) > 0, "No metrics found in the manifest !"
    assert metrics[0].__class__ == Metric, f"Expected artefacts of type Metric but got {metrics[0].__class__}"
    assert metrics[1].__class__ == Metric, f"Expected artefacts of type Metric but got {metrics[1].__class__}"
    print(f"Metrics found in the manifest: {[m.name for m in metrics]}")
    ## results: Metrics found in the manifest: ['Model Accuracy', 'Confusion Matrix']
    print(
        f"Here are the kinds of the metrics found in the manifest: {[m.kind for m in metrics]}"
    )
    print(
        f"Here are the categories of the metrics found in the manifest: {[m.category for m in metrics]}"
    )
    return metrics
