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


def split_string(the_string=None, chunk_size=None):
    length = 0
    output = str()
    chunks = the_string.split()
    for chunk in chunks:
        length += len(chunk)
        output += chunk
        if length >= chunk_size:
            output += "\n"
            length = 0
        else:
            output += " "
    return output.rstrip()


def output_secgroup_list(secgroups=None):
    """
    @type secgroups: dict
    """
    td = list()
    table_header = [Color('{autoblue}group id{/autoblue}'),
                    Color('{autoblue}group name{/autoblue}'),
                    Color('{autoblue}description{/autoblue}')]
    for secgroup in secgroups.get('SecurityGroups'):
        td.append([secgroup.get('GroupId'),
                  split_string(secgroup.get('GroupName'), chunk_size=30),
                  split_string(secgroup.get('Description'), chunk_size=40)])
    output_ascii_table_list(table_title=Color('{autowhite}security groups{/autowhite}'),
                            table_data=td,
                            table_header=table_header,
                            inner_heading_row_border=True)
    exit(0)


def get_ip_ranges(ip_ranges):
    out = str()
    for ip_range in ip_ranges:
        out += "{0}\n".format(ip_range.get('CidrIp'))
    return out.rstrip()


def get_uid_group_pairs(uid_gps=None):
    out = str()
    for uid_gp in uid_gps:
        out += '{0} - {1}\n'.format(uid_gp.get('UserId'), uid_gp.get('GroupId'))
    return out.strip()


def output_secgroup_info(secgroup=None):
    """
    @type secgroup: ec2.SecurityGroup
    """
    if secgroup:
        td = list()
        td.append([Color('{autoblue}group id{/autoblue}'), secgroup.get('GroupId')])
        td.append([Color('{autoblue}group name{/autoblue}'), secgroup.get('GroupName')])
        td.append([Color('{autoblue}description{/autoblue}'), secgroup.get('Description')])
        td.append([Color('{autoblue}vpc id{/autoblue}'), dash_if_none(secgroup.get('VpcId'))])
        if secgroup.get('IpPermissions'):
            td.append(['ip permissions', '{0}'.format("-" * 30)])
            for ip_perm in secgroup.get('IpPermissions'):
                td.append([Color('{autoblue}from port{/autoblue}'),
                           dash_if_none(ip_perm.get('FromPort'))])
                td.append([Color('{autoblue}to port{/autoblue}'),
                           dash_if_none(ip_perm.get('ToPort'))])
                td.append([Color('{autoblue}ip ranges{/autoblue}'),
                           dash_if_none(get_ip_ranges(ip_perm.get('IpRanges')))])
                td.append([Color('{autoblue}ip protocol{/autoblue}'),
                           dash_if_none(ip_perm.get('IpProtocol'))])
                if ip_perm.get('UserIdGroupPairs'):
                    td.append(['user id group pairs', '{0}'.format("-" * 30)])
                    td.append(['', get_uid_group_pairs(uid_gps=ip_perm.get('UserIdGroupPairs'))])

        if secgroup.get('IpPermissionsEgress'):
            td.append(['ip permissions egress', '{0}'.format("-" * 30)])
            for ip_perm_egress in secgroup.get('IpPermissionsEgress'):
                td.append([Color('{autoblue}prefix list ids{/autoblue}'),
                           dash_if_none(ip_perm_egress.get('PrefixListIds'))])
                td.append([Color('{autoblue}from port{/autoblue}'),
                           dash_if_none(ip_perm_egress.get('FromPort'))])
                td.append([Color('{autoblue}to port{/autoblue}'),
                           dash_if_none(ip_perm_egress.get('ToPort'))])
                td.append([Color('{autoblue}ip ranges{/autoblue}'),
                           dash_if_none(get_ip_ranges(ip_perm_egress.get('IpRanges')))])
                td.append([Color('{autoblue}ip protocol{/autoblue}'),
                           dash_if_none(ip_perm_egress.get('IpProtocol'))])
                if ip_perm_egress.get('UserIdGroupPairs'):
                    td.append(['user id group pairs', '{0}'.format("-" * 30)])
                    td.append(['', get_uid_group_pairs(uid_gps=ip_perm_egress.get('UserIdGroupPairs'))])
        output_ascii_table(table_title=Color('{autowhite}security group info{/autowhite}'),
                           table_data=td)
    else:
        exit('Security group does not exist.')
    exit(0)
