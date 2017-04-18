# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)

from botocore.exceptions import ClientError

from acli.connections import get_client
from acli.errors import handle_boto_errors
from acli.output.efs import output_filesystems, output_filesystem_info


@handle_boto_errors
def efs_list(aws_config=None):
    """
    @type aws_config: Config
    """
    efs_client = get_client(client_type='efs', config=aws_config)
    res = efs_client.describe_file_systems()
    filesystems = res.get('FileSystems')
    mount_targets = list()
    for fs in filesystems:
        res = efs_client.describe_mount_targets(FileSystemId=fs.get('FileSystemId'))
        for mt in res.get('MountTargets'):
            mount_targets.append(mt)
    if filesystems:
        output_filesystems(filesystems=filesystems, mount_targets=mount_targets)
    else:
        exit("No file systems found.")


@handle_boto_errors
def efs_info(aws_config=None, filesystem_id=None):
    """
    @type aws_config: Config
    @type filesystem_id: unicode
    """
    efs_client = get_client(client_type='efs', config=aws_config)
    try:
        filesystem = efs_client.describe_file_systems(FileSystemId=filesystem_id)
        mount_targets = list()
        res = efs_client.describe_mount_targets(FileSystemId=filesystem['FileSystems'][0]['FileSystemId'])
        for mt in res.get('MountTargets'):
            mount_targets.append(mt)
        output_filesystem_info(filesystem=filesystem, mount_targets=mount_targets)
    except (ClientError, IndexError):
        exit("Cannot find filesystem: {0}".format(filesystem_id))
