# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)
from boto3.session import Session
from acli.output.route53 import (output_route53_list, output_route53_info)
import botocore.exceptions


def get_boto3_session(aws_config):
    return Session(region_name=aws_config.region,
                   aws_access_key_id=aws_config.access_key_id,
                   aws_secret_access_key=aws_config.secret_access_key)


def route53_list(aws_config=None):
    session = get_boto3_session(aws_config)
    conn = session.client('route53')
    output_route53_list(output_media='console', zones=conn.list_hosted_zones())


def route53_info(aws_config=None, zone_id=None):
    """
    @type aws_config: Config
    @type zone_id: unicode
    """
    session = get_boto3_session(aws_config)
    conn = session.client('route53')
    try:
        hosted_zone = conn.get_hosted_zone(Id=zone_id)
        record_sets = conn.list_resource_record_sets(HostedZoneId=zone_id)
        if hosted_zone['HostedZone']['Id']:
            output_route53_info(output_media='console',
                                zone=hosted_zone,
                                record_sets=record_sets)
    except AttributeError:
        exit("Cannot find hosted zone: {0}".format(zone_id))
    except botocore.exceptions.ClientError:
        exit("Cannot request hosted zone: {0}".format(zone_id))
