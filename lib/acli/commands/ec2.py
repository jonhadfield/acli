# -*- coding: utf-8 -*-
"""Usage:
    acli ec2 (ls | list | summary) [options] [--region=<region>]
    acli ec2 (start | stop | reboot | terminate | info | cpu | vols | net) <instance_id> [options]

    -f, --filter=<term>             filter results by term
    -s, --start=<start_date>        metrics start-date
    -e, --end=<end_date>            metrics end-date
    -p, --period=<period>           metrics period
    -i, --intervals=<intervals>     metrics intervals
    -h, --help
"""
from __future__ import (absolute_import, print_function, unicode_literals)
from docopt import docopt
from acli.services import (ec2, cloudwatch)


def ec2_command(argv=None, aws_config=None):
    ec2_res = docopt(__doc__, argv=argv)
    if any((ec2_res.get('ls'), ec2_res.get('list'))):
        ec2.ec2_list(aws_config, filter_term=ec2_res.get('--filter'))
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

if __name__ == '__main__':
    print(docopt(__doc__))
