from typing import Callable

from DSL4Pipelines.src.metamodel.artefacts.artefacts import SoftwareFile
from DSL4Pipelines.src.metamodel.artefacts.metrics import Metric
from DSL4Pipelines.src.metamodel.catalogs.MetricCatalog import MetricCatalog
from DSL4Pipelines.src.metamodel.core.structure import Element
from DSL4Pipelines.src.metamodel.catalogs.vocabulary import RelationshipType
from DSL4Pipelines.src.tools.verifications.discover import get_all_data
from DSL4Pipelines.src.tests.pipelines.NotebookIRISManifest import (
    get_manifestFromNBonIrisClassification,
)


# metrics = ["perf:accuracy", "fair:bias", "perf:latency"]
def filter_metrics(metrics: list[str], keyword: str) -> list[str]:
    # Garder seulement celles qui contiennent "perf"
    # Note : 'm' est typé comme str ici
    keyword_only = list(filter(lambda m: keyword in m, metrics))
    return keyword_only


def check(element: Element, condition_func: Callable[[dict], bool]) -> bool:
    # 1. On prépare les données
    data = get_all_data(element)
    try:
        # 2. On teste la condition
        return condition_func(data)
    except KeyError:
        # Si on demande une clé qui n'existe pas pour cet objet
        return False


# --- EXEMPLES D'UTILISATION ---
# =====================================================================
# ---Test bloc and usage example---
# =====================================================================
if __name__ == "__main__":
    metric_accuracy = Metric(
        name="Model Accuracy",
        description="Accuracy du modèle de classification sur le dataset IRIS.",
        value=0.95,
        kind=MetricCatalog.PERFORMANCE.ACCURACY,
        # unit="%",
        properties=[{"calculation_method": "accuracy_score from scikit-learn"}],
    )
    metrics = ["perf:accuracy", "fair:bias", "perf:latency"]
    res = filter_metrics(metrics, "perf")
    assert res == ["perf:accuracy", "perf:latency"], (
        f"Expected ['perf:accuracy', 'perf:latency'], but got {res}"
    )
    # print(get_all_data(metric_accuracy))

    # Does the metric have a value greater than 0.9 ?
    is_value_high = lambda d: d.value > 0.9
    assert is_value_high(metric_accuracy) == True

    # work on all the data but with a potential KeyError if the 'value' key is missing (we use get with a default value to avoid the error)
    is_value_high_with_keyerror = lambda d: d.get("value", 0) > 0.9

    # Does the metric belong to the "accuracy" type in the catalog ? (we check if the kind contains "accuracy")
    is_accuracy: Callable[[Metric], bool] = lambda d: (
        "accuracy" in d.kind or "ACCURACY" in d.kind
    )
    # lambda m: m.category == "PERFORMANCE" and m.kind == "accuracy"
    assert is_accuracy(metric_accuracy) == True

    # Working on notebook example from the manisfest
    manifest = get_manifestFromNBonIrisClassification()

    # What are the metric kinds used to evaluate the performance of the model ? (we check if the kind is in the PERFORMANCE category of the catalog)
    ## 1. We first look for artefacts of type Metric in the manifest
    metrics = [e for e in manifest.artefacts if e.__class__ == Metric]
    print(f"Metrics found in the manifest: {[m.name for m in metrics]}")
    ## results: Metrics found in the manifest: ['Model Accuracy', 'Confusion Matrix']
    print(
        f"Here are the kinds of the metrics found in the manifest: {[m.kind for m in metrics]}"
    )
    print(
        f"Here are the categories of the metrics found in the manifest: {[m.category for m in metrics]}"
    )

    # Do we have the code used to evaluate the metric ?
    ##Get the relationships in the manifest that link the metric to a SoftwareFile (which would be the code)
    metric1 = metrics[0]
    linksToMetrics = [
        r
        for r in manifest.relations
        if r.to_ == metric1 and r.relationship_type == RelationshipType.EVALUATES
    ]
    print(f"Relationships linking to the metric {metric1.name} : {linksToMetrics} ")
    step = linksToMetrics[0].from_
    print(f"Step linked to the metric {metric1.name} : {step.name} ")
    linksToFiles = [
        r
        for r in manifest.relations
        if r.from_ == step and any(isinstance(r.to_, SoftwareFile))
    ]
    print(f"Relationships linking to the step {step.name} to {linksToFiles}")
    print(
        f"Relationships linking to the metric {metric1.name} : from {
            [(r.from_.__class__, r.relationship_type) for r in linksToMetrics]
        }"
    )

    code_links = [
        r
        for r in linksToMetrics
        if r.relationship_type == "DEPENDS_ON"
        and r.from_ in metrics
        and any(isinstance(t, SoftwareFile) for t in r.to_)
    ]

    # Do we have information about the dataset used for the evaluation ?

    # Est-ce qu'il y a du français dans les classes ?
    has_french = lambda d: "fr" in d.get("class_names", [])

    # Est-ce que c'est un Dataset avec plus de 100 lignes ?
    is_big_dataset = lambda d: d["type"] == "Data" and d.get("num_instances", 0) > 100

    # On lance le test sur un objet 'iris'
    print(f"Résultat du test : {check(metric_accuracy, is_value_high_with_keyerror)}")
