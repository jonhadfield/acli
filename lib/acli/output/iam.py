# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)

from colorclass import Color, Windows

from acli.output import (output_ascii_table, output_ascii_table_list, dash_if_none)

Windows.enable(auto_colors=True, reset_atexit=True)


def colour_staus(status=None):
    if not status:
        return Color('{autoblack}-{/autoblack}')
    elif status == 'Active':
        return Color('{autogreen}' + status + '{/autogreen}')
    elif status == 'Inactive':
        return Color('{autored}' + status + '{/autored}')


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


def output_iam_user_info(user=None, user_mfa_devices=None, user_access_keys=None, user_policies=None, user_groups=None):
    """
    @type user: dict
    @type user_mfa_devices: list
    @type user_access_keys: list
    @type user_policies: list
    @type user_groups: list
    """
    td = list()
    td.append([Color('{autoblue}name{/autoblue}'),
               dash_if_none(user.get('UserName'))])
    td.append([Color('{autoblue}id{/autoblue}'),
               dash_if_none(user.get('UserId'))])
    td.append([Color('{autoblue}arn{/autoblue}'),
               dash_if_none(user.get('Arn'))])
    td.append([Color('{autoblue}path{/autoblue}'),
               dash_if_none(user.get('Path'))])
    td.append([Color('{autoblue}password last used{/autoblue}'),
               dash_if_none(user.get('PasswordLastUsed'))])
    td.append([Color('{autoblue}created{/autoblue}'),
               dash_if_none(user.get('CreateDate'))])
    if user_groups:
        td.append([Color('{autoblue}groups{/autoblue}'), ",".join(user_groups)])
    else:
        td.append([Color('{autoblue}groups{/autoblue}'),
                   dash_if_none()])
    td.append([Color('{autoblue}policies{/autoblue}'),
               dash_if_none(",".join(user_policies))])
    if not user_access_keys:
        td.append([Color('{autoblue}access keys{/autoblue}'),
                   dash_if_none()])
    else:
        td.append([Color('{autowhite}access keys{/autowhite}'), ""])
        for key in user_access_keys:
            td.append([Color('{autoblue}  id / status / enabled{/autoblue}'),
                       "{0} / {1} / {2}".format(key.get('AccessKeyId'), colour_staus(key.get('Status')),
                                                key.get('CreateDate'))])
    if not user_mfa_devices:
        td.append([Color('{autoblue}mfa devices{/autoblue}'),
                   dash_if_none()])
    else:
        td.append([Color('{autowhite}mfa devices{/autowhite}'), ""])
        for md in user_mfa_devices:
            td.append([Color('{autoblue}  serial / enabled{/autoblue}'),
                       "{0} / {1}".format(md.get('SerialNumber'), md.get('EnableDate'))])

    output_ascii_table(table_title=Color('{autowhite}user info{/autowhite}'),
                       table_data=td)
    exit(0)
