# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)
from acli.output.route53 import (output_route53_list, output_route53_info)
import botocore.exceptions
from acli.connections import get_boto3_session


def route53_list(aws_config=None):
    """
    @type aws_config: Config
    """
    session = get_boto3_session(aws_config)
    conn = session.client('route53')
    zones = conn.list_hosted_zones()
    if zones.get('HostedZones', None):
        output_route53_list(output_media='console', zones=conn.list_hosted_zones())
    else:
        exit("No hosted zones found.")


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
