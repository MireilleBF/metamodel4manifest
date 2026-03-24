from DSL4Pipelines.src.metamodel.artefacts.metrics import Metric
from DSL4Pipelines.src.metamodel.core.structure import Element


#TODO make it reflexive and not specific to a given element type (e.g. Pipeline, Task, etc.)

def get_all_data(element : Element) -> dict:
    # On commence par les attributs de base
    #data = {
    #    "name": element.name,
    #    "type": element.type,
    #    "uid": element.uid
    #}
    data = element.__dict__.copy() # .copy() est plus sûr pour ne pas modifier l'objet original

    if hasattr(element, "properties"):
        if element.properties is not None:
            if isinstance(element.properties, dict):
                # Si properties est déjà un dict, on peut l'ajouter directement
                data.update(element.properties)
            elif isinstance(element.properties, list):
                # Si properties est une liste de dicts, on peut les fusionner en un seul dict
                for prop in element.properties:
                    if isinstance(prop, dict):
                        data.update(prop)
                    else:
                        print(f"Warning: Ignoring non-dict property {prop} in element {element.name}")

    return data



def discover_keys(elements_list):
    keys = set()
    for el in elements_list:
        # On récupère les clés du dictionnaire plat
        full_data = get_all_data(el)
        keys.update(full_data.keys())
    return sorted(list(keys))






#=====================================================================
# ---Test bloc and usage example---
#=====================================================================
if __name__ == "__main__":
    metric_accuracy = Metric(
        name="Model Accuracy",
        description="Accuracy du modèle de classification sur le dataset IRIS.",
        #value=0.95,
        #unit="%",
        properties=[{"calculation_method": "accuracy_score from scikit-learn"}]
    )

    dictionary = get_all_data(metric_accuracy)
    print(f"Here is the flattened dictionary for the metric_accuracy object:\n \t {dictionary}")

    # Test de la fonction discover_keys
    keys = discover_keys([metric_accuracy])
    print(f"Here are the discovered keys from the metric_accuracy object:\n \t {keys}")

