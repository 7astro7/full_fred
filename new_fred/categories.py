
from .fred_base import FredBase

class Categories(FredBase):
    
    def __init__(self):
        """
        """
        super().__init__()
        self.category_stack = dict() 

    # param docstrings are checked
    def get_a_category(
            self, 
            category_id: int = None,
            ) -> dict:
        """
        Get a category of FRED data.

        Parameters
        ----------
        category_id: int, default None
            The ID of the category.
            If None, root category_id of 0 is used.

        Returns
        -------
        dict
            Metadata of category: id, name, parent_id

        See Also
        --------

        Notes
        -----
        fred/category
        https://fred.stlouisfed.org/docs/api/fred/category.html

        Examples
        --------
        """
        url_prefix = "category?category_id=" 
        try:
            url = url_prefix + str(category_id)
        except TypeError:
            print("Cannot cast category_id %s to str" % category_id)
        self.category_stack["get_a_category"] = self._fetch_data(url)
        return self.category_stack["get_a_category"] 

    # param docstrings are checked
    def get_child_categories(
            self, 
            category_id: int,
            realtime_start: str = None,
            realtime_end: str = None,
            ) -> dict:
        """
        Get child categories of a category.

        Parameters
        ----------
        category_id: int, default None
            The ID of the category.
            If None, root category_id of 0 is used.
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
            id, name, parent_id for each child category.

        See Also
        --------

        Notes
        -----
        fred/category/children
        https://fred.stlouisfed.org/docs/api/fred/category_children.html
        """
        url_prefix = "category/children?category_id=" 
        try:
            url_prefix += str(category_id)
        except TypeError:
            print("Cannot cast category_id %s to str" % category_id)
        optional_args = {
                "&realtime_start=": realtime_start,
                "&realtime_end=": realtime_end,
                }
        url = self._add_optional_params(url_prefix, optional_args)
        self.category_stack["get_child_categories"] = self._fetch_data(url)
        return self.category_stack["get_child_categories"] 

    # param docstrings are checked
    def get_related_categories(
            self, 
            category_id: int,
            realtime_start: str = None, 
            realtime_end: str = None,
            ):
        """
        Get the related categories for a category. FRED web service 
        defines a related category as a one-way relation between 2 
        categories where neither of the 2 is the parent category of
        the other. According to FRED web service most categories
        don't have related categories.

        Parameters
        ----------
        category_id: int
            The ID of the category.
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
            id, name, parent_id of related categories.

        See Also
        --------

        Notes
        -----
        fred/category/related
        https://fred.stlouisfed.org/docs/api/fred/category_related.html

        Examples
        --------
        """
        url_prefix = "category/related?category_id="
        try:
            url_prefix += str(category_id)
        except TypeError:
            print("Cannot cast category_id %s to str" % category_id) # doesn't this line contradict itself?
        optional_args = {
                "&realtime_start=": realtime_start,
                "&realtime_end=": realtime_end,
            }
        url = self._add_optional_params(url_prefix, optional_args)
        self.category_stack["get_related_categories"] = self._fetch_data(url)
        return self.category_stack["get_related_categories"] 

    # param docstrings are checked
    def get_series_in_a_category(
            self, 
            category_id: int,
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
            ): 
        """
        Get the series that belong to a category (metadata, not dataframes for each series). 

        Parameters
        ----------
        category_id: int
            The ID of the category.
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
            If None, offset of 0 is used.
        order_by: str, default None
            Order results by values of the specified attribute.
            Can be one of "series_id", "title", "units", "frequency", 
            "seasonal_adjustment", "reatime_start", "realtime_end",
            "last_updated", "observation_start", "observation_end",
            "popularity", "group_popularity"
            If None, "series_id" is used.
        sort_order: str, default None 
            Sort results in ascending or descending order for attribute values specified by order_by.
            Can be "asc" or "desc".
            If None, "asc" is used.
        filter_variable: str, default None
            The attribute to filter results by.
            Can be one of "frequency", "units", "seasonal_adjustment".
            If None, no filter variable is used.
        filter_value: str, default None
            The value of filter_variable to filter results by.
        tag_names: list, default None
            list of tags [str] to include in returned data, excluding any tag not in tag_names;
            each tag must be present in the tag of returned series.
            If None, no filtering by tag names is done.
        exclude_tag_names: list, default None
            list of tag names that series match none of.
            If None, no filtering by tag names is done.

        Returns 
        -------
        dict
            Metadata of series that belong to category. 

        See Also
        --------

        Notes
        -----
        fred/category/series
        https://fred.stlouisfed.org/docs/api/fred/category_series.html

        Examples
        --------
        """
        url_prefix = "category/series?category_id="
        try:
            url_prefix += str(category_id)
        except TypeError:
            print("Cannot cast category_id %s to str" % category_id) # doesn't this line contradict itself?
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
        self.category_stack["get_series_in_a_category"] = self._fetch_data(url)
        return self.category_stack["get_series_in_a_category"]

    # param docstrings are checked
    # rename to get_tags_in_a_category?
    def get_tags_for_a_category(
            self, 
            category_id: int,
            realtime_start: str = None,
            realtime_end: str = None,
            tag_names: list = None,
            tag_group_id: str = None,
            search_text: str = None,
            limit: int = None,
            offset: int = None,
            order_by: str = None,
            sort_order: str = None,
            ):
        """
        Get the FRED tags for a category.

        Parameters
        ----------
        category_id: int
            The ID of the category.
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
            A tag group id to filter tags by type with.
            Can be one of 'freq' for frequency, 'gen' for general or concept,
            'geo' for geography, 'geot' for geography type, 'rls' for release,
            'seas' for seasonal adjustment, 'src' for source.
            If None, no filtering by tag group is done.
        search_text: str, default None
            The words to find matching tags with.
            If None, no filtering by search words.
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
            Metadata of all FRED tags found in a category.

        See Also
        --------

        Notes
        -----
        fred/category/tags
        https://fred.stlouisfed.org/docs/api/fred/category_tags.html

        Examples
        --------
        """
        url_prefix = "category/tags?category_id="
        try:
            url_prefix += str(category_id)
        except TypeError:
            print("Cannot cast category_id %s to str" % category_id) # doesn't this line contradict itself?
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
        self.category_stack["get_tags_for_a_category"] = self._fetch_data(url)
        return self.category_stack["get_tags_for_a_category"]

    # param docstrings are checked
    def get_related_tags_for_a_category(
            self, 
            category_id: int,
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
        Get the related FRED tags for one or more FRED tags within a category.

        Parameters
        ----------
        category_id: int
            The ID of the category.
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
        exclude_tag_names: list, default None
            list of tag names that series match none of.
            If None, no filtering by tag names is done.
        tag_group_id: str, default None
            A tag group id to filter tags by type with.
            Can be one of 'freq' for frequency, 'gen' for general or concept,
            'geo' for geography, 'geot' for geography type, 'rls' for release,
            'seas' for seasonal adjustment, 'src' for source.
            If None, no filtering by tag group is done.
        search_text: str, default None
            The words to find matching tags with.
            If None, no filtering by search words.
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

        See Also
        --------

        Notes
        -----
        fred/category/related_tags
        https://fred.stlouisfed.org/docs/api/fred/category_related_tags.html
        """
        url_prefix = "category/related_tags?category_id="
        try:
            url_prefix += str(category_id)
        except TypeError:
            print("Cannot cast category_id %s to str" % category_id) # doesn't this line contradict itself?
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
        self.category_stack["get_related_tags_for_a_category"] = self._fetch_data(url)
        return self.category_stack["get_related_tags_for_a_category"]


