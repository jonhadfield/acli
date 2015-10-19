# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)
from acli.output.account import output_account_info
from acli.connections import get_boto3_session
from botocore.exceptions import NoCredentialsError
from contextlib import contextmanager


@contextmanager
def cred_checked(iam_client):
    try:
        assert iam_client.list_users()
        yield iam_client
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
    with cred_checked(iam_client) as checked_iam_client:
        users = checked_iam_client.list_users(MaxItems=1)
        if users.get('Users', None):
            account_id = users.get('Users')[0]['Arn'].split(':')[4]
            aliases = checked_iam_client.list_account_aliases().get('AccountAliases')
            output_account_info(output_media='console',
                                account_id=account_id,
                                account_aliases=aliases)
