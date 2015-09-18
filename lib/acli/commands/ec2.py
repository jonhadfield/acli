"""usage: acli ec2 (list | info <instance_id> | stats <instance_id>)

    -h, --help
"""
from docopt import docopt

if __name__ == '__main__':
    print(docopt(__doc__))
