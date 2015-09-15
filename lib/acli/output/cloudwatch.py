from acli.output import output_ascii_table, dash_if_none


def output_ec2_stats(output_media=None, instance=None, cpu_stats=None):
    if output_media == 'console':
        td = list()
        td.append(['id', instance.id])
        td.append(['name', instance.tags.get('Name', '-')])
        td.append(['cpu 1min / 5min / 15min',
                   "{0} / {1} / {2}".format(cpu_stats.get('one_min'),
                                            cpu_stats.get('five_mins'),
                                            cpu_stats.get('fifteen_mins'))])
        output_ascii_table(table_title="EC2 Stats",
                           table_data=td)
