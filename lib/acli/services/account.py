# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)
from acli.output.account import output_account_info
from acli.connections import get_boto3_session


def account_info(aws_config):
    session = get_boto3_session(aws_config)
    iam_client = session.client('iam')
    aliases = iam_client.list_account_aliases().get('AccountAliases')
    account_id = iam_client.get_user().get('User').get('Arn').split(':')[4]
    output_account_info(output_media='console',
                        account_id=account_id,
                        account_aliases=aliases)
