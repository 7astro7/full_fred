
from .tags import Tags


class Fred(Tags):
    
    def __init__(
            self,
            api_key_file: str = None,
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

            In neither case is your api key stored.

        Accessing Fetched Data 
        ----------------------
        When a request to FRED's servers is made, the returned data is available in a dictionary. 
        category_stack for category requests, tag_stack for tag requests, etc. Each stack is a dictionary with method names for keys and the retrieved 
        data for values. For example, after calling fred.get_tags(), fred.tag_stack["get_tags"] will return the data FRED web service responded with, 
        until a new get_tags method invocation is made or you pop "get_tags". 

        Setting Realtime Defaults
        -------------------------
        fred.realtime_start is set to '1776-07-04', earliest available, by default. 
        fred.realtime_end is set to '9999-12-31', latest available, by default. 

        All queries with realtime_start as a parameter will use whatever fred.realtime_start is set to if no argument for it is given. If you 
        set fred.realtime_start to None FRED web service will determine the default value. When fred.realtime_start = None and no argument is given 
        for realtime_start, in most cases today's date will be used. Same with fred.realtime_end.
        """
        super().__init__()
        if api_key_file is not None:
            self.set_api_key_file(api_key_file)
        else:
            self.api_key_file = api_key_file




