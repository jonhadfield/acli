from __future__ import (absolute_import, print_function)
from boto3.session import Session
from acli.output.asg import (output_asg_list, output_asg_info,
                             output_lc_list, output_lc_info)


def get_boto3_session(aws_config):
    return Session(region_name=aws_config.region,
                   aws_access_key_id=aws_config.access_key_id,
                   aws_secret_access_key=aws_config.secret_access_key)


def asg_list(aws_config=None):
    session = get_boto3_session(aws_config)
    conn = session.client('autoscaling')
    output_asg_list(output_media='console',
                    asg_list=conn.describe_auto_scaling_groups().get('AutoScalingGroups', None))


def asg_info(aws_config=None, asg_name=None):
    session = get_boto3_session(aws_config)
    conn = session.client('autoscaling')
    asg = conn.describe_auto_scaling_groups(AutoScalingGroupNames=[asg_name])
    print(asg.__class__.__name__)
    print(str(asg))
    if asg:
        asg_details = asg.get('AutoScalingGroups')[0]
        print(asg_details.__class__.__name__)
        output_asg_info(output_media='console', asg=asg.get('AutoScalingGroups')[0])
    else:
        exit("Auto Scaling Group: {0} not found.".format(asg_name))


def lc_list(aws_config=None):
    session = get_boto3_session(aws_config)
    conn = session.client('autoscaling')
    output_lc_list(output_media='console',
                   lc_list=conn.describe_launch_configurations().get('LaunchConfigurations', None))


def lc_info(aws_config=None, lc_name=None):
    session = get_boto3_session(aws_config)
    conn = session.client('autoscaling')
    lc = conn.describe_launch_configurations(LaunchConfigurationNames=[lc_name])
    if lc:
        output_lc_info(output_media='console', lc=lc.get('LaunchConfigurations')[0])
    else:
        exit("Launch Configuration: {0} not found.".format(lc_name))
