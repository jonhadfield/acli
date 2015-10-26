from __future__ import (absolute_import, print_function, unicode_literals)
from acli.output.route53 import (output_route53_list, output_route53_info)
from acli.services.route53 import (route53_list, route53_info)
from acli.config import Config
from moto import mock_route53

import pytest
from boto3.session import Session
session = Session(region_name="eu-west-1")


@pytest.yield_fixture(scope='function')
def route53_zone():
    """ELB mock service"""
    mock = mock_route53()
    mock.start()
    client = session.client('route53')
    client.create_hosted_zone(Name="testdns.aws.com", CallerReference='auniqueref',
                              HostedZoneConfig={'Comment': 'string', 'PrivateZone': False})
    yield client.list_hosted_zones()
    mock.stop()


config = Config(cli_args={'--region': 'eu-west-1',
                          '--access_key_id': 'AKIAIOSFODNN7EXAMPLE',
                          '--secret_access_key': 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'})


def test_elb_list_service(route53_zone):
    with pytest.raises(SystemExit):
        assert route53_list(aws_config=config)


def test_elb_info_service(route53_zone):
    with pytest.raises(SystemExit):
        print(route53_zone)
        assert route53_info(aws_config=config, zone_id=route53_zone.get('HostedZones')[0].get('Id'))
