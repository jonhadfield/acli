from __future__ import (absolute_import, print_function)
from acli.output.ec2 import (output_ec2_list, output_ec2_info)
from moto import mock_ec2
import pytest
from boto3.session import Session
session = Session(region_name="eu-west-1")


@pytest.yield_fixture(scope='function')
def ec2_instances():
    """EC2 mock service"""
    mock = mock_ec2()
    mock.start()
    client = session.client('ec2')
    client.create_security_group(GroupName='group1', Description='my first sec group')
    reservations = client.run_instances(ImageId='ami-12345', MinCount=2, MaxCount=2, SecurityGroups=['group1'])
    for i, s in enumerate(reservations.get('Instances')):
        client.create_tags(
            Resources=[s.get('InstanceId')],
            Tags=[{'Key': 'Name', 'Value': 'Bob'}])
    ec2_resource = session.resource('ec2')
    all_instances = ec2_resource.instances.all()
    yield all_instances
    mock.stop()


def test_ec2_list(ec2_instances):
    with pytest.raises(SystemExit):
        assert output_ec2_list(output_media='console', instances=ec2_instances)


def test_ec2_info(ec2_instances):
    with pytest.raises(SystemExit):
        instance = list(ec2_instances)[0]
        print(dir(instance))
        assert output_ec2_info(output_media='console', instance=instance)
