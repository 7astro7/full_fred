from datetime import datetime, timedelta
import os


def returned_ok(
    observed: dict,
    expected: dict = None,
    check_union: list = None,
) -> bool:
    """
    Parameters
    ----------
    observed: dict
        A FRED web service response.
    expected: dict
        expected key, value pairs to check observed key, value pairs against.
    check_union: list, default None
        iterable of keys; if no element of check_union is present in
        observed.keys(), return False.

    Returns
    -------
    bool
        Whether observed contains expected data.
    """
    if not isinstance(observed, dict):
        return False
    if expected is not None:
        for expected_key in expected.keys():
            if not expected_key in observed.keys():
                return False
            if expected[expected_key] != observed[expected_key]:
                return False
    if check_union is None:
        return True
    for key in check_union:
        if key in observed.keys():
            return True
    return False


def make_time_string(
    start: bool = False,
) -> str:
    """
    Method to create start_time, end_time arguments for
    test_series_methods.test_get_series_updates_method_works
    """
    time_string = datetime.now() - timedelta(days=10)  # start_time
    if not start:
        time_string = datetime.now() - timedelta(days=5)  # end_time
    return time_string.strftime(format="%Y%m%d%H%M")


def api_key_found_in_env() -> bool:
    if "FRED_API_KEY" not in os.environ.keys():
        return False
    return True
