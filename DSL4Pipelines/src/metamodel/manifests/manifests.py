"""
This module defines the Manifest class,
which represents a manifest in the DSL4Pipelines metamodel.
A manifest is a collection of artefacts and their relationships,
associated with a specific pipeline.
It serves as a comprehensive representation of all the components
involved in a pipeline, including metrics, datasets, models,
and their interconnections.
"""

from dataclasses import field, dataclass
from typing import List

from DSL4Pipelines.src.metamodel.artefacts.artefacts import Artefact
from DSL4Pipelines.src.metamodel.artefacts.metrics import Metric
from DSL4Pipelines.src.metamodel.core.structure import Element
from DSL4Pipelines.src.metamodel.pipelines.workflow import Pipeline
from DSL4Pipelines.src.metamodel.relations.relations import Relationship


@dataclass
class Manifest(Element):
    """Manifest represents a collection of artefacts and their relationships,
    associated with a specific pipeline. It serves as a comprehensive representation
    of all the components involved in a pipeline, including metrics, datasets, models,
    and their interconnections."""

    pipeline: Pipeline = None
    artefacts: List[Artefact] = field(default_factory=list)
    relations: List[Relationship] = field(default_factory=list)
    type: str = "Manifest"

    def get_metrics(self) -> List[Metric]:
        """Returns a list of all metrics in the manifest."""
        return [a for a in self.artefacts if isinstance(a, Metric)]

    def find_artefacts(self, **criteria) -> List[Artefact]:
        """
        Loop through all artefacts in the manifest and
        check if they match the given criteria.
        The criteria are passed as keyword arguments,
        where the key is the name of the property to check,
        and the value is the expected value of that property.
        Exemple: manifest.find_artifacts(type="SoftwareFile", languages=["english"])
        """
        results = []
        for art in self.artefacts:
            match = True
            for key, expected_value in criteria.items():
                # we use our get_value method to get the value of the property, which will check both the actual attributes and the properties field of the artefact.
                actual_value = art.get_value(key)

                if actual_value != expected_value:
                    match = False
                    break

            if match:
                results.append(art)
        return results


# =====================================================================
# ---Test bloc and usage example---
# =====================================================================
if __name__ == "__main__":
    print("------------ 1. Testing PipelineManifest creation")
    manifest = Manifest(
        name="Example Manifest",
        uid="manifest-123",
        pipeline=Pipeline(name="Example Pipeline", uid="pipeline-123"),
        relations=[],
    )
    print(manifest)
    print("------------ 2. PipelineManifest created successfully")
    assert manifest.name == "Example Manifest"
    assert manifest.uid == "manifest-123"
    assert manifest.pipeline.name == "Example Pipeline"
    assert len(manifest.artefacts) == 1
    assert isinstance(manifest.artefacts[0], Metric)
    print("------------ 3. Testing get_metrics method")
    assert len(manifest.get_metrics()) == 1

    print("------------ 4. Testing on big manifest from notebook example")
    from examples.NotebookIRISManifest import (
        test_build_manifestFromNBonIrisClassification,
    )

    manifest = test_build_manifestFromNBonIrisClassification()
    metrics = manifest.get_metrics()
    assert len(metrics) == 2, (
        f"Expected 2 metrics, but got {len(manifest.get_metrics())}"
    )
    print(
        f"------------ 5. Metrics retrieved successfully: {[m.name for m in metrics]}"
    )
