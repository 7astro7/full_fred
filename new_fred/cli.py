"""
A command-line interface for Federal Reserve Economic Data (FRED) via fredapi.
API Key Info: FRED_API_KEY environment variable is valid api key. 
To get a free key use https://fred.stlouisfed.org/ -> My Account -> API Keys.

Usage:
    fred (a | all) <series-id>
    fred configure
    fred examples
    fred (f | first) <series-id>
    fred (i | info) <series-id>
    fred (l | latest) <series-id>
    fred (s | series) [-start=<start-date>] [-end=<end-date>] <series-id>
    fred (s | series) [-o=<filename>] <series-id>
    fred (s | series) [-asof=<date>] <series-id>
    fred search [--limit=<limit>] [--orderby=<column>] [--asc | --desc] [--filter=<condition>] <search-text>
    fred search <search-text>
    fred search [-i | --infile] <filename> 
    fred (sr | search-release) [--limit=<limit>] [--orderby=<column>] <release-id>
    fred (sr | search-release) [--limit=<limit>] [--orderby=<column>] [--sort-order desc] [--filter=<condition>] <release-id>
    fred (sr | search-release) [-i | --infile]
    fred (sc | search-category) [--limit=<limit>] [--orderby=<column>] <category-id>
    fred (sc | search-category) [-i | --infile] <filename>

Options:
    -h, --help              Print this help message and exit
    --asof                  Get series data asof a specific date
    -start                 Specify desired start date of series
    -end                   Specify desired end date of series
    --plot                  Display matplotlib line plot of series
    -o                      Save fetched data in a file
    -i, --infile            Read in command options from a file
    --key                   Specify an API key
    --asc                   Sort search results in ascending order
    --desc                  Sort search results in descending order

Commands:
    a, all              Fetch all series data including revisions
    asof                Fetch series as of date
    i, info             Fetch series metadata such as frequency, units, etc.
    s, series           Fetch series. Default returns same as $ fred latest <series-id>
    f, first            Fetch first release of series
    l, latest           Fetch latest release of series
    search              Do a full-text search for a series
    sr, search-release  Search for series that belongs to a release id
    search-category     Search for series that belongs to a category id
    category-list       Show categories 
    vintage             Fetch a list of vintage dates for series. Vintage date: date of data revision or data release 
    configure           Change fredcli configuration including API Key 
    examples            Print example commands
    version             Print version and exit

Arguments:
    <series-id>
    <date>
    <start-date>
    <end-date>
    <search-text>
    <category-id>
    <release-id>
    <filename>
    <condition>

"""

# determine whether writing an api / fred class from scratch is auspicous:
#   the methods in fredapi might not necessarily be the optimal methods
#   of all that fred's api can support (reference site, gauge from there)
#       - categories, releases, series, tags, sources can all be classes potentially
# need to subclass Fred: 
#   _fetch_data() and get_series_info() need to be modified to raise 
#   exceptions with minimal output to terminal
# make sure all comands are filtered in cli function
# it may be prudent to ask for user configuration on first use 
#   this can include whether to save series by default in cwd
# order usage alphabetically by command
# order commands alphabetically 
# note defaults in __doc__
# add methods not included in fredapi
# create option for **kwargs
# help $ command for a specific command
# add tests for each module
# add to search params e.g. filter
# logging
# add clarity about api key in doc
# browser command? to open default browser to fred site
# add relevant options to doc
# set up configuration: some may not want to set env. var for api key
# caching data
# man pages?
# generate fredapi docs in this module so docopt has something to map cli arguments to fredapi parameters with
# examples: make valid date arguments clear to user

# Add:
# See Also
#    fredcli provides an interface to Fred via fredapi. fredapi has clear 
#    documentation, source code is available at https://github.com/mortada/fredapi

from .constants import VERSION
from fredapi import Fred
from fredapi.fred import (
        urlopen, ET, pd, HTTPError,
        )
from docopt import docopt
import sys
import os


def main():
    """
    Main function
    """
    try:
        cli()
    except KeyboardInterrupt:
        print("Exit")
        sys.exit(1)

