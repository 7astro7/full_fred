from .series import Series


class Sources(Series):
    def __init__(self):
        """
        FRED source = a provider of economic data series such as
        Bank of Japan, Chicago Board Options Exchange, etc.
        """
        super().__init__()
        self.source_stack = dict()

    def get_all_sources(
        self,
        realtime_start: str = None,
        realtime_end: str = None,
        limit: int = None,
        offset: int = None,
        order_by: str = None,
        sort_order: str = None,
    ) -> dict:
        """
        Get all sources of economic data.

        Parameters
        ----------
        realtime_start: str, default None
            The start of the real-time period formatted as "YYYY-MM-DD".
            If None, fred.realtime_start is used.
            If fred.realtime_start = None, FRED web service will use today's date.
        realtime_end: str, default None
            The end of the real-time period formatted as "YYYY-MM-DD".
            If None, fred.realtime_end is used.
            If fred.realtime_end = None, FRED web service will use today's date.
        limit: int, default None
            The maximum number of results to return.
            Values can be in range(1, 1_001).
            If None, FRED will use limit = 1_000.
        offset: int, default None
            Can be a non-negative int.
            If None, offset of 0 is used.
        order_by: str, default None
            Order results by values of the specified attribute.
            Can be one of "source_id", "name", "realtime_start", "realtime_end".
            If None, "source_id" is used.
        sort_order: str, default None
            Sort results in ascending or descending order for attribute values specified by order_by.
            Can be "asc" or "desc".
            If None, "asc" is used.

        Returns
        -------
        dict
            Metadata of requested FRED sources.

        See Also
        --------
        fred.get_a_source: Get metadata about a source.

        Notes
        -----
        FRED web service endpoint: fred/sources
        https://fred.stlouisfed.org/docs/api/fred/sources.html

        Examples
        --------
        >>> fred.get_all_sources(order_by = 'name', limit = 3, sort_order = 'desc')
        {'realtime_start': '2021-04-05',
        'realtime_end': '2021-04-05',
        'order_by': 'name',
        'sort_order': 'desc',
        'count': 103,
        'offset': 0,
        'limit': 3,
        'sources': [
            {'id': 57,
            'realtime_start': '2021-04-05',
            'realtime_end': '2021-04-05',
            'name': 'World Bank',
            'link': 'http://www.worldbank.org/'},
            {'id': 44, ..........
        """
        self._viable_api_key()
        url_prefix = "sources?"
        optional_args = {
            "&realtime_start=": realtime_start,
            "&realtime_end=": realtime_end,
            "&limit=": limit,
            "&offset=": offset,
            "&order_by=": order_by,
            "&sort_order=": sort_order,
        }
        url = self._add_optional_params(url_prefix, optional_args)
        self.source_stack["get_all_sources"] = self._fetch_data(url)
        return self.source_stack["get_all_sources"]

    def get_a_source(
        self,
        source_id: int,
        realtime_start: str = None,
        realtime_end: str = None,
    ) -> dict:
        """
        Get a source of economic data.

        Parameters
        ----------
        source_id: int
            The ID of the series.
        realtime_start: str, default None
            The start of the real-time period formatted as "YYYY-MM-DD".
            If None, fred.realtime_start is used.
            If fred.realtime_start = None, FRED web service will use today's date.
        realtime_end: str, default None
            The end of the real-time period formatted as "YYYY-MM-DD".
            If None, fred.realtime_end is used.
            If fred.realtime_end = None, FRED web service will use today's date.

        Returns
        -------
        dict
            Metadata of requested FRED source.

        See Also
        --------
        fred.get_all_sources: Get all sources of economic data.

        Notes
        -----
        FRED web service endpoint: fred/source
        https://fred.stlouisfed.org/docs/api/fred/source.html

        Examples
        --------
        >>> fred.get_a_source(1)
        {'realtime_start': '2021-04-05',
        'realtime_end': '2021-04-05',
        'sources': [{'id': 1,
        'realtime_start': '2021-04-05',
        'realtime_end': '2021-04-05',
        'name': 'Board of Governors of the Federal Reserve System (US)',
        'link': 'http://www.federalreserve.gov/'}]}
        """
        self._viable_api_key()
        url_prefix_params = {
            "a_url_prefix": "source?source_id=",
            "an_int_id": source_id,
        }
        url_prefix = self._append_id_to_url(**url_prefix_params)
        optional_args = {
            "&realtime_start=": realtime_start,
            "&realtime_end=": realtime_end,
        }
        url = self._add_optional_params(url_prefix, optional_args)
        self.source_stack["get_a_source"] = self._fetch_data(url)
        return self.source_stack["get_a_source"]

    def get_releases_for_a_source(
        self,
        source_id: int,
        realtime_start: str = None,
        realtime_end: str = None,
        limit: int = None,
        offset: int = None,
        order_by: str = None,
        sort_order: str = None,
    ):
        """
        Get the releases for a source.

        Parameters
        ----------
        source_id: int
            The ID of the series.
        realtime_start: str, default None
            The start of the real-time period formatted as "YYYY-MM-DD".
            If None, fred.realtime_start is used.
            If fred.realtime_start = None, FRED web service will use today's date.
        realtime_end: str, default None
            The end of the real-time period formatted as "YYYY-MM-DD".
            If None, fred.realtime_end is used.
            If fred.realtime_end = None, FRED web service will use today's date.
        limit: int, default None
            The maximum number of results to return.
            Values can be in range(1, 1_001).
            If None, FRED will use limit = 1_000.
        offset: int, default None
            Can be a non-negative int.
            If None, offset of 0 is used.
        order_by: str, default None
            Order results by values of the specified attribute.
            Can be one of "release_id", "name", "press_release", "realtime_start", "realtime_end".
            If None, "release_id" is used.
        sort_order: str, default None
            Sort results in ascending or descending order for attribute values specified by order_by.
            Can be "asc" or "desc".
            If None, "asc" is used.

        Returns
        -------
        dict
            Metadata of each release for a source.

        See Also
        --------
        fred.get_series_on_a_release: Get the series within a release of economic data.

        Notes
        -----
        FRED web service endpoint: fred/source/releases
        https://fred.stlouisfed.org/docs/api/fred/source_releases.html

        Examples
        --------
        >>> fred.get_releases_for_a_source(source_id = 1, limit = 3, order_by = 'press_release', sort_order = 'desc')
        {'realtime_start': '2021-04-05',
        'realtime_end': '2021-04-05',
        'order_by': 'press_release',
        'sort_order': 'desc',
        'count': 34,
        'offset': 0,
        'limit': 3,
        'releases': [
            {'id': 13,
            'realtime_start': '2021-04-05',
            'realtime_end': '2021-04-05',
            'name': 'G.17 Industrial Production and Capacity Utilization',
            'press_release': True,
            'link': 'http://www.federalreserve.gov/releases/g17/'},
            {'id': 14, ......
        """
        self._viable_api_key()
        url_prefix_params = {
            "a_url_prefix": "source/releases?source_id=",
            "an_int_id": source_id,
        }
        url_prefix = self._append_id_to_url(**url_prefix_params)
        optional_args = {
            "&realtime_start=": realtime_start,
            "&realtime_end=": realtime_end,
            "&limit=": limit,
            "&offset=": offset,
            "&order_by=": order_by,
            "&sort_order=": sort_order,
        }
        url = self._add_optional_params(url_prefix, optional_args)
        self.source_stack["get_releases_for_a_source"] = self._fetch_data(url)
        return self.source_stack["get_releases_for_a_source"]
