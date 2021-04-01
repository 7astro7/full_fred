

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
    for key in check_union:
        if key in observed.keys():
            return True
    return False
