# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)
from acli.output import (output_ascii_table, dash_if_none)
from colorclass import Color, Windows
Windows.enable(auto_colors=True, reset_atexit=True)


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
            tenancy = vpc.get('InstanceTenancy')
            state = vpc.get('State')
            dhcpoptions = vpc.get('DhcpOptionsId')
            default = str(vpc.get('IsDefault'))
            td.append([vpcid,
                       dash_if_none(get_tag(name='Name', tags=vpc.get('Tags', None))),
                       dash_if_none(cidr_block),
                       dash_if_none(tenancy),
                       dash_if_none(state),
                       dash_if_none(dhcpoptions),
                       default])
        output_ascii_table(table_title=Color('{autowhite}VPCs{/autowhite}'),
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
            td.append(['vpc id', vpc.get('VpcId')])
            td.append(['CIDR block', vpc.get('CidrBlock')])
            td.append(['default', str(vpc.get('IsDefault'))])
            td.append(['tenancy', vpc.get('InstanceTenancy')])
            td.append(['state', dash_if_none(vpc.get('State'))])
            td.append(['tags', " "])
            if vpc.get('Tags'):
                for vpc_tag in vpc.get('Tags'):
                    td.append([" {0}".format(vpc_tag.get('Key')), " {0}".format(vpc_tag.get('Value'))])
            if subnets:
                td.append(["{0}".format('-' * 30), "{0}".format('-' * 30)])
                td.append(['SUBNETS', " "])
                for subnet in subnets.get('Subnets'):
                    td.append(["{0}".format('-' * 30), "{0}".format('-' * 30)])
                    td.append(['subnet id', subnet.get('SubnetId')])
                    td.append(['az', subnet.get('AvailabilityZone')])
                    td.append(['state', subnet.get('State')])
                    td.append(['available IPs', str(subnet.get('AvailableIpAddressCount'))])
                    td.append(['CIDR block', subnet.get('CidrBlock')])
                    td.append(['default for az', str(subnet.get('DefaultForAz'))])
                    td.append(['map public IP on launch', str(subnet.get('MapPublicIpOnLaunch'))])
                    if subnet.get('Tags'):
                        td.append(['tags', "-"])
                        for tag in subnet.get('Tags'):
                            tag_key, tag_value = dash_if_none(tag.get('Key', None)), dash_if_none(tag.get('Value', None))
                            td.append([" {}".format(tag_key), "{}".format(tag_value)])
            output_ascii_table(table_title=Color('{autowhite}vpc info{/autowhite}'),
                               table_data=td)
    else:
        exit('VPC does not exist.')
    exit(0)
