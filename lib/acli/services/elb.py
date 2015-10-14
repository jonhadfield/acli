# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)
from acli.output.elb import output_elbs, output_elb_info
from acli.connections import get_boto3_session


def get_elb_list(aws_config):
    """
    @type aws_config: Config
    """
    session = get_boto3_session(aws_config)
    elb_conn = session.client('elb')
    elbs = elb_conn.describe_load_balancers().get('LoadBalancerDescriptions')
    return elbs


def get_elb(aws_config, elb_name=None):
    """
    @type aws_config: Config
    @type elb_name: unicode
    """
    if elb_name:
        session = get_boto3_session(aws_config)
        elb_conn = session.client('elb')
        return elb_conn.describe_load_balancers(LoadBalancerNames=[elb_name])


def elb_list(aws_config):
    """
    @type aws_config: Config
    """
    output_elbs(output_media='console',
                elbs=get_elb_list(aws_config))


def elb_info(aws_config=None, elb_name=None):
    """
    @type aws_config: Config
    @type elb_name: unicode
    """
    output_elb_info(output_media='console',
                    elb=get_elb(aws_config,
                                elb_name=elb_name))
