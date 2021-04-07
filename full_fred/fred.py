
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
            Automatically detected and used for queries if no api_key string or api_key_file are given. To check that Fred 
            detects FRED_API_KEY:
                fred.env_api_key_found()
            
            api_key_file
            ------------
            Fred(api_key_file = 'key_file.txt')
            fred.set_api_key_file('key_file.txt')

            If an api_key_file is given Fred will ensure the file can be found and will use the string on the file's first line for queries.
            To get current api_key_file value:
                fred.get_api_key_file()

        Accessing Fetched Data 
        ----------------------
        When a request to FRED's servers is made, the returned data is available in a dictionary. 
        category_stack for category requests, tag_stack for tag requests, etc. Keys are the name of the method used to retrieve the data.
        For example, after calling fred.get_tags(), fred.tag_stack["get_tags"] will return the data that FRED responded with, until a new get_tags method
        invocation is made. 

        Setting Realtime Defaults
        -------------------------
        define realtime_start and realtime_end
        """
        super().__init__()
        if api_key_file is not None:
            self.set_api_key_file(api_key_file)
        else:
            self.api_key_file = api_key_file




