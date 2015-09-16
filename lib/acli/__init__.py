#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""acli.

Usage:
  acli account
  acli ec2 list
  acli ec2 info <instance_id>
  acli ec2 stats <instance_id>
  acli elb list
  acli elb info <elb_name>
  acli ami list
  acli ami info <ami_id>
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
from acli.services import (ec2, elb, account, cloudwatch)
from acli.config import Config
from acli.output.ec2 import (output_ec2_list, output_ec2_info,
                             output_amis, output_ami_info)
from acli.output.cloudwatch import output_ec2_stats
from acli.output.elb import (output_elbs, output_elb_info)
init(autoreset=True)


def real_main():
    args = docopt(__doc__, version='0.0.1')
    aws_config = Config(args)

    if args.get('account'):
        iam_conn = account.get_iam_conn(aws_config)
        print("alias: {0} | id: {1}".format(", ".join(account.get_account_aliases(iam_conn)),
                                            account.get_account_id(iam_conn)))

    if args.get('ec2'):
        if args.get('list'):
            ec2.ec2_list(aws_config)
        if args.get('info'):
            ec2.ec2_info(aws_config, instance_id=args.get('<instance_id>'))

        if args.get('stats'):
            ec2.ec2_stats(aws_config=aws_config, instance_id=args.get('<instance_id>'))
            output_ec2_stats(output_media='console',
                             instance=ec2.get_ec2_instance(aws_config,
                                                           instance_id=args.get('<instance_id>')),
                             cpu_stats=cloudwatch.get_ec2_cpu_stats(aws_config=aws_config,
                                                                    instance_id=args.get('<instance_id>')),
                             network_stats=cloudwatch.get_ec2_network_stats(aws_config=aws_config,
                                                                            instance_id=args.get('<instance_id>'))
                             )

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

    if args.get('ami'):
        if args.get('list'):
            output_amis(
                output_media='console',
                amis=ec2.get_ami_list(aws_config))
        if args.get('info'):
            if args.get('<ami_id>'):
                output_ami_info(output_media='console',
                                ami=ec2.get_ami(aws_config,
                                                ami_id=args.get('<ami_id>')))
