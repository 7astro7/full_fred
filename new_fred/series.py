
from .releases import Releases
import pandas as pd
import requests
import os

class Series(Releases):

    def __init__(self):
        super().__init__()
        self.series_stack = dict() 

    # fred/series

    def get_series(
            self, 
            series_id: str, 
            realtime_start: str = None, 
            realtime_end: str = None,
            ):
        """
        Get an economic data series using series_id. If the 
        series hasn't been fetched it's added to Fred.series_stack, 
        a dictionary that stores FredSeries objects 
        all parameters fred offers: y (need tags though)
        FRED accepts upper case series_id: maybe integrate something to capitalize automatically
        default realtime start and realtime end: first to last available
        if series_id attribute is not set, FredSeries.series_id will be set to 
        the series_id passed in this method
        explain that not merely the requested data is retrieved and stored but rather
        a FredSeries object is instantiated 

        Parameters
        ----------
        series_id: int
            the id of the series
        realtime_start: str, default "1776-07-04" (earliest)
            YYY-MM-DD as per fred
        realtime_end: str, default "9999-12-31" (last available) 
            YYY-MM-DD as per fred

        Returns
        -------

        Notes
        -----
        fred/series
        """
        if not series_id in self.series_stack.keys():
            self.series_stack[series_id] = FredSeries(series_id)
        params = dict(
                series_id = series_id, # revisit: series_id given in constructor above
                                        # but above code may not be executed
                realtime_start = realtime_start,
                realtime_end = realtime_end,
                )
        return self.series_stack[series_id].get_series(**params) 

    def get_categories_of_series(
            self,
            series_id: str, 
            realtime_start: str = None, 
            realtime_end: str = None,
            ):
        """
        Get the categories that FRED uses to classify series associated with series_id
        if series_id attribute is not set, FredSeries.series_id will be set to 
        the series_id passed in this method
        add examples
        explain that not merely the requested data is retrieved and stored but rather
        a FredSeries object is instantiated so the data need not be requested again: it's stored
        (but deletable to minimize risk of bloat)
        all parameters fred offers: y (need tags though)

        Parameters
        ----------
        series_id: int
            the id of the series
        realtime_start: str, default "1776-07-04" (earliest)
            YYY-MM-DD as per fred
        realtime_end: str, default "9999-12-31" (last available) 
            YYY-MM-DD as per fred

        Returns
        -------

        Notes
        -----
        fred/series/categories
        """
        if not series_id in self.series_stack.keys():
            self.series_stack[series_id] = FredSeries(series_id)
        params = dict(
                series_id = series_id, # revisit: series_id given in constructor above
                                        # but above code may not be executed
                realtime_start = realtime_start,
                realtime_end = realtime_end,
                )
        return self.series_stack[series_id].get_categories_of_series(**params) 

    def get_series_df(
            self, 
            series_id: str,
            realtime_start: str = None, 
            realtime_end: str = None,
            limit: int = 100_000,
            offset: int = 0,
            sort_order: str = 'asc',
            observation_start: str = "1776-07-04",
            observation_end: str = "9999-12-31",
            units: str = None,
            frequency: str = None,
            aggregation_method: str = None,
            output_type: int = None,
            vintage_dates: str = None,
            ):
        """
        Get the data values in (pandas) DataFrame form for series associated
        with series_id
        distinguish between observation_start and realtime_start, same for end

        Parameters
        ----------
        series_id: int
            the id of the series
        realtime_start: str, default "1776-07-04" (earliest)
            YYY-MM-DD as per fred
        realtime_end: str, default "9999-12-31" (last available) 
            YYY-MM-DD as per fred
        limit: int, default 100_000
            maximum number of observations / rows 
            range [1, 100_000]
        offset: int, default 0
            n/a, 
        sort_order: str, default 'asc' 
            return rows in ascending or descending order of observation_date 
            options are 'asc' and 'desc'
        observation_start: str, default "1776-07-04" (earliest)
            YYY-MM-DD as per fred
        observation_end: str, default "9999-12-31" (last available) 
            YYY-MM-DD as per fred
        units: str, default "lin" (no data value transformation)
            see unit_info for more information
        frequency
        aggregation_method: str, default "avg"
        output_type: int default None (realtime period)
            1: real
            2: vintage date, all observations
            3: vintage date, new and revised observations only
            4: initial release only
        vintage_dates

        Returns
        -------

        Notes
        -----
        fred/series/observations
        """
        url_prefix_params = dict(
                a_url_prefix = "series/observations?series_id=",
                a_str_id = series_id)
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
        self.series_stack[series_id] = self._fetch_data(url)
        return self.series_stack[series_id]

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
            the id of the series
        observation_start: str, default "1776-07-04" (earliest)
            YYY-MM-DD as per fred
        observation_end: str, default "9999-12-31" (last available) 
            YYY-MM-DD as per fred

        Returns
        -------
        dict

        Notes
        -----
        fred/series/release
        """
        url_prefix_params = dict(
                a_url_prefix = "series/release?series_id=",
                a_str_id = series_id)
        url_prefix = self._append_id_to_url(**url_prefix_params)
        optional_args = {
                "&realtime_start=": realtime_start,
                "&realtime_end=": realtime_end,
                }
        url = self._add_optional_params(url_prefix, optional_args)
        self.series_stack[series_id] = self._fetch_data(url)
        return self.series_stack[series_id]

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
        realtime_start: str, default "1776-07-04" (earliest)
            YYY-MM-DD as per fred
        realtime_end: str, default "9999-12-31" (last available) 
            YYY-MM-DD as per fred
        limit: int, default None (FRED will use limit = 1_000)
            maximum number of results to return
            range [1, 1_000]
        offset: non-negative integer, default None (offset of 0)
        order_by: str, default "source_count"
            order results by values of the specified attribute
            can be one of "source_count", "popularity", "created", "name", "group_id"
        sort_order: str, default None (FRED will use "asc")
            sort results in ascending or descending order for attribute values specified by order_by
        filter_variable: str default None
            the attribute to filter results by
        filter_value: str default None
            the value of the filter_variable attribute to filter results by
        tag_names: list
            list of tags (str); each tag must be present in the tag of returned series
        exclude_tag_names: list, default None (don't exclude any tags)
            tags that returned series must not have

        Returns
        -------
        dict

        Notes
        -----
        fred/series/search
        https://fred.stlouisfed.org/docs/api/fred/series_search.html
        """
        fused_search_text = self._join_strings_by(search_text, '+')
        url_prefix_params = dict(
                a_url_prefix = "series/search?search_text=",
                a_str_id = fused_search_text,
                )
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

    def get_tags_for_a_series_search(
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
        realtime_start: str, default "1776-07-04" (earliest)
            YYY-MM-DD as per fred
        realtime_end: str, default "9999-12-31" (last available) 
            YYY-MM-DD as per fred
        tag_names: list
            list of tags (str); each tag must be present in the tag of returned series
        tag_group_id: str, default None
            a tag group id to filter tags by type with
            can be one of 'freq' for frequency, 'gen' for general or concept, 
            'geo' for geography, 'geot' for geography type, 'rls' for release, 
            'seas' for seasonal adjustment, 'src' for source
        tag_search_text: list, default None (no filtering by tag group)
            the words to find matching tags with
        limit: int, default None (FRED will use limit = 1_000)
            maximum number of results to return
            range [1, 1_000]
        offset: non-negative integer, default None (offset of 0)
        order_by: str, default "source_count"
            order results by values of the specified attribute
            can be one of "source_count", "popularity", "created", "name", "group_id"
        sort_order: str, default None (FRED will use "asc")
            sort results in ascending or descending order for attribute values specified by order_by

        Returns
        -------
        dict

        Notes
        -----
        fred/series/search/tags
        """
        search_text = self._join_strings_by(series_search_text, '+')
        url_prefix_params = dict(
                a_url_prefix = "series/search/tags?series_search_text=",
                a_str_id = search_text,
                )
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

    def get_related_tags_for_a_series_search(
            self, 
            series_search_text: list,
            realtime_start: str = None,
            realtime_end: str = None,
            tag_names: list = None,
            exclude_tag_names: list = None,
            tag_group_id: str = None,
            tag_search_text: list = None,
            limit: int = None,
            offset: int = None,
            order_by: str = None,
            sort_order: str = None,
            ) -> dict:
        """
        Get the related FRED tags for a series search. 

        Parameters
        ----------
        series_search_text: list
            list or tuple or words to match against economic data series
        realtime_start: str, default "1776-07-04" (earliest)
            YYY-MM-DD as per fred
        realtime_end: str, default "9999-12-31" (last available) 
            YYY-MM-DD as per fred
        tag_names: list
            list of tags (str); each tag must be present in the tag of returned series
        exclude_tag_names: list, default None (don't exclude any tags)
            tags that returned series must not have
        tag_group_id: str, default None
            a tag group id to filter tags by type with
            can be one of 'freq' for frequency, 'gen' for general or concept, 
            'geo' for geography, 'geot' for geography type, 'rls' for release, 
            'seas' for seasonal adjustment, 'src' for source
        tag_search_text: list, default None (no filtering by tag group)
            the words to find matching tags with
        limit: int, default None (FRED will use limit = 1_000)
            maximum number of results to return
            range [1, 1_000]
        offset: non-negative integer, default None (offset of 0)
        order_by: str, default "source_count"
            order results by values of the specified attribute
            can be one of "source_count", "popularity", "created", "name", "group_id"
        sort_order: str, default None (FRED will use "asc")
            sort results in ascending or descending order for attribute values specified by order_by

        Returns
        -------
        dict

        Notes
        -----
        fred/series/search/related_tags
        """
        search_text = self._join_strings_by(series_search_text, '+')
        fused_tag_names = self._join_strings_by(tag_names, ';')
        url_prefix_params = dict(
                a_url_prefix = "series/search/related_tags?series_search_text=",
                a_str_id = search_text,
                )
        url_prefix = self._append_id_to_url(**url_prefix_params)
        url_prefix = self._append_id_to_url(url_prefix, tag_names)
        optional_args = {
                "&realtime_start=": realtime_start,
                "&realtime_end=": realtime_end,
                "&tag_names=": fused_tag_names,
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

    def get_tags_for_a_series(
            self,
            series_id: str,
            realtime_start: str = None,
            realtime_end: str = None,
            order_by: str = None,
            sort_order: str = None,
            ) -> dict:
        """
        Get the FRED tags for a series.

        Parameters
        ----------
        series_id: int
            the id of the series
        realtime_start: str, default "1776-07-04" (earliest)
            YYY-MM-DD as per fred
        realtime_end: str, default "9999-12-31" (last available) 
            YYY-MM-DD as per fred
        order_by: str, default "source_count"
            order results by values of the specified attribute
            can be one of "source_count", "popularity", "created", "name", "group_id"
        sort_order: str, default None (FRED will use "asc")
            sort results in ascending or descending order for attribute values specified by order_by

        Returns
        -------
        dict

        Notes
        -----
        fred/series/tags
        """
        url_prefix_params = dict(
                a_url_prefix = "series/tags?series_id=",
                a_str_id = series_id)
        url_prefix = self._append_id_to_url(**url_prefix_params)
        optional_args = {
                "&realtime_start=": realtime_start,
                "&realtime_end=": realtime_end,
                "&order_by=": order_by,
                "&sort_order=": sort_order,
                }
        url = self._add_optional_params(url_prefix, optional_args)
        self.series_stack[series_id] = self._fetch_data(url)
        return self.series_stack[series_id]

    def get_series_by_update(
            self,
            realtime_start: str = None,
            realtime_end: str = None,
            limit: int = None,
            offset: int = None,
            filter_value: str = None,
            start_time: str = None,
            end_time: str = None,
            ):
        """
        Get economic data series sorted by when observations were updated on the FRED server. 
        Results are limited to series updated within the last two weeks.

        fred/series/updates

        Parameters
        ----------
        realtime_start: str, default "1776-07-04" (earliest)
            YYY-MM-DD as per fred
        realtime_end: str, default "9999-12-31" (last available) 
            YYY-MM-DD as per fred
        limit: int, default None (FRED will use limit = 1_000)
            maximum number of results to return
            range [1, 1_000]
        offset: non-negative integer, default None (offset of 0)
        filter_value: str default None
        start_time: str, default None
            lower bound for a time range
            can be precise to the minute
        end_time: str, default None
            upper bound for a time range
            can be precise to the minute

        Returns
        -------
        dict

        Notes
        -----
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

        # change key used here to something more detailed for clarity
        self.series_stack['updates'] = self._fetch_data(url) 
        return self.series_stack['updates']

    def get_series_vintage_dates(
            self,
            series_id: str,
            realtime_start: str = None,
            realtime_end: str = None,
            limit: int = None,
            offset: int = None,
            sort_order: str = None,
            ) -> dict:
        """
        Get the dates in history when a series' data values were revised or new data values were released.
        Vintage dates are the release dates for a series excluding release dates when the 
        data for the series did not change.

        Parameters
        ----------
        series_id: int
            the id of the series
        realtime_start: str, default "1776-07-04" (earliest)
            YYY-MM-DD as per fred
        realtime_end: str, default "9999-12-31" (last available) 
            YYY-MM-DD as per fred
        limit: int, default None (FRED will use limit = 1_000)
            maximum number of results to return
            range [1, 1_000]
        offset: non-negative integer, default None (offset of 0)
        sort_order: str, default None (FRED will use "asc")
            sort results in ascending or descending order for attribute values specified by order_by

        Returns
        -------
        dict

        Notes
        -----
        fred/series/vintagedates
        """
        url_prefix_params = dict(
                a_url_prefix = "series/vintagedates?series_id=",
                a_str_id = series_id)
        url_prefix = self._append_id_to_url(**url_prefix_params)
        optional_args = {
                "&realtime_start=": realtime_start,
                "&realtime_end=": realtime_end,
                "&limit=": limit,
                "&offset=": offset,
                "&sort_order=": sort_order,
                }
        url = self._add_optional_params(url_prefix, optional_args)
        self.series_stack[series_id] = self._fetch_data(url)
        return self.series_stack[series_id]

