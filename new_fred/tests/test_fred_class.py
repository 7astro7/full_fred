
import pytest
from new_fred.fred import Fred

# I can use the returned METAdata to test success of a method
# ensure method coverage
# test different realtime dates

@pytest.fixture
def fred():
    return Fred()

@pytest.fixture
def expected_get_category_id_125():
    expected = {
        'categories': [
            {'id': 125, 
            'name': 'Trade Balance', 
            'parent_id': 13}
            ]
        }
    return expected

@pytest.fixture
def expected_get_series_id():
    """
    The expected value associated with key 'id' in the map returned
    by fred.get_series('GNPCA')
    """
    return "GNPCA"

@pytest.fixture
def expected_get_series_title():
    """
    The expected value associated with key 'title' in the map returned
    by fred.get_series('GNPCA')
    """
    return "Real Gross National Product"

@pytest.mark.skip("passed v1")
def test_get_category_id_125_returns_trade_balance(
        fred: Fred, 
        expected_get_category_id_125: dict,
        ):
    expected = expected_get_category_id_125 
    assert fred.get_a_category(125) == expected

@pytest.fixture
def expected_names_get_categories_of_series():
    return ("Japan", "Monthly Rates",)

@pytest.mark.skip("passed v1")
def test_get_child_categories_id_13_returns_children_with_parentid_13(
        fred: Fred, 
        ):
    """
    New child categories may be added to the category subtree rooted 
    at "U.S. Trade and Transactions" (category_id 13) and make this 
    test fail despite fred.get_child_categories(13) returning the 
    requested data. Instead of testing equivalence it makes more 
    sense to test whether each category returned by the method call 
    has parent_id of 13
    """
    returned_correctly = False
    observed = fred.get_child_categories(13) 
    for i in range(len(observed["categories"])):
        a_category = observed["categories"][i]
        if "parent_id" not in a_category.keys():
            break
        if a_category["parent_id"] != 13:
            break
        if i == len(observed["categories"]) - 1:
            returned_correctly = True
    assert returned_correctly == True


@pytest.mark.skip("passed v1")
def test_get_series(
        fred: Fred,
        expected_get_series_id: str,
        expected_get_series_title: str,
        ):
    returned_correctly = False
    observed = fred.get_series("GNPCA")
    if "id" in observed.keys():
        if not observed["id"] == expected_get_series_id:
            assert returned_correctly == True
    if "title" in observed.keys():
        if not observed["title"] == expected_get_series_title: 
            assert returned_correctly == True
    returned_correctly = True
    assert returned_correctly == True

@pytest.mark.skip("passed v1")
def test_get_categories_of_series(
        fred: Fred,
        expected_names_get_categories_of_series: tuple,
        ):
    returned_correctly = False
    observed = fred.get_categories_of_series("EXJPUS")
    if not isinstance(observed, dict):
        assert returned_correctly == True
    if not "categories" in observed.keys():
        assert returned_correctly == True
    categories = observed["categories"] # categories is a list
    expected_keys = ("id", "name", "parent_id")
    for key in categories[0].keys():
        if key not in expected_keys:
            assert returned_correctly == True
    expected_names = expected_names_get_categories_of_series
    for a_category in categories:
        if expected_names[0] in a_category.values():
            returned_correctly = True
        if expected_names[1] in a_category.values():
            returned_correctly = True
    assert returned_correctly == True

@pytest.fixture
def tags_for_get_series_matching_tags():
    return ("food", "slovenia",)

@pytest.mark.skip("passed v1")
def test_get_series_matching_tags(
        fred: Fred,
        tags_for_get_series_matching_tags: tuple,
        ):
    returned_correctly = False
    tag_names = tags_for_get_series_matching_tags
    observed = fred.get_series_matching_tags(tag_names)
    if not isinstance(observed, dict):
        assert returned_correctly == True
    observed_keys = tuple(observed.keys())
    for k in range(len(observed_keys)):
        if "series" in observed_keys[k]:
            key_name = observed_keys[k] # fred returns this key as 'seriess'
            # key_name will be 'seriess' or 'series'
            break
        if k == len(observed_keys) - 1:
            assert returned_correctly == True

    # returned_series: list of dicts where each has metadata about a series
    returned_series = observed[key_name] 
    n = len(returned_series) 

    for i in range(n):
        a_series = returned_series[i]
        # join to create 1 string to check: avoid nested loop
        matching_series_keys = "".join(a_series.keys()).lower()
        if "title" not in matching_series_keys:
            break
        food = tag_names[0] in a_series["title"].lower()
        slovenia = tag_names[1] in a_series["title"].lower()
        if not (food or slovenia): 
            break
        if i == n - 1:
            returned_correctly = True
    assert returned_correctly == True

