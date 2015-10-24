# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)
from acli.output import (output_ascii_table)
import re
from colorclass import Color, Windows
Windows.enable(auto_colors=True, reset_atexit=True)


def output_s3_list(output_media=None, buckets=None, bucket_name=None, objects=None, folders=None, item=None):
    """
    @type output_media: unicode
    @type buckets: dict
    @type objects: dict
    @type bucket_name: unicode
    """
    to_remove_len = 0
    if bucket_name:
        to_remove_len = len(re.sub(bucket_name, '', item))-1
    if buckets:
        sorted_buckets = sorted(buckets, key=lambda k: ['Name'])
        td = list()
        td.append(['name', 'created'])
        for bucket in sorted_buckets:
            if output_media == 'console':
                td.append([Color('{autocyan}'+bucket.get('Name')+'{/autocyan}'), str(bucket.get('CreationDate'))])
        output_ascii_table(table_title="S3 Buckets",
                           table_data=td,
                           inner_heading_row_border=True)
    if any((objects, folders)):
        td = list()
        td.append(['item', 'size (bytes)', 'last modified (UTC)', 'class', 'etag'])
        if folders:
            for folder in folders:
                td.append([Color('{autogreen}'+folder.get('Prefix')[to_remove_len:]+'{/autogreen}'), '-', '-'])
        object_list = objects.get('Contents', None)
        if objects.get('Contents', None):
            sorted_object_list = sorted(object_list, key=lambda k: ['Key'])
            for index, an_object in enumerate(sorted_object_list):
                an_object_key = an_object.get('Key')[to_remove_len:]
                if an_object_key:
                    td.append([an_object_key,
                               str(an_object.get('Size')),
                               str(an_object.get('LastModified').replace(tzinfo=None)),
                               str(an_object.get('StorageClass')),
                               # str(an_object.get('Owner')),
                               str(an_object.get('ETag')[1:-1])])

        else:
            print("NO OBJECTS TO OUTPUT :(")
        output_ascii_table(table_title=item,
                           table_data=td,
                           inner_heading_row_border=True)
    exit(0)
