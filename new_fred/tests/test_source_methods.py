
import pytest
from new_fred.fred import Fred

# I can use the returned METAdata to test success of a method
# ensure method coverage
# test different realtime dates

@pytest.fixture
def get_all_sources_method_works():
    # fred/sources
    params = {
            'limit': 2,
            }
    observed = Fred().get_all_sources(**params)
    if not isinstance(observed, dict):
        return False
    if not "limit" in observed.keys():
        return False
    if observed["limit"] != params["limit"]:
        return False
    if not "sources" in observed.keys():
        return False
    return True

#@pytest.mark.skip("passed v1")
def test_get_all_sources(
        get_all_sources_method_works: bool,
        ):
    assert get_all_sources_method_works == True

@pytest.fixture
def get_a_source_method_works() -> bool:
    # fred/source
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
