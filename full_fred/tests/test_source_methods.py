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
def get_all_sources_method_works(
    fred: Fred,
    returned_ok_params: dict,
) -> bool:
    params = {
        "limit": 2,
        "realtime_start": "2000-01-01",
        "sort_order": "desc",
        "order_by": "name",
    }
    fred.get_all_sources(**params)
    returned_ok_params["observed"] = fred.source_stack["get_all_sources"]
    returned_ok_params["check_union"] = ("sources",)
    returned_ok_params["expected"] = params
    return returned_ok(**returned_ok_params)


@pytest.mark.skipif(not ENV_API_KEY, reason="Tests need api key")
def test_get_all_sources(
    get_all_sources_method_works: bool,
):
    assert get_all_sources_method_works == True


@pytest.fixture
def get_a_source_method_works(
    fred: Fred,
    returned_ok_params: dict,
) -> bool:
    params = {
        "source_id": 1,
        "realtime_end": "2009-04-09",
    }
    fred.get_a_source(**params)
    returned_ok_params["observed"] = fred.source_stack["get_a_source"]
    returned_ok_params["check_union"] = ("sources",)
    return returned_ok(**returned_ok_params)


@pytest.mark.skipif(not ENV_API_KEY, reason="Tests need api key")
def test_get_a_source(
    get_a_source_method_works: bool,
):
    assert get_a_source_method_works == True


@pytest.fixture
def get_releases_for_a_source_method_works(
    fred: Fred,
    returned_ok_params: dict,
) -> bool:
    params = {
        "source_id": 1,
        "limit": 3,
        "realtime_start": "2019-08-22",
        "order_by": "press_release",
        "sort_order": "desc",
    }
    fred.get_releases_for_a_source(**params)
    returned_ok_params["observed"] = fred.source_stack["get_releases_for_a_source"]
    params.pop("source_id")
    returned_ok_params["expected"] = params
    returned_ok_params["check_union"] = ("releases",)
    return returned_ok(**returned_ok_params)


@pytest.mark.skipif(not ENV_API_KEY, reason="Tests need api key")
def test_get_releases_for_a_source(
    get_releases_for_a_source_method_works: bool,
):
    assert get_releases_for_a_source_method_works == True
