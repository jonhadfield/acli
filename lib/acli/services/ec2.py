# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)

from botocore.exceptions import ClientError

from acli.connections import get_client
from acli.errors import handle_boto_errors
from acli.output.ec2 import (output_ec2_list, output_ec2_info,
                             output_ami_list, output_ami_info,
                             output_ec2_summary)
from acli.utils import get_tag_value


@handle_boto_errors
def ec2_summary(aws_config=None):
    """
    @type aws_config: Config
    """
    elb_client = get_client(client_type='elb', config=aws_config)
    ec2_client = get_client(client_type='ec2', config=aws_config)
    elbs = len(elb_client.describe_load_balancers().get('LoadBalancerDescriptions'))
    instances = list()
    for reservation in ec2_client.describe_instances().get('Reservations', []):
        for instance in reservation.get('Instances'):
            instances.append(instance)

    amis = len(list(ec2_client.describe_images(Owners=['self']).get('Images')))
    secgroups = len(ec2_client.describe_security_groups().get('SecurityGroups', 0))
    addresses = ec2_client.describe_addresses()['Addresses']
    eips = len([x for x, _ in enumerate(addresses)])
    volumes = ec2_client.describe_volumes().get('Volumes')
    summary = {'instances': instances, 'elbs': elbs, 'eips': eips,
               'amis': amis, 'secgroups': secgroups, 'volumes': volumes}
    output_ec2_summary(summary=summary)
    exit(0)


@handle_boto_errors
def ec2_list(aws_config=None, filter_term=None):
    """
    @type aws_config: Config
    @type filter_term: unicode
    """
    ec2_client = get_client(client_type='ec2', config=aws_config)
    instances_req = ec2_client.describe_instances()
    reservations = instances_req.get('Reservations')
    all_instances = list()
    for reservation in reservations:
        for instance in reservation.get('Instances'):
            if instance.get('Tags') and filter_term and filter_term not in get_tag_value(name='Name',
                                                                                         tags=instance.get('Tags')):
                continue
            all_instances.append(instance)
    if all_instances:
        output_ec2_list(instances=all_instances)
    exit('No ec2 instances found.')


@handle_boto_errors
def ec2_info(aws_config=None, instance_id=None):
    """
    @type aws_config: Config
    @type instance_id: unicode
    """
    ec2_client = get_client(client_type='ec2', config=aws_config)
    ec2_query = ec2_client.describe_instances(Filters=[{'Name': 'instance-id', 'Values': [instance_id]}])
    reservations = ec2_query.get('Reservations')
    try:
        instance = reservations[0].get('Instances')[0]
        if instance.get('InstanceId'):
            output_ec2_info(instance=instance)
    except IndexError:
        raise SystemExit("Cannot find instance: {0}".format(instance_id))


@handle_boto_errors
def ec2_instance_stop(instance_id=None, instance_state=None, ec2_client=None):
    if instance_state in ('pending', 'rebooting', 'stopping', 'terminated', 'shutting-down'):
        exit("Cannot stop instance as state is {0}.".format(instance_state))
    elif instance_state in ('stopping', 'stopped', 'shutting-down'):
        exit("Instance {0} is already {1}.".format(instance_id, instance_state))
    else:
        ec2_client.stop_instances(InstanceIds=[instance_id])
        exit("Instance {0} stopping.".format(instance_id))


@handle_boto_errors
def ec2_instance_start(instance_id=None, instance_state=None, ec2_client=None):
    if instance_state in ('rebooting', 'stopping',
                          'terminated', 'shutting-down'):
        exit("Cannot start instance {0} as state is {1}.".format(instance_id,
                                                                 instance_state))
    elif instance_state in ('pending', 'rebooting',
                            'stopping', 'terminated',
                            'shutting-down', 'running'):
        exit("Instance {0} is already {1}.".format(instance_id, instance_state))
    else:
        ec2_client.start_instances(InstanceIds=[instance_id])
        exit("Instance {0} starting.".format(instance_id))


