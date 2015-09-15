# from tabulate import tabulate
from terminaltables import AsciiTable


def output_ascii_table(table_title=None,
                       table_data=None,
                       inner_heading_row_border=False,
                       inner_row_border=False):
    table = AsciiTable(table_data)
    table.inner_heading_row_border = inner_heading_row_border
    table.inner_row_border = inner_row_border
    table.title = table_title
    print(table.table)


def get_ec2_instance_name_tag(ec2_instance=None,
                              max_length=40):
    instance_name = ec2_instance.tags.get('Name', '-')
    if len(instance_name) > max_length:
        return "{0}...".format(instance_name[:max_length-3])
    else:
        return instance_name


def output_ec2_list(output_media=None, instances=None):
    if output_media == 'console':
        td = list()
        td.append(['id', 'name', 'state', 'type', 'image',
                   'public ip', 'private ip', 'profile'])
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
            td.append([instance_id,
                       instance_name,
                       instance_state,
                       instance_type,
                       image_id,
                       public_ip if public_ip else '-',
                       private_ip if private_ip else '-',
                       instance_profile_out])
        output_ascii_table(table_title="EC2 Instances",
                           table_data=td,
                           inner_heading_row_border=True)


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


def output_tags(tags):
    tag_list = []
    for tag_name, tag_value in tags.iteritems():
        tag_list.append("{0}:{1}".format(tag_name, tag_value))
    if tag_list:
        return ", ".join(tag_list)
    return "-"


def output_name_tag(tags):
    for tag_name, tag_value in tags.iteritems():
        if tag_name == 'Name':
            return tag_value
    return "-"


def output_ec2_info(output_media=None, instance=None):
    if output_media == 'console':
        td = list()
        td.append(['id', instance.id])
        td.append(['name', instance.tags.get('Name', '-')])
        td.append(['groups', get_sec_group_names(instance.groups)])
        td.append(['public ip', dash_if_none(instance.ip_address)])
        td.append(['public dns name', dash_if_none(instance.public_dns_name)])
        td.append(['private ip', dash_if_none(instance.private_ip_address)])
        td.append(['private dns name', dash_if_none(instance.private_dns_name)])
        td.append(['state', dash_if_none(instance.state)])
        td.append(['previous state', dash_if_none(instance.previous_state)])
        td.append(['key name', dash_if_none(instance.key_name)])
        td.append(['instance type', dash_if_none(instance.instance_type)])
        td.append(['launch time', dash_if_none(instance.launch_time)])
        td.append(['image id', dash_if_none(instance.image_id)])
        td.append(['placement', dash_if_none(instance.placement)])
        td.append(['monitored', dash_if_none(str(instance.monitored))])
        td.append(['subnet id', dash_if_none(instance.subnet_id)])
        td.append(['vpc id', dash_if_none(instance.vpc_id)])
        td.append(['root device type', dash_if_none(instance.root_device_type)])
        td.append(['state reason', dash_if_none(instance.state_reason)])
        td.append(['interfaces', dash_if_none(get_interface_ids(instance.interfaces))])
        td.append(['ebs optimized', dash_if_none(instance.ebs_optimized)])
        td.append(['instance profile', dash_if_none(short_instance_profile(instance.instance_profile))])
        td.append(['tags', output_tags(instance.tags)])
        output_ascii_table(table_title="Instance Info",
                           table_data=td)
        return True


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


def output_amis(output_media=None, amis=None):
    if output_media == 'console':
        td = [['id', 'name', 'created']]
        for ami in amis:
            td.append([ami.id, ami.name, ami.creationDate])
        output_ascii_table(table_title="AMIs",
                           inner_heading_row_border=True,
                           table_data=td)


def output_block_device_mapping(bdm=None):
    out = ""
    for i, (key, value) in enumerate(bdm.iteritems()):
        out += "{0},{1},{2}".format(key, value.volume_type, value.size)
        if i < len(bdm)-1:
            out += "\n"
    return out


def output_ami_permissions(perms=None):
    out = ""
    for i, (key, value) in enumerate(perms.iteritems()):
        out += "{0},{1}".format(key, str(value))
        if i < len(perms)-1:
            out += "\n"
    return out


def output_ami_info(output_media=None, ami=None):
    if output_media == 'console':
        td = list()
        td.append(['id', ami.id])
        td.append(['name', ami.name])
        td.append(['creationDate', dash_if_none(ami.creationDate)])
        td.append(['description', dash_if_none(ami.description)])
        td.append(['block_device_mapping', output_block_device_mapping(bdm=ami.block_device_mapping)])
        td.append(['get launch permissions', output_ami_permissions(ami.get_launch_permissions())])
        td.append(['get ramdisk', dash_if_none(str(ami.get_ramdisk()))])
        td.append(['hypervisor', dash_if_none(ami.hypervisor)])
        td.append(['is_public', dash_if_none(str(ami.is_public))])
        td.append(['kernel_id', dash_if_none(ami.kernel_id)])
        td.append(['location', dash_if_none(ami.location)])
        td.append(['owner_id', dash_if_none(ami.owner_id)])
        td.append(['owner_alias', dash_if_none(ami.owner_alias)])
        td.append(['platform', dash_if_none(ami.platform)])
        td.append(['product codes', ",".join(ami.product_codes)])
        td.append(['ramdisk_id', dash_if_none(ami.ramdisk_id)])
        td.append(['region', dash_if_none(str(ami.region.name))])
        td.append(['root_device_name', dash_if_none(ami.root_device_name)])
        td.append(['root_device_type', dash_if_none(ami.root_device_type)])
        td.append(['sriov_net_support', dash_if_none(ami.sriov_net_support)])
        td.append(['state', dash_if_none(ami.state)])
        td.append(['type', dash_if_none(ami.type)])
        td.append(['virtualization_type', dash_if_none(ami.virtualization_type)])
        output_ascii_table(table_title="AMI Info",
                           table_data=td)
