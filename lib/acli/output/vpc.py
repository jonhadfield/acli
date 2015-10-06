# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)
from acli.output import (output_ascii_table, dash_if_none)


def get_tag(name=None, tags=None):
    if tags:
        for tag in tags:
            if tag.get('Key') == name:
                return tag.get('Value')


def output_vpc_list(output_media=None, vpcs=None):
    """
    @type output_media: unicode
    @type vpcs: dict
    """
    if output_media == 'console':
        td = list()
        td.append(['VpcId', 'name', 'CIDR block', 'tenancy', 'state', 'DHCP options id', 'default'])
        for vpc in vpcs.get('Vpcs'):
            vpcid = vpc.get('VpcId')
            cidr_block = vpc.get('CidrBlock')
            tenancy = vpc.get('tenancy')
            state = vpc.get('state')
            dhcpoptions = vpc.get('DhcpOptionsId')
            default = str(vpc.get('isDefault'))
            td.append([vpcid,
                       dash_if_none(get_tag(name='Name', tags=vpc.get('Tags', None))),
                       dash_if_none(cidr_block),
                       dash_if_none(tenancy),
                       dash_if_none(state),
                       dash_if_none(dhcpoptions),
                       dash_if_none(default)])
        output_ascii_table(table_title="VPCs",
                           table_data=td,
                           inner_heading_row_border=True)
    exit(0)


def output_vpc_info(output_media=None, zone=None, record_sets=None):
    """
    @type output_media: unicode
    @type zone: zone
    @type record_sets: ResourceRecordSets
    """
    if output_media == 'console':
        td = list()
        td.append(['id', zone['HostedZone']['Id']])
        td.append(['Name', zone['HostedZone']['Name']])
        td.append(['Count', str(zone['HostedZone']['ResourceRecordSetCount'])])
        td.append(['Comment', zone['HostedZone']['Config']['Comment']])
        td.append(['Private', str(zone['HostedZone']['Config']['PrivateZone'])])
        td.append(['Name Servers', "\n".join(zone['DelegationSet']['NameServers'])])
        td.append(['Records', ' '])
        td.append(['{0}'.format("-" * 12), '{0}'.format("-" * 20)])
        for record_set in record_sets['ResourceRecordSets']:
            td.append(['Name', record_set['Name']])
            td.append([' Type', record_set['Type']])
            td.append([' TTL', str(record_set['TTL'])])
            td.append([' Values', "\n".join((record_set['ResourceRecords']))])
        output_ascii_table(table_title="Zone Info",
                           table_data=td)
    exit(0)