@handle_boto_errors
def ec2_instance_reboot(instance_id=None, instance_state=None, ec2_client=None):
    if instance_state in ('pending', 'stopping', 'terminated', 'shutting-down'):
        exit("Cannot reboot instance {0} as state is {1}.".format(instance_id,
                                                                  instance_state))
    elif instance_state == 'rebooting':
        exit("Instance {0} is already {1}.".format(instance_id, instance_state))
    else:
        ec2_client.reboot_instances(InstanceIds=[instance_id])
        exit("Instance {0} rebooting.".format(instance_id))


@handle_boto_errors
def ec2_instance_terminate(instance_id=None, instance_state=None, ec2_client=None):
    if instance_state in ('rebooting', 'stopping',
                          'terminated', 'shutting-down'):
        exit("Cannot terminate instance {0} as state is {1}.".format(instance_id,
                                                                     instance_state))
    elif instance_state in ('rebooting',
                            'stopping', 'terminated',
                            'shutting-down'):
        exit("Instance {0} is already {1}.".format(instance_id, instance_state))
    else:
        ec2_client.terminate_instances(InstanceIds=[instance_id])
        exit("Instance {0} terminating.".format(instance_id))


@handle_boto_errors
def ec2_manage(aws_config=None, instance_id=None, action=None):
    """
    @type aws_config: Config
    @type instance_id: unicode
    @type action: unicode
    """
    ec2_client = get_client(client_type='ec2', config=aws_config)
    reservations = ec2_client.describe_instances(InstanceIds=[instance_id])
    instance = reservations.get('Reservations')[0].get('Instances')[0]
    try:
        instance_id = instance.get('InstanceId')
        instance_state = instance['State']['Name']
        if instance_id:
            if action == 'stop':
                ec2_instance_stop(instance_id=instance_id,
                                  instance_state=instance_state,
                                  ec2_client=ec2_client)
            elif action == 'start':
                ec2_instance_start(instance_id=instance_id,
                                   instance_state=instance_state,
                                   ec2_client=ec2_client)
            elif action == 'reboot':
                ec2_instance_reboot(instance_id=instance_id,
                                    instance_state=instance_state,
                                    ec2_client=ec2_client)
            elif action == 'terminate':
                ec2_instance_terminate(instance_id=instance_id,
                                       instance_state=instance_state,
                                       ec2_client=ec2_client)
    except AttributeError:
        exit("Cannot find instance: {0}".format(instance_id))


@handle_boto_errors
def ami_info(aws_config=None, ami_id=None):
    """
    @type aws_config: Config
    @type ami_id: unicode
    """
    ec2_client = get_client(client_type='ec2', config=aws_config)
    try:
        output_ami_info(ami=ec2_client.describe_images(ImageIds=[ami_id]).get('Images')[0],
                        launch_permissions=ec2_client.describe_image_attribute(ImageId=ami_id,
                                                                               Attribute='launchPermission'))
    except ClientError:
        exit('Unable to find ami: {0}'.format(ami_id))


@handle_boto_errors
def ami_list(aws_config=None, filter_term=None):
    """
    @type aws_config: Config
    @type filter_term: unicode
    """
    all_images = list()
    ec2_client = get_client(client_type='ec2', config=aws_config)
    for image in ec2_client.describe_images(Owners=['self']).get('Images'):
        if filter_term and filter_term not in image.get('Name'):
            continue
        all_images.append(image)
    if all_images:
        output_ami_list(amis=all_images)
    elif filter_term:
        exit('No mathching amis found.')
    else:
        exit('No amis found.')


@handle_boto_errors
def ec2_get_instance_vols(aws_config=None, instance_id=None):
    """
    @type aws_config: Config
    @type instance_id: unicode
    """
    ec2_client = get_client(client_type='ec2', config=aws_config)
    reservations = ec2_client.describe_instances(InstanceIds=[instance_id])
    reservation = reservations.get('Reservations')[0]
    instance = reservation.get('Instances')[0]
    vols = list()
    for bdm in instance.get('BlockDeviceMappings'):
        vols.append(bdm)
    return vols
