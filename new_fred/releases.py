
from .categories import Categories
import pandas as pd
import requests
import os


class Releases(Categories):

    def __init__(self):
        super().__init__()
        self.release_stack = dict()

    # fred/release 

    def get_all_releases(
            self,
            realtime_start: str = None, 
            realtime_end: str = None,
            limit: int = None,
            offset: int = None,
            order_by: str = None,
            sort_order: str = None,
            ) -> dict:
        """
        Get all releases of economic data.

        Parameters
        ----------
        realtime_start: str, default "1776-07-04" (earliest)
            YYY-MM-DD as per fred
        realtime_end: str, default "9999-12-31" (last available) 
            YYY-MM-DD as per fred
        limit: int default None
        offset: int default None
        order_by: str default None
        sort_order: str default None

        Returns 
        -------
        dict

        Notes
        -----
        fred/releases
        """
        url_prefix = "releases?"
        optional_args = {
                "&realtime_start=": realtime_start,
                "&realtime_end=": realtime_end,
                "&limit=": limit,
                "&offset=": offset,
                "&order_by=": order_by,
                "&sort_order=": sort_order,
            }
        url = self._add_optional_params(url_prefix, optional_args)
        # change key (first part of key) to all_releases?
        self.release_stack["releases"] = self._fetch_data(url)
        return self.release_stack["releases"]

    def get_release_dates_all_releases(
            self,
            realtime_start: str = None, 
            realtime_end: str = None,
            limit: int = None,
            offset: int = None,
            order_by: str = None,
            sort_order: str = None,
            include_release_dates_with_no_data: bool = None,
            ) -> dict:
        """
        Get release dates for all releases of economic data.

        Parameters
        ----------
        realtime_start: str, default "1776-07-04" (earliest)
            YYY-MM-DD as per fred
        realtime_end: str, default "9999-12-31" (last available) 
            YYY-MM-DD as per fred
        limit: int default None
        offset: int default None
        order_by: str default None
        sort_order: str default None
        include_release_dates_with_no_data: bool, default None

        Returns 
        -------
        dict

        Notes
        -----
        fred/releases
        """
        url_prefix = "releases/dates?"
        optional_args = {
                "&realtime_start=": realtime_start,
                "&realtime_end=": realtime_end,
                "&limit=": limit,
                "&offset=": offset,
                "&order_by=": order_by,
                "&sort_order=": sort_order,
                "&include_release_dates_with_no_data":
                include_release_dates_with_no_data,
            }
        url = self._add_optional_params(url_prefix, optional_args)
        self.release_stack["dates_all_releases"] = self._fetch_data(url)
        return self.release_stack["dates_all_releases"]

    def get_a_release(
            self,
            release_id: int,
            realtime_start: str = None, 
            realtime_end: str = None,
            ):
        """
        Get a release of economic data
        
        Parameters
        ----------
        release_id: int
            id for a release
        realtime_start: str, default "1776-07-04" (earliest)
            YYY-MM-DD as per fred
        realtime_end: str, default "9999-12-31" (last available) 
            YYY-MM-DD as per fred

        Returns 
        -------

        Notes
        -----
        fred/release
        """
        url_prefix = "release?release_id="
        try:
            url_prefix += str(release_id)
        except TypeError:
            print("Unable to cast release_id %s to str" % release_id)
        realtime_period = self._get_realtime_date(
                realtime_start, 
                realtime_end
                )
        url_prefix += realtime_period
