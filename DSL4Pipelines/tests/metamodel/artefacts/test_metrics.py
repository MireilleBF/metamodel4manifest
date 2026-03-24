from DSL4Pipelines.src.metamodel.artefacts.metrics import Metric
from DSL4Pipelines.src.metamodel.catalogs.MetricCatalog import MetricCatalog

PERFORMANCE = MetricCatalog.PREDICT_PERFORMANCE.NAME

def test_metric_validation_fills_category():
    m = Metric(kind="accuracy", value="0.95")
    m.validate_with_catalog()

    assert m.category == PERFORMANCE
    assert m.kind == "accuracy"
    assert m.type == "Metric"


def test_unknown_metric_returns_false():
    m = Metric(kind="unknown_thing")
    result = m.validate_with_catalog()
    assert result is False
