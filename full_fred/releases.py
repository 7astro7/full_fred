
from .categories import Categories

class Releases(Categories):

    def __init__(self):
        """
        """
        super().__init__()
        self.release_stack = dict()

    # param docstrings are checked
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
        realtime_start: str, default None
            The start of the real-time period formatted as "YYY-MM-DD".
            If None, default realtime_start is used.
            If default isn't set by user, "1776-07-04" (earliest available) is used.
        realtime_end: str, default None
            The start of the real-time period formatted as "YYY-MM-DD".
            If None, default realtime_end is used.
            If default isn't set by user, "9999-12-31" (latest available) is used.
        limit: int, default None
            The maximum number of results to return.
            Values can be in range(1, 1_001).
            If None, FRED will use limit = 1_001.
        offset: int, default None
            If None, offset of 0 is used.
        order_by: str, default None
            Order results by values of the specified attribute.
            Can be one of "release_id", "name", "realtime_start", "realtime_end",
            If None, "release_id" is used.
        sort_order: str, default None
            Sort results in ascending or descending order for attribute values specified by order_by.
            Can be "asc" or "desc".
            If None, "asc" is used.

        Returns 
        -------
        dict
            ID, name, url, other metadata for all FRED releases.

        See Also
        --------

        Notes
        -----
        FRED web service endpoint: fred/releases
        https://fred.stlouisfed.org/docs/api/fred/releases.html

        Examples
        --------
        """
        self._viable_api_key()
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
        self.release_stack["get_all_releases"] = self._fetch_data(url)
        return self.release_stack["get_all_releases"]

    # param docstrings are checked
    def get_release_dates_all_releases(
            self,
            realtime_start: str = None, 
            realtime_end: str = None,
            limit: int = None,
            offset: int = None,
            order_by: str = None,
            sort_order: str = None,
            include_empty: bool = None,
            ) -> dict:
        """
        Get release dates for all releases of economic data. 
        FRED's data sources publish release dates: release 
        dates may be published before the data in the release
        is available on FRED's servers via this API.

        Parameters
        ----------
        realtime_start: str, default None
            The start of the real-time period formatted as "YYY-MM-DD".
            If None, default realtime_start is used.
            If default isn't set by user, "1776-07-04" (earliest available) is used.
        realtime_end: str, default None
            The start of the real-time period formatted as "YYY-MM-DD".
            If None, default realtime_end is used.
            If default isn't set by user, "9999-12-31" (latest available) is used.
        limit: int, default None
            The maximum number of results to return.
            Values can be in range(1, 1_001).
            If None, FRED will use limit = 1_001.
        offset: int, default None
            If None, offset of 0 is used.
        order_by: str, default None
            Order results by values of the specified attribute.
            Can be one of "release_date", "release_id", "release_name", 
            If None, "release_date" is used.
        sort_order: str, default None
            Sort results in ascending or descending order for attribute values specified by order_by.
            Can be "asc" or "desc".
            If None, "asc" is used.
        include_empty: bool, default None
            Indicates whether to return release dates with no data.
            If False, release dates without any data are excluded, namely future release dates.
            If None, False is used.

        Returns 
        -------
        dict
            release_id, release_name, date for all releases

        See Also
        --------

        Notes
        -----
        FRED web service endpoint: fred/releases
        https://fred.stlouisfed.org/docs/api/fred/releases_dates.html

        Examples
        --------
        """
        self._viable_api_key()
        url_prefix = "releases/dates?"
        optional_args = {
                "&realtime_start=": realtime_start,
                "&realtime_end=": realtime_end,
                "&limit=": limit,
                "&offset=": offset,
                "&order_by=": order_by,
                "&sort_order=": sort_order,
                "&include_release_dates_with_no_data":
                include_empty,
            }
        url = self._add_optional_params(url_prefix, optional_args)
        self.release_stack["get_release_dates_all_releases"] = self._fetch_data(url)
        return self.release_stack["get_release_dates_all_releases"]

    
    # param docstrings are checked
    def get_a_release(
            self,
            release_id: int,
            realtime_start: str = None, 
            realtime_end: str = None,
            ):
        """
        Get a release of economic data.
        
        Parameters
        ----------
        release_id: int
            The ID of the release.
        realtime_start: str, default None
            The start of the real-time period formatted as "YYY-MM-DD".
            If None, default realtime_start is used.
            If default isn't set by user, "1776-07-04" (earliest available) is used.
        realtime_end: str, default None
            The start of the real-time period formatted as "YYY-MM-DD".
            If None, default realtime_end is used.
            If default isn't set by user, "9999-12-31" (latest available) is used.

        Returns 
        -------
        dict
            Release name, id, realtime start and end, url to release,
            whether the release is a press_release.

        See Also
        --------

        Notes
        -----
        FRED web service endpoint: fred/release
        https://fred.stlouisfed.org/docs/api/fred/release.html

        Examples
        -----
        """
        self._viable_api_key()
        url_prefix = "release?release_id="
        try:
            url_prefix += str(release_id)
        except TypeError:
            print("Unable to cast release_id %s to str" % release_id) # line contradicts itself
        optional_args = {
                "&realtime_start=": realtime_start,
                "&realtime_end=": realtime_end,
                }
        url = self._add_optional_params(url_prefix, optional_args)
        self.release_stack["get_a_release"] = self._fetch_data(url)
        return self.release_stack["get_a_release"]

    # param docstrings are checked
    def get_release_dates(
            self,
            release_id: int,
            realtime_start: str = None,
            realtime_end: str = None,
            limit: int = None,
            offset: int = None,
            sort_order: str = None,
            include_empty: bool = None,
            ) -> dict:
        """
        Get release dates for a release of economic data.
        FRED's data sources publish release dates: release 
        dates may be published before the data in the release
        is available on FRED's servers via this API.

        Parameters
        ----------
        release_id: int
            The ID of the release.
        realtime_start: str, default None
            The start of the real-time period formatted as "YYY-MM-DD".
            If None, default realtime_start is used.
            If default isn't set by user, "1776-07-04" (earliest available) is used.
        realtime_end: str, default None
            The start of the real-time period formatted as "YYY-MM-DD".
            If None, default realtime_end is used.
            If default isn't set by user, "9999-12-31" (latest available) is used.
        limit: int, default None
            The maximum number of results to return.
            Values can be in range(1, 10_001).
            If None, FRED will use limit = 10_001.
        offset: int, default None
            If None, offset of 0 is used.
        sort_order: str, default None
            Sort results in ascending or descending order for attribute values specified by order_by.
            Can be "asc" or "desc".
            If None, "asc" is used.
        include_empty: bool, default None
            Indicates whether to return release dates with no data.
            If False, release dates without any data are excluded, namely future release dates.
            If None, False is used.

        Returns 
        -------
        dict
            The release dates for each release of release_id.

        See Also
        --------
        get_release_dates_all_releases

        Notes
        -----
        FRED web service endpoint: fred/release/dates
        https://fred.stlouisfed.org/docs/api/fred/release_dates.html

        Examples
        -----
        """
        self._viable_api_key()
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
                "&include_release_dates_with_no_data=": include_empty,
            }
        url = self._add_optional_params(url_prefix, optional_args)
        self.release_stack["get_release_dates"] = self._fetch_data(url)
        return self.release_stack["get_release_dates"]

    # param docstrings are checked
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
        Get series on a release of economic data.

        Parameters
        ----------
        release_id: int
            The ID of the release.
        realtime_start: str, default None
            The start of the real-time period formatted as "YYY-MM-DD".
            If None, default realtime_start is used.
            If default isn't set by user, "1776-07-04" (earliest available) is used.
        realtime_end: str, default None
            The start of the real-time period formatted as "YYY-MM-DD".
            If None, default realtime_end is used.
            If default isn't set by user, "9999-12-31" (latest available) is used.
        limit: int, default None
            The maximum number of results to return.
            Values can be in range(1, 1_001).
            If None, FRED will use limit = 1_001.
        offset: int, default None
            If None, offset of 0 is used.
        order_by: str, default None
            Order results by values of the specified attribute.
            Can be one of "series_id", "title", "units", "frequency",
            "seasonal_adjustment", "realtime_start", "realtime_end",
            "last_updated", "observation_start", "observation_end",
            "popularity", "group_popularity".
            If None, "series_id" is used.
        sort_order: str, default None
            Sort results in ascending or descending order for attribute values specified by order_by.
            Can be "asc" or "desc".
            If None, "asc" is used.
        filter_variable: str, default None
            The attribute to filter results by.
            Can be one of "frequency", "units", "seasonal_adjustment".
            If None, no filter is used.
        filter_value: str, default None
            The value of filter_variable to filter results by.
            If None, no filter is used.
        tag_names: list, default None
            list of tags [str] to include in returned data, excluding any tag not in tag_names;
            If None, no filtering by tag names is done.
        exclude_tag_names: list, default None
            list of tag names that series match none of.
            If None, no filtering by excluding tag names is done.

        Returns 
        -------
        dict
            ID, title, units, and other metadata for each series included in 
            the release.

        See Also
        --------

        Notes
        -----
        FRED web service endpoint: fred/release/series
        https://fred.stlouisfed.org/docs/api/fred/release_series.html

        Examples
        -----
        """
        self._viable_api_key()
        url_prefix_params = dict(
                a_url_prefix = "release/series?release_id=",
                an_int_id = release_id,
                )
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
        self.release_stack["get_series_on_a_release"] = self._fetch_data(url)
        return self.release_stack["get_series_on_a_release"]

    # param docstrings are checked
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
            The ID of the release.
        realtime_start: str, default None
            The start of the real-time period formatted as "YYY-MM-DD".
            If None, default realtime_start is used.
            If default isn't set by user, "1776-07-04" (earliest available) is used.
        realtime_end: str, default None
            The start of the real-time period formatted as "YYY-MM-DD".
            If None, default realtime_end is used.
            If default isn't set by user, "9999-12-31" (latest available) is used.

        Returns 
        -------
        dict
            source_id, name, url, and other metadata about sources of
            data found in the release.

        See Also
        --------

        Notes
        -----
        FRED web service endpoint: fred/release/sources
        https://fred.stlouisfed.org/docs/api/fred/releases_dates.html

        Examples
        -----
        """
        self._viable_api_key()
        url_prefix_params = dict(
                a_url_prefix = "release/sources?release_id=",
                an_int_id = release_id)
        url_prefix = self._append_id_to_url(**url_prefix_params)
        optional_args = {
                "&realtime_start=": realtime_start,
                "&realtime_end=": realtime_end,
                }
        url = self._add_optional_params(url_prefix, optional_args)
        self.release_stack["get_sources_for_a_release"] = self._fetch_data(url)
        return self.release_stack["get_sources_for_a_release"]

    # param docstrings are checked
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
        Get the FRED tags for a release.

        Parameters
        ----------
        release_id: int
            The ID of the release.
        realtime_start: str, default None
            The start of the real-time period formatted as "YYY-MM-DD".
            If None, default realtime_start is used.
            If default isn't set by user, "1776-07-04" (earliest available) is used.
        realtime_end: str, default None
            The start of the real-time period formatted as "YYY-MM-DD".
            If None, default realtime_end is used.
            If default isn't set by user, "9999-12-31" (latest available) is used.
        tag_names: list, default None
            list of tags [str] to include in returned data, excluding any tag not in tag_names;
            If None, no filtering by tag names is done.
        tag_group_id: str, default None
            a tag group id to filter tags by type with
            can be one of 'freq' for frequency, 'gen' for general or concept, 
            'geo' for geography, 'geot' for geography type, 'rls' for release, 
            'seas' for seasonal adjustment, 'src' for source
        search_text: str, default None
            the words to find matching tags with
            if None, no filtering by search words
        limit: int, default None
            The maximum number of results to return.
            Values can be in range(1, 1_001).
            If None, FRED will use limit = 1_001.
        offset: int, default None
            If None, offset of 0 is used.
        order_by: str, default None
            Order results by values of the specified attribute.
            Can be one of "series_count", "popularity", "created", 
            "name", "group_id".
            If None, "series_count" is used.
        sort_order: str, default None
            Sort results in ascending or descending order for attribute values specified by order_by.
            Can be "asc" or "desc".
            If None, "asc" is used.

        Returns 
        -------
        dict
            name, group ID, notes, and other metadata for each tag.

        See Also
        --------
        get_related_tags_for_release

        Notes
        -----
        FRED web service endpoint: fred/release/tags
        https://fred.stlouisfed.org/docs/api/fred/release_tags.html

        Examples
        -----
        """
        self._viable_api_key()
        url_prefix_params = {
                "a_url_prefix": "release/tags?release_id=",
                "an_int_id": release_id,
                }
        url_prefix = self._append_id_to_url(**url_prefix_params)
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
        self.release_stack["get_tags_for_a_release"] = self._fetch_data(url)
        return self.release_stack["get_tags_for_a_release"]

    # param docstrings are checked
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
            The ID of the release.
        tag_names: list, default None
            list of tags [str] to include in returned data, excluding any tag not in tag_names;
        realtime_start: str, default None
            The start of the real-time period formatted as "YYY-MM-DD".
            If None, default realtime_start is used.
            If default isn't set by user, "1776-07-04" (earliest available) is used.
        realtime_end: str, default None
            The start of the real-time period formatted as "YYY-MM-DD".
            If None, default realtime_end is used.
            If default isn't set by user, "9999-12-31" (latest available) is used.
        exclude_tag_names: list, default None
            list of tag names that series match none of.
            If None, no filtering by excluding tag names is done.
        tag_group_id: str, default None
            A tag group id to filter tags by type with
            can be one of 'freq' for frequency, 'gen' for general or concept, 
            'geo' for geography, 'geot' for geography type, 'rls' for release, 
            'seas' for seasonal adjustment, 'src' for source
        search_text: str, default None
            The words to find matching tags with
            If None, no filtering by search words
        limit: int, default None
            The maximum number of results to return.
            Values can be in range(1, 1_001).
            If None, FRED will use limit = 1_001.
        offset: int, default None
            If None, offset of 0 is used.
        order_by: str, default None
            Order results by values of the specified attribute.
            Can be one of "series_count", "popularity", "created", 
            "name", "group_id".
            If None, "series_count" is used.
        sort_order: str, default None
            Sort results in ascending or descending order for attribute values specified by order_by.
            Can be "asc" or "desc".
            If None, "asc" is used.

        Returns 
        -------
        dict
            name, group ID, notes, series count, and other metadata for each related tag.
            

        See Also
        --------
        get_tags_for_release

        Notes
        -----
        FRED web service endpoint: fred/release/related_tags
        https://fred.stlouisfed.org/docs/api/fred/release_related_tags.html

        Examples
        -----
        """
        url_prefix_params = {
                "a_url_prefix": "release/related_tags?release_id=",
                "an_int_id": release_id,
                }
        url_prefix = self._append_id_to_url(**url_prefix_params)
        optional_args_plus_tag_names = {
                "&tag_names=": tag_names,
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
        url = self._add_optional_params(url_prefix, optional_args_plus_tag_names)
        self.release_stack["get_related_tags_for_release"] = self._fetch_data(url)
        return self.release_stack["get_related_tags_for_release"]

    # param docstrings are checked
    # add further notes that FRED clarifies with
    def get_release_tables(
            self,
            release_id: int,
            element_id: int = None,
            include_observation_values: bool = None,
            observation_date: str = None,
            ) -> dict:
        """
        Get release tables for a given release.
        
        Parameters
        ----------
        release_id: int
            The ID of the release.
        element_id: int, default None
            The release table element id to retrieve
            If None, root (most general) element_id for the release is used.
        realtime_start: str, default None
            The start of the real-time period formatted as "YYY-MM-DD".
            If None, default realtime_start is used.
            If default isn't set by user, "1776-07-04" (earliest available) is used.
        realtime_end: str, default None
            The start of the real-time period formatted as "YYY-MM-DD".
            If None, default realtime_end is used.
            If default isn't set by user, "9999-12-31" (latest available) is used.
        include_observation_values: bool, default None
            Indicates that observations need to be returned.
            Observation value and date are only returned for a series
            element type.
            If None, observations are not returned.
        observation_date: str, default None
            The observation date to be included with the returned release table.
            String formatted as 'YYY-MM-DD' 
            If None, '9999-12-31' is used.

        Returns 
        -------

        See Also
        --------

        Notes
        -----
        FRED web service endpoint: fred/release/tables
        https://fred.stlouisfed.org/docs/api/fred/release_tables.html

        Examples
        --------
        """
        self._viable_api_key()
        url_prefix_params = {
                "a_url_prefix": "release/tables?release_id=",
                "an_int_id": release_id,
                }
        url_prefix = self._append_id_to_url(**url_prefix_params)
        optional_args_plus_tag_names = {
                "&element_id=": element_id,
                "&include_observation_values=": include_observation_values,
                "&observation_date=": observation_date,
                }
        url = self._add_optional_params(url_prefix, optional_args_plus_tag_names)
        self.release_stack["get_release_tables"] = self._fetch_data(url)
        return self.release_stack["get_release_tables"]