def cli():
    """
    Run commands sent as user input
    """

    args = docopt(__doc__, version = VERSION) # save version as a constant. reference Python versioning system
                                            # may make sense to base version on fredapi 

    print(args, type(args))

    if args.get("a") or args.get("all"):
        check_id_param(args)

    elif args.get("f") or args.get("first"):
        check_id_param(args)

    elif args.get("i") or args.get("info"):
        check_id_param(args, "<series-id>")
        # try / except
        series_id = args.get("<series-id>").upper()
        series_info = FredCLI().get_series_info(series_id)
        if args.get("-o"):
            outfile = args.get("-o")
            check_user_input(outfile)
        print(series_info)

    elif args.get("latest"):
        check_id_param(args)

    elif args.get("configure"):
        pass
        # api key

    elif args.get("vintage"):
        check_id_param(args)

    elif args.get("examples"):
        pass
        #print_examples()

    if args.get("<series-id>"):
        try: 
            fred = FredCLI()
        except ValueError:
            pass

        # if only series-id is passed:
        #       equivalent to $ fred info

    if args.get("s") or args.get("series"):
        check_id_param(args, "<series-id>")
        print('args.get(series) works')
        # possible logic:
        # if retrieved previously:
        #       decompress archive
        #       if data that was just decompressed is up to date:
        #           return the series
        #       query fred for residual rows to update frame with
        # series has not been fetched at all yet: 
        #       fred.search() 
        if args.get("-asof"):
            pass

    elif args.get("search"):
        print('args.get(search) works')
        # check:
        #   text
        #   limit
        #   order by
        #   sort order
        #   filter
        fred.search(**params)

    elif args.get("sr") or args.get("search-release"):
        check_id_param(args, "<release-id>")
        # check:
        #   release id
        #   limit
        #   order by
        #   sort order
        #   filter

    elif args.get("sc") or args.get("search-category"):
        check_id_param(args, "<category-id>")
        # check:
        #   category id
        #   limit
        #   order by
        #   sort order
        #   filter
        # check:
        #   
        pass


search_type_map = {
        0: "full_text",
        1: "release",
        2: "category",
        }

def check_search_params(search_params, search_type: int = 0):
    """
    search type: 
        0: search by category
        1: search by release
        2: full-text search
    """
    search_type = search_type_map[search_type]



def check_id_param(args: dict, id_to_check: str):
    """

    """
    if not args.get(id_to_check):
        print("No %s passed" % id_to_check.strip("<").strip(">"))
        sys.exit(1)
    print('after sys.exit(1)')

def check_user_input(outfile: str):
    """
    
    """
    if os.path.exists(outfile):
        while True:
            print("File %s already exists. Do you want to overwrite it?" % outfile)
            print(" y for yes\n n for no \n c to choose a different name")
            user_choice = input("Please enter your choice or press \
                    enter now to quit").strip().lower()
            if user_choice == "c":
                check_user_input(user_choice)
            if user_choice == "" or user_choice == "n":
                print("Quitting")
                sys.exit(0) # double-check that exit code should be 0
            if user_choice == "y":
                with open(outfile, 'w') as f:
                    f.writelines()  # double-check this

class FredCLI(Fred):
    """
    A subclass of fredapi.fred.Fred. Exceptions are modified to
    be minimal and tailored for output to a terminal
    """

    def __init__(self):
        super().__init__()
        self.__series_url_prefix = self.root_url + "/series?series_id="

    def _fetch_data(self, url):
        # override to raise quiet exceptions
        # return bool to indicate failed operation and proceed from there, sidestepping
        # verbose exception messages (verbose for terminal)
        url += "&api_key=" + self.api_key

        # test next 2 lines for possible exceptions to handle them quietly
        try:
            response = urlopen(url).read()
            root = ET.fromstring(response)
        except HTTPError:
            return
        return root

    def get_series_info(self, series_id):
        # override to raise quiet exceptions
        # return bool to indicate failed operation and proceed from there, sidestepping
        # verbose exception messages (verbose for terminal)
        fetched_info = self._fetch_data(self.__series_url_prefix + series_id)
        if not fetched_info:
            print("Could not fetch info using series_id: %s" % series_id)
            sys.exit(1) # ascertain whether this is better than returning None
        return pd.Series(list(fetched_info)[0].attrib)








