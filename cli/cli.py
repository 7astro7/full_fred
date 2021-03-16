"""
A CLI for fredapi

Usage:
    fred-cli (-h | --help)
    fred-cli configure
    fred-cli series 
    fred-cli examples

Options:
    -i --id             Use series_id --id.
    --plot              Display matplotlib line plot of series.
    --save OUTFILE      Save series as OUTFILE.csv, add JSON option

Commands:
    series              Fetch series.
    search              Do a full-text search for a series.
    search-release      Search for series that belongs to a release id.
    search-category     Search for series that belongs to a category id.
    configure           ---
    examples            Print example commands.
"""


from fredapi import Fred
from docopt import docopt
import sys

# use docopt to parse command-line arguments
# add tests for each module
# logging?
# set up configuration
# caching data
# man pages?
# generate fredapi docs in this module so docopt has something to map cli arguments to fredapi parameters with

fred = Fred()

def main():
    """
    Main function
    """
    try:
        cli()
    except KeyboardInterrupt:
        print("Quitting...")
        sys.exit(1)

def cli():
    """
    Run command sent as user input
    """

    args = docopt(__doc__, version = '0.01')

    if args.get("search"):
        fred.search()

    elif args.get("series"):
        if not (args.get("-i") or args.get("--id")):
            while True:
                user_choice = input(
                "No series_id passed. Specify one now or press q to quit."
                ).lower().strip()
                if user_choice == "q":
                    sys.exit(0)
                    # return None?
        fred.get_series()



# make setup.cfg




if __name__ == "__main__":
    main()

