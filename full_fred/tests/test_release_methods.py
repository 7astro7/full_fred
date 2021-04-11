import pytest
from full_fred.fred import Fred
from .fred_test_utils import (
    returned_ok,
    api_key_found_in_env,
)

ENV_API_KEY = api_key_found_in_env()


@pytest.fixture
def fred():
    return Fred()


@pytest.fixture
def returned_ok_params() -> dict:
    return dict()


@pytest.fixture
def get_all_releases_method_works(
    fred: Fred,
    returned_ok_params: dict,
) -> bool:
    params = {
        "limit": 2,
        "realtime_start": "2018-02-02",
        "offset": 1,
        "sort_order": "desc",
        "order_by": "press_release",
    }
    fred.get_all_releases(**params)
    returned_ok_params["observed"] = fred.release_stack["get_all_releases"]
    returned_ok_params["check_union"] = ("releases",)
    returned_ok_params["expected"] = params
    return returned_ok(**returned_ok_params)


@pytest.mark.skipif(not ENV_API_KEY, reason="Tests need api key")
def test_get_all_releases(
    get_all_releases_method_works: bool,
):
    assert get_all_releases_method_works == True


@pytest.fixture
def get_release_dates_all_releases_method_works(
    fred: Fred,
    returned_ok_params: dict,
) -> bool:
    params = {
        "limit": 2,
        "realtime_end": "2018-02-02",
        "include_empty": True,
        "offset": 1,
        "sort_order": "asc",
        "order_by": "release_name",
    }
    fred.get_release_dates_all_releases(**params)
    returned_ok_params["observed"] = fred.release_stack[
        "get_release_dates_all_releases"
    ]
    returned_ok_params["check_union"] = ("release_dates",)
    params.pop("include_empty")
    returned_ok_params["expected"] = params
    return returned_ok(**returned_ok_params)


@pytest.mark.skipif(not ENV_API_KEY, reason="Tests need api key")
def test_get_release_dates_all_releases(
    get_release_dates_all_releases_method_works: bool,
):
    assert get_release_dates_all_releases_method_works == True


@pytest.fixture
def get_a_release_method_works(
    fred: Fred,
    returned_ok_params: dict,
) -> bool:
    params = {
        "release_id": 53,
        "realtime_end": "2018-02-02",
    }
    fred.get_a_release(**params)
    returned_ok_params["observed"] = fred.release_stack["get_a_release"]
    params.pop("release_id")
    returned_ok_params["expected"] = params
    returned_ok_params["check_union"] = ("releases",)
    return returned_ok(**returned_ok_params)


@pytest.mark.skipif(not ENV_API_KEY, reason="Tests need api key")
def test_get_a_release(
    get_a_release_method_works: bool,
):
    assert get_a_release_method_works == True


@pytest.fixture
def get_release_dates_method_works(
    fred: Fred,
    returned_ok_params: dict,
) -> bool:
    params = {
        "release_id": 82,
        "limit": 3,
        "realtime_end": "2015-02-02",
        "include_empty": True,
        "offset": 1,
        "sort_order": "desc",
    }
    fred.get_release_dates(**params)
    returned_ok_params["observed"] = fred.release_stack["get_release_dates"]
    params.pop("release_id")
    params.pop("include_empty")
    returned_ok_params["expected"] = params
    returned_ok_params["check_union"] = ("release_dates",)
    return returned_ok(**returned_ok_params)


@pytest.mark.skipif(not ENV_API_KEY, reason="Tests need api key")
def test_get_release_dates(
    get_release_dates_method_works: bool,
):
    assert get_release_dates_method_works == True


@pytest.fixture
def get_series_on_a_release_method_works(
    fred: Fred,
    returned_ok_params: dict,
) -> bool:
    params = {
        "release_id": 51,
        "limit": 3,
        "realtime_end": "2020-12-24",
        "order_by": "last_updated",
        "offset": 1,
        "sort_order": "desc",
        "tag_names": ("japan",),
    }
    fred.get_series_on_a_release(**params)
    returned_ok_params["observed"] = fred.release_stack["get_series_on_a_release"]
    returned_ok_params["check_union"] = (
        "seriess",
        "series",
    )
    params.pop("release_id")
    params.pop("tag_names")
    returned_ok_params["expected"] = params
    return returned_ok(**returned_ok_params)


