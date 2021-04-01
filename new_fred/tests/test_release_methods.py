
import pytest
from new_fred.fred import Fred
from .fred_test_utils import returned_ok

@pytest.fixture
def fred():
    return Fred()

@pytest.fixture
def get_all_releases_method_works(fred: Fred) -> bool:
    params = {
            'limit': 2,
            'offset': 1,
            'sort_order': 'desc',
            'order_by': 'press_release',
            }
    fred.get_all_releases(**params)
    observed = fred.release_stack['get_all_releases']
    check_union = ('releases',)
    returned_ok_params = {
            'observed': observed,
            'expected': params,
            'check_union': check_union,
            }
    return returned_ok(**returned_ok_params)

#@pytest.mark.skip("passed v2")
def test_get_all_releases(
        get_all_releases_method_works: bool,
        ):
    assert get_all_releases_method_works == True

@pytest.fixture
def get_release_dates_all_releases_method_works() -> bool:
    # fred/releases
    params = {
            'limit': 2,
            }
    observed = fred.get_release_dates_all_releases(**params)
    if not "limit" in observed.keys():
        return False
    if observed["limit"] != params["limit"]:
        return False
    if not "release_dates" in observed.keys():
        return False
    return True

@pytest.mark.skip("passed v1")
def test_get_release_dates_all_releases(
        get_release_dates_all_releases_method_works: bool,
        ):
    # fred/releases/dates
    assert get_release_dates_all_releases_method_works == True

@pytest.fixture
def get_a_release_method_works() -> bool:
    # fred/release
    observed = fred.get_a_release(53)
    if not "releases" in observed.keys():
        return False
    releases_list = observed["releases"] # list of dicts
    if "id" in releases_list[0].keys():
        if releases_list[0]["id"] == 53:
            return True
    return False

@pytest.mark.skip("passed v1")
def test_get_a_release(get_a_release_method_works: bool):
    # fred/release
    assert get_a_release_method_works == True

@pytest.fixture
def get_release_tables_method_works() -> bool:
    # fred/release/tables
    observed = fred.get_release_tables(53)
    if not isinstance(observed, dict):
        return False
    observed_keys = tuple(observed.keys())
    for i in range(len(observed_keys)):
        if "release" in observed_keys[i]:
            key = observed_keys[i]
            break
        if i == len(observed_keys) - 1:
            return False
    if isinstance(observed[key], list):
        nested_dict = observed[key][0]
        for k in nested_dict.keys():
            if "id" in k:
                if not str(nested_dict[k]) == "53":
                    return False
    return True

@pytest.mark.skip("passed v1")
def test_get_release_tables(get_release_tables_method_works: bool):
    # fred/release/tables
    assert get_release_tables_method_works == True

@pytest.fixture
def get_release_dates_of_release_works() -> bool:
    # fred/release/dates
    params = {
            'release_id': 82,
            'limit': 3,
            }
    observed = fred.get_release_dates(**params)
#    breakpoint()
    if not isinstance(observed, dict):
        return False
    if not "limit" in observed.keys():
        return False
    if not observed['limit'] == params['limit']:
        return False
    if not "release_dates" in observed.keys():
        return False
    release_dates_map = observed["release_dates"]
    for dated_release_map in release_dates_map:
        if not isinstance(dated_release_map, dict):
            return False
        if not "release_id" in dated_release_map.keys():
            return False
        if not dated_release_map["release_id"] == params["release_id"]:
            return False
    return True

@pytest.mark.skip("passed v1")
def test_get_release_dates_of_release(
        get_release_dates_of_release_works: bool,
        ):
    # fred/release/dates
    assert get_release_dates_of_release_works == True

@pytest.fixture
def get_related_tags_for_release_method_works() -> bool:
    # fred/release/related_tags
    params = {
            'release_id': 1,
            'tag_names': ('sa', 'foreign',),
            'limit': 3,
            }
    observed = fred.get_related_tags_for_release(**params)
#    breakpoint()
    if not isinstance(observed, dict):
        return False
    if not "tags" in observed.keys():
        return False
    if not "limit" in observed.keys():
        return False
    return True

@pytest.mark.skip("passed v1")
def test_get_related_tags_for_release(
        get_related_tags_for_release_method_works: bool,
        ):
    # fred/release/related_tags
    assert get_related_tags_for_release_method_works == True

@pytest.fixture
def get_tags_for_a_release_method_works() -> bool:
    # fred/release/tags
    params = {
            'release_id': 86,
            'limit': 3,
            }
    observed = fred.get_tags_for_a_release(**params)
    if not isinstance(observed, dict):
        return False
    if not "tags" in observed.keys():
        return False
    if not "limit" in observed.keys():
        return False
    return True

@pytest.mark.skip("passed v1")
def test_get_tags_for_a_release(
        get_tags_for_a_release_method_works: bool,
        ):
    # fred/release/tags
    assert get_tags_for_a_release_method_works == True

@pytest.fixture
def get_sources_for_a_release_method_works() -> bool:
    # fred/release/source
    params = {
            'release_id': 51,
            }
    observed = fred.get_sources_for_a_release(**params)
    if not isinstance(observed, dict):
        return False
    if not "sources" in observed.keys():
        return False
    return True

@pytest.mark.skip("passed v1")
def test_get_sources_for_a_release(
        get_sources_for_a_release_method_works: bool,
        ):
    # fred/release/source
    assert get_sources_for_a_release_method_works == True

@pytest.fixture
def get_series_on_a_release_method_works() -> bool:
    # fred/release/series
    params = {
            'release_id': 51,
            'limit': 3,
            }
    observed = fred.get_series_on_a_release(**params)
    if not isinstance(observed, dict):
        return False
    if not "limit" in observed.keys():
        return False
    if observed["limit"] != params["limit"]:
        return False
    if not "series" in observed.keys():
        if not "seriess" in observed.keys():
            return False
    return True

@pytest.mark.skip("passed v1")
def test_get_series_on_a_release(
        get_series_on_a_release_method_works: bool,
        ):
    # fred/release/series
    assert get_series_on_a_release_method_works == True
