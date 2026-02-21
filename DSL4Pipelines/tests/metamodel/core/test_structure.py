from DSL4Pipelines.src.metamodel.core.structure import Element


def test_get_value():
    element = Element(
        name="TestElement",
        description="A test element for unit testing.",
        properties={"key1": "value1", "key2": "value2"},
    )
    assert element.get_value("name") == "TestElement"
    assert element.get_value("description") == "A test element for unit testing."
    assert element.get_value("properties") == {"key1": "value1", "key2": "value2"}
    assert element.get_value("nonexistent") is None
    assert (
        element.get_value("key1") == "value1"
    )  # Should return the value from properties
    assert (
        element.get_value("key2") == "value2"
    )  # Should return the value from properties
