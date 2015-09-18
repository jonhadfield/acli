from __future__ import (absolute_import, print_function)
from acli.output.ec2 import (output_ec2_list, output_ec2_info)
from moto import mock_ec2
import pytest
from boto.ec2.tag import Tag
import boto


@pytest.yield_fixture(scope='function')
def ec2():
    """EC2 mock service"""
    mock = mock_ec2()
    mock.start()
    conn = boto.ec2.connect_to_region("eu-west-1")

    reservations = conn.run_instances(image_id='ami-12345', min_count=2, max_count=2)
    for i, s in enumerate(reservations.instances):
        conn.create_tags(
            resource_ids=[s.id],
            tags={'Name': 'BOB'})
    yield{'servers': reservations}
    mock.stop()


def test_ec2_list(ec2):
    with pytest.raises(SystemExit):
        assert output_ec2_list(output_media='console')


def test_ec2_info(ec2):
    with pytest.raises(SystemExit):
        assert output_ec2_info(output_media='console', instance=ec2.get('servers').instances[0])
