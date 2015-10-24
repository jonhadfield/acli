from __future__ import (absolute_import, print_function, unicode_literals)
from acli.services.s3 import (s3_list)
from acli.config import Config
from moto import mock_s3

import pytest
from boto3.session import Session
session = Session(region_name="eu-west-1")


@pytest.yield_fixture(scope='function')
def s3_bucket():
    """S3 mock service"""
    mock = mock_s3()
    mock.start()
    s3_client = session.client('s3')
    s3_client.create_bucket(Bucket='test_bucket_1')
    yield s3_client.list_buckets()
    mock.stop()


config = Config(cli_args={'--region': 'eu-west-1',
                          '--access_key_id': 'AKIAIOSFODNN7EXAMPLE',
                          '--secret_access_key': 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'})


def test_s3_list_service(s3_bucket):
    with pytest.raises(SystemExit):
        assert s3_list(aws_config=config)
