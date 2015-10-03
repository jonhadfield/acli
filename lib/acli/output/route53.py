# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)
from acli.output import (output_ascii_table, dash_if_none)


def output_route53_list(output_media=None, zones=None):
    if isinstance(zones, dict):
        hosted_zones_list = [zones]
        for hosted_zone_dict in hosted_zones_list:
                if output_media == 'console':
                    td = list()
                    td.append(['id', 'name', 'count', 'comment', 'private zone'])
                    for hosted_zone in hosted_zone_dict.get('HostedZones'):
                        zone_id = dash_if_none(hosted_zone.get('Id'))
                        zone_name = hosted_zone.get('Name')
                        record_count = str(hosted_zone.get('ResourceRecordSetCount'))
                        comment = hosted_zone.get('Config').get('Comment')
                        private_zone = str(hosted_zone.get('Config').get('PrivateZone'))
                        td.append([zone_id,
                                   zone_name,
                                   record_count,
                                   comment,
                                   private_zone])
                    output_ascii_table(table_title="Route53 Zones",
                                       table_data=td,
                                       inner_heading_row_border=True)
    exit(0)


def output_route53_info(output_media=None, instance=None):
    if output_media == 'console':
        td = list()
        td.append(['id', instance.id])
        output_ascii_table(table_title="Instance Info",
                           table_data=td)
    exit(0)
