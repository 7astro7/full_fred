
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
            print(base + os.environ["FRED_API_KEY"] + file_type)
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

fred_categories_map = {
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

    def get_a_category(self, category_id: int):
        """
        Get a category of FRED data using its id
        """
        try:
            path_crux = "category?category_id=" + str(category_id)
        except TypeError:
            print("Unable to cast category_id %s to string" % \
                    category_id)
        url = self._make_request_url(path_crux)
        print(url)
        json_data = self._get_response(url)
        if json_data is None:
            message = "Category data could not be retrieved using" \
                    " category_id: %s" % category_id
            print(message)
            return
        self.__category_stack[len(self.__category_stack)] = (
                "get_a_category", category_id,)
        return json_data

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
        
        
