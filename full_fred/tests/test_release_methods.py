
import pytest
from full_fred.fred import Fred
from .fred_test_utils import returned_ok

@pytest.fixture
def fred():
    return Fred()

@pytest.fixture
def get_all_releases_method_works(fred: Fred) -> bool:
    params = {
            'limit': 2,
            'offset': 1,
            'sort_order': 'desc',
            'order_by': 'press_release',
            }
    fred.get_all_releases(**params)
    observed = fred.release_stack['get_all_releases']
    check_union = ('releases',)
    returned_ok_params = {
            'observed': observed,
            'expected': params,
            'check_union': check_union,
            }
    return returned_ok(**returned_ok_params)

@pytest.mark.skip("passed v2")
def test_get_all_releases(
        get_all_releases_method_works: bool,
        ):
    assert get_all_releases_method_works == True

@pytest.fixture
def get_release_dates_all_releases_method_works(fred: Fred) -> bool:
    params = {
            'limit': 2,
            'include_empty': True,
            'offset': 1,
            'sort_order': 'asc',
            'order_by': 'release_name',
            }
    fred.get_release_dates_all_releases(**params)
    observed = fred.release_stack['get_release_dates_all_releases']
    check_union = ('release_dates',)
    params.pop('include_empty')
    returned_ok_params = {
            'observed': observed,
            'expected': params,
            'check_union': check_union,
            }
    return returned_ok(**returned_ok_params)

@pytest.mark.skip("passed v2")
def test_get_release_dates_all_releases(
        get_release_dates_all_releases_method_works: bool,
        ):
    assert get_release_dates_all_releases_method_works == True

@pytest.fixture
def get_a_release_method_works(fred: Fred) -> bool:
    params = {
            'release_id': 53,
            }
    fred.get_a_release(**params)
    observed = fred.release_stack['get_a_release']
    check_union = ('releases',)
    returned_ok_params = {
            'observed': observed,
            'check_union': check_union,
            }
    return returned_ok(**returned_ok_params)

@pytest.mark.skip("passed v2")
def test_get_a_release(
        get_a_release_method_works: bool,
        ):
    assert get_a_release_method_works == True

@pytest.fixture
def get_release_dates_method_works(fred: Fred) -> bool:
    params = {
            'release_id': 82,
            'limit': 3,
            'include_empty': True,
            'offset': 1,
            'sort_order': 'desc',
            }
    fred.get_release_dates(**params)
    observed = fred.release_stack['get_release_dates']
    check_union = ('release_dates',)
    params.pop('release_id')
    params.pop('include_empty')
    expected = params
    returned_ok_params = {
            'observed': observed,
            'expected': expected,
            'check_union': check_union,
            }
    return returned_ok(**returned_ok_params)

@pytest.mark.skip("passed v2")
def test_get_release_dates(
        get_release_dates_method_works: bool,
        ):
    assert get_release_dates_method_works == True

@pytest.fixture
def get_series_on_a_release_method_works(fred: Fred) -> bool:
    params = {
            'release_id': 51,
            'limit': 3,
            'order_by': 'last_updated',
            'offset': 1,
            'sort_order': 'desc',
            'tag_names': ('japan',),
            }
    fred.get_series_on_a_release(**params)
    observed = fred.release_stack['get_series_on_a_release']
    check_union = ('seriess', 'series',)
    params.pop('release_id')
    params.pop('tag_names')
    expected = params
    returned_ok_params = {
            'observed': observed,
            'expected': expected,
            'check_union': check_union,
            }
    return returned_ok(**returned_ok_params)

@pytest.mark.skip("passed v2")
def test_get_series_on_a_release(
        get_series_on_a_release_method_works: bool,
        ):
    assert get_series_on_a_release_method_works == True

@pytest.fixture
def get_sources_for_a_release_method_works(fred: Fred) -> bool:
    params = {
            'release_id': 51,
            }
    fred.get_sources_for_a_release(**params)
    observed = fred.release_stack['get_sources_for_a_release']
    check_union = ('sources',)
    returned_ok_params = {
            'observed': observed,
            'check_union': check_union,
            }
    return returned_ok(**returned_ok_params)

@pytest.mark.skip("passed v2")
def test_get_sources_for_a_release(
        get_sources_for_a_release_method_works: bool,
        ):
    assert get_sources_for_a_release_method_works == True

@pytest.fixture
def get_tags_for_a_release_method_works(fred: Fred) -> bool:
    params = {
            'release_id': 86,
            'limit': 3,
            'tag_names': 'gnp',
            'offset': 3,
            'sort_order': 'desc',
            'order_by': 'created',
            }
    fred.get_tags_for_a_release(**params)
    observed = fred.release_stack['get_tags_for_a_release']
    check_union = ('tags',)
    params.pop('release_id')
    params.pop('tag_names')
    expected = params
    returned_ok_params = {
            'observed': observed,
            'expected': expected,
            'check_union': check_union,
            }
    return returned_ok(**returned_ok_params)

@pytest.mark.skip("passed v2")
def test_get_tags_for_a_release(
        get_tags_for_a_release_method_works: bool,
        ):
    assert get_tags_for_a_release_method_works == True

@pytest.fixture
def get_related_tags_for_release_method_works(fred: Fred) -> bool:
    params = {
            'release_id': 86,
            'tag_names': ('sa', 'foreign',),
            'limit': 3,
            'offset': 3,
            'sort_order': 'desc',
            'order_by': 'created',
            'realtime_end': '2013-08-14',
            }
    fred.get_related_tags_for_release(**params)
    observed = fred.release_stack['get_related_tags_for_release']
    check_union = ('tags',)
    params.pop('release_id')
    params.pop('tag_names')
    expected = params
    returned_ok_params = {
            'observed': observed,
            'expected': expected,
            'check_union': check_union,
            }
    return returned_ok(**returned_ok_params)

@pytest.mark.skip("passed v2")
def test_get_related_tags_for_release(
        get_related_tags_for_release_method_works: bool,
        ):
    assert get_related_tags_for_release_method_works == True

@pytest.fixture
def get_release_tables_method_works(fred: Fred) -> bool:
    params = {
            'release_id': 53,
            'element_id': 12886,
            'include_observation_values': True,
            }
    fred.get_release_tables(**params)
    observed = fred.release_stack['get_release_tables']
    params.pop('include_observation_values')
    expected = params
    expected['release_id'] = str(expected['release_id'])
    check_union = ('elements',)
    returned_ok_params = {
            'observed': observed,
            'expected': expected,
            'check_union': check_union,
            }
    return returned_ok(**returned_ok_params)

#@pytest.mark.skip("passed v2")
def test_get_release_tables(
        get_release_tables_method_works: bool,
        ):
    assert get_release_tables_method_works == True




