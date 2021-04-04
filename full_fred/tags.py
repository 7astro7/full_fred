
from .sources import Sources

class Tags(Sources):

    def __init__(self):
        """
        FRED tag = an attribute assigned to a series. 
        Metadata for a tag includes name, group_id, notes, date of creation, popularity, series count. 
        FRED web service endpoint: fred/tags
        https://fred.stlouisfed.org/docs/api/fred/
        """
        super().__init__()
        self.tag_stack = dict()

    # sort order checked
    def get_all_tags(
            self,
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
        Get all FRED tags, search for FRED tags, get metadata for FRED tags.

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
        tag_names: list, default None
            list of tags [str] to include in returned data, excluding any tag not in tag_names;
            each tag must be present in the tag of returned series.
            If None, no filtering by tag names is done.
        tag_group_id: str, default None
            a tag group id to filter tags by type with.
            Can be one of 'freq' for frequency, 'gen' for general or concept, 
            'geo' for geography, 'geot' for geography type, 'rls' for release, 
            'seas' for seasonal adjustment, 'src' for source, 'cc' for copyright.
            If None, no filtering by tag group is done.
        search_text: str, default None
            The words to find matching tags with.
            If None, no filtering by search words.
        limit: int, default None 
            The maximum number of results to return.
            Values can be in range(1, 1_001).
            If None, FRED will use limit = 1_000.
        offset: int, default None 
            If None, offset of 0 is used.
        order_by: str, default None
            Order results by values of the specified attribute.
            Can be one of "series_count", "popularity", "created", "name", "group_id".
            If None, "series_count" is used.
        sort_order: str, default None 
            Sort results in ascending or descending order for attribute values specified by order_by.
            Can be "asc" or "desc".
            If None, "asc" is used.

        Returns
        -------
        dict
            Metadata of requested FRED tags

        See Also
        --------
        get_related_tags_for_a_tag: get related tags

        Notes
        -----
        FRED web service endpoint: fred/tags
        https://fred.stlouisfed.org/docs/api/fred/tags.html

        Examples
        --------
        """
        url_prefix = "tags?"
        optional_args = {
                "&realtime_start=": realtime_start,
                "&realtime_end=": realtime_end,
                "&tag_names=": tag_names,
                "&tag_group_id=": tag_group_id,
                "&search_text=": search_text,
                "&limit=": limit,
                "&offset=": offset,
                "&order_by=": order_by,
                "&sort_order=": sort_order,
            }
        url = self._add_optional_params(url_prefix, optional_args)
        self.tag_stack["get_all_tags"] = self._fetch_data(url) 
        return self.tag_stack["get_all_tags"] 

    # sort order checked
    def get_related_tags_for_a_tag(
            self,
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
            ):
        """
        Get related FRED tags for one or more FRED tags.

        Parameters
        ----------
        tag_names: list
            list of tags that series match all of. 
            Each tag must be present in the tag of returned series.
        realtime_start: str, default None
            the start of the real-time period formatted as "YYY-MM-DD".
            If None, default realtime_start is used.
            If default isn't set by user, "1776-07-04" (earliest available) is used.
        realtime_end: str, default None
            the end of the real-time period formatted as "YYY-MM-DD".
            If None, default realtime_end is used.
            If default isn't set by user, "9999-12-31" (latest available) is used.
        exclude_tag_names: list, default None 
            A list of tag names that series match none of.
            If None, no tag names are excluded.
        tag_group_id: str, default None
            A tag group id to filter tags by type with.
            Can be one of 'freq' for frequency, 'gen' for general or concept, 
            'geo' for geography, 'geot' for geography type, 'rls' for release, 
            'seas' for seasonal adjustment, 'src' for source.
            If None, no filtering by tag group is done.
        search_text: str, default None
            The words to find matching tags with.
            If None, no filtering by search words is done.
        limit: int, default None 
            The maximum number of results to return.
            Values can be in range(1, 1_001).
            If None, FRED will use limit = 1_000.
        offset: int, default None 
            If None, offset of 0 is used.
        order_by: str, default None
            Order results by values of the specified attribute.
            Can be one of "series_count", "popularity", "created", "name", "group_id".
            If None, "series_count" is used.
        sort_order: str, default None 
            Sort results in ascending or descending order for attribute values specified by order_by.
            Can be "asc" or "desc".
            If None, "asc" is used.

        Returns
        -------
        dict

        See Also
        --------
        get_all_tags: get all tags in use

        Notes
        -----
        FRED web service endpoint: fred/related_tags
        https://fred.stlouisfed.org/docs/api/fred/related_tags.html

        Examples
        --------
        f = Fred()
        f.get_related_tags_for_a_tag(exclude_tag_names = ("discontinued",))
        """
        url_prefix = "related_tags?tag_names="
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
        self.tag_stack["get_related_tags_for_a_tag"] = self._fetch_data(url)
        return self.tag_stack["get_related_tags_for_a_tag"]

    # sort order checked
    def get_series_matching_tags(
            self, 
            tag_names: list,
            exclude_tag_names: list = None,
            realtime_start: str = None,
            realtime_end: str = None,
            limit: int = None,
            offset: int = None,
            order_by: str = None,
            sort_order: str = None,
            ) -> dict:
        """
        Get the series matching all tags in tag_names parameter and 
        no tags in the exclude_tag_names parameter.
            
        Parameters
        ----------
        tag_names: list
            list of tags that series match all of. 
            Each tag must be present in the tag of returned series.
        exclude_tag_names: list, default None 
            A list of tag names that series match none of.
            If None, no tag names are excluded.
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
            If None, FRED will use limit = 1_000.
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

        Returns
        -------
        dict
            Metadata of series with requested tags.

        See Also
        --------

        Notes
        -----
        FRED web service endpoint: fred/tags/series
        https://fred.stlouisfed.org/docs/api/fred/tags_series.html

        Examples
        --------
        """
        url_prefix = "tags/series?tag_names=" 
        try:
            url_prefix += ";".join(tag_names)
        except TypeError:
            print("tag_names must be list or tuple")
        optional_args = {
                "&exclude_tag_names=": exclude_tag_names,
                "&realtime_start=": realtime_start,
                "&realtime_end=": realtime_end,
                "&limit=": limit,
                "&offset=": offset,
                "&order_by=": order_by,
                "&sort_order=": sort_order,
            }
        url = self._add_optional_params(url_prefix, optional_args)
        self.tag_stack["get_series_matching_tags"] = self._fetch_data(url)
        return self.tag_stack["get_series_matching_tags"]


