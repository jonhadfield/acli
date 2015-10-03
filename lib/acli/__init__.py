#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
usage: acli [--version] [--help]
            <command> [<args>...]
       acli account
       acli ec2 list [options]
       acli ec2 (start | stop | reboot | terminate | info | cpu | vols | net) <instance_id> [options]
       acli lc list [options]
       acli asg list [options]
       acli asg (info | cpu | mem | net) <asg_name> [options]
       acli ami (list | info <ami_id>)
       acli elb (list | info <elb_name>)
options:
   -h, --help  help

The most common commands are:
   account      Get account info
   ec2          Manage ec2 instances
   elb          Manage elb instances
   ami          Manage amis
   asg          Manage auto-scaling groups
   lc           Manage launch configurations
   eip          Manage elastic ips
   secgroup     Manage security groups
   route53      Manage route 53 configuration

See 'acli help <command>'
"""

from __future__ import (absolute_import, print_function, unicode_literals)
from docopt import docopt
from colorama import init
from acli.services import (ec2, elb, account,
                           cloudwatch, asg, route53)
from acli.config import Config
from acli import utils
init(autoreset=True)


def real_main():
    args = docopt(__doc__,
                  version='0.0.1',
                  options_first=True)
    aws_config = Config(args)
    argv = [args['<command>']] + args['<args>']

    if args['<command>'] == 'account':
        from acli.commands import account as command_account
        # acc_res = docopt(command_account.__doc__, argv=argv)
        account.account_info(aws_config)
    if args['<command>'] == 'ec2':
        from acli.commands import ec2 as command_ec2
        ec2_res = docopt(command_ec2.__doc__, argv=argv)
        if ec2_res.get('list'):
            ec2.ec2_list(aws_config)
        elif ec2_res.get('info'):
            ec2.ec2_info(aws_config, instance_id=ec2_res.get('<instance_id>'))
        elif ec2_res.get('stop'):
            ec2.ec2_manage(aws_config, instance_id=ec2_res.get('<instance_id>'), action="stop")
        elif ec2_res.get('reboot'):
            ec2.ec2_manage(aws_config, instance_id=ec2_res.get('<instance_id>'), action="reboot")
        elif ec2_res.get('start'):
            ec2.ec2_manage(aws_config, instance_id=ec2_res.get('<instance_id>'), action="start")
        elif ec2_res.get('terminate'):
            ec2.ec2_manage(aws_config, instance_id=ec2_res.get('<instance_id>'), action="terminate")
        elif ec2_res.get('cpu'):
            cloudwatch.ec2_cpu(aws_config=aws_config, instance_id=ec2_res.get('<instance_id>'))
        elif ec2_res.get('net'):
            cloudwatch.ec2_net(aws_config=aws_config,
                               instance_id=ec2_res.get('<instance_id>'),
                               output_type=ec2_res.get('--output', None),
                               start=ec2_res.get('--start', None),
                               period=ec2_res.get('--end', None),
                               intervals=ec2_res.get('intervals', None)
                               )
        elif ec2_res.get('vols'):
            cloudwatch.ec2_vol(aws_config=aws_config,
                               instance_id=ec2_res.get('<instance_id>'),
                               output_type=ec2_res.get('--output', None),
                               start=ec2_res.get('--start', None),
                               period=ec2_res.get('--end', None),
                               intervals=ec2_res.get('intervals', None)
                               )
    if args['<command>'] == 'elb':
        from acli.commands import elb as command_elb
        elb_res = docopt(command_elb.__doc__, argv=argv)
        if elb_res.get('list'):
            elb.elb_list(aws_config)
        elif elb_res.get('info'):
            elb.elb_info(aws_config, elb_name=elb_res.get('<elb_name>'))
    if args['<command>'] == 'lc':
        from acli.commands import lc as command_lc
        lc_res = docopt(command_lc.__doc__, argv=argv)
        if lc_res.get('list'):
            asg.lc_list(aws_config)
        elif lc_res.get('info'):
            asg.lc_info(aws_config, lc_name=lc_res.get('<lc_name>'))
    if args['<command>'] == 'asg':
        from acli.commands import asg as command_asg
        asg_res = docopt(command_asg.__doc__, argv=argv)
        if asg_res.get('list'):
            asg.asg_list(aws_config)
        elif asg_res.get('info'):
            asg.asg_info(aws_config, asg_name=asg_res.get('<asg_name>'))
        elif asg_res.get('cpu'):
            cloudwatch.asg_cpu(aws_config=aws_config,
                               asg_name=asg_res.get('<asg_name>'),
                               output_type=asg_res.get('--output', None),
                               start=asg_res.get('--start'),
                               period=asg_res.get('--end'),
                               intervals=asg_res.get('intervals')
                               )
    if args['<command>'] == 'ami':
        from acli.commands import ami as command_ami
        ami_res = docopt(command_ami.__doc__, argv=argv)
        if ami_res.get('list'):
            ec2.ami_list(aws_config)
        elif ami_res.get('info'):
            ec2.ami_info(aws_config, ami_id=ami_res.get('<ami_id>'))
    if args['<command>'] == 'route53':
        from acli.commands import route53 as command_route53
        route53_res = docopt(command_route53.__doc__, argv=argv)
        if route53_res.get('list'):
            route53.route53_list(aws_config)
        elif route53_res.get('info'):
            route53.route53_info(aws_config, instance_id=route53_res.get('<zone>'))

    elif args['<command>'] in ['help', None] and args['<args>']:
        if args['<args>'][0] == 'ec2':
            from acli.commands import ec2 as command_ec2
            print(docopt(command_ec2.__doc__, argv=argv))
    elif args['<command>'] in ['help', None] and not args['<args>']:
        print("usage: acli help <command>")
    else:
        exit("%r is not an acli command. See 'acli --help'." % args['<command>'])
