"""usage: acli elb (list | info <elb_name>)

    -h, --help
"""
from docopt import docopt

if __name__ == '__main__':
    print(docopt(__doc__))
