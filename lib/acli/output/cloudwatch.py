# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)


def output_ec2_cpu(dates=None, values=None,
                   instance_id=None, output_type=None):
    """
    @type dates: list
    @type values: list
    @type instance_id: unicode
    @type output_type: unicode
    """
    try:
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
    except ImportError:
        exit('matplotlib required to output graphs.')
    if output_type in ('graph', None):
        plt.subplots_adjust(bottom=0.2)
        plt.xticks(rotation=25)
        ax = plt.gca()
        xfmt = mdates.DateFormatter('%Y-%m-%d %H:%M:%S')
        ax.xaxis.set_major_formatter(xfmt)
        plt.plot(dates, values)
        plt.gcf().autofmt_xdate()
        plt.title('CPU statistics for: {0}'.format(instance_id))
        plt.xlabel('Time (UTC)')
        plt.ylabel('CPU %')
        plt.grid(True)
        plt.ylim([0, 100])
        plt.show()
    exit(0)


def output_ec2_mem(dates=None, values=None, instance_id=None, output_type=None):
    """
    @type dates: list
    @type values: list
    @type instance_id: unicode
    @type output_type: unicode
    """
    try:
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
    except ImportError:
        exit('matplotlib required to output graphs.')
    if output_type in ('graph', None):
        plt.subplots_adjust(bottom=0.2)
        plt.xticks(rotation=25)
        ax = plt.gca()
        xfmt = mdates.DateFormatter('%Y-%m-%d %H:%M:%S')
        ax.xaxis.set_major_formatter(xfmt)
        plt.plot(dates, values)
        plt.gcf().autofmt_xdate()
        plt.title(' Memory usage for: {0}'.format(instance_id))
        plt.xlabel('Time (UTC)')
        plt.ylabel('Memory Usage %')
        plt.grid(True)
        plt.show()
    exit(0)


def output_ec2_net(in_dates=None, in_values=None, out_dates=None,
                   out_values=None, instance_id=None, output_type=None):
    """
    @type in_dates: list
    @type in_values: list
    @type out_dates: list
    @type out_values: list
    @type instance_id: unicode
    @type output_type: unicode
    """
    try:
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
    except ImportError:
        exit('matplotlib required to output graphs.')
    if output_type in ('graph', None):
        plt.subplots_adjust(bottom=0.2)
        plt.xticks(rotation=25)
        ax = plt.gca()
        xfmt = mdates.DateFormatter('%Y-%m-%d %H:%M:%S')
        ax.xaxis.set_major_formatter(xfmt)
        in_line = plt.plot(in_dates, in_values)
        out_line = plt.plot(out_dates, out_values)
        plt.setp(in_line, color='g', linewidth=2.0, label='inbound')
        plt.setp(out_line, color='b', linewidth=2.0, label='outbound')
        plt.gcf().autofmt_xdate()
        plt.title('Network statistics for: {0}'.format(instance_id))
        plt.xlabel('Time (UTC)')
        plt.ylabel('Network (Bytes/s)')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles, labels)
        plt.subplots_adjust(bottom=0.2)
        plt.xticks(rotation=25)
        plt.grid()
        plt.show()
        exit(0)


def output_ec2_vols(vols_datapoints=None, instance_id=None, output_type=None):
    """
    @type vols_datapoints: list
    @type instance_id: unicode
    @type output_type: unicode
    """
    try:
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
    except ImportError:
        exit('matplotlib required to output graphs.')
    try:
        import numpy as np
    except ImportError:
        exit('install numpy.')
    if output_type in ('graph', None):
        num_plots = len(vols_datapoints)
        f, axarr = plt.subplots(num_plots, sharex=True, sharey=True)
        f.suptitle('Volumes for instance: {0}'.format(instance_id), fontsize=16)
        plt.ylabel('Bytes')
        if isinstance(axarr, np.ndarray):
            for index, vol_set in enumerate(vols_datapoints):
                read_dates = vol_set.get('read_dates')
                read_values = vol_set.get('read_values')
                write_dates = vol_set.get('write_dates')
                write_values = vol_set.get('write_values')
                axarr[index].set_title(vol_set.get('device_name'))
                axarr[index].grid(True)
                axarr[index].plot(write_dates, write_values, label='write')
                axarr[index].plot(read_dates, read_values, label='read')
                axarr[index].legend(loc="upper right",
                                    title=None,
                                    fancybox=False)
            plt.subplots_adjust(bottom=0.2)
            plt.xticks(rotation=25)
            plt.xlabel('Time (UTC)')
        else:
            read_dates = vols_datapoints[0].get('read_dates')
            read_values = vols_datapoints[0].get('read_values')
            write_dates = vols_datapoints[0].get('write_dates')
            write_values = vols_datapoints[0].get('write_values')
            axarr.set_title(vols_datapoints[0].get('device_name'))
            axarr.plot(write_dates, write_values, label='write')
            axarr.plot(read_dates, read_values, label='read')
            axarr.legend(loc="upper right",
                         title=None,
                         fancybox=False)
            axarr.grid(True)
            plt.subplots_adjust(bottom=0.2)
            plt.xticks(rotation=25)
            plt.xlabel('Time (UTC)')
        ax = plt.gca()
        ax.set_ylim(bottom=0)
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles, labels)
        xfmt = mdates.DateFormatter('%Y-%m-%d %H:%M:%S')
        ax.xaxis.set_major_formatter(xfmt)
        plt.grid(True)
        plt.show()
        exit(0)


def output_asg_cpu(dates=None, values=None,
                   asg_name=None, output_type=None):
    """
    @type dates: list
    @type values: list
    @type asg_name: unicode
    @type output_type: unicode
    """
    try:
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
    except ImportError:
        exit('matplotlib required to output graphs.')
    if output_type in ('graph', None):
        plt.subplots_adjust(bottom=0.2)
        plt.xticks(rotation=25)
        ax = plt.gca()
        xfmt = mdates.DateFormatter('%Y-%m-%d %H:%M:%S')
        ax.xaxis.set_major_formatter(xfmt)
        plt.plot(dates, values)
        plt.gcf().autofmt_xdate()
        plt.title('CPU statistics for: {0}'.format(asg_name))
        plt.xlabel('Time (UTC)')
        plt.ylabel('CPU %')
        plt.grid()
        plt.ylim([0, 100])
        plt.show()
        exit(0)
