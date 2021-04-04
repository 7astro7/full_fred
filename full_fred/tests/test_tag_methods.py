
import pytest
from full_fred.fred import Fred
from .fred_test_utils import returned_ok

@pytest.fixture
def fred() -> Fred:
    return Fred()

@pytest.fixture
def get_all_tags_method_works(fred: Fred) -> bool:
    params = {
            'limit': 2,
            'sort_order' : 'desc',
            'tag_names': ('gdp', 'oecd',),
            'order_by': "name",
            }
    fred.get_all_tags(**params)
    observed = fred.tag_stack["get_all_tags"]
    params.pop('tag_names')
    expected = params
    check_union = ('tags',)
    returned_ok_params = {
            'observed': observed,
            'expected': expected,
            'check_union': check_union,
            }
    return returned_ok(**returned_ok_params)

@pytest.mark.skip("passed v2")
def test_get_all_tags(
        get_all_tags_method_works: bool,
        ):
    assert get_all_tags_method_works == True

@pytest.fixture
def get_related_tags_for_a_tag_method_works(fred: Fred) -> bool:
    params = {
            'tag_names': ('monetary aggregates', 'weekly'),
            'limit': 2,
            'tag_group_id': 'geo',
            'order_by': 'name',
            'sort_order': 'desc',
            'search_text': ('beans', 'cabbage',),
            }
    fred.get_related_tags_for_a_tag(**params)
    observed = fred.tag_stack["get_related_tags_for_a_tag"]
    params.pop('tag_names')
    params.pop('tag_group_id')
    params.pop('search_text')
    expected = params
    check_union = ('tags',)
    returned_ok_params = {
            'observed': observed,
            'expected': expected,
            'check_union': check_union,
            }
    return returned_ok(**returned_ok_params)

@pytest.mark.skip("passed v2")
def test_get_related_tags_for_a_tag(
        get_related_tags_for_a_tag_method_works: bool,
        ):
    assert get_related_tags_for_a_tag_method_works == True

@pytest.fixture
def get_series_matching_tags_method_works(fred: Fred) -> bool:
    params = {
            'tag_names': ('slovenia', 'food', 'oecd',),
            'limit': 2,
            'offset': 1,
            'order_by': 'seasonal_adjustment',
            'sort_order': 'desc',
            'realtime_start': '2000-01-01',
            'realtime_end': '2003-01-01',
            }
    fred.get_series_matching_tags(**params)
    observed = fred.tag_stack["get_series_matching_tags"]
    params.pop('tag_names')
    expected = params
    check_union = ('series', 'seriess',)
    returned_ok_params = {
            'observed': observed,
            'expected': expected,
            'check_union': check_union,
            }
    return returned_ok(**returned_ok_params)

@pytest.mark.skip("passed v2")
def test_get_series_matching_tags(
        get_series_matching_tags_method_works: bool,
        ):
    assert get_series_matching_tags_method_works == True


