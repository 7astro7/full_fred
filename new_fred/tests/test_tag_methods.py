
import pytest
from new_fred.fred import Fred

# I can use the returned METAdata to test success of a method
# ensure method coverage
# test different realtime dates

# v2: 
# don't assign returned data but rather assign 
# the value from tag_stack
# limit, sort_order, tag_names

@pytest.fixture
def fred() -> Fred:
    return Fred()

@pytest.fixture
def get_tags_method_works(fred: Fred) -> bool:
    params = {
            'limit': 2,
            'sort_order' : 'desc',
            'tag_names': ('gdp', 'oecd',),
            }
    fred.get_tags(**params)
    if not "get_tags" in fred.tag_stack.keys():
        return False
    observed = fred.tag_stack["get_tags"]
    if not isinstance(observed, dict):
        return False
    if not "limit" in observed.keys():
        return False
    if not observed["limit"] == params["limit"]:
        return False
    if not "tags" in observed.keys():
        return False
    if not "sort_order" in observed.keys():
        return False
    if observed["sort_order"] != params["sort_order"]:
        return False
    return True

@pytest.mark.skip("passed v2")
def test_get_tags(
        get_tags_method_works: bool,
        ):
    assert get_tags_method_works == True

@pytest.fixture
def get_related_tags_for_a_tag_method_works(fred: Fred) -> bool:
    params = {
            'tag_names': ('monetary aggregates', 'weekly'),
            'limit': 2,
            'sort_order': 'desc',
            }
    fred.get_related_tags_for_a_tag(**params)
    if not "get_related_tags_for_a_tag" in fred.tag_stack.keys():
        return False
    observed = fred.tag_stack["get_related_tags_for_a_tag"]
    if not isinstance(observed, dict):
        return False
    if not "limit" in observed.keys():
        return False
    if not observed["limit"] == params["limit"]:
        return False
    if not "tags" in observed.keys():
        return False
    if not "sort_order" in observed.keys():
        return False
    if observed["sort_order"] != params["sort_order"]:
        return False
    return True

@pytest.mark.skip("passed v2")
def test_get_related_tags_for_a_tag(
        get_related_tags_for_a_tag_method_works: bool,
        ):
    assert get_related_tags_for_a_tag_method_works == True


@pytest.fixture
def get_series_matching_tags_method_works(fred: Fred) -> bool:
    params = {
            'tag_names': ('slovenia', 'food', 'oecd',),
            'limit': 2,
            'sort_order': 'desc',
            }
    fred.get_series_matching_tags(**params)
    if not "get_series_matching_tags" in fred.tag_stack.keys():
        return False
    observed = fred.tag_stack["get_series_matching_tags"]
    if not isinstance(observed, dict):
        return False
    if not "limit" in observed.keys():
        return False
    if not observed["limit"] == params["limit"]:
        return False
    if not "seriess" in observed.keys():
        if not "series" in observed.keys():
            return False
    if not "sort_order" in observed.keys():
        return False
    if observed["sort_order"] != params["sort_order"]:
        return False
    return True

@pytest.mark.skip("passed v2")
def test_get_series_matching_tags(
        get_series_matching_tags_method_works: bool,
        ):
    assert get_series_matching_tags_method_works == True


