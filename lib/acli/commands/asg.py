# -*- coding: utf-8 -*-
"""Usage:
    acli asg (ls | list) [options]
    acli asg  info <asg_name> [options]
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
from acli.services import (cloudwatch, asg)


def asg_command(argv=None, aws_config=None):
    asg_res = docopt(__doc__, argv=argv)
    if any((asg_res.get('ls'), asg_res.get('list'))):
        asg.asg_list(aws_config)
    elif asg_res.get('info'):
        asg.asg_info(aws_config, asg_name=asg_res.get('<asg_name>'))
    elif asg_res.get('cpu'):
        cloudwatch.asg_cpu(aws_config=aws_config,
                           asg_name=asg_res.get('<asg_name>'),
                           output_type=asg_res.get('--output'),
                           start=asg_res.get('--start'),
                           period=asg_res.get('--end'),
                           intervals=asg_res.get('intervals')
                           )
    elif asg_res.get('delete'):
        asg.asg_delete(aws_config, asg_name=asg_res.get('<asg_name>'))


if __name__ == '__main__':
    print(docopt(__doc__))
