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
    if not item:
        if buckets.get('Buckets', None):
            output_s3_list(output_media='console', buckets=buckets.get('Buckets'))
        else:
            exit("No buckets found.")
    else:
        bucket_name = None
        prefix = None
        # if item and '/' in item:
        print('Got fully qualified path')
        path_elements = item.split('/')
        bucket_name = path_elements[0]
        prefix = "/".join(path_elements[1:])
        print('prefix = {}'.format(prefix))
        try:
            objects = s3_client.list_objects(Bucket=bucket_name, Prefix=prefix)
            if objects.get('Contents'):
                for content in objects.get('Contents'):
                    print(content)
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
