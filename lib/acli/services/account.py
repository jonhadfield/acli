from __future__ import (absolute_import, print_function, unicode_literals)
from boto3.session import Session
from acli.output.account import output_account_info


def get_boto3_session(aws_config):
    return Session(region_name=aws_config.region,
                   aws_access_key_id=aws_config.access_key_id,
                   aws_secret_access_key=aws_config.secret_access_key)


def account_info(aws_config):
    session = get_boto3_session(aws_config)
    iam_client = session.client('iam')
    aliases = iam_client.list_account_aliases().get('AccountAliases')
    account_id = iam_client.get_user().get('User').get('Arn').split(':')[4]
    output_account_info(output_media='console',
                        account_id=account_id,
                        account_aliases=aliases)
