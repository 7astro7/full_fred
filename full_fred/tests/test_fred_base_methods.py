
import pytest
from full_fred.fred_base import FredBase
from .fred_test_utils import api_key_found_in_env

ENV_API_KEY = api_key_found_in_env()

@pytest.fixture
def fredbase() -> FredBase:
    return FredBase()

@pytest.fixture
def observation_start_attr() -> str:
    return "2020-05-10"

@pytest.fixture
def observation_end_attr() -> str:
    return "2021-05-10"

@pytest.mark.skipif(not ENV_API_KEY, reason = 'Tests need api key')
def test_add_optional_params(
        fredbase: FredBase,
        observation_end_attr: str,
        observation_start_attr: str,
        ):
    """
    uses optional parameters of series.get_series_df() 
    """

    # test append_id_to_url first for specificity
    url_prefix_params = {
            "a_url_prefix": "series/observations?series_id=",
            "a_str_id": "UNRATE",
            }
    url_prefix = fredbase._append_id_to_url(**url_prefix_params)
    assert url_prefix == "series/observations?series_id=UNRATE"

    # set observation_start, observation_end: new_url_str should 
    # include the values the attributes point to
    optional_args = {
            "&realtime_start=": None,
            "&realtime_end=": None,
            "&limit=": None,
            "&offset=": None,
            "&sort_order=": None,
            "&observation_start=": None,
            "&observation_end=": None,
            "&units=": None,
            "&frequency=": None,
            "&aggregation_method=": None,
            "&output_type=": None,
            "&vintage_dates=": None,
        }
    fredbase.observation_start = observation_start_attr 
    fredbase.observation_end = observation_end_attr 
    url_string = fredbase._add_optional_params(url_prefix, optional_args)
    assert "observation_start" in url_string
    assert "observation_end" in url_string
    assert observation_start_attr in url_string
    assert observation_end_attr in url_string



