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
        print(table.table)


def dash_if_none(item=None):
    return item if item else '-'

def short_instance_profile(instance_profile):
    return instance_profile.get('arn').split('/')[-1]


def output_ec2_info(output_media=None, instance=None):
    if output_media == 'console':
        table_data = [['id', instance.id]]
        table_data.append(['groups', str(instance.groups)])
        table_data.append(['public dns name', dash_if_none(instance.public_dns_name)])
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
        table_data.append(['interfaces', dash_if_none(str(instance.interfaces))])
        table_data.append(['ebs optimized', dash_if_none(instance.ebs_optimized)])
        table_data.append(['instance profile', dash_if_none(short_instance_profile(instance.instance_profile))])

        #for instance in instances:
        #    instance_id = instance[0].id
        #    instance_state = instance[0].state
        #    instance_type = instance[0].instance_type
        #    image_id = instance[0].image_id
        #    public_ip = instance[0].ip_address
        #    private_ip = instance[0].private_ip_address
        #    instance_profile = instance[0].instance_profile
        #    instance_profile_out = '-'
        #    instance_name = instance[0].tags.get('Name', '-')
        #    if len(instance_name) > 40:
        #        instance_name = "{0}...".format(instance_name[:30])
        #    if instance_profile:
        #        instance_profile_out = instance_profile.get('arn').split('/')[-1]
        #    table_data.append([instance_id,
        #                       instance_name,
        #                       instance_state,
        #                       instance_type,
        #                       image_id,
        #                       public_ip if public_ip else '-',
        #                       private_ip if private_ip else '-',
        #                       instance_profile_out])
        table = AsciiTable(table_data)
        table.inner_heading_row_border = False
        print(table.table)


def output_elb(output_media=None, elbs=None):
    if output_media == 'console':
        heading = ['id', 'name']
        table_data = [heading]

        for elb in elbs:
            elb_id = elb.name
            elb_name = elb.name
            table_data.append([elb_id, elb_name])
        table = AsciiTable(table_data)
        print(table.table)
