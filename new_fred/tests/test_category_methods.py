
import pytest
from new_fred.fred import Fred
from .fred_test_utils import returned_ok

@pytest.fixture
def fred() -> Fred:
    return Fred()

# also test with no id
@pytest.fixture
def get_a_category_method_works(fred: Fred) -> bool:
    params = {
            'category_id': 125, 
            }
    fred.get_a_category(**params)
    observed = fred.category_stack["get_a_category"]
    check_union = ('categories',)
    return returned_ok(observed = observed, check_union = check_union)

@pytest.mark.skip("passed v2")
def test_get_a_category(
        get_a_category_method_works: bool,
        ):
    assert get_a_category_method_works == True

@pytest.fixture
def get_child_categories_method_works(fred: Fred) -> bool:
    params = {
            'category_id': 13, 
            }
    fred.get_child_categories(**params)
    observed = fred.category_stack["get_child_categories"]
    check_union = ('categories',)
    return returned_ok(observed = observed, check_union = check_union)

@pytest.mark.skip("passed v2")
def test_get_child_categories(
        get_child_categories_method_works: bool,
        ):
    assert get_child_categories_method_works == True

@pytest.fixture
def get_related_categories_method_works(fred: Fred) -> bool:
    params = {
            'category_id': 13, 
            }
    fred.get_related_categories(**params)
    observed = fred.category_stack["get_related_categories"]
    check_union = ('categories',)
    return returned_ok(observed = observed, check_union = check_union)

@pytest.mark.skip("passed v2")
def test_get_related_categories(
        get_related_categories_method_works: bool,
        ):
    assert get_related_categories_method_works == True

@pytest.fixture
def get_series_in_a_category_method_works(fred: Fred) -> bool:
    params = {
            'category_id': 125,
            'limit': 3,
            'filter_variable': 'units',
            'order_by': 'units',
            'sort_order': 'desc',
            'offset': 1,
            }
    fred.get_series_in_a_category(**params)
    observed = fred.category_stack["get_series_in_a_category"]
    params.pop('category_id')
    params.pop('filter_variable')
    expected = params
    check_union = ('series', 'seriess',)
    returned_ok_params = {
            'observed': observed, 
            'expected': expected, 
            'check_union': check_union,
            }
    return returned_ok(**returned_ok_params)

@pytest.mark.skip("passed v2")
def test_get_series_in_a_category(
    get_series_in_a_category_method_works: bool,
    ):
    assert get_series_in_a_category_method_works == True

@pytest.fixture
def get_tags_for_a_category_method_works(fred: Fred) -> bool:
    params = {
            'category_id': 125,
            'limit': 3,
            'order_by': 'created',
            'sort_order': 'desc',
            'offset': 1,
            }
    fred.get_tags_for_a_category(**params)
    observed = fred.category_stack["get_tags_for_a_category"] 
    params.pop('category_id')
    expected = params
    check_union = ('tags',)
    returned_ok_params = {
            'observed': observed, 
            'expected': expected, 
            'check_union': check_union,
            }
    return returned_ok(**returned_ok_params)

@pytest.mark.skip("passed v2")
def test_get_tags_for_a_category(
        get_tags_for_a_category_method_works: bool,
        ):
    assert get_tags_for_a_category_method_works == True

@pytest.fixture
def get_related_tags_for_a_category_method_works(fred: Fred) -> bool:
    params = {
            'category_id': 125,
            'tag_names': ('services', 'quarterly'),
            'limit': 3,
            'order_by': 'created',
            'sort_order': 'desc',
            'offset': 1,
            }
    fred.get_related_tags_for_a_category(**params)
    observed = fred.category_stack["get_related_tags_for_a_category"] 
    params.pop('category_id')
    params.pop('tag_names')
    expected = params
    check_union = ('tags',)
    returned_ok_params = {
            'observed': observed, 
            'expected': expected, 
            'check_union': check_union,
            }
    return returned_ok(**returned_ok_params)

#@pytest.mark.skip("passed v2")
def test_get_related_tags_for_a_category(
        get_related_tags_for_a_category_method_works: bool,
        ):
    assert get_related_tags_for_a_category_method_works == True


