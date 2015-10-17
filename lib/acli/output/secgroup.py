# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)
from acli.output import (output_ascii_table, dash_if_none)


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


def output_secgroup_list(output_media=None, secgroups=None):
    """
    @type output_media: unicode
    @type secgroups: dict
    """
    if output_media == 'console':
        td = list()
        td.append(['Group ID', 'Group Name', 'Description'])
        for secgroup in secgroups.get('SecurityGroups'):
            td.append([secgroup.get('GroupId'),
                      split_string(secgroup.get('GroupName'), chunk_size=30),
                      split_string(secgroup.get('Description'), chunk_size=40)])
        output_ascii_table(table_title="Security Groups",
                           table_data=td,
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


def output_secgroup_info(output_media=None, secgroup=None):
    """
    @type output_media: unicode
    @type secgroup: ec2.SecurityGroup
    """
    if secgroup:
        if output_media == 'console':
            td = list()
            td.append(['group id', secgroup.id])
            td.append(['group name', secgroup.group_name])
            td.append(['description', secgroup.description])
            td.append(['vpc id', dash_if_none(secgroup.vpc_id)])
            td.append(['meta', str(secgroup.meta)])
            td.append(['tags', str(secgroup.tags)])

            if secgroup.ip_permissions:
                td.append(['ip permissions', '{0}'.format("-" * 30)])
                for ip_perm in secgroup.ip_permissions:
                    td.append(['from port', str(ip_perm.get('FromPort'))])
                    td.append(['to port', str(ip_perm.get('ToPort'))])
                    td.append(['ip ranges', dash_if_none(get_ip_ranges(ip_perm.get('IpRanges')))])
                    td.append(['ip protocol', str(ip_perm.get('IpProtocol'))])
                    if ip_perm.get('UserIdGroupPairs'):
                        td.append(['user id group pairs', '{0}'.format("-" * 30)])
                        td.append(['', get_uid_group_pairs(uid_gps=ip_perm.get('UserIdGroupPairs'))])

            if secgroup.ip_permissions_egress:
                td.append(['ip permissions egress', '{0}'.format("-" * 30)])
                for ip_perm_egress in secgroup.ip_permissions_egress:
                    td.append(['prefix list ids', dash_if_none(ip_perm_egress.get('PrefixListIds'))])
                    td.append(['from port', str(ip_perm_egress.get('FromPort'))])
                    td.append(['to port', str(ip_perm_egress.get('ToPort'))])
                    td.append(['ip ranges', dash_if_none(get_ip_ranges(ip_perm_egress.get('IpRanges')))])
                    td.append(['ip protocol', str(ip_perm_egress.get('IpProtocol'))])
                    if ip_perm_egress.get('UserIdGroupPairs'):
                        td.append(['user id group pairs', '{0}'.format("-" * 30)])
                        td.append(['', get_uid_group_pairs(uid_gps=ip_perm_egress.get('UserIdGroupPairs'))])
        output_ascii_table(table_title="Security Group Info",
                           table_data=td)
    else:
        exit('Security group does not exist.')
    exit(0)
