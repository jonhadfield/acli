# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)
from acli.output.vpc import (output_vpc_list, output_vpc_info)
from acli.connections import get_boto3_session


def vpc_list(aws_config=None):
    """
    @type aws_config: Config
    """
    session = get_boto3_session(aws_config)
    conn = session.client('ec2')
    vpcs = conn.describe_vpcs()
    if vpcs.get('Vpcs', None):
        output_vpc_list(output_media='console', vpcs=vpcs)
    else:
        exit("No VPCs found.")


def vpc_info(aws_config=None, vpc_id=None):
    """
    @type aws_config: Config
    @type vpc_id: unicode
    """
    session = get_boto3_session(aws_config)
    conn = session.resource('ec2')
    vpc = conn.Vpc(vpc_id)
    if hasattr(vpc, 'cidr_block'):
        subnets = vpc.subnets.all()
        output_vpc_info(output_media='console', vpc=vpc, subnets=subnets)
    else:
        exit("Cannot find VPC: {0}.".format(vpc_id))
