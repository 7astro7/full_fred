
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

#@pytest.mark.skip("passed v2")
def test_get_child_categories(
        get_child_categories_method_works: bool,
        ):
    assert get_child_categories_method_works == True

@pytest.fixture
def get_related_categories_method_works():
    # fred/category/related
    observed = Fred().get_related_categories(32073)
    if not isinstance(observed, dict):
        return False
    if not "categories" in observed.keys():
        return False
    list_of_categories_maps = observed["categories"]
    for a_series_map in list_of_categories_maps:
        if not "parent_id" in a_series_map.keys():
            break
        if a_series_map["parent_id"] == 27281:
            return True
    return False

@pytest.mark.skip("passed v1")
def test_get_related_categories(
        get_related_categories_method_works: bool,
        ):
    # fred/category/related
    assert get_related_categories_method_works == True

@pytest.fixture
def get_series_in_a_category_method_works() -> bool:
    # fred/category/series
    params = {
            'category_id': 125,
            'limit': 3,
            }
    observed = Fred().get_series_in_a_category(**params)
    if not isinstance(observed, dict):
        return False
    if not "limit" in observed.keys():
        return False
    if not observed['limit'] == params['limit']:
        return False
    for k in observed.keys():
        if 'series' in k:
            return True
    return False

@pytest.mark.skip("passed v1")
def test_get_series_in_a_category(
    get_series_in_a_category_method_works: bool,
    ):
    # fred/category/series
    assert get_series_in_a_category_method_works == True

@pytest.fixture
def get_tags_for_a_category_method_works() -> bool:
    # fred/category/tags
    params = {
            'category_id': 125,
            'limit': 3,
            }
    observed = Fred().get_tags_for_a_category(**params)
#    breakpoint()
    if not isinstance(observed, dict):
        return False
    if not "limit" in observed.keys():
        return False
    if not observed['limit'] == params['limit']:
        return False
    for k in observed.keys():
        if 'tags' in k:
            return True
    return False

@pytest.mark.skip("passed v1")
def test_get_tags_for_a_category(
        get_tags_for_a_category_method_works: bool,
        ):
    # fred/category/tags
    assert get_tags_for_a_category_method_works == True

@pytest.fixture
def get_related_tags_for_a_category_method_works() -> bool:
    # fred/category/related_tags
    params = {
            'category_id': 125,
            'tag_names': ('services', 'quarterly'),
            'limit': 3,
            }
    observed = Fred().get_related_tags_for_a_category(**params)
#    breakpoint()
    if not isinstance(observed, dict):
        return False
    if not "limit" in observed.keys():
        return False
    if not observed['limit'] == params['limit']:
        return False
    for k in observed.keys():
        if 'tags' in k:
            return True
    return False

@pytest.mark.skip("passed v1")
def test_get_related_tags_for_a_category(
        get_related_tags_for_a_category_method_works: bool,
        ):
    # fred/category/related_tags
    assert get_related_tags_for_a_category_method_works == True
