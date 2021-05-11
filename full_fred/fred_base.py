from requests.exceptions import RequestException
import requests
import os


class FredBase:
    def __init__(
        self,
        api_key_file: str = None,
    ):
        """
        FredBase defines methods common to Categories, Releases,
        Series, Releases, Sources, Tags classes.
        """
        self.realtime_start = None
        self.realtime_end = None
        self.observation_start = None
        self.observation_end = None
        self.__url_base = "https://api.stlouisfed.org/fred/"
        if api_key_file is not None:
            self.set_api_key_file(api_key_file)
        else:
            self.api_key_file = api_key_file

    def get_api_key_file(
        self,
    ) -> str:
        """
        Return currently assigned api_key_file.
        """
        return self.api_key_file

    def set_api_key_file(
        self,
        api_key_file: str,
    ) -> bool:
        """
        Return True if api_key_file has been found.
        """
        if not os.path.isfile(api_key_file):
            e = "Can't find %s on path" % api_key_file
            raise FileNotFoundError(e)
        self.api_key_file = api_key_file
        return True

    def _read_api_key_file(
        self,
    ) -> str:
        """
        Read FRED api key from file. This method exists to minimize the
        time that the user's API key is human-readable
        """
        try:
            with open(self.api_key_file, "r") as key_file:
                return key_file.readline().strip()
        except FileNotFoundError as e:
            print(e)

    def env_api_key_found(self) -> bool:
        """
        Indicate whether a FRED_API_KEY environment variable is detected.
        """
        if "FRED_API_KEY" in os.environ.keys():
            if os.environ["FRED_API_KEY"] is not None:
                return True
        return False

    def _add_optional_params(
        self,
        og_url_string: str,
        optional_params: dict,
    ) -> str:
        """
        Create a parameter string that adds any non-None parameters in optional_params to
        og_url_string and return og_url_string with these additions. If all optional_params
        are None, return og_url_string

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
            og_url_string with any existent k, v pairs concatenated to it.

        Notes
        -----
        Not all paramaters passed in optional_params need be optional. Most are.

        If tag_names is a substring of a parameter in optional_params, whitespace is
        replaced with "+" so the request URL encodes the whitespace in a standard way.
        There's more on this at
        https://fred.stlouisfed.org/docs/api/fred/related_tags.html
        """
        new_url_string = og_url_string

        # use user-set attribute value if set and argument for it 
        # isn't passed in optional_params
        attribute_map = {
                "&observation_start=": self.observation_start, 
                "&observation_end=": self.observation_end, 
                "&realtime_start=": self.realtime_start, 
                "&realtime_end=": self.realtime_end, 
                }

        for k in optional_params.keys():
            if k in attribute_map.keys():
                if optional_params[k] is None:
                    if attribute_map[k] is not None:
                        optional_params[k] = attribute_map[k]
            if optional_params[k] is not None:
                if k == "&include_release_dates_with_no_data=":
                    try:
                        optional_params[k] = str(optional_params[k]).lower()
                    except TypeError:
                        e = (
                            "Cannot cast include_empty to str, "
                            "cannot create request url to fetch"
                            " data"
                        )
                        print(e)
                if "tag_names" in k:
                    tag_names = optional_params[k]
                    try:
                        str_names = self._join_strings_by(tag_names, ";")
                        str_names = str_names.strip().replace(" ", "+")
                        optional_params[k] = str_names
                    except TypeError:
                        e = "Cannot add tag_names to FRED query url"
                        print(e)
                try:
                    a_parameter_string = k + str(optional_params[k])
                    new_url_string += a_parameter_string
                except TypeError:
                    print(k + " " + optional_params[k] + " cannot be cast to str")
        return new_url_string

    def _viable_api_key(self) -> str:
        """
        Verifies that there's an api key to make a request url with.
        Raises error if necessary to allow methods to catch, early in
        query process, whether a request for data can be sent to FRED.
        If there's a usable key, return which one to use

        Returns
        -------
        str
            A string indicating where to find user's api key
            attribute: user has set self.__api_key attribute
            env: it's an environment variable
            file: user has specified a file holding the key
        """
        if self.api_key_file is None:
            if not self.env_api_key_found():
                raise AttributeError("Cannot locate a FRED API key")
            return "env"
        return "file"

    def _make_request_url(
        self,
        var_url: str,
    ) -> str:
        """
        Return the url that can be used to retrieve the desired data given var_url.
        """
        key_to_use = self._viable_api_key()
        url_base = [
            self.__url_base,
            var_url,
            "&file_type=json&api_key=",
        ]
        base = "".join(url_base)
        if key_to_use == "env":
            try:
                return base + os.environ["FRED_API_KEY"]
            except KeyError as sans:
                print(sans, " no longer found in environment")
        if key_to_use == "file":
            return base + self._read_api_key_file()

    def _fetch_data(
        self,
        url_prefix: str,
    ) -> dict:
        """
        Make request URL, send it to FRED, return JSON upshot
        """
        url = self._make_request_url(url_prefix)
        json_data = self._get_response(url)
        if json_data is None:
            # never print api key in message for security
            message = "Data could not be retrieved, returning None"
            print(message)
            return
        return json_data

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
