#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""acli.

Usage:
  acli ec2 (list | info | search)
  acli elb (list | info | search)
  acli --version

Options:
  -h --help                    show this help message and exit
  -l --list                    list resources
  -r --region=REGION           aws region to connect to
  --version                    show version and exit
"""

from __future__ import print_function

from docopt import docopt
from colorama import init
from services import (ec2, elb)
init(autoreset=True)


def real_main():
    """ The function called from the script

    :return: None
    """
    arguments = docopt(__doc__, version='0.0.1')
    print(arguments)
    chosen_aws_region = arguments.get('--region')
    if not chosen_aws_region:
        region = 'eu-west-1'
    else:
        region = chosen_aws_region

    if arguments.get('ec2'):
        conn = ec2.get_ec2_conn(region)
        print(conn)
        for instance in conn.get_all_instances():
            print(instance)

    if arguments.get('elb'):
        conn = elb.get_elb_conn(region)
        print(conn)
        for instance in conn.get_all_load_balancers():
            print(instance)

if __name__ == '__main__':
    real_main()
