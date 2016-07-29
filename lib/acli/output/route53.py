# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)
from acli.output import (output_ascii_table, output_ascii_table_list, dash_if_none)
from colorclass import Color, Windows
Windows.enable(auto_colors=True, reset_atexit=True)


def output_route53_list(zones=None):
    """
    @type zones: list | dict
    """
    td = list()
    table_header = list()
    if isinstance(zones, dict):
        zones = [zones]
    for hosted_zone_dict in zones:
        td = list()
        table_header = [Color('{autoblue}id{/autoblue}'), Color('{autoblue}name{/autoblue}'),
                        Color('{autoblue}count{/autoblue}'), Color('{autoblue}comment{/autoblue}'),
                        Color('{autoblue}private zone{/autoblue}')]
        hosted_zones = sorted(hosted_zone_dict.get('HostedZones'), key=lambda k: k['Name'])
        for hosted_zone in hosted_zones:
            zone_id = dash_if_none(hosted_zone.get('Id'))
            zone_name = dash_if_none(hosted_zone.get('Name'))
            record_count = str(hosted_zone.get('ResourceRecordSetCount'))
            comment = dash_if_none(hosted_zone.get('Config').get('Comment'))
            private_zone = dash_if_none(hosted_zone.get('Config').get('PrivateZone'))
            td.append([zone_id,
                       zone_name,
                       record_count,
                       comment,
                       private_zone])
    output_ascii_table_list(table_title=Color('{autowhite}route53 zones{/autowhite}'),
                            table_data=td,
                            table_header=table_header,
                            inner_heading_row_border=True)
    exit(0)


def get_record_set_values(resource_records):
    """
    @type resource_records: list
    """
    out = list()
    for record in resource_records:
        out.append(record.get('Value'))
    return out


def output_route53_info(zone=None, record_sets=None):
    """
    @type zone: zone
    @type record_sets: ResourceRecordSets
    """
    td = list()
    td.append([Color('{autoblue}id{/autoblue}'),
               dash_if_none(zone.get('HostedZone').get('Id'))])
    td.append([Color('{autoblue}name{/autoblue}'),
               dash_if_none(zone.get('HostedZone').get('Name'))])
    td.append([Color('{autoblue}records{/autoblue}'),
               dash_if_none(zone.get('HostedZone').get('ResourceRecordSetCount'))])
    td.append([Color('{autoblue}comment{/autoblue}'),
               dash_if_none(zone.get('HostedZone').get('Config').get('Comment'))])
    td.append([Color('{autoblue}private{/autoblue}'),
               dash_if_none(zone.get('HostedZone').get('Config').get('PrivateZone'))])
    td.append([Color('{autoblue}name servers{/autoblue}'),
               "\n".join(zone['DelegationSet']['NameServers'])])
    td.append([Color('{autoblue}records{/autoblue}'), ' '])
    td.append(['{0}'.format("-" * 12), '{0}'.format("-" * 20)])
    for record_set in record_sets['ResourceRecordSets']:
        td.append([Color('{autoblue}name{/autoblue}'),
                   record_set['Name']])
        td.append([Color('{autoblue} type{/autoblue}'),
                   record_set['Type']])
        td.append([Color('{autoblue} ttl{/autoblue}'),
                   str(record_set['TTL'])])
        td.append([Color('{autoblue} values{/autoblue}'),
                   "\n".join(get_record_set_values(record_set['ResourceRecords']))])
    output_ascii_table(table_title=Color('{autowhite}zone info{/autowhite}'),
                       table_data=td)
    exit(0)
