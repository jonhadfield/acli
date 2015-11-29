# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)
from acli.output.snapshots import (output_snapshot_list)
from acli.connections import get_client


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


# def terminate_unnamed_instances(aws_config=None, noop=False):
#    """
#    @type aws_config: Config
#    @type noop: bool
#    """
