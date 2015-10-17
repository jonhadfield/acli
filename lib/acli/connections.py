# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)
from boto3.session import Session
from botocore.exceptions import ClientError, PartialCredentialsError, NoCredentialsError


def get_boto3_session(aws_config):
    """
    @type aws_config: Config
    """
    session = Session(region_name=aws_config.region,
                      aws_access_key_id=aws_config.access_key_id,
                      aws_secret_access_key=aws_config.secret_access_key)
    try:
        iam_client = session.client('iam')
        iam_client.list_account_aliases()
        return session
    except ClientError:
        exit('Please check credentials.')
    except NoCredentialsError:
        exit('Credentials not found.')
    except PartialCredentialsError:
        exit('Credentials are incomplete.')
