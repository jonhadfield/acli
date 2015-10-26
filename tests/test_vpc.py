from __future__ import (absolute_import, print_function, unicode_literals)
from acli.services.vpc import (vpc_list, vpc_info)
from acli.config import Config
from moto import mock_ec2
from acli.connections import get_client

import pytest
from boto3.session import Session
session = Session(region_name="eu-west-1")


config = Config(cli_args={'--region': 'eu-west-1',
                          '--access_key_id': 'AKIAIOSFODNN7EXAMPLE',
                          '--secret_access_key': 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'})


@pytest.yield_fixture(scope='function')
def fake_vpcs():
    """VPC mock service"""
    mock = mock_ec2()
    mock.start()
    ec2_client = get_client(client_type='ec2', config=config)
    vpc = ec2_client.create_vpc(CidrBlock='10.0.0.0/16')
    print(vpc)
    ec2_client.create_subnet(VpcId=vpc['Vpc']['VpcId'], CidrBlock="10.0.0.0/18")
    yield ec2_client.describe_vpcs()
    mock.stop()


@pytest.yield_fixture(scope='function')
def fake_empty_vpcs():
    """VPC mock service"""
    mock = mock_ec2()
    mock.start()
    yield None
    mock.stop()


def test_vpc_list_service(fake_vpcs):
    with pytest.raises(SystemExit):
        assert vpc_list(aws_config=config)


def test_vpc_list_service_empty(fake_empty_vpcs, capsys):
    with pytest.raises(SystemExit):
        out, err = capsys.readouterr(vpc_list(aws_config=config))
        assert err == "No VPCs found."


def test_vpc_info_service(fake_vpcs):
    with pytest.raises(SystemExit):
        vpc_info(aws_config=config, vpc_id=fake_vpcs.get('Vpcs')[0].get('VpcId'))
        assert vpc_info(aws_config=config, vpc_id=fake_vpcs.get('Vpcs')[0].get('VpcId'))


def test_vpc_info_service_empty(fake_empty_vpcs, capsys):
    with pytest.raises(SystemExit):
        invalid_vpc_id = 'invalid'
        out, err = capsys.readouterr(vpc_info(aws_config=config, vpc_id=invalid_vpc_id))
        assert err == "Cannot find VPC: {0}".format(invalid_vpc_id)
