# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)

from botocore.exceptions import ClientError

from acli.connections import get_client
from acli.errors import handle_boto_errors
from acli.output.eip import (output_eip_list, output_eip_info)


@handle_boto_errors
def eip_list(aws_config=None):
    """
    @type aws_config: Config
    """
    ec2_client = get_client(client_type='ec2', config=aws_config)
    addresses_response = ec2_client.describe_addresses()
    addresses = addresses_response.get('Addresses')
    if addresses:
        output_eip_list(addresses=addresses)
    exit('No elastic IPs found.')


@handle_boto_errors
def eip_info(aws_config=None, eip=None):
    """
    @type aws_config: Config
    @type eip: unicode
    """
    ec2_client = get_client(client_type='ec2', config=aws_config)
    try:
        addresses_response = ec2_client.describe_addresses(PublicIps=[eip])
        address = addresses_response.get('Addresses')[0]
        if address:
            output_eip_info(address=address)
    except ClientError:
        exit('EIP {0} not found.'.format(eip))
