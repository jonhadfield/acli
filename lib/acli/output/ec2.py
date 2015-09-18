from __future__ import (absolute_import, print_function)
from acli.output import (output_ascii_table, dash_if_none, output_tags)


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
                   'public ip', 'private ip'])
        for instance in instances:
            instance_id = instance[0].id
            instance_state = instance[0].state
            instance_type = instance[0].instance_type
            image_id = instance[0].image_id
            public_ip = instance[0].ip_address
            private_ip = instance[0].private_ip_address
            instance_name = get_ec2_instance_name_tag(ec2_instance=instance[0])
            td.append([instance_id,
                       instance_name,
                       instance_state,
                       instance_type,
                       image_id,
                       public_ip if public_ip else '-',
                       private_ip if private_ip else '-'])
        output_ascii_table(table_title="EC2 Instances",
                           table_data=td,
                           inner_heading_row_border=True)
    exit(0)


def short_instance_profile(instance_profile):
    if instance_profile:
        return instance_profile.get('arn').split('/')[-1]


def get_sec_group_names(groups=None):
    sec_group_names = [x.name for x in groups]
    return ",".join(sec_group_names)


def get_interface_ids(interfaces=None):
    interface_ids = [x.id for x in interfaces]
    return ",".join(interface_ids)


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
    exit(0)


def output_amis(output_media=None, amis=None):
    if output_media == 'console':
        td = [['id', 'name', 'created']]
        for ami in amis:
            td.append([ami.id, ami.name, ami.creationDate])
        output_ascii_table(table_title="AMIs",
                           inner_heading_row_border=True,
                           table_data=td)
    exit(0)


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
    exit(0)
