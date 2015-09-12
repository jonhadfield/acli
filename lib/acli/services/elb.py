import boto
import os


def get_elb_conn(region):
    elb_region = boto.regioninfo.RegionInfo( name=region, endpoint='elasticloadbalancing.eu-west-1.amazonaws.com')
    return boto.connect_elb(region=elb_region,
                            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY', None),
                            aws_secret_access_key=os.environ.get('AWS_SECRET_KEY', None))
