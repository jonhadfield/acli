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
        td.append([Color('{autoblue}name{/autoblue}'), Color('{autoblue}created{/autoblue}')])
        for bucket in sorted_buckets:
            if output_media == 'console':
                td.append([bucket.get('Name'),
                           str(bucket.get('CreationDate').replace(tzinfo=None, microsecond=0))])
        output_ascii_table(table_title=Color('{autowhite}s3 buckets{/autowhite}'),
                           table_data=td,
                           inner_heading_row_border=True)
    if any((objects, folders)):
        td = list()
        td.append([Color('{autoblue}item{/autoblue}'), Color('{autoblue}size (bytes){/autoblue}'),
                  Color('{autoblue}last modified (UTC){/autoblue}'),
                  Color('{autoblue}class{/autoblue}'), Color('{autoblue}etag{/autoblue}')])
        if folders:
            for folder in folders:
                td.append([Color('{autogreen}'+folder.get('Prefix')[to_remove_len:]+'{/autogreen}'),
                           Color('{autoblack}-{/autoblack}'),
                           Color('{autoblack}-{/autoblack}'),
                           Color('{autoblack}-{/autoblack}'),
                           Color('{autoblack}-{/autoblack}')])
        object_list = objects.get('Contents', None)
        if objects.get('Contents', None):
            sorted_object_list = sorted(object_list, key=lambda k: ['Key'])
            for index, an_object in enumerate(sorted_object_list):
                an_object_key = an_object.get('Key')[to_remove_len:]
                if an_object_key:
                    td.append([an_object_key,
                               str(an_object.get('Size')),
                               str(an_object.get('LastModified').replace(tzinfo=None, microsecond=0)),
                               str(an_object.get('StorageClass')),
                               # str(an_object.get('Owner')),
                               str(an_object.get('ETag')[1:-1])])
        output_ascii_table(table_title=Color('{autowhite}'+item+'{/autowhite}'),
                           table_data=td,
                           inner_heading_row_border=True)
    exit(0)
