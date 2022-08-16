import argparse
from urllib.error import URLError
url:str
limit:int
verb=False
jtype=False
def arguments() -> None:
    """Arguments for this peace of software:
        URL a mandatory arg for source url
        --version - programm version
        --json - returns output in JSON format
        --verbose - adds some spice verbose
        --limit - the amount of topics to show"""
    parser = argparse.ArgumentParser()
    parser.add_argument('URL', metavar='source', action='store', type=str,
                        help='RSS URL')
    parser.add_argument('--version', action='version',
                        version='Fancy RSS reader: version 0.1', help='Print version info')
    parser.add_argument('--json', action='store_true',
                        help='Print result as JSON in stdout')
    parser.add_argument('--verbose', action='store_true',
                        help='Outputs verbose status messages')
    parser.add_argument('--limit', metavar='LIMIT', action='store', type=int,
                        help='Limit news topics if this parameter provided')
    args = parser.parse_args()
    global url
    url=args.URL
    global limit
    limit=args.limit
    if args.json:
        global jtype
        jtype = True
    if args.verbose:
        global verb
        verb = True
        print('Verbose turned on!')