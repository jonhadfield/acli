import boto.ec2


def get_ec2_conn(aws_config):
    return boto.ec2.connect_to_region(region_name=aws_config.region,
                                      aws_access_key_id=aws_config.access_key_id,
                                      aws_secret_access_key=aws_config.secret_access_key)


def get_ec2_list(aws_config):
    ec2_conn = get_ec2_conn(aws_config)
    reservations = [reservation for reservation in ec2_conn.get_all_instances()]
    instances = []
    for reservation in reservations:
        instances.append(reservation.instances)
    return instances


def get_ec2_instance(aws_config, instance_id=None):
    if instance_id:
        ec2_conn = get_ec2_conn(aws_config)
        reservations = ec2_conn.get_all_instances(instance_ids=[instance_id])
        return reservations[0].instances[0]


def get_ami_list(aws_config):
    ec2_conn = get_ec2_conn(aws_config)
    return ec2_conn.get_all_images(owners=['self'])


def get_ami(aws_config, ami_id=None):
    if ami_id:
        ec2_conn = get_ec2_conn(aws_config)
        all_matching_images = ec2_conn.get_all_images(image_ids=[ami_id])
        if all_matching_images:
            return all_matching_images[0]
