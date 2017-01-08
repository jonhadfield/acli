# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)

from colorclass import Color, Windows

from acli.output import (output_ascii_table, output_ascii_table_list, dash_if_none)

Windows.enable(auto_colors=True, reset_atexit=True)


def colour_state(state=None):
    if not state:
        return Color('{autoblack}-{/autoblack}')
    elif state == 'running':
        return Color('{autogreen}' + state + '{/autogreen}')
    elif state in ('stopped', 'stopping', 'shutting-down', 'terminated'):
        return Color('{autored}' + state + '{/autored}')
    elif state in ('rebooting', 'pending'):
        return Color('{autoyellow}' + state + '{/autoyellow}')


def user_has_mfa_assigned(username=None, password_last_used=None, mfa_devices=None):
    for mfa_device in mfa_devices:
        if mfa_device['User']['UserName'] == username:
            return Color('{autogreen}TRUE{/autogreen}')
    if password_last_used:
        return Color('{autored}FALSE{/autored}')
    else:
        return Color('FALSE')


def output_iam_user_list(users=None, mfa_devices=None):
    """
    @type users: list
    @type mfa_devices: list
    """
    td = list()
    table_header = [Color('{autoblue}user name{/autoblue}'),
                    Color('{autoblue}created{/autoblue}'),
                    Color('{autoblue}password last used{/autoblue}'),
                    Color('{autoblue}mfa enabled{/autoblue}')]
    for user in users:
        td.append([dash_if_none(user.get('UserName')),
                   dash_if_none(user.get('CreateDate')),
                   dash_if_none(user.get('PasswordLastUsed')),
                   user_has_mfa_assigned(username=user.get('UserName'), password_last_used=user.get('PasswordLastUsed'),
                                         mfa_devices=mfa_devices)])
    output_ascii_table_list(table_title=Color('{autowhite}user list{/autowhite}'),
                            table_data=td,
                            table_header=table_header,
                            inner_heading_row_border=True)
    exit(0)


def output_eip_info(address=None):
    """
    @type address: dict
    """
    td = list()
    td.append([Color('{autoblue}public ip{/autoblue}'),
               dash_if_none(address.get('PublicIp'))])
    td.append([Color('{autoblue}allocation id{/autoblue}'),
               dash_if_none(address.get('AllocationId'))])
    td.append([Color('{autoblue}instance id{/autoblue}'),
               dash_if_none(address.get('InstanceId'))])
    td.append([Color('{autoblue}association id{/autoblue}'),
               dash_if_none(address.get('AssociationId'))])
    td.append([Color('{autoblue}domain{/autoblue}'),
               dash_if_none(address.get('Domain'))])
    td.append([Color('{autoblue}network interface id{/autoblue}'),
               dash_if_none(address.get('NetworkInterfaceId'))])
    td.append([Color('{autoblue}network interface owner id{/autoblue}'),
               dash_if_none(address.get('NetworkInterfaceOwnerId'))])
    td.append([Color('{autoblue}private ip{/autoblue}'),
               dash_if_none(address.get('PrivateIpAddress'))])
    output_ascii_table(table_title=Color('{autowhite}eip info{/autowhite}'),
                       table_data=td)
    exit(0)
