import pytest
from full_fred.fred import Fred
from .fred_test_utils import (
    returned_ok,
    api_key_found_in_env,
)

ENV_API_KEY = api_key_found_in_env()


@pytest.fixture
def fred() -> Fred:
    return Fred()


@pytest.fixture
def returned_ok_params() -> dict:
    return dict()


@pytest.fixture
def get_all_tags_method_works(
    fred: Fred,
    returned_ok_params: dict,
) -> bool:
    params = {
        "limit": 2,
        "realtime_start": "1950-12-19",
        "sort_order": "desc",
        "tag_names": (
            "gdp",
            "oecd",
        ),
        "order_by": "name",
    }
    fred.get_all_tags(**params)
    returned_ok_params["observed"] = fred.tag_stack["get_all_tags"]
    params.pop("tag_names")
    returned_ok_params["expected"] = params
    returned_ok_params["check_union"] = ("tags",)
    return returned_ok(**returned_ok_params)


@pytest.mark.skipif(not ENV_API_KEY, reason="Tests need api key")
def test_get_all_tags(
    get_all_tags_method_works: bool,
):
    assert get_all_tags_method_works == True


@pytest.fixture
def get_related_tags_for_a_tag_method_works(
    fred: Fred,
    returned_ok_params: dict,
) -> bool:
    params = {
        "tag_names": ("monetary aggregates", "weekly"),
        "limit": 2,
        "tag_group_id": "geo",
        "order_by": "name",
        "sort_order": "desc",
        "search_text": (
            "beans",
            "cabbage",
        ),
    }
    fred.get_related_tags_for_a_tag(**params)
    returned_ok_params["observed"] = fred.tag_stack["get_related_tags_for_a_tag"]
    params.pop("tag_names")
    params.pop("tag_group_id")
    params.pop("search_text")
    returned_ok_params["expected"] = params
    returned_ok_params["check_union"] = ("tags",)
    return returned_ok(**returned_ok_params)


@pytest.mark.skipif(not ENV_API_KEY, reason="Tests need api key")
def test_get_related_tags_for_a_tag(
    get_related_tags_for_a_tag_method_works: bool,
):
    assert get_related_tags_for_a_tag_method_works == True


@pytest.fixture
def get_series_matching_tags_method_works(
    fred: Fred,
    returned_ok_params: dict,
) -> bool:
    params = {
        "tag_names": (
            "slovenia",
            "food",
            "oecd",
        ),
        "limit": 2,
        "offset": 1,
        "order_by": "seasonal_adjustment",
        "sort_order": "desc",
        #            'realtime_start': '2000-01-01',
        "realtime_end": "2003-01-01",
    }
    fred.get_series_matching_tags(**params)
    returned_ok_params["observed"] = fred.tag_stack["get_series_matching_tags"]
    params.pop("tag_names")
    returned_ok_params["expected"] = params
    returned_ok_params["check_union"] = (
        "series",
        "seriess",
    )
    return returned_ok(**returned_ok_params)


@pytest.mark.skipif(not ENV_API_KEY, reason="Tests need api key")
def test_get_series_matching_tags(
    get_series_matching_tags_method_works: bool,
):
    assert get_series_matching_tags_method_works == True
