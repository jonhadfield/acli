from __future__ import (absolute_import, print_function, unicode_literals)
import boto.ec2.elb
from acli.output.elb import output_elbs, output_elb_info


def get_elb_conn(aws_config):
    return boto.ec2.elb.connect_to_region(aws_access_key_id=aws_config.access_key_id,
                                          aws_secret_access_key=aws_config.secret_access_key,
                                          region_name=aws_config.region)


def get_elb_list(aws_config):
    elb_conn = get_elb_conn(aws_config)
    return [elb for elb in elb_conn.get_all_load_balancers()]


def get_elb(aws_config, elb_name=None):
    if elb_name:
        elb_conn = get_elb_conn(aws_config)
        return elb_conn.get_all_load_balancers(load_balancer_names=[elb_name])


def elb_list(aws_config):
    output_elbs(
                output_media='console',
                elbs=get_elb_list(aws_config))


def elb_info(aws_config=None, elb_name=None):
    output_elb_info(output_media='console',
                    elb=get_elb(aws_config,
                                elb_name=elb_name))
