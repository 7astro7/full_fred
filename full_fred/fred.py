from .tags import Tags


class Fred(Tags):
    def __init__(
        self,
        api_key_file: str = None,
        observation_start: str = None,
        observation_end: str = None,
    ):
        """
        API Key
        -------
        Querying FRED's servers can be done with an API key. To get a new key use https://fred.stlouisfed.org/ -> My Account -> API Keys.

            FRED_API_KEY environment variable
            ---------------------------------
            Automatically detected and used for queries if no api_key_file is given. To check that Fred detects FRED_API_KEY in environment:
                fred.env_api_key_found()

            api_key_file
            ------------
            Fred(api_key_file = 'example_key.txt')
            fred.set_api_key_file('example_key.txt')

            If an api_key_file is given Fred will ensure the file can be found and will use the string on the file's first line for queries.
            To get current api_key_file value:
                fred.get_api_key_file()

            In neither case is your api key stored. When a request is made your key will be read from api_key_file or environment.

        Accessing Fetched Data
        ----------------------
        When a request to FRED's servers is made, the returned data is available in a dictionary.
        category_stack for category requests, tag_stack for tag requests, etc. Each stack is a dictionary with method names for keys and the retrieved
        data for values. For example, after calling fred.get_tags(), fred.tag_stack["get_tags"] will return the data FRED web service responded with,
        until a new get_tags method invocation is made or you pop "get_tags".

        Setting Realtime, Observation Start/End Defaults
        -------------------------
        fred.realtime_start: if set, will be used when realtime_start argument is not given. 
        fred.realtime_end: if set, will be used when realtime_end argument is not given. 
        fred.observation_start: if set, will be used when observation_start argument is not given. 
        fred.observation_end: if set, will be used when observation_end argument is not given. 

        All queries with realtime_start as a parameter will use whatever fred.realtime_start is set to if no realtime_start argument is given. If
        fred.realtime_start is set to None, FRED web service will determine the default value. In most cases where realtime_start isn't specified FRED
        web service will use today's date. Same with fred.realtime_end.
        All queries that include observation_start as a parameter will use whatever fred.observation_start is set to if no observation_start argument is given. If
        fred.observation_start is set to None, FRED web service will determine the default value. In cases where observation_start isn't specified FRED
        web service will use '1776-07-04', and '9999-12-31' for fred.observation_end.
        """
        super().__init__()
        if api_key_file is not None:
            self.set_api_key_file(api_key_file)
        else:
            self.api_key_file = api_key_file
