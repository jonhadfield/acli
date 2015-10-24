from __future__ import (absolute_import, print_function, unicode_literals)
from acli.services.cloudwatch import (ec2_cpu)
from acli.config import Config
from moto import mock_cloudwatch
from datetime import datetime

import pytest
from boto3.session import Session
session = Session(region_name="eu-west-1")


@pytest.yield_fixture(scope='function')
def cw_alarm():
    """ELB mock service"""
    mock = mock_cloudwatch()
    mock.start()
    cw_client = session.client('cloudwatch')
    cw_client.put_metric_alarm(AlarmName='CW Alarm Name', AlarmDescription='CW Alarm Desc',
                               ActionsEnabled=True, OKActions=[], AlarmActions=[], InsufficientDataActions=[],
                               MetricName='CPUUtilization', Namespace='AWS/EC2', Statistic='Average',
                               Dimensions=[{'Name': 'InstanceId', 'Value': 'i-0123456'}], Period=123,
                               Unit='Seconds', EvaluationPeriods=123, Threshold=123.0,
                               ComparisonOperator='GreaterThanOrEqualToThreshold')
    yield cw_client.describe_alarms()
    mock.stop()


config = Config(cli_args={'--region': 'eu-west-1',
                          '--access_key_id': 'AKIAIOSFODNN7EXAMPLE',
                          '--secret_access_key': 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'})


def test_cw(cw_alarm):
    with pytest.raises(SystemExit):
        assert ec2_cpu(aws_config=config, instance_id='i-0123456', intervals=1, period=1,
                       start=None, end=datetime.datetime.utcnow(), output_type=None)
