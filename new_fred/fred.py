
from requests.exceptions import RequestException
import pandas as pd
import requests
import os

# expand on current docstrings to explain with greater clarity
# define tags, sources, series, categories, releases, etc.
# define realtime_start and realtime_end
# create a thing on how to set environment variables to enable broad use 
# integrate ALFRED, GeoFRED

class FredBase:
    """
    go heavy on getters and setters so data can be stored
    store api key with salts
    """
    def __init__(self, 
            api_key = None, 
            api_key_file = None):
        self.__realtime_start = "1776-07-04"
        self.__realtime_end = "9999-12-31"
        self.__url_base = "https://api.stlouisfed.org/fred/"
        self.__api_key_env_var = False
        if os.environ["FRED_API_KEY"] is not None:
            self.__api_key_env_var = True
        self.__api_key = api_key

    def api_key_found(self):
        return self.__api_key_env_var
    
    def _make_request_url(self, var_url: str):
        """
        Return the url that can be used to retrieve the desired data for series_id
        need to integrate other parameters as well
        Maximizes security in allowing direct pass of environment variable FRED_API_KEY 
        as api key sent to fred's web service

        var_url must include id irrespective of whether series_id, category_id, etc.
        """
        url_base = [self.__url_base, var_url, "&api_key="]
        base = "".join(url_base)
        file_type = "&file_type=json"
        if self.__api_key_env_var:
            return base + os.environ["FRED_API_KEY"] + file_type
        return base + self.__api_key + file_type

    def _fetch_data(self, url_prefix: str) -> dict:
        """
        """
        url = self._make_request_url(url_prefix)
        json_data = self._get_response(url)
        if json_data is None:
            message = "Data could not be retrieved using" \
                    "id : %s" % an_id
            print(message)
            return
        return json_data

    def _get_realtime_date(self, 
            realtime_start: str = None,
            realtime_end: str = None,
            ) -> str:
        """
        Takes a string as input and returns the YYY-MM-DD 
        realtime date string to use for construction of a request url
        """
        rt_start = "&realtime_start="
        rt_end = "&realtime_end="
        if realtime_start is None:
            rt_start += self.__realtime_start
        else:
            try:
                realtime_start = str(realtime_start)
            except TypeError:
                pass # this needs to be more effective
        if realtime_end is None:
            rt_end += self.__realtime_end
        else:
            try:
                realtime_end = str(realtime_end)
            except TypeError:
                pass # this needs to be more effective
        return rt_start + rt_end
        
    def _get_response(self, a_url: str) -> dict:
        """
        Return a JSON dictionary response with data retrieved from a_url
        """
        try:
            response = requests.get(a_url)
        except RequestException:
            return
        return response.json()
            
class FredSeries(FredBase):
    
    # return series name and metadata in __str__
    def __init__(self, series_id: str = None):
        super().__init__()
        self.series_id = series_id
        self.__metadata = None # change get_series to something akin to get_metadata
        self.observations = None
        self.release = None
        self.__categories = None
        self.__df = None

#    def __str__(self):
#        return self.series_id

    def _check_series_id(
            self, 
            series_id: str,
            ):
        """
        if self.series_id has not been set, this method sets it to series_id if
        it is a string
        checks that series_id is the same as self.series_id
        """
        # if self.series_id is already set and it's set to another id:
        #   deal with this potential situation
        if self.series_id is None: 
            e = "series_id attribute has not been set"
            raise AttributeError(e)
        if not isinstance(series_id, str):
            raise TypeError("series_id must be str")
        self.series_id = series_id

    def get_series(
            self, 
            series_id: str = None, 
            realtime_start: str = None, 
            realtime_end: str = None, 
            ):
        """
        Get an economic data series
        all parameters fred offers: y
        FRED accepts upper case series_id
        default realtime start and realtime end: first to last available
        if series_id attribute is not set, FredSeries.series_id will be set to 
        the series_id passed in this method

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
        """
        if series_id is not None:
            self._check_series_id(series_id)
        if self.__metadata is not None:
            return self.__metadata
        url_prefix = "series?series_id=" + self.series_id
        realtime_period = self._get_realtime_date(
                realtime_start, 
                realtime_end
                )
        url_prefix += realtime_period
        self.__metadata = self._fetch_data(url_prefix)
        return self.__metadata

    # a name attribute?
    def get_categories_of_series(
            self, 
            series_id: str,
            realtime_start: str = None,
            realtime_end: str = None,
            ):
        """
        Get categories that FRED uses to classify series 

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
        """
        if series_id is not None:
            self._check_series_id(series_id)
        if self.__categories is not None:
            return self.__categories
        url_prefix = "series/categories?series_id=" + self.series_id
        realtime_period = self._get_realtime_date(
                realtime_start, 
                realtime_end
                )
        url_prefix += realtime_period
        self.__categories = self._fetch_data(url_prefix)
        return self.__categories


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
            ):
        """
        Get the observations for an series in a pandas DataFrame
        """
        if series_id is not None:
            self._check_series_id(series_id)
        if self.__categories is not None:
            return self.__categories
        url_prefix = "series/observations?series_id=" + self.series_id
        realtime_period = self._get_realtime_date(
                realtime_start, 
                realtime_end
                )
        url_prefix += realtime_period
        self.__df = self._fetch_data(url_prefix)
        return self.__df

    def get_release_of_series(self):
        """
        Get the release for an economic data series
        """
        pass


