# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)
from acli.output import output_ascii_table, output_ascii_table_list, dash_if_none
from colorclass import Color, Windows
from external.six import iteritems

Windows.enable(auto_colors=True, reset_atexit=True)


def get_elb_instances(instances=None):
    """
    @type instances: list
    """
    instance_ids = [x.id for x in instances]
    return ",".join(instance_ids)


def output_elbs(elbs=None):
    """
    @type elbs: list
    """
    if elbs:
        elbs.sort(key=lambda k: k.get('DNSName'))
        td = list()
        table_header = [Color('{autoblue}name{/autoblue}'),
                        Color('{autoblue}instances{/autoblue}'),
                        Color('{autoblue}dns name{/autoblue}')]
        for elb in elbs:
            td.append([elb.get('LoadBalancerName'), str(len(elb.get('Instances'))), elb.get('DNSName')])
        output_ascii_table_list(table_title=Color('{autowhite}ELBs{/autowhite}'),
                                table_data=td,
                                table_header=table_header,
                                inner_heading_row_border=True)
    else:
        print("No ELBs found.")
    exit(0)


def get_elb_policies(policies=None):
    """
    @type policies: Policies
    """
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
    for listener in listeners:
        listener_config = listener.get('Listener')
        output += "LB Port: {0} \n" \
                  "LB Protocol: {1} \n" \
                  "Instance Port: {2} \n" \
                  "Instance Protocol: " \
                  "{3}\n".format(listener_config.get('LoadBalancerPort', '-'),
                                 listener_config.get('Protocol', '-'),
                                 listener_config.get('InstancePort', '-'),
                                 listener_config.get('InstanceProtocol', '-'))
    if output:
        return output.rstrip()


def get_source_secgroup_name(source_secgroup=None):
    if source_secgroup:
        return source_secgroup.get('GroupName')


def get_healthcheck(hc=None):
    if hc:
        out = str()
        for key, value in iteritems(hc):
            out += "{0}: {1}\n".format(key, value)
        return out.rstrip()


def output_elb_info(elb=None):
    """
    @type elb: dict
    """
    td = list()
    td.append([Color('{autoblue}name{/autoblue}'),
               elb.get('LoadBalancerName')])
    td.append([Color('{autoblue}dns name{/autoblue}'),
               elb.get('DNSName')])
    # print(elb.get('ListenerDescriptions'))
    td.append([Color('{autoblue}listeners{/autoblue}'),
               dash_if_none(get_elb_listeners(elb.get('ListenerDescriptions')))])
    td.append([Color('{autoblue}canonical hosted zone name{/autoblue}'),
               dash_if_none(elb.get('CanonicalHostedZoneName'))])
    td.append([Color('{autoblue}canonical hosted zone name id{/autoblue}'),
               dash_if_none(elb.get('CanonicalHostedZoneNameID'))])
    # td.append(['connection', str(elb.connection)])
    # td.append(['policies', dash_if_none(get_elb_policies(elb.get('Policies)))])
    td.append([Color('{autoblue}health check{/autoblue}'),
               dash_if_none(get_healthcheck(elb.get('HealthCheck')))])
    td.append([Color('{autoblue}created{/autoblue}'),
               str(dash_if_none(elb.get('CreatedTime').replace(tzinfo=None, microsecond=0)))])
    # td.append(['instances', get_elb_instances(elb.get('Instances'))])
    td.append([Color('{autoblue}availability zones{/autoblue}'),
               ",".join(elb.get('AvailabilityZones'))])
    td.append([Color('{autoblue}source security group{/autoblue}'),
               dash_if_none(get_source_secgroup_name(elb.get('SourceSecurityGroup')))])
    td.append([Color('{autoblue}security groups{/autoblue}'),
               ",".join(elb.get('SecurityGroups'))])
    td.append([Color('{autoblue}subnets{/autoblue}'),
               ",".join(elb.get('Subnets'))])
    td.append([Color('{autoblue}vpc id{/autoblue}'),
               dash_if_none(elb.get('VPCId'))])
    output_ascii_table(table_title=Color('{autowhite}elb info{/autowhite}'),
                       table_data=td)
    exit(0)
