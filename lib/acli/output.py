# from tabulate import tabulate
from terminaltables import AsciiTable


def output_ec2(output_type=None, instances=None):
    if output_type == 'console':
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
            instance_name = instance[0].tags.get('Name', '-')
            if len(instance_name) > 40:
                instance_name = "{0}...".format(instance_name[:30])
            if instance_profile:
                instance_profile_out = instance_profile.get('arn').split('/')[-1]
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


def output_elb(output_type=None, elbs=None):
    if output_type == 'console':
        heading = ['id', 'name']
        table_data = [heading]

        for elb in elbs:
            elb_id = elb.name
            elb_name = elb.name
            table_data.append([elb_id, elb_name])
        table = AsciiTable(table_data)
        print(table.table)
