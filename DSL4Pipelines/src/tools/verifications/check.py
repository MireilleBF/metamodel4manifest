from typing import Callable

from DSL4Pipelines.src.metamodel.artefacts.artefacts import SoftwareFile
from DSL4Pipelines.src.metamodel.artefacts.metrics import Metric
from DSL4Pipelines.src.metamodel.catalogs.MetricCatalog import MetricCatalog
from DSL4Pipelines.src.metamodel.core.structure import Element
from DSL4Pipelines.src.metamodel.catalogs.vocabulary import RelationshipType
from DSL4Pipelines.src.tools.verifications.discover import get_all_data


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

# work on all the data but with a potential KeyError if the 'value' key is missing (we use get with a default value to avoid the error)
is_value_high_with_keyerror = lambda d : d.get("value", 0) > 0.9
