# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)
from acli.output import (output_ascii_table, dash_if_none)


def output_s3_list(output_media=None, buckets=None, bucket_name=None, objects=None):
    """
    @type output_media: unicode
    @type buckets: list
    @type objects: list
    @type bucket_name: list
    """
    if buckets:
        sorted_buckets = sorted(buckets, key=lambda k: ['Name'])
        td = list()
        td.append(['name', 'created'])
        for bucket in sorted_buckets:
            if output_media == 'console':
                td.append([bucket.get('Name'), str(bucket.get('CreationDate'))])
        output_ascii_table(table_title="S3 Buckets",
                           table_data=td,
                           inner_heading_row_border=True)
    if objects:
        print(bucket_name)
        print(objects)
        print('done with objects')
        # if item and '\\' not in item:
        #    print('got bucke')
        # path_elements = item.split('/')

        # contents = item.get('Contents')
        # for content in contents:
        #    print('\n')
        #    print(content)
    exit(0)


def output_s3_info(output_media=None, item=None):
    """
    @type output_media: unicode
    @type item: unicode
    """
    # if output_media == 'console':
    #    td = list()
    #    td.append(['id', zone['HostedZone']['Id']])
    #    td.append(['Name', zone['HostedZone']['Name']])
    #    td.append(['Count', str(zone['HostedZone']['ResourceRecordSetCount'])])
    #    td.append(['Comment', zone['HostedZone']['Config']['Comment']])
    #    td.append(['Private', str(zone['HostedZone']['Config']['PrivateZone'])])
    #    td.append(['Name Servers', "\n".join(zone['DelegationSet']['NameServers'])])
    #    td.append(['Records', ' '])
    #    td.append(['{0}'.format("-" * 12), '{0}'.format("-" * 20)])
    #    for record_set in record_sets['ResourceRecordSets']:
    #        td.append(['Name', record_set['Name']])
    #        td.append([' Type', record_set['Type']])
    #        td.append([' TTL', str(record_set['TTL'])])
    #        td.append([' Values', "\n".join(get_record_set_values(record_set['ResourceRecords']))])
    #    output_ascii_table(table_title="Zone Info",
    #                       table_data=td)
    exit(0)
