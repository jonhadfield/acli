# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)
from acli.output import (output_ascii_table, dash_if_none)
import six


def get_ec2_instance_tags(ec2_instance=None, tag_key=None,
                          max_length=40):
    """
    @type ec2_instance: ec2.Instance
    @type tag_key: unicode
    @type max_length: int
    """
    if ec2_instance.get('Tags', None):
        ret = []
        for tag in ec2_instance.get('Tags'):
            if tag_key and tag.get('Key') == tag_key:
                return tag.get('Value', "-")
            else:
                val = tag.get('Value', None)
                if val and len(val) > max_length:
                    val = "{0}...".format(val[:max_length-3])
                ret.append('{0}:{1}\n'.format(tag.get('Key'), val))
        return "".join(ret).rstrip()
    else:
        return ""


def get_interfaces(interfaces):
    """
    @type interfaces: list
    """
    ret = list()
    for interface in interfaces:
        ret.append("{0}\n".format(interface.get('NetworkInterfaceId')))
        ret.append(" Attachment:\n")
        for akey, avalue in six.iteritems(interface.get('Attachment')):
                ret.append("  {}:{}\n".format(str(akey), str(avalue)))
        ret.append(" Private IP Addresses:\n")
        for private_ip_address in interface.get('PrivateIpAddresses'):
                for pkey, pvalue in six.iteritems(private_ip_address):
                    if pkey == "Association":
                        ret.append("  Association:\n")
                        for qqkey, qqvalue in six.iteritems(pvalue):
                            ret.append("   {}:{}\n".format(qqkey, qqvalue))
                    else:
                        ret.append("  {}:{}\n".format(str(pkey), str(pvalue)))
        ret.append(" Security Groups:\n")
        for group in interface.get('Groups'):
            for gkey, gvalue in six.iteritems(group):
                ret.append("  {}:{}\n".format(str(gkey), str(gvalue)))
        for key, value in six.iteritems(interface):
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
    for key, value in six.iteritems(placement):
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
            if instance:
                instance_id = instance.get('InstanceId')
                instance_state = dash_if_none(instance.get('State').get('Name', None))
                instance_type = dash_if_none(str(instance.get('InstanceType', None)))
                image_id = dash_if_none(instance.get('ImageId'))
                public_ip = dash_if_none(instance.get('PublicIpAddress', None))
                private_ip = dash_if_none(instance.get('PrivateIpAddress', None))
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
    if bdms:
        for bdm in bdms:
            ret += "{0}\n".format(bdm.get('DeviceName', '-'))
            ebs = bdm.get('Ebs', None)
            if ebs:
                ret += " Status: {0}\n".format(ebs.get('Status', '-'))
                ret += " Snapshot Id: {0}\n".format(ebs.get('SnapshotId', '-'))
                ret += " Volume Size: {0}\n".format(ebs.get('VolumeSize', '-'))
                ret += " Volume Type: {0}\n".format(ebs.get('VolumeType', '-'))
                ret += " Encrypted: {0}\n".format(str(ebs.get('Encrypted', '-')))
                ret += " Delete on Termination: {0}\n".format(ebs.get('DeleteOnTermination', '-'))
                ret += " Attach Time: {0}\n".format(str(ebs.get('AttachTime', '-')))
        return ret.rstrip()
    else:
        return ret


