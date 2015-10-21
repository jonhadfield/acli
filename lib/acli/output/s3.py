# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)
from acli.output import (output_ascii_table, dash_if_none)


def output_s3_list(output_media=None, item=None):
    """
    @type output_media: unicode
    @type item: unicode
    """
    #if isinstance(zones, dict):
    #    zones = [zones]
    #for hosted_zone_dict in zones:
    #        if output_media == 'console':
    #            td = list()
    #            td.append(['id', 'name',
    #                       'count', 'comment',
    #                       'private zone'])
    #            hosted_zones = sorted(hosted_zone_dict.get('HostedZones'), key=lambda k: k['Name'])
    #            for hosted_zone in hosted_zones:
    #                zone_id = dash_if_none(hosted_zone.get('Id'))
    #                zone_name = hosted_zone.get('Name')
    #                record_count = str(hosted_zone.get('ResourceRecordSetCount'))
    #                comment = hosted_zone.get('Config').get('Comment')
    #                private_zone = str(hosted_zone.get('Config').get('PrivateZone'))
    #                td.append([zone_id,
    #                           zone_name,
    #                           record_count,
    #                           comment,
    #                           private_zone])
    #            output_ascii_table(table_title="Route53 Zones",
    #                               table_data=td,
    #                               inner_heading_row_border=True)
    exit(0)


def output_route53_info(output_media=None, item=None):
    """
    @type output_media: unicode
    @type item: unicode
    """
    # if output_media == 'console':
    #    td = list()
    #    td.append(['id', zone['HostedZone']['Id']])
    #    td.append(['Name', zone['HostedZone']['Name']])
    #    td.append(['Count', str(zone['HostedZone']['ResourceRecordSetCount'])])
    #    td.append(['Comment', zone['HostedZone']['Config']['Comment']])
    #    td.append(['Private', str(zone['HostedZone']['Config']['PrivateZone'])])
    #    td.append(['Name Servers', "\n".join(zone['DelegationSet']['NameServers'])])
    #    td.append(['Records', ' '])
    #    td.append(['{0}'.format("-" * 12), '{0}'.format("-" * 20)])
    #    for record_set in record_sets['ResourceRecordSets']:
    #        td.append(['Name', record_set['Name']])
    #        td.append([' Type', record_set['Type']])
    #        td.append([' TTL', str(record_set['TTL'])])
    #        td.append([' Values', "\n".join(get_record_set_values(record_set['ResourceRecords']))])
    #    output_ascii_table(table_title="Zone Info",
    #                       table_data=td)
    exit(0)
