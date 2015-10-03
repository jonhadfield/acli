# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)
from boto3.session import Session
from acli.output.route53 import (output_route53_list, output_route53_info)


def get_boto3_session(aws_config):
    return Session(region_name=aws_config.region,
                   aws_access_key_id=aws_config.access_key_id,
                   aws_secret_access_key=aws_config.secret_access_key)


def route53_list(aws_config=None):
    session = get_boto3_session(aws_config)
    conn = session.client('route53')
    output_route53_list(output_media='console', zones=conn.list_hosted_zones())


def route53_info(aws_config=None, instance_id=None):
    session = get_boto3_session(aws_config)
    conn = session.resource('ec2')
    instance = conn.Instance(instance_id)
    try:
        if instance.instance_id:
            output_route53_info(output_media='console',
                                instance=instance)
    except AttributeError:
        exit("Cannot find instance: {0}".format(instance_id))
