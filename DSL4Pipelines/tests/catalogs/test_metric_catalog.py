from typing import List

from DSL4Pipelines.src.metamodel.catalogs.MetricCatalog import MetricCatalog
from DSL4Pipelines.src.metamodel.artefacts.metrics import Metric


def test_metric_catalog_get_all_types_():
    # Usage example: Get all metric types from the catalog
    print("\n--------------- All metric types in the catalog:\n \t")
    res = MetricCatalog.get_all_types()
    print(res)

    metric = Metric(kind="perf:accuracy", value="0.95")
    # With the list, on peut vérifier que c'est dans la liste mais on ne sait pas à quelle catégorie ça appartient
    assert metric.kind in MetricCatalog.get_all_types()

    # with (Dictionnaire)
    catalog: dict[str, str] = MetricCatalog.get_all_types_map()
    category = catalog.get(metric.kind)
    assert category is not None, (
        f"Métrique {metric.kind} non trouvée dans le catalogue !"
    )
    assert category == "PERFORMANCE", (
        f"Métrique {metric.kind} trouvée dans le catalogue mais avec une catégorie incorrecte : {category}"
    )


def test_metric_catalog_get_categories_and_subtypes():
    print("\n--------------- All metric categories in the catalog:\n \t")
    categories: List[str] = MetricCatalog.get_categories()
    print(categories)
    assert "PERFORMANCE" in categories
    assert "FAIRNESS" in categories
    assert "SUSTAINABILITY" in categories
    # Résultat : ['Performance', 'Fairness', 'Sustainability', 'Robustness']

    print("\n--------------- Subtypes for category 'Performance':\n \t")
    res: List[str] = MetricCatalog.get_subtypes_for_category("PERFORMANCE")
    print(res)
    assert "perf:accuracy" in res
    assert "perf:f1_score" in res
    assert "perf:latency" in res
    # Résultat : ['perf:accuracy', 'perf:f1_score', 'perf:latency']
    print("\n--------------- Subtypes for category 'Fairness':\n \t")
    res = MetricCatalog.get_subtypes_for_category("Fairness")
    print(res)
    assert "fair:demographic_parity" in res
    assert "fair:equalized_odds" in res
    # Résultat : ['fair:demographic_parity', 'fair:equalized_odds']
    print("\n--------------- Subtypes for category 'Sustainability':\n \t")
    res = MetricCatalog.get_subtypes_for_category("Sustainability")
    print(res)
    assert "env:energy_consumption" in res
    # Résultat : ['env:energy_consumption', 'env:carbon_footprint


def test_find_category_for_metric():
    print("\n--------------- categories for accuracy :\n \t")
    res = MetricCatalog.find_category_for_metric("accuracy")
    # print(res)
    assert res == "PERFORMANCE", f"Expected 'PERFORMANCE' but got '{res}'"

    res = MetricCatalog.find_category_for_metric("perf:accuracy")
    # print(res)
    assert res == "PERFORMANCE", f"Expected 'PERFORMANCE' but got '{res}'"

    res = MetricCatalog.find_category_for_metric("unknown_metric")
    # print(res)
    assert res == "UNKNOWN", f"Expected 'UNKNOWN' but got '{res}'"
