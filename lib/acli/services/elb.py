# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)
import boto.ec2.elb
from acli.output.elb import output_elbs, output_elb_info
from acli.connections import get_elb_conn


def get_elb_list(aws_config):
    """
    @type aws_config: Config
    """
    elb_conn = get_elb_conn(aws_config)
    return [elb for elb in elb_conn.get_all_load_balancers()]


def get_elb(aws_config, elb_name=None):
    """
    @type aws_config: Config
    @type elb_name: unicode
    """
    if elb_name:
        elb_conn = get_elb_conn(aws_config)
        return elb_conn.get_all_load_balancers(load_balancer_names=[elb_name])


def elb_list(aws_config):
    """
    @type aws_config: Config
    """
    output_elbs(
                output_media='console',
                elbs=get_elb_list(aws_config))


def elb_info(aws_config=None, elb_name=None):
    """
    @type aws_config: Config
    @type elb_name: unicode
    """
    output_elb_info(output_media='console',
                    elb=get_elb(aws_config,
                                elb_name=elb_name))
