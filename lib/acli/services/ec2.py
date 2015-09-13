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
