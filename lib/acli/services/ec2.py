from __future__ import (absolute_import, print_function)
import boto.ec2
from acli.output.ec2 import (output_ec2_list, output_ec2_info,
                             output_amis, output_ami_info)


def get_ec2_conn(aws_config):
    return boto.ec2.connect_to_region(region_name=aws_config.region,
                                      aws_access_key_id=aws_config.access_key_id,
                                      aws_secret_access_key=aws_config.secret_access_key)


def get_ec2_list(aws_config):
    ec2_conn = get_ec2_conn(aws_config)
    reservations = [reservation for reservation in ec2_conn.get_all_instances()]
    instances = []
    for reservation in reservations:
        instances.append(reservation.instances)
    return instances


def get_ec2_instance(aws_config, instance_id=None):
    if instance_id:
        ec2_conn = get_ec2_conn(aws_config)
        reservations = ec2_conn.get_all_instances(instance_ids=[instance_id])
        return reservations[0].instances[0]


def ec2_list(aws_config):
    output_ec2_list(output_media='console',
                    instances=get_ec2_list(aws_config))


def ec2_info(aws_config=None, instance_id=None):
    output_ec2_info(output_media='console',
                    instance=get_ec2_instance(aws_config, instance_id=instance_id))


def get_ami_list(aws_config):
    ec2_conn = get_ec2_conn(aws_config)
    return ec2_conn.get_all_images(owners=['self'])


def ami_info(aws_config=None, ami_id=None):
    output_ami_info(output_media='console',
                    ami=get_ami(aws_config,
                                ami_id=ami_id))


def list_amis(aws_config):
    output_amis(output_media='console',
                amis=get_ami_list(aws_config))


def get_ami(aws_config, ami_id=None):
    if ami_id:
        ec2_conn = get_ec2_conn(aws_config)
        all_matching_images = ec2_conn.get_all_images(image_ids=[ami_id])
        if all_matching_images:
            return all_matching_images[0]
