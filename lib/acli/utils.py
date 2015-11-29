# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)
import sys
import os
import platform
import base64


BASH_COMPLETION_SCRIPT = "TBC"
BASH_COMPLETION_PATH_OSX = "/usr/local/etc/bash_completion.d"
BASH_COMPLETION_PATH_LINUX = "/etc/bash_completion.d"


def install_completion():
    if platform.system() == 'Darwin':
        if os.path.exists(BASH_COMPLETION_PATH_OSX):
            with open("{0}/acli".format(BASH_COMPLETION_PATH_OSX), 'w') as acli_file:
                acli_file.write(base64.b64decode(BASH_COMPLETION_SCRIPT))
            sys.exit("bash completion script written to: {0}/acli\nrestart terminal to use.".format(
                BASH_COMPLETION_PATH_OSX)
            )
        else:
            sys.exit("bash completion not installed. try 'brew install bash-completion'.")
    elif platform.system() == 'Linux':
        if os.path.exists(BASH_COMPLETION_PATH_LINUX):
            with open("{0}/acli".format(BASH_COMPLETION_PATH_LINUX), 'w') as acli_file:
                acli_file.write(base64.b64decode(BASH_COMPLETION_SCRIPT))
            sys.exit("bash completion script written to: {0}/acli\nrestart terminal to use.".format(
                BASH_COMPLETION_PATH_LINUX)
            )
        else:
            sys.exit("bash completion not installed.")

    else:
        sys.exit("Shell completion only available on Linux and OS X.")


def get_console_dimensions():
    try:
        rows, columns = os.popen('stty size', 'r').read().split()
    except ValueError:
        rows, columns = 80, 25
    return rows, columns


def is_readable(path=None):
    """Test if the supplied filesystem path can be read
    :param path: A filesystem path
    :return: True if the path is a file that can be read. Otherwise, False.
    """
    if os.path.isfile(path) and os.access(path, os.R_OK):
        return True
    return False


def is_writeable(path=None):
    """Test if the supplied filesystem path can be written to
    :param path: A filesystem path
    :return: True if the path is a file that can be written. Otherwise, False.
    """
    if os.path.isfile(path) and os.access(path, os.W_OK):
        return True


def get_tag_value(name=None, tags=None):
    if tags:
        for tag in tags:
            if tag.get('Key') == name:
                return tag.get('Value')
