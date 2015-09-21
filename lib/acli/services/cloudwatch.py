from __future__ import (absolute_import, print_function)
from boto3.session import Session
import datetime
from acli.output.cloudwatch import output_ec2_cpu, output_asg_cpu


def get_boto3_session(aws_config):
    return Session(region_name=aws_config.region,
                   aws_access_key_id=aws_config.access_key_id,
                   aws_secret_access_key=aws_config.secret_access_key)


def ec2_stats(aws_config=None, instance_id=None, period=72000, intervals=60):
    session = get_boto3_session(aws_config)
    cloudwatch_client = session.client('cloudwatch')
    out = cloudwatch_client.get_metric_statistics(
            Namespace='AWS/EC2',
            MetricName='CPUUtilization',
            Dimensions=[
                {
                 'Name': 'InstanceId',
                 'Value': instance_id
                }
            ],
            StartTime=datetime.datetime.utcnow() - datetime.timedelta(seconds=period),
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
    output_ec2_cpu(dates=dates, values=values)
    exit(0)


def asg_stats(aws_config=None, asg_name=None, period=72000, intervals=60):
    session = get_boto3_session(aws_config)
    cloudwatch_client = session.client('cloudwatch')
    out = cloudwatch_client.get_metric_statistics(
            Namespace='AWS/EC2',
            MetricName='CPUUtilization',
            Dimensions=[
                {
                 'Name': 'AutoScalingGroupName',
                 'Value': asg_name
                }
            ],
            StartTime=datetime.datetime.utcnow() - datetime.timedelta(seconds=period),
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
    print(datapoints)
    sorted_datapoints = sorted(datapoints, key=lambda v: v.get('Timestamp'))
    dates = list()
    values = list()
    for datapoint in sorted_datapoints:
        dates.append(datapoint.get('Timestamp'))
        values.append(datapoint.get('Average'))
    output_asg_cpu(dates=dates, values=values)
    exit(0)


#def _get_network_in_utilisation_avg(conn=None, instance_id=None, period=None):
#    stat = conn.get_metric_statistics(
#        period, datetime.datetime.utcnow() - datetime.timedelta(seconds=period),
#        datetime.datetime.utcnow(),
#        'NetworkIn',
#        'AWS/EC2',
#        'Average',
#        dimensions={'InstanceId': instance_id})
#    return stat


#def _get_network_out_utilisation_avg(conn=None, instance_id=None, period=None):
#    stat = conn.get_metric_statistics(
#        period, datetime.datetime.utcnow() - datetime.timedelta(seconds=period),
#        datetime.datetime.utcnow(),
#        'NetworkOut',
#        'AWS/EC2',
#        'Average',
#        dimensions={'InstanceId': instance_id})
#    return stat


#def round_to_two(num=None):
#    return "{0:.2f}".format(num)


#def get_ec2_cpu_stats(aws_config=None, instance_id=None):
#    conn = get_cw_conn(aws_config)
#    fifteen_mins, thirty_mins, one_hour = "-", "-", "-"
#    _fifteen_mins = _get_cpu_utilisation_avg(conn, instance_id=instance_id, period=900)
#    if _fifteen_mins:
#        fifteen_mins = round_to_two(_fifteen_mins[0].get('Average'))
#    _thirty_mins = _get_cpu_utilisation_avg(conn, instance_id=instance_id, period=1800)
#    if _thirty_mins:
#        thirty_mins = round_to_two(_thirty_mins[0].get('Average'))
#    _one_hour = _get_cpu_utilisation_avg(conn, instance_id=instance_id, period=3600)
#    if _one_hour:
#        one_hour = round_to_two(_one_hour[0].get('Average'))
#    return {'fifteen_mins': fifteen_mins,
#            'thirty_mins': thirty_mins,
#            'one_hour': one_hour}


#def ec2_stats(aws_config=None, instance_id=None):
#    output_ec2_stats(output_media='console',
#                     instance=get_ec2_instance(aws_config,
#                                               instance_id=instance_id),
#                     cpu_stats=get_ec2_cpu_stats(aws_config=aws_config,
#                                                 instance_id=instance_id),
#                     network_stats=get_ec2_network_stats(aws_config=aws_config,
#                                                         instance_id=instance_id)
#                     )


#def get_ec2_network_stats(aws_config=None, instance_id=None):
#    conn = get_cw_conn(aws_config)
#    one_hour_in, six_hours_in, twelve_hours_in = "-", "-", "-"
#    one_hour_out, six_hours_out, twelve_hours_out = "-", "-", "-"
#    _one_hour_in = _get_network_in_utilisation_avg(conn, instance_id=instance_id, period=3600)
#    if _one_hour_in:
#        one_hour_in = round_to_two(_one_hour_in[0].get('Average'))
#    _six_hours_in = _get_network_in_utilisation_avg(conn, instance_id=instance_id, period=21600)
#    if _six_hours_in:
#        six_hours_in = round_to_two(_six_hours_in[0].get('Average'))
#    _twelve_hours_in = _get_network_in_utilisation_avg(conn, instance_id=instance_id, period=43200)
#    if _twelve_hours_in:
#        twelve_hours_in = round_to_two(_twelve_hours_in[0].get('Average'))
#    _one_hour_out = _get_network_out_utilisation_avg(conn, instance_id=instance_id, period=3600)
#    if _one_hour_out:
#        one_hour_out = round_to_two(_one_hour_out[0].get('Average'))
#    _six_hours_out = _get_network_out_utilisation_avg(conn, instance_id=instance_id, period=21600)
#    if _six_hours_out:
#        six_hours_out = round_to_two(_six_hours_out[0].get('Average'))
#    _twelve_hours_out = _get_network_out_utilisation_avg(conn, instance_id=instance_id, period=43200)
#    if _twelve_hours_out:
#        twelve_hours_out = round_to_two(_twelve_hours_out[0].get('Average'))
#    return {'one_hour_in': one_hour_in,
#            'six_hours_in': six_hours_in,
#            'twelve_hours_in': twelve_hours_in,
#            'one_hour_out': one_hour_out,
#            'six_hours_out': six_hours_out,
#            'twelve_hours_out': twelve_hours_out}
