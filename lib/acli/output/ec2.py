# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)
from acli.output import (output_ascii_table, dash_if_none)


def get_ec2_instance_tags(ec2_instance=None, tag_key=None,
                          max_length=40):
    """
    @type ec2_instance: ec2.Instance
    @type tag_key: unicode
    @type max_length: int
    """
    if ec2_instance.tags:
        ret = []
        for tag in ec2_instance.tags:
            if tag_key and tag.get('Key') == tag_key:
                return tag.get('Value', "-")
            else:
                val = tag.get('Value', None)
                if val and len(val) > max_length:
                    val = "{0}...".format(val[:max_length-3])
                ret.append('{0}:{1}\n'.format(tag.get('Key'), val))
        return "".join(ret).rstrip()


def get_interfaces(interfaces):
    """
    @type interfaces: list
    """
    ret = list()
    for interface in interfaces:
        ret.append("{0}\n".format(interface.get('NetworkInterfaceId')))
        ret.append(" Attachment:\n")
        for akey, avalue in interface.get('Attachment').iteritems():
                ret.append("  {}:{}\n".format(str(akey), str(avalue)))
        ret.append(" Private IP Addresses:\n")
        for private_ip_address in interface.get('PrivateIpAddresses'):
                for pkey, pvalue in private_ip_address.iteritems():
                    if pkey == "Association":
                        ret.append("  Association:\n")
                        for qqkey, qqvalue in pvalue.iteritems():
                            ret.append("   {}:{}\n".format(qqkey, qqvalue))
                    else:
                        ret.append("  {}:{}\n".format(str(pkey), str(pvalue)))
        ret.append(" Security Groups:\n")
        for group in interface.get('Groups'):
            for gkey, gvalue in group.iteritems():
                ret.append("  {}:{}\n".format(str(gkey), str(gvalue)))
        for key, value in interface.iteritems():
            if str(key) not in ("Attachment", "NetworkInterfaceId",
                                "PrivateIpAddresses", "Groups", "Association",
                                "PrivateIpAddress"):
                ret.append(" {}:{}\n".format(str(key), str(value)))
    return ("".join(ret)).rstrip()


def get_placement_details(placement):
    """
    @type placement: dict
    """
    ret = []
    for key, value in placement.iteritems():
        ret.append("{0}:{1}".format(key, value))
    if ret:
        return "\n".join(ret)


def output_ec2_list(output_media=None, instances=None):
    """
    @type output_media: unicode
    @type instances: list
    """
    if output_media == 'console':
        td = list()
        td.append(['id', 'name', 'state', 'type', 'image',
                   'public ip', 'private ip'])
        instances = sorted(instances,
                           key=lambda k: get_ec2_instance_tags(ec2_instance=k, tag_key='Name'))
        for instance in instances:
            instance_id = instance.instance_id
            instance_state = dash_if_none(instance.state.get('Name', None))
            instance_type = dash_if_none(str(instance.instance_type))
            image_id = dash_if_none(instance.image_id)
            public_ip = dash_if_none(instance.public_ip_address)
            private_ip = dash_if_none(instance.private_ip_address)
            instance_name = dash_if_none(get_ec2_instance_tags(ec2_instance=instance, tag_key='Name'))
            td.append([instance_id,
                       instance_name,
                       instance_state,
                       instance_type,
                       image_id,
                       public_ip,
                       private_ip])
        output_ascii_table(table_title="EC2 Instances",
                           table_data=td,
                           inner_heading_row_border=True)
    exit(0)


def short_instance_profile(instance_profile=None):
    """
    @type instance_profile: dict
    """
    if instance_profile and instance_profile.get('Arn', None):
        return instance_profile.get('Arn', None)


def get_sec_group_names(groups=None):
    """
    @type groups: list
    """
    sec_group_names = [x.name for x in groups]
    return ",".join(sec_group_names)


def get_sec_groups_name_and_id(groups=None):
    """
    @type groups: list
    """
    ret = []
    for group in groups:
        ret.append('GroupName:{}, GroupId:{}'.format(group.get('GroupName', '-'), group.get('GroupId', '-')))
    return "\n".join(ret).rstrip()


def get_interface_ids(interfaces=None):
    """
    @type interfaces: list
    """
    interface_ids = [x.id for x in interfaces]
    return ",".join(interface_ids)


def get_state_reason(state_reason=None):
    """
    @type state_reason: dict
    """
    if state_reason:
        return state_reason.get('Message', None)


def get_block_devices(bdms=None):
    """
    @type bdms: list
    """
    ret = ""
    for bdm in bdms:
        ret += "{0}\n".format(bdm.get('DeviceName', '-'))
        ebs = bdm.get('Ebs', None)
        if ebs:
            ret += " Status: {0}\n".format(ebs.get('Status', '-'))
            ret += " Delete on Termination: {0}\n".format(ebs.get('DeleteOnTermination', '-'))
            ret += " Volume Id: {0}\n".format(ebs.get('VolumeId', '-'))
            ret += " Attach Time: {0}\n".format(str(ebs.get('AttachTime', '-')))
    return ret.rstrip()


