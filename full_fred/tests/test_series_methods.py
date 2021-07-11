import pytest
from full_fred.fred import Fred
from pandas import DataFrame
from .fred_test_utils import (
    returned_ok,
    make_time_string,
    api_key_found_in_env,
)

ENV_API_KEY = api_key_found_in_env()


@pytest.fixture
def fred():
    return Fred()


@pytest.fixture
def returned_ok_params():
    return dict()


@pytest.fixture
def get_a_series_method_works(
    fred: Fred,
    returned_ok_params: dict,
) -> bool:
    params = {
        "series_id": "GNPCA",
        "realtime_start": "2007-11-01",
    }
    fred.get_a_series(**params)
    returned_ok_params["observed"] = fred.series_stack["get_a_series"]
    params.pop("series_id")
    returned_ok_params["expected"] = params
    returned_ok_params["check_union"] = (
        "series",
        "seriess",
    )
    return returned_ok(**returned_ok_params)


@pytest.mark.skipif(not ENV_API_KEY, reason="Tests need api key")
def test_get_series(
    get_a_series_method_works: bool,
):
    assert get_a_series_method_works == True


@pytest.fixture
def get_categories_of_series_method_works(
    fred: Fred,
    returned_ok_params: dict,
):
    params = {
        "series_id": "EXJPUS",
        # EXJPUS doesn't exist in ALFRED, forego realtime param
        #            'realtime_end': '1995-12-01',
    }
    fred.get_categories_of_series(**params)
    returned_ok_params["observed"] = fred.series_stack["get_categories_of_series"]
    params.pop("series_id")
    returned_ok_params["expected"] = params
    returned_ok_params["check_union"] = ("categories",)
    return returned_ok(**returned_ok_params)


@pytest.mark.skipif(not ENV_API_KEY, reason="Tests need api key")
def test_get_categories_of_series(
    get_categories_of_series_method_works: bool,
):
    assert get_categories_of_series_method_works == True


@pytest.fixture
def get_series_df_method_works(
    fred: Fred,
    returned_ok_params: dict,
) -> bool:
    params = {
        "series_id": "GNPCA",
        "limit": 10,
        "realtime_start": "2003-01-01",
        #            'units': 'log',
        "sort_order": "desc",
        "offset": 1,
        "observation_start": "1776-07-04",
        "observation_end": "9999-12-31",
    }
    fred.get_series_df(**params)
    returned_ok_params["observed"] = fred.series_stack["get_series_df"]
    if not "observation_start" in returned_ok_params["observed"].keys():
        return False

    # 1600-01-01 was returned for 1776-07-04
    expected_obs_start = (
        "1776-07-04",
        "1600-01-01",
    )
    if returned_ok_params["observed"]["observation_start"] not in expected_obs_start:
        return False
    params.pop("observation_start")

    # series_id is manually added to metadata of DataFrame,
    # so series_id in params is retained as an expected key
    returned_ok_params["expected"] = params
    returned_ok_params["check_union"] = (
        "df",
        "observations",
    )
    if not returned_ok(**returned_ok_params):
        return False
    if isinstance(returned_ok_params["observed"]["df"], DataFrame):
        return True
    return False


@pytest.mark.skipif(not ENV_API_KEY, reason="Tests need api key")
def test_get_series_df(
    get_series_df_method_works: bool,
):
    assert get_series_df_method_works == True

@pytest.mark.skipif(not ENV_API_KEY, reason="Tests need api key")
def test_get_series_df_raises(fred: Fred):
    with pytest.raises(KeyError):
        fred.get_series_df('GOLDPMGBD229NLBM')

@pytest.fixture
def get_release_for_a_series_method_works(
    fred: Fred,
    returned_ok_params: dict,
) -> bool:
    params = {
        "series_id": "IRA",
        "realtime_end": "2014-07-04",
    }
    fred.get_release_for_a_series(**params)
    returned_ok_params["observed"] = fred.series_stack["get_release_for_a_series"]
    params.pop("series_id")
    returned_ok_params["expected"] = params
    returned_ok_params["check_union"] = ("releases",)
    return returned_ok(**returned_ok_params)


@pytest.mark.skipif(not ENV_API_KEY, reason="Tests need api key")
def test_get_release_for_a_series(
    get_release_for_a_series_method_works: bool,
):
    assert get_release_for_a_series_method_works == True


@pytest.fixture
def search_for_series_method_works(
    fred: Fred,
    returned_ok_params: dict,
) -> bool:
    params = {
        "search_words": (
            "monetary",
            "service",
            "index",
        ),
        "limit": 3,
        "realtime_end": "2019-06-03",
        #            'search_type': 'series_id',
        "order_by": "title",
        "sort_order": "desc",
        "offset": 2,
    }
    fred.search_for_series(**params)
    returned_ok_params["observed"] = fred.series_stack["search_for_series"]
    params.pop("search_words")
    returned_ok_params["expected"] = params
    returned_ok_params["check_union"] = (
        "seriess",
        "series",
    )
    return returned_ok(**returned_ok_params)


@pytest.mark.skipif(not ENV_API_KEY, reason="Tests need api key")
def test_search_for_series(
    search_for_series_method_works: bool,
):
    assert search_for_series_method_works == True


