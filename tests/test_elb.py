from __future__ import (absolute_import, print_function, unicode_literals)
from acli.output.elb import (output_elb_info, output_elbs)
from acli.services.elb import (elb_info, elb_list)
from acli.config import Config
from moto import mock_elb
import pytest
from boto3.session import Session
session = Session(region_name="eu-west-1")


@pytest.yield_fixture(scope='function')
def elb_instances():
    """ELB mock service"""
    mock = mock_elb()
    mock.start()
    client = session.client('elb')
    zones = ['eu-west-1a', 'eu-west-1b']
    listeners = [{
            'Protocol': 'string',
            'LoadBalancerPort': 123,
            'InstanceProtocol': 'string',
            'InstancePort': 123,
            'SSLCertificateId': 'string'}]
    client.create_load_balancer(LoadBalancerName='my-lb', AvailabilityZones=zones, Listeners=listeners)
    yield client.describe_load_balancers()
    mock.stop()


config = Config(cli_args={'--region': 'eu-west-1',
                          '--access_key_id': 'AKIAIOSFODNN7EXAMPLE',
                          '--secret_access_key': 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'})


def test_elb_list_service(elb_instances):
    with pytest.raises(SystemExit):
        assert elb_list(aws_config=config)


def test_elb_info_service(elb_instances):
    with pytest.raises(SystemExit):
        assert elb_info(aws_config=config, elb_name='my-lb')