class Category(FredBase):

    # tenuous
    
    def __init__(self, 
            id: int = None, 
            name: str = None,
            parent_id: int = None
            ):
        super().__init__()
        self.id = id
        self.name = name
        self.parent_id = parent_id

# utilize stacks

fred_category_map = {
        "get_a_category": "fred/category",
        "get_child_categories": "fred/category/children",
        "get_related_categories": "fred/category/related",
        "get_series_in_a_category": "fred/category/series",
        "get_tags_for_a_category": "fred/category/tags",
        "get_related_tags_for_a_category": "fred/category/related_tags",
        }

fred_all_releases_map = {
        "get_all_releases": "fred/releases",
        "get_dates_of_all_releases": "fred/releases/dates",
        }

fred_releases_map = {
        "get_a_release": "fred/release",
        "get_dates_for_a_release": "fred/release/dates",
        "get_series_of_a_release": "fred/release/series",
        "get_sources_for_a_release": "fred/release/sources",
        "get_related_tags_for_a_release": "fred/release/related_tags",
        "get_tables_for_a_release": "fred/release/tables", # * revisit this
        }

fred_series_map = {
        "get_a_series": "fred/series",
        "get_categories_of_series": "fred/series/categories",
        "get_observations_of_series": "fred/series/observations",
        "get_release_for_a_series": "fred/series/release",
        "search_series_by_keywords": "fred/series/search",
        "get_tags_for_a_series_search": "fred/series/tags", # revisit
        "get_related_tags_for_a_series_search": "fred/series/search/related_tags",
        "get_tags_of_a_series": "fred/series/tags",
        "get_series_sorted_by_latest_update": "fred/series/updates", # requires clarification
        "get_dates_of_series_revisions": "fred/series/vintagedates", 
        }

fred_sources_map = {
        "get_all_sources": "fred/sources", # revisit
        "get_a_source": "fred/source",
        "get_releases_for_a_source": "fred/source/releases",
        }

fred_tags_map = {
        "get_all_tags": "fred/tags", # revisit
        "get_related_tags": "fred/related_tags", 
        "get_series_matching_tags": "fred/series", 
        }

