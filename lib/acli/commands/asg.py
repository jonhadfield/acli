"""usage: acli asg (list | info <asg_name> | stats <asg_name>)

    -h, --help
"""
from docopt import docopt

if __name__ == '__main__':
    print(docopt(__doc__))
