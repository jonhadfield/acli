import datetime
import boto.ec2.cloudwatch as cw


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
                   dimensions={'InstanceId': instance_id})
    return stat


def round_to_two(num=None):
    return "{0:.2f}".format(num)


def get_ec2_cpu_stats(aws_config=None, instance_id=None):
    conn = get_cw_conn(aws_config)
    one_min = "-"
    five_mins = "-"
    fifteen_mins = "-"
    _one_min = _get_cpu_utilisation_avg(conn, instance_id=instance_id, period=60)
    if _one_min:
        one_min = round_to_two(_one_min[0].get('Average'))
    _five_mins = _get_cpu_utilisation_avg(conn, instance_id=instance_id, period=300)
    if _five_mins:
        five_mins = round_to_two(_five_mins[0].get('Average'))
    _fifteen_mins = _get_cpu_utilisation_avg(conn, instance_id=instance_id, period=900)
    if _fifteen_mins:
        fifteen_mins = round_to_two(_fifteen_mins[0].get('Average'))
    return {'one_min': one_min,
            'five_mins': five_mins,
            'fifteen_mins': fifteen_mins}