@pytest.fixture
def get_a_release_method_works() -> bool:
    observed = Fred().get_a_release(53)
    if not "releases" in observed.keys():
        return False
    releases_list = observed["releases"] # list of dicts
    if "id" in releases_list[0].keys():
        if releases_list[0]["id"] == 53:
            return True
    return False

@pytest.mark.skip("passed v1")
def test_get_a_release(get_a_release_method_works: bool):
    assert get_a_release_method_works == True

@pytest.fixture
def get_release_tables_method_works() -> bool:
    observed = Fred().get_release_tables(53)
    if not isinstance(observed, dict):
        return False
    observed_keys = tuple(observed.keys())
    for i in range(len(observed_keys)):
        if "release" in observed_keys[i]:
            key = observed_keys[i]
            break
        if i == len(observed_keys) - 1:
            return False
    if isinstance(observed[key], list):
        nested_dict = observed[key][0]
        for k in nested_dict.keys():
            if "id" in k:
                if not str(nested_dict[k]) == "53":
                    return False
    return True

@pytest.mark.skip("passed v1")
def test_get_release_tables(get_release_tables_method_works: bool):
    assert get_release_tables_method_works == True

@pytest.fixture
def get_related_tags_for_a_tag_method_works():
    params = dict(tag_names = ('monetary+aggregates', 'weekly'),
            limit = 5)
    observed = Fred().get_related_tags_for_a_tag(**params)
#    breakpoint()
    if not isinstance(observed, dict):
        return False
    if not "tags" in observed.keys():
        return False
    return True

@pytest.mark.skip("passed v1")
def test_get_related_tags_for_a_tag(
        get_related_tags_for_a_tag_method_works: bool,
        ):
    assert get_related_tags_for_a_tag_method_works == True

@pytest.fixture
def get_related_categories_method_works():
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
    assert get_related_categories_method_works == True

@pytest.fixture
def get_series_in_a_category_method_works() -> bool:
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
    assert get_series_in_a_category_method_works == True

@pytest.fixture
def get_tags_for_a_category_method_works() -> bool:
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
    assert get_tags_for_a_category_method_works == True

@pytest.fixture
def get_related_tags_for_a_category_method_works() -> bool:
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
    assert get_related_tags_for_a_category_method_works == True

@pytest.fixture
def get_release_dates_of_release_works() -> bool:
    params = {
            'release_id': 82,
            'limit': 3,
            }
    observed = Fred().get_release_dates(**params)
#    breakpoint()
    if not isinstance(observed, dict):
        return False
    if not "limit" in observed.keys():
        return False
    if not observed['limit'] == params['limit']:
        return False
    if not "release_dates" in observed.keys():
        return False
    release_dates_map = observed["release_dates"]
    for dated_release_map in release_dates_map:
        if not isinstance(dated_release_map, dict):
            return False
        if not "release_id" in dated_release_map.keys():
            return False
        if not dated_release_map["release_id"] == params["release_id"]:
            return False
    return True

@pytest.mark.skip("passed v1")
def test_get_release_dates_of_release(
        get_release_dates_of_release_works: bool,
        ):
    assert get_release_dates_of_release_works == True

@pytest.fixture
def get_a_source_method_works() -> bool:
    params = {
            'source_id': 1,
            }
    observed = Fred().get_a_source(**params)
    if not isinstance(observed, dict):
        return False
    if not "sources" in observed.keys():
        return False
    list_of_source_maps = observed['sources']
#    breakpoint()
    for a_source_map in list_of_source_maps:
        if not "id" in a_source_map.keys():
            return False
        if a_source_map["id"] != params["source_id"]:
            return False
    return True

@pytest.mark.skip("passed v1")
def test_get_a_source(
        get_a_source_method_works: bool,
        ):
    assert get_a_source_method_works == True

