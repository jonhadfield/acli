# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)

import math
import os

from colorclass import Color, Windows
from terminaltables import AsciiTable

from acli.utils import get_console_dimensions

try:
    input = raw_input
except NameError:
    pass
Windows.enable(auto_colors=True, reset_atexit=True)


def output_ascii_table(table_title=None,
                       table_data=None,
                       inner_heading_row_border=False,
                       inner_footing_row_border=False,
                       inner_row_border=False):
    """
    @type table_title: unicode
    @type table_data: list
    @type inner_heading_row_border: bool
    @type inner_footing_row_border: bool
    @type inner_row_border: bool
    """
    table = AsciiTable(table_data)
    table.inner_heading_row_border = inner_heading_row_border
    table.inner_row_border = inner_row_border
    table.inner_footing_row_border = inner_footing_row_border
    table.title = table_title
    print(table.table)


def output_ascii_table_list(table_title=None,
                            table_data=None,
                            table_header=None,
                            inner_heading_row_border=False,
                            inner_row_border=False):
    """
    @type table_title: unicode
    @type table_data: list
    @type inner_heading_row_border: bool
    @type inner_row_border: bool
    @type table_header: list
    """
    console_rows, _ = get_console_dimensions()
    console_rows = int(console_rows)
    full_display_length = len(table_data) + 7
    items_per_page = console_rows - 7
    num_pages = 0
    if full_display_length > console_rows:
        try:
            num_pages = int(math.ceil(float(len(table_data)) / float(items_per_page)))
        except ZeroDivisionError:
            exit('Console too small to display.')
    if num_pages:
        running_count = 0
        for page in range(1, num_pages + 1):
            page_table_output = list()
            page_table_output.insert(0, table_header)
            upper = (console_rows + running_count) - 7
            if upper > len(table_data):
                upper = len(table_data)
            for x in range(running_count, upper):
                page_table_output.append(table_data[x])
                running_count += 1
            table = AsciiTable(page_table_output)
            table.inner_heading_row_border = inner_heading_row_border
            table.inner_row_border = inner_row_border
            table.title = table_title
            if page != 1:
                print('')
            print(table.table)
            if page < num_pages:
                input("Press Enter to continue...")
                os.system('clear')
    else:
        table_data.insert(0, table_header)
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
