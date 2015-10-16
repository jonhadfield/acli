# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)
from acli.output import output_ascii_table, dash_if_none


def get_elb_instances(instances=None):
    """
    @type instances: list
    """
    instance_ids = [x.id for x in instances]
    return ",".join(instance_ids)


def output_elbs(output_media=None, elbs=None):
    """
    @type output_media: unicode
    @type elbs: list
    """
    if elbs:
        elbs.sort(key=lambda k: k.get('DNSName'))
        if output_media == 'console':
            td = [['name', 'instances', 'dns_name']]
            for elb in elbs:
                td.append([elb.get('LoadBalancerName'), str(len(elb.get('Instances'))), elb.get('DNSName')])
            output_ascii_table(table_title="ELBs",
                               table_data=td,
                               inner_heading_row_border=True)
    else:
        print("No ELBs found.")
    exit(0)


def get_elb_policies(policies=None):
    """
    @type policies: Policies
    """
    print(policies.__class__.__name__)
    output = ""
    if policies.app_cookie_stickiness_policies:
        for acsp in policies.app_cookie_stickiness_policies:
            output += "{0}\n".format(str(acsp))
    if policies.lb_cookie_stickiness_policies:
        for lcsp in policies.lb_cookie_stickiness_policies:
            output += "{0}\n".format(str(lcsp))
    if policies.other_policies:
        for op in policies.lb_cookie_stickiness_policies:
            output += "{0}\n".format(str(op))
    if output:
        return output.rstrip()


def get_elb_listeners(listeners=None):
    """
    @type listeners: list
    """
    output = ""
    print(listeners)
    for listener in listeners:
        print(listener.__class__.__name__)
        print(listener)
        output += "LB Port: {0} " \
                  "Instance Port: {1} " \
                  "Protocol: {2} " \
                  "Instance Protocol: " \
                  "{3}\n".format(listener.get('LoadBalancerPort'),
                                 listener.get('InstancePort'),
                                 listener.get('Protocol'),
                                 listener.get('InstanceProtocol'))
    if output:
        return output.rstrip()


def get_source_secgroup_name(source_secgroup=None):
    if source_secgroup:
        return source_secgroup.get('GroupName')


def output_elb_info(output_media=None, elb=None):
    """
    @type output_media: unicode
    @type elb: dict
    """
    if output_media == 'console':
        td = list()
        td.append(['name', elb.get('LoadBalancerName')])
        td.append(['dns name', elb.get('DNSName')])
        # print(elb.get('ListenerDescriptions'))
        td.append(['listeners', dash_if_none(get_elb_listeners(elb.get('ListenerDescriptions')))])
        td.append(['canonical hosted zone name', dash_if_none(elb.get('CanonicalHostedZoneName'))])
        td.append(['canonical hosted zone name id', dash_if_none(elb.get('CanonicalHostedZoneNameID'))])
        # td.append(['connection', str(elb.connection)])
        # td.append(['policies', dash_if_none(get_elb_policies(elb.get('Policies)))])
        td.append(['health check', str(elb.get('HealthCheck'))])
        td.append(['created time', str(dash_if_none(elb.get('CreatedTime')))])
        # td.append(['instances', get_elb_instances(elb.get('Instances'))])
        td.append(['availability zones', ",".join(elb.get('AvailabilityZones'))])
        td.append(['source security group',
                   dash_if_none(get_source_secgroup_name(elb.get('SourceSecurityGroup', None)))])
        td.append(['security groups', ",".join(elb.get('SecurityGroups'))])
        td.append(['subnets', ",".join(elb.get('Subnets'))])
        td.append(['vpc id', dash_if_none(elb.get('VPCId'))])
        output_ascii_table(table_title="ELB Info",
                           table_data=td)
    exit(0)
