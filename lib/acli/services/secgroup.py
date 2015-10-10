# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)
from boto3.session import Session
from acli.output.secgroup import (output_secgroup_list, output_secgroup_info)
# import botocore.exceptions


def get_boto3_session(aws_config):
    """
    @type aws_config: Config
    """
    return Session(region_name=aws_config.region,
                   aws_access_key_id=aws_config.access_key_id,
                   aws_secret_access_key=aws_config.secret_access_key)


def secgroup_list(aws_config=None):
    """
    @type aws_config: Config
    """
    session = get_boto3_session(aws_config)
    conn = session.client('ec2')
    secgroups = conn.describe_security_groups()
    if secgroups:
        output_secgroup_list(output_media='console', secgroups=secgroups)
    else:
        exit("No security groups found.")


def secgroup_info(aws_config=None, secgroup_id=None):
    """
    @type aws_config: Config
    @type secgroup_id: unicode
    """
    session = get_boto3_session(aws_config)
    conn = session.resource('ec2')
    secgroup = conn.SecurityGroup(secgroup_id)
    if secgroup:
        output_secgroup_info(output_media='console', secgroup=secgroup)
    else:
        exit("Cannot find security group: {0}.".format(secgroup_id))
