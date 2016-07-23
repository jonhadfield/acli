# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)

from boto3.session import Session


def get_boto3_session(aws_config):
    """
    @type aws_config: Config
    """
    if all((aws_config.region, aws_config.access_key_id, aws_config.secret_access_key)):
        return Session(region_name=aws_config.region,
                       aws_access_key_id=aws_config.access_key_id,
                       aws_secret_access_key=aws_config.secret_access_key)
    elif aws_config.region:
        return Session(region_name=aws_config.region)
    else:
        return Session()


def get_client(client_type=None, config=None):
    """
    @type client_type: basestring
    @type config: Config
    """
    session = get_boto3_session(aws_config=config)
    if client_type == 'ec2':
        return session.client('ec2')
    elif client_type == 'elb':
        return session.client('elb')
    elif client_type == 'iam':
        return session.client('iam')
    elif client_type == 'autoscaling':
        return session.client('autoscaling')
    elif client_type == 'cloudwatch':
        return session.client('cloudwatch')
    elif client_type == 'route53':
        return session.client('route53')
    elif client_type == 's3':
        return session.client('s3')
    elif client_type == 'es':
        return session.client('es')
    elif client_type == 'efs':
        return session.client('efs')
