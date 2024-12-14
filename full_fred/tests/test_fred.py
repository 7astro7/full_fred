import pytest

from full_fred.fred import Fred


@pytest.fixture
def fred() -> Fred:
    return Fred(observation_start="2024-01-01", observation_end="2024-06-30")


def test_observation_start_end_assigned(fred: Fred):
    assert fred.observation_start == "2024-01-01"
    assert fred.observation_end == "2024-06-30"
