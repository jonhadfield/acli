#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
usage: acli [--version] [--help] [--install-completion]
       acli [--region=<region>] [--access_key_id=<access_key_id>] [--secret_access_key=<secret_access_key>]
            <command> [<args>...]
       acli account [options]
       acli ec2 (ls | list | summary) [options]
       acli ec2 (start | stop | reboot | terminate | info | cpu | vols | net) <instance_id> [options]
       acli lc (ls | list) [options]
       acli asg (ls | list) [options]
       acli asg (info | cpu | mem | net | delete) <asg_name> [options]
       acli ami (ls | list) info <ami_id>
       acli ami info <ami_id>
       acli eip ([ls | list]| info <eip>)
       acli eip (ls | list)
       acli elb (ls | list)
       acli elb info <elb_name>
       acli route53 (ls | list)
       acli route53 info <zone_id>
       acli vpc (ls | list)
       acli vpc info <vpc_id>
       acli secgroup (ls | list)
       acli secgroup info <secgroup_id>
       acli s3 (ls | list) [<item>]
       acli s3 info [<item>]
       acli s3 cp <source> <dest>
       acli s3 (del | rm) <item>
       acli es (ls | list)
       acli es info <domain>
       acli efs (ls | list) [options]
       acli clean (delete_orphaned_snapshots | delete_unnammed_volumes)


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
   es           Manage Elasticsearch
   efs          Manage Elastic file systems
   clean        Tools for reporting on and removing unused service items
See 'acli <command> -h'
"""

from __future__ import (absolute_import,
                        print_function,
                        unicode_literals)

from docopt import docopt

from acli.commands.asg import asg_command
from acli.commands.ec2 import ec2_command
from acli.config import Config
from acli.services import (ec2, elb, account, vpc, eip, asg,
                           route53, secgroup, s3, es, clean, efs)
from acli.utils import install_completion


def elb_command(argv=None, aws_config=None):
    from acli.commands import elb as command_elb
    elb_res = docopt(command_elb.__doc__, argv=argv)
    if any((elb_res.get('ls'), elb_res.get('list'))):
        elb.elb_list(aws_config)
    elif elb_res.get('info'):
        elb.elb_info(aws_config, elb_name=elb_res.get('<elb_name>'))


def ami_command(argv=None, aws_config=None):
    from acli.commands import ami as command_ami
    ami_res = docopt(command_ami.__doc__, argv=argv)
    if any((ami_res.get('ls'), ami_res.get('list'))):
        ec2.ami_list(aws_config, filter_term=ami_res.get('--filter'))
    elif ami_res.get('info'):
        ec2.ami_info(aws_config, ami_id=ami_res.get('<ami_id>'))


def lc_command(argv=None, aws_config=None):
    from acli.commands import lc as command_lc
    lc_res = docopt(command_lc.__doc__, argv=argv)
    if any((lc_res.get('ls'), lc_res.get('list'))):
        asg.lc_list(aws_config)
    elif lc_res.get('info'):
        asg.lc_info(aws_config, lc_name=lc_res.get('<lc_name>'))


def route53_command(argv=None, aws_config=None):
    from acli.commands import route53 as command_route53
    route53_res = docopt(command_route53.__doc__, argv=argv)
    if any((route53_res.get('ls'), route53_res.get('list'))):
        route53.route53_list(aws_config)
    elif route53_res.get('info'):
        route53.route53_info(aws_config, zone_id=route53_res.get('<zone_id>'))


def vpc_command(argv=None, aws_config=None):
    from acli.commands import vpc as command_vpc
    vpc_res = docopt(command_vpc.__doc__, argv=argv)
    if any((vpc_res.get('ls'), vpc_res.get('list'))):
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
    if any((eip_res.get('ls'), eip_res.get('list'))):
        eip.eip_list(aws_config)
    elif eip_res.get('info'):
        eip.eip_info(aws_config, eip=eip_res.get('<eip>'))


def s3_command(argv=None, aws_config=None):
    from acli.commands import s3 as command_s3
    s3_res = docopt(command_s3.__doc__, argv=argv)
    if any((s3_res.get('ls'), s3_res.get('list'))):
        path = s3_res.get('<item>')
        if path and not '/' == path[-1:]:
            path += '/'
        s3.s3_list(aws_config, item=path)
    elif s3_res.get('info'):
        s3.s3_info(aws_config, item=s3_res.get('<item>'))
    elif s3_res.get('cp'):
        s3.s3_cp(aws_config, source=s3_res.get('<source>'), dest=s3_res.get('<dest>'))
    elif any((s3_res.get('rm'), s3_res.get('del'))):
        s3.s3_rm(aws_config, item=s3_res.get('<item>'))


def es_command(argv=None, aws_config=None):
    from acli.commands import es as command_es
    es_res = docopt(command_es.__doc__, argv=argv)
    if any((es_res.get('ls'), es_res.get('list'))):
        es.es_list(aws_config)
    elif es_res.get('info'):
        es.es_info(aws_config, domain_name=es_res.get('<domain>'))


def efs_command(argv=None, aws_config=None):
    from acli.commands import efs as command_efs
    efs_res = docopt(command_efs.__doc__, argv=argv)
    if any((efs_res.get('ls'), efs_res.get('list'))):
        efs.efs_list(aws_config)
    elif efs_res.get('info'):
        efs.efs_info(aws_config, domain_name=efs_res.get('<filesystem_id>'))


def clean_command(argv=None, aws_config=None):
    from acli.commands import clean as command_clean
    clean_res = docopt(command_clean.__doc__, argv=argv)
    if clean_res.get('delete_orphaned_snapshots'):
        clean.delete_orphaned_snapshots(aws_config=aws_config, noop=clean_res.get('--noop'))
    elif clean_res.get('delete_unnamed_volumes'):
        clean.delete_unnamed_volumes(aws_config=aws_config, noop=clean_res.get('--noop'))


def real_main():
    args = docopt(__doc__,
                  version='0.1.30',
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
    elif args['<command>'] == 'es':
        es_command(argv=argv, aws_config=aws_config)
    elif args['<command>'] == 'efs':
        efs_command(argv=argv, aws_config=aws_config)
    elif args['<command>'] == 'clean':
        clean_command(argv=argv, aws_config=aws_config)
    elif args['<command>'] in ['help'] and not args['<args>']:
        print("usage: acli <command> -h")
    elif args['<command>']:
        exit("{0} is not an acli command. See 'acli -h'.".format(args['<command>']))
    else:
        print(__doc__)
