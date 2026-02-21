import inspect


class MetricCatalog:
    class PERFORMANCE:
        ACCURACY = "perf:accuracy"
        F1_SCORE = "perf:f1_score"
        LATENCY = "perf:latency"
        CONFUSION_MATRIX = "perf:confusion_matrix"

    class FAIRNESS:
        DEMOGRAPHIC_PARITY = "fair:demographic_parity"
        EQUALIZED_ODDS = "fair:equalized_odds"

    class SUSTAINABILITY:
        ENERGY_KWH = "env:energy_consumption"
        CARBON_GCO2 = "env:carbon_footprint"

    class ROBUSTNESS:
        ADVERSARIAL_ACCURACY = "rob:adversarial_accuracy"
        NOISE_SENSITIVITY = "rob:noise_sensitivity"

    @classmethod
    def get_all_types_map(cls) -> dict[str, str]:
        """Retourne un dictionnaire {valeur: categorie} pour un lookup rapide."""
        types_map = {}

        # On parcourt les classes internes (Performance, Fairness, etc.)
        for cat_name, inner_class in inspect.getmembers(cls):
            if inspect.isclass(inner_class) and not cat_name.startswith("__"):
                # On parcourt les attributs de ces classes
                for attr_name, technical_value in inner_class.__dict__.items():
                    if not attr_name.startswith("__"):
                        # On stocke la valeur technique comme clé pour le lookup
                        # et le nom de la catégorie (ex: Performance) comme valeur
                        types_map[technical_value] = cat_name

        return types_map

    @classmethod
    def get_all_types(cls) -> list:
        # Extract all metric types defined in the catalog and return them as a list.
        types = []
        # For each inner class (Performance, Fairness, etc.) in the MetricCatalog, we extract the class attributes that represent the metric types.
        for name, obj in inspect.getmembers(cls):
            if inspect.isclass(obj) and not name.startswith("__"):
                # Extract all class attributes that are not special methods (i.e., those that don't start with "__")
                for attr, value in obj.__dict__.items():
                    if not attr.startswith("__"):
                        types.append(value)
        return types

    @classmethod
    def get_categories(cls) -> list[str]:
        # return the list of metric categories defined in the catalog (e.g., "Performance", "Fairness", etc.)
        return [
            name
            for name, obj in inspect.getmembers(MetricCatalog)
            if inspect.isclass(obj) and not name.startswith("__")
        ]

    @classmethod
    def get_subtypes_for_category(cls, category_name: str) -> list[str]:
        # Given a category name (e.g., "Performance"), return the list of metric types that belong to that category.
        # We first check if the category exists in the catalog, and if so, we extract its class attributes that represent the metric types.
        # members = dict(inspect.getmembers(cls))
        # print(members)
        # On cherche notre "sous-type" (la classe imbriquée)
        # category_class = members.get(category_name.upper())
        category_class = getattr(cls, category_name.upper(), None)

        # category_class = getattr(cls, category_name.upper(), None)
        # print(category_class)
        if not category_class:
            return []
        # We extract all class attributes that are not special methods (i.e., those that don't start with "__") and return their values as a list.
        return [
            value
            for name, value in inspect.getmembers(category_class)
            if not name.startswith("__") and not inspect.isroutine(value)
        ]

    @classmethod
    def find_category_for_metric(cls, metric_name: str) -> str:
        """Retrouve la catégorie (ex: PERFORMANCE) pour une métrique donnée (ex: accuracy)"""
        # 1. On parcourt les membres de MetricCatalog
        for cat_name, cat_class in inspect.getmembers(cls):
            # On ne s'intéresse qu'aux classes internes (PERFORMANCE, FAIRNESS...)
            if inspect.isclass(cat_class) and not cat_name.startswith("__"):
                # 2. On récupère toutes les valeurs définies dans cette sous-classe
                # On récupère les valeurs (ex: ["perf:accuracy", ...])
                values = [
                    v for k, v in cat_class.__dict__.items() if not k.startswith("__")
                ]

                for val in values:
                    # On compare la valeur brute OU la valeur sans le préfixe (ce qui suit le ':')
                    clean_val = val.split(":")[-1] if ":" in val else val

                    if metric_name == val.lower() or metric_name == clean_val.lower():
                        return cat_name
        return "UNKNOWN"


# =====================================================================
# ---Test bloc and usage example---
# =====================================================================


if __name__ == "__main__":
    # Usage example: Get all metric types from the catalog
    print("All metric types in the catalog:\n \t")
    print(MetricCatalog.get_all_types())
    # Résultat : ['perf:accuracy', 'perf:f1_score', 'fair:demographic_parity']
    print("\nAll metric categories in the catalog:\n \t")
    print(MetricCatalog.get_categories())
    # Résultat : ['Performance', 'Fairness', 'Sustainability', 'Robustness']
    print("\nSubtypes for category 'Performance':\n \t")
    print(MetricCatalog.get_subtypes_for_category("PERFORMANCE"))
    # Résultat : ['perf:accuracy', 'perf:f1_score', 'perf:latency']
    print("\nSubtypes for category 'Fairness':\n \t")
    print(MetricCatalog.get_subtypes_for_category("Fairness"))
    # Résultat : ['fair:demographic_parity', 'fair:equalized_odds']
    print("\nSubtypes for category 'Sustainability':\n \t")
    print(MetricCatalog.get_subtypes_for_category("Sustainability"))
    # Résultat : ['env:energy_consumption', 'env:carbon_footprint
    print(MetricCatalog.find_category_for_metric("accuracy"))  # -> PERFORMANCE
    print(MetricCatalog.find_category_for_metric("perf:accuracy"))  # -> PERFORMANCE

    # Résultat : 'Performance'
