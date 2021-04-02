
import pytest
from new_fred.fred import Fred
from .fred_test_utils import returned_ok

@pytest.fixture
def fred():
    return Fred()

@pytest.fixture
def get_a_series_method_works(fred: Fred) -> bool:
    params = {
            'series_id': 'GNPCA',
            }
    fred.get_a_series(**params)
    observed = fred.series_stack['get_a_series']
    returned_ok_params = {
            'observed': observed,
            'check_union': ('series', 'seriess',),
            }
    return returned_ok(**returned_ok_params)

@pytest.mark.skip("passed v2")
def test_get_series(
        get_a_series_method_works: bool,
        ):
    assert get_a_series_method_works == True

@pytest.fixture
def get_categories_of_series_method_works(fred: Fred):
    params = {
            'series_id': 'EXJPUS',
            }
    fred.get_categories_of_series(**params)
    observed = fred.series_stack['get_categories_of_series']
    returned_ok_params = {
            'observed': observed,
            'check_union': ('categories',),
            }
    return returned_ok(**returned_ok_params)

@pytest.mark.skip("passed v2")
def test_get_categories_of_series(
        get_categories_of_series_method_works: bool,
        ):
    assert get_categories_of_series_method_works == True

@pytest.fixture
def get_series_df_method_works(fred: Fred) -> bool:
    params = {
            'series_id': 'GNPCA',
            'limit': 10,
            }
    observed = fred.get_series_df(**params)
    if not isinstance(observed, dict):
        return False
    if not 'limit' in observed.keys():
        return False
    if observed["limit"] != params["limit"]:
        return False
    if not 'observations' in observed.keys():
        return False
    return True

@pytest.mark.skip("passed v1")
def test_get_series_df(
        get_series_df_method_works: bool,
        ):
    assert get_series_df_method_works == True

@pytest.fixture
def get_release_for_a_series_method_works(fred: Fred) -> bool:
    params = {
            'series_id': 'IRA',
            }
    observed = fred.get_release_for_a_series(**params)
    if not isinstance(observed, dict):
        return False
    if not "releases" in observed.keys():
        return False
    return True

@pytest.mark.skip("passed v1")
def test_get_release_for_a_series(
        get_release_for_a_series_method_works: bool,
        ):
    assert get_release_for_a_series_method_works == True

@pytest.fixture
def search_for_a_series_method_works(fred: Fred) -> bool:
    params = {
            'search_text': ('monetary', 'service', 'index',),
            'limit': 3,
            }
    observed = fred.search_for_a_series(**params)
    if not isinstance(observed, dict):
        return False
    if not "limit" in observed.keys():
        return False
    if not "series" in observed.keys():
        if not "seriess" in observed.keys():
            return False
    # for v2 can look at each title to see if search text words are
    # present
    return True

@pytest.mark.skip("passed v1")
def test_search_for_a_series(
        search_for_a_series_method_works: bool,
        ):
    assert search_for_a_series_method_works == True

@pytest.fixture
def get_tags_for_a_series_search_method_works(fred: Fred) -> bool:
    params = {
            'series_search_text': ('monetary', 'service', 'index',),
            'limit': 3,
            }
    observed = fred.get_tags_for_a_series_search(**params)
    if not isinstance(observed, dict):
        return False
    if not "tags" in observed.keys():
        return False
    return True

@pytest.mark.skip("passed v1")
def test_get_tags_for_a_series_search(
        get_tags_for_a_series_search_method_works: bool,
        ):
    assert get_tags_for_a_series_search_method_works == True

@pytest.fixture
def get_related_tags_for_a_series_search_method_works(fred: Fred) -> bool:
    params = {
            'series_search_text': ('mortgage', 'rate', 'index',),
            'tag_names': ('30-year', 'frb',),
            'limit': 3,
            }
    observed = fred.get_related_tags_for_a_series_search(**params)
    if not isinstance(observed, dict):
        return False
    if not "limit" in observed.keys():
        return False
    if params["limit"] != observed["limit"]:
        return False
    if not "tags" in observed.keys():
        return False
    return True

@pytest.mark.skip("passed v1")
def test_get_related_tags_for_a_series_search(
        get_related_tags_for_a_series_search_method_works: bool,
        ):
    assert get_related_tags_for_a_series_search_method_works == True

@pytest.fixture
def get_tags_for_a_series_method_works(fred: Fred) -> bool:
    params = {
            'series_id': 'STLFSI',
            }
    observed = fred.get_tags_for_a_series(**params)
    if not isinstance(observed, dict):
        return False
    if not "tags" in observed.keys():
        return False
    return True

@pytest.mark.skip("passed v1")
def test_get_tags_for_a_series(
        get_tags_for_a_series_method_works: bool,
        ):
    assert get_tags_for_a_series_method_works == True

@pytest.fixture
def get_series_vintage_dates_method_works(fred: Fred) -> bool:
    params = {
            'series_id': 'GNPCA',
            'limit': 3,
            }
    observed = fred.get_series_vintage_dates(**params)
    if not isinstance(observed, dict):
        return False
    if not "limit" in observed.keys():
        return False
    if observed["limit"] != params["limit"]:
        return False
    if not "vintage_dates" in observed.keys():
        return False
    return True

@pytest.mark.skip("passed v1")
def test_get_series_vintage_dates(
        get_series_vintage_dates_method_works: bool,
        ):
    # fred/series/vintagedates
    assert get_series_vintage_dates_method_works == True

