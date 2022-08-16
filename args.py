import argparse

def arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', action='version',
                        version='%(prog)s 1.0', help='Print version info')
    parser.add_argument('--limit', metavar='N', type=int,
                        help='Limit news topics if this parameter provided')
    args = parser.parse_args()