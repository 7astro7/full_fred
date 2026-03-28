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
def get_geo_series_group_method_works(
    fred: Fred,
    returned_ok_params: dict,
) -> bool:
    fred.get_geo_series_group(series_id="SMU56000000500000001a")
    returned_ok_params["observed"] = fred.maps_stack["get_geo_series_group"]
    returned_ok_params["check_union"] = ("series_group",)
    return returned_ok(**returned_ok_params)


@pytest.mark.skipif(not ENV_API_KEY, reason="Tests need api key")
def test_get_geo_series_group(
    get_geo_series_group_method_works: bool,
):
    assert get_geo_series_group_method_works == True


@pytest.fixture
def get_geo_series_method_works(
    fred: Fred,
    returned_ok_params: dict,
) -> bool:
    fred.get_geo_series(series_id="WIPCPI", date="2012-01-01")
    returned_ok_params["observed"] = fred.maps_stack["get_geo_series"]
    returned_ok_params["check_union"] = ("meta",)
    return returned_ok(**returned_ok_params)


@pytest.mark.skipif(not ENV_API_KEY, reason="Tests need api key")
def test_get_geo_series(
    get_geo_series_method_works: bool,
):
    assert get_geo_series_method_works == True


@pytest.fixture
def get_regional_data_method_works(
    fred: Fred,
    returned_ok_params: dict,
) -> bool:
    params = {
        "series_group": "882",
        "date": "2013-01-01",
        "region_type": "state",
        "units": "Dollars",
        "frequency": "a",
        "season": "NSA",
    }
    fred.get_regional_data(**params)
    returned_ok_params["observed"] = fred.maps_stack["get_regional_data"]
    returned_ok_params["check_union"] = ("meta",)
    return returned_ok(**returned_ok_params)


@pytest.mark.skipif(not ENV_API_KEY, reason="Tests need api key")
def test_get_regional_data(
    get_regional_data_method_works: bool,
):
    assert get_regional_data_method_works == True


@pytest.fixture
def get_shape_files_method_works(
    fred: Fred,
    returned_ok_params: dict,
) -> bool:
    fred.get_shape_files(shape="state")
    returned_ok_params["observed"] = fred.maps_stack["get_shape_files"]
    returned_ok_params["check_union"] = ("type", "features")
    return returned_ok(**returned_ok_params)


@pytest.mark.skipif(not ENV_API_KEY, reason="Tests need api key")
def test_get_shape_files(
    get_shape_files_method_works: bool,
):
    assert get_shape_files_method_works == True
