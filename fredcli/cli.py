"""
A CLI for Federal Reserve Economic Data (FRED) via fredapi.
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
    fred (sr | search-release) [--limit=<limit>] [--orderby=<column>] [--sort-order desc] [--filter seasonal-adjustment] <release-id>
    fred (sr | search-release) [-i | --infile]
    fred (sc | search-category) [--limit=<limit>] [--orderby=<column>] <category-id>
    fred (sc | search-category) [-i | --infile] <filename>

Options:
    -h, --help              Print this help message and exit
    --asof                  Get series data asof a specific date
    -start                 Specify desired start date of series
    -end                   Specify desired end date of series
    --plot                  Display matplotlib line plot of series
    -o                      Save series data in a file
    -i, --infile            Read in command options from a file
    --key                   Specify an API key
    --asc                   Sort search results in ascending order
    --desc                  Sort search results in descending order

Commands:
    i, info             Fetch series metadata such as frequency, units, etc.
    s, series           Fetch series. Default returns same as $ fred latest <series-id>
    f, first            Fetch first release of series
    l, latest           Fetch latest release of series
    asof                Fetch series as of date
    a, all              Fetch all series data including revisions
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

# order usage alphabetically by command
# note defaults in __doc__
# help $ command for a specific command
# add tests for each module
# add to search params e.g. filter
# logging
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
    Run command sent as user input
    """

    args = docopt(__doc__, version = VERSION) # save version as a constant. reference Python versioning system
                                            # may make sense to base version on fredapi 

    if args.get("a") or args.get("all"):
        if not args.get("series-id"):
            pass

    elif args.get("-asof"):
        if not args.get("series-id"):
            pass

    elif args.get("f") or args.get("first"):
        if not args.get("series-id"):
            pass

    elif args.get("i") or args.get("info"):
        if not args.get("series-id"):
            pass

    elif args.get("latest"):
        if not args.get("series-id"):
            pass

    elif args.get("configure"):
        pass
        # api key

    elif args.get("examples"):
        pass
        #print_examples()

    if args.get("series-id"):
        try: 
            fred = Fred()
        except ValueError:
            pass

        # if only series-id is passed:
        #       equivalent to $ fred info

    if args.get("s") or args.get("series"):
        print('args.get(series) works')
        # possible logic:
        # if retrieved previously:
        #       decompress archive
        #       if data that was just decompressed is up to date:
        #           return the series
        #       query fred for residual rows to update frame with
        # series has not been fetched at all yet: 
        #       fred.search() 

    elif args.get("search"):
        print('args.get(search) works')
        if not args.get("series-id"):
            while True:
                user_choice = input(
                "No series_id passed. Specify one now or press q to quit."
                ).lower().strip()
                if user_choice == "q":
                    sys.exit(0)
                    # return None?
        fred.get_series()

    elif args.get("sc") or args.get("search-category"):
        pass

