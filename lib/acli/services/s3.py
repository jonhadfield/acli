# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)
from acli.output.route53 import (output_route53_list, output_route53_info)
import botocore.exceptions
from acli.connections import get_client


def s3_list(aws_config=None):
    """
    @type aws_config: Config
    """
    s3_client = get_client(client_type='s3', config=aws_config)
    buckets = s3_client.list_buckets()
    print(buckets)
    #if zones.get('HostedZones', None):
    #    output_route53_list(output_media='console', zones=route53_client.list_hosted_zones())
    #else:
    #    exit("No hosted zones found.")


def s3_info(aws_config=None, item=None):
    """
    @type aws_config: Config
    @type path: unicode
    """
    s3_client = get_client(client_type='ec2', config=aws_config)
    print(s3_client)
    #try:
    #    hosted_zone = s3_client.get_hosted_zone(Id=zone_id)
    #    record_sets = s3_client.list_resource_record_sets(HostedZoneId=zone_id)
    #    if hosted_zone['HostedZone']['Id']:
    #        output_route53_info(output_media='console',
    #                            zone=hosted_zone,
    #                            record_sets=record_sets)
    #except AttributeError:
    #    exit("Cannot find hosted zone: {0}".format(zone_id))
    #except botocore.exceptions.ClientError:
    #    exit("Cannot request hosted zone: {0}".format(zone_id))
