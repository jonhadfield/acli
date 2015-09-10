#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""acli.

Usage:
  acli ec2 [--list] [--region=REGION]
  acli elb [--list]
  acli --version

Options:
  -h --help                    show this help message and exit
  -l --list                    list resources
  -r --region=REGION           aws region to connect to
  --version                    show version and exit
"""

from __future__ import print_function
from docopt import docopt
import boto.ec2
import os
from colorama import Fore, init
import acli.ec2
init(autoreset=True)


def get_ec2_conn(region):
    return boto.ec2.connect_to_region(region,
           aws_access_key_id=os.environ.get('AWS_ACCESS_KEY', None),
           aws_secret_access_key=os.environ.get('AWS_SECRET_KEY', None))


def real_main():
    """ The function called from the script

    :return: None
    """
    arguments = docopt(__doc__, version='0.0.1')
    print(arguments)
    region = arguments.get('--region')
    if arguments.get('ec2'):
        conn = get_ec2_conn(region)
        for instance in conn.get_all_instances():
            print(instance)

if __name__ == '__main__':
    real_main()
