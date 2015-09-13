from __future__ import (absolute_import, print_function)
import boto.ec2.elb


def get_elb_conn(aws_config):
    return boto.ec2.elb.connect_to_region(aws_access_key_id=aws_config.access_key_id,
                                          aws_secret_access_key=aws_config.secret_access_key,
                                          region_name=aws_config.region)


def get_elb_list(aws_config):
    elb_conn = get_elb_conn(aws_config)
    for elb in elb_conn.get_all_load_balancers():
        print(elb)
