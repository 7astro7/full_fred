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
def get_a_category_method_works(
    fred: Fred,
    returned_ok_params: dict,
) -> bool:
    fred.get_a_category()  # root category of 0
    returned_ok_params["observed"] = fred.category_stack["get_a_category"]
    returned_ok_params["check_union"] = ("categories",)
    return returned_ok(**returned_ok_params)


@pytest.mark.skipif(not ENV_API_KEY, reason="Tests need api key")
def test_get_a_category(
    get_a_category_method_works: bool,
):
    assert get_a_category_method_works == True


@pytest.fixture
def get_child_categories_method_works(
    fred: Fred,
    returned_ok_params: dict,
) -> bool:
    params = {
        "category_id": 13,
    }
    fred.get_child_categories(**params)
    returned_ok_params["observed"] = fred.category_stack["get_child_categories"]
    returned_ok_params["check_union"] = ("categories",)
    return returned_ok(**returned_ok_params)


@pytest.mark.skipif(not ENV_API_KEY, reason="Tests need api key")
def test_get_child_categories(
    get_child_categories_method_works: bool,
):
    assert get_child_categories_method_works == True


@pytest.fixture
def get_related_categories_method_works(
    fred: Fred,
    returned_ok_params: dict,
) -> bool:
    params = {
        "category_id": 32073,
    }
    fred.get_related_categories(**params)
    returned_ok_params["observed"] = fred.category_stack["get_related_categories"]
    returned_ok_params["check_union"] = ("categories",)
    return returned_ok(**returned_ok_params)


@pytest.mark.skipif(not ENV_API_KEY, reason="Tests need api key")
def test_get_related_categories(
    get_related_categories_method_works: bool,
):
    assert get_related_categories_method_works == True


@pytest.fixture
def get_series_in_a_category_method_works(
    fred: Fred,
    returned_ok_params: dict,
) -> bool:
    params = {
        "category_id": 125,
        "limit": 3,
        "realtime_start": "2020-01-01",
        "filter_variable": "units",
        "order_by": "units",
        "sort_order": "desc",
        "offset": 1,
    }
    fred.get_series_in_a_category(**params)
    returned_ok_params["observed"] = fred.category_stack["get_series_in_a_category"]
    params.pop("category_id")
    params.pop("filter_variable")
    returned_ok_params["expected"] = params
    returned_ok_params["check_union"] = (
        "series",
        "seriess",
    )
    return returned_ok(**returned_ok_params)


@pytest.mark.skipif(not ENV_API_KEY, reason="Tests need api key")
def test_get_series_in_a_category(
    get_series_in_a_category_method_works: bool,
):
    assert get_series_in_a_category_method_works == True


@pytest.fixture
def get_tags_for_a_category_method_works(
    fred: Fred,
    returned_ok_params: dict,
) -> bool:
    params = {
        "category_id": 125,
        "limit": 3,
        "realtime_end": "2018-05-22",
        "order_by": "created",
        "sort_order": "desc",
        "offset": 1,
    }
    fred.get_tags_for_a_category(**params)
    returned_ok_params["observed"] = fred.category_stack["get_tags_for_a_category"]
    params.pop("category_id")
    returned_ok_params["expected"] = params
    returned_ok_params["check_union"] = ("tags",)
    return returned_ok(**returned_ok_params)


@pytest.mark.skipif(not ENV_API_KEY, reason="Tests need api key")
def test_get_tags_for_a_category(
    get_tags_for_a_category_method_works: bool,
):
    assert get_tags_for_a_category_method_works == True


@pytest.fixture
def get_related_tags_for_a_category_method_works(
    fred: Fred,
    returned_ok_params: dict,
) -> bool:
    params = {
        "category_id": 125,
        "tag_names": ("services", "quarterly"),
        "limit": 3,
        "realtime_end": "2015-09-21",
        "order_by": "created",
        "sort_order": "desc",
        "offset": 1,
    }
    fred.get_related_tags_for_a_category(**params)
    returned_ok_params["observed"] = fred.category_stack[
        "get_related_tags_for_a_category"
    ]
    params.pop("category_id")
    params.pop("tag_names")
    returned_ok_params["expected"] = params
    returned_ok_params["check_union"] = ("tags",)
    return returned_ok(**returned_ok_params)


@pytest.mark.skipif(not ENV_API_KEY, reason="Tests need api key")
def test_get_related_tags_for_a_category(
    get_related_tags_for_a_category_method_works: bool,
):
    assert get_related_tags_for_a_category_method_works == True
