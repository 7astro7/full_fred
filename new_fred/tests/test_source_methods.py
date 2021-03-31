
import pytest
from new_fred.fred import Fred

@pytest.fixture
def fred() -> Fred:
    return Fred()

def returned_ok(
        """
        params:         arguments actually passed
                        when invoking Fred() method
                        that returned observed dict.
        observed:       FRED web service response dict.
        check_union:    iterable of keys, if none are 
                        present in observed.keys(), 
                        return False.
        """
        params: dict, 
        observed: dict,
        check_union: list = None,
        ) -> bool:
    if not isinstance(observed, dict):
        return False
    for expected_key in params.keys():
        if not expected_key in observed.keys():
            return False
        if params[expected_key] != observed[expected_key]:
            return False
    for key in check_union:
        if key in observed.keys():
            return True
    return False

@pytest.fixture
def get_all_sources_method_works(fred: Fred):
    params = {
            'limit': 2,
            'sort_order': 'desc',
            'order_by': 'name',
            }
    fred.get_all_sources(**params)
    observed = Fred().get_all_sources(**params)
    check_union = ('sources',)
    return returned_ok(params, observed, check_union)

@pytest.mark.skip("passed v2")
def test_get_all_sources(
        get_all_sources_method_works: bool,
        ):
    assert get_all_sources_method_works == True

@pytest.fixture
def get_a_source_method_works() -> bool:
    params = {
            'source_id': 1,
            }
    observed = Fred().get_a_source(**params)
    if not isinstance(observed, dict):
        return False
    if not "sources" in observed.keys():
        return False
    list_of_source_maps = observed['sources']
#    breakpoint()
    for a_source_map in list_of_source_maps:
        if not "id" in a_source_map.keys():
            return False
        if a_source_map["id"] != params["source_id"]:
            return False
    return True

@pytest.mark.skip("passed v1")
def test_get_a_source(
        get_a_source_method_works: bool,
        ):
    # fred/source
    assert get_a_source_method_works == True

@pytest.fixture
def get_releases_for_a_source_method_works() -> bool:
    # fred/source/releases
    params = {
            'source_id': 1,
            'limit': 3,
            }
    observed = Fred().get_releases_for_a_source(**params)
    if not isinstance(observed, dict):
        return False
    if not "releases" in observed.keys():
        return False
    if not "limit" in observed.keys():
        return False
    return True

@pytest.mark.skip("passed v1")
def test_get_releases_for_a_source(
        get_releases_for_a_source_method_works: bool,
        ):
    # fred/source/releases
    assert get_releases_for_a_source_method_works == True