# make keys for each stack the parameters that were passed, not only the id used
# set default params to None, not fred web service params
# add option to retrieve tag notes
# heavily integrate pandas
# add parameter to return all requested data as dataframes
# create a stack that holds only the parameters of the *latest* request
# must provide for case where new parameters are sent to already-used method and data has to be queried again
# Can save metadata about last df query to check new request against
class Fred(FredBase):
    """
    Clarify what series_map is
    """

    # go ham on docstrings for methods
    """
    Use api_key_found() to determine if an api key is found as 
    an environment variable with name FRED_API_KEY
    """
    
    def __init__(self):
        super().__init__()
        self.__category_stack = dict() # eh
        self.series_map = dict() # eh
        self.unit_info = dict() # put explanation of units options
        self.tag_stack = dict()
        self.release_stack = dict()

    # not finished
    # may be redundant
    def peek_last_category_query(self):
        """
        Returns the key (method called + category_id used) 
        of the top of the category query stack
        """
        return self.__category_stack.keys() # fix this

    def get_all_category_query_keys(self):
        """
        Returns the keys (key: str = method called + category_id used) 
        of all queries in the category query stack
        """
        return list(self.__category_stack.keys())

    # work on this
    def get_category_query(self, key: str):
        """
        Returns the value for key from the category query stack 
        (key: str = method called + category_id used) 
        of all queries in the category query stack

        Parameters
        ----------

        Returns
        -------

        """
        try:
            query = self.__category_stack[key]
        except KeyError:
            print("Key %s " % key)
        return self.__category_stack.keys() # fix this

    def get_a_category(self, category_id: int) -> dict:
        """
        Get a category of FRED data using its id

        Parameters
        ----------

        Returns
        -------
        """
        try:
            url_prefix = "category?category_id=" + str(category_id)
        except TypeError:
            print("Cannot cast category_id %s to str" % category_id)
        json_data = self._fetch_data(url_prefix)
        key = "get_a_category__category_id_" + str(category_id)
        self.__category_stack[key] = json_data
        return json_data

    def get_child_categories(
            self, 
            category_id: int,
            realtime_start: str = None,
            realtime_end: str = None,
            ) -> dict:
        """
        Get child categories (category_id, name, parent_id) 
        of category associated with category_id

        Parameters
        ----------

        Returns
        -------
        """
        url_prefix = "category/children?category_id=" 
        try:
            url_prefix += str(category_id)
        except TypeError:
            print("Cannot cast category_id %s to str" % category_id)
        realtime_period = self._get_realtime_date(
                realtime_start, 
                realtime_end
                )
        url_prefix += realtime_period
        json_data = self._fetch_data(url_prefix)
        key = "get_child_categories__category_id_" + str(category_id)
        self.__category_stack[key] = json_data
        return json_data

    def get_related_categories(self, category_id: int):
        """
        add all parameters fred offers
        unclear how to test rn
        count parameter***
        """
        url_prefix = "category/related?category_id="
        json_data = self._fetch_data(url_prefix, category_id)
        key = "get_related_categories__category_id_" + str(category_id) 
        # add realtime params to key if they're passed (later)
        self.__category_stack[key] = json_data
    
    # add parameter to remove discontinued series
    def get_series_in_a_category(self, category_id: int): 
        """
        add all parameters fred offers
        unclear how to test rn
        count parameter***
        """
        url_prefix = "category/series?category_id="
        pass

    def get_tags_for_a_category(self, category_id: int):
        """
        add all parameters fred offers
        unclear how to test rn
        count parameter***
        """
        url_prefix = "category/tags?category_id="
        pass

    def get_related_tags_for_a_category(self, category_id: int):
        """
        add all parameters fred offers
        unclear how to test rn
        count parameter***
        """
        url_prefix = "category/related_tags?category_id="
        pass

    # fred/release 
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


    # fred/series

    def get_series(
            self, 
            series_id: str, 
            realtime_start: str = None, 
            realtime_end: str = None,
            ):
        """
        Get an economic data series using series_id. If the 
        series hasn't been fetched it's added to Fred.series_maps, 
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
        """
        if not series_id in self.series_map.keys():
            self.series_map[series_id] = FredSeries(series_id)
        params = dict(
                series_id = series_id, # revisit: series_id given in constructor above
                                        # but above code may not be executed
                realtime_start = realtime_start,
                realtime_end = realtime_end,
                )
        return self.series_map[series_id].get_series(**params) 

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
        """
        if not series_id in self.series_map.keys():
            self.series_map[series_id] = FredSeries(series_id)
        params = dict(
                series_id = series_id, # revisit: series_id given in constructor above
                                        # but above code may not be executed
                realtime_start = realtime_start,
                realtime_end = realtime_end,
                )
        return self.series_map[series_id].get_categories_of_series(**params) 

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
        output_type
        vintage_dates

        Returns
        -------

        Notes
        -----
        """
        if not series_id in self.series_map.keys():
            self.series_map[series_id] = FredSeries(series_id)
        params = dict(
                series_id = series_id, # revisit: series_id given in constructor above
                realtime_start = realtime_start,
                realtime_end = realtime_end,
                )
        return self.series_map[series_id].get_series_df(**params) 

    def find_series_by_keyword(self, keywords: list):
        """
        Get economic data series that match keywords
        """
        pass

    def get_search_tags(self, keywords: list):
        """
        /series/search/tags
        Get economic data series that match keywords
        """
        pass

    # fred/tags

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
            ):
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


        
