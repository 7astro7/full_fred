from full_fred.fred import Fred
import pytest
import os
from .fred_test_utils import returned_ok

key_file = "example_key.txt"
test_key_file = True if key_file in os.listdir() else False


@pytest.fixture
def fred():
    return Fred(api_key_file=key_file)


@pytest.mark.skipif(not test_key_file, reason="file to read api key from is absent")
def test_api_key_file_works_with_get_a_category_method(
    fred: Fred,
) -> bool:
    fred.get_a_category(0)
    returned_ok_params = {
        "observed": fred.category_stack["get_a_category"],
        "check_union": ("categories",),
    }
    return returned_ok(**returned_ok_params)


@pytest.fixture
def a_random_api_key_dummy_file() -> str:
    return "orange_juice_and_peanuts.txt"


def test_api_key_file_get_works_after_constructor(
    a_random_api_key_dummy_file: str,
):
    with pytest.raises(FileNotFoundError):
        Fred(api_key_file=a_random_api_key_dummy_file)
