# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)

from botocore.exceptions import NoCredentialsError, NoRegionError


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
        except Exception as e:
            exit('Unhandled exception: {0}'.format(e))
    return handle_errors


