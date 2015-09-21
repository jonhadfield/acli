from acli.output import output_ascii_table


def output_asg_list(output_media=None, asg_list=None):
    if isinstance(asg_list, list):
        if output_media == 'console':
            td = [['name', 'instances', 'min', 'max', 'lc']]
            for asg in asg_list:
                td.append([asg.get('AutoScalingGroupName', '-'),
                           str(len(asg.get('Instances', '-'))),
                           str(asg.get('MinSize', '-')),
                           str(asg.get('MaxSize', '-')),
                           asg.get('LaunchConfigurationName', '-')
                           ])
            output_ascii_table(table_title="ASGs",
                               table_data=td,
                               inner_heading_row_border=True)
    exit(0)


def output_asg_info():
    pass
