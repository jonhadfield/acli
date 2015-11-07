# -*- coding: utf-8 -*-
"""Usage:
    acli asg (list | info <asg_name>) [options]
    acli asg (cpu | mem | net | delete) <asg_name> [options]
    -s, --start=<start_date>        metrics start-date
    -e, --end=<end_date>            metrics end-date
    -p, --period<period>            metrics period
    -i, --intervals=<intervals>     metrics intervals
    -o, --output=<output_type>      table, json, yaml or graph [default: graph].
    -h, --help
"""
from __future__ import (absolute_import, print_function, unicode_literals)
from docopt import docopt
if __name__ == '__main__':
    print(docopt(__doc__))
