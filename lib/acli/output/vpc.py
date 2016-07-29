# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)
from acli.output import (output_ascii_table, output_ascii_table_list, dash_if_none)
from colorclass import Color, Windows
Windows.enable(auto_colors=True, reset_atexit=True)


def get_tag(name=None, tags=None):
    if tags:
        for tag in tags:
            if tag.get('Key') == name:
                return tag.get('Value')


def output_vpc_list(vpcs=None):
    """
    @type vpcs: dict
    """
    td = list()
    table_header = [Color('{autoblue}vpc id{/autoblue}'), Color('{autoblue}name{/autoblue}'),
                    Color('{autoblue}CIDR block{/autoblue}'), Color('{autoblue}tenancy{/autoblue}'),
                    Color('{autoblue}state{/autoblue}'), Color('{autoblue}DHCP options{/autoblue}'),
                    Color('{autoblue}default vpc{/autoblue}')]
    for vpc in vpcs.get('Vpcs'):
        vpcid = vpc.get('VpcId')
        cidr_block = vpc.get('CidrBlock')
        tenancy = vpc.get('InstanceTenancy')
        state = vpc.get('State')
        dhcpoptions = vpc.get('DhcpOptionsId')
        default = str(vpc.get('IsDefault'))
        td.append([vpcid,
                   dash_if_none(get_tag(name='Name', tags=vpc.get('Tags'))),
                   dash_if_none(cidr_block),
                   dash_if_none(tenancy),
                   dash_if_none(state),
                   dash_if_none(dhcpoptions),
                   default])
    output_ascii_table_list(table_title=Color('{autowhite}VPCs{/autowhite}'),
                            table_data=td,
                            table_header=table_header,
                            inner_heading_row_border=True)
    exit(0)


def output_vpc_info(vpc=None, subnets=None):
    """
    @type vpc: ec2.Vpc
    @type subnets: dict
    """
    if vpc:
        td = list()
        td.append([Color('{autoblue}vpc id{/autoblue}'), vpc.get('VpcId')])
        td.append([Color('{autoblue}CIDR block{/autoblue}'), vpc.get('CidrBlock')])
        td.append([Color('{autoblue}default{/autoblue}'), str(vpc.get('IsDefault'))])
        td.append([Color('{autoblue}tenancy{/autoblue}'), vpc.get('InstanceTenancy')])
        td.append([Color('{autoblue}state{/autoblue}'), dash_if_none(vpc.get('State'))])
        td.append([Color('{autoblue}tags{/autoblue}'), " "])
        if vpc.get('Tags'):
            for vpc_tag in vpc.get('Tags'):
                td.append([Color('{autoblue}' + "{0}".format(vpc_tag.get('Key'))+'{/autoblue}'),
                           " {0}".format(vpc_tag.get('Value'))])
        if subnets:
            td.append(["{0}".format('-' * 30), "{0}".format('-' * 30)])
            td.append([Color('{autowhite}SUBNETS{/autowhite}'), " "])
            for subnet in subnets.get('Subnets'):
                td.append(["{0}".format('-' * 30),
                           "{0}".format('-' * 30)])
                td.append([Color('{autoblue}subnet id{/autoblue}'),
                           subnet.get('SubnetId')])
                td.append([Color('{autoblue}az{/autoblue}'),
                           subnet.get('AvailabilityZone')])
                td.append([Color('{autoblue}state{/autoblue}'),
                           subnet.get('State')])
                td.append([Color('{autoblue}available IPs{/autoblue}'),
                           str(subnet.get('AvailableIpAddressCount'))])
                td.append([Color('{autoblue}CIDR block{/autoblue}'),
                           subnet.get('CidrBlock')])
                td.append([Color('{autoblue}default for az{/autoblue}'),
                           str(subnet.get('DefaultForAz'))])
                td.append([Color('{autoblue}map public ip on launch{/autoblue}'),
                           str(subnet.get('MapPublicIpOnLaunch'))])
                if subnet.get('Tags'):
                    td.append([Color('{autoblue}tags{/autoblue}'), "-"])
                    for tag in subnet.get('Tags'):
                        tag_key, tag_value = dash_if_none(tag.get('Key')), dash_if_none(tag.get('Value'))
                        td.append([Color('{autoblue}'+" {}".format(tag_key)+'{/autoblue}'), "{}".format(tag_value)])
        output_ascii_table(table_title=Color('{autowhite}vpc info{/autowhite}'),
                           table_data=td)
    else:
        exit('VPC does not exist.')
    exit(0)
