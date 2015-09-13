# from tabulate import tabulate
from terminaltables import AsciiTable


def get_ec2_instance_name_tag(ec2_instance=None,
                              max_length=40):
    instance_name = ec2_instance.tags.get('Name', '-')
    if len(instance_name) > max_length:
        return "{0}...".format(instance_name[:max_length-3])
    else:
        return instance_name


def output_ec2_list(output_media=None, instances=None):
    if output_media == 'console':
        table_data = [['id', 'name', 'state', 'type', 'image',
                      'public ip', 'private ip', 'profile']]

        for instance in instances:
            instance_id = instance[0].id
            instance_state = instance[0].state
            instance_type = instance[0].instance_type
            image_id = instance[0].image_id
            public_ip = instance[0].ip_address
            private_ip = instance[0].private_ip_address
            instance_profile = instance[0].instance_profile
            instance_profile_out = '-'
            instance_name = get_ec2_instance_name_tag(ec2_instance=instance[0])
            if instance_profile:
                instance_profile_out = short_instance_profile(instance_profile)
            table_data.append([instance_id,
                               instance_name,
                               instance_state,
                               instance_type,
                               image_id,
                               public_ip if public_ip else '-',
                               private_ip if private_ip else '-',
                               instance_profile_out])
        table = AsciiTable(table_data)
        table.title = "EC2 Instances"
        print(table.table)


def dash_if_none(item=None):
    return item if item else '-'


def short_instance_profile(instance_profile):
    if instance_profile:
        return instance_profile.get('arn').split('/')[-1]


def get_sec_group_names(groups=None):
    sec_group_names = [x.name for x in groups]
    return ",".join(sec_group_names)


def get_interface_ids(interfaces=None):
    interface_ids = [x.id for x in interfaces]
    return ",".join(interface_ids)


def output_elb_instances(instances=None):
    instance_ids = [x.id for x in instances]
    return ",".join(instance_ids)


def output_ec2_info(output_media=None, instance=None):
    if output_media == 'console':
        table_data = [['id', instance.id]]
        table_data.append(['groups', get_sec_group_names(instance.groups)])
        table_data.append(['public ip', dash_if_none(instance.ip_address)])
        table_data.append(['public dns name', dash_if_none(instance.public_dns_name)])
        table_data.append(['private ip', dash_if_none(instance.private_ip_address)])
        table_data.append(['private dns name', dash_if_none(instance.private_dns_name)])
        table_data.append(['state', dash_if_none(instance.state)])
        table_data.append(['previous state', dash_if_none(instance.previous_state)])
        table_data.append(['key name', dash_if_none(instance.key_name)])
        table_data.append(['instance type', dash_if_none(instance.instance_type)])
        table_data.append(['launch time', dash_if_none(instance.launch_time)])
        table_data.append(['image id', dash_if_none(instance.image_id)])
        table_data.append(['placement', dash_if_none(instance.placement)])
        table_data.append(['monitored', dash_if_none(str(instance.monitored))])
        table_data.append(['subnet id', dash_if_none(instance.subnet_id)])
        table_data.append(['vpc id', dash_if_none(instance.vpc_id)])
        table_data.append(['root device type', dash_if_none(instance.root_device_type)])
        table_data.append(['state reason', dash_if_none(instance.state_reason)])
        table_data.append(['interfaces', dash_if_none(get_interface_ids(instance.interfaces))])
        table_data.append(['ebs optimized', dash_if_none(instance.ebs_optimized)])
        table_data.append(['instance profile', dash_if_none(short_instance_profile(instance.instance_profile))])
        table = AsciiTable(table_data)
        table.inner_heading_row_border = False
        table.inner_row_border = False
        table.title = "Instance Info"
        print(table.table)


def output_elbs(output_media=None, elbs=None):
    if output_media == 'console':
        table_data = [['name', 'instances', 'dns_name']]
        for elb in elbs:
            table_data.append([elb.name, str(len(elb.instances)), elb.dns_name])
        table = AsciiTable(table_data)
        table.title = "ELBs"
        print(table.table)


def output_elb_info(output_media=None, elb=None):
    if output_media == 'console':
        table_data = [['name', elb[0].name]]
        table_data.append(['dns name', elb[0].dns_name])
        table_data.append(['listeners', ",".join(elb[0].listeners)])
        table_data.append(['created time', dash_if_none(elb[0].created_time)])
        table_data.append(['instances', output_elb_instances(elb[0].instances)])
        table_data.append(['availability zones', ",".join(elb[0].availability_zones)])
        table_data.append(['source security group', dash_if_none(elb[0].source_security_group.name)])
        table_data.append(['security groups', ",".join(elb[0].security_groups)])
        table_data.append(['subnets', ",".join(elb[0].subnets)])
        table_data.append(['vpc id', dash_if_none(elb[0].vpc_id)])

        table = AsciiTable(table_data)
        table.inner_heading_row_border = False
        table.inner_row_border = False
        table.title = "ELB Info"
        print(table.table)

