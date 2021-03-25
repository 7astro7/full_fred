
import pytest
from fredcli.fred import Fred

# ensure method coverage

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

@pytest.mark.skip("passed")
def test_get_category_id_125_returns_trade_balance(
        fred: Fred, 
        expected_get_category_id_125: dict,
        ):
    expected = expected_get_category_id_125 
    assert fred.get_a_category(125) == expected

@pytest.mark.skip("passed")
def test_get_child_categories_id_13_returns_5_children_categories(
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
        if not a_category["parent_id"] == 13:
            break
        if i == len(observed["categories"]) - 1:
            returned_correctly = True
    assert returned_correctly == True


