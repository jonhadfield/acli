from __future__ import (absolute_import, print_function)
import datetime
import boto.ec2.cloudwatch as cw
from acli.output.cloudwatch import output_ec2_stats
from acli.services.ec2 import get_ec2_instance


def get_cw_conn(aws_config):
    return cw.connect_to_region(region_name=aws_config.region,
                                aws_access_key_id=aws_config.access_key_id,
                                aws_secret_access_key=aws_config.secret_access_key)


def _get_cpu_utilisation_avg(conn=None, instance_id=None, period=None):
    stat = conn.get_metric_statistics(
        period, datetime.datetime.utcnow() - datetime.timedelta(seconds=period),
        datetime.datetime.utcnow(),
        'CPUUtilization',
        'AWS/EC2',
        'Average',
        dimensions={'InstanceId': instance_id},
        unit='Percent')
    return stat


def _get_network_in_utilisation_avg(conn=None, instance_id=None, period=None):
    stat = conn.get_metric_statistics(
        period, datetime.datetime.utcnow() - datetime.timedelta(seconds=period),
        datetime.datetime.utcnow(),
        'NetworkIn',
        'AWS/EC2',
        'Average',
        dimensions={'InstanceId': instance_id})
    return stat


def _get_network_out_utilisation_avg(conn=None, instance_id=None, period=None):
    stat = conn.get_metric_statistics(
        period, datetime.datetime.utcnow() - datetime.timedelta(seconds=period),
        datetime.datetime.utcnow(),
        'NetworkOut',
        'AWS/EC2',
        'Average',
        dimensions={'InstanceId': instance_id})
    return stat


def round_to_two(num=None):
    return "{0:.2f}".format(num)


def get_ec2_cpu_stats(aws_config=None, instance_id=None):
    conn = get_cw_conn(aws_config)
    fifteen_mins, thirty_mins, one_hour = "-", "-", "-"
    _fifteen_mins = _get_cpu_utilisation_avg(conn, instance_id=instance_id, period=900)
    if _fifteen_mins:
        fifteen_mins = round_to_two(_fifteen_mins[0].get('Average'))
    _thirty_mins = _get_cpu_utilisation_avg(conn, instance_id=instance_id, period=1800)
    if _thirty_mins:
        thirty_mins = round_to_two(_thirty_mins[0].get('Average'))
    _one_hour = _get_cpu_utilisation_avg(conn, instance_id=instance_id, period=3600)
    if _one_hour:
        one_hour = round_to_two(_one_hour[0].get('Average'))
    return {'fifteen_mins': fifteen_mins,
            'thirty_mins': thirty_mins,
            'one_hour': one_hour}


def ec2_stats(aws_config=None, instance_id=None):
    output_ec2_stats(output_media='console',
                     instance=get_ec2_instance(aws_config,
                                               instance_id=instance_id),
                     cpu_stats=get_ec2_cpu_stats(aws_config=aws_config,
                                                 instance_id=instance_id),
                     network_stats=get_ec2_network_stats(aws_config=aws_config,
                                                         instance_id=instance_id)
                     )


def get_ec2_network_stats(aws_config=None, instance_id=None):
    conn = get_cw_conn(aws_config)
    one_hour_in, six_hours_in, twelve_hours_in = "-", "-", "-"
    one_hour_out, six_hours_out, twelve_hours_out = "-", "-", "-"
    _one_hour_in = _get_network_in_utilisation_avg(conn, instance_id=instance_id, period=3600)
    if _one_hour_in:
        one_hour_in = round_to_two(_one_hour_in[0].get('Average'))
    _six_hours_in = _get_network_in_utilisation_avg(conn, instance_id=instance_id, period=21600)
    if _six_hours_in:
        six_hours_in = round_to_two(_six_hours_in[0].get('Average'))
    _twelve_hours_in = _get_network_in_utilisation_avg(conn, instance_id=instance_id, period=43200)
    if _twelve_hours_in:
        twelve_hours_in = round_to_two(_twelve_hours_in[0].get('Average'))
    _one_hour_out = _get_network_out_utilisation_avg(conn, instance_id=instance_id, period=3600)
    if _one_hour_out:
        one_hour_out = round_to_two(_one_hour_out[0].get('Average'))
    _six_hours_out = _get_network_out_utilisation_avg(conn, instance_id=instance_id, period=21600)
    if _six_hours_out:
        six_hours_out = round_to_two(_six_hours_out[0].get('Average'))
    _twelve_hours_out = _get_network_out_utilisation_avg(conn, instance_id=instance_id, period=43200)
    if _twelve_hours_out:
        twelve_hours_out = round_to_two(_twelve_hours_out[0].get('Average'))
    return {'one_hour_in': one_hour_in,
            'six_hours_in': six_hours_in,
            'twelve_hours_in': twelve_hours_in,
            'one_hour_out': one_hour_out,
            'six_hours_out': six_hours_out,
            'twelve_hours_out': twelve_hours_out}
