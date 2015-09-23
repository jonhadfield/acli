"""Usage:
    acli ec2 list [options]
    acli ec2 (start | stop | reboot | terminate | info | cpu | mem | net) <instance_id> [options]

    -s, --start=<start_date>        metrics start-date
    -e, --end=<end_date>            metrics end-date
    -o, --output=<output_type>      table, json, yaml or graph [default: table].
    -h, --help
"""
from docopt import docopt

if __name__ == '__main__':
    print(docopt(__doc__))
