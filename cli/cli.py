"""
A CLI for Federal Reserve Economic Data (FRED) via fredapi

API Key
    - FRED_API_KEY environment variable is valid api key
    To get a free key
        - https://fred.stlouisfed.org/ -> My Account -> API Keys 

Usage:
    fred (i | info) <series-id>
    fred (s | series) <series-id>
    fred (s | series) --start 7-15-2000 --end 10-25-2018 <series-id>
    fred (f | first) <series-id>
    fred (l | latest) <series-id>
    fred asof 10-25-2018 <series-id>
    fred configure
    fred examples

Options:
    --start                 Specify desired start date of series
    --end                   Specify desired end date of series
    --plot                  Display matplotlib line plot of series.
    -o                      Save series as OUTFILE
    --key FRED_API_KEY      Use 

Commands:
    i, info             Fetch series metadata such as frequency, units, etc.
    s, series           Fetch series
    f, first            Fetch first release of series
    l, latest           Fetch latest release of series
    asof                Fetch -----
    search              Do a full-text search for a series
    search-release      Search for series that belongs to a release id
    search-category     Search for series that belongs to a category id
    category-list       Show categories 
    configure           ---
    examples            Print example commands.

Arguments:
    <series-id>
"""

# I left off comparing get_series_first_release() in fredapi


from fredapi import Fred
from docopt import docopt
import sys

# use docopt to parse command-line arguments
# add tests for each module
# logging
# browser command? to open default browser to fred site
# add relevant options to doc
# set up configuration: some may not want to set env. var for api key
# caching data
# man pages?
# generate fredapi docs in this module so docopt has something to map cli arguments to fredapi parameters with
# examples: make valid date arguments clear to user

fred = Fred()

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

    args = docopt(__doc__, version = '0.01') # save version as a constant. reference Python versioning system
                                            # may make sense to base version on fredapi 

    if args.get("series-id"):
        # if only series-id is passed:
        #       equivalent to $ fred info

    if args.get("series"):
        # possible logic:
        # if retrieved previously:
        #       decompress archive
        #       if data that was just decompressed is up to date:
        #           return the series
        #       query fred for residual rows to update frame with
        # series has not been fetched at all yet: 
        #       fred.search() 

    elif args.get("search"):
        if not (args.get("-i") or args.get("--id")):
            while True:
                user_choice = input(
                "No series_id passed. Specify one now or press q to quit."
                ).lower().strip()
                if user_choice == "q":
                    sys.exit(0)
                    # return None?
        fred.get_series()







if __name__ == "__main__":
    main()

