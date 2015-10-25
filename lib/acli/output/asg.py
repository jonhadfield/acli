# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)
from acli.output import output_ascii_table, dash_if_none, get_tags
from colorclass import Color, Windows
Windows.enable(auto_colors=True, reset_atexit=True)


def get_instances_output(instances):
    """
    @type instances: list
    """
    ret = ""
    for instance in instances:
        ret += "{0}\n".format(instance.get('InstanceId'))
    if ret:
        return ret.rstrip()


def output_asg_list(output_media=None, asg_list=None):
    """
    @type output_media: unicode
    @type asg_list: list
    """
    if isinstance(asg_list, list):
        if output_media == 'console':
            td = [[Color('{autoblue}name{/autoblue}'), Color('{autoblue}instances{/autoblue}'), Color('{autoblue}min{/autoblue}'), Color('{autoblue}max{/autoblue}'), Color('{autoblue}lc{/autoblue}')]]
            for asg in asg_list:
                td.append([asg.get('AutoScalingGroupName', '-'),
                           str(len(asg.get('Instances', '-'))),
                           str(asg.get('MinSize', '-')),
                           str(asg.get('MaxSize', '-')),
                           asg.get('LaunchConfigurationName', '-')
                           ])
            output_ascii_table(table_title=Color('{autowhite}ASGs{/autowhite}'),
                               table_data=td,
                               inner_heading_row_border=True)
    exit(0)


def output_asg_info(output_media=None, asg=None):
    """
    @type output_media: unicode
    @type asg: dict
    """
    if output_media == 'console':
        td = list()
        td.append(['name', dash_if_none(asg.get('AutoScalingGroupName'))])
        td.append(['arn', dash_if_none(asg.get('AutoScalingGroupARN'))])
        td.append(['lc', dash_if_none(asg.get('LaunchConfigurationName'))])
        td.append(['min size', str(dash_if_none(asg.get('MinSize')))])
        td.append(['max size', str(dash_if_none(asg.get('MaxSize')))])
        td.append(['desired size', str(dash_if_none(asg.get('DesiredCapacity')))])
        td.append(['default cooldown', str(dash_if_none(asg.get('DefaultCooldown')))])
        td.append(['availability zones', str(dash_if_none(asg.get('AvailabilityZones')))])
        td.append(['load balancer names', str(dash_if_none(asg.get('LoadBalancerNames')))])
        td.append(['health check type', str(dash_if_none(asg.get('HealthCheckType')))])
        td.append(['HealthCheckGracePeriod', str(dash_if_none(asg.get('HealthCheckGracePeriod')))])
        td.append(['instances', dash_if_none(get_instances_output(asg.get('Instances')))])
        td.append(['CreatedTime', str(dash_if_none(asg.get('CreatedTime')))])
        td.append(['SuspendedProcesses', str(dash_if_none(asg.get('SuspendedProcesses')))])
        td.append(['PlacementGroup', str(dash_if_none(asg.get('PlacementGroup')))])
        td.append(['VPCZoneIdentifier', str(dash_if_none(asg.get('VPCZoneIdentifier')))])
        td.append(['EnabledMetrics', str(dash_if_none(asg.get('EnabledMetrics')))])
        td.append(['Status', str(dash_if_none(asg.get('Status')))])
        td.append(['Tags', dash_if_none(get_tags(asg.get('Tags')))])
        td.append(['TerminationPolicies', str(dash_if_none(asg.get('TerminationPolicies')))])
        output_ascii_table(table_title=Color('{autowhite}asg info{/autowhite}'),
                           table_data=td)
    exit(0)


def output_lc_list(output_media=None, lc_list=None):
    """
    @type output_media: unicode
    @type lc_list: list
    """
    if isinstance(lc_list, list):
        if output_media == 'console':
            td = [[Color('{autoblue}name{/autoblue}'), Color('{autoblue}image id{/autoblue}'),
                   Color('{autoblue}instance type{/autoblue}'), Color('{autoblue}created{/autoblue}')]]
            for lc in lc_list:
                td.append([lc.get('LaunchConfigurationName', '-'),
                           str(lc.get('ImageId', '-')),
                           str(lc.get('InstanceType', '-')),
                           str(lc.get('CreatedTime', '-'))
                           ])
            output_ascii_table(table_title=Color('{autowhite}launch configurations{/autowhite}'),
                               table_data=td,
                               inner_heading_row_border=True)
    exit(0)


def output_lc_info(output_media=None, lc=None):
    """
    @type output_media: unicode
    @type lc: dict
    """
    pass
    if output_media == 'console':
        td = list()
        td.append(['name', dash_if_none(lc.get('LaunchConfigurationName'))])
        td.append(['arn', dash_if_none(lc.get('ImageId'))])
        td.append(['lc', dash_if_none(lc.get('InstanceType'))])
        td.append(['created', str(dash_if_none(lc.get('CreatedTime')))])
        td.append(['iam instance profile', str(dash_if_none(lc.get('IamInstanceProfile')))])
        td.append(['ebs optimised', str(dash_if_none(lc.get('EbsOptimized')))])
        td.append(['instance monitoring', str(dash_if_none(lc.get('InstanceMonitoring')))])
        td.append(['classiclink vpc security groups', str(dash_if_none(lc.get('ClassicLinkVPCSecurityGroups')))])
        td.append(['block device mappings', str(dash_if_none(lc.get('BlockDeviceMappings')))])
        td.append(['key name', str(dash_if_none(lc.get('KeyName')))])
        td.append(['security groups', str(dash_if_none(lc.get('SecurityGroups')))])
        td.append(['kernel ID', str(dash_if_none(lc.get('KernelId')))])
        td.append(['ramdisk ID', str(dash_if_none(lc.get('RamdiskId')))])
        td.append(['image ID', str(dash_if_none(lc.get('ImageId')))])
        td.append(['Instance Type', str(dash_if_none(lc.get('InstanceType')))])
        td.append(['associate public IP', str(dash_if_none(lc.get('AssociatePublicIpAddress')))])
        td.append(['user data', str(dash_if_none(lc.get('UserData')))])
        output_ascii_table(table_title=Color('{autowhite}launch configuration info{/autowhite}'),
                           table_data=td)
    exit(0)
