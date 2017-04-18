# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)

import humanize
from colorclass import Color, Windows

from acli.output import (output_ascii_table, output_ascii_table_list, dash_if_none)
from external.six import iteritems

Windows.enable(auto_colors=True, reset_atexit=True)


def get_tag(name=None, tags=None):
    if tags:
        for tag in tags:
            if tag.get('Key') == name:
                return tag.get('Value')


def colour_state(state=None):
    if not state:
        return Color('{autoblack}-{/autoblack}')
    elif state == 'available':
        return Color('{autogreen}' + state + '{/autogreen}')
    elif state in ('deleting', 'deleted'):
        return Color('{autored}' + state + '{/autored}')
    elif state == 'creating':
        return Color('{autoyellow}' + state + '{/autoyellow}')


def output_filesystems(filesystems=None, mount_targets=None):
    """
    @type filesystems: dict
    @type mount_targets: list
    """
    td = list()
    table_header = [Color('{autoblue}id{/autoblue}'),
                    Color('{autoblue}name{/autoblue}'),
                    Color('{autoblue}state{/autoblue}'),
                    Color('{autoblue}size / time (UTC){/autoblue}'),
                    Color('{autoblue}mode{/autoblue}'),
                    Color('{autoblue}mount targets{/autoblue}')
                    ]
    fs_ids = list()
    for fs in filesystems:
        size_in_bytes = fs.get('SizeInBytes')
        size_in_bytes_value = size_in_bytes.get('Value')
        if size_in_bytes_value:
            size_in_bytes_value = humanize.naturalsize(size_in_bytes_value)
        size_in_bytes_timestamp = size_in_bytes.get('Timestamp')
        if size_in_bytes_timestamp:
            size_in_bytes_timestamp = size_in_bytes_timestamp.replace(tzinfo=None, second=0)
        created_time = fs.get('CreationTime')
        if created_time:
            created_time = created_time.replace(tzinfo=None, second=0)

        td.append([fs.get('FileSystemId'),
                   dash_if_none(fs.get('Name')),
                   colour_state(fs.get('LifeCycleState')),
                   '{0} / {1}'.format(size_in_bytes_value,
                                      dash_if_none(size_in_bytes_timestamp)),
                   fs.get('PerformanceMode'),
                   dash_if_none(fs.get('NumberOfMountTargets'))
                   ])
        fs_ids.append(fs.get('FileSystemId'))
    output_ascii_table_list(table_title=Color('{autowhite}EFS Filesystems{/autowhite}'),
                            table_data=td,
                            table_header=table_header,
                            inner_heading_row_border=True)
    # Output mount targets
    td = list()
    table_header = [Color('{autoblue}mount target id{/autoblue}'),
                    Color('{autoblue}filesystem id{/autoblue}'),
                    Color('{autoblue}lifecycle state{/autoblue}')
                    ]
    for mt in mount_targets:
        td.append([mt.get('MountTargetId'),
                   mt.get('FileSystemId'),
                   colour_state(mt.get('LifeCycleState'))
                   ])
    output_ascii_table_list(table_title=Color('{autowhite}EFS Mount Targets{/autowhite}'),
                            table_data=td,
                            table_header=table_header,
                            inner_heading_row_border=True)
    exit(0)


def output_dict(dict_=None):
    """
    @type dict_: dict
    """
    output = list()
    for k, v in iteritems(dict_):
        output.append('{0}: {1}\n'.format(k, str(v)))
    return ''.join(output).rstrip()


def colour_created(state=None):
    if not state:
        return Color('{autoyellow}False{/autoyellow}')
    else:
        return Color('{autogreen}True{/autogreen}')


def colour_deleted(state=None):
    if not state:
        return Color('{autogreen}False{/autogreen}')
    else:
        return Color('{autored}True{/autored}')


def colour_processing(state=None):
    if not state:
        return Color('{autogreen}False{/autogreen}')
    else:
        return Color('{autoyellow}True{/autoyellow}')


def output_filesystem_info(filesystem=None, mount_targets=None):
    """
    @type filesystem: dict
    @type mount_targets: list
    """
    if filesystem:
        filesystem_details = filesystem.get('FileSystems')[0]
        td = list()
        td.append([Color('{autoblue}filesystem name{/autoblue}'),
                   dash_if_none(filesystem_details.get('Name'))])
        td.append([Color('{autoblue}id{/autoblue}'),
                   filesystem_details.get('FileSystemId')])
        td.append([Color('{autoblue}size{/autoblue}'),
                   filesystem_details['SizeInBytes']['Value']])
        td.append([Color('{autoblue}owner id{/autoblue}'),
                   dash_if_none(filesystem_details.get('OwnerId'))])
        td.append([Color('{autoblue}creation time{/autoblue}'),
                   dash_if_none(filesystem_details.get('CreationTime'))])
        td.append([Color('{autoblue}lifecycle state{/autoblue}'),
                   dash_if_none(filesystem_details.get('LifeCycleState'))])
        td.append([Color('{autoblue}no. mount targets{/autoblue}'),
                   dash_if_none(filesystem_details.get('NumberOfMountTargets'))])
        td.append([Color('{autoblue}performance mode{/autoblue}'),
                   dash_if_none(filesystem_details.get('PerformanceMode'))])
        td.append([Color('{autoblue}creation token{/autoblue}'),
                   dash_if_none(filesystem_details.get('CreationToken'))])
        output_ascii_table(table_title=Color('{autowhite}EFS filesystem info{/autowhite}'),
                           table_data=td)
    else:
        exit('filesystem does not exist.')

    if mount_targets:
        table_header = [Color('{autoblue}mount target id{/autoblue}'),
                        Color('{autoblue}filesystem id{/autoblue}'),
                        Color('{autoblue}lifecycle state{/autoblue}'),
                        Color('{autoblue}ip address{/autoblue}'),
                        Color('{autoblue}subnet id{/autoblue}'),
                        Color('{autoblue}interface id{/autoblue}'),
                        Color('{autoblue}owner id{/autoblue}')
                        ]
        td = list()
        for mt in mount_targets:
            td.append([mt.get('MountTargetId'),
                       mt.get('FileSystemId'),
                       colour_state(mt.get('LifeCycleState')),
                       mt.get('IpAddress'),
                       mt.get('SubnetId'),
                       mt.get('NetworkInterfaceId'),
                       mt.get('OwnerId')
                       ])
        output_ascii_table_list(table_title=Color('{autowhite}EFS Mount Targets{/autowhite}'),
                                table_header=table_header,
                                table_data=td,
                                inner_heading_row_border=True)
    exit(0)
