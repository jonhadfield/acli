# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)
from acli.output.account import output_account_info
from acli.connections import get_boto3_session
from botocore.exceptions import NoCredentialsError
from contextlib import contextmanager


@contextmanager
def cred_checked(iam_client):
    try:
        yield iam_client.list_account_aliases()
    except NoCredentialsError:
        exit('No credentials found.')
    except Exception as e:
        exit('Unhanded exception: {0}'.format(e))


def account_info(aws_config):
    """
    @type aws_config: Config
    """
    session = get_boto3_session(aws_config)
    iam_client = session.client('iam')
    with cred_checked(iam_client):
        account_aliases = iam_client.list_account_aliases()
        account_id = account_aliases.get_user().get('User').get('Arn').split(':')[4]
        output_account_info(output_media='console',
                            account_id=account_id,
                            account_aliases=account_aliases)
