from __future__ import (absolute_import, print_function)
from boto3.session import Session
import datetime
from acli.output.cloudwatch import (output_ec2_cpu, output_ec2_net, output_asg_cpu)


def get_boto3_session(aws_config):
    return Session(region_name=aws_config.region,
                   aws_access_key_id=aws_config.access_key_id,
                   aws_secret_access_key=aws_config.secret_access_key)


def ec2_cpu(aws_config=None, instance_id=None, intervals=None, period=None,
            start=None, end=datetime.datetime.utcnow(), output_type=None):
    if not intervals:
        intervals = 60
    if not period:
        period = 7200
    print("output type: {0}".format(output_type))
    session = get_boto3_session(aws_config)
    cloudwatch_client = session.client('cloudwatch')
    if not start:
        start = end - datetime.timedelta(seconds=period)
    out = cloudwatch_client.get_metric_statistics(
            Namespace='AWS/EC2',
            MetricName='CPUUtilization',
            Dimensions=[
                {
                 'Name': 'InstanceId',
                 'Value': instance_id
                }
            ],
            StartTime=start,
            EndTime=datetime.datetime.utcnow(),
            Period=intervals,
            Statistics=[
                'Average',
            ],
            Unit='Percent'
        )
    # 'SampleCount'|'Average'|'Sum'|'Minimum'|'Maximum',
    # Unit='Seconds'|'Microseconds'|'Milliseconds'|'Bytes'|'Kilobytes'|'Megabytes'|'Gigabytes'|'Terabytes'|'Bits'|'Kilobits'|'Megabits'|'Gigabits'|'Terabits'|'Percent'|'Count'|'Bytes/Second'|'Kilobytes/Second'|'Megabytes/Second'|'Gigabytes/Second'|'Terabytes/Second'|'Bits/Second'|'Kilobits/Second'|'Megabits/Second'|'Gigabits/Second'|'Terabits/Second'|'Count/Second'|'None'
    datapoints = out.get('Datapoints')
    sorted_datapoints = sorted(datapoints, key=lambda v: v.get('Timestamp'))
    dates = list()
    values = list()
    for datapoint in sorted_datapoints:
        dates.append(datapoint.get('Timestamp'))
        values.append(datapoint.get('Average'))
    output_ec2_cpu(dates=dates, values=values, instance_id=instance_id)
    exit(0)


def ec2_get_vol_ids(instance_id=None, session=None):
    return True


def ec2_ebs_vols(aws_config=None, instance_id=None, intervals=None, period=None,
                 start=None, end=datetime.datetime.utcnow(), output_type=None):
    if not intervals:
        intervals = 60
    if not period:
        period = 7200
    print("output type: {0}".format(output_type))
    session = get_boto3_session(aws_config)
    vol_ids = ec2_get_vol_ids(instance_id=instance_id, session=session)

    cloudwatch_client = session.client('cloudwatch')
    if not start:
        start = end - datetime.timedelta(seconds=period)
    out = cloudwatch_client.get_metric_statistics(
            Namespace='AWS/EBS',
            MetricName='DiskReadOps',
            Dimensions=[
                {
                 'Name': 'VolumeId',
                 'Value': volume_id
                }
            ],
            StartTime=start,
            EndTime=datetime.datetime.utcnow(),
            Period=intervals,
            Statistics=[
                'Average',
            ],
            Unit='Percent'
        )
    # 'SampleCount'|'Average'|'Sum'|'Minimum'|'Maximum',
    # Unit='Seconds'|'Microseconds'|'Milliseconds'|'Bytes'|'Kilobytes'|'Megabytes'|'Gigabytes'|'Terabytes'|'Bits'|'Kilobits'|'Megabits'|'Gigabits'|'Terabits'|'Percent'|'Count'|'Bytes/Second'|'Kilobytes/Second'|'Megabytes/Second'|'Gigabytes/Second'|'Terabytes/Second'|'Bits/Second'|'Kilobits/Second'|'Megabits/Second'|'Gigabits/Second'|'Terabits/Second'|'Count/Second'|'None'
    datapoints = out.get('Datapoints')
    sorted_datapoints = sorted(datapoints, key=lambda v: v.get('Timestamp'))
    dates = list()
    values = list()
    for datapoint in sorted_datapoints:
        dates.append(datapoint.get('Timestamp'))
        values.append(datapoint.get('Average'))
    output_ec2_cpu(dates=dates, values=values, instance_id=instance_id)
    exit(0)


