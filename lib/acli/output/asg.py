from acli.output import output_ascii_table, dash_if_none, get_tags


def get_instances_output(instances):
    ret = ""
    for instance in instances:
        ret += "{0}\n".format(instance.get('InstanceId'))
    if ret:
        return ret.rstrip()


def output_asg_list(output_media=None, asg_list=None):
    if isinstance(asg_list, list):
        if output_media == 'console':
            td = [['name', 'instances', 'min', 'max', 'lc']]
            for asg in asg_list:
                td.append([asg.get('AutoScalingGroupName', '-'),
                           str(len(asg.get('Instances', '-'))),
                           str(asg.get('MinSize', '-')),
                           str(asg.get('MaxSize', '-')),
                           asg.get('LaunchConfigurationName', '-')
                           ])
            output_ascii_table(table_title="ASGs",
                               table_data=td,
                               inner_heading_row_border=True)
    exit(0)


def output_asg_info(output_media=None, asg=None):
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
        td.append(['Tags', get_tags(asg.get('Tags'))])
        td.append(['TerminationPolicies', str(dash_if_none(asg.get('TerminationPolicies')))])
        output_ascii_table(table_title="ASG Info",
                           table_data=td)
    exit(0)
