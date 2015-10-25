# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)
from acli.output import output_ascii_table, dash_if_none
from colorclass import Color, Windows
Windows.enable(auto_colors=True, reset_atexit=True)


def output_account_info(output_media=None, account_id=None, account_aliases=None):
    """
    @type output_media: unicode
    @type account_id: unicode
    @type account_aliases: list
    """
    if output_media == 'console':
        td = list()
        td.append(['id', dash_if_none(account_id)])
        td.append(['aliases', dash_if_none(", ".join(account_aliases))])
        output_ascii_table(table_title=Color('{autowhite}Account Info{/autowhite}'),
                           table_data=td)
    exit(0)