#        breakpoint()
        self.release_stack[release_id] = self._fetch_data(url_prefix)
        return self.release_stack[release_id]

    def get_release_dates(
            self,
            release_id: int,
            realtime_start: str = None,
            realtime_end: str = None,
            limit: int = None,
            offset: int = None,
            sort_order: str = None,
            include_release_dates_with_no_data: bool = None,
            ) -> dict:
        """
        Get release dates for a release of economic data.

        Parameters
        ----------
        release_id: int
            id for a release
        realtime_start: str, default "1776-07-04" (earliest)
            YYY-MM-DD as per fred
        realtime_end: str, default "9999-12-31" (last available) 
            YYY-MM-DD as per fred
        include_release_dates_with_no_data: bool default False
            if None, FRED excudes release dates that don't have data, 
            notably future dates that are already in FRED's calendar

        Returns 
        -------

        Notes
        -----
        fred/release/dates
        """
        url_prefix = "release/dates?release_id="
        try:
            url_prefix += str(release_id)
        except TypeError:
            print("Unable to cast release_id %s to str" % release_id)
        optional_args = {
                "&realtime_start=": realtime_start,
                "&realtime_end=": realtime_end,
                "&limit=": limit,
                "&offset=": offset,
                "&sort_order=": sort_order,
                "&include_release_dates_with_no_data=": 
                include_release_dates_with_no_data,
            }
        url = self._add_optional_params(url_prefix, optional_args)
        self.release_stack[release_id] = self._fetch_data(url)
        return self.release_stack[release_id]

    def get_series_on_a_release(
            self,
            release_id: int,
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
        Get release dates for a release of economic data.

        Parameters
        ----------
        release_id: int
            id for a release
        realtime_start: str, default "1776-07-04" (earliest)
            YYY-MM-DD as per fred
        realtime_end: str, default "9999-12-31" (last available) 
            YYY-MM-DD as per fred
        limit: int, default None (FRED will use limit = 1_000)
            maximum number of results to return
            range [1, 1_000]
        offset: non-negative integer, default None (offset of 0)
        order_by: str, default "series_count"
            order results by values of the specified attribute
            can be one of "series_count", "popularity", "created", "name", "group_id"
        sort_order: str, default None (FRED will use "asc")
            sort results in ascending or descending order for attribute values specified by order_by
        filter_variable: str = None,
        filter_value:str = None,
        tag_names: list
            list of tags (str); each tag must be present in the tag of returned series
            example: ['defense', 'investment']
        exclude_tag_names: list, default None (don't exclude any tags)

        Returns 
        -------
        dict

        Examples
        -----

        Notes
        -----
        fred/release/series
        """
        url_prefix_params = dict(
                a_url_prefix = "release/series?release_id=",
                an_int_id = release_id)
        url_prefix = self._append_id_to_url(**url_prefix_params)
        optional_args = {
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
        self.release_stack[release_id] = self._fetch_data(url)
        return self.release_stack[release_id]

    def get_sources_for_a_release(
            self,
            release_id: int,
            realtime_start: str = None,
            realtime_end: str = None,
            ) -> dict:
        """
        Get the sources for a release of economic data.

        Parameters
        ----------
        release_id: int
            id for a release
        realtime_start: str, default "1776-07-04" (earliest)
            YYY-MM-DD as per fred
        realtime_end: str, default "9999-12-31" (last available) 
            YYY-MM-DD as per fred

        Returns 
        -------
        dict

        Examples
        -----

        Notes
        -----
        fred/release/sources
        """
        url_prefix_params = dict(
                a_url_prefix = "release/sources?release_id=",
                an_int_id = release_id)
        url_prefix = self._append_id_to_url(**url_prefix_params)
        optional_args = {
                "&realtime_start=": realtime_start,
                "&realtime_end=": realtime_end,
                }
        url = self._add_optional_params(url_prefix, optional_args)
        self.release_stack[release_id] = self._fetch_data(url)
        return self.release_stack[release_id]

    def get_tags_for_a_release(
            self,
            release_id: int,
            realtime_start: str = None,
            realtime_end: str = None,
            tag_names: list = None,
            tag_group_id: str = None,
            search_text: str = None,
            limit: int = None,
            offset: int = None,
            order_by: str = None,
            sort_order: str = None,
            ) -> dict:
        """
        Get the FRED tags for a release

        Parameters
        ----------
        release_id: int
            id for a release
        realtime_start: str, default "1776-07-04" (earliest)
            YYY-MM-DD as per fred
        realtime_end: str, default "9999-12-31" (last available) 
            YYY-MM-DD as per fred
        tag_names: list
            list of tags (str); each tag must be present in the tag of returned series
            example: ['defense', 'investment']
        tag_group_id: str, default None
            a tag group id to filter tags by type with
            can be one of 'freq' for frequency, 'gen' for general or concept, 
            'geo' for geography, 'geot' for geography type, 'rls' for release, 
            'seas' for seasonal adjustment, 'src' for source
        search_text: str, default None
            the words to find matching tags with
            if None, no filtering by search words
        limit: int, default None (FRED will use limit = 1_000)
            maximum number of results to return
            range [1, 1_000]
        offset: non-negative integer, default None (offset of 0)
        order_by: str, default "series_count"
            order results by values of the specified attribute
            can be one of "series_count", "popularity", "created", "name", "group_id"
        sort_order: str, default None (FRED will use "asc")
            sort results in ascending or descending order for attribute values specified by order_by

        Returns 
        -------
        dict

        Examples
        -----

        Notes
        -----
        fred/release/tags
        """
        url_prefix = "release/tags?release_id="
        try:
            url_prefix += str(release_id)
        except TypeError:
            print("Unable to cast release_id %s to str" % release_id)
        # method to try to join string by join_string for "&tag_names="
        optional_args = {
                "&realtime_start=": realtime_start,
                "&realtime_end=": realtime_end,
                "&tag_group_id=": tag_group_id,
                "&search_text=": search_text,
                "&limit=": limit,
                "&offset=": offset,
                "&order_by=": order_by,
                "&sort_order=": sort_order,
                }
        url = self._add_optional_params(url_prefix, optional_args)
        self.release_stack[release_id] = self._fetch_data(url)
        return self.release_stack[release_id]

    def get_related_tags_for_release(
            self,
            release_id: int,
            tag_names: list,
            realtime_start: str = None,
            realtime_end: str = None,
            exclude_tag_names: list = None,
            tag_group_id: str = None,
            search_text: str = None,
            limit: int = None,
            offset: int = None,
            order_by: str = None,
            sort_order: str = None,
            ) -> dict:
        """
        Get the related FRED tags for one or more FRED tags within a release.

        Parameters
        ----------
        release_id: int
            id for a release
        tag_names: list
            list of tags (str); each tag must be present in the tag of returned series
            example: ['defense', 'investment']
        realtime_start: str, default "1776-07-04" (earliest)
            YYY-MM-DD as per fred
        realtime_end: str, default "9999-12-31" (last available) 
            YYY-MM-DD as per fred
        exclude_tag_names: list, default None (don't exclude any tags)
            tags that returned series must not have
        tag_group_id: str, default None
            a tag group id to filter tags by type with
            can be one of 'freq' for frequency, 'gen' for general or concept, 
            'geo' for geography, 'geot' for geography type, 'rls' for release, 
            'seas' for seasonal adjustment, 'src' for source
        search_text: str, default None
            the words to find matching tags with
            if None, no filtering by search words
        limit: int, default None (FRED will use limit = 1_000)
            maximum number of results to return
            range [1, 1_000]
        offset: non-negative integer, default None (offset of 0)
        order_by: str, default "series_count"
            order results by values of the specified attribute
            can be one of "series_count", "popularity", "created", "name", "group_id"
        sort_order: str, default None (FRED will use "asc")
            sort results in ascending or descending order for attribute values specified by order_by

        Returns 
        -------
        dict

        Examples
        -----

        Notes
        -----
        fred/release/related_tags
        """
        url_prefix = "release/related_tags?release_id="
        try:
            url_prefix += str(release_id)
        except TypeError:
            print("Unable to cast release_id %s to str" % release_id)
        url_prefix += "&tag_names="
        try:
            url_prefix += ";".join(tag_names)
        except TypeError:
            print("tag_names must be list or tuple")
        optional_args = {
                "&realtime_start=": realtime_start,
                "&realtime_end=": realtime_end,
                "&exclude_tag_names=": exclude_tag_names,
                "&tag_group_id=": tag_group_id,
                "&search_text=": search_text,
                "&limit=": limit,
                "&offset=": offset,
                "&order_by=": order_by,
                "&sort_order=": sort_order,
                }
        url = self._add_optional_params(url_prefix, optional_args)
        self.release_stack[release_id] = self._fetch_data(url)
        return self.release_stack[release_id]

    def get_release_tables(
            self,
            release_id: int,
            element_id: int = None,
            include_observation_values: bool = None,
            observation_date: str = None,
            ):
        """
        Get a release of economic data
        *add fred's description*
        
        Parameters
        ----------
        release_id: int
            id for a release
        realtime_start: str, default "1776-07-04" (earliest)
            YYY-MM-DD as per fred
        realtime_end: str, default "9999-12-31" (last available) 
            YYY-MM-DD as per fred
        include_observation_values: bool default False
        observation_date: str, default None
            the observation date to be included with the returned release table

        Returns 
        -------

        Notes
        -----
        fred/release/tables
        """
        url_prefix = "release?release_id="
        try:
            url_prefix += str(release_id)
        except TypeError:
            print("Unable to cast release_id %s to str" % release_id)
        url_base = [self._FredBase__url_base, url_prefix, "&api_key=",]
#        breakpoint()
        base = "".join(url_base)
        file_type = "&file_type=json"
        if element_id is not None:
            str_element_id = "&element_id=" + str(element_id)
        if self._FredBase__api_key_env_var:
            if element_id is None:
                json_data = self._get_response(base + os.environ["FRED_API_KEY"] + file_type)
            else:
                json_data = self._get_response(base + os.environ["FRED_API_KEY"] + str_element_id + file_type)
        else:
            json_data = self._get_response(base + self.__api_key + file_type)
        if json_data is None:
            message = "Data could not be retrieved using" \
                    "id : %s" % an_id
            print(message)
            return
        self.release_stack[release_id] = self._fetch_data(url_prefix)
        return self.release_stack[release_id] 
