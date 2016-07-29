# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)

import humanize
from colorclass import Color, Windows
from external.six import iteritems

from acli.output import (output_ascii_table, output_ascii_table_list, dash_if_none)

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


def output_filesystems(filesystems=None):
    """
    @type filesystems: dict
    """
    td = list()
    table_header = [Color('{autoblue}id{/autoblue}'),
                    Color('{autoblue}owner id{/autoblue}'),
                    Color('{autoblue}name{/autoblue}'),
                    Color('{autoblue}state{/autoblue}'),
                    Color('{autoblue}size / time (UTC){/autoblue}'),
                    Color('{autoblue}mode{/autoblue}'),
                    Color('{autoblue}mount targets{/autoblue}'),
                    Color('{autoblue}created (UTC){/autoblue}')
                    ]
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
                   fs.get('OwnerId'),
                   fs.get('Name'),
                   colour_state(fs.get('LifeCycleState')),
                   '{0} / {1}'.format(size_in_bytes_value,
                                      dash_if_none(size_in_bytes_timestamp)),
                   fs.get('PerformanceMode'),
                   fs.get('NumberOfMountTargets'),
                   dash_if_none(created_time)
                   ])
    output_ascii_table_list(table_title=Color('{autowhite}EFS{/autowhite}'),
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


def output_filesystem_info(domain=None):
    """
    @type domain: dict
    """
    if domain:
        domain_details = domain.get('DomainStatusList')[0]
        cluster_conf = domain_details.get('ElasticsearchClusterConfig')
        td = list()
        td.append([Color('{autoblue}domain name{/autoblue}'),
                   domain_details.get('DomainName')])
        td.append([Color('{autoblue}endpoint{/autoblue}'),
                   domain_details.get('Endpoint')])
        td.append([Color('{autoblue}created{/autoblue}'),
                   colour_created(domain_details.get('Created'))])
        td.append([Color('{autoblue}deleted{/autoblue}'),
                   colour_deleted(domain_details.get('Deleted'))])
        td.append([Color('{autoblue}processing{/autoblue}'),
                   colour_processing(domain_details.get('Processing'))])
        td.append([Color('{autoblue}cluster config{/autoblue}'),
                   ' '])
        td.append([Color('{autoblue} dedicated master enabled{/autoblue}'),
                   str(cluster_conf.get('DedicatedMasterEnabled'))])
        td.append([Color('{autoblue} instance type{/autoblue}'),
                   str(cluster_conf.get('InstanceType'))])
        td.append([Color('{autoblue} instance count{/autoblue}'),
                   str(cluster_conf.get('InstanceCount'))])
        td.append([Color('{autoblue} zone awareness{/autoblue}'),
                   str(cluster_conf.get('ZoneAwarenessEnabled'))])
        td.append([Color('{autoblue}domain id{/autoblue}'),
                   domain_details.get('DomainId')])
        td.append([Color('{autoblue}snapshot options{/autoblue}'),
                   output_dict(domain_details.get('SnapshotOptions'))])
        td.append([Color('{autoblue}advanced options{/autoblue}'),
                   output_dict(domain_details.get('AdvancedOptions'))])
        td.append([Color('{autoblue}ARN{/autoblue}'),
                   domain_details.get('ARN')])
        output_ascii_table(table_title=Color('{autowhite}ES domain info{/autowhite}'),
                           table_data=td)
    else:
        exit('Domain does not exist.')
    exit(0)
