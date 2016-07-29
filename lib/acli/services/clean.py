# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)

from acli.connections import get_client
from acli.errors import handle_boto_errors
from acli.output.snapshots import (output_snapshot_list)


@handle_boto_errors
def delete_orphaned_snapshots(aws_config=None, noop=False):
    """
    @type aws_config: Config
    @type noop: bool
    """
    account_id = None
    try:
        iam_client = get_client(client_type='iam', config=aws_config)
        users = iam_client.list_users(MaxItems=1)
        if users.get('Users'):
            account_id = users.get('Users')[0]['Arn'].split(':')[4]
    except:
        exit('Unable to get account details. Please check your permissions.')
    if account_id:
        ec2_client = get_client(client_type='ec2', config=aws_config)
        desc_snapshots_result = ec2_client.describe_snapshots(OwnerIds=[account_id])
        snapshots = desc_snapshots_result.get('Snapshots')
        desc_images_result = ec2_client.describe_images()
        images = desc_images_result['Images']
        image_id_list = [image['ImageId'] for image in images]

        orphaned_snapshots = list()
        for snapshot in snapshots:
            snapshot_description = snapshot.get('Description')
            if snapshot_description.startswith('Created by CreateImage'):
                ami_string_start = snapshot_description.find('ami-')
                ami_string_end = snapshot_description.find(' ', ami_string_start)
                ami_id = snapshot_description[ami_string_start:ami_string_end]
                if ami_id not in image_id_list:
                    orphaned_snapshots.append(snapshot)

        if orphaned_snapshots:
            if not noop:
                print("Total snapshots: {}".format(len(snapshots)))
                print("Orphaned snapshots: {}".format(len(orphaned_snapshots)))
                total_deleted = 0
                try:
                    for index, orphaned_snapshot in enumerate(orphaned_snapshots, start=1):
                        ec2_client.delete_snapshot(SnapshotId=orphaned_snapshot.get('SnapshotId'))
                        total_deleted = index

                except:
                    print('An error occurred whilst deleting snapshots.')
                exit('Deleted {0} out of a possible {1}.'.format(total_deleted, len(orphaned_snapshots)))

            else:
                output_snapshot_list(snapshots=orphaned_snapshots)
        else:
            print('No orphaned snapshots were found.')


def delete_unnamed_volumes(aws_config=None, noop=False):
    """
    @type aws_config: Config
    @type noop: bool
    """
    ec2_client = get_client(client_type='ec2', config=aws_config)
    desc_volumes_result = ec2_client.describe_volumes()
    volumes = desc_volumes_result.get('Volumes')
    total_volumes = len(volumes)
    volumes_to_delete = list()
    for volume in volumes:
        volume_has_name = False
        volume_tags = volume.get('Tags')
        if volume_tags:
            for volume_tag in volume_tags:
                if volume_tag.get('Key') and volume_tag.get('Key') == 'Name':
                    volume_has_name = True
                    break
        if not volume_has_name and not volume.get('Attachments'):
            volumes_to_delete.append(volume)
    total_volumes_to_delete = len(volumes_to_delete)
    total_volumes_deleted = 0
    if not noop:
        try:
            for index, volume_to_delete in enumerate(volumes_to_delete, start=1):
                ec2_client.delete_volume(VolumeId=volume_to_delete.get('VolumeId'))
                total_volumes_deleted = index
        except:
            print('An error occurred whislt deleting volumes.')
        if total_volumes_to_delete:
            exit('Deleted {0} volumes out of a total of {1} volumes '
                 'that are unnamed and unattached.'.format(total_volumes_deleted,
                                                           total_volumes_to_delete))
        else:
            exit('No unnamed and unattached volumes were found.')
    elif total_volumes_to_delete:
        exit('There are {0} volumes out of a total of {1} volumes '
             'that are unnamed and unattached.'.format(total_volumes_to_delete,
                                                       total_volumes))
    else:
        exit('No unnamed and unattached volumes were found.')
