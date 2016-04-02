# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)

from colorclass import Color, Windows

from acli.output import (output_ascii_table_list, dash_if_none)

Windows.enable(auto_colors=True, reset_atexit=True)


def colour_state(state=None):
    if not state:
        return Color('{autoblack}-{/autoblack}')
    elif state == 'running':
        return Color('{autogreen}' + state + '{/autogreen}')
    elif state in ('stopped', 'stopping', 'shutting-down', 'terminated'):
        return Color('{autored}' + state + '{/autored}')
    elif state in ('rebooting', 'pending'):
        return Color('{autoyellow}' + state + '{/autoyellow}')


def output_snapshot_list(snapshots=None):
    """
    @type snapshots: list
    """
    td = list()
    table_header = [Color('{autoblue}name{/autoblue}'),
                    Color('{autoblue}id{/autoblue}'),
                    Color('{autoblue}size (GiB){/autoblue}'),
                    Color('{autoblue}description{/autoblue}'),
                    Color('{autoblue}status{/autoblue}'),
                    Color('{autoblue}started{/autoblue}'),
                    Color('{autoblue}progress{/autoblue}'),
                    Color('{autoblue}encrypted{/autoblue}')]
    for snapshot in snapshots:
        td.append([dash_if_none(snapshot.get('Tags')),
                   dash_if_none(snapshot.get('SnapshotId')),
                   dash_if_none(snapshot.get('VolumeSize')),
                   dash_if_none(snapshot.get('Description')),
                   dash_if_none(snapshot.get('State')),
                   dash_if_none(snapshot.get('StartTime (UTC)')),
                   dash_if_none(snapshot.get('Progress')),
                   str(snapshot.get('Encrypted'))])
    output_ascii_table_list(table_title=Color('{autowhite}orphaned snapshots{/autowhite}'),
                            table_data=td,
                            table_header=table_header,
                            inner_heading_row_border=True)
    exit(0)
