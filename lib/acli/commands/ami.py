"""Usage:
    acli ami (list | info <ami_id>)

    -h, --help
"""
from docopt import docopt

if __name__ == '__main__':
    print(docopt(__doc__))
