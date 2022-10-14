import pytest

from hw_1_5.service.search import get_response, search


def test_search():
    program = search("Family Guy")
    assert program.name == "Family Guy"
    assert program.network.name == "FOX"
    assert program.network.country.name == "United States"
    assert program.summary != ""


def test_get_response():
    response = get_response("Family Guy")
    assert response["name"] == "Family Guy"
    assert response["network"]["name"] == "FOX"
    assert response["network"]["country"]["name"] == "United States"
    assert response["summary"] != ""


@pytest.mark.parametrize("query", ["Family Guy", "The Simpsons", "South Park"])
def test_search_with_different_queries(query):
    program = search(query)
    assert program.name == query


def test_search_with_incorrect_query():
    with pytest.raises(AttributeError):
        search("a")
