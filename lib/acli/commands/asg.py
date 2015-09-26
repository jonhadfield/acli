"""Usage:
    acli asg list [options]
    acli asg (info | cpu | mem | net) <asg_name> [options]

    -s, --start=<start_date>        metrics start-date
    -e, --end=<end_date>            metrics end-date
    -p, --period<period>            metrics period
    -i, --intervals=<intervals>     metrics intervals
    -o, --output=<output_type>      table, json, yaml or graph [default: table].
    -h, --help
"""
from docopt import docopt

if __name__ == '__main__':
    print(docopt(__doc__))