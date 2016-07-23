# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)

from botocore.exceptions import ClientError

from acli.connections import get_client
from acli.errors import handle_boto_errors
from acli.output.efs import output_filesystems


@handle_boto_errors
def efs_list(aws_config=None):
    """
    @type aws_config: Config
    """
    efs_client = get_client(client_type='efs', config=aws_config)
    res = efs_client.describe_file_systems()
    filesystems = res.get('FileSystems')
    if filesystems:
        output_filesystems(filesystems=filesystems)
    else:
        exit("No file systems found.")

#
# @handle_boto_errors
# def efs_info(aws_config=None, domain_name=None):
#     """
#     @type aws_config: Config
#     @type domain_name: unicode
#     """
#     es_client = get_client(client_type='es', config=aws_config)
#     try:
#         domain = es_client.describe_elasticsearch_domains(DomainNames=[domain_name])
#         output_domain_info(domain=domain)
#     except (ClientError, IndexError):
#         exit("Cannot find domain: {0}".format(domain_name))
