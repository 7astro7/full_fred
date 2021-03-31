
from .series import Series

class Sources(Series):

    def __init__(self):
        super().__init__()
        self.source_stack = dict()

    # fred/sources          make into class

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

        Returns
        -------
        dict

        Notes
        -----
        fred/sources
        """
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
        self.source_stack["sources"] = self._fetch_data(url) # improve this key
        return self.source_stack["sources"]

    def get_a_source(
            self,
            source_id: int,
            realtime_start: str = None,
            realtime_end: str = None,
            ):
        """
        Get a source of economic data.

        Parameters
        ----------
        source_id: int
            the id of the series
        realtime_start: str, default "1776-07-04" (earliest)
            YYY-MM-DD as per fred
        realtime_end: str, default "9999-12-31" (last available) 
            YYY-MM-DD as per fred

        Returns
        -------

        Notes
        -----
        fred/source
        """
        url_prefix = "source?source_id="
        try:
            url_prefix += str(source_id)
        except TypeError:
            print("Unable to cast source_id %s to str" % source_id)
        optional_args = {
                "&realtime_start=": realtime_start,
                "&realtime_end=": realtime_end,
            }
        url = self._add_optional_params(url_prefix, optional_args)
        self.source_stack[source_id] = self._fetch_data(url)
        return self.source_stack[source_id]

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
            the id of the series

        realtime_start: str default None

        realtime_end: str default None

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

        Notes
        -----
        fred/source/releases
        """
        url_prefix = "source/releases?source_id="
        try:
            url_prefix += str(source_id)
        except TypeError:
            print("Unable to cast source_id %s to str" % source_id)
        optional_args = {
                "&realtime_start=": realtime_start,
                "&realtime_end=": realtime_end,
                "&limit=": limit,
                "&offset=": offset,
                "&order_by=": order_by,
                "&sort_order=": sort_order,
            }
        url = self._add_optional_params(url_prefix, optional_args)
        self.source_stack[source_id] = self._fetch_data(url)
        return self.source_stack[source_id]
