from .fred_base import FredBase


class Categories(FredBase):

    def __init__(self):
        """"""
        super().__init__()
        self.category_stack = dict()

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
            Metadata of category: ID, name, parent_id

        See Also
        --------
        fred.get_child_categories: Get specific categories within a category.
        fred.get_related_categories: Get similar categories that aren't part of a child-parent link.

        Notes
        -----
        FRED web service endpoint: fred/category
        https://fred.stlouisfed.org/docs/api/fred/category.html

        Examples
        --------
        >>> fred.get_a_category(32991)
        {'categories': [{'id': 32991,
            'name': 'Money, Banking, & Finance',
            'parent_id': 0}]}

        >>> fred.get_a_category(0)
        >>> fred.category_stack['get_a_category']
        {'categories': [{'id': 0, 'name': 'Categories', 'parent_id': 0}]}
        """
        self._viable_api_key()
        url_prefix_params = {
            "a_url_prefix": "category?category_id=",
            "an_int_id": category_id,
        }
        if url_prefix_params["an_int_id"] is None:
            url_prefix_params["an_int_id"] = 0
        url = self._append_id_to_url(**url_prefix_params)
        self.category_stack["get_a_category"] = self._fetch_data(url)
        return self.category_stack["get_a_category"]

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
            ID, name, parent_id for each child category.

        See Also
        --------
        fred.get_related_categories: Get similar categories that aren't part of a child-parent link.

        Notes
        -----
        FRED web service endpoint: fred/category/children
        https://fred.stlouisfed.org/docs/api/fred/category_children.html

        Examples
        --------
        >>> fred.get_child_categories(0)
        {'categories': [{'id': 32991,
            'name': 'Money, Banking, & Finance',
            'parent_id': 0},
            {'id': 10,
            'name': 'Population, Employment, & Labor Markets',
            'parent_id': 0},
            {'id': 32992, 'name': 'National Accounts', 'parent_id': 0},
            {'id': 1, 'name': 'Production & Business Activity', 'parent_id': 0},
            {'id': 32455, 'name': 'Prices', 'parent_id': 0},
            {'id': 32263, 'name': 'International Data', 'parent_id': 0},
            {'id': 3008, 'name': 'U.S. Regional Data', 'parent_id': 0},
            {'id': 33060, 'name': 'Academic Data', 'parent_id': 0}]}
        """
        self._viable_api_key()
        url_prefix_params = {
            "a_url_prefix": "category/children?category_id=",
            "an_int_id": category_id,
        }
        url_prefix = self._append_id_to_url(**url_prefix_params)
        optional_args = {
            "&realtime_start=": realtime_start,
            "&realtime_end=": realtime_end,
        }
        url = self._add_optional_params(url_prefix, optional_args)
        self.category_stack["get_child_categories"] = self._fetch_data(url)
        return self.category_stack["get_child_categories"]

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
            ID, name, parent_id of related categories.

        See Also
        --------
        fred.get_child_categories: Get specific categories within a category.

        Notes
        -----
        FRED web service endpoint: fred/category/related
        https://fred.stlouisfed.org/docs/api/fred/category_related.html

        Examples
        --------
        >>> fred.get_related_categories(32073)
        {'categories': [{'id': 149, 'name': 'Arkansas', 'parent_id': 27281},
            {'id': 150, 'name': 'Illinois', 'parent_id': 27281},
            {'id': 151, 'name': 'Indiana', 'parent_id': 27281},
            {'id': 152, 'name': 'Kentucky', 'parent_id': 27281},
            {'id': 153, 'name': 'Mississippi', 'parent_id': 27281},
            {'id': 154, 'name': 'Missouri', 'parent_id': 27281},
            {'id': 193, 'name': 'Tennessee', 'parent_id': 27281}]}
        """
        self._viable_api_key()
        url_prefix_params = {
            "a_url_prefix": "category/related?category_id=",
            "an_int_id": category_id,
        }
        url_prefix = self._append_id_to_url(**url_prefix_params)
        optional_args = {
            "&realtime_start=": realtime_start,
            "&realtime_end=": realtime_end,
        }
        url = self._add_optional_params(url_prefix, optional_args)
        self.category_stack["get_related_categories"] = self._fetch_data(url)
        return self.category_stack["get_related_categories"]

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
        filter_value: str = None,
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

        Notes
        -----
        FRED web service endpoint: fred/category/series
        https://fred.stlouisfed.org/docs/api/fred/category_series.html

        Examples
        --------
        >>> params = {
            'category_id': 125,
            'limit': 3,
            'filter_variable': 'units',
            'order_by': 'units',
            'sort_order': 'desc',
            'offset': 1,
            }
        >>> fred.get_series_in_a_category(**params)
        {'realtime_start': '2021-04-05',
        'realtime_end': '2021-04-05',
        'filter_variable': 'units',
        'filter_value': None,
        'order_by': 'units',
        'sort_order': 'desc',
        'count': 47,
        'offset': 1,
        'limit': 3,
        'seriess': [{'id': 'IEABCSIA',
            'realtime_start': '2021-04-05',
            'realtime_end': '2021-04-05',
            'title': 'Balance on secondary income',
            'observation_start': '1999-01-01',
            'observation_end': '2020-01-01',
            'frequency': 'Annual',
            'frequency_short': 'A',
            'units': 'Millions of Dollars',
            'units_short': 'Mil. of $',
            'seasonal_adjustment': 'Not Seasonally Adjusted',
            'seasonal_adjustment_short': 'NSA',
            'last_updated': '2021-03-23 07:31:14-05',
            'popularity': 3,
            'group_popularity': 4,
            'notes': 'Calculated by subtracting the secondary income (current transfer) payments from the secondary income (current transfer) receipts'},
            {'id': 'IEABCSIN', .......
        """
        self._viable_api_key()
        url_prefix_params = {
            "a_url_prefix": "category/series?category_id=",
            "an_int_id": category_id,
        }
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
        self.category_stack["get_series_in_a_category"] = self._fetch_data(url)
        return self.category_stack["get_series_in_a_category"]

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
            The start of the real-time period formatted as "YYYY-MM-DD".
            If None, fred.realtime_start is used.
            If fred.realtime_start = None, FRED web service will use today's date.
        realtime_end: str, default None
            The end of the real-time period formatted as "YYYY-MM-DD".
            If None, fred.realtime_end is used.
            If fred.realtime_end = None, FRED web service will use today's date.
        tag_names: list, default None
            list of tags [str] to include in returned data, excluding any tag not in tag_names;
            each tag must be present in the tag of returned series.
            If None, no filtering by tag names is done.
        tag_group_id: str, default None
            A tag group ID to filter tags by type with.
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
        fred.get_related_tags_for_a_category: Find related tags for tags within a FRED category.

        Notes
        -----
        FRED web service endpoint: fred/category/tags
        https://fred.stlouisfed.org/docs/api/fred/category_tags.html

        Examples
        --------
        >>> fred.get_tags_for_a_category(category_id = 125, limit = 3, order_by = 'created')
        {'realtime_start': '2021-04-05',
        'realtime_end': '2021-04-05',
        'order_by': 'created',
        'sort_order': 'desc',
        'count': 27,
        'offset': 0,
        'limit': 3,
        'tags': [
            {'name': 'public domain: citation requested',
            'group_id': 'cc',
            'notes': None,
            'created': '2018-12-17 23:33:13-06',
            'popularity': 100,
            'series_count': 42},
            {'name': 'headline figure', ...........

        """
        self._viable_api_key()
        url_prefix_params = {
            "a_url_prefix": "category/tags?category_id=",
            "an_int_id": category_id,
        }
        url_prefix = self._append_id_to_url(**url_prefix_params)
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
            The start of the real-time period formatted as "YYYY-MM-DD".
            If None, fred.realtime_start is used.
            If fred.realtime_start = None, FRED web service will use today's date.
        realtime_end: str, default None
            The end of the real-time period formatted as "YYYY-MM-DD".
            If None, fred.realtime_end is used.
            If fred.realtime_end = None, FRED web service will use today's date.
        tag_names: list, default None
            list of tags [str] to include in returned data, excluding any tag not in tag_names;
            each tag must be present in the tag of returned series.
            If None, no filtering by tag names is done.
        exclude_tag_names: list, default None
            list of tag names that series match none of.
            If None, no filtering by tag names is done.
        tag_group_id: str, default None
            A tag group ID to filter tags by type with.
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
            Metadata for each related tag.

        See Also
        --------
        fred.get_tags_for_a_category: Get tags found within a category.

        Notes
        -----
        FRED web service endpoint: fred/category/related_tags
        https://fred.stlouisfed.org/docs/api/fred/category_related_tags.html

        Examples
        --------
        >>> fred.get_related_tags_for_a_category(category_id = 125, tag_names = ('services', 'quarterly',), limit = 3)
        {'realtime_start': '2021-04-05',
        'realtime_end': '2021-04-05',
        'order_by': 'series_count',
        'sort_order': 'desc',
        'count': 9,
        'offset': 0,
        'limit': 3,
        'tags': [
            {'name': 'balance',
            'group_id': 'gen',
            'notes': '',
            'created': '2012-02-27 10:18:19-06',
            'popularity': 47,
            'series_count': 10},
            {'name': 'bea', .........
        """
        self._viable_api_key()
        url_prefix_params = {
            "a_url_prefix": "category/related_tags?category_id=",
            "an_int_id": category_id,
        }
        url_prefix = self._append_id_to_url(**url_prefix_params)
        optional_args = {
            "&tag_names=": tag_names,  # tag_names are required *
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
