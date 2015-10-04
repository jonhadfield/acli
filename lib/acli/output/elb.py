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
        if output_media == 'console':
            td = [['name', 'instances', 'dns_name']]
            for elb in elbs:
                td.append([elb.name, str(len(elb.instances)), elb.dns_name])
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
    for listener in listeners:
        output += "LB Port: {0} Instance Port: {1} Protocol: {2}\n".format(listener[0], listener[1], listener[2])
    if output:
        return output.rstrip()


def output_elb_info(output_media=None, elb=None):
    """
    @type output_media: unicode
    @type elb: list
    """
    if output_media == 'console':
        td = list()
        td.append(['name', elb[0].name])
        td.append(['dns name', elb[0].dns_name])
        td.append(['listeners', dash_if_none(get_elb_listeners(elb[0].listeners))])
        td.append(['canonical hosted zone name', dash_if_none(elb[0].canonical_hosted_zone_name)])
        td.append(['canonical hosted zone name id', dash_if_none(elb[0].canonical_hosted_zone_name_id)])
        td.append(['connection', str(elb[0].connection)])
        td.append(['policies', dash_if_none(get_elb_policies(elb[0].policies))])
        td.append(['health check', str(elb[0].health_check)])
        td.append(['created time', dash_if_none(elb[0].created_time)])
        td.append(['instances', get_elb_instances(elb[0].instances)])
        td.append(['availability zones', ",".join(elb[0].availability_zones)])
        td.append(['source security group', dash_if_none(elb[0].source_security_group.name)])
        td.append(['security groups', ",".join(elb[0].security_groups)])
        td.append(['subnets', ",".join(elb[0].subnets)])
        td.append(['vpc id', dash_if_none(elb[0].vpc_id)])
        output_ascii_table(table_title="ELB Info",
                           table_data=td)
    exit(0)
