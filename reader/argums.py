import argparse
import logging
import warnings
import sys
url:str
limit=None
verb=False
jtype=False
date=None
def arguments() -> None:
    """Arguments for this peace of software:
        URL a mandatory arg for source url
        --version - programm version
        --json - returns output in JSON format
        --verbose - adds some spicy verbose
        --limit - the amount of topics to show"""
    parser = argparse.ArgumentParser()
    parser.add_argument('URL', metavar='source', nargs='?', action='store', type=str,
                        help='RSS URL')
    parser.add_argument('--version', action='version',
                        version='Fancy RSS reader: version 0.4', help='Print version info')
    parser.add_argument('--json', action='store_true',
                        help='Print result as JSON in stdout')
    parser.add_argument('--verbose', action='store_true',
                        help='Outputs verbose status messages')
    parser.add_argument('--limit', metavar='LIMIT', action='store', type=int,
                        help='Limit news topics if this parameter provided')
    parser.add_argument('--date', metavar='DATE', action='store', type=str,
                        help='Provides cached items with corresponding date')
    args = parser.parse_args()
    global url
    url=args.URL
    global limit
    limit=args.limit
    if args.date:
        global date
        date=args.date
    if args.json:
        global jtype
        jtype = True
    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    else:
        warnings.filterwarnings("ignore", category=UserWarning, module='bs4')