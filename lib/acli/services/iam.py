# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)

from botocore.exceptions import ClientError

from acli.connections import get_client
from acli.errors import handle_boto_errors
from acli.output.iam import (output_iam_user_list)
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
