
import requests
import os

from requests.exceptions import RequestException

# expand on current docstrings to explain with greater clarity
# define tags, sources, series, categories, releases, etc.

class FredBase:
    """
    go heavy on getters and setters so data can be stored
    store api key with salts
    """
    def __init__(self, 
            api_key = None, 
            api_key_file = None):
        self.__url_base = "https://api.stlouisfed.org/fred/"
        self.__api_key_env_var = False
        if os.environ["FRED_API_KEY"] is not None:
            self.__api_key_env_var = True
        self.__api_key = api_key

    def api_key_found(self):
        return self.__api_key_env_var
    
    def _make_request_url(self, path_crux: str):
        """
        Return the url that can be used to retrieve the desired data for series_id
        need to integrate other parameters as well
        Maximizes security in allowing direct pass of environment variable FRED_API_KEY 
        as api key sent to fred's web service

        path_crux must include id irrespective of whether series_id, category_id, etc.
        """
        url_base = [self.__url_base, path_crux, "&api_key="]
        base = "".join(url_base)
        file_type = "&file_type=json"
        if self.__api_key_env_var:
            return base + os.environ["FRED_API_KEY"] + file_type
        return base + self.__api_key + file_type
        
    def _get_response(self, a_url: str) -> dict:
        """
        Return a JSON dictionary response with data retrieved from a_url
        """
        try:
            response = requests.get(a_url)
        except RequestException:
            return
        return response.json()
            
class Series(FredBase):
    
    def __init__(self, series_id: str = None):
        super().__init__()
        self.series_id = series_id
        self.series = None
        self.observations = None
        self.release = None


    def get_series(self):
        """
        Get an economic data series
        """
        pass
    
    # remove _of_series for all ?
    def get_categories_of_series(self):
        """
        Get the categories for an economic data series
        """
        pass


    def get_observations_of_series(self):
        """
        Get the observations or data values for an economic data series
        """
        pass

    def get_release_of_series(self):
        """
        Get the release for an economic data series
        """
        pass

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

class Fred(FredBase):

    # go ham on docstrings for methods
    """
    Use api_key_found() to determine if an api key is found as 
    an environment variable with name FRED_API_KEY
    """
    
    def __init__(self):
        super().__init__()
        self.__category_stack = dict() # eh
        self.__series_stack = dict() # eh

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


    # move to FredBase?
    def _fetch_data(self, url_prefix: str, an_id: int) -> dict:
        """
        """
        path_crux = self._make_path_crux(url_prefix, an_id)
        url = self._make_request_url(path_crux)
        json_data = self._get_response(url)
        if json_data is None:
            message = "Data could not be retrieved using" \
                    "id : %s" % an_id
            print(message)
            return
        return json_data

    # move to FredBase?
    def _make_path_crux(self, 
            path_crux_prefix: str, 
            an_id: int
            ): # think twice about int
        """
        Returns variable portion of url that can fetch the desired data
        from FRED API. If an_id is not an int there's substantial probability
        the url won't be constructed correctly even in absence of an exception
        """
        try:
            path_crux = path_crux_prefix + str(an_id)
        except TypeError:
            print("Unable to cast id %s to string" % an_id)
        return path_crux

    def get_a_category(self, category_id: int) -> dict:
        """
        Get a category of FRED data using its id

        Parameters
        ----------

        Returns
        -------
        """
        url_prefix = "category?category_id=" 
        json_data = self._fetch_data(url_prefix, category_id)
        key = "get_a_category__category_id_" + str(category_id)
        self.__category_stack[key] = json_data
        return json_data

    def get_child_categories(self, category_id: int) -> dict:
        """
        Get child categories (category_id, name, parent_id) 
        of category associated with category_id

        Parameters
        ----------

        Returns
        -------
        """
        url_prefix = "category/children?category_id="
        json_data = self._fetch_data(url_prefix, category_id)
        key = "get_child_categories__category_id_" + str(category_id)
        self.__category_stack[key] = json_data
        return json_data

    def get_related_categories(self, category_id: int):
        url_prefix = "category/related?category_id="
        pass
    
    def get_series_in_a_category(self, category_id: int): 
        pass

    def get_tags_for_a_category(self, category_id: int):
        pass

    def get_related_tags_for_a_category(self, category_id: int):
        pass

    def get_a_series(self, series_id: int):
        pass


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
        
        
