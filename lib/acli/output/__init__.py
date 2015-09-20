from terminaltables import AsciiTable


def output_ascii_table(table_title=None,
                       table_data=None,
                       inner_heading_row_border=False,
                       inner_row_border=False):
    table = AsciiTable(table_data)
    table.inner_heading_row_border = inner_heading_row_border
    table.inner_row_border = inner_row_border
    table.title = table_title
    print(table.table)


def dash_if_none(item=None):
    return item if item else '-'


def get_tags(tags, separator=', '):
    tag_list = []
    for tag in tags:
        tag_list.append("{0}:{1}".format(tag.get('Key'), tag.get('Value')))
    if tag_list:
        return separator.join(tag_list)


def get_name_tag(tags):
    for tag_name, tag_value in tags.iteritems():
        if tag_name == 'Name':
            return tag_value
    return "-"
