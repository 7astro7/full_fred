
from .sources import Sources

class Tags(Sources):

    def __init__(self):
        """
        FRED tag = an attribute assigned to a series. 
        Metadata for a tag includes name, group_id, notes, date of creation, popularity, series count. 
        define further
        FRED web service endpoint: fred/tags
        https://fred.stlouisfed.org/docs/api/fred/
        """
        super().__init__()
        self.tag_stack = dict()

    def get_tags(
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
        Get FRED tags. All parameters are optional.

        Parameters
        ----------
        realtime_start: str, default None
            the start of the real-time period formatted as "YYY-MM-DD".
            If None, "1776-07-04" (earliest) is used.
        realtime_end: str, default None
            the start of the real-time period formatted as "YYY-MM-DD".
            If None, "9999-12-31" (last available) is used.
        tag_names: list, default None
            list of tags (of string type) to exclude from response.
            If None,
        tag_group_id: str, default None
            a tag group id to filter tags by type with
            can be one of 'freq' for frequency, 'gen' for general or concept, 
            'geo' for geography, 'geot' for geography type, 'rls' for release, 
            'seas' for seasonal adjustment, 'src' for source
            If None,
        search_text: str, default None
            the words to find matching tags with
            if None, no filtering by search words
        limit: int, default None (FRED will use limit = 1_000)
            maximum number of results to return
            range [1, 1_000]
            If None,
        offset: non-negative integer, default None (offset of 0)
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
            Metadata of requested FRED tags

        See Also
        --------
        get_related_tags_for_a_tag: get related tags

        Notes
        -----
        FRED web service endpoint:fred/tags

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
        self.tag_stack["tags"] = self._fetch_data(url) # make key better
        return self.tag_stack["tags"] 

    # clarify intersection of tags and union of tags*********
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
        Get related FRED tags for one or more FRED tags

        Parameters
        ----------
        tag_names: list
            list of tags (str); each tag must be present in the tag of returned series

        realtime_start: str default None

        realtime_end: str default None

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

        See Also
        --------
        get_tags: get all tags in use

        Notes
        -----
        FRED web service endpoint: fred/related_tags

        Examples
        --------
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
        key = "_".join(tag_names)
        self.tag_stack[key] = self._fetch_data(url)
        return self.tag_stack[key]

    def get_series_matching_tags(
            self, 
            tag_names: list,
            exclude_tag_names: list = None,
            realtime_start: str = None,
            realtime_end: str = None,
            limit: int = 100_000,
            offset: int = 0,
            order_by: str = "series_id",
            sort_order: str = "asc",
            ) -> dict:
        """
        Get the metadata of series conditional on the series having ALL tags in tag_names 
        and exclude any tags in exclude_tag_names
        intersection of tag names, not union
        tag_names[0] AND tag_names[1] AND ... tag_names[n - 1] must be in returned series' tags
        double-check filtering mechanism (name or tag of series?)
        all fred params:
            
        Parameters
        ----------
        tag_names: list
            list of tags (str); each tag must be present in the tag of returned series

        exclude_tag_names: list, default None
            example: ['alcohol', 'quarterly',] to exclude series with either tag 'alcohol' or tag 'quarterly'

        realtime_start: str default None

        realtime_end: str default None

        limit: int, default 1_000
            maximum number of observations / rows 
            range [1, 1_000]

        Returns
        -------
        dict

        Notes
        -----
        FRED web service endpoint: fred/tags/series
        """
        # perhaps check first to see if there's a matching query in self.tag_stack
        url_prefix = "tags/series?tag_names=" 
        try:
            url_prefix += ";".join(tag_names)
        except TypeError:
            print("tag_names must be list or tuple")
        # make each returned series a FredSeries
        realtime_period = self._get_realtime_date(
                realtime_start, 
                realtime_end
                )
        url_prefix += realtime_period
#        breakpoint()
        key = "_".join(tag_names)
        self.tag_stack[key] = self._fetch_data(url_prefix)
        return self.tag_stack[key]
