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
            default = str(vpc.get('IsDefault'))
            td.append([vpcid,
                       dash_if_none(get_tag(name='Name', tags=vpc.get('Tags', None))),
                       dash_if_none(cidr_block),
                       dash_if_none(tenancy),
                       dash_if_none(state),
                       dash_if_none(dhcpoptions),
                       default])
        output_ascii_table(table_title="VPCs",
                           table_data=td,
                           inner_heading_row_border=True)
    exit(0)


def output_vpc_info(output_media=None, vpc=None, subnets=None):
    """
    @type output_media: unicode
    @type vpc: ec2.Vpc
    """
    if vpc:
        if output_media == 'console':
            td = list()
            td.append(['id', vpc.id])
            td.append(['CIDR block', vpc.cidr_block])
            td.append(['default', str(vpc.is_default)])
            td.append(['tenancy', vpc.instance_tenancy])
            td.append(['state', dash_if_none(vpc.state)])
            td.append(['tags', dash_if_none(str(vpc.tags))])
            if subnets:
                td.append(['subnets', "{0}".format('-' * 30)])
                for subnet in subnets:
                    print(subnet.tags)
                    td.append(['id', subnet.subnet_id])
                    td.append([' az', subnet.availability_zone])
                    td.append([' state', subnet.state])
                    td.append([' available IPs', str(subnet.available_ip_address_count)])
                    td.append([' CIDR block', subnet.cidr_block])
                    td.append([' default for az', str(subnet.default_for_az)])
                    td.append([' map public IP on launch', str(subnet.map_public_ip_on_launch)])
                    for tag in subnet.tags:
                        td.append([" {0}".format(tag.get('Key'), dash_if_none(tag.get('Value')))])

                        #for tag_name, tag_value in tag.iteritems():
                        #    td.append([" {0}".format(tag_name), tag_value])

            output_ascii_table(table_title="VPC Info",
                               table_data=td)
    else:
        exit('VPC does not exist.')
    exit(0)