def output_ec2_info(output_media=None, instance=None):
    """
    @type output_media: unicode
    @type instance: ec2.Instance
    """
    if output_media == 'console':
        td = list()
        td.append(['id', instance.get('InstanceId')])
        td.append(['name', dash_if_none(get_ec2_instance_tags(ec2_instance=instance, tag_key='Name'))])
        td.append(['groups', dash_if_none(get_sec_groups_name_and_id(instance.get('SecurityGroups')))])
        td.append(['public ip', dash_if_none(instance.get('PublicIpAddress', None))])
        td.append(['public dns name', dash_if_none(instance.get('PublicDnsName', None))])
        td.append(['private ip', dash_if_none(instance.get('PrivateIpAddress', None))])
        td.append(['private dns name', dash_if_none(instance.get('PrivateDnsName', None))])
        td.append(['state', str(dash_if_none(instance.get('State', None)))])
        td.append(['key name', dash_if_none(instance.get('KeyName', None))])
        td.append(['instance type', dash_if_none(instance.get('InstanceType', None))])
        td.append(['launch time', str(instance.get('LaunchTime'))])
        td.append(['image id', dash_if_none(instance.get('ImageId'))])
        td.append(['placement', get_placement_details(instance.get('Placement'))])
        td.append(['monitored', str(dash_if_none(instance.get('Monitoring')))])
        td.append(['subnet id', dash_if_none(instance.get('SubnetId'))])
        td.append(['vpc id', dash_if_none(instance.get('VpcId'))])
        td.append(['root device type', dash_if_none(instance.get('RootDeviceType', None))])
        td.append(['state transition reason', dash_if_none(instance.get('StateTransitionReason', None))])
        td.append(['ebs optimized', dash_if_none(instance.get('EbsOptimized', None))])
        td.append(['instance profile', dash_if_none(short_instance_profile(instance.get('IamInstanceProfile', None)))])
        td.append(['tags', get_ec2_instance_tags(ec2_instance=instance)])
        td.append(['block devices', get_block_devices(instance.get('BlockDeviceMappings'))])
        td.append(['interfaces', dash_if_none(get_interfaces(instance.get('NetworkInterfaces', None)))])
        output_ascii_table(table_title="Instance Info",
                           table_data=td)
    exit(0)


def output_ami_list(output_media=None, amis=None):
    """
    @type output_media: unicode
    @type amis: list
    """
    amis = sorted(amis, key=lambda k: k.get('CreationDate'), reverse=True)
    if output_media == 'console':
        td = [['id', 'name', 'created']]
        for ami in amis:
            td.append([ami.get('ImageId'), dash_if_none(ami.get('Name')), dash_if_none(ami.get('CreationDate'))])
        output_ascii_table(table_title="AMIs",
                           inner_heading_row_border=True,
                           table_data=td)
    exit(0)


def output_ami_permissions(perms=None):
    """
    @type perms: dict
    """
    out = ""
    for i, (key, value) in enumerate(six.iteritems(perms)):
        out += "{0},{1}".format(key, str(value))
        if i < len(perms)-1:
            out += "\n"
    return out


def get_product_codes(product_codes=None):
    """
    @type product_codes: dict
    """
    if product_codes:
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
        td.append(['id', ami.get('ImageId')])
        td.append(['name', ami.get('Name')])
        td.append(['creationDate', dash_if_none(ami.get('CreationDate'))])
        td.append(['description', dash_if_none(ami.get('Description'))])
        td.append(['hypervisor', dash_if_none(ami.get('Hypervisor'))])
        td.append(['is_public', dash_if_none(str(ami.get('Public')))])
        td.append(['kernel_id', dash_if_none(ami.get('KernelId'))])
        td.append(['location', dash_if_none(ami.get('ImageLocation'))])
        td.append(['owner_id', dash_if_none(ami.get('OwnerId'))])
        td.append(['owner_alias', dash_if_none(ami.get('ImageOwnerAlias'))])
        td.append(['platform', dash_if_none(ami.get('Platform'))])
        td.append(['product codes', dash_if_none(get_product_codes(ami.get('ProductCodes')))])
        td.append(['root_device_name', dash_if_none(ami.get('RootDeviceName'))])
        td.append(['root_device_type', dash_if_none(ami.get('RootDeviceType'))])
        td.append(['sriov_net_support', dash_if_none(ami.get('SriovNetSupport'))])
        td.append(['state', dash_if_none(ami.get('State'))])
        td.append(['virtualization_type', dash_if_none(ami.get('VirtualizationType'))])
        td.append(['block_device_mapping', get_block_devices(bdms=ami.get('BlockDeviceMappings'))])
        output_ascii_table(table_title="AMI Info",
                           table_data=td)
    exit(0)


def output_ec2_summary(output_media=None, summary=None):
    """
    @type output_media: unicode
    @type summary: dict
    """
    if output_media == 'console':
        td = list()
        td.append(['Running instances', str(summary.get('instances', '0')),
                   'Load Balancers', str(summary.get('elbs', '0'))])
        td.append(['Elastic IPs', str(summary.get('eips', '0')),
                   'AMIs', str(summary.get('amis', '0'))])
        td.append(['Security Groups', str(summary.get('secgroups', '0')),
                   'Security Groups', str(summary.get('secgroups', '0'))])
        output_ascii_table(table_title="EC2 Summary",
                           table_data=td)
    exit(0)
