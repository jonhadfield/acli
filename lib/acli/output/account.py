# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)
from acli.output import output_ascii_table, dash_if_none
from colorclass import Color, Windows
Windows.enable(auto_colors=True, reset_atexit=True)


def output_account_info(account_id=None, account_aliases=None):
    """
    @type account_id: unicode
    @type account_aliases: list
    """
    td = list()
    td.append([Color('{autoblue}id{/autoblue}'), dash_if_none(account_id)])
    td.append([Color('{autoblue}aliases{/autoblue}'), dash_if_none(", ".join(account_aliases))])
    output_ascii_table(table_title=Color('{autowhite}Account Info{/autowhite}'),
                       table_data=td)
    exit(0)
