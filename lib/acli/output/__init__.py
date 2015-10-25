# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)
from terminaltables import AsciiTable
from colorclass import Color, Windows
Windows.enable(auto_colors=True, reset_atexit=True)


def output_ascii_table(table_title=None,
                       table_data=None,
                       inner_heading_row_border=False,
                       inner_row_border=False):
    """
    @type table_title: unicode
    @type table_data: list
    @type inner_heading_row_border: bool
    @type inner_row_border: bool
    """
    table = AsciiTable(table_data)
    table.inner_heading_row_border = inner_heading_row_border
    table.inner_row_border = inner_row_border
    table.title = table_title
    print(table.table)


def dash_if_none(item=None):
    """
    @type item: object
    """
    return str(item) if item else Color('{autoblack}-{/autoblack}')


def get_tags(tags, separator=', '):
    """
    @type tags: list
    @type separator: unicode
    """
    tag_list = list()
    for tag in tags:
        tag_list.append("{0}:{1}".format(tag.get('Key'), tag.get('Value')))
    if tag_list:
        return separator.join(tag_list)


def get_name_tag(tags):
    """
    @type tags: dict
    """
    for tag_name, tag_value in tags.iteritems():
        if tag_name == 'Name':
            return tag_value
    return "-"
