# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)
from acli.output.s3 import (output_s3_list, output_s3_info)
import botocore.exceptions
from acli.connections import get_client


def check_bucket_accessible(s3_client=None, bucket_name=None):
    try:
        s3_client.head_bucket(Bucket=bucket_name)
        return True
    except botocore.exceptions.ClientError:
        exit("Unable to access bucket.")
    except Exception as unhandled:
        exit('Unhandled exception: {0}'.format(unhandled))


def s3_list(aws_config=None, item=None):
    """
    @type aws_config: Config
    """
    s3_client = get_client(client_type='s3', config=aws_config)
    buckets = s3_client.list_buckets()
    if not item:
        if buckets.get('Buckets', None):
            output_s3_list(buckets=buckets.get('Buckets'))
        else:
            exit("No buckets found.")
    else:
        prefix = ''
        if item and '/' in item:
            path_elements = item.split('/')
            bucket_name = path_elements[0]
            prefix = "/".join(path_elements[1:])
        else:
            bucket_name = item
        check_bucket_accessible(s3_client=s3_client, bucket_name=bucket_name)
        try:
            objects = s3_client.list_objects(Bucket=bucket_name, Prefix=prefix, Delimiter='/')
            if not any((objects.get('CommonPrefixes', None),
                        (objects.get('Contents', None) and len(objects.get('Contents')) > 1))):
                exit('Nothing found in: {0}'.format(item[:-1]))
            common_prefixes = objects.get('CommonPrefixes', list())
            folders = list()
            for first_bit in common_prefixes:
                folders.append(first_bit)
            output_s3_list(objects=objects, folders=folders, item=item, bucket_name=bucket_name)
        except botocore.exceptions.ClientError as error:
            if 'NoSuchBucket' in error.response['Error']['Code']:
                exit('Bucket not found.')
            else:
                exit('Unhandled error: {0}'.format(error.response['Error']['Code']))


def s3_info(aws_config=None, item=None):
    """
    @type aws_config: Config
    @type item: unicode
    """
    s3_client = get_client(client_type='s3', config=aws_config)
    prefix = ''
    if item and '/' in item:
        path_elements = item.split('/')
        bucket_name = path_elements[0]
        prefix = "/".join(path_elements[1:])
        if prefix.endswith('/'):
            prefix = prefix[:-1]
    else:
        bucket_name = item
    check_bucket_accessible(s3_client=s3_client, bucket_name=bucket_name)
    try:
        s3_object = s3_client.list_objects(Bucket=bucket_name, Prefix=prefix, Delimiter='/')
        if 'Contents' in s3_object.keys():
            output_s3_info(s3_object=s3_object)
        else:
            # TODO: Decide on output or message
            print("path, not object was requested")
    except botocore.exceptions.ClientError as error:
        if 'NoSuchBucket' in error.response['Error']['Code']:
            exit('Bucket not found.')
        else:
            exit('Unhandled error: {0}'.format(error.response['Error']['Code']))
