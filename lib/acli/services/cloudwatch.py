# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)
import datetime
from acli.output.cloudwatch import (output_ec2_cpu, output_ec2_net,
                                    output_asg_cpu, output_ec2_vols)
from acli.services.ec2 import ec2_get_instance_vols
from acli.connections import get_client
from acli.errors import handle_boto_errors


@handle_boto_errors
def ec2_net(aws_config=None, instance_id=None, intervals=None, period=None,
            start=None, end=datetime.datetime.utcnow()):
    """
    @type aws_config: Config
    @type instance_id: unicode
    @type intervals: int
    @type period: int
    @type start: datetime
    @type end: datetime
    """
    if not intervals:
        intervals = 60
    if not period:
        period = 7200
    cloudwatch_client = get_client(client_type='cloudwatch', config=aws_config)
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


@handle_boto_errors
def ec2_cpu(aws_config=None, instance_id=None, intervals=None, period=None,
            start=None, end=datetime.datetime.utcnow()):
    """
    @type aws_config: Config
    @type instance_id: unicode
    @type intervals: int
    @type period: int
    @type start: datetime
    @type end: datetime
    """
    if not intervals:
        intervals = 60
    if not period:
        period = 7200
    cloudwatch_client = get_client(client_type='cloudwatch', config=aws_config)
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
    datapoints = out.get('Datapoints')
    sorted_datapoints = sorted(datapoints, key=lambda v: v.get('Timestamp'))
    dates = list()
    values = list()
    for datapoint in sorted_datapoints:
        dates.append(datapoint.get('Timestamp'))
        values.append(datapoint.get('Average'))
    output_ec2_cpu(dates=dates, values=values, instance_id=instance_id)
    exit(0)


@handle_boto_errors
def asg_cpu(aws_config=None, asg_name=None, start=None, period=None, intervals=None,
            output_type=None):
    """
    @type aws_config: Config
    @type asg_name: unicode
    @type intervals: int
    @type period: int
    @type start: datetime
    @type output_type: unicode
    """
    end = datetime.datetime.utcnow()
    if not output_type or output_type == 'graph':
        if not intervals:
            intervals = 60
        if not period:
            period = 7200
        cloudwatch_client = get_client(client_type='cloudwatch', config=aws_config)
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


@handle_boto_errors
def ec2_vol(aws_config=None, instance_id=None, intervals=None, period=None,
            start=None, end=datetime.datetime.utcnow()):
    """
    @type aws_config: Config
    @type instance_id: unicode
    @type intervals: int
    @type period: int
    @type start: datetime
    @type end: datetime
    """
    ebs_vols = ec2_get_instance_vols(aws_config=aws_config, instance_id=instance_id)
    if not intervals:
        intervals = 60
    if not period:
        period = 7200

    cloudwatch_client = get_client(client_type='cloudwatch', config=aws_config)
    if not start:
        start = end - datetime.timedelta(seconds=period)
    vol_datapoints = list()
    for ebs_vol in ebs_vols:
        read_ops = cloudwatch_client.get_metric_statistics(
                Namespace='AWS/EBS',
                MetricName='VolumeReadBytes',
                Dimensions=[{'Name': 'VolumeId', 'Value': ebs_vol['Ebs']['VolumeId']}],
                StartTime=start,
                EndTime=datetime.datetime.utcnow(),
                Period=intervals,
                Statistics=['Average'],
                Unit='Bytes'
        )
        write_ops = cloudwatch_client.get_metric_statistics(
                Namespace='AWS/EBS',
                MetricName='VolumeWriteBytes',
                Dimensions=[{'Name': 'VolumeId', 'Value': ebs_vol['Ebs']['VolumeId']}],
                StartTime=start,
                EndTime=datetime.datetime.utcnow(),
                Period=intervals,
                Statistics=['Average'],
                Unit='Bytes'
            )
        sorted_read_datapoints = sorted(read_ops.get('Datapoints'), key=lambda v: v.get('Timestamp'))
        sorted_write_datapoints = sorted(write_ops.get('Datapoints'), key=lambda v: v.get('Timestamp'))
        read_dates = [x1.get('Timestamp') for x1 in sorted_read_datapoints]
        read_values = [x2.get('Average') for x2 in sorted_read_datapoints]
        write_dates = [y1.get('Timestamp') for y1 in sorted_write_datapoints]
        write_values = [y2.get('Average') for y2 in sorted_write_datapoints]
        vol_datapoints.append({'device_name': ebs_vol['DeviceName'],
                               'read_dates': read_dates, 'read_values': read_values,
                               'write_dates': write_dates, 'write_values': write_values})
    output_ec2_vols(vols_datapoints=vol_datapoints, instance_id=instance_id)
