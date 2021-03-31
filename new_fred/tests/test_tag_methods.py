
import pytest
from new_fred.fred import Fred

# I can use the returned METAdata to test success of a method
# ensure method coverage
# test different realtime dates

# v2: limit, sort_order, tag_names

@pytest.fixture
def get_tags_method_works() -> bool:
    # add params
    params = {
            'limit': 2,
            'sort_order' : 'desc',
            'tag_names': ('gdp', 'oecd',),
            }
    observed = Fred().get_tags(**params)
    if not isinstance(observed, dict):
        return False
    if not "limit" in observed.keys():
        return False
    if not observed["limit"] == params["limit"]:
        return False
    if not "tags" in observed.keys():
        return False
    if not "sort_order" in observed.keys():
        return False
    if observed["sort_order"] != params["sort_order"]:
        return False
    return True

@pytest.mark.skip("passed v2")
def test_get_tags(
        get_tags_method_works: bool,
        ):
    assert get_tags_method_works == True

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


