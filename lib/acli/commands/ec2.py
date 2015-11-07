# -*- coding: utf-8 -*-
"""Usage:
    acli ec2 (list | summary) [options] [--region=<region>]
    acli ec2 (start | stop | reboot | terminate | info | cpu | vols | net) <instance_id> [options]

    -s, --start=<start_date>        metrics start-date
    -e, --end=<end_date>            metrics end-date
    -p, --period=<period>            metrics period
    -i, --intervals=<intervals>     metrics intervals
    -h, --help
"""
from __future__ import (absolute_import, print_function, unicode_literals)
from docopt import docopt

if __name__ == '__main__':
    print(docopt(__doc__))