def ec2_net(aws_config=None, instance_id=None, intervals=None, period=None,
            start=None, end=datetime.datetime.utcnow(), output_type=None):
    if not intervals:
        intervals = 60
    if not period:
        period = 7200
    print("output type: {0}".format(output_type))
    session = get_boto3_session(aws_config)
    cloudwatch_client = session.client('cloudwatch')
    if not start:
        start = end - datetime.timedelta(seconds=period)
    net_in = cloudwatch_client.get_metric_statistics(
            Namespace='AWS/EC2',
            MetricName='NetworkIn',
            Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
            StartTime=start,
            EndTime=datetime.datetime.utcnow(),
            Period=intervals,
            Statistics=['Average'],
            Unit='Bytes'
        )
    net_out = cloudwatch_client.get_metric_statistics(
            Namespace='AWS/EC2',
            MetricName='NetworkOut',
            Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
            StartTime=start,
            EndTime=datetime.datetime.utcnow(),
            Period=intervals,
            Statistics=['Average'],
            Unit='Bytes'
        )

    # 'SampleCount'|'Average'|'Sum'|'Minimum'|'Maximum',
    # Unit='Seconds'|'Microseconds'|'Milliseconds'|'Bytes'|'Kilobytes'|'Megabytes'|'Gigabytes'|'Terabytes'|'Bits'|'Kilobits'|'Megabits'|'Gigabits'|'Terabits'|'Percent'|'Count'|'Bytes/Second'|'Kilobytes/Second'|'Megabytes/Second'|'Gigabytes/Second'|'Terabytes/Second'|'Bits/Second'|'Kilobits/Second'|'Megabits/Second'|'Gigabits/Second'|'Terabits/Second'|'Count/Second'|'None'
    net_in_datapoints, net_out_datapoints = net_in.get('Datapoints'), net_out.get('Datapoints')
    if not all((net_in_datapoints, net_out_datapoints)):
        exit("Metrics unavailable.")
    sorted_net_in_datapoints = sorted(net_in_datapoints, key=lambda v: v.get('Timestamp'))
    sorted_net_out_datapoints = sorted(net_out_datapoints, key=lambda v: v.get('Timestamp'))
    in_dates = [x1.get('Timestamp') for x1 in sorted_net_in_datapoints]
    in_values = [x2.get('Average') for x2 in sorted_net_in_datapoints]
    out_dates = [x3.get('Timestamp') for x3 in sorted_net_out_datapoints]
    out_values = [x4.get('Average') for x4 in sorted_net_out_datapoints]
    output_ec2_net(in_dates=in_dates, in_values=in_values,
                   out_dates=out_dates, out_values=out_values,
                   instance_id=instance_id)
    exit(0)


def asg_cpu(aws_config=None, asg_name=None, intervals=None, period=None,
            start=None, end=datetime.datetime.utcnow(), output_type=None):
    if not output_type or output_type == 'graph':
        if not intervals:
            intervals = 60
        if not period:
            period = 7200
        session = get_boto3_session(aws_config)
        cloudwatch_client = session.client('cloudwatch')
        if not start:
            start = end - datetime.timedelta(seconds=period)
        out = cloudwatch_client.get_metric_statistics(
                Namespace='AWS/EC2',
                MetricName='CPUUtilization',
                Dimensions=[
                    {
                     'Name': 'AutoScalingGroupName',
                     'Value': asg_name
                    }
                ],
                StartTime=start,
                EndTime=datetime.datetime.utcnow(),
                Period=intervals,
                Statistics=[
                    'Average',
                ],
                Unit='Percent'
            )
        datapoints = out.get('Datapoints')
        sorted_datapoints = sorted(datapoints, key=lambda v: v.get('Timestamp'))
        dates = [y1.get('Timestamp') for y1 in sorted_datapoints]
        values = [y2.get('Average') for y2 in sorted_datapoints]

        output_asg_cpu(dates=dates, values=values, asg_name=asg_name)
        exit(0)
    elif output_type == 'table':
        print("table")
        exit(0)