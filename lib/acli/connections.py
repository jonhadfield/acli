# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)
from boto3.session import Session
from contextlib import contextmanager
from botocore.exceptions import NoCredentialsError, NoRegionError


def exit_with_credentials_message():
    exit('Credentials not found. See here for more information:\n'
         'http://boto3.readthedocs.org/en/latest/guide/configuration.html#configuration-files')


@contextmanager
def checked_autoscaling_client(autoscaling_client):
    try:
        assert autoscaling_client.describe_launch_configurations()
        yield autoscaling_client
    except NoCredentialsError:
        exit_with_credentials_message()
    except Exception as e:
        exit('Unhandled exception: {0}'.format(e))


@contextmanager
def checked_iam_client(iam_client):
    try:
        assert iam_client.list_users()
        yield iam_client
    except NoCredentialsError:
        exit_with_credentials_message()
    except Exception as e:
        exit('Unhandled exception: {0}'.format(e))


@contextmanager
def checked_ec2_client(ec2_client):
    try:
        assert ec2_client.describe_instances(MaxResults=5)
        yield ec2_client
    except NoCredentialsError:
        exit_with_credentials_message()
    except Exception as e:
        exit('Unhandled exception: {0}'.format(e))


@contextmanager
def checked_elb_client(elb_client):
    try:
        assert elb_client.describe_load_balancers()
        yield elb_client
    except NoCredentialsError:
        exit_with_credentials_message()
    except Exception as e:
        exit('Unhandled exception: {0}'.format(e))


@contextmanager
def checked_cloudwatch_client(cloudwatch_client):
    try:
        assert cloudwatch_client.describe_alarms(MaxRecords=1)
        yield cloudwatch_client
    except NoCredentialsError:
        exit_with_credentials_message()
    except Exception as e:
        exit('Unhandled exception: {0}'.format(e))


@contextmanager
def checked_route53_client(route53_client):
    try:
        assert route53_client.list_hosted_zones(MaxItems='1')
        yield route53_client
    except NoCredentialsError:
        exit_with_credentials_message()
    except Exception as e:
        exit('Unhandled exception: {0}'.format(e))


@contextmanager
def checked_s3_client(s3_client):
    try:
        assert s3_client.list_buckets()
        yield s3_client
    except NoCredentialsError:
        exit_with_credentials_message()
    except Exception as e:
        exit('Unhandled exception: {0}'.format(e))


@contextmanager
def checked_es_client(es_client):
    try:
        assert es_client.list_domain_names()
        yield es_client
    except NoCredentialsError:
        exit_with_credentials_message()
    except Exception as e:
        exit('Unhandled exception: {0}'.format(e))


def get_boto3_session(aws_config):
    """
    @type aws_config: Config
    """
    if all((aws_config.region, aws_config.access_key_id, aws_config.secret_access_key)):
        return Session(region_name=aws_config.region,
                       aws_access_key_id=aws_config.access_key_id,
                       aws_secret_access_key=aws_config.secret_access_key)
    elif aws_config.region:
        return Session(region_name=aws_config.region)
    else:
        return Session()


def get_client(client_type=None, config=None):
    """
    @type client_type: basestring
    @type config: Config
    """
    session = get_boto3_session(aws_config=config)
    try:
        if client_type == 'ec2':
            with checked_ec2_client(session.client('ec2')) as ec2_client:
                return ec2_client
        elif client_type == 'elb':
            with checked_elb_client(session.client('elb')) as elb_client:
                return elb_client
        elif client_type == 'iam':
            with checked_iam_client(session.client('iam')) as iam_client:
                return iam_client
        elif client_type == 'autoscaling':
            with checked_autoscaling_client(session.client('autoscaling')) as autoscaling_client:
                return autoscaling_client
        elif client_type == 'cloudwatch':
            with checked_cloudwatch_client(session.client('cloudwatch')) as cloudwatch_client:
                return cloudwatch_client
        elif client_type == 'route53':
            with checked_route53_client(session.client('route53')) as route53_client:
                return route53_client
        elif client_type == 's3':
            with checked_s3_client(session.client('s3')) as s3_client:
                return s3_client
        elif client_type == 'es':
            with checked_es_client(session.client('es')) as es_client:
                return es_client
    except NoRegionError:
        exit('Cannot perform this task without specifying an AWS region.\n'
             'Please check your boto/aws settings or specify using \'acli --region=<region>\'.')
    except Exception as e:
        exit('Unhandled exception: {0}'.format(e))
