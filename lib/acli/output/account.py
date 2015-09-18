from __future__ import (absolute_import, print_function)
from acli.output import output_ascii_table, dash_if_none


def output_account_info(output_media=None, account_id=None, account_aliases=None):
    if output_media == 'console':
        td = list()
        td.append(['id', dash_if_none(account_id)])
        td.append(['aliases', dash_if_none(", ".join(account_aliases))])
        output_ascii_table(table_title="Account Info",
                           table_data=td)
