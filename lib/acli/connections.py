# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)
import boto.ec2.elb


def get_elb_conn(aws_config):
    """
    @type aws_config: Config
    """
    return boto.ec2.elb.connect_to_region(aws_access_key_id=aws_config.access_key_id,
                                          aws_secret_access_key=aws_config.secret_access_key,
                                          region_name=aws_config.region)
