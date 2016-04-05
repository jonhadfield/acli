# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)

import botocore.exceptions

from acli.connections import get_client
from acli.errors import handle_boto_errors
from acli.output.elb import output_elbs, output_elb_info


@handle_boto_errors
def get_elb_list(aws_config):
    """
    @type aws_config: Config
    """
    elb_client = get_client(client_type='elb', config=aws_config)
    elbs = elb_client.describe_load_balancers().get('LoadBalancerDescriptions')
    return elbs


@handle_boto_errors
def get_elb(aws_config, elb_name=None):
    """
    @type aws_config: Config
    @type elb_name: unicode
    """
    if elb_name:
        try:
            elb_client = get_client(client_type='elb', config=aws_config)
            elbs = elb_client.describe_load_balancers(LoadBalancerNames=[elb_name])
            if elbs and elbs.get('LoadBalancerDescriptions'):
                return elbs.get('LoadBalancerDescriptions')[0]
        except botocore.exceptions.ClientError:
            exit('ELB: {0} could not be found.'.format(elb_name))


def elb_list(aws_config):
    """
    @type aws_config: Config
    """
    output_elbs(elbs=get_elb_list(aws_config))


def elb_info(aws_config=None, elb_name=None):
    """
    @type aws_config: Config
    @type elb_name: unicode
    """
    output_elb_info(elb=get_elb(aws_config,
                                elb_name=elb_name))
