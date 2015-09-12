import boto.ec2
import os


def get_ec2_conn(region):
    return boto.ec2.connect_to_region(region,
                                      aws_access_key_id=os.environ.get('AWS_ACCESS_KEY', None),
                                      aws_secret_access_key=os.environ.get('AWS_SECRET_KEY', None))
