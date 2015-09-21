from __future__ import (absolute_import, print_function)
from boto3.session import Session
from acli.output.asg import (output_asg_list, output_asg_info)


def get_boto3_session(aws_config):
    return Session(region_name=aws_config.region,
                   aws_access_key_id=aws_config.access_key_id,
                   aws_secret_access_key=aws_config.secret_access_key)


def asg_list(aws_config=None):
    session = get_boto3_session(aws_config)
    conn = session.client('autoscaling')
    output_asg_list(output_media='console',
                    asg_list=conn.describe_auto_scaling_groups().get('AutoScalingGroups', None))


def asg_info(aws_config=None, instance_id=None):
    session = get_boto3_session(aws_config)
    conn = session.client('autoscaling')
    output_asg_info(output_media='console',
                    instance=conn.Instance(instance_id))
