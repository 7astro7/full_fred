
from .tags import Tags

# create getters and setters for default realtime variables

# api key
# expand on current docstrings to explain with greater clarity
# define tags, sources, series, categories, releases, etc.
# define realtime_start and realtime_end
# create a thing on how to set environment variables to enable broad use 
# integrate ALFRED, GeoFRED

# go heavy on examples
# make keys for each stack the parameters that were passed, not only the id used
# set default params to None, not fred web service params
# add option to retrieve tag notes
# heavily integrate pandas
# add parameter to return all requested data as dataframes
# create a stack that holds only the parameters of the *latest* request
# must provide for case where new parameters are sent to already-used method and data has to be queried again
# Can save metadata about last df query to check new request against
class Fred(Tags):
    """
    Clarify what series_stack is
    # go ham on docstrings for methods
    Use api_key_found() to determine if an api key is found as 
    an environment variable with name FRED_API_KEY
    realtime period: (start, end), not [start, end]

    define realtime periods

    set return_type for pd.DataFrame
    """
    
    def __init__(self):
        super().__init__()
        self.unit_info = dict() # put explanation of units options<- no, explain in method doc
        self.return_type = dict

    def get_realtime_start(self):
        """
        Returns default realtime_start
        """
        return self._FredBase_realtime_start

    def set_realtime_start(self, new_rt_start: str):
        """
        Sets default realtime_start
        """
        self._FredBase_realtime_start = new_rt_start

    def get_realtime_end(self):
        """
        Returns default realtime_end
        """
        return self._FredBase_realtime_end

    def set_realtime_end(self, new_rt_end: str):
        """
        Sets default realtime_end
        """
        self._FredBase_realtime_end = new_rt_end



