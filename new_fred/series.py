
from .releases import Releases
import pandas as pd

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

    # param docstrings are checked
    def get_a_series(
            self, 
            series_id: str, 
            realtime_start: str = None, 
            realtime_end: str = None,
            ):
        """
        Get the metadata of a FRED series. 
        FRED accepts upper case series_id: maybe integrate something to capitalize automatically
        default realtime start and realtime end: first to latest available
        if series_id attribute is not set, FredSeries.series_id will be set to 
        the series_id passed in this method
        explain that not merely the requested data is retrieved and stored but rather
        a FredSeries object is instantiated 

        Parameters
        ----------
        series_id: int
            The ID of the series.
        realtime_start: str, default None
            The start of the real-time period formatted as "YYY-MM-DD".
            If None, default realtime_start is used.
            If default isn't set by user, "1776-07-04" (earliest available) is used.
        realtime_end: str, default None
            The end of the real-time period formatted as "YYY-MM-DD".
            If None, default realtime_end is used.
            If default isn't set by user, "9999-12-31" (latest available) is used.

        Returns
        -------
        dict
            Title, ID, units, frequency, notes, seasonal adjustment 
            condition, and other metadata of the series.

        See Also
        --------
        get_series_df: get a pd.DataFrame of a series' observations / data values

        Notes
        -----
        FRED web service endpoint: fred/series
        https://fred.stlouisfed.org/docs/api/fred/series.html

        Examples
        --------
        f = Fred()
        f.get_a_series(series_id = "SAHMCURRENT")
        """
        url_prefix_params = {
                "a_url_prefix": "series?series_id=",
                "a_str_id": series_id
                }
        url_prefix = self._append_id_to_url(**url_prefix_params)
        optional_args = {
                "&realtime_start=": realtime_start,
                "&realtime_end=": realtime_end,
                }
        url = self._add_optional_params(url_prefix, optional_args)
        self.series_stack["get_a_series"] = self._fetch_data(url)
        return self.series_stack["get_a_series"]

    # param docstrings are checked
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
            The start of the real-time period formatted as "YYY-MM-DD".
            If None, default realtime_start is used.
            If default isn't set by user, "1776-07-04" (earliest available) is used.
        realtime_end: str, default None
            The end of the real-time period formatted as "YYY-MM-DD".
            If None, default realtime_end is used.
            If default isn't set by user, "9999-12-31" (latest available) is used.

        Returns
        -------
        dict
            ID, name, ID of parent category for each category FRED uses to classify series_id

        See Also
        --------
        get_series: get metadata for a series

        Notes
        -----
        FRED web service endpoint: fred/series/categories
        https://fred.stlouisfed.org/docs/api/fred/series_categories.html

        Examples
        --------
        """
        url_prefix_params = {
                "a_url_prefix": "series/categories?series_id=",
                "a_str_id": series_id
                }
        url_prefix = self._append_id_to_url(**url_prefix_params)
        optional_args = {
                "&realtime_start=": realtime_start,
                "&realtime_end=": realtime_end,
                }
        url = self._add_optional_params(url_prefix, optional_args)
        self.series_stack["get_categories_of_series"] = self._fetch_data(url)
        return self.series_stack["get_categories_of_series"]

    # param docstrings are checked EXCEPT vintage dates
    # vintage dates
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
            vintage_dates: str = None,
            ) -> pd.DataFrame:
        """
        Get the observations, the data values, for an economic data 
        series in a pd.DataFrame.

        Parameters
        ----------
        series_id: int
            The ID of the series.
        realtime_start: str, default None
            The start of the real-time period formatted as "YYY-MM-DD".
            If None, default realtime_start is used.
            If default isn't set by user, "1776-07-04" (earliest available) is used.
        realtime_end: str, default None
            The end of the real-time period formatted as "YYY-MM-DD".
            If None, default realtime_end is used.
            If default isn't set by user, "9999-12-31" (latest available) is used.
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
            The start of the observation period formatted as "YYY-MM-DD".
            If None, "1776-07-04" (earliest available) is used.
        observation_end: str, default None
            The end of the observation period formatted as "YYY-MM-DD".
            If None, "9999-12-31" (latest available) is used.
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
            If None, no vintage dates are set.

        Returns
        -------
        pd.DataFrame
            DataFrame of requested observations. Metadata regarding
            the series is accessible with: f.series_stack['get_series_df']

        See Also
        --------
        FRED's unit transformation: https://alfred.stlouisfed.org/help#growth_formulas

        Notes
        -----
        FRED web service endpoint:/series/observations
        https://fred.stlouisfed.org/docs/api/fred/series_observations.html

        Examples
        --------
        """
        url_prefix_params = {
                "a_url_prefix": "series/observations?series_id=",
                "a_str_id": series_id
                }
        url_prefix = self._append_id_to_url(**url_prefix_params)
        optional_args = {
                "&realtime_start=": realtime_start,
                "&realtime_end=": realtime_end,
                "&limit=": limit,
                "&offset=": offset,
                "&sort_order=": sort_order,
                "&observation_start": observation_start,
                "&observation_end": observation_end,
                "&units": units,
                "&frequency": frequency,
                "&aggregation_method": aggregation_method,
                "&output_type=": output_type,
                "&vintage_dates=": vintage_dates,
                }
        url = self._add_optional_params(url_prefix, optional_args)
        df_and_metadata = self._fetch_data(url)
        self.series_stack["get_series_df"] = df_and_metadata
        self.series_stack["get_series_df"]["series_id"] = series_id
        try:
            df = pd.DataFrame(df_and_metadata["observations"])
        except KeyError:
            e = "No key 'observations' found, cannot make DataFrame"
            print(e)
        self.series_stack["get_series_df"].pop("observations")
        self.series_stack["get_series_df"]["df"] = df
        return self.series_stack["get_series_df"]["df"]

    # param docstrings are checked
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
            The start of the real-time period formatted as "YYY-MM-DD".
            If None, default realtime_start is used.
            If default isn't set by user, "1776-07-04" (earliest available) is used.
        realtime_end: str, default None
            The end of the real-time period formatted as "YYY-MM-DD".
            If None, default realtime_end is used.
            If default isn't set by user, "9999-12-31" (latest available) is used.

        Returns
        -------
        dict
            ID, name, url, other metadata of release for given realtime period.

        See Also
        --------

        Notes
        -----
        FRED web service endpoint:/series/release
        https://fred.stlouisfed.org/docs/api/fred/series_release.html

        Examples
        --------
        """
        url_prefix_params = {
                "a_url_prefix": "series/release?series_id=",
                "a_str_id": series_id
                }
        url_prefix = self._append_id_to_url(**url_prefix_params)
        optional_args = {
                "&realtime_start=": realtime_start,
                "&realtime_end=": realtime_end,
                }
        url = self._add_optional_params(url_prefix, optional_args)
        self.series_stack["get_release_for_a_series"] = self._fetch_data(url)
        return self.series_stack["get_release_for_a_series"]

    # case senstivity 
    def search_for_a_series(
            self, 
            search_text: list,
            search_type: str = None,
            realtime_start: str = None,
            realtime_end: str = None,
            limit: int = None,
            offset: int = None,
            order_by: str = None,
            sort_order: str = None,
            filter_variable: str = None,
            filter_value:str = None,
            tag_names: list = None,
            exclude_tag_names: list = None,
            ) -> dict:
        """
        Get economic data series that match search_text.
        **** add fred url to each method for user reference

        Parameters
        ----------
        search_text: list
            list or tuple or words to match against economic data series
        search_type: str
            one of: 'full_text', 'series_id'
            *** explain with reference to fred web service
            determines the type of search to perform
            If None,
        realtime_start: str, default "1776-07-04" (earliest available)
            YYY-MM-DD as per fred
            If None,
        realtime_end: str, default "9999-12-31" (latest available) 
            YYY-MM-DD as per fred
            If None,
        limit: int, default None (FRED will use limit = 1_000)
            maximum number of results to return
            range [1, 1_000]
            If None,
        offset: non-negative integer, default None (offset of 0)
            Non-negative integer.
            If None,
        order_by: str, default "source_count"
            order results by values of the specified attribute
            can be one of "source_count", "popularity", "created", "name", "group_id"
            If None,
        sort_order: str, default None (FRED will use "asc")
            sort results in ascending or descending order for attribute values specified by order_by
            If None,
        filter_variable: str default None
            the attribute to filter results by
            If None,
        filter_value: str default None
            the value of the filter_variable attribute to filter results by
            If None,
        tag_names: list
            list of tags (str); each tag must be present in the tag of returned series
            If None,
        exclude_tag_names: list, default None (don't exclude any tags)
            tags that returned series must not have
            If None,

        Returns
        -------
        dict

        See Also
        --------

        Notes
        -----
        FRED web service endpoint:/series/search
        https://fred.stlouisfed.org/docs/api/fred/series_search.html

        Examples
        --------
        """
        fused_search_text = self._join_strings_by(search_text, '+')
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
        self.series_stack[fused_search_text] = self._fetch_data(url)
        return self.series_stack[fused_search_text]

    def get_tags_for_series_search(
            self, 
            series_search_text: list,
            realtime_start: str = None,
            realtime_end: str = None,
            tag_names: list = None,
            tag_group_id: str = None,
            tag_search_text: list = None,
            limit: int = None,
            offset: int = None,
            order_by: str = None,
            sort_order: str = None,
            ) -> dict:
        """
        Get the FRED tags for a series search. 

        Parameters
        ----------
        series_search_text: list
            list or tuple or words to match against economic data series
        search_type: str
            one of: 'full_text', 'series_id'
            *** explain with reference to fred web service
            determines the type of search to perform
            If None,
        realtime_start: str, default "1776-07-04" (earliest available)
            YYY-MM-DD as per fred
            If None,
        realtime_end: str, default "9999-12-31" (latest available) 
            YYY-MM-DD as per fred
            If None,
        tag_names: list
            list of tags (str); each tag must be present in the tag of returned series
            If None,
        tag_group_id: str, default None
            a tag group id to filter tags by type with
            can be one of 'freq' for frequency, 'gen' for general or concept, 
            'geo' for geography, 'geot' for geography type, 'rls' for release, 
            'seas' for seasonal adjustment, 'src' for source
            If None,
        tag_search_text: list, default None (no filtering by tag group)
            the words to find matching tags with
            If None,
        limit: int, default None (FRED will use limit = 1_000)
            maximum number of results to return
            range [1, 1_000]
            If None,
        offset: non-negative integer, default None (offset of 0)
            Non-negative integer.
            If None,
        order_by: str, default "source_count"
            order results by values of the specified attribute
            can be one of "source_count", "popularity", "created", "name", "group_id"
            If None,
        sort_order: str, default None (FRED will use "asc")
            sort results in ascending or descending order for attribute values specified by order_by
            If None,

        Returns
        -------
        dict

        See Also
        --------

        Notes
        -----
        FRED web service endpoint:/series/search/tags

        Examples
        --------
        """
        search_text = self._join_strings_by(series_search_text, '+')
        url_prefix_params = {
                "a_url_prefix": "series/search/tags?series_search_text=",
                "a_str_id": search_text,
                }
        url_prefix = self._append_id_to_url(**url_prefix_params)
        optional_args = {
                "&realtime_start=": realtime_start,
                "&realtime_end=": realtime_end,
                "&tag_names=": tag_names,
                "&tag_group_id=": tag_group_id,
                "&tag_search_text=": tag_search_text,
                "&limit=": limit,
                "&offset=": offset,
                "&order_by=": order_by,
                "&sort_order=": sort_order,
                }
        url = self._add_optional_params(url_prefix, optional_args)
        self.series_stack[search_text] = self._fetch_data(url)
        return self.series_stack[search_text]

    # param docstrings are checked
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
        tag_names: list, default None
            list of tags [str] that series match all of, excluding 
            any tag not in tag_names.
        realtime_start: str, default None
            The start of the real-time period formatted as "YYY-MM-DD".
            If None, default realtime_start is used.
            If default isn't set by user, "1776-07-04" (earliest available) is used.
        realtime_end: str, default None
            The end of the real-time period formatted as "YYY-MM-DD".
            If None, default realtime_end is used.
            If default isn't set by user, "9999-12-31" (latest available) is used.
        exclude_tag_names: list, default None 
            A list of tags that returned series match none of.
            If None, no tag names are excluded.
        tag_group_id: str, default None
            A tag group id to filter tags by type with.
            can be one of 'freq' for frequency, 'gen' for general or concept, 
            'geo' for geography, 'geot' for geography type, 'rls' for release, 
            'seas' for seasonal adjustment, 'src' for source
            If None, no filtering by tag group is done.
        tag_search_words: list, default None (no filtering by tag group)
            The words to find matching tags with.
            If None, no filtering by search words is done.
        limit: int, default None 
            The maximum number of results to return.
            Values can be in range(1, 1_001).
            If None, FRED will use limit = 1_001.
        offset: int, default None
            Non-negative integer.
            If None, offset of 0 is used.
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

        See Also
        --------
        get_tags_for_series_search:

        Notes
        -----
        FRED web service endpoint:/series/search/related_tags
        https://fred.stlouisfed.org/docs/api/fred/series_search_related_tags.html

        Examples
        --------
        """
        series_search_text = self._join_strings_by(search_words, '+')
        fused_tag_names = "&tag_names=" + self._join_strings_by(tag_names, ';')
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
#        breakpoint()
        self.series_stack["get_related_tags_for_series_search"] = self._fetch_data(url)
        return self.series_stack["get_related_tags_for_series_search"]

    # param docstrings are checked
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
            The start of the real-time period formatted as "YYY-MM-DD".
            If None, default realtime_start is used.
            If default isn't set by user, "1776-07-04" (earliest available) is used.
        realtime_end: str, default None
            The end of the real-time period formatted as "YYY-MM-DD".
            If None, default realtime_end is used.
            If default isn't set by user, "9999-12-31" (latest available) is used.
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

        See Also
        --------

        Notes
        -----
        FRED web service endpoint:/series/tags
        https://fred.stlouisfed.org/docs/api/fred/series_tags.html

        Examples
        --------
        """
        url_prefix_params = {
                "a_url_prefix": "series/tags?series_id=",
                "a_str_id": series_id
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

    # param docstrings are checked
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
            The start of the real-time period formatted as "YYY-MM-DD".
            If None, default realtime_start is used.
            If default isn't set by user, "1776-07-04" (earliest available) is used.
        realtime_end: str, default None
            The end of the real-time period formatted as "YYY-MM-DD".
            If None, default realtime_end is used.
            If default isn't set by user, "9999-12-31" (latest available) is used.
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
            Expected format is "YYYMMDDHhmm". 
            "1999-12-31 23:59": "199912312359"
            Can filter down to minutes.
            If start_time is passed, end_time is required.
            If None, end_time must also be None.
        end_time: str, default None
            The end time for limiting results for a time range.
            If end_time is passed, end_time is required.
            If None, start_time must also be None.

        Returns
        -------
        dict
            FRED series sorted by when each was last updated.
            Metadata for each series includes series_id, title,
            units of measurement, time of last update, etc.

        See Also
        --------

        Notes
        -----
        FRED web service endpoint:/series/updates
        https://fred.stlouisfed.org/docs/api/fred/series_updates.html

        Examples
        --------
        """
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
        self.series_stack['get_series_updates'] = self._fetch_data(url) 
        return self.series_stack['get_series_updates']

    # param docstrings are checked
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
        the release dates for a series excluding release dates when 
        the data for the series did not change.

        Parameters
        ----------
        series_id: int
            The ID of the series.
        realtime_start: str, default None
            The start of the real-time period formatted as "YYY-MM-DD".
            If None, default realtime_start is used.
            If default isn't set by user, "1776-07-04" (earliest available) is used.
        realtime_end: str, default None
            The end of the real-time period formatted as "YYY-MM-DD".
            If None, default realtime_end is used.
            If default isn't set by user, "9999-12-31" (latest available) is used.
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
            

        See Also
        --------

        Notes
        -----
        FRED web service endpoint: fred/series/vintagedates
        https://fred.stlouisfed.org/docs/api/fred/series_vintagedates.html

        Examples
        --------
        """
        url_prefix_params = {
                "a_url_prefix": "series/vintagedates?series_id=",
                "a_str_id": series_id
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

