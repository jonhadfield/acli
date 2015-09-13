#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""acli.

Usage:
  acli ec2 list
  acli ec2 info <instance_id>
  acli elb list
  acli elb info <elb_name>
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
from acli.output import (output_ec2_list, output_ec2_info, output_elbs, output_elb_info)
init(autoreset=True)


def real_main():
    args = docopt(__doc__, version='0.0.1')
    aws_config = Config(args)
    if args.get('ec2'):
        if args.get('list'):
            output_ec2_list(
                output_media='console',
                instances=ec2.get_ec2_list(aws_config))
        if args.get('info'):
            if args.get('<instance_id>'):
                output_ec2_info(output_media='console',
                                instance=ec2.get_ec2_instance(aws_config,
                                                              instance_id=args.get('<instance_id>')))

    if args.get('elb'):
        if args.get('list'):
            output_elbs(
                output_media='console',
                elbs=elb.get_elb_list(aws_config))
        if args.get('info'):
            if args.get('<elb_name>'):
                output_elb_info(output_media='console',
                                elb=elb.get_elb(aws_config,
                                                elb_name=args.get('<elb_name>')))

