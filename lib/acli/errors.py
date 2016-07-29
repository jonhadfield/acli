# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)

from botocore.exceptions import NoCredentialsError, NoRegionError, ClientError


def handle_boto_errors(function):
    def handle_errors(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except NoCredentialsError:
            exit('Credentials not found. See here for more information:\n'
                 'http://boto3.readthedocs.org/en/latest/guide/configuration.html#configuration-files')
        except NoRegionError:
            exit('Cannot perform this task without specifying an AWS region.\n'
                 'Please check your boto/aws settings or specify using \'acli --region=<region>\'.')
        except ClientError as ce:
            response = ce.response
            error_args = ce.args
            error_message = response['Error']['Message']
            error_code = response['Error']['Code']
            joined_args = "".join(error_args)
            if error_code in ('AccessDenied', 'AccessDeniedException'):
                if 'iam:ListUsers' in error_message:
                    exit('You do not have permission to access IAM user list.\nDetail: {0}'.format(error_message))
                elif 'DescribeLaunchConfigurations' in joined_args:
                    exit('You do not have permission to list Launch Configurations.')
                elif 'DescribeAutoScalingGroups' in joined_args:
                    exit('You do not have permission to list Auto Scaling Groups.')
                elif 'DescribeLoadBalancers' in joined_args:
                    exit('You do not have permission to list Elastic Load Balancers.')
                elif 'ListDomainNames' in joined_args:
                    exit('You do not have permission to list Elastic Search domains.')
                elif 'ListHostedZones' in joined_args:
                    exit('You do not have permission to list Route53 zones.')
                else:
                    raise
            elif error_code == 'UnauthorizedOperation':
                if 'DescribeImages' in joined_args:
                    exit('You do not have permission to list AMIs.')
                elif 'DescribeInstances' in joined_args:
                    exit('You do not have permission to list instances.')
                elif 'DescribeAddresses' in joined_args:
                    exit('You do not have permission to list addresses.')
                elif 'DescribeVpcs' in joined_args:
                    exit('You do not have permission to list VPCs.')
                elif 'DescribeSecurityGroups' in joined_args:
                    exit('You do not have permission to list Security Groups.')

                else:
                    raise
            else:
                raise
        except Exception:
            raise
    return handle_errors
