
import pytest
from full_fred.fred import Fred
from .fred_test_utils import returned_ok

@pytest.fixture
def fred() -> Fred:
    return Fred()

@pytest.fixture
def get_all_sources_method_works(fred: Fred) -> bool:
    params = {
            'limit': 2,
            'sort_order': 'desc',
            'order_by': 'name',
            }
    fred.get_all_sources(**params)
    observed = fred.source_stack["get_all_sources"]
    check_union = ('sources',)
    expected = params
    returned_ok_params = {
            'observed': observed,
            'expected': expected,
            'check_union': check_union,
            }
    return returned_ok(**returned_ok_params)

@pytest.mark.skip("passed v2")
def test_get_all_sources(
        get_all_sources_method_works: bool,
        ):
    assert get_all_sources_method_works == True

@pytest.fixture
def get_a_source_method_works(fred: Fred) -> bool:
    params = {
            'source_id': 1,
            }
    fred.get_a_source(**params)
    observed = fred.source_stack["get_a_source"]
    check_union = ('sources',)
    returned_ok_params = {
            'observed': observed,
            'check_union': check_union,
            }
    return returned_ok(**returned_ok_params)

@pytest.mark.skip("passed v2")
def test_get_a_source(
        get_a_source_method_works: bool,
        ):
    assert get_a_source_method_works == True

@pytest.fixture
def get_releases_for_a_source_method_works(fred: Fred) -> bool:
    params = {
            'source_id': 1,
            'limit': 3,
            'order_by': 'press_release',
            'sort_order': 'desc',
            }
    fred.get_releases_for_a_source(**params)
    observed = fred.source_stack["get_releases_for_a_source"]
    check_union = ('releases',)
    params.pop('source_id')
    expected = params
    returned_ok_params = {
            'observed': observed,
            'expected': expected,
            'check_union': check_union,
            }
    return returned_ok(**returned_ok_params)

@pytest.mark.skip("passed v2")
def test_get_releases_for_a_source(
        get_releases_for_a_source_method_works: bool,
        ):
    assert get_releases_for_a_source_method_works == True


