
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

    def _add_optional_params(
            self,
            og_url_string: str,
            optional_params: dict,
            ) -> str:
        """
        Create a parameter string that adds any non-None parameters in optional_params to
        og_url_string

        Parameters
        ----------
        og_url_string: str
            the string to append new, non-null parameter strings to

        optional_params: dict
            a dictionary mapping parameter strings to actual arguments passed by user
            for example:
                "&tag_group_id=": None 
                "&limit=": 23
            if the value is not None, "&limit=" + str(23) is added to og_url_string

        Returns
        -------
        str

        """
        new_url_string = og_url_string
        for k in optional_params.keys():
            if optional_params[k] is not None:
                try:
                    a_parameter_string = k + str(optional_params[k])
                    new_url_string += a_parameter_string
                except TypeError:
                    print(k + " " + optional_params[k] + " cannot be cast to str")
        return new_url_string
    
    def _make_request_url(
            self, 
            var_url: str, 
            ):
        """
        Return the url that can be used to retrieve the desired data for series_id
        need to integrate other parameters as well
        Maximizes security in allowing direct pass of environment variable FRED_API_KEY 
        as api key sent to fred's web service

        var_url must include id irrespective of whether series_id, category_id, etc.
        """
#        file_type = "&file_type=json"
        url_base = [
                self.__url_base, 
                var_url, 
                "&file_type=json&api_key=",
                ]
        base = "".join(url_base)
        if self.__api_key_env_var:
            return base + os.environ["FRED_API_KEY"] #+ file_type
        return base + self.__api_key #+ file_type

    # modify: never print api key in message
    def _fetch_data(self, url_prefix: str) -> dict:
        """
        """
        url = self._make_request_url(url_prefix)
        json_data = self._get_response(url)
        if json_data is None:
            # modify here to never print api key in message
            message = "Data could not be retrieved using " 
            message += url_prefix 
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

    def _append_id_to_url(
            self, 
            a_url_prefix: str,
            an_int_id: int = None,
            a_str_id: str = None,
            ) -> str:
        """
        Return a_url_prefix with either an_int_id or a_str_id appended to it. 
        """
        if an_int_id is None and a_str_id is None:
            raise ValueError("No id argument given, cannot append to url")
        passed_id = an_int_id
        new_url_str = a_url_prefix
        if passed_id is None:
            passed_id = a_str_id
        try:
            new_url_str += str(passed_id)
        except TypeError:
            print("Unable to cast id to str, cannot append to url string")
        return new_url_str

    def _join_strings_by(
            self,
            strings: list,
            use_str: str,
            ) -> str:
        """
        Join an iterable of strings using use_str and return the fused string.
        """
        if strings is None or use_str is None:
            raise TypeError("strings and use_str are both required")
        try:
            fused_str = use_str.join(strings)
        except TypeError:
            print("Unable to join strings using %s" % use_str)
        return fused_str
            
