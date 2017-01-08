# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)

from acli.connections import get_client
from acli.errors import handle_boto_errors
from acli.output.iam import (output_iam_user_list, output_iam_summary, output_iam_user_info)
from botocore.exceptions import ClientError


# from acli.output.iam import (output_iam_user_list, output_iam_user_info)


@handle_boto_errors
def iam_user_list(aws_config=None):
    """
    @type aws_config: Config
    """
    iam_client = get_client(client_type='iam', config=aws_config)
    users_response = iam_client.list_users()
    mfa_devices_response = iam_client.list_virtual_mfa_devices(AssignmentStatus='Assigned')
    mfa_devices = mfa_devices_response.get('VirtualMFADevices')
    users = users_response.get('Users')
    if users:
        output_iam_user_list(users=users, mfa_devices=mfa_devices)
    exit('No users found.')


def iam_user_info(aws_config=None, username=None):
    """
    @type aws_config: Config
    @type username: str
    """
    iam_client = get_client(client_type='iam', config=aws_config)
    try:
        user_response = iam_client.get_user(UserName=username)
        user = user_response['User']

        user_access_keys_response = iam_client.list_access_keys(UserName=username)
        user_access_keys = user_access_keys_response.get('AccessKeyMetadata')

        user_policies_response = iam_client.list_user_policies(UserName=username)
        user_policies = user_policies_response.get('PolicyNames')

        user_groups_response = iam_client.list_groups_for_user(UserName=username)
        user_groups = user_groups_response.get('Groups')
        group_names = list()
        for ug in user_groups:
            group_names.append(ug['GroupName'])

        mfa_devices_response = iam_client.list_virtual_mfa_devices(AssignmentStatus='Assigned')
        mfa_devices = mfa_devices_response.get('VirtualMFADevices')
        user_mfa_devices = list()
        for mfa_device in mfa_devices:
            if mfa_device['User']['UserName'] == username:
                user_mfa_devices.append(mfa_device)
        output_iam_user_info(user=user, user_mfa_devices=user_mfa_devices, user_access_keys=user_access_keys,
                             user_policies=user_policies, user_groups=group_names)
    except (ClientError, IndexError):
        exit("Cannot find user: {0}".format(username))


def summary(aws_config=None):
    """
    @type aws_config: Config
    """
    iam_client = get_client(client_type='iam', config=aws_config)
    summary_response = iam_client.get_account_summary()
    summary_map = summary_response['SummaryMap']
    output_iam_summary(summary_map=summary_map)

#
# @handle_boto_errors
# def eip_info(aws_config=None, eip=None):
#     """
#     @type aws_config: Config
#     @type eip: unicode
#     """
#     ec2_client = get_client(client_type='ec2', config=aws_config)
#     try:
#         addresses_response = ec2_client.describe_addresses(PublicIps=[eip])
#         address = addresses_response.get('Addresses')[0]
#         if address:
#             output_eip_info(address=address)
#     except ClientError:
#         exit('EIP {0} not found.'.format(eip))
