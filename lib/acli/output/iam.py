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


def output_iam_summary(summary_map=None):
    """
    @type summary_map: dict
    """
    td = list()
    td.append([Color('{autoblue}users{/autoblue}'),
               dash_if_none(summary_map.get('Users'))])
    td.append([Color('{autoblue}groups{/autoblue}'),
               dash_if_none(summary_map.get('Groups'))])
    td.append([Color('{autoblue}roles{/autoblue}'),
               dash_if_none(summary_map.get('Roles'))])
    td.append([Color('{autoblue}policies{/autoblue}'),
               summary_map.get('Policies')])
    td.append([Color('{autoblue}account access keys present{/autoblue}'),
               summary_map.get('AccountAccessKeysPresent')])
    td.append([Color('{autoblue}policy versions in use{/autoblue}'),
               summary_map.get('PolicyVersionsInUse')])
    td.append([Color('{autoblue}server certificates{/autoblue}'),
               summary_map.get('ServerCertificates')])
    td.append([Color('{autoblue}mfa devices{/autoblue}'),
               dash_if_none(summary_map.get('MFADevices'))])
    td.append([Color('{autoblue}mfa devices in use{/autoblue}'),
               summary_map.get('MFADevicesInUse')])
    td.append([Color('{autoblue}account MFA enabled{/autoblue}'),
               dash_if_none(summary_map.get('AccountMFAEnabled'))])
    td.append([Color('{autoblue}providers{/autoblue}'),
               summary_map.get('Providers')])
    td.append([Color('{autoblue}instance profiles{/autoblue}'),
               dash_if_none(summary_map.get('InstanceProfiles'))])
    td.append(["", ""])
    td.append([Color('{autowhite}quotas{/autowhite}'), ""])

    td.append([Color('{autoblue}user policy size quota{/autoblue}'),
               dash_if_none(summary_map.get('UserPolicySizeQuota'))])
    td.append([Color('{autoblue}assume role policy size quota{/autoblue}'),
               dash_if_none(summary_map.get('AssumeRolePolicySizeQuota'))])
    td.append([Color('{autoblue}server certificates quota{/autoblue}'),
               dash_if_none(summary_map.get('ServerCertificatesQuota'))])
    td.append([Color('{autoblue}users quota{/autoblue}'),
               dash_if_none(summary_map.get('UsersQuota'))])

    td.append([Color('{autoblue}policy size quota{/autoblue}'),
               dash_if_none(summary_map.get('PolicySizeQuota'))])

    td.append([Color('{autoblue}attached policies per group quota{/autoblue}'),
               dash_if_none(summary_map.get('AttachedPoliciesPerGroupQuota'))])

    td.append([Color('{autoblue}groups per user quota{/autoblue}'),
               dash_if_none(summary_map.get('GroupsPerUserQuota'))])
    td.append([Color('{autoblue}groups quota{/autoblue}'),
               dash_if_none(summary_map.get('GroupsQuota'))])
    td.append([Color('{autoblue}instance profiles quota{/autoblue}'),
               dash_if_none(summary_map.get('InstanceProfilesQuota'))])
    td.append([Color('{autoblue}attached policies per role quota{/autoblue}'),
               dash_if_none(summary_map.get('AttachedPoliciesPerRoleQuota'))])
    td.append([Color('{autoblue}access keys per user quota{/autoblue}'),
               dash_if_none(summary_map.get('AccessKeysPerUserQuota'))])
    td.append([Color('{autoblue}group policy size quota{/autoblue}'),
               dash_if_none(summary_map.get('GroupPolicySizeQuota'))])
    td.append([Color('{autoblue}versions per policy quota{/autoblue}'),
               dash_if_none(summary_map.get('VersionsPerPolicyQuota'))])

    td.append([Color('{autoblue}roles quota{/autoblue}'),
               dash_if_none(summary_map.get('RolesQuota'))])

    td.append([Color('{autoblue}policy version in use quota{/autoblue}'),
               dash_if_none(summary_map.get('PolicyVersionsInUseQuota'))])
    td.append([Color('{autoblue}policies quota{/autoblue}'),
               dash_if_none(summary_map.get('PoliciesQuota'))])
    td.append([Color('{autoblue}role policy size quota{/autoblue}'),
               dash_if_none(summary_map.get('RolePolicySizeQuota'))])
    output_ascii_table(table_title=Color('{autowhite}iam account summary{/autowhite}'),
                       table_data=td)
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
