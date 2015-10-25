# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)
from acli.output.route53 import (output_route53_list, output_route53_info)
import botocore.exceptions
from acli.connections import get_client


def route53_list(aws_config=None):
    """
    @type aws_config: Config
    """
    route53_client = get_client(client_type='route53', config=aws_config)
    zones = route53_client.list_hosted_zones()
    if zones.get('HostedZones', None):
        output_route53_list(output_media='console', zones=route53_client.list_hosted_zones())
    else:
        exit("No hosted zones found.")


def route53_info(aws_config=None, zone_id=None):
    """
    @type aws_config: Config
    @type zone_id: unicode
    """
    route53_client = get_client(client_type='route53', config=aws_config)
    try:
        hosted_zone = route53_client.get_hosted_zone(Id=zone_id)
        record_sets = route53_client.list_resource_record_sets(HostedZoneId=zone_id)
        if hosted_zone['HostedZone']['Id']:
            output_route53_info(output_media='console',
                                zone=hosted_zone,
                                record_sets=record_sets)
    #except AttributeError:
    #    exit("Cannot find hosted zone: {0}".format(zone_id))
    except botocore.exceptions.ClientError:
        exit("Cannot request hosted zone: {0}".format(zone_id))
