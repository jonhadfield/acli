# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)
from boto3.session import Session
from contextlib import contextmanager
from botocore.exceptions import NoCredentialsError


@contextmanager
def cred_checked_iam_client(iam_client):
    try:
        assert iam_client.list_users()
        yield iam_client
    except NoCredentialsError:
        exit('No credentials found.')
    except Exception as e:
        exit('Unhanded exception: {0}'.format(e))


@contextmanager
def cred_checked_ec2_client(ec2_client):
    try:
        assert ec2_client.describe_account_attributes()
        yield ec2_client
    except NoCredentialsError:
        exit('No credentials found.')
    except Exception as e:
        exit('Unhanded exception: {0}'.format(e))


@contextmanager
def cred_checked_elb_client(elb_client):
    try:
        assert elb_client.describe_load_balancers()
        yield elb_client
    except NoCredentialsError:
        exit('No credentials found.')
    except Exception as e:
        exit('Unhanded exception: {0}'.format(e))


def get_boto3_session(aws_config):
    """
    @type aws_config: Config
    """
    if all((aws_config.region, aws_config.access_key_id, aws_config.secret_access_key)):
        return Session(region_name=aws_config.region,
                       aws_access_key_id=aws_config.access_key_id,
                       aws_secret_access_key=aws_config.secret_access_key)
    # Fall back to Boto searching for the session
    return Session()


def get_client(client_type=None, config=None):
    """
    @type client_type: basestring
    @type config: Config
    """
    session = get_boto3_session(aws_config=config)
    if client_type == 'ec2':
        with cred_checked_ec2_client(session.client('ec2')) as ec2_client:
            return ec2_client
    elif client_type == 'elb':
        with cred_checked_elb_client(session.client('elb')) as elb_client:
            return elb_client
    elif client_type == 'iam':
        with cred_checked_iam_client(session.client('iam')) as iam_client:
            return iam_client
