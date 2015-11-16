# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)
from acli.output.secgroup import (output_secgroup_list, output_secgroup_info)
from acli.connections import get_client
from botocore.exceptions import ClientError


def secgroup_list(aws_config=None):
    """
    @type aws_config: Config
    """
    ec2_client = get_client(client_type='ec2', config=aws_config)
    secgroups = ec2_client.describe_security_groups()
    output_secgroup_list(secgroups=secgroups)


def secgroup_info(aws_config=None, secgroup_id=None):
    """
    @type aws_config: Config
    @type secgroup_id: unicode
    """
    ec2_client = get_client(client_type='ec2', config=aws_config)
    try:
        result = ec2_client.describe_security_groups(GroupIds=[secgroup_id])
        secgroups = result.get('SecurityGroups')
        secgroup = secgroups[0]
        output_secgroup_info(secgroup=secgroup)
    except (ClientError, IndexError):
        exit("Cannot find security group: {0}.".format(secgroup_id))
