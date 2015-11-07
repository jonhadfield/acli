# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)
from acli.output import (output_ascii_table, output_ascii_table_list, dash_if_none)
import pprint
import json
import six
from colorclass import Color, Windows
Windows.enable(auto_colors=True, reset_atexit=True)


def default(obj):
    """Default JSON serializer."""
    import calendar, datetime

    if isinstance(obj, datetime.datetime):
        if obj.utcoffset() is not None:
            obj = obj - obj.utcoffset()
        millis = int(
            calendar.timegm(obj.timetuple()) * 1000 +
            obj.microsecond / 1000
        )
        return millis
    raise TypeError('Not sure how to serialize %s' % obj)


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


def colour_state(state=None):
    if not state:
        return Color('{autoblack}-{/autoblack}')
    elif state == 'running':
        return Color('{autogreen}'+state+'{/autogreen}')
    elif state in ('stopped', 'stopping', 'shutting-down', 'terminated'):
        return Color('{autored}'+state+'{/autored}')
    elif state in ('rebooting', 'pending'):
        return Color('{autoyellow}'+state+'{/autoyellow}')


def output_ec2_list(instances=None):
    """
    @type instances: list
    """
    td = list()
    table_header = [Color('{autoblue}id{/autoblue}'), Color('{autoblue}name{/autoblue}'),
                    Color('{autoblue}state{/autoblue}'), Color('{autoblue}type{/autoblue}'),
                    Color('{autoblue}image{/autoblue}'),
                    Color('{autoblue}public ip{/autoblue}'), Color('{autoblue}private ip{/autoblue}')]
    instances = sorted(instances,
                       key=lambda k: get_ec2_instance_tags(ec2_instance=k, tag_key='Name'))
    for instance in instances:
        if instance:
            instance_id = instance.get('InstanceId')
            instance_state = colour_state(instance.get('State').get('Name', None))
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
    output_ascii_table_list(table_title=Color('{autowhite}ec2 instances{/autowhite}'),
                            table_header=table_header,
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
        ret.append('GroupName:{}\nGroupId:{}'.format(group.get('GroupName', '-'), group.get('GroupId', '-')))
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


def output_ec2_info(instance=None):
    """
    @type instance: ec2.Instance
    """
    td = list()
    td.append([Color('{autoblue}id{/autoblue}'),
               instance.get('InstanceId')])
    td.append([Color('{autoblue}name{/autoblue}'),
               dash_if_none(get_ec2_instance_tags(ec2_instance=instance, tag_key='Name'))])
    td.append([Color('{autoblue}groups{/autoblue}'),
               dash_if_none(get_sec_groups_name_and_id(instance.get('SecurityGroups')))])
    td.append([Color('{autoblue}public ip{/autoblue}'),
               dash_if_none(instance.get('PublicIpAddress', None))])
    td.append([Color('{autoblue}public dns name{/autoblue}'),
               dash_if_none(instance.get('PublicDnsName', None))])
    td.append([Color('{autoblue}private ip{/autoblue}'),
               dash_if_none(instance.get('PrivateIpAddress', None))])
    td.append([Color('{autoblue}private dns name{/autoblue}'),
               dash_if_none(instance.get('PrivateDnsName', None))])
    td.append([Color('{autoblue}state{/autoblue}'),
               colour_state(instance.get('State')['Name'])])
    td.append([Color('{autoblue}key name{/autoblue}'),
               dash_if_none(instance.get('KeyName', None))])
    td.append([Color('{autoblue}instance type{/autoblue}'),
               dash_if_none(instance.get('InstanceType', None))])
    td.append([Color('{autoblue}launch time{/autoblue}'),
               str(instance.get('LaunchTime'))])
    td.append([Color('{autoblue}image id{/autoblue}'),
               dash_if_none(instance.get('ImageId'))])
    td.append([Color('{autoblue}placement{/autoblue}'),
               get_placement_details(instance.get('Placement'))])
    td.append([Color('{autoblue}monitored{/autoblue}'),
               'enabled' if instance.get('Monitoring')['State'] == 'enabled' else 'disabled'])
    td.append([Color('{autoblue}subnet id{/autoblue}'),
               dash_if_none(instance.get('SubnetId'))])
    td.append([Color('{autoblue}vpc id{/autoblue}'),
               dash_if_none(instance.get('VpcId'))])
    td.append([Color('{autoblue}root device type{/autoblue}'),
               dash_if_none(instance.get('RootDeviceType', None))])
    td.append([Color('{autoblue}state transition reason{/autoblue}'),
               dash_if_none(instance.get('StateTransitionReason', None))])
    td.append([Color('{autoblue}ebs optimized{/autoblue}'),
               dash_if_none(instance.get('EbsOptimized', None))])
    td.append([Color('{autoblue}instance profile{/autoblue}'),
               dash_if_none(short_instance_profile(instance.get('IamInstanceProfile', None)))])
    td.append([Color('{autoblue}tags{/autoblue}'),
               get_ec2_instance_tags(ec2_instance=instance)])
    td.append([Color('{autoblue}block devices{/autoblue}'),
               get_block_devices(instance.get('BlockDeviceMappings'))])
    td.append([Color('{autoblue}interfaces{/autoblue}'),
               dash_if_none(get_interfaces(instance.get('NetworkInterfaces', None)))])
    output_ascii_table(table_title=Color('{autowhite}instance info{/autowhite}'),
                       table_data=td)
    exit(0)


def trim_creation_date(creation_date=None):
    if creation_date:
        return creation_date[:-5].replace('T', ' ')


def output_ami_list(output_media=None, amis=None):
    """
    @type output_media: unicode
    @type amis: list
    """
    amis = sorted(amis, key=lambda k: k.get('CreationDate'), reverse=True)
    if output_media == 'console':
        td = [[Color('{autoblue}image id{/autoblue}'),
               Color('{autoblue}name{/autoblue}'),
               Color('{autoblue}created (UTC){/autoblue}')]]
        for ami in amis:
            td.append([ami.get('ImageId'),
                       dash_if_none(ami.get('Name')),
                       dash_if_none(trim_creation_date(ami.get('CreationDate')))])
        output_ascii_table(table_title=Color('{autowhite}AMIs{/autowhite}'),
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
        td.append([Color('{autoblue}id{/autoblue}'),
                   ami.get('ImageId')])
        td.append([Color('{autoblue}name{/autoblue}'),
                   ami.get('Name')])
        td.append([Color('{autoblue}created (UTC){/autoblue}'),
                   dash_if_none(trim_creation_date(ami.get('CreationDate')))])
        td.append([Color('{autoblue}description{/autoblue}'),
                   dash_if_none(ami.get('Description'))])
        td.append([Color('{autoblue}hypervisor{/autoblue}'),
                   dash_if_none(ami.get('Hypervisor'))])
        td.append([Color('{autoblue}public{/autoblue}'),
                   dash_if_none(str(ami.get('Public')))])
        td.append([Color('{autoblue}kernel id{/autoblue}'),
                   dash_if_none(ami.get('KernelId'))])
        td.append([Color('{autoblue}location{/autoblue}'),
                   dash_if_none(ami.get('ImageLocation'))])
        td.append([Color('{autoblue}owner id{/autoblue}'),
                   dash_if_none(ami.get('OwnerId'))])
        td.append([Color('{autoblue}owner alias{/autoblue}'),
                   dash_if_none(ami.get('ImageOwnerAlias'))])
        td.append([Color('{autoblue}platform{/autoblue}'),
                   dash_if_none(ami.get('Platform'))])
        td.append([Color('{autoblue}product codes{/autoblue}'),
                   dash_if_none(get_product_codes(ami.get('ProductCodes')))])
        td.append([Color('{autoblue}root device name{/autoblue}'),
                   dash_if_none(ami.get('RootDeviceName'))])
        td.append([Color('{autoblue}root device typr{/autoblue}'),
                   dash_if_none(ami.get('RootDeviceType'))])
        td.append([Color('{autoblue}sriov net support{/autoblue}'),
                   dash_if_none(ami.get('SriovNetSupport'))])
        td.append([Color('{autoblue}state{/autoblue}'),
                   dash_if_none(ami.get('State'))])
        td.append([Color('{autoblue}virtualisation type{/autoblue}'),
                   dash_if_none(ami.get('VirtualizationType'))])
        td.append([Color('{autoblue}block device mapping{/autoblue}'),
                   get_block_devices(bdms=ami.get('BlockDeviceMappings'))])
        output_ascii_table(table_title=Color('{autowhite}AMI info{/autowhite}'),
                           table_data=td)
    exit(0)


def output_ec2_summary(output_media=None, summary=None):
    """
    @type output_media: unicode
    @type summary: dict
    """
    if output_media == 'console':
        td = list()
        td.append([Color('{autoblue}running instances{/autoblue}'), str(summary.get('instances', '0')),
                   Color('{autoblue}load balancers{/autoblue}'), str(summary.get('elbs', '0'))])
        td.append([Color('{autoblue}elastic IPs{/autoblue}'), str(summary.get('eips', '0')),
                   Color('{autoblue}AMIs{/autoblue}'), str(summary.get('amis', '0'))])
        td.append([Color('{autoblue}security groups{/autoblue}'), str(summary.get('secgroups', '0')),
                   '', ''])
        output_ascii_table(table_title=Color('{autowhite}ec2 summary{/autowhite}'),
                           table_data=td)
    exit(0)
