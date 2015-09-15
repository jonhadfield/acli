from acli.output import output_ascii_table, dash_if_none


def output_elb_instances(instances=None):
    instance_ids = [x.id for x in instances]
    return ",".join(instance_ids)


def output_elbs(output_media=None, elbs=None):
    if output_media == 'console':
        td = [['name', 'instances', 'dns_name']]
        for elb in elbs:
            td.append([elb.name, str(len(elb.instances)), elb.dns_name])
        output_ascii_table(table_title="ELBs",
                           table_data=td,
                           inner_heading_row_border=True)


def output_elb_info(output_media=None, elb=None):
    if output_media == 'console':
        td = list()
        td.append(['name', elb[0].name])
        td.append(['dns name', elb[0].dns_name])
        td.append(['listeners', str(elb[0].listeners)])
        td.append(['canonical hosted zone name', dash_if_none(elb[0].canonical_hosted_zone_name)])
        td.append(['canonical hosted zone name id', dash_if_none(elb[0].canonical_hosted_zone_name_id)])
        td.append(['connection', str(elb[0].connection)])
        td.append(['policies', str(elb[0].policies)])
        td.append(['health check', str(elb[0].health_check)])
        td.append(['created time', dash_if_none(elb[0].created_time)])
        td.append(['instances', output_elb_instances(elb[0].instances)])
        td.append(['availability zones', ",".join(elb[0].availability_zones)])
        td.append(['source security group', dash_if_none(elb[0].source_security_group.name)])
        td.append(['security groups', ",".join(elb[0].security_groups)])
        td.append(['subnets', ",".join(elb[0].subnets)])
        td.append(['vpc id', dash_if_none(elb[0].vpc_id)])
        output_ascii_table(table_title="ELB Info",
                           table_data=td)