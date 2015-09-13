#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""acli.

Usage:
  acli ec2 (list | info | search)
  acli elb (list | info | search)
  acli --version

Options:
  -h --help                             show this help message and exit
  -r --region=REGION                    set aws region
  --access_key_id=ACCESS_KEY_ID         set access key id
  --secret_access_id=SECRET_ACCESS_KEY  set secret access key
  --version                             show version and exit
"""

from __future__ import (absolute_import, print_function)

from docopt import docopt
from colorama import init
from acli.services import (ec2, elb)
from acli.config import Config
init(autoreset=True)


def real_main():
    args = docopt(__doc__, version='0.0.1')
    print(args)
    aws_config = Config()
    aws_config.load_config(args)

    if args.get('ec2'):
        ec2.get_ec2_list(aws_config)

    if args.get('elb'):
        elb.get_elb_list(aws_config)