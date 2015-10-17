from __future__ import (absolute_import, print_function, unicode_literals)
from acli.services.vpc import (vpc_list, vpc_info)
from acli.config import Config
from moto import mock_ec2

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
    client = session.client('ec2')
    client.create_vpc(CidrBlock='10.0.0.0/16')
    yield client.describe_vpcs()
    mock.stop()


@pytest.yield_fixture(scope='function')
def fake_empty_vpcs():
    """VPC mock service"""
    mock = mock_ec2()
    mock.start()
    client = session.client('ec2')
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
        assert vpc_info(aws_config=config, vpc_id=fake_vpcs.get('Vpcs')[0].get('VpcId'))


def test_vpc_info_service_empty(fake_empty_vpcs, capsys):
    with pytest.raises(SystemExit):
        invalid_vpc_id = 'invalid'
        out, err = capsys.readouterr(vpc_info(aws_config=config, vpc_id=invalid_vpc_id))
        print("out: {} err: {}".format(out, err))
        assert err == "Cannot find VPC: {0}".format(invalid_vpc_id)

