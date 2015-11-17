#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
usage: acli [--version] [--help] [--install-completion]
       acli [--region=<region>] [--access_key_id=<access_key_id>] [--secret_access_key=<secret_access_key>]
            <command> [<args>...]
       acli account [options]
       acli ec2 (list | summary) [options]
       acli ec2 (start | stop | reboot | terminate | info | cpu | vols | net) <instance_id> [options]
       acli lc list [options]
       acli asg list [options]
       acli asg (info | cpu | mem | net | delete) <asg_name> [options]
       acli ami (list | info <ami_id>)
       acli eip (list | info <eip>)
       acli elb (list | info <elb_name>)
       acli route53 (list | info <zone_id>)
       acli vpc (list | info <vpc_id>)
       acli secgroup (list | info)
       acli s3 list [<item>]
       acli s3 info <item>

options:
   -h, --help      help

The most common commands are:
   account      Get account info
   ec2          Manage ec2 instances
   eip          Manage elastic IPs
   elb          Manage elb instances
   ami          Manage amis
   asg          Manage auto-scaling groups
   lc           Manage launch configurations
   eip          Manage elastic ips
   secgroup     Manage security groups
   route53      Manage route 53 configuration
   vpc          Manage VPCs
   secgroup     Manage Security Groups
   s3           Manage S3 storage
See 'acli help <command>'
"""

from __future__ import (absolute_import,
                        print_function,
                        unicode_literals)
from docopt import docopt
from acli.services import (ec2, elb, account, cloudwatch, vpc,
                           eip, asg, route53, secgroup, s3)
from acli.config import Config
from acli.utils import install_completion


def ec2_command(argv=None, aws_config=None):
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
                           start=ec2_res.get('--start'),
                           period=ec2_res.get('--end'),
                           intervals=ec2_res.get('intervals')
                           )
    elif ec2_res.get('vols'):
        cloudwatch.ec2_vol(aws_config=aws_config,
                           instance_id=ec2_res.get('<instance_id>'),
                           start=ec2_res.get('--start'),
                           period=ec2_res.get('--end'),
                           intervals=ec2_res.get('intervals')
                           )
    elif ec2_res.get('summary'):
        ec2.ec2_summary(aws_config=aws_config)


def elb_command(argv=None, aws_config=None):
    from acli.commands import elb as command_elb
    elb_res = docopt(command_elb.__doc__, argv=argv)
    if elb_res.get('list'):
        elb.elb_list(aws_config)
    elif elb_res.get('info'):
        elb.elb_info(aws_config, elb_name=elb_res.get('<elb_name>'))


def ami_command(argv=None, aws_config=None):
    from acli.commands import ami as command_ami
    ami_res = docopt(command_ami.__doc__, argv=argv)
    if ami_res.get('list'):
        ec2.ami_list(aws_config)
    elif ami_res.get('info'):
        ec2.ami_info(aws_config, ami_id=ami_res.get('<ami_id>'))


def lc_command(argv=None, aws_config=None):
    from acli.commands import lc as command_lc
    lc_res = docopt(command_lc.__doc__, argv=argv)
    if lc_res.get('list'):
        asg.lc_list(aws_config)
    elif lc_res.get('info'):
        asg.lc_info(aws_config, lc_name=lc_res.get('<lc_name>'))


def asg_command(argv=None, aws_config=None):
    from acli.commands import asg as command_asg
    asg_res = docopt(command_asg.__doc__, argv=argv)
    if asg_res.get('list'):
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


def route53_command(argv=None, aws_config=None):
    from acli.commands import route53 as command_route53
    route53_res = docopt(command_route53.__doc__, argv=argv)
    if route53_res.get('list'):
        route53.route53_list(aws_config)
    elif route53_res.get('info'):
        route53.route53_info(aws_config, zone_id=route53_res.get('<zone_id>'))


def vpc_command(argv=None, aws_config=None):
    from acli.commands import vpc as command_vpc
    vpc_res = docopt(command_vpc.__doc__, argv=argv)
    if vpc_res.get('list'):
        vpc.vpc_list(aws_config)
    elif vpc_res.get('info'):
        vpc.vpc_info(aws_config, vpc_id=vpc_res.get('<vpc_id>'))


def secgroup_command(argv=None, aws_config=None):
    from acli.commands import secgroup as command_secgroup
    secgroup_res = docopt(command_secgroup.__doc__, argv=argv)
    if secgroup_res.get('list'):
        secgroup.secgroup_list(aws_config)
    elif secgroup_res.get('info'):
        secgroup.secgroup_info(aws_config, secgroup_id=secgroup_res.get('<secgroup_id>'))


def eip_command(argv=None, aws_config=None):
    from acli.commands import eip as command_eip
    eip_res = docopt(command_eip.__doc__, argv=argv)
    if eip_res.get('list'):
        eip.eip_list(aws_config)
    elif eip_res.get('info'):
        eip.eip_info(aws_config, eip=eip_res.get('<eip>'))


def s3_command(argv=None, aws_config=None):
    from acli.commands import s3 as command_s3
    s3_res = docopt(command_s3.__doc__, argv=argv)
    if s3_res.get('list'):
        path = s3_res.get('<item>')
        if path and not '/' == path[-1:]:
            path += '/'
        s3.s3_list(aws_config, item=path)
    elif s3_res.get('info'):
        s3.s3_info(aws_config, item=s3_res.get('<item>'))


def real_main():
    args = docopt(__doc__,
                  version='0.1.14',
                  options_first=True)
    aws_config = Config(args)
    argv = [args['<command>']] + args['<args>']
    if args['--install-completion']:
        install_completion()
    elif args['<command>'] == 'account':
        account.account_info(aws_config)
    elif args['<command>'] == 'ec2':
        ec2_command(argv=argv, aws_config=aws_config)
    elif args['<command>'] == 'elb':
        elb_command(argv=argv, aws_config=aws_config)
    elif args['<command>'] == 'lc':
        lc_command(argv=argv, aws_config=aws_config)
    elif args['<command>'] == 'asg':
        asg_command(argv=argv, aws_config=aws_config)
    elif args['<command>'] == 'ami':
        ami_command(argv=argv, aws_config=aws_config)
    elif args['<command>'] == 'route53':
        route53_command(argv=argv, aws_config=aws_config)
    elif args['<command>'] == 'vpc':
        vpc_command(argv=argv, aws_config=aws_config)
    elif args['<command>'] == 'secgroup':
        secgroup_command(argv=argv, aws_config=aws_config)
    elif args['<command>'] == 'eip':
        eip_command(argv=argv, aws_config=aws_config)
    elif args['<command>'] == 's3':
        s3_command(argv=argv, aws_config=aws_config)
    elif args['<command>'] in ['help', None] and not args['<args>']:
        print("usage: acli help <command>")
    else:
        exit("{0} is not an acli command. See 'acli --help'.".format(args['<command>']))
