# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)

from acli.connections import get_client
from acli.errors import handle_boto_errors
from acli.output.asg import (output_asg_list, output_asg_info,
                             output_lc_list, output_lc_info)


@handle_boto_errors
def asg_list(aws_config=None):
    """
    @type aws_config: Config
    """
    asg_client = get_client(client_type='autoscaling', config=aws_config)
    all_asgs = asg_client.describe_auto_scaling_groups().get('AutoScalingGroups')
    if all_asgs:
        output_asg_list(asg_list=all_asgs)
    else:
        exit("No auto scaling groups were found.")


@handle_boto_errors
def asg_info(aws_config=None, asg_name=None):
    """
    @type aws_config: Config
    @type asg_name: unicode
    """
    asg_client = get_client(client_type='autoscaling', config=aws_config)
    asg = asg_client.describe_auto_scaling_groups(AutoScalingGroupNames=[asg_name])
    if asg.get('AutoScalingGroups'):
        output_asg_info(asg=asg.get('AutoScalingGroups')[0])
    else:
        exit("Auto Scaling Group: {0} not found.".format(asg_name))


@handle_boto_errors
def asg_delete(aws_config=None, asg_name=None):
    """
    @type aws_config: Config
    @type asg_name: unicode
    """
    asg_client = get_client(client_type='autoscaling', config=aws_config)
    asg = asg_client.describe_auto_scaling_groups(AutoScalingGroupNames=[asg_name])
    if asg.get('AutoScalingGroups'):
        asg_instance = asg.get('AutoScalingGroups')[0]
        asg_instance_name = asg_instance.get('AutoScalingGroupName')
        asg_client.update_auto_scaling_group(
            AutoScalingGroupName=asg_instance_name,
            MinSize=0,
            MaxSize=0,
        )
        asg_client.delete_auto_scaling_group(
            AutoScalingGroupName=asg_instance_name,
            ForceDelete=False
        )
        exit("Auto Scaling Group {0} is being deleted.".format(asg_instance_name))
    else:
        exit("Auto Scaling Group: {0} not found.".format(asg_name))


@handle_boto_errors
def lc_list(aws_config=None):
    """
    @type aws_config: Config
    """
    asg_client = get_client(client_type='autoscaling', config=aws_config)
    all_lcs = asg_client.describe_launch_configurations().get('LaunchConfigurations')
    if all_lcs:
        output_lc_list(lc_list=all_lcs)
    else:
        exit("No launch configurations were found.")


@handle_boto_errors
def lc_info(aws_config=None, lc_name=None):
    """
    @type aws_config: Config
    @type lc_name: unicode
    """
    asg_client = get_client(client_type='autoscaling', config=aws_config)
    lc = asg_client.describe_launch_configurations(LaunchConfigurationNames=[lc_name])
    lc_details = lc.get('LaunchConfigurations')
    if lc_details:
        output_lc_info(lc=lc_details[0])
    else:
        exit("Launch Configuration: {0} not found.".format(lc_name))
