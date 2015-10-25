# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)
from acli.output import (output_ascii_table, dash_if_none)
from colorclass import Color, Windows
Windows.enable(auto_colors=True, reset_atexit=True)


def colour_state(state=None):
    if not state:
        return Color('{autoblack}-{/autoblack}')
    elif state == 'running':
        return Color('{autogreen}'+state+'{/autogreen}')
    elif state in ('stopped', 'stopping', 'shutting-down', 'terminated'):
        return Color('{autored}'+state+'{/autored}')
    elif state in ('rebooting', 'pending'):
        return Color('{autoyellow}'+state+'{/autoyellow}')


def output_eip_list(output_media=None, addresses=None):
    """
    @type output_media: unicode
    @type addresses: list
    """
    if output_media == 'console':
        td = list()
        td.append([Color('{autoblue}public ip{/autoblue}'),
                   Color('{autoblue}instance id{/autoblue}'),
                   Color('{autoblue}domain{/autoblue}'),
                   Color('{autoblue}private ip address{/autoblue}')])
        for addr in addresses:
            td.append([dash_if_none(addr.get('PublicIp', None)),
                       dash_if_none(addr.get('InstanceId')),
                       dash_if_none(addr.get('Domain', None)),
                       dash_if_none(addr.get('PrivateIpAddress', None))])
        output_ascii_table(table_title=Color('{autowhite}address list{/autowhite}'),
                           table_data=td,
                           inner_heading_row_border=True)
    exit(0)


def output_eip_info(output_media=None, address=None):
    """
    @type output_media: unicode
    @type address: dict
    """
    if output_media == 'console':
        td = list()
        td.append([Color('{autoblue}public ip{/autoblue}'),
                   dash_if_none(address.get('PublicIp', None))])
        td.append([Color('{autoblue}allocation id{/autoblue}'),
                   dash_if_none(address.get('AllocationId', None))])
        td.append([Color('{autoblue}association id{/autoblue}'),
                   dash_if_none(address.get('AssociationId', None))])
        td.append([Color('{autoblue}domain{/autoblue}'),
                   dash_if_none(address.get('Domain', None))])
        td.append([Color('{autoblue}network interface id{/autoblue}'),
                   dash_if_none(address.get('NetworkInterfaceId', None))])
        td.append([Color('{autoblue}network interface owner id{/autoblue}'),
                   dash_if_none(address.get('NetworkInterfaceOwnerId', None))])
        td.append([Color('{autoblue}private ip{/autoblue}'),
                   dash_if_none(address.get('PrivateIpAddress', None))])
        output_ascii_table(table_title=Color('{autowhite}eip info{/autowhite}'),
                           table_data=td)
    exit(0)