@pytest.mark.skipif(not ENV_API_KEY, reason="Tests need api key")
def test_get_series_on_a_release(
    get_series_on_a_release_method_works: bool,
):
    assert get_series_on_a_release_method_works == True


@pytest.fixture
def get_sources_for_a_release_method_works(
    fred: Fred,
    returned_ok_params: dict,
) -> bool:
    params = {
        "release_id": 51,
        "realtime_start": "2020-12-24",
    }
    fred.get_sources_for_a_release(**params)
    returned_ok_params["observed"] = fred.release_stack["get_sources_for_a_release"]
    params.pop("release_id")
    returned_ok_params["expected"] = params
    returned_ok_params["check_union"] = ("sources",)
    return returned_ok(**returned_ok_params)


@pytest.mark.skipif(not ENV_API_KEY, reason="Tests need api key")
def test_get_sources_for_a_release(
    get_sources_for_a_release_method_works: bool,
):
    assert get_sources_for_a_release_method_works == True


@pytest.fixture
def get_tags_for_a_release_method_works(
    fred: Fred,
    returned_ok_params: dict,
) -> bool:
    params = {
        "release_id": 86,
        "limit": 3,
        "realtime_start": "2018-10-18",
        "tag_names": "gnp",
        "offset": 3,
        "sort_order": "desc",
        "order_by": "created",
    }
    fred.get_tags_for_a_release(**params)
    returned_ok_params["observed"] = fred.release_stack["get_tags_for_a_release"]
    returned_ok_params["check_union"] = ("tags",)
    params.pop("release_id")
    params.pop("tag_names")
    returned_ok_params["expected"] = params
    return returned_ok(**returned_ok_params)


@pytest.mark.skipif(not ENV_API_KEY, reason="Tests need api key")
def test_get_tags_for_a_release(
    get_tags_for_a_release_method_works: bool,
):
    assert get_tags_for_a_release_method_works == True


@pytest.fixture
def get_related_tags_for_release_method_works(
    fred: Fred,
    returned_ok_params: dict,
) -> bool:
    params = {
        "release_id": 86,
        "tag_names": (
            "sa",
            "foreign",
        ),
        "limit": 3,
        "offset": 3,
        "sort_order": "desc",
        "order_by": "created",
        "realtime_end": "2013-08-14",
    }
    fred.get_related_tags_for_release(**params)
    returned_ok_params["observed"] = fred.release_stack["get_related_tags_for_release"]
    params.pop("release_id")
    params.pop("tag_names")
    returned_ok_params["expected"] = params
    returned_ok_params["check_union"] = ("tags",)
    return returned_ok(**returned_ok_params)


@pytest.mark.skipif(not ENV_API_KEY, reason="Tests need api key")
def test_get_related_tags_for_release(
    get_related_tags_for_release_method_works: bool,
):
    assert get_related_tags_for_release_method_works == True


@pytest.fixture
def get_release_tables_method_works(
    fred: Fred,
    returned_ok_params: dict,
) -> bool:
    params = {
        "release_id": 53,
        "element_id": 12886,
        "include_observation_values": True,
    }
    fred.get_release_tables(**params)
    returned_ok_params["observed"] = fred.release_stack["get_release_tables"]
    params.pop("include_observation_values")
    returned_ok_params["expected"] = params
    str_release_id = str(returned_ok_params["expected"]["release_id"])
    returned_ok_params["expected"]["release_id"] = str_release_id
    returned_ok_params["check_union"] = ("elements",)
    return returned_ok(**returned_ok_params)


@pytest.mark.skipif(not ENV_API_KEY, reason="Tests need api key")
def test_get_release_tables(
    get_release_tables_method_works: bool,
):
    assert get_release_tables_method_works == True
