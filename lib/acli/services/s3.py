# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)
from acli.output.s3 import (output_s3_list, output_s3_info)
import botocore.exceptions
from acli.connections import get_client


def s3_list(aws_config=None, item=None):
    """
    @type aws_config: Config
    """
    s3_client = get_client(client_type='s3', config=aws_config)
    buckets = s3_client.list_buckets()
    # NO ITEM, SO TRY TO LIST BUCKETS
    if not item:
        if buckets.get('Buckets', None):
            output_s3_list(output_media='console', buckets=buckets.get('Buckets'))
        else:
            exit("No buckets found.")
    else:
        # ITEM PROVIDED SO EXTRACT BUCKET NAME, KEY AND THEN OUTPUT
        print("GOT AN ITEM")
        bucket_name = None
        prefix = ''
        if item and '/' in item:
            print('Got fully qualified path')
            path_elements = item.split('/')
            print('path elements: {}'.format(path_elements))
            bucket_name = path_elements[0]
            print('GOT AN ITEM AND BUCKET NAME = {}'.format(bucket_name))
            prefix = "/".join(path_elements[1:])
            print('PREFIX: {}'.format(prefix))
        else:
            bucket_name = item
        print(bucket_name)

        print('prefix = {}'.format(prefix))
        try:
            s3_client.head_bucket(Bucket=bucket_name)
        except botocore.exceptions.ClientError:
            exit("Unable to access bucket.")
        except Exception as unhandled:
            exit('Unhandled exception: {0}'.format(unhandled))
        # BUCKET DOES EXIST, SO GET CONTENTS
        try:
            objects = s3_client.list_objects(Bucket=bucket_name, Prefix=prefix, Delimiter='/')
            if not objects:
                exit('nothing there')
            print("OBJECT = ".format(str(objects)))
            common_prefixes = objects.get('CommonPrefixes', list())
            folders = list()
            for first_bit in common_prefixes:
                folders.append(first_bit)
            print(folders)
            if objects.get('Contents'):
                for content in objects.get('Contents'):
                    print("content = " + str(content.get('Key')))
            print("--END--")
            #print(objects.get('Contents', None))
            if objects:
                print(objects)
                output_s3_list(objects=objects, folders=folders, item=item)
            else:
                print("NO OBJECTS")
            # objects = s3_client.list_objects(Bucket=bucket_name, Prefix=prefix)
            # paginator = s3_client.get_paginator('list_objects')
            # for result in paginator.paginate(Bucket=bucket_name, Delimiter='/', Prefix=prefix):
            #    print("Requested top name: {0}".format(result.get('Name')))
            #    for prefix1 in result.get('CommonPrefixes'):
            #        print(prefix1)
                    # for sub in paginator.paginate(Bucket=bucket_name, Delimiter='/', Prefix='/'+prefix1.get('Prefix')):
                    #    print("child of requested: {0}".format(sub.get('Name')))
        except botocore.exceptions.ClientError as error:
            if 'NoSuchBucket' in error.response['Error']['Code']:
                exit('Bucket not found.')
            else:
                exit('Unhandled error: {0}'.format(error.response['Error']['Code']))
        # output_s3_list(output_media='console', bucket_name=bucket_name, objects=objects)
        #elif '/' not in item:
        #    print('Got potential bucket')
        #    print(buckets.get('Buckets'))
        #    bucket = [bucket for bucket in buckets.get('Buckets') if bucket.get('Name') == item]
        #    if bucket:
        #        print('bucket = {}'.format(bucket))
        #        output_s3_list(output_media='console', buckets=bucket)
        #    else:
        #        exit('Bucket does not exist.')
        #print("{0} - {1}".format(bucket_name, prefix))
            #if item in buckets.get('Buckets')
            #output_s3_list(output_media='console', item=item)


def s3_info(aws_config=None, item=None):
    """
    @type aws_config: Config
    @type item: unicode
    """
    s3_client = get_client(client_type='ec2', config=aws_config)
    print(s3_client)
    #try:
    #    hosted_zone = s3_client.get_hosted_zone(Id=zone_id)
    #    record_sets = s3_client.list_resource_record_sets(HostedZoneId=zone_id)
    #    if hosted_zone['HostedZone']['Id']:
    #        output_route53_info(output_media='console',
    #                            zone=hosted_zone,
    #                            record_sets=record_sets)
    #except AttributeError:
    #    exit("Cannot find hosted zone: {0}".format(zone_id))
    #except botocore.exceptions.ClientError:
    #    exit("Cannot request hosted zone: {0}".format(zone_id))
