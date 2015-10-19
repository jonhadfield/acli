# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)
from acli.output.secgroup import (output_secgroup_list, output_secgroup_info)
from acli.connections import get_boto3_session, get_client


def secgroup_list(aws_config=None):
    """
    @type aws_config: Config
    """
    ec2_client = get_client(client_type='ec2', config=aws_config)
    secgroups = ec2_client.describe_security_groups()
    output_secgroup_list(output_media='console', secgroups=secgroups)


def secgroup_info(aws_config=None, secgroup_id=None):
    """
    @type aws_config: Config
    @type secgroup_id: unicode
    """
    session = get_boto3_session(aws_config)
    conn = session.resource('ec2')
    secgroup = conn.SecurityGroup(secgroup_id)
    if hasattr(secgroup, 'group_id'):
        output_secgroup_info(output_media='console', secgroup=secgroup)
    else:
        exit("Cannot find security group: {0}.".format(secgroup_id))
