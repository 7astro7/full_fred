from .releases import Releases
import pandas as pd
from datetime import datetime


class Series(Releases):
    def __init__(self):
        """
        FRED series = measurements of an economic variable at different points in time.
        Metadata for a series includes series id, title, frequency, seasonal adjustment,
        units, observation start, observation end, etc.
        For a series' metadata use get_series.
        For a pd.DataFrame of a series use get_series_df
        """
        super().__init__()
        self.series_stack = dict()

    def get_a_series(
        self,
        series_id: str,
        realtime_start: str = None,
        realtime_end: str = None,
    ):
        """
        Get the metadata of a FRED series.

        Parameters
        ----------
        series_id: int
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
            Title, ID, units, frequency, notes, seasonal adjustment
            condition, and other metadata of the series.

        See Also
        --------
        fred.get_series_df: Get observations of a series in pd.DataFrame form.

        Notes
        -----
        FRED web service endpoint: fred/series
        https://fred.stlouisfed.org/docs/api/fred/series.html

        Examples
        --------
        >>> fred.get_a_series(series_id = "SAHMCURRENT")
        {'realtime_start': '1776-07-04',
        'realtime_end': '9999-12-31',
        'seriess': [
            {'id': 'SAHMCURRENT',
            'realtime_start': '2019-09-06',
            'realtime_end': '9999-12-31',
            'title': 'Sahm Rule Recession Indicator',
            'observation_start': '1949-03-01',
            'observation_end': '2021-03-01',
            'frequency': 'Monthly',
            'frequency_short': 'M',
            'units': 'Percentage Points',
            'units_short': 'Percentage Points',
            'seasonal_adjustment': 'Seasonally Adjusted',
            'seasonal_adjustment_short': 'SA',
            'last_updated': '2021-04-02 08:01:39-05',
            'popularity': 44,
            'notes': 'Sahm Recession Indicator signals the start of .....
        """
        self._viable_api_key()
        url_prefix_params = {"a_url_prefix": "series?series_id=", "a_str_id": series_id}
        url_prefix = self._append_id_to_url(**url_prefix_params)
        optional_args = {
            "&realtime_start=": realtime_start,
            "&realtime_end=": realtime_end,
        }
        url = self._add_optional_params(url_prefix, optional_args)
        self.series_stack["get_a_series"] = self._fetch_data(url)
        return self.series_stack["get_a_series"]

    def get_categories_of_series(
        self,
        series_id: str,
        realtime_start: str = None,
        realtime_end: str = None,
    ):
        """
        Get the categories that FRED uses to classify a series.

        Parameters
        ----------
        series_id: int
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
            ID, name, ID of parent category for each category FRED uses to classify series_id.

        See Also
        --------
        fred.get_a_series: Get metadata of a series.

        Notes
        -----
        FRED web service endpoint: fred/series/categories
        https://fred.stlouisfed.org/docs/api/fred/series_categories.html

        Examples
        --------
        >>> fred.get_categories_of_series('SAHMCURRENT')
        {'categories': [
            {'id': 33120,
            'name': 'Recession Probabilities',
            'parent_id': 33060}]}
        """
        self._viable_api_key()
        url_prefix_params = {
            "a_url_prefix": "series/categories?series_id=",
            "a_str_id": series_id,
        }
        url_prefix = self._append_id_to_url(**url_prefix_params)
        optional_args = {
            "&realtime_start=": realtime_start,
            "&realtime_end=": realtime_end,
        }
        url = self._add_optional_params(url_prefix, optional_args)
        self.series_stack["get_categories_of_series"] = self._fetch_data(url)
        return self.series_stack["get_categories_of_series"]

    def get_series_df(
        self,
        series_id: str,
        realtime_start: str = None,
        realtime_end: str = None,
        limit: int = None,
        offset: int = None,
        sort_order: str = None,
        observation_start: str = None,
        observation_end: str = None,
        units: str = None,
        frequency: str = None,
        aggregation_method: str = None,
        output_type: int = None,
        vintage_dates: list = None,
    ) -> pd.DataFrame:
        """
        Get the observations, the data values, for an economic data
        series in a pd.DataFrame.

        Parameters
        ----------
        series_id: int
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
            Values can be in range(1, 100_001).
            If None, FRED will use limit = 100_001.
        offset: int, default None
            Non-negative integer.
            If None, offset of 0 is used.
        sort_order: str, default None
            Return rows in ascending or descending order of observation_date.
            Can be "asc" or "desc".
            If None, "asc" is used.
        observation_start: str, default None
            The start of the observation period formatted as "YYYY-MM-DD".
            If None, fred.observation_start is used.
            If fred.observation_start = None, FRED web service will use '1776-07-04' (earliest available).
        observation_end: str, default None
            The end of the observation period formatted as "YYYY-MM-DD".
            If None, fred.observation_end is used.
            If fred.observation_end = None, FRED web service will use '9999-12-31' (earliest available).
        units: str, default None
            A string that indicates a data value transformation.
            Can be one of :
                "lin" : Levels / No transformation
                "chg" : Change
                "ch1" : Change from 1 year ago
                "pch" : Percent Change
                "pc1" : Percent Change from 1 year go
                "pca" : Compounded annual rate of change
                "cch" : Continuously compounded rate of change
                "cca" : Continuously compounded annual rate of change
                "log" : Natural log
            If None, "lin": Levels / No transformation
        frequency: str, default None
            A string that indicates a lower frequency to aggregate
            values to. Frequency aggregation converts higher
            frequency series (such as daily) into lower frequency
            series (such as monthly). If a frequency is given,
            aggregation_method can indicate how aggregation is calculated.
            If None, no frequency aggregation.
            Frequency without period description can be one of:
                "d": Daily
                "w": Weekly
                "bw": Biweekly
                "m": Monthly
                "q": Quarterly
                "sa": Semiannual
                "a": Annual
            Frequency with period description can be one of:
                "wem": Weekly, Ending Monday
                "bwem": Biweekly, Ending Monday
                "wetu": Weekly, Ending Tuesday
                "wew": Weekly, Ending Wednesday
                "bwew": Biweekly, Ending Wednesday
                "weth": Weekly, Ending Thursday
                "wef": Weekly, Ending Friday
                "wesa": Weekly, Ending Saturday
                "wesu": Weekly, Ending Sunday
            Note: Attempting to aggregate from lower frequency such as annual
            into higher frequency such as daily will likely generate an error
            with no DataFrame returned.
            FRED's frequency aggregation detail is at:
            https://fred.stlouisfed.org/docs/api/fred/series_observations.html.
        aggregation_method: str, default None
            A string that indicates the aggregation method used for frequency aggregation.
            If no argument is passed for frequency parameter, aggregation_method is moot.
            Can be one of "avg", "sum", "eop" (end of period).
            If None and frequency argument is given, "avg" is used.
        output_type: int, default None
            An integer that indicates an output type.
            1: Observations by Real-Time Period
            2: Observations by Vintage Date, All Observations
            3: Observations by Vintage Date, New and Revised Observations Only
            4: Observations, Initial Release Only
            If None, 1: Observations by Real-Time Period is used.
        vintage_dates
            A list[str] of "YYY-MM-DD" formatted dates in history: FRED web service returns
            observations of the series as it existed on these historical dates.
            Specifying vintage_dates can be a substitute for specifying a realtime period.
            For more on vintage_dates, see the URL in the Notes section below.
            If None, no vintage dates are set.

        Returns
        -------
        pd.DataFrame
            DataFrame of requested observations. Metadata regarding
            the series is accessible with: f.series_stack['get_series_df']

        See Also
        --------
        Details of FRED's unit transformation: https://alfred.stlouisfed.org/help#growth_formulas

        Notes
        -----
        FRED web service endpoint:/series/observations
        https://fred.stlouisfed.org/docs/api/fred/series_observations.html

        Examples
        --------
        >>> params = {'series_id': 'GNPCA',
                    'limit': 10,
                    'realtime_start': '2003-01-01',
                    'sort_order': 'desc',
                    'offset': 1,
                    'observation_start': '1776-07-04',
                    'observation_end': '9999-12-31'}
        >>>  fred.get_series_df(**params)
          realtime_start realtime_end        date      value
        0     2020-03-26   2020-07-29  2019-01-01   19351.27
        1     2020-07-30   9999-12-31  2019-01-01  19338.371
        2     2019-03-28   2019-07-25  2018-01-01  18815.882
        3     2019-07-26   2020-07-29  2018-01-01    18897.8
        4     2020-07-30   9999-12-31  2018-01-01  18951.897
        5     2018-03-28   2018-07-26  2017-01-01  17275.268
        6     2018-07-27   2019-07-25  2017-01-01  18284.031
        7     2019-07-26   2020-07-29  2017-01-01  18344.563
        8     2020-07-30   9999-12-31  2017-01-01  18421.034
        9     2017-03-30   2017-07-27  2016-01-01    16835.2

        >>> fred.get_series_df(series_id = 'FYFSD')
            realtime_start realtime_end        date       value
        0       1998-02-02   9999-12-31  1901-06-30          63
        1       1998-02-02   9999-12-31  1902-06-30          77
        2       1998-02-02   9999-12-31  1903-06-30          45
        3       1998-02-02   9999-12-31  1904-06-30         -43
        4       1998-02-02   9999-12-31  1905-06-30         -23
        ..             ...          ...         ...         ...
        238     2020-02-12   9999-12-31  2018-09-30   -779137.0
        239     2019-10-25   2020-02-11  2019-09-30   -984388.0
        240     2020-02-12   2020-10-15  2019-09-30   -984155.0
        241     2020-10-16   9999-12-31  2019-09-30   -984388.0
        242     2020-10-16   9999-12-31  2020-09-30  -3131917.0

        [243 rows x 4 columns]
        """
        self._viable_api_key()
        url_prefix_params = {
            "a_url_prefix": "series/observations?series_id=",
            "a_str_id": series_id,
        }
        url_prefix = self._append_id_to_url(**url_prefix_params)
        optional_args = {
            "&realtime_start=": realtime_start,
            "&realtime_end=": realtime_end,
            "&limit=": limit,
            "&offset=": offset,
            "&sort_order=": sort_order,
            "&observation_start=": observation_start,
            "&observation_end=": observation_end,
            "&units=": units,
            "&frequency=": frequency,
            "&aggregation_method=": aggregation_method,
            "&output_type=": output_type,
            "&vintage_dates=": vintage_dates,
        }
        url = self._add_optional_params(url_prefix, optional_args)
        df_and_metadata = self._fetch_data(url)
        self.series_stack["get_series_df"] = df_and_metadata
        self.series_stack["get_series_df"]["series_id"] = series_id
        try:
            df = pd.DataFrame(df_and_metadata["observations"])
        except KeyError as e:
            if 'error_code' in self.series_stack["get_series_df"].keys():
                error_message = self.series_stack["get_series_df"]["error_message"]
                print(f"Error Message: {error_message}")
            else:
                print(e)
        self.series_stack["get_series_df"].pop("observations")
        self.series_stack["get_series_df"]["df"] = df
        return self.series_stack["get_series_df"]["df"]

    def get_release_for_a_series(
        self,
        series_id: str,
        realtime_start: str = None,
        realtime_end: str = None,
    ) -> dict:
        """
        Get the release for an economic data series.

        Parameters
        ----------
        series_id: int
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
            ID, name, url, other metadata of release for given realtime period.

        Notes
        -----
        FRED web service endpoint:/series/release
        https://fred.stlouisfed.org/docs/api/fred/series_release.html

        Examples
        --------
        >>> fred.get_release_for_a_series(series_id = 'IRA', realtime_end = '2014-07-04')
        {'realtime_start': '1776-07-04',
        'realtime_end': '2014-07-04',
        'releases': [
            {'id': 21,
            'realtime_start': '1996-12-12',
            'realtime_end': '1998-12-09',
            'name': 'H.6 Money Stock, Liquid Assets, and Debt Measures',
            'press_release': True,
            'link': 'http://www.federalreserve.gov/releases/h6/'},
            {'id': 21, .......
        """
        self._viable_api_key()
        url_prefix_params = {
            "a_url_prefix": "series/release?series_id=",
            "a_str_id": series_id,
        }
        url_prefix = self._append_id_to_url(**url_prefix_params)
        optional_args = {
            "&realtime_start=": realtime_start,
            "&realtime_end=": realtime_end,
        }
        url = self._add_optional_params(url_prefix, optional_args)
        self.series_stack["get_release_for_a_series"] = self._fetch_data(url)
        return self.series_stack["get_release_for_a_series"]

    def search_for_series(
        self,
        search_words: list,
        search_type: str = None,
        realtime_start: str = None,
        realtime_end: str = None,
        limit: int = None,
        offset: int = None,
        order_by: str = None,
        sort_order: str = None,
        filter_variable: str = None,
        filter_value: str = None,
        tag_names: list = None,
        exclude_tag_names: list = None,
    ) -> dict:
        """
        Get economic data series that match search_words using search_type.

        Parameters
        ----------
        search_words: list
            list of words to match against economic data series.
        search_type: str, default None
            Determines the type of search to perform.
            Can be either 'full_text', 'series_id'.
            full_text:
                Searches series' attributes title, frequency, units, tags
                via parsing words into stems.
            series_id:
                Substring search of series' IDs.
            If None, 'full_text' is used.
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
            If None, FRED will use limit = 1_001.
        offset: int, default None
            Non-negative integer.
            If None, offset of 0 is used.
        order_by: str, default None
            Order results by values of the specified attribute.
            Can be one of "search_rank", "series_id", "title",
            "units", "frequency", "seasonal_adjustment", "realtime_start",
            "realtime_end", "last_updated", "observation_start",
            "observation_end", "popularity", "group_popularity".
            If None and search_type is full_text, "search_rank" is used.
            If None and search_type is series_id, "series_id" is used.
        sort_order: str, default None
            Return rows in ascending or descending order for attribute values specified by order_by.
            Can be "asc" or "desc".
            If None and order_by is "popularity" or "search_rank", "desc" is used.
            If None and order_by is neither "popularity" nor "search_rank", "asc" is used.
        filter_variable: str default None
            The attribute to filter results by.
            Can be one of "frequency", "units", "seasonal_adjustment".
            If None, no filter is used.
        filter_value: str default None
            The value of the filter_variable attribute to filter results by.
            If None, no filter is used.
        tag_names: list, default None
            list of tags [str] that series match all of, excluding any tag not in tag_names.
            If None, no filtering by tag names.
        exclude_tag_names: list, default None
            A list of tags that returned series match none of.
            If passed, tag_names must also be passed to limit number
            of matching series (as per FRED web service)
            https://fred.stlouisfed.org/docs/api/fred/series_search.html
            If None, no tag names are excluded.

        Returns
        -------
        dict
            Metadata for each matching series.

        See Also
        --------
        fred.get_series_df: Get observations of a series in pd.DataFrame form.

        Notes
        -----
        FRED web service endpoint:/series/search
        https://fred.stlouisfed.org/docs/api/fred/series_search.html

        Examples
        --------
        >>> fred.search_for_series(('SAHM',), limit = 5)
        {'realtime_start': '1776-07-04',
        'realtime_end': '9999-12-31',
        'order_by': 'search_rank',
        'sort_order': 'desc',
        'count': 2,
        'offset': 0,
        'limit': 5,
        'seriess': [
            {'id': 'SAHMREALTIME',
            'realtime_start': '2019-09-06',
            'realtime_end': '9999-12-31',
            'title': 'Real-time Sahm Rule Recession Indicator',
            'observation_start': '1959-12-01',
            'observation_end': '2021-03-01',
            'frequency': 'Monthly',
            'frequency_short': 'M',
            'units': 'Percentage Points',
            'units_short': 'Percentage Points',
            'seasonal_adjustment': 'Seasonally Adjusted',
            'seasonal_adjustment_short': 'SA',
            'last_updated': '2021-04-02 08:01:07-05',
            'popularity': 62,
            'group_popularity': 62,
            'notes': 'Sahm Recession Indicator signals the start of a ...
            {'id': 'SAHMCURRENT', ........

        >>> fred.search_for_series(['trade', 'manufacturing',], limit = 3)
        {'realtime_start': '1776-07-04',
        'realtime_end': '9999-12-31',
        'order_by': 'search_rank',
        'sort_order': 'desc',
        'count': 384,
        'offset': 0,
        'limit': 3,
        'seriess': [
            {'id': 'ISRATIO',
            'realtime_start': '1997-03-14',
            'realtime_end': '9999-12-31',
            'title': 'Total Business: Inventories to Sales Ratio',
            'observation_start': '1948-01-01',
            'observation_end': '2021-01-01',
            'frequency': 'Monthly',
            'frequency_short': 'M',
            'units': 'Ratio',
            'units_short': 'Ratio',
            'seasonal_adjustment': 'Seasonally Adjusted',
            'seasonal_adjustment_short': 'SA',
            'last_updated': '2021-03-16 09:06:02-05',
            'popularity': 69,
            'group_popularity': 70,
            'notes': 'Effective June 14, 2001, data were ...
            {'id': 'CMRMTSPL', ........
        """
        self._viable_api_key()
        fused_search_text = self._join_strings_by(search_words, "+")
        url_prefix_params = {
            "a_url_prefix": "series/search?search_text=",
            "a_str_id": fused_search_text,
        }
        url_prefix = self._append_id_to_url(**url_prefix_params)
        optional_args = {
            "&search_type=": search_type,
            "&realtime_start=": realtime_start,
            "&realtime_end=": realtime_end,
            "&limit=": limit,
            "&offset=": offset,
            "&order_by=": order_by,
            "&sort_order=": sort_order,
            "&filter_variable=": filter_variable,
            "&filter_value=": filter_value,
            "&tag_names=": tag_names,
            "&exclude_tag_names=": exclude_tag_names,
        }
        url = self._add_optional_params(url_prefix, optional_args)
        self.series_stack["search_for_series"] = self._fetch_data(url)
        return self.series_stack["search_for_series"]

    def get_tags_for_series_search(
        self,
        search_words: list,
        realtime_start: str = None,
        realtime_end: str = None,
        tag_names: list = None,
        tag_group_id: str = None,
        tag_search_words: list = None,
        limit: int = None,
        offset: int = None,
        order_by: str = None,
        sort_order: str = None,
    ) -> dict:
        """
        Get the FRED tags for a series search.

        Parameters
        ----------
        search_words: list
            list of words to match against economic data series.
        realtime_start: str, default None
            The start of the real-time period formatted as "YYYY-MM-DD".
            If None, fred.realtime_start is used.
            If fred.realtime_start = None, FRED web service will use today's date.
        realtime_end: str, default None
            The end of the real-time period formatted as "YYYY-MM-DD".
            If None, fred.realtime_end is used.
            If fred.realtime_end = None, FRED web service will use today's date.
        tag_names: list, default None
            list of tags [str] that series match all of, excluding
            any tag not in tag_names.
            If None, no filtering by tag names.
        tag_group_id: str, default None
            A tag group id to filter tags by type with.
            can be one of 'freq' for frequency, 'gen' for general or concept,
            'geo' for geography, 'geot' for geography type, 'rls' for release,
            'seas' for seasonal adjustment, 'src' for source
            If None, no filtering by tag group is done.
        tag_search_words: list, default None
            The words to find matching tags with.
            If None, no filtering by search words is done.
        limit: int, default None
            The maximum number of results to return.
            Values can be in range(1, 1_001).
            If None, FRED will use limit = 1_001.
        offset: int, default None
            Non-negative integer.
            If None, offset of 0 is used.
        order_by: str, default None
            order results by values of the specified attribute
            can be one of "series_count", "popularity", "created", "name", "group_id"
            If None, "series_count" is used.
        sort_order: str, default None
            Return rows in ascending or descending order for
            attribute values specified by order_by.
            Can be "asc" or "desc".
            If None, "asc" is used.

        Returns
        -------
        dict
            name, group_id, notes, creation date, series count, other
            metadata for each tag.

        See Also
        --------
        fred.search_for_series: Search for data series using keywords.

        Notes
        -----
        FRED web service endpoint:/series/search/tags
        https://fred.stlouisfed.org/docs/api/fred/series_search_tags.html

        Examples
        --------
        >>> fred.get_tags_for_series_search(('SAHM',), limit = 5)
        {'realtime_start': '1776-07-04',
        'realtime_end': '9999-12-31',
        'order_by': 'series_count',
        'sort_order': 'desc',
        'count': 8,
        'offset': 0,
        'limit': 5,
        'tags': [
            {'name': 'academic data',
            'group_id': 'gen',
            'notes': '',
            'created': '2012-08-29 10:22:19-05',
            'popularity': 47,
            'series_count': 2},
            {'name': 'claudia sahm', .......

        >>> fred.get_tags_for_series_search(['trade', 'manufacturing',], limit = 3)
        {'realtime_start': '1776-07-04',
        'realtime_end': '9999-12-31',
        'order_by': 'series_count',
        'sort_order': 'desc',
        'count': 221,
        'offset': 0,
        'limit': 3,
        'tags': [
            {'name': 'usa',
            'group_id': 'geo',
            'notes': 'United States of America',
            'created': '2012-02-27 10:18:19-06',
            'popularity': 100,
            'series_count': 370},
            {'name': 'nation', ......
        """
        self._viable_api_key()
        series_search_text = self._join_strings_by(search_words, "+")
        url_prefix_params = {
            "a_url_prefix": "series/search/tags?series_search_text=",
            "a_str_id": series_search_text,
        }
        url_prefix = self._append_id_to_url(**url_prefix_params)
        optional_args = {
            "&realtime_start=": realtime_start,
            "&realtime_end=": realtime_end,
            "&tag_names=": tag_names,
            "&tag_group_id=": tag_group_id,
            "&tag_search_text=": tag_search_words,
            "&limit=": limit,
            "&offset=": offset,
            "&order_by=": order_by,
            "&sort_order=": sort_order,
        }
        url = self._add_optional_params(url_prefix, optional_args)
        self.series_stack["get_tags_for_series_search"] = self._fetch_data(url)
        return self.series_stack["get_tags_for_series_search"]

    def get_related_tags_for_series_search(
        self,
        search_words: list,
        tag_names: list,
        realtime_start: str = None,
        realtime_end: str = None,
        exclude_tag_names: list = None,
        tag_group_id: str = None,
        tag_search_words: list = None,
        limit: int = None,
        offset: int = None,
        order_by: str = None,
        sort_order: str = None,
    ) -> dict:
        """
        Get the related FRED tags for a series search.

        Parameters
        ----------
        search_words: list
            list of words to match against economic data series.
        tag_names: list
            list of tags [str] that series match all of, excluding
            any tag not in tag_names.
        realtime_start: str, default None
            The start of the real-time period formatted as "YYYY-MM-DD".
            If None, fred.realtime_start is used.
            If fred.realtime_start = None, FRED web service will use today's date.
        realtime_end: str, default None
            The end of the real-time period formatted as "YYYY-MM-DD".
            If None, fred.realtime_end is used.
            If fred.realtime_end = None, FRED web service will use today's date.
        exclude_tag_names: list, default None
            A list of tags that returned series match none of.
            If None, no tag names are excluded.
        tag_group_id: str, default None
            A tag group id to filter tags by type with.
            can be one of 'freq' for frequency, 'gen' for general or concept,
            'geo' for geography, 'geot' for geography type, 'rls' for release,
            'seas' for seasonal adjustment, 'src' for source
            If None, no filtering by tag group is done.
        tag_search_words: list, default None
            The words to find matching tags with.
            If None, no filtering by search words is done.
        limit: int, default None
            The maximum number of results to return.
            Values can be in range(1, 1_001).
            If None, FRED will use limit = 1_001.
        offset: int, default None
            Non-negative integer.
            If None, offset of 0 is used.
        order_by: str, default None
            order results by values of the specified attribute
            can be one of "series_count", "popularity", "created", "name", "group_id"
            If None, "series_count" is used.
        sort_order: str, default None
            Return rows in ascending or descending order for
            attribute values specified by order_by.
            Can be "asc" or "desc".
            If None, "asc" is used.

        Returns
        -------
        dict
            Metadata for each related tag.

        See Also
        --------
        fred.get_tags_for_series_search: Get the FRED tags for a series search.
        fred.search_for_series: Search for data series using keywords.

        Notes
        -----
        FRED web service endpoint:/series/search/related_tags
        https://fred.stlouisfed.org/docs/api/fred/series_search_related_tags.html

        Examples
        --------
        >>> fred.get_related_tags_for_series_search(('SAHM',), limit = 5, tag_names = ('claudia sahm',))
        {'realtime_start': '1776-07-04',
        'realtime_end': '9999-12-31',
        'order_by': 'series_count',
        'sort_order': 'desc',
        'count': 7,
        'offset': 0,
        'limit': 5,
        'tags': [
            {'name': 'academic data',
            'group_id': 'gen',
            'notes': '',
            'created': '2012-08-29 10:22:19-05',
            'popularity': 47,
            'series_count': 2},
            {'name': 'monthly', .......

        >>> fred.get_related_tags_for_series_search(['trade', 'manufacturing',], limit = 3, tag_names = ['usa', 'nation',])
        {'realtime_start': '1776-07-04',
        'realtime_end': '9999-12-31',
        'order_by': 'series_count',
        'sort_order': 'desc',
        'count': 165,
        'offset': 0,
        'limit': 3,
        'tags': [
            {'name': 'manufacturing',
            'group_id': 'gen',
            'notes': '',
            'created': '2012-02-27 10:18:19-06',
            'popularity': 68,
            'series_count': 242},
            {'name': 'nsa', ........
        """
        self._viable_api_key()
        series_search_text = self._join_strings_by(search_words, "+")
        fused_tag_names = "&tag_names=" + self._join_strings_by(tag_names, ";")
        url_prefix_params = {
            "a_url_prefix": "series/search/related_tags?series_search_text=",
            "a_str_id": series_search_text,
        }
        url_prefix0 = self._append_id_to_url(**url_prefix_params)
        url_prefix1 = self._append_id_to_url(url_prefix0, fused_tag_names)
        optional_args = {
            "&realtime_start=": realtime_start,
            "&realtime_end=": realtime_end,
            "&exclude_tag_names=": exclude_tag_names,
            "&tag_group_id=": tag_group_id,
            # this needs to be examined
            "&tag_search_text=": tag_search_words,
            "&limit=": limit,
            "&offset=": offset,
            "&order_by=": order_by,
            "&sort_order=": sort_order,
        }
        url = self._add_optional_params(url_prefix1, optional_args)
        self.series_stack["get_related_tags_for_series_search"] = self._fetch_data(url)
        return self.series_stack["get_related_tags_for_series_search"]

    def get_tags_for_a_series(
        self,
        series_id: str,
        realtime_start: str = None,
        realtime_end: str = None,
        order_by: str = None,
        sort_order: str = None,
    ) -> dict:
        """
        Get the FRED tags for a series. A FRED tag is an attribute
        assigned to a series, such as 'monetary aggregates',
        'weekly', 'oecd', 'slovenia', 'food', 'gdp'.

        Parameters
        ----------
        series_id: int
            The ID of the series.
        realtime_start: str, default None
            The start of the real-time period formatted as "YYYY-MM-DD".
            If None, fred.realtime_start is used.
            If fred.realtime_start = None, FRED web service will use today's date.
        realtime_end: str, default None
            The end of the real-time period formatted as "YYYY-MM-DD".
            If None, fred.realtime_end is used.
            If fred.realtime_end = None, FRED web service will use today's date.
        order_by: str, default "source_count"
            order results by values of the specified attribute
            can be one of "series_count", "popularity", "created", "name", "group_id"
            If None, "series_count" is used.
        sort_order: str, default None
            Return rows in ascending or descending order for
            attribute values specified by order_by.
            Can be "asc" or "desc".
            If None, "asc" is used.

        Returns
        -------
        dict
            name, series_count, date of creation, notes, group_id
            for each tag that's assigned to the series.

        Notes
        -----
        FRED web service endpoint:/series/tags
        https://fred.stlouisfed.org/docs/api/fred/series_tags.html

        Examples
        --------
        >>> fred.get_tags_for_a_series('FYFSD')
        {'realtime_start': '1998-02-02',
        'realtime_end': '9999-12-31',
        'order_by': 'series_count',
        'sort_order': 'desc',
        'count': 8,
        'offset': 0,
        'limit': 1000,
        'tags': [
            {'name': 'omb',
            'group_id': 'src',
            'notes': 'Office of Management and Budget',
            'created': '2012-02-27 10:18:19-06',
            'popularity': 39,
            'series_count': 6},
            {'name': 'usa', .........
        """
        self._viable_api_key()
        url_prefix_params = {
            "a_url_prefix": "series/tags?series_id=",
            "a_str_id": series_id,
        }
        url_prefix = self._append_id_to_url(**url_prefix_params)
        optional_args = {
            "&realtime_start=": realtime_start,
            "&realtime_end=": realtime_end,
            "&order_by=": order_by,
            "&sort_order=": sort_order,
        }
        url = self._add_optional_params(url_prefix, optional_args)
        self.series_stack["get_tags_for_a_series"] = self._fetch_data(url)
        return self.series_stack["get_tags_for_a_series"]

    def get_series_updates(
        self,
        realtime_start: str = None,
        realtime_end: str = None,
        limit: int = None,
        offset: int = None,
        filter_value: str = None,
        start_time: str = None,
        end_time: str = None,
    ) -> dict:
        """
        Get economic data series sorted by when observations were updated on the FRED server.
        Results are limited to series updated within the last two weeks.

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
            If None, FRED will use limit = 1_001.
        offset: int, default None
            Non-negative integer.
            If None, offset of 0 is used.
        filter_value: str, default None
            Limit results by geography.
            Can be one of:
                "macro": national
                "regional": state, county, metropolitan area
                "all": no filtering results by geography
            If None, no filtering by geographic type of series.
        start_time: str, default None
            The start time for limiting results for a time range.
            Expected format is "YYYYMMDDHhmm", 24-hour (11:59PM = 23:59).
            If start_time is passed, end_time is required.
            If None, end_time must also be None.
        end_time: str, default None
            The end time for limiting results for a time range.
            Expected format is "YYYYMMDDHhmm", 24-hour (11:59PM = 23:59).
            If end_time is passed, end_time is required.
            If None, start_time must also be None.

        Returns
        -------
        dict
            FRED series sorted by when each was last updated.
            Metadata for each series includes series_id, title,
            units of measurement, time of last update, etc.

        Notes
        -----
        FRED web service endpoint:/series/updates
        https://fred.stlouisfed.org/docs/api/fred/series_updates.html

        Examples
        --------
        >>> params = {'limit': 3,
                    'filter_value': 'macro',
                    'start_time': '202104011659',
                    'end_time': '202104061300'}
        >>> fred.get_series_updates(**params)
        {'realtime_end': '9999-12-31',
        'filter_variable': 'geography',
        'filter_value': 'macro',
        'order_by': 'last_updated',
        'sort_order': 'desc',
        'count': 31838,
        'offset': 0,
        'limit': 3,
        'seriess': [
            {'id': 'AB14AAAMT',
            'realtime_start': '1776-07-04',
            'realtime_end': '9999-12-31',
            'title': 'Total Value of Issues, with a Maturity ...
            'observation_start': '2001-01-02',
            'observation_end': '2021-04-05',
            'frequency': 'Daily',
            'frequency_short': 'D',
            'units': 'Millions of Dollars',
            'units_short': 'Mil. of $',
            'seasonal_adjustment': 'Not Seasonally Adjusted',
            'seasonal_adjustment_short': 'NSA',
            'last_updated': '2021-04-06 12:12:13-05',
            'popularity': 2,
            'notes': 'For more information, please see http://www.federalreserve.gov/releases/cp/about.htm.'},
            {'id': 'AB14AAVOL', .......

        >>> params = {'limit': 3,
                    'filter_value': 'regional',
                    'offset': 2,
                    'start_time': '202104010000',
                    'end_time': '202104060000'}
        >>> fred.get_series_updates(**params)
        {'realtime_start': '1776-07-04',
        'realtime_end': '9999-12-31',
        'filter_variable': 'geography',
        'filter_value': 'regional',
        'order_by': 'last_updated',
        'sort_order': 'desc',
        'count': 132717,
        'offset': 2,
        'limit': 3,
        'seriess': [
            {'id': 'MDINSUREDUR',
            'realtime_start': '1776-07-04',
            'realtime_end': '9999-12-31',
            'title': 'Insured Unemployment Rate in Maryland',
            'observation_start': '1986-02-08',
            'observation_end': '2021-03-20',
            'frequency': 'Weekly, Ending Saturday',
            'frequency_short': 'W',
            'units': 'Percent',
            'units_short': '%',
            'seasonal_adjustment': 'Not Seasonally Adjusted',
            'seasonal_adjustment_short': 'NSA',
            'last_updated': '2021-04-05 07:37:03-05',
            'popularity': 1,
            'notes': 'The insured unemployment rate (% of ...
            {'id': 'MDICLAIMS', ........
        """
        self._viable_api_key()
        if start_time is not None or end_time is not None:
            if start_time is None or end_time is None:
                e = "Both start_time and end_time are required if one is given"
                raise TypeError(e)
            only_digit = end_time.isdigit() and start_time.isdigit()
            correct_len = len(end_time) == len(start_time) == 12
            if not (only_digit and correct_len):
                e = "start_time and end_time must be YYYYMMDDHhmm"
                raise ValueError(e)
            diff = datetime.now() - datetime.strptime(end_time, "%Y%m%d%H%M")
            if diff.days > 14:
                e = "Start date must come from last 2 weeks"
                raise ValueError(e)
        url_prefix = "series/updates?"
        optional_args = {
            "&realtime_start=": realtime_start,
            "&realtime_end=": realtime_end,
            "&limit=": limit,
            "&offset=": offset,
            "&filter_value=": filter_value,
            "&start_time=": start_time,
            "&end_time=": end_time,
        }
        url = self._add_optional_params(url_prefix, optional_args)
        self.series_stack["get_series_updates"] = self._fetch_data(url)
        return self.series_stack["get_series_updates"]

    def get_series_vintagedates(
        self,
        series_id: str,
        realtime_start: str = None,
        realtime_end: str = None,
        limit: int = None,
        offset: int = None,
        sort_order: str = None,
    ) -> dict:
        """
        Get the dates in history when a series' data values were
        revised or new data values were released. Vintage dates are
        the release dates for a series, excluding release dates when
        the data for the series did not change.

        Parameters
        ----------
        series_id: int
            The ID of the series.
        realtime_start: str, default None
            The start of the real-time period formatted as "YYYY-MM-DD".
            If None, fred.realtime_start is used.
            If fred.realtime_start = None, FRED web service will use "1776-07-04".
        realtime_end: str, default None
            The end of the real-time period formatted as "YYYY-MM-DD".
            If None, fred.realtime_end is used.
            If fred.realtime_end = None, FRED web service will use "9999-12-31".
        limit: int, default None
            The maximum number of results to return.
            Values can be in range(1, 10_001).
            If None, FRED will use limit = 10_001.
        offset: int, default None
            Non-negative integer.
            If None, offset of 0 is used.
        sort_order: str, default None
            Return rows in ascending or descending order of vintagedate.
            Can be "asc" or "desc".
            If None, "asc" is used.

        Returns
        -------
        dict
            The vintage dates for the series.

        Notes
        -----
        FRED web service endpoint: fred/series/vintagedates
        https://fred.stlouisfed.org/docs/api/fred/series_vintagedates.html

        Examples
        --------
        >>> params = {'series_id': 'FYFSD',
                    'limit': 3,
                    'realtime_start': '1812-06-18',
                    'sort_order': 'desc'}
        >>> fred.get_series_vintagedates(**params)
        {'realtime_start': '1812-06-18',
        'realtime_end': '9999-12-31',
        'order_by': 'vintage_date',
        'sort_order': 'desc',
        'count': 46,
        'offset': 0,
        'limit': 3,
        'vintage_dates': ['2020-10-16', '2020-02-12', '2019-10-25']}
        """
        self._viable_api_key()
        url_prefix_params = {
            "a_url_prefix": "series/vintagedates?series_id=",
            "a_str_id": series_id,
        }
        url_prefix = self._append_id_to_url(**url_prefix_params)
        optional_args = {
            "&realtime_start=": realtime_start,
            "&realtime_end=": realtime_end,
            "&limit=": limit,
            "&offset=": offset,
            "&sort_order=": sort_order,
        }
        url = self._add_optional_params(url_prefix, optional_args)
        self.series_stack["get_series_vintagedates"] = self._fetch_data(url)
        return self.series_stack["get_series_vintagedates"]