def output_ec2_info(output_media=None, instance=None):
    """
    @type output_media: unicode
    @type instance: ec2.Instance
    """
    if output_media == 'console':
        td = list()
        td.append(['id', instance.id])
        td.append(['name', dash_if_none(get_ec2_instance_tags(ec2_instance=instance, tag_key='Name'))])
        td.append(['groups', dash_if_none(get_sec_groups_name_and_id(instance.security_groups))])
        td.append(['public ip', dash_if_none(instance.public_ip_address)])
        td.append(['public dns name', dash_if_none(instance.public_dns_name)])
        td.append(['private ip', dash_if_none(instance.private_ip_address)])
        td.append(['private dns name', dash_if_none(instance.private_dns_name)])
        td.append(['state', dash_if_none(instance.state.get('Name', None))])
        td.append(['key name', dash_if_none(instance.key_name)])
        td.append(['instance type', dash_if_none(instance.instance_type)])
        td.append(['launch time', str(instance.launch_time)])
        td.append(['image id', dash_if_none(instance.image_id)])
        td.append(['placement', get_placement_details(instance.placement)])
        td.append(['monitored', dash_if_none(instance.monitoring.get('State'))])
        td.append(['subnet id', dash_if_none(instance.subnet_id)])
        td.append(['vpc id', dash_if_none(instance.vpc_id)])
        td.append(['root device type', dash_if_none(instance.root_device_type)])
        td.append(['state reason', dash_if_none(get_state_reason(instance.state_reason))])
        td.append(['state transition reason', dash_if_none(instance.state_transition_reason)])
        td.append(['ebs optimized', dash_if_none(instance.ebs_optimized)])
        td.append(['instance profile', dash_if_none(short_instance_profile(instance.iam_instance_profile))])
        td.append(['tags', get_ec2_instance_tags(ec2_instance=instance)])
        td.append(['block devices', get_block_devices(instance.block_device_mappings)])
        td.append(['interfaces', dash_if_none(get_interfaces(instance.network_interfaces))])
        output_ascii_table(table_title="Instance Info",
                           table_data=td)
    exit(0)


def output_ami_list(output_media=None, amis=None):
    """
    @type output_media: unicode
    @type amis: list
    """
    if output_media == 'console':
        td = [['id', 'name', 'created']]
        for ami in amis:
            td.append([ami.id, ami.name, ami.creation_date])
        output_ascii_table(table_title="AMIs",
                           inner_heading_row_border=True,
                           table_data=td)
    exit(0)


def output_ami_permissions(perms=None):
    """
    @type perms: dict
    """
    out = ""
    for i, (key, value) in enumerate(perms.iteritems()):
        out += "{0},{1}".format(key, str(value))
        if i < len(perms)-1:
            out += "\n"
    return out


def get_product_codes(product_codes=None):
    """
    @type product_codes: dict
    """
    out = ""
    for prodcode in product_codes:
        out += "{0}/{1}".format(prodcode.get('ProductCodeId'), prodcode.get('ProductCodeType'))
    return out


def output_ami_info(output_media=None, ami=None):
    """
    @type output_media: unicode
    @type ami: ec2.Ami
    """
    if output_media == 'console':
        td = list()
        td.append(['id', ami.id])
        td.append(['name', ami.name])
        td.append(['creationDate', dash_if_none(ami.creation_date)])
        td.append(['description', dash_if_none(ami.description)])
        td.append(['hypervisor', dash_if_none(ami.hypervisor)])
        td.append(['is_public', dash_if_none(str(ami.public))])
        td.append(['kernel_id', dash_if_none(ami.kernel_id)])
        td.append(['location', dash_if_none(ami.image_location)])
        td.append(['owner_id', dash_if_none(ami.owner_id)])
        td.append(['owner_alias', dash_if_none(ami.image_owner_alias)])
        td.append(['platform', dash_if_none(ami.platform)])
        td.append(['product codes', get_product_codes(ami.product_codes)])
        td.append(['root_device_name', dash_if_none(ami.root_device_name)])
        td.append(['root_device_type', dash_if_none(ami.root_device_type)])
        td.append(['sriov_net_support', dash_if_none(ami.sriov_net_support)])
        td.append(['state', dash_if_none(ami.state)])
        td.append(['virtualization_type', dash_if_none(ami.virtualization_type)])
        td.append(['block_device_mapping', get_block_devices(bdms=ami.block_device_mappings)])
        output_ascii_table(table_title="AMI Info",
                           table_data=td)
    exit(0)
