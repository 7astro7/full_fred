
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

@pytest.mark.skip("passed v2")
def test_get_all_releases(
        get_all_releases_method_works: bool,
        ):
    assert get_all_releases_method_works == True

@pytest.fixture
def get_release_dates_all_releases_method_works(fred: Fred) -> bool:
    params = {
            'limit': 2,
            'include_empty': True,
            'offset': 1,
            'sort_order': 'asc',
            'order_by': 'release_name',
            }
    fred.get_release_dates_all_releases(**params)
    observed = fred.release_stack['get_release_dates_all_releases']
    check_union = ('release_dates',)
    params.pop('include_empty')
    returned_ok_params = {
            'observed': observed,
            'expected': params,
            'check_union': check_union,
            }
    return returned_ok(**returned_ok_params)

@pytest.mark.skip("passed v2")
def test_get_release_dates_all_releases(
        get_release_dates_all_releases_method_works: bool,
        ):
    assert get_release_dates_all_releases_method_works == True

@pytest.fixture
def get_a_release_method_works(fred: Fred) -> bool:
    params = {
            'release_id': 53,
            }
    fred.get_a_release(**params)
    observed = fred.release_stack['get_a_release']
    check_union = ('releases',)
    returned_ok_params = {
            'observed': observed,
            'check_union': check_union,
            }
    return returned_ok(**returned_ok_params)

@pytest.mark.skip("passed v2")
def test_get_a_release(
        get_a_release_method_works: bool,
        ):
    assert get_a_release_method_works == True

@pytest.fixture
def get_release_dates_method_works(fred: Fred) -> bool:
    params = {
            'release_id': 82,
            'limit': 3,
            'include_empty': True,
            'offset': 1,
            'sort_order': 'desc',
            }
    fred.get_release_dates(**params)
    observed = fred.release_stack['get_release_dates']
    check_union = ('release_dates',)
    params.pop('release_id')
    params.pop('include_empty')
    expected = params
    returned_ok_params = {
            'observed': observed,
            'expected': expected,
            'check_union': check_union,
            }
    return returned_ok(**returned_ok_params)

#@pytest.mark.skip("passed v2")
def test_get_release_dates(
        get_release_dates_method_works: bool,
        ):
    assert get_release_dates_method_works == True

@pytest.fixture
def get_release_tables_method_works(fred: Fred) -> bool:
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
def test_get_release_tables(
        get_release_tables_method_works: bool,
        ):
    assert get_release_tables_method_works == True



@pytest.fixture
def get_related_tags_for_release_method_works(fred: Fred) -> bool:
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
def get_tags_for_a_release_method_works(fred: Fred) -> bool:
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
def get_sources_for_a_release_method_works(fred: Fred) -> bool:
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
def get_series_on_a_release_method_works(fred: Fred) -> bool:
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