@pytest.fixture
def get_tags_for_series_search_method_works(
    fred: Fred,
    returned_ok_params: dict,
) -> bool:
    params = {
        "search_words": (
            "monetary",
            "service",
            "index",
        ),
        "limit": 3,
        "realtime_end": "2019-06-03",
        #            'tag_search_words': ('', '',),
        "order_by": "created",
        "sort_order": "desc",
        "offset": 2,
    }
    fred.get_tags_for_series_search(**params)
    returned_ok_params["observed"] = fred.series_stack["get_tags_for_series_search"]
    params.pop("search_words")
    returned_ok_params["expected"] = params
    returned_ok_params["check_union"] = ("tags",)
    return returned_ok(**returned_ok_params)


@pytest.mark.skipif(not ENV_API_KEY, reason="Tests need api key")
def test_get_tags_for_series_search(
    get_tags_for_series_search_method_works: bool,
):
    assert get_tags_for_series_search_method_works == True


@pytest.fixture
def get_related_tags_for_series_search_method_works(
    fred: Fred,
    returned_ok_params: dict,
) -> bool:
    params = {
        "search_words": (
            "mortgage",
            "rate",
            "index",
        ),
        "tag_names": (
            "30-year",
            "frb",
        ),
        #            'tag_search_words': ('', '',),
        "limit": 3,
        "realtime_end": "2020-02-13",
        "order_by": "name",
        "sort_order": "desc",
        "offset": 2,
    }
    fred.get_related_tags_for_series_search(**params)
    returned_ok_params["observed"] = fred.series_stack[
        "get_related_tags_for_series_search"
    ]
    params.pop("search_words")
    params.pop("tag_names")
    returned_ok_params["expected"] = params
    returned_ok_params["check_union"] = ("tags",)
    return returned_ok(**returned_ok_params)


@pytest.mark.skipif(not ENV_API_KEY, reason="Tests need api key")
def test_get_related_tags_for_series_search(
    get_related_tags_for_series_search_method_works: bool,
):
    assert get_related_tags_for_series_search_method_works == True


@pytest.fixture
def get_tags_for_a_series_method_works(
    fred: Fred,
    returned_ok_params: dict,
) -> bool:
    params = {
        "series_id": "STLFSI",
        "realtime_end": "2019-02-13",
        "order_by": "name",
        "sort_order": "desc",
    }
    fred.get_tags_for_a_series(**params)
    returned_ok_params["observed"] = fred.series_stack["get_tags_for_a_series"]
    params.pop("series_id")
    returned_ok_params["expected"] = params
    returned_ok_params["check_union"] = ("tags",)
    return returned_ok(**returned_ok_params)


@pytest.mark.skipif(not ENV_API_KEY, reason="Tests need api key")
def test_get_tags_for_a_series(
    get_tags_for_a_series_method_works: bool,
):
    assert get_tags_for_a_series_method_works == True


@pytest.mark.skipif(not ENV_API_KEY, reason="Tests need api key")
def test_get_series_updates_raises_type_error(
    fred: Fred,
):
    """
    Test TypeError raised when only one of start_time, end_time is
    passed
    """
    with pytest.raises(TypeError):
        fred.get_series_updates(start_time="202103210851")


@pytest.mark.skipif(not ENV_API_KEY, reason="Tests need api key")
def test_get_series_updates_raises_value_error(
    fred: Fred,
):
    """
    Test ValueError raised when current time - end_time > 2 weeks.
    FRED's servers send error code 500 for start dates earlier than
    last 2 weeks. if end_date is earlier than last 2 weeks, FRED will
    return 500 error code
    """
    params = {
        "start_time": "202103110851",
        "end_time": "202103210851",
    }
    with pytest.raises(ValueError):
        fred.get_series_updates(**params)


@pytest.fixture
def get_series_updates_method_works(
    fred: Fred,
    returned_ok_params: dict,
) -> bool:
    params = {
        "limit": 3,
        "filter_value": "regional",
        "offset": 2,
        "start_time": make_time_string(start=True),
        "end_time": make_time_string(start=False),
    }
    fred.get_series_updates(**params)
    returned_ok_params["observed"] = fred.series_stack["get_series_updates"]
    params.pop("start_time")
    params.pop("end_time")
    returned_ok_params["expected"] = params
    returned_ok_params["check_union"] = (
        "seriess",
        "series",
    )
    return returned_ok(**returned_ok_params)


@pytest.mark.skipif(not ENV_API_KEY, reason="Tests need api key")
def test_get_series_updates(
    get_series_updates_method_works: bool,
):
    assert get_series_updates_method_works == True


@pytest.fixture
def get_series_vintagedates_method_works(
    fred: Fred,
    returned_ok_params: dict,
) -> bool:
    params = {
        "series_id": "GNPCA",
        "limit": 3,
        "realtime_start": "1812-06-18",
        "sort_order": "desc",
        "offset": 2,
    }
    returned_ok_params["observed"] = fred.get_series_vintagedates(**params)
    params.pop("series_id")
    returned_ok_params["expected"] = params
    returned_ok_params["check_union"] = ("vintage_dates",)
    return returned_ok(**returned_ok_params)


@pytest.mark.skipif(not ENV_API_KEY, reason="Tests need api key")
def test_get_series_vintagedates(
    get_series_vintagedates_method_works: bool,
):
    assert get_series_vintagedates_method_works == True
