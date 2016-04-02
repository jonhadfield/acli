# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)

from acli.connections import get_client
from acli.errors import handle_boto_errors
from acli.output.account import output_account_info


@handle_boto_errors
def account_info(aws_config):
    """
    @type aws_config: Config
    """
    iam_client = get_client(client_type='iam', config=aws_config)
    users = iam_client.list_users(MaxItems=1)
    if users.get('Users'):
        account_id = users.get('Users')[0]['Arn'].split(':')[4]
        aliases = iam_client.list_account_aliases().get('AccountAliases')
        output_account_info(account_id=account_id,
                            account_aliases=aliases)
