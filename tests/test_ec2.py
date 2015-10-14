from __future__ import (absolute_import, print_function, unicode_literals)
from acli.output.ec2 import (output_ec2_list, output_ec2_info)
from acli.services.ec2 import (ec2_list, ec2_info)
from acli.config import Config
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
    print(list(all_instances)[0].id)
    yield all_instances
    mock.stop()


config = Config(cli_args={'--region': 'eu-west-1',
                          '--access_key_id': 'AKIAIOSFODNN7EXAMPLE',
                          '--secret_access_key': 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'})

@mock_ec2
def test_ec2_list_service():
    with pytest.raises(SystemExit):
        assert ec2_list(aws_config=config)


def test_ec2_info_service(ec2_instances):
    config = Config(cli_args={'--region': 'eu-west-1',
                              '--access_key_id': 'AKIAIOSFODNN7EXAMPLE',
                              '--secret_access_key': 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'})
    with pytest.raises(SystemExit):
        print(list(ec2_instances))
        assert ec2_info(aws_config=config, instance_id=list(ec2_instances)[0].id)


def test_ec2_list_output(ec2_instances):
    with pytest.raises(SystemExit):
        assert output_ec2_list(output_media='console', instances=ec2_instances)


def test_ec2_output(ec2_instances):
    with pytest.raises(SystemExit):
        instance = list(ec2_instances)[0]
        print(dir(instance))
        assert output_ec2_info(output_media='console', instance=instance)
