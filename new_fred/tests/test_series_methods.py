
import pytest
from new_fred.fred import Fred

# I can use the returned METAdata to test success of a method
# ensure method coverage
# test different realtime dates

@pytest.fixture
def get_a_series_method_works() -> bool:
    params = {
            'series_id': 'GNPCA',
            }
    observed = Fred().get_a_series(**params)
    if not isinstance(observed, dict):
        assert returned_correctly == True
    series_key = "seriess" if "seriess" in observed.keys() else "series"
    if not series_key in observed.keys():
        return False
    metadata_map = observed[series_key][0] # get map at index 0
    if not "id" in metadata_map.keys():
        return False
    if metadata_map["id"] != params["series_id"]:
        return False
    return True

@pytest.mark.skip("passed v1")
def test_get_series(
        get_a_series_method_works: bool,
        ):
    assert get_a_series_method_works == True

@pytest.fixture
def get_categories_of_series_method_works():
    params = {
            'series_id': 'EXJPUS',
            }
    observed = Fred().get_categories_of_series("EXJPUS")
    if not isinstance(observed, dict):
        return False
    if not "categories" in observed.keys():
        return False
    return True

@pytest.mark.skip("passed v1")
def test_get_categories_of_series(
        get_categories_of_series_method_works: bool,
        ):
    assert get_categories_of_series_method_works == True

@pytest.fixture
def get_series_df_method_works() -> bool:
    params = {
            'series_id': 'GNPCA',
            'limit': 10,
            }
    observed = Fred().get_series_df(**params)
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
def get_release_for_a_series_method_works() -> bool:
    # fred/series/release
    params = {
            'series_id': 'IRA',
            }
    observed = Fred().get_release_for_a_series(**params)
    if not isinstance(observed, dict):
        return False
    if not "releases" in observed.keys():
        return False
    return True

@pytest.mark.skip("passed v1")
def test_get_release_for_a_series(
        get_release_for_a_series_method_works: bool,
        ):
    # fred/series/release
    assert get_release_for_a_series_method_works == True

@pytest.fixture
def search_for_a_series_method_works() -> bool:
    # fred/series/search
    params = {
            'search_text': ('monetary', 'service', 'index',),
            'limit': 3,
            }
    observed = Fred().search_for_a_series(**params)
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
    # fred/series/search
    assert search_for_a_series_method_works == True





@pytest.fixture
def get_tags_for_a_series_search_method_works() -> bool:
    # fred/series/search/tags
    params = {
            'series_search_text': ('monetary', 'service', 'index',),
            'limit': 3,
            }
    observed = Fred().get_tags_for_a_series_search(**params)
    if not isinstance(observed, dict):
        return False
    if not "tags" in observed.keys():
        return False
    return True

@pytest.mark.skip("passed v1")
def test_get_tags_for_a_series_search(
        get_tags_for_a_series_search_method_works: bool,
        ):
    # fred/series/search/tags
    assert get_tags_for_a_series_search_method_works == True

@pytest.fixture
def get_related_tags_for_a_series_search_method_works() -> bool:
    # fred/series/search/related_tags
    params = {
            'series_search_text': ('mortgage', 'rate', 'index',),
            'tag_names': ('30-year', 'frb',),
            'limit': 3,
            }
    observed = Fred().get_related_tags_for_a_series_search(**params)
#    breakpoint()
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
    # fred/series/search/related_tags
    assert get_related_tags_for_a_series_search_method_works == True

@pytest.fixture
def get_tags_for_a_series_method_works() -> bool:
    # fred/series/tags
    params = {
            'series_id': 'STLFSI',
            }
    observed = Fred().get_tags_for_a_series(**params)
    if not isinstance(observed, dict):
        return False
    if not "tags" in observed.keys():
        return False
    return True

@pytest.mark.skip("passed v1")
def test_get_tags_for_a_series(
        get_tags_for_a_series_method_works: bool,
        ):
    # fred/series/tags
    assert get_tags_for_a_series_method_works == True

@pytest.fixture
def get_series_vintage_dates_method_works() -> bool:
    # fred/series/vintagedates
    params = {
            'series_id': 'GNPCA',
            'limit': 3,
            }
    observed = Fred().get_series_vintage_dates(**params)
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

