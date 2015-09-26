from __future__ import (absolute_import, print_function)
from boto3.session import Session
from acli.output.ec2 import (output_ec2_list, output_ec2_info,
                             output_ami_list, output_ami_info)


def get_boto3_session(aws_config):
    return Session(region_name=aws_config.region,
                   aws_access_key_id=aws_config.access_key_id,
                   aws_secret_access_key=aws_config.secret_access_key)


def ec2_list(aws_config=None):
    session = get_boto3_session(aws_config)
    conn = session.resource('ec2')
    output_ec2_list(output_media='console', instances=conn.instances.all())


def ec2_info(aws_config=None, instance_id=None):
    session = get_boto3_session(aws_config)
    conn = session.resource('ec2')
    output_ec2_info(output_media='console',
                    instance=conn.Instance(instance_id))


def ami_info(aws_config=None, ami_id=None):
    session = get_boto3_session(aws_config)
    conn = session.resource('ec2')
    ami = None
    for image in conn.images.filter(ImageIds=[ami_id]):
        ami = image
    output_ami_info(output_media='console',
                    ami=ami)


def ami_list(aws_config):
    session = get_boto3_session(aws_config)
    conn = session.resource('ec2')
    output_ami_list(output_media='console',
                    amis=conn.images.filter(Owners=['self']))


def ec2_get_vol_ids(session=None, aws_config=None, instance_id=None):
    conn = session.resource('ec2')
    ec2_instance = conn.instances.filter(InstanceIds=[instance_id])
    vol_ids = list()
    for instance in ec2_instance:
        for bdm in instance.block_device_mappings:
            vol_ids.append(bdm['Ebs']['VolumeId'])
    return vol_ids



