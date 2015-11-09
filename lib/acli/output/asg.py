# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)
from acli.output import output_ascii_table, output_ascii_table_list, dash_if_none, get_tags
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


def output_asg_list(asg_list=None):
    """
    @type asg_list: list
    """
    if isinstance(asg_list, list):
        td = list()
        table_header = [Color('{autoblue}name{/autoblue}'), Color('{autoblue}instances{/autoblue}'),
                        Color('{autoblue}desired{/autoblue}'), Color('{autoblue}min{/autoblue}'),
                        Color('{autoblue}max{/autoblue}'),
                        Color('{autoblue}lc{/autoblue}')]
        for asg in asg_list:
            td.append([asg.get('AutoScalingGroupName', '-'),
                       str(len(asg.get('Instances', '-'))),
                       str(asg.get('DesiredCapacity', '-')),
                       str(asg.get('MinSize', '-')),
                       str(asg.get('MaxSize', '-')),
                       asg.get('LaunchConfigurationName', '-')
                       ])
        output_ascii_table_list(table_title=Color('{autowhite}ASGs{/autowhite}'),
                                table_data=td,
                                table_header=table_header,
                                inner_heading_row_border=True)
    exit(0)


def output_asg_info(asg=None):
    """
    @type asg: dict
    """
    td = list()
    td.append([Color('{autoblue}name{/autoblue}'),
               dash_if_none(asg.get('AutoScalingGroupName'))])
    # td.append([Color('{autoblue}arn{/autoblue}'), dash_if_none(asg.get('AutoScalingGroupARN'))])
    td.append([Color('{autoblue}lc{/autoblue}'),
               dash_if_none(asg.get('LaunchConfigurationName'))])
    td.append([Color('{autoblue}min size{/autoblue}'),
               str(dash_if_none(asg.get('MinSize')))])
    td.append([Color('{autoblue}max size{/autoblue}'),
               str(dash_if_none(asg.get('MaxSize')))])
    td.append([Color('{autoblue}desired size{/autoblue}'),
               str(dash_if_none(asg.get('DesiredCapacity')))])
    td.append([Color('{autoblue}default cooldown{/autoblue}'),
               str(dash_if_none(asg.get('DefaultCooldown')))])
    td.append([Color('{autoblue}availability zones{/autoblue}'),
               str(dash_if_none('\n'.join(asg.get('AvailabilityZones'))))])
    td.append([Color('{autoblue}load balancer names{/autoblue}'),
               str(dash_if_none('\n'.join(asg.get('LoadBalancerNames'))))])
    td.append([Color('{autoblue}health check type{/autoblue}'),
               str(dash_if_none(asg.get('HealthCheckType')))])
    td.append([Color('{autoblue}health check grace period{/autoblue}'),
               str(dash_if_none(asg.get('HealthCheckGracePeriod')))])
    td.append([Color('{autoblue}instances{/autoblue}'),
               dash_if_none(get_instances_output(asg.get('Instances')))])
    td.append([Color('{autoblue}created{/autoblue}'),
               str(dash_if_none(asg.get('CreatedTime').replace(tzinfo=None, microsecond=0)))])
    td.append([Color('{autoblue}suspended processes{/autoblue}'),
               dash_if_none(asg.get('SuspendedProcesses'))])
    td.append([Color('{autoblue}placement group{/autoblue}'),
               dash_if_none(asg.get('PlacementGroup'))])
    td.append([Color('{autoblue}vpc zone identifier{/autoblue}'),
               str(dash_if_none(asg.get('VPCZoneIdentifier')))])
    td.append([Color('{autoblue}metrics enabled{/autoblue}'),
               dash_if_none(asg.get('EnabledMetrics'))])
    td.append([Color('{autoblue}status{/autoblue}'),
               dash_if_none(asg.get('Status'))])
    td.append([Color('{autoblue}tags{/autoblue}'),
               dash_if_none(get_tags(asg.get('Tags')))])
    td.append([Color('{autoblue}termination policies{/autoblue}'),
               str(dash_if_none(asg.get('TerminationPolicies')))])
    output_ascii_table(table_title=Color('{autowhite}asg info{/autowhite}'),
                       table_data=td)
    exit(0)


def output_lc_list(lc_list=None):
    """
    @type lc_list: list
    """
    if isinstance(lc_list, list):
        td = list()
        table_header = [Color('{autoblue}name{/autoblue}'),
                        Color('{autoblue}image id{/autoblue}'),
                        Color('{autoblue}instance type{/autoblue}'),
                        Color('{autoblue}created{/autoblue}')]
        for lc in lc_list:
            td.append([
                      dash_if_none(lc.get('LaunchConfigurationName')),
                      dash_if_none(lc.get('ImageId')),
                      dash_if_none(lc.get('InstanceType')),
                      dash_if_none(lc.get('CreatedTime').replace(tzinfo=None, microsecond=0))
                      ])
        output_ascii_table_list(table_title=Color('{autowhite}launch configurations{/autowhite}'),
                                table_header=table_header,
                                table_data=td,
                                inner_heading_row_border=True)
    exit(0)


def output_lc_info(lc=None):
    """
    @type lc: dict
    """
    td = list()
    td.append([Color('{autoblue}name{/autoblue}'),
               dash_if_none(lc.get('LaunchConfigurationName'))])
    td.append([Color('{autoblue}image id{/autoblue}'),
               dash_if_none(lc.get('ImageId'))])
    td.append([Color('{autoblue}instance type{/autoblue}'),
               dash_if_none(lc.get('InstanceType'))])
    td.append([Color('{autoblue}created (UTC){/autoblue}'),
               str(dash_if_none(lc.get('CreatedTime').replace(tzinfo=None, microsecond=0)))])
    td.append([Color('{autoblue}iam instance profile{/autoblue}'),
               dash_if_none(lc.get('IamInstanceProfile'))])
    td.append([Color('{autoblue}ebs optimised{/autoblue}'),
               dash_if_none("Yes" if lc.get('EbsOptimized') else "No")])
    td.append([Color('{autoblue}instance monitoring{/autoblue}'),
               dash_if_none("Yes" if lc.get('InstanceMonitoring').get('Enabled') else "No")])
    td.append([Color('{autoblue}classiclink VPC sec groups{/autoblue}'),
               dash_if_none(lc.get('ClassicLinkVPCSecurityGroups'))])
    td.append([Color('{autoblue}block device mappings{/autoblue}'),
               dash_if_none(lc.get('BlockDeviceMappings'))])
    td.append([Color('{autoblue}keypair{/autoblue}'),
               dash_if_none(lc.get('KeyName'))])
    td.append([Color('{autoblue}security groups{/autoblue}'),
               dash_if_none(", ".join(lc.get('SecurityGroups')))])
    td.append([Color('{autoblue}kernel ID{/autoblue}'),
               dash_if_none(lc.get('KernelId'))])
    td.append([Color('{autoblue}ramdisk id{/autoblue}'),
               dash_if_none(lc.get('RamdiskId'))])
    td.append([Color('{autoblue}image id{/autoblue}'),
               dash_if_none(lc.get('ImageId'))])
    td.append([Color('{autoblue}instance typr{/autoblue}'),
               dash_if_none(lc.get('InstanceType'))])
    td.append([Color('{autoblue}associate public ip{/autoblue}'),
               dash_if_none(lc.get('AssociatePublicIpAddress'))])
    td.append([Color('{autoblue}user data{/autoblue}'),
               dash_if_none(lc.get('UserData'))])
    output_ascii_table(table_title=Color('{autowhite}launch configuration info{/autowhite}'),
                       table_data=td)
    exit(0)
