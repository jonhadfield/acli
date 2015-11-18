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
        if buckets.get('Buckets'):
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
            if not any((objects.get('CommonPrefixes'),
                        (objects.get('Contents')))):
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
        s3_object = s3_client.get_object(Bucket=bucket_name, Key=prefix)
        output_s3_info(s3_object=s3_object, key=prefix, bucket=bucket_name)
    except botocore.exceptions.ClientError as error:
        if 'NoSuchBucket' in error.response['Error']['Code']:
            exit('Bucket not found.')
        else:
            exit('Unhandled error: {0}'.format(error.response['Error']['Code']))


def s3_cp(aws_config=None, source=None, dest=None):
    """
    @type aws_config: Config
    @type source: unicode
    @type dest: unicode
    """
    from acli.utils import (is_readable,
                            is_writeable)
    from boto3.s3.transfer import S3Transfer, TransferConfig
    import os
    config = TransferConfig(
                            multipart_threshold=200 * 1024 * 1024,
                            max_concurrency=10,
                            num_download_attempts=10,
                            )

    s3_prefix = 's3://'
    s3_client = get_client(client_type='s3', config=aws_config)
    if source.startswith(s3_prefix) and not dest.startswith(s3_prefix):
        # COPYING FROM S3 TO LOCAL
        print('Transferring: {0} to: {1}'.format(source, dest))
        s3_location = source[5:].split('/')
        bucket_name = s3_location[0]
        s3_source = '/'.join(s3_location[1:])
        check_bucket_accessible(s3_client=s3_client, bucket_name=bucket_name)
        if dest == '/':
            dest = '{0}{1}'.format(os.path.abspath(dest), s3_location[-1])
        elif dest == '.' or dest.endswith('/'):
            print('first')
            dest = '{0}/{1}'.format(os.path.abspath(dest), s3_location[-1])
        elif os.path.isdir(os.path.abspath(dest)):
            dest = '{0}/{1}'.format(dest, s3_location[-1])
        transfer = S3Transfer(s3_client, config)
        try:
            transfer.download_file(bucket_name, s3_source, dest)
        except BaseException as e:
            if e.strerror == 'Permission denied':
                exit('Permission denied.')
            else:
                print('Unhandled exception: {0}'.format(e))
    elif source.startswith(s3_prefix) and dest.startswith(s3_prefix):
        # COPYING FROM S3 TO S3
        print('Transferring: {0} to: {1}'.format(source, dest))
        exit('Not yet implemented.')
    elif not source.startswith(s3_prefix) and dest.startswith(s3_prefix):
        try:
            # COPYING ITEM(S) FROM LOCAL TO S3
            print('Transferring: {0} to: {1}'.format(source, dest))
            if not os.path.isfile(source):
                exit('File transfers only for now.')
            else:
                # COPY LOCAL FILE TO S3
                if not is_readable(source):
                    exit('Cannot access: {0}'.format(source))
                s3_location = dest[5:].split('/')
                bucket_name = s3_location[0]
                s3_dest = '/'.join(s3_location[1:])
                # COPYING FILE TO A FOLDER
                if dest.endswith('/'):
                    file_name = source.split('/')[-1]
                    s3_dest += file_name
                check_bucket_accessible(s3_client=s3_client, bucket_name=bucket_name)
                transfer = S3Transfer(s3_client, config)
                transfer.upload_file(source, bucket_name, s3_dest)
        except Exception as e:
            print('Unhandled exception: {0}'.format(e))
    else:
        exit('Source or dest must be an S3 location defined with s3://.')
    exit()